# Developer preview 2026-11-12

## Included firmware

| Image | Size | SHA-256 |
|---|---:|---|
| `VIIALA_PDU1_V0_A001_DEV_KEY_BENCH_ONLY.bin` | 58,480 bytes | `8fc28a75b3508c335df48a137c5e1fb8828c47963a046b7788883af7ce6ea681` |
| `VIIALA_PDU1_V0_B001_DEV_KEY_BENCH_ONLY.bin` | 58,480 bytes | `c6789a5451b230c0fb170b07d5d28ee2517642a030cb738b5c8d486a4c863af6` |

## Verified

- CANopen heartbeat, NMT, SDO and four current/state TPDOs.
- A/B identity through `0x100A:00`.
- CANopen firmware transfer, MCUboot activation and confirmation.
- All outputs OFF before and during update.
- AD7490 SPI mode 0 and channel communication.
- Output requests, protection configuration and latched fault control objects.
- Linux GUI connection, telemetry, raw SDO access and firmware update workflow.

## Pending validation

- Calibrated current slope using known fused loads in the 0.5–5 A range.
- Protection trip timing across all fifteen outputs.
- Per-channel current offset and gain characterization.
- Thermal, short-circuit, brownout and interrupted-update testing.
- Replacement of the public MCUboot development key.
- Production rollback/recovery architecture.

