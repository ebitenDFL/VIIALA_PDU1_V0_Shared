#!/usr/bin/env python3
"""CANopen transport and data model for the VIIALA PDU desktop GUI."""

from __future__ import annotations

import hashlib
import os
import struct
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

import can
import canopen


MCUBOOT_MAGIC = 0x96F3B83D
MAX_ACTIVE_IMAGE_SIZE = 64 * 1024
OUTPUT_COUNT = 15

NMT_NAMES = {
    0x00: "Boot-up",
    0x04: "Stopped",
    0x05: "Operational",
    0x7F: "Pre-operational",
}


def decode_u(data: bytes) -> int:
    """Decode a little-endian unsigned CANopen scalar."""
    return int.from_bytes(data, "little", signed=False)


def decode_i(data: bytes) -> int:
    """Decode a little-endian signed CANopen scalar."""
    return int.from_bytes(data, "little", signed=True)


def decode_text(data: bytes) -> str:
    """Decode a CANopen visible string."""
    return data.rstrip(b"\0").decode("ascii", errors="replace")


def inspect_update_image(path: str | os.PathLike[str]) -> dict[str, object]:
    """Validate the basic MCUboot container shape before transmission."""
    image_path = Path(path)
    data = image_path.read_bytes()
    if len(data) < 32:
        raise ValueError("Image is too small to contain an MCUboot header")
    magic = struct.unpack_from("<I", data, 0)[0]
    if magic != MCUBOOT_MAGIC:
        raise ValueError("File does not begin with an MCUboot image header")
    if len(data) > MAX_ACTIVE_IMAGE_SIZE:
        raise ValueError(
            f"Image is {len(data):,} bytes; active slot limit is "
            f"{MAX_ACTIVE_IMAGE_SIZE:,} bytes"
        )
    identities = [token.decode("ascii") for token in (b"A001", b"B001") if token in data]
    return {
        "path": str(image_path),
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "identity": identities[0] if len(identities) == 1 else "unknown",
    }


@dataclass
class PduSnapshot:
    timestamp: float = field(default_factory=time.time)
    device_name: str = "—"
    hardware_version: str = "—"
    software_version: str = "—"
    nmt_state: str = "Unknown"
    heartbeat_age_s: Optional[float] = None
    error_register: int = 0
    output_states: int = 0
    output_commanded: int = 0
    output_faults: int = 0
    overcurrent_faults: int = 0
    open_load_faults: int = 0
    output_disabled: int = 0
    output_request: int = 0
    pending_node_id: int = 10
    pending_bitrate_kbps: int = 500
    communication_apply: int = 0
    total_current_ma: int = 0xFFFFFFFF
    supply_voltage_mv: int = 0xFFFF
    board_temperature_dc: int = 0x7FFF
    mcu_temperature_dc: int = 0x7FFF
    uptime_s: int = 0
    reset_reason: int = 0xFFFF
    brownout_count: int = 0
    can_busoff_count: int = 0
    warning_flags: int = 0
    telemetry_validity: int = 0
    program_control: int = 0
    flash_status: int = 0
    currents_ma: list[int] = field(default_factory=lambda: [0xFFFF] * OUTPUT_COUNT)
    raw_adc: list[int] = field(default_factory=lambda: [0xFFFF] * OUTPUT_COUNT)
    peak_currents_ma: list[int] = field(default_factory=lambda: [0xFFFF] * OUTPUT_COUNT)
    trip_counts: list[int] = field(default_factory=lambda: [0] * OUTPUT_COUNT)
    current_limits_ma: list[int] = field(default_factory=lambda: [5000] * OUTPUT_COUNT)
    current_trip_times_ms: list[int] = field(default_factory=lambda: [100] * OUTPUT_COUNT)
    inrush_limits_ma: list[int] = field(default_factory=lambda: [8000] * OUTPUT_COUNT)
    inrush_times_ms: list[int] = field(default_factory=lambda: [500] * OUTPUT_COUNT)
    read_errors: list[str] = field(default_factory=list)


class _FrameListener(can.Listener):
    def __init__(self, client: "PduCanClient") -> None:
        self.client = client

    def on_message_received(self, message: can.Message) -> None:
        self.client._on_frame(message)


