# CANopen developer guide

## Network defaults

- Node ID: 10
- Bitrate: 500 kbit/s
- Heartbeat producer: 1000 ms
- Device name: `VIIALA_PDU1_V0`

CANopen multibyte values and SDO write bytes are little-endian.

## Default TPDOs

For node ID 10:

| PDO | COB-ID | Payload |
|---|---:|---|
| TPDO1 | `0x18A` | Currents 1–4, four `uint16` mA values |
| TPDO2 | `0x28A` | Currents 5–8, four `uint16` mA values |
| TPDO3 | `0x38A` | Currents 9–12, four `uint16` mA values |
| TPDO4 | `0x48A` | Currents 13–15, then active-output `uint16` bitmap |
| TPDO5 | `0x68A` | Supply mV, MCU die temperature in 0.1 °C, MCU VDDA mV, warning flags; four 16-bit values |

TPDO transmission type is 254. TPDO1–4 use a 100 ms event timer and 100 ms
inhibit time; TPDO5 is sent every five seconds. PDO transmission begins in Operational state.

## Primary SDO objects

| Index | Type/access | Description |
|---|---|---|
| `0x1008:00` | visible string, RO | Device name |
| `0x1009:00` | visible string, RO | Hardware version |
| `0x100A:00` | visible string, RO | A/B software identity |
| `0x2000:00` | `uint16`, RO | Active-output bitmap |
| `0x2001:00` | `uint16`, RO | Commanded-output bitmap |
| `0x2002:00` | `uint16`, RO | Combined fault bitmap |
| `0x2003:00` | `uint16`, RO | Overcurrent-fault bitmap |
| `0x2006:00` | `uint32`, RO | Total current in mA |
| `0x2007:00` | `uint16`, RO | PDU input voltage in mV |
| `0x2009:00` | `int16`, RO | MCU die temperature in 0.1 °C |
| `0x200F:00` | `uint32`, RO | Telemetry-validity bitmap |
| `0x2010:00` | `uint16`, RO | MCU analog supply (VDDA) in mV |
| `0x2103:00` | `uint16`, RW | Requested-output bitmap |
| `0x2104:00` | `uint16`, RW | Fault-clear pulse bitmap |
| `0x2105:00` | `uint8`, RW | Pending node ID |
| `0x2106:00` | `uint16`, RW | Pending bitrate in kbit/s |
| `0x2107:00` | `uint8`, RW | Write `0xA5` to apply communication settings |
| `0x3000:01..0F` | `uint16`, RO | Currents 1–15 in mA |
| `0x3001:01..0F` | `uint16`, RO | Raw ADC values |
| `0x3002:01..0F` | `uint16`, RO | Peak currents in mA |
| `0x3003:01..0F` | `uint32`, RO | Overcurrent trip counters |
| `0x3100:01..0F` | `uint16`, RW | Continuous current limits in mA |
| `0x3101:01..0F` | `uint16`, RW | Continuous trip delays in ms |
| `0x3102:01..0F` | `uint16`, RW | Inrush limits in mA |
| `0x3103:01..0F` | `uint16`, RW | Inrush allowance times in ms |

The complete standard and manufacturer object set is defined by the EDS files
in `object_dictionary/`.

## Telemetry validity

`0x200F` uses bit 0 for output-state validity, bits 1–15 for current channels,
bit 16 for total current, bits 17–19 for voltage/temperatures, bit 20 for fault
masks, bit 21 for diagnostic counters and bit 22 for MCU VDDA. Check validity before consuming a
telemetry object.

## Python example

```python
import canopen

network = canopen.Network()
network.connect(interface="socketcan", channel="can0")
node = network.add_node(10, "object_dictionary/VIIALA_PDU1_V0_A001.eds")

print(node.sdo[0x1008].raw)
print(node.sdo[0x100A].raw)

node.nmt.state = "OPERATIONAL"
node.sdo[0x3100][1].raw = 5000   # OUT1 continuous limit: 5 A
node.sdo[0x3101][1].raw = 100    # OUT1 delay: 100 ms
node.sdo[0x2103].raw = 0x0001    # request OUT1 ON

# Always request OFF before disconnecting the commissioning tool.
node.sdo[0x2103].raw = 0
network.disconnect()
```

## Node ID and bitrate changes

Allowed node IDs are 1–127. Allowed bitrates are 125, 250, 500 and
1000 kbit/s. Write pending values first, then write `0xA5` to `0x2107:00`.
The node resets CANopen communication and all outputs remain OFF.

Settings are volatile and revert to node 10 / 500 kbit/s after power loss.

## Firmware download objects

The GUI uses program-control/data/status objects `0x1F50`, `0x1F51`,
`0x1F56`, and `0x1F57`. Use a response timeout of at least ten seconds for the
128 KiB staging-sector erase. Do not start an update with active outputs.

