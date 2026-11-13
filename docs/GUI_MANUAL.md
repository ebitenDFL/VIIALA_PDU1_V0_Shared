# VIIALA PDU CANopen Workbench manual

## Purpose

The workbench is a Linux desktop application for commissioning, monitoring and
updating `VIIALA_PDU1_V0`. It communicates through SocketCAN and uses standard
CANopen NMT, heartbeat, PDO and SDO services.

The tested adapter is PEAK PCAN-USB exposed as `can0`. Other SocketCAN adapters
should work when their Linux driver creates a CAN network interface.

## Installation

On Ubuntu/Debian:

```bash
sudo apt install -y python3-venv python3-tk can-utils
cd VIIALA_PDU1_V0_Shared/gui
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
chmod +x run_gui.sh
```

## CAN interface setup

The PDU defaults to 500 kbit/s. The launcher checks `can0` and leaves it alone
when it is already active at the correct bitrate. Otherwise it configures and
starts the interface with 100 ms automatic bus-off recovery. Linux may display
one administrator-password prompt because CAN network configuration requires
elevated permission.

Advanced users can override the defaults with `PDU_CAN_IFACE` and
`PDU_CAN_BITRATE`.

Optional traffic monitor:

```bash
candump -tz can0
```

## Start the GUI

```bash
cd VIIALA_PDU1_V0_Shared/gui
./run_gui.sh
```

Enter the SocketCAN interface and current node ID, then select **Connect**.
Default values are `can0` and node 10.

## Overview tab

The Overview tab displays:

- device, hardware and A/B firmware identity;
- CANopen NMT state and heartbeat age;
- uptime and active-output count;
- total measured output current;
- available supply/temperature telemetry and health flags.

Use **Pre-op**, **Start**, and **Stop** for NMT state changes. Output requests
only actuate while the node is Operational and current acquisition is valid.
Leaving Operational state clears all output requests.

## Fifteen Channels tab

The table shows actual/commanded state, current, raw ADC, peak current, trip
count and fault state for every output. Each row has dedicated **ON**, **OFF**
and **Reset** buttons:

- **ON** checks that the node is Operational and asks for confirmation before
  writing the output request over SDO.
- **OFF** immediately clears that output's request over SDO.
- **Reset** first forces that output's request OFF, then pulses its latched-
  fault clear object.

To configure a channel:

1. Select its number.
2. Select **Load channel** to read the current settings.
3. Enter the continuous limit in amperes and its trip delay in milliseconds.
4. Enter the inrush limit in amperes and its allowed time in milliseconds.
5. Select **Save limits** and confirm the SDO writes.

Accepted firmware ranges:

| Setting | Range | Default |
|---|---:|---:|
| Continuous current | 0.1–10 A | 5 A |
| Continuous trip delay | 1–5000 ms | 100 ms |
| Inrush current | 0.1–10 A | 8 A |
| Inrush allowance | 0–10000 ms | 500 ms |

To operate an output, verify the load and limits, place the node Operational,
then use its row controls. The top **Request ON/OFF** and **Clear fault**
controls remain available for the selected channel.

### Current display notes

Inactive outputs publish 0 mA. Their raw ADC value may show the NCV84045
OFF-state diagnostic level (often 4095); this is not load current. Active
channels use trimmed multi-sample averaging. Very small loads around tens of
milliamperes are below the practical accuracy of this high-current sense path.

## Diagnostics and raw SDO access

The SDO inspector reads any object by hexadecimal index and sub-index. For a
write, enter little-endian bytes and confirm the operation. Examples:

| Operation | Index:sub | Data bytes |
|---|---|---|
| Request OUT1 ON | `2103:00` | `01 00` |
| Request all outputs OFF | `2103:00` | `00 00` |
| Set pending node ID to 12 | `2105:00` | `0C` |
| Set pending bitrate to 500 | `2106:00` | `F4 01` |
| Apply communication settings | `2107:00` | `A5` |

Raw SDO writes bypass GUI-level range checks. Use the supplied EDS and verify
the object type before writing.

## Changing node ID or bitrate

Set the pending node ID and bitrate, then apply. The GUI disconnects because
the PDU performs a CANopen communication reset. If bitrate changed, reconfigure
`can0` before reconnecting.

Communication changes are RAM-only. A power cycle restores node 10 at
500 kbit/s.

## CANopen firmware update

1. Confirm all output requests are OFF and disconnect unsafe loads.
2. Connect to the current node ID and select the Diagnostics & Update tab.
3. Choose the intended signed `.bin` from `firmware/`.
4. Confirm the filename, size and A/B identity.
5. Select **Stage & activate** and do not remove power or CAN connectivity.
6. Wait for the transfer, MCUboot activation, reboot and identity confirmation.

The update erases the 128 KiB staging sector and can take several seconds
before transfer begins. The current layout has no automatic rollback. Keep
ST-LINK recovery access available during development.

## Troubleshooting

- **No heartbeat / SDO timeout:** verify termination, bitrate, node ID and that
  only one application owns the same SDO channel.
- **Object does not exist (`0x06020000`):** the PDU is running an older
  dictionary/firmware; update it before using the new control objects.
- **Permission denied on `can0`:** accept the launcher's administrator prompt,
  or configure the interface manually and verify local networking permissions.
- **No GUI display from SSH:** run on the Linux desktop or use X forwarding.
- **Raw value 4095 while OFF:** expected OFF-state diagnostic; use the current
  column and validity/state information.