class PduCanClient:
    """Thread-confined CANopen client with a passive raw-frame observer."""

    def __init__(
        self,
        channel: str = "can0",
        node_id: int = 10,
        frame_callback: Optional[Callable[[str], None]] = None,
    ) -> None:
        self.channel = channel
        self.node_id = node_id
        self.frame_callback = frame_callback
        self.network: Optional[canopen.Network] = None
        self.node = None
        self.raw_bus: Optional[can.BusABC] = None
        self.notifier: Optional[can.Notifier] = None
        self.connected = False
        self.last_heartbeat_monotonic: Optional[float] = None
        self.nmt_code: Optional[int] = None
        self._frame_lock = threading.Lock()

    def connect(self) -> None:
        if self.connected:
            return
        network = canopen.Network()
        network.connect(interface="socketcan", channel=self.channel)
        node = network.add_node(self.node_id, None)
        node.sdo.RESPONSE_TIMEOUT = 2.0
        node.sdo.MAX_RETRIES = 2

        raw_bus = can.Bus(interface="socketcan", channel=self.channel)
        notifier = can.Notifier(raw_bus, [_FrameListener(self)], timeout=1.0)

        self.network = network
        self.node = node
        self.raw_bus = raw_bus
        self.notifier = notifier
        self.connected = True

    def disconnect(self) -> None:
        self.connected = False
        if self.notifier is not None:
            self.notifier.stop()
            self.notifier = None
        if self.raw_bus is not None:
            self.raw_bus.shutdown()
            self.raw_bus = None
        if self.network is not None:
            self.network.disconnect()
            self.network = None
        self.node = None

    def _on_frame(self, message: can.Message) -> None:
        cob_id = message.arbitration_id
        if cob_id == 0x700 + self.node_id and message.data:
            with self._frame_lock:
                self.last_heartbeat_monotonic = time.monotonic()
                self.nmt_code = message.data[0]

        relevant = {
            0x080 + self.node_id,
            0x180 + self.node_id,
            0x280 + self.node_id,
            0x380 + self.node_id,
            0x480 + self.node_id,
            0x580 + self.node_id,
            0x600 + self.node_id,
            0x700 + self.node_id,
        }
        if self.frame_callback is not None and cob_id in relevant:
            timestamp = time.strftime("%H:%M:%S")
            direction = "RTR" if message.is_remote_frame else message.data.hex(" ").upper()
            self.frame_callback(f"{timestamp}  {cob_id:03X}  [{message.dlc}]  {direction}")

    def _require_node(self):
        if not self.connected or self.node is None:
            raise RuntimeError("Not connected to the PDU")
        return self.node

    def upload(self, index: int, subindex: int = 0) -> bytes:
        return self._require_node().sdo.upload(index, subindex)

    def download(self, index: int, subindex: int, data: bytes) -> None:
        self._require_node().sdo.download(index, subindex, data)

    def _read(self, snapshot: PduSnapshot, index: int, subindex: int, decoder, default):
        try:
            return decoder(self.upload(index, subindex))
        except Exception as exc:  # Keep a partial dashboard alive.
            snapshot.read_errors.append(f"0x{index:04X}:{subindex:02X} {exc}")
            return default

    def read_snapshot(self, include_channels: bool = True) -> PduSnapshot:
        snap = PduSnapshot()
        with self._frame_lock:
            if self.last_heartbeat_monotonic is not None:
                snap.heartbeat_age_s = time.monotonic() - self.last_heartbeat_monotonic
            if self.nmt_code is not None:
                snap.nmt_state = NMT_NAMES.get(self.nmt_code, f"0x{self.nmt_code:02X}")

        text_items = (
            ("device_name", 0x1008),
            ("hardware_version", 0x1009),
            ("software_version", 0x100A),
        )
        for attr, index in text_items:
            setattr(snap, attr, self._read(snap, index, 0, decode_text, "—"))

        scalars = (
            ("error_register", 0x1001, 0, decode_u, 0),
            ("output_states", 0x2000, 0, decode_u, 0),
            ("output_commanded", 0x2001, 0, decode_u, 0),
            ("output_faults", 0x2002, 0, decode_u, 0),
            ("overcurrent_faults", 0x2003, 0, decode_u, 0),
            ("open_load_faults", 0x2004, 0, decode_u, 0),
            ("output_disabled", 0x2005, 0, decode_u, 0),
            ("output_request", 0x2103, 0, decode_u, 0),
            ("pending_node_id", 0x2105, 0, decode_u, self.node_id),
            ("pending_bitrate_kbps", 0x2106, 0, decode_u, 500),
            ("communication_apply", 0x2107, 0, decode_u, 0),
            ("total_current_ma", 0x2006, 0, decode_u, 0xFFFFFFFF),
            ("supply_voltage_mv", 0x2007, 0, decode_u, 0xFFFF),
            ("board_temperature_dc", 0x2008, 0, decode_i, 0x7FFF),
            ("mcu_temperature_dc", 0x2009, 0, decode_i, 0x7FFF),
            ("uptime_s", 0x200A, 0, decode_u, 0),
            ("reset_reason", 0x200B, 0, decode_u, 0xFFFF),
            ("brownout_count", 0x200C, 0, decode_u, 0),
            ("can_busoff_count", 0x200D, 0, decode_u, 0),
            ("warning_flags", 0x200E, 0, decode_u, 0),
            ("telemetry_validity", 0x200F, 0, decode_u, 0),
            ("program_control", 0x1F51, 1, decode_u, 0),
            ("flash_status", 0x1F57, 1, decode_u, 0),
        )
        for attr, index, subindex, decoder, default in scalars:
            setattr(snap, attr, self._read(snap, index, subindex, decoder, default))

        if include_channels:
            arrays = (
                ("currents_ma", 0x3000, 0xFFFF),
                ("raw_adc", 0x3001, 0xFFFF),
                ("peak_currents_ma", 0x3002, 0xFFFF),
                ("trip_counts", 0x3003, 0),
                ("current_limits_ma", 0x3100, 5000),
                ("current_trip_times_ms", 0x3101, 100),
                ("inrush_limits_ma", 0x3102, 8000),
                ("inrush_times_ms", 0x3103, 500),
            )
            for attr, index, default in arrays:
                values = [
                    self._read(snap, index, channel, decode_u, default)
                    for channel in range(1, OUTPUT_COUNT + 1)
                ]
                setattr(snap, attr, values)
        return snap

    def send_nmt(self, state: str) -> None:
        node = self._require_node()
        node.nmt.state = state

    def firmware_update(
        self,
        image_path: str,
        progress: Callable[[int, int, str], None],
    ) -> str:
        """Stage, activate and confirm a signed MCUboot image over CANopen."""
        info = inspect_update_image(image_path)
        node = self._require_node()
        total = int(info["size"])
        old_timeout = node.sdo.RESPONSE_TIMEOUT
        old_retries = node.sdo.MAX_RETRIES
        node.sdo.RESPONSE_TIMEOUT = 10.0
        node.sdo.MAX_RETRIES = 3
        try:
            progress(0, total, "Entering Pre-operational")
            node.nmt.state = "PRE-OPERATIONAL"
            self.download(0x1F51, 1, b"\x00")  # stop
            progress(0, total, "Erasing the 128 KiB staging sector")
            self.download(0x1F51, 1, b"\x03")  # clear
            flash_status = decode_u(self.upload(0x1F57, 1))
            if flash_status != 0:
                raise RuntimeError(f"Staging erase failed, flash status 0x{flash_status:08X}")

            progress(0, total, "Transferring signed image")
            sent = 0
            with open(image_path, "rb") as infile:
                with node.sdo.open(0x1F50, 1, "wb", buffering=1024, size=total) as outfile:
                    while True:
                        chunk = infile.read(512)
                        if not chunk:
                            break
                        outfile.write(chunk)
                        sent += len(chunk)
                        progress(sent, total, "Transferring signed image")

            flash_status = decode_u(self.upload(0x1F57, 1))
            if flash_status != 0:
                raise RuntimeError(f"Download failed, flash status 0x{flash_status:08X}")

            progress(total, total, "Activating image through MCUboot")
            self.download(0x1F51, 1, b"\x01")
            node.nmt.wait_for_bootup(timeout=45.0)
            identity = decode_text(self.upload(0x100A, 0))
            node.nmt.state = "PRE-OPERATIONAL"
            if decode_u(self.upload(0x1F51, 1)) == 0x80:
                self.download(0x1F51, 1, b"\x80")
            progress(total, total, f"Update complete: {identity}")
            return identity
        finally:
            node.sdo.RESPONSE_TIMEOUT = old_timeout
            node.sdo.MAX_RETRIES = old_retries
