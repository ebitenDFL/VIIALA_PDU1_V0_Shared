#!/usr/bin/env python3
"""VIIALA PDU Linux CANopen dashboard."""

from __future__ import annotations

import queue
import subprocess
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from pdu_can import OUTPUT_COUNT, PduCanClient, PduSnapshot, decode_text, decode_u, inspect_update_image


BG = "#101419"
PANEL = "#182028"
PANEL_2 = "#202A34"
TEXT = "#E8EEF3"
MUTED = "#8FA1AF"
ACCENT = "#34D399"
BLUE = "#60A5FA"
WARN = "#FBBF24"
ERROR = "#F87171"


def fmt_duration(seconds: int) -> str:
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, secs = divmod(remainder, 60)
    prefix = f"{days}d " if days else ""
    return f"{prefix}{hours:02d}:{minutes:02d}:{secs:02d}"


def fmt_unknown(value: int, unknown: int, suffix: str = "") -> str:
    return "—" if value == unknown else f"{value:,}{suffix}"


class PduGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("VIIALA_PDU1_V0 · CANopen Workbench")
        self.root.geometry("1280x850")
        self.root.minsize(1080, 700)
        self.root.configure(bg=BG)

        self.events: queue.Queue = queue.Queue(maxsize=4000)
        self.commands: queue.Queue = queue.Queue()
        self.stop_event = threading.Event()
        self.client: PduCanClient | None = None
        self.connected = False
        self.updating = False
        self.last_snapshot: PduSnapshot | None = None
        self.selected_image = ""

        self.channel = tk.StringVar(value="can0")
        self.node_id = tk.IntVar(value=10)
        self.connection_text = tk.StringVar(value="DISCONNECTED")
        self.status_text = tk.StringVar(value="Connect to the PEAK adapter to begin.")
        self.device_text = tk.StringVar(value="—")
        self.version_text = tk.StringVar(value="—")
        self.nmt_text = tk.StringVar(value="Unknown")
        self.heartbeat_text = tk.StringVar(value="No heartbeat")
        self.uptime_text = tk.StringVar(value="—")
        self.output_text = tk.StringVar(value="0 / 15 active")
        self.current_text = tk.StringVar(value="—")
        self.voltage_text = tk.StringVar(value="—")
        self.temperature_text = tk.StringVar(value="—")
        self.health_text = tk.StringVar(value="Waiting for data")
        self.update_file_text = tk.StringVar(value="No signed image selected")
        self.update_progress_text = tk.StringVar(value="Idle")
        self.sdo_index = tk.StringVar(value="100A")
        self.sdo_subindex = tk.StringVar(value="00")
        self.sdo_result = tk.StringVar(value="—")
        self.sdo_write_data = tk.StringVar(value="")
        self.selected_channel = tk.IntVar(value=1)
        self.limit_amps = tk.StringVar(value="5.0")
        self.trip_time_ms = tk.StringVar(value="100")
        self.inrush_amps = tk.StringVar(value="8.0")
        self.inrush_time_ms = tk.StringVar(value="500")
        self.pending_node_id = tk.IntVar(value=10)
        self.pending_bitrate = tk.IntVar(value=500)

        self._configure_style()
        self._build_ui()
        self.worker = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker.start()
        self.root.after(100, self._tick)
        self.root.protocol("WM_DELETE_WINDOW", self._close)

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(".", background=BG, foreground=TEXT, fieldbackground=PANEL_2)
        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("Card.TFrame", background=PANEL_2)
        style.configure("TLabel", background=BG, foreground=TEXT)
        style.configure("Panel.TLabel", background=PANEL, foreground=TEXT)
        style.configure("Active.Panel.TLabel", background=PANEL, foreground=ACCENT)
        style.configure("Fault.Panel.TLabel", background=PANEL, foreground=ERROR)
        style.configure("Card.TLabel", background=PANEL_2, foreground=TEXT)
        style.configure("Muted.TLabel", background=BG, foreground=MUTED)
        style.configure("PanelMuted.TLabel", background=PANEL, foreground=MUTED)
        style.configure("Title.TLabel", font=("DejaVu Sans", 22, "bold"), foreground=TEXT)
        style.configure("Hero.TLabel", background=PANEL_2, font=("DejaVu Sans", 20, "bold"), foreground=TEXT)
        style.configure("CardTitle.TLabel", background=PANEL_2, font=("DejaVu Sans", 9), foreground=MUTED)
        style.configure("Accent.TButton", background=ACCENT, foreground="#07120D", padding=(14, 8))
        style.map("Accent.TButton", background=[("active", "#6EE7B7"), ("disabled", "#33443D")])
        style.configure("TButton", background=PANEL_2, foreground=TEXT, padding=(10, 7))
        style.map("TButton", background=[("active", "#2C3945")])
        style.configure("Small.TButton", background=PANEL_2, foreground=TEXT, padding=(7, 3))
        style.configure("On.Small.TButton", background=ACCENT, foreground="#07120D", padding=(7, 3))
        style.map("On.Small.TButton", background=[("active", "#6EE7B7"), ("disabled", "#33443D")])
        style.configure("Off.Small.TButton", background="#334155", foreground=TEXT, padding=(7, 3))
        style.map("Off.Small.TButton", background=[("active", "#475569")])
        style.configure("Reset.Small.TButton", background="#78350F", foreground=TEXT, padding=(7, 3))
        style.map("Reset.Small.TButton", background=[("active", "#92400E")])
        style.configure("TEntry", fieldbackground=PANEL_2, foreground=TEXT, insertcolor=TEXT)
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=PANEL, foreground=MUTED, padding=(16, 9))
        style.map("TNotebook.Tab", background=[("selected", PANEL_2)], foreground=[("selected", TEXT)])
        style.configure("Treeview", background=PANEL, fieldbackground=PANEL, foreground=TEXT, rowheight=29)
        style.configure("Treeview.Heading", background=PANEL_2, foreground=TEXT, relief="flat")
        style.map("Treeview", background=[("selected", "#27465B")])
        style.configure("Horizontal.TProgressbar", troughcolor=PANEL_2, background=ACCENT)

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer)
        header.pack(fill="x", pady=(0, 14))
        title_box = ttk.Frame(header)
        title_box.pack(side="left")
        ttk.Label(title_box, text="VIIALA_PDU1_V0", style="Title.TLabel").pack(anchor="w")
        ttk.Label(title_box, text="CANopen workbench · monitored output control", style="Muted.TLabel").pack(anchor="w")

        connect_box = ttk.Frame(header)
        connect_box.pack(side="right")
        ttk.Label(connect_box, text="Interface", style="Muted.TLabel").grid(row=0, column=0, padx=4)
        ttk.Entry(connect_box, textvariable=self.channel, width=8).grid(row=0, column=1, padx=4)
        ttk.Label(connect_box, text="Node", style="Muted.TLabel").grid(row=0, column=2, padx=4)
        ttk.Spinbox(connect_box, from_=1, to=127, textvariable=self.node_id, width=5).grid(row=0, column=3, padx=4)
        self.connect_button = ttk.Button(connect_box, text="Connect", style="Accent.TButton", command=self._toggle_connect)
        self.connect_button.grid(row=0, column=4, padx=(10, 0))

        state_bar = ttk.Frame(outer, style="Panel.TFrame", padding=(14, 9))
        state_bar.pack(fill="x", pady=(0, 12))
        self.connection_label = ttk.Label(state_bar, textvariable=self.connection_text, style="Panel.TLabel", font=("DejaVu Sans", 10, "bold"))
        self.connection_label.pack(side="left")
        ttk.Label(state_bar, textvariable=self.status_text, style="PanelMuted.TLabel").pack(side="left", padx=18)
        ttk.Label(state_bar, text="500 kbit/s", style="PanelMuted.TLabel").pack(side="right")

        self.notebook = ttk.Notebook(outer)
        self.notebook.pack(fill="both", expand=True)
        self.overview_tab = ttk.Frame(self.notebook, padding=(0, 14, 0, 0))
        self.channels_tab = ttk.Frame(self.notebook, padding=(0, 14, 0, 0))
        self.tools_tab = ttk.Frame(self.notebook, padding=(0, 14, 0, 0))
        self.traffic_tab = ttk.Frame(self.notebook, padding=(0, 14, 0, 0))
        self.notebook.add(self.overview_tab, text="Overview")
        self.notebook.add(self.channels_tab, text="15 Channels")
        self.notebook.add(self.tools_tab, text="Diagnostics & Update")
        self.notebook.add(self.traffic_tab, text="CAN Traffic")
        self._build_overview()
        self._build_channels()
        self._build_tools()
        self._build_traffic()

    def _card(self, parent, title: str, variable: tk.StringVar, column: int, row: int = 0) -> ttk.Frame:
        card = ttk.Frame(parent, style="Card.TFrame", padding=16)
        card.grid(row=row, column=column, sticky="nsew", padx=5, pady=5)
        ttk.Label(card, text=title.upper(), style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(card, textvariable=variable, style="Hero.TLabel").pack(anchor="w", pady=(7, 0))
        return card

    def _build_overview(self) -> None:
        cards = ttk.Frame(self.overview_tab)
        cards.pack(fill="x")
        variables = (
            ("Device", self.device_text),
            ("Firmware", self.version_text),
            ("CANopen state", self.nmt_text),
            ("Heartbeat", self.heartbeat_text),
            ("Uptime", self.uptime_text),
            ("Outputs", self.output_text),
            ("Total current", self.current_text),
            ("Supply", self.voltage_text),
        )
        for idx, (title, var) in enumerate(variables):
            self._card(cards, title, var, idx % 4, idx // 4)
        for col in range(4):
            cards.columnconfigure(col, weight=1, uniform="cards")

        lower = ttk.Frame(self.overview_tab)
        lower.pack(fill="both", expand=True, pady=(12, 0))
        health = ttk.Frame(lower, style="Panel.TFrame", padding=18)
        health.pack(side="left", fill="both", expand=True, padx=(5, 7))
        ttk.Label(health, text="SYSTEM HEALTH", style="Panel.TLabel", font=("DejaVu Sans", 11, "bold")).pack(anchor="w")
        ttk.Label(health, textvariable=self.health_text, style="Panel.TLabel", font=("DejaVu Sans", 18, "bold"), wraplength=470).pack(anchor="w", pady=(18, 8))
        ttk.Label(health, textvariable=self.temperature_text, style="PanelMuted.TLabel").pack(anchor="w")

        controls = ttk.Frame(lower, style="Panel.TFrame", padding=18)
        controls.pack(side="right", fill="both", expand=True, padx=(7, 5))
        ttk.Label(controls, text="CANOPEN NETWORK", style="Panel.TLabel", font=("DejaVu Sans", 11, "bold")).pack(anchor="w")
        row = ttk.Frame(controls, style="Panel.TFrame")
        row.pack(fill="x", pady=(18, 10))
        for label, state in (("Pre-op", "PRE-OPERATIONAL"), ("Start", "OPERATIONAL"), ("Stop", "STOPPED")):
            ttk.Button(row, text=label, command=lambda value=state: self._send_command("nmt", value)).pack(side="left", expand=True, fill="x", padx=3)
        ttk.Button(controls, text="Reset node", command=self._confirm_reset).pack(fill="x", pady=3)
        ttk.Label(
            controls,
            text="Outputs start OFF and require Operational state, valid current telemetry and an explicit request. Overcurrent trips latch OFF.",
            style="PanelMuted.TLabel",
            wraplength=470,
        ).pack(anchor="w", pady=(18, 0))

    def _build_channels(self) -> None:
        controls = ttk.Frame(self.channels_tab, style="Panel.TFrame", padding=12)
        controls.pack(fill="x", pady=(0, 10))
        labels = (("Output", self.selected_channel, 1, 15), ("Continuous A", self.limit_amps, None, None),
                  ("Trip delay ms", self.trip_time_ms, None, None), ("Inrush A", self.inrush_amps, None, None),
                  ("Inrush time ms", self.inrush_time_ms, None, None))
        for col, (label, variable, low, high) in enumerate(labels):
            ttk.Label(controls, text=label, style="PanelMuted.TLabel").grid(row=0, column=col, sticky="w", padx=4)
            if low is None:
                ttk.Entry(controls, textvariable=variable, width=12).grid(row=1, column=col, padx=4)
            else:
                ttk.Spinbox(controls, from_=low, to=high, textvariable=variable, width=7).grid(row=1, column=col, padx=4)
        ttk.Button(controls, text="Load channel", command=self._load_channel_settings).grid(row=1, column=5, padx=4)
        ttk.Button(controls, text="Save limits", command=self._save_channel_settings).grid(row=1, column=6, padx=4)
        ttk.Button(controls, text="Request ON/OFF", style="Accent.TButton", command=self._toggle_output).grid(row=1, column=7, padx=4)
        ttk.Button(controls, text="Clear fault", command=self._clear_channel_fault).grid(row=1, column=8, padx=4)

        table = ttk.Frame(self.channels_tab, style="Panel.TFrame", padding=(8, 6))
        table.pack(fill="both", expand=True)
        headings = ("Output", "Actual", "Commanded", "Current", "ADC raw", "Peak", "Trips", "Fault", "Direct SDO control")
        weights = (0, 0, 0, 1, 1, 1, 0, 1, 0)
        for col, (heading, weight) in enumerate(zip(headings, weights)):
            ttk.Label(table, text=heading, style="PanelMuted.TLabel", anchor="center").grid(
                row=0, column=col, sticky="ew", padx=4, pady=(0, 5)
            )
            table.columnconfigure(col, weight=weight, minsize=70 if col < 8 else 220)

        self.channel_values: list[dict[str, tk.StringVar]] = []
        self.channel_value_labels: list[list[ttk.Label]] = []
        for channel in range(1, OUTPUT_COUNT + 1):
            variables = {
                "actual": tk.StringVar(value="OFF"),
                "requested": tk.StringVar(value="OFF"),
                "current": tk.StringVar(value="—"),
                "raw": tk.StringVar(value="—"),
                "peak": tk.StringVar(value="—"),
                "trips": tk.StringVar(value="0"),
                "fault": tk.StringVar(value="—"),
            }
            self.channel_values.append(variables)
            ttk.Label(table, text=f"OUT {channel:02d}", style="Panel.TLabel", anchor="center").grid(
                row=channel, column=0, sticky="ew", padx=4, pady=2
            )
            labels = []
            for col, key in enumerate(("actual", "requested", "current", "raw", "peak", "trips", "fault"), start=1):
                label = ttk.Label(table, textvariable=variables[key], style="Panel.TLabel", anchor="center")
                label.grid(row=channel, column=col, sticky="ew", padx=4, pady=2)
                labels.append(label)
            self.channel_value_labels.append(labels)

            actions = ttk.Frame(table, style="Panel.TFrame")
            actions.grid(row=channel, column=8, sticky="e", padx=(8, 2), pady=1)
            ttk.Button(
                actions,
                text="ON",
                style="On.Small.TButton",
                command=lambda selected=channel: self._request_output(selected, True),
            ).pack(side="left", padx=2)
            ttk.Button(
                actions,
                text="OFF",
                style="Off.Small.TButton",
                command=lambda selected=channel: self._request_output(selected, False),
            ).pack(side="left", padx=2)
            ttk.Button(
                actions,
                text="Reset",
                style="Reset.Small.TButton",
                command=lambda selected=channel: self._reset_output(selected),
            ).pack(side="left", padx=2)

    def _build_tools(self) -> None:
        left = ttk.Frame(self.tools_tab, style="Panel.TFrame", padding=18)
        left.pack(side="left", fill="both", expand=True, padx=(0, 7))
        ttk.Label(left, text="SDO INSPECTOR", style="Panel.TLabel", font=("DejaVu Sans", 11, "bold")).pack(anchor="w")
        fields = ttk.Frame(left, style="Panel.TFrame")
        fields.pack(fill="x", pady=(15, 8))
        ttk.Label(fields, text="Index", style="PanelMuted.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Entry(fields, textvariable=self.sdo_index, width=10).grid(row=1, column=0, padx=(0, 8))
        ttk.Label(fields, text="Sub-index", style="PanelMuted.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Entry(fields, textvariable=self.sdo_subindex, width=8).grid(row=1, column=1, padx=(0, 8))
        ttk.Button(fields, text="Read", command=self._read_sdo).grid(row=1, column=2)
        ttk.Label(fields, text="Write bytes (hex, little-endian)", style="PanelMuted.TLabel").grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))
        ttk.Entry(fields, textvariable=self.sdo_write_data, width=25).grid(row=3, column=0, columnspan=2, sticky="ew", padx=(0, 8))
        ttk.Button(fields, text="Write", command=self._write_sdo).grid(row=3, column=2)
        ttk.Label(left, textvariable=self.sdo_result, style="Panel.TLabel", font=("DejaVu Sans Mono", 11), wraplength=510).pack(anchor="w", pady=(10, 22))

        ttk.Label(left, text="COMMUNICATION SETTINGS (VOLATILE)", style="Panel.TLabel", font=("DejaVu Sans", 11, "bold")).pack(anchor="w")
        comm = ttk.Frame(left, style="Panel.TFrame")
        comm.pack(fill="x", pady=(10, 16))
        ttk.Label(comm, text="Node ID", style="PanelMuted.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(comm, from_=1, to=127, textvariable=self.pending_node_id, width=7).grid(row=1, column=0, padx=(0, 8))
        ttk.Label(comm, text="Bitrate kbit/s", style="PanelMuted.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Combobox(comm, values=(125, 250, 500, 1000), textvariable=self.pending_bitrate, width=9, state="readonly").grid(row=1, column=1, padx=(0, 8))
        ttk.Button(comm, text="Apply & reset communication", command=self._apply_communication).grid(row=1, column=2)

        ttk.Label(left, text="DIAGNOSTIC SUMMARY", style="Panel.TLabel", font=("DejaVu Sans", 11, "bold")).pack(anchor="w")
        self.diagnostic_text = tk.Text(left, height=15, bg=PANEL_2, fg=TEXT, insertbackground=TEXT, relief="flat", font=("DejaVu Sans Mono", 10), padx=10, pady=10)
        self.diagnostic_text.pack(fill="both", expand=True, pady=(10, 0))
        self.diagnostic_text.configure(state="disabled")

        right = ttk.Frame(self.tools_tab, style="Panel.TFrame", padding=18)
        right.pack(side="right", fill="both", expand=True, padx=(7, 0))
        ttk.Label(right, text="SIGNED CAN FIRMWARE UPDATE", style="Panel.TLabel", font=("DejaVu Sans", 11, "bold")).pack(anchor="w")
        ttk.Label(
            right,
            text="Bench path: 64 KiB active slot, 128 KiB staging slot, overwrite-only with no rollback.",
            style="PanelMuted.TLabel",
            wraplength=510,
        ).pack(anchor="w", pady=(6, 16))
        ttk.Label(right, textvariable=self.update_file_text, style="Panel.TLabel", wraplength=510).pack(anchor="w", pady=4)
        buttons = ttk.Frame(right, style="Panel.TFrame")
        buttons.pack(fill="x", pady=8)
        ttk.Button(buttons, text="Select signed .bin", command=self._select_image).pack(side="left", expand=True, fill="x", padx=(0, 4))
        self.update_button = ttk.Button(buttons, text="Stage & activate", style="Accent.TButton", command=self._start_update)
        self.update_button.pack(side="right", expand=True, fill="x", padx=(4, 0))
        self.update_progress = ttk.Progressbar(right, mode="determinate", maximum=100)
        self.update_progress.pack(fill="x", pady=(18, 7))
        ttk.Label(right, textvariable=self.update_progress_text, style="PanelMuted.TLabel", wraplength=510).pack(anchor="w")
        ttk.Label(
            right,
            text="The repository currently uses MCUboot's public development key. Replace it before field deployment.",
            style="PanelMuted.TLabel",
            wraplength=510,
        ).pack(anchor="w", side="bottom", pady=(16, 0))

    def _build_traffic(self) -> None:
        toolbar = ttk.Frame(self.traffic_tab)
        toolbar.pack(fill="x", pady=(0, 8))
        ttk.Label(toolbar, text="PDU-relevant COB-IDs only", style="Muted.TLabel").pack(side="left")
        ttk.Button(toolbar, text="Clear", command=lambda: self.can_log.delete("1.0", "end")).pack(side="right")
        self.can_log = tk.Text(self.traffic_tab, bg="#0B0F13", fg="#A7F3D0", insertbackground=TEXT, relief="flat", font=("DejaVu Sans Mono", 10), padx=12, pady=12)
        self.can_log.pack(fill="both", expand=True)

    def _toggle_connect(self) -> None:
        if self.connected:
            self._send_command("disconnect")
        else:
            self.connect_button.configure(state="disabled")
            self.connection_text.set("CONNECTING")
            self.status_text.set(f"Opening {self.channel.get()} as CANopen node {self.node_id.get()}…")
            self._send_command("connect", self.channel.get().strip(), self.node_id.get())

    def _send_command(self, name: str, *args) -> None:
        self.commands.put((name, *args))

    def _confirm_reset(self) -> None:
        if messagebox.askyesno("Reset node", "Reset CANopen node 10? Power outputs remain inactive."):
            self._send_command("nmt", "RESET")

    def _read_sdo(self) -> None:
        try:
            index = int(self.sdo_index.get().strip(), 16)
            subindex = int(self.sdo_subindex.get().strip(), 16)
        except ValueError:
            messagebox.showerror("Invalid SDO address", "Use hexadecimal values such as 100A and 00.")
            return
        self.sdo_result.set("Reading…")
        self._send_command("sdo_read", index, subindex)

    def _write_sdo(self) -> None:
        try:
            index = int(self.sdo_index.get().strip(), 16)
            subindex = int(self.sdo_subindex.get().strip(), 16)
            data = bytes.fromhex(self.sdo_write_data.get().strip())
            if not data:
                raise ValueError("empty data")
        except ValueError:
            messagebox.showerror("Invalid SDO write", "Use a hex index/sub-index and bytes such as F4 01 for uint16 value 500.")
            return
        if messagebox.askyesno("Confirm SDO write", f"Write {data.hex(' ').upper()} to 0x{index:04X}:{subindex:02X}?"):
            self._send_command("sdo_write", index, subindex, data)

    def _load_channel_settings(self) -> None:
        if self.last_snapshot is None:
            return
        i = self.selected_channel.get() - 1
        self.limit_amps.set(f"{self.last_snapshot.current_limits_ma[i] / 1000:.3f}")
        self.trip_time_ms.set(str(self.last_snapshot.current_trip_times_ms[i]))
        self.inrush_amps.set(f"{self.last_snapshot.inrush_limits_ma[i] / 1000:.3f}")
        self.inrush_time_ms.set(str(self.last_snapshot.inrush_times_ms[i]))

    def _save_channel_settings(self) -> None:
        try:
            channel = self.selected_channel.get()
            values = (round(float(self.limit_amps.get()) * 1000), int(self.trip_time_ms.get()),
                      round(float(self.inrush_amps.get()) * 1000), int(self.inrush_time_ms.get()))
            if not (100 <= values[0] <= 10000 and 1 <= values[1] <= 5000 and
                    100 <= values[2] <= 10000 and 0 <= values[3] <= 10000):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid limits", "Continuous/inrush: 0.1–10 A; trip delay: 1–5000 ms; inrush time: 0–10000 ms.")
            return
        if messagebox.askyesno("Save protection limits", f"Write protection settings for output {channel}?"):
            self._send_command("channel_settings", channel, *values)

    def _toggle_output(self) -> None:
        if self.last_snapshot is None:
            return
        channel = self.selected_channel.get()
        bit = 1 << (channel - 1)
        turning_on = not bool(self.last_snapshot.output_request & bit)
        self._request_output(channel, turning_on)

    def _request_output(self, channel: int, turning_on: bool) -> None:
        if not self.connected or self.last_snapshot is None:
            messagebox.showerror("Not connected", "Connect to the PDU before controlling an output.")
            return
        if turning_on and self.last_snapshot.nmt_state != "Operational":
            messagebox.showerror("Node not Operational", "Start the CANopen node before requesting an output ON.")
            return
        self.selected_channel.set(channel)
        if turning_on:
            prompt = f"Request output {channel} ON?\n\nVerify the connected load and current limits first."
            if not messagebox.askyesno("Request output ON", prompt):
                return
        self._send_command("output_request", channel, turning_on)

    def _reset_output(self, channel: int) -> None:
        if not self.connected:
            messagebox.showerror("Not connected", "Connect to the PDU before resetting an output.")
            return
        self.selected_channel.set(channel)
        self._send_command("output_reset", channel)

    def _clear_channel_fault(self) -> None:
        channel = self.selected_channel.get()
        if messagebox.askyesno("Clear latched fault", f"Clear output {channel} fault? The output request must be OFF."):
            self._send_command("fault_clear", channel)

    def _apply_communication(self) -> None:
        node_id, bitrate = self.pending_node_id.get(), self.pending_bitrate.get()
        prompt = (f"Change this running session to node {node_id} at {bitrate} kbit/s?\n\n"
                  "This is RAM-only and reverts to node 10 / 500 kbit/s after power loss. "
                  "The GUI will disconnect; change can0 bitrate before reconnecting if needed.")
        if messagebox.askyesno("Apply communication settings", prompt):
            self._send_command("communication", node_id, bitrate)

    def _select_image(self) -> None:
        path = filedialog.askopenfilename(title="Select signed MCUboot image", filetypes=(("MCUboot binary", "*.bin"), ("All files", "*")))
        if not path:
            return
        try:
            info = inspect_update_image(path)
        except (OSError, ValueError) as exc:
            messagebox.showerror("Invalid update image", str(exc))
            return
        self.selected_image = path
        self.update_file_text.set(
            f"{Path(path).name}\n{info['size']:,} bytes · identity {info['identity']}\nSHA-256 {str(info['sha256'])[:16]}…"
        )

    def _start_update(self) -> None:
        if not self.connected:
            messagebox.showerror("Not connected", "Connect to the PDU first.")
            return
        if not self.selected_image:
            messagebox.showerror("No image selected", "Select a signed MCUboot .bin image first.")
            return
        info = inspect_update_image(self.selected_image)
        prompt = (
            f"Transfer {Path(self.selected_image).name} ({info['size']:,} bytes) to the PDU?\n\n"
            "The node will enter Pre-operational, erase the staging sector, reboot, and replace the active image. "
            "This bench layout has no automatic rollback."
        )
        if not messagebox.askyesno("Confirm firmware update", prompt):
            return
        self.updating = True
        self.update_button.configure(state="disabled")
        self.update_progress.configure(value=0)
        self._send_command("firmware_update", self.selected_image)

    def _frame_event(self, line: str) -> None:
        try:
            self.events.put_nowait(("frame", line))
        except queue.Full:
            pass

    def _worker_loop(self) -> None:
        next_poll = 0.0
        while not self.stop_event.is_set():
            try:
                command = self.commands.get(timeout=0.08)
            except queue.Empty:
                command = None

            if command is not None:
                name, *args = command
                try:
                    if name == "connect":
                        channel, node_id = args
                        client = PduCanClient(channel, int(node_id), self._frame_event)
                        client.connect()
                        self.client = client
                        next_poll = 0.0
                        self.events.put(("connected",))
                    elif name == "disconnect":
                        if self.client:
                            self.client.disconnect()
                        self.client = None
                        self.events.put(("disconnected",))
                    elif name == "nmt" and self.client:
                        self.client.send_nmt(str(args[0]))
                        self.events.put(("message", f"NMT command sent: {args[0]}"))
                    elif name == "sdo_read" and self.client:
                        index, subindex = args
                        data = self.client.upload(int(index), int(subindex))
                        self.events.put(("sdo", int(index), int(subindex), data))
                    elif name == "sdo_write" and self.client:
                        index, subindex, data = args
                        self.client.download(int(index), int(subindex), bytes(data))
                        self.events.put(("message", f"SDO write complete: 0x{int(index):04X}:{int(subindex):02X}"))
                        next_poll = 0.0
                    elif name == "output_request" and self.client:
                        channel, turning_on = int(args[0]), bool(args[1])
                        bit = 1 << (channel - 1)
                        bitmap = decode_u(self.client.upload(0x2103, 0))
                        bitmap = (bitmap | bit) if turning_on else (bitmap & ~bit)
                        self.client.download(0x2103, 0, bitmap.to_bytes(2, "little"))
                        action = "ON" if turning_on else "OFF"
                        self.events.put(("message", f"Output {channel} requested {action} by SDO"))
                        next_poll = 0.0
                    elif name == "output_reset" and self.client:
                        channel = int(args[0])
                        bit = 1 << (channel - 1)
                        bitmap = decode_u(self.client.upload(0x2103, 0)) & ~bit
                        self.client.download(0x2103, 0, bitmap.to_bytes(2, "little"))
                        self.client.download(0x2104, 0, bit.to_bytes(2, "little"))
                        self.client.download(0x2104, 0, b"\x00\x00")
                        self.events.put(("message", f"Output {channel} forced OFF and fault reset by SDO"))
                        next_poll = 0.0
                    elif name == "channel_settings" and self.client:
                        channel, limit_ma, trip_ms, inrush_ma, inrush_ms = map(int, args)
                        for index, value in ((0x3100, limit_ma), (0x3101, trip_ms),
                                             (0x3102, inrush_ma), (0x3103, inrush_ms)):
                            self.client.download(index, channel, value.to_bytes(2, "little"))
                        self.events.put(("message", f"Output {channel} protection settings saved"))
                        next_poll = 0.0
                    elif name == "fault_clear" and self.client:
                        channel = int(args[0])
                        bit = 1 << (channel - 1)
                        self.client.download(0x2104, 0, bit.to_bytes(2, "little"))
                        self.client.download(0x2104, 0, b"\x00\x00")
                        self.events.put(("message", f"Output {channel} fault-clear pulse sent"))
                        next_poll = 0.0
                    elif name == "communication" and self.client:
                        node_id, bitrate = map(int, args)
                        self.client.download(0x2105, 0, node_id.to_bytes(1, "little"))
                        self.client.download(0x2106, 0, bitrate.to_bytes(2, "little"))
                        self.client.download(0x2107, 0, b"\xA5")
                        self.client.disconnect()
                        self.client = None
                        self.events.put(("disconnected",))
                        self.events.put(("message", "Communication reset applied; reconnect with the new settings"))
                    elif name == "firmware_update" and self.client:
                        identity = self.client.firmware_update(str(args[0]), self._update_worker_progress)
                        self.events.put(("update_done", identity))
                        next_poll = 0.0
                except Exception as exc:
                    self.events.put(("error", name, str(exc)))

            if self.client and self.client.connected and not self.updating and time.monotonic() >= next_poll:
                try:
                    self.events.put(("snapshot", self.client.read_snapshot(include_channels=True)))
                except Exception as exc:
                    self.events.put(("error", "poll", str(exc)))
                next_poll = time.monotonic() + 2.0

        if self.client:
            self.client.disconnect()

    def _update_worker_progress(self, sent: int, total: int, message: str) -> None:
        self.events.put(("update_progress", sent, total, message))

    def _tick(self) -> None:
        for _ in range(300):
            try:
                event = self.events.get_nowait()
            except queue.Empty:
                break
            kind = event[0]
            if kind == "connected":
                self.connected = True
                self.connect_button.configure(text="Disconnect", state="normal")
                self.connection_text.set("CONNECTED")
                self.status_text.set("Reading object dictionary…")
            elif kind == "disconnected":
                self.connected = False
                self.connect_button.configure(text="Connect", state="normal")
                self.connection_text.set("DISCONNECTED")
                self.status_text.set("Disconnected from the PDU.")
            elif kind == "snapshot":
                self._apply_snapshot(event[1])
            elif kind == "frame":
                self.can_log.insert("end", event[1] + "\n")
                if int(self.can_log.index("end-1c").split(".")[0]) > 1500:
                    self.can_log.delete("1.0", "300.0")
                self.can_log.see("end")
            elif kind == "sdo":
                _, index, subindex, data = event
                text = decode_text(data) if data and all(32 <= byte < 127 for byte in data.rstrip(b"\0")) else ""
                suffix = f" · ASCII {text!r}" if text else f" · unsigned {decode_u(data)}"
                self.sdo_result.set(f"0x{index:04X}:{subindex:02X} = {data.hex(' ').upper()}{suffix}")
            elif kind == "message":
                self.status_text.set(event[1])
            elif kind == "update_progress":
                _, sent, total, message = event
                percent = 100.0 * sent / total if total else 0
                self.update_progress.configure(value=percent)
                self.update_progress_text.set(f"{message} · {sent:,}/{total:,} bytes ({percent:.1f}%)")
            elif kind == "update_done":
                self.updating = False
                self.update_button.configure(state="normal")
                self.update_progress.configure(value=100)
                self.update_progress_text.set(f"Update complete · running {event[1]}")
                self.status_text.set(f"Firmware update successful: {event[1]}")
                messagebox.showinfo("Firmware update complete", f"The PDU rebooted successfully and reports {event[1]}.")
            elif kind == "error":
                _, operation, message = event
                if operation in ("connect", "disconnect"):
                    self.connected = False
                    self.connect_button.configure(text="Connect", state="normal")
                    self.connection_text.set("DISCONNECTED")
                if operation == "firmware_update":
                    self.updating = False
                    self.update_button.configure(state="normal")
                self.status_text.set(f"{operation}: {message}")
                if operation != "poll":
                    messagebox.showerror("PDU operation failed", f"{operation}: {message}")
        if not self.stop_event.is_set():
            self.root.after(100, self._tick)

    def _apply_snapshot(self, snap: PduSnapshot) -> None:
        self.last_snapshot = snap
        self.device_text.set(f"{snap.device_name}\n{snap.hardware_version}")
        self.version_text.set(snap.software_version)
        self.nmt_text.set(snap.nmt_state)
        if snap.heartbeat_age_s is None:
            self.heartbeat_text.set("No heartbeat")
        else:
            self.heartbeat_text.set(f"{snap.heartbeat_age_s:.1f} s ago")
        self.uptime_text.set(fmt_duration(snap.uptime_s))
        active = snap.output_states.bit_count()
        self.output_text.set(f"{active} / {OUTPUT_COUNT} active")
        self.current_text.set(fmt_unknown(snap.total_current_ma, 0xFFFFFFFF, " mA"))
        self.voltage_text.set("—" if snap.supply_voltage_mv == 0xFFFF else f"{snap.supply_voltage_mv / 1000:.2f} V")
        board_temp = "—" if snap.board_temperature_dc == 0x7FFF else f"{snap.board_temperature_dc / 10:.1f} °C"
        mcu_temp = "—" if snap.mcu_temperature_dc == 0x7FFF else f"{snap.mcu_temperature_dc / 10:.1f} °C"
        self.temperature_text.set(f"Board temperature {board_temp} · MCU temperature {mcu_temp}")

        issues = []
        if snap.error_register:
            issues.append(f"CANopen error register 0x{snap.error_register:02X}")
        if snap.output_faults:
            issues.append(f"output fault mask 0x{snap.output_faults:04X}")
        if snap.warning_flags:
            issues.append(f"warnings 0x{snap.warning_flags:04X}")
        if snap.flash_status:
            issues.append(f"flash status 0x{snap.flash_status:08X}")
        if snap.heartbeat_age_s is None or snap.heartbeat_age_s > 2.5:
            issues.append("heartbeat stale")
        self.health_text.set("Healthy · current protection active" if not issues else " · ".join(issues))
        self.status_text.set("Live CANopen data" + (f" · {len(snap.read_errors)} unavailable reads" if snap.read_errors else ""))

        for index in range(OUTPUT_COUNT):
            bit = 1 << index
            actual = bool(snap.output_states & bit)
            commanded = bool(snap.output_commanded & bit)
            fault = bool(snap.output_faults & bit)
            current = fmt_unknown(snap.currents_ma[index], 0xFFFF, " mA")
            raw = fmt_unknown(snap.raw_adc[index], 0xFFFF)
            peak = fmt_unknown(snap.peak_currents_ma[index], 0xFFFF, " mA")
            values = self.channel_values[index]
            values["actual"].set("ON" if actual else "OFF")
            values["requested"].set("ON" if commanded else "OFF")
            values["current"].set(current)
            values["raw"].set(raw)
            values["peak"].set(peak)
            values["trips"].set(str(snap.trip_counts[index]))
            values["fault"].set("FAULT" if fault else "—")
            label_style = "Panel.TLabel"
            if fault:
                label_style = "Fault.Panel.TLabel"
            elif actual:
                label_style = "Active.Panel.TLabel"
            for label in self.channel_value_labels[index]:
                label.configure(style=label_style)

        diagnostics = (
            f"Software identity : {snap.software_version}\n"
            f"CANopen state     : {snap.nmt_state}\n"
            f"Error register    : 0x{snap.error_register:02X}\n"
            f"Validity bitmap   : 0x{snap.telemetry_validity:08X}\n"
            f"Output states     : 0x{snap.output_states:04X}\n"
            f"Output commanded  : 0x{snap.output_commanded:04X}\n"
            f"Output requested  : 0x{snap.output_request:04X}\n"
            f"Output faults     : 0x{snap.output_faults:04X}\n"
            f"Overcurrent       : 0x{snap.overcurrent_faults:04X}\n"
            f"Open load         : 0x{snap.open_load_faults:04X}\n"
            f"Disabled outputs  : 0x{snap.output_disabled:04X}\n"
            f"Brownout count    : {snap.brownout_count}\n"
            f"CAN bus-off count : {snap.can_busoff_count}\n"
            f"Program control   : 0x{snap.program_control:02X}\n"
            f"Flash status      : 0x{snap.flash_status:08X}\n"
            f"Reset reason      : 0x{snap.reset_reason:04X}\n"
            f"Pending node ID   : {snap.pending_node_id}\n"
            f"Pending bitrate   : {snap.pending_bitrate_kbps} kbit/s\n"
        )
        self.diagnostic_text.configure(state="normal")
        self.diagnostic_text.delete("1.0", "end")
        self.diagnostic_text.insert("1.0", diagnostics)
        self.diagnostic_text.configure(state="disabled")

    def _close(self) -> None:
        self.stop_event.set()
        self.root.after(50, self.root.destroy)


def main() -> None:
    root = tk.Tk()
    PduGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
