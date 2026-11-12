# VIIALA_PDU1_V0 developer package

Public integration package for the VIIALA 15-channel CANopen power distribution
unit. This repository contains the Linux workbench, CANopen object dictionaries,
documentation, and signed A/B firmware-update images.

## Package contents

- `gui/` — Linux SocketCAN/CANopen workbench.
- `object_dictionary/` — A001 and B001 EDS files plus the generated C header.
- `firmware/` — signed MCUboot images for CANopen firmware transfer.
- `docs/GUI_MANUAL.md` — installation and complete GUI usage guide.
- `docs/FIRMWARE_DESCRIPTION.md` — hardware, firmware and protection overview.
- `docs/CANOPEN_DEVELOPER_GUIDE.md` — PDO/SDO integration reference.
- `RELEASE_NOTES.md` — release status, hashes and known limitations.

## Default connection

| Setting | Default |
|---|---:|
| CANopen node ID | 10 |
| CAN bitrate | 500 kbit/s |
| Device name (`0x1008:00`) | `VIIALA_PDU1_V0` |
| Hardware version (`0x1009:00`) | `HW20` |
| Firmware identity (`0x100A:00`) | `A001` or `B001` |

Start with [the GUI manual](docs/GUI_MANUAL.md) or the
[CANopen developer guide](docs/CANOPEN_DEVELOPER_GUIDE.md).

## Safety and release status

This is a **developer-preview/bench package**, not a production firmware
release.

- The binaries use MCUboot's public development signing key. Anyone can create
  another image accepted by that key; replace it before field deployment.
- The STM32F722RCT6 internal-flash layout is overwrite-only. A/B identifies
  firmware variants but does not provide rollback or redundant active slots.
- High-current calibration and protection timing still require validation with
  known fused loads.
- These images are only for the verified VIIALA/SPEEDER PDU HW20 board.
- Confirm every output is OFF before firmware transfer or bench wiring changes.

No warranty is provided. The integrator remains responsible for electrical,
thermal, vehicle and functional-safety validation.

