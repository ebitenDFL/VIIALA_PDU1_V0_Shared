# Developer preview 2026-11-13

## Included firmware

| Image | Size | SHA-256 |
|---|---:|---|
| `VIIALA_PDU1_V0_A001_DEV_KEY_BENCH_ONLY.bin` | 62,348 bytes | `cf342f40a9bfffafef0a33dc4f2764aa512fb7f251e4b1b2886feddbf1202f29` |
| `VIIALA_PDU1_V0_B001_DEV_KEY_BENCH_ONLY.bin` | 62,348 bytes | `e355496c8148342862517a74cb16498fa91feb299bee071645250cc6bbe4e2f8` |

## Verified

- CANopen heartbeat, NMT, SDO, four current/state TPDOs and a five-second slow telemetry TPDO.
- A/B identity through `0x100A:00`.
- CANopen firmware transfer, MCUboot activation and confirmation.
- All outputs OFF before and during update.
- AD7490 SPI mode 0 and channel communication.
- Output requests, protection configuration and latched fault control objects.
- Linux GUI connection, telemetry, raw SDO access and firmware update workflow.
- Zephyr 4.5.0 compile, signing and A-to-B CAN update on the connected F7.
- Automatic SocketCAN setup and per-row ON/OFF/Reset workbench controls.
- Live IN15 input voltage, factory-calibrated MCU die temperature and VDDA.

## Pending validation

- Calibrated current slope using known fused loads in the 0.5–5 A range.
- Protection trip timing across all fifteen outputs.
- Per-channel current offset and gain characterization.
- Thermal, short-circuit, brownout and interrupted-update testing.
- Replacement of the public MCUboot development key.
- Production rollback/recovery architecture.

