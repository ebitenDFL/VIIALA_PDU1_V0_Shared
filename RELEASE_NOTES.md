# Developer preview 2026-11-13

## Included firmware

| Image | Size | SHA-256 |
|---|---:|---|
| `VIIALA_PDU1_V0_A001_DEV_KEY_BENCH_ONLY.bin` | 61,140 bytes | `f1175746a0ef250087bbff5aa03c19a3eba767b2c3df229d86fa439df1d2933e` |
| `VIIALA_PDU1_V0_B001_DEV_KEY_BENCH_ONLY.bin` | 61,140 bytes | `1fab89ced28a11d775b0b1f322f8cc4dfddd67a1f9b6a0eac95c075ea869b0ed` |

## Verified

- CANopen heartbeat, NMT, SDO and four current/state TPDOs.
- A/B identity through `0x100A:00`.
- CANopen firmware transfer, MCUboot activation and confirmation.
- All outputs OFF before and during update.
- AD7490 SPI mode 0 and channel communication.
- Output requests, protection configuration and latched fault control objects.
- Linux GUI connection, telemetry, raw SDO access and firmware update workflow.
- Zephyr 4.5.0 compile, signing and A-to-B CAN update on the connected F7.
- Automatic SocketCAN setup and per-row ON/OFF/Reset workbench controls.

## Pending validation

- Calibrated current slope using known fused loads in the 0.5–5 A range.
- Protection trip timing across all fifteen outputs.
- Per-channel current offset and gain characterization.
- Thermal, short-circuit, brownout and interrupted-update testing.
- Replacement of the public MCUboot development key.
- Production rollback/recovery architecture.

