# Firmware description

The included A001 and B001 images are built with the pinned Zephyr 4.5.0
release and Zephyr SDK 1.0.1.

## Target hardware

`VIIALA_PDU1_V0` targets the verified HW20 board with an STM32F722RCT6
(256 KiB internal flash), fifteen NCV84045 protected high-side outputs, an
AD7490 16-channel 12-bit ADC and CAN1 on PB8/PB9.

Verified ADC connections:

| Function | MCU pin |
|---|---|
| SPI1 SCK | PA5 |
| SPI1 MISO | PA6 |
| SPI1 MOSI | PA7 |
| AD7490 chip select | PA15, active low |
| NCV84045 current-sense enable | PB15, active high |

The AD7490 uses SPI mode 0 at 1 MHz. Channels 0–14 correspond to outputs
1–15. Channel 15 measures the PDU supply through the fitted 100 kohm / 22 kohm
divider and is published every five seconds. With the 2.5 V ADC reference the
present divider saturates at approximately 13.86 V.

The STM32 factory calibration values are used for MCU die temperature and VDDA.
Die temperature is junction temperature, not PCB or ambient temperature.

## Startup and fail-safe behavior

- All fifteen output GPIOs are configured inactive before CANopen starts.
- No output can activate without an explicit request, Operational NMT state,
  valid current acquisition and no latched fault.
- Leaving Operational state or losing valid ADC acquisition turns every output
  OFF and clears the request bitmap.
- Communication reset and firmware update force all outputs OFF.

## Current acquisition

Current-sense voltage is digitized against a nominal 2.5 V reference. The
initial engineering conversion uses the NCV84045 typical sense ratio and the
fitted 301-ohm sense resistor. Active channels use the verified VI_PDU3 method:
three settling reads, sixteen samples, removal of minimum and maximum, then
averaging. A provisional six-count zero offset is applied before conversion.

Inactive channels publish 0 mA while retaining their raw OFF-state diagnostic
value. High-current calibration is still pending; do not treat the present
conversion as a production measurement standard.

## Protection behavior

Each output has independent continuous and inrush thresholds. During the
configured inrush window, exceeding the inrush threshold trips on the next
filtered sample. After the window, the continuous limit must remain exceeded
for its configured trip delay.

An overcurrent trip:

1. turns the output OFF;
2. sets a latched fault bit;
3. increments its trip counter;
4. prevents reactivation until the request is OFF and a clear pulse is sent.

The first sample after activation is ignored because it belongs to the prior
OFF-state diagnostic condition.

## CANopen services

The firmware provides NMT slave behavior, heartbeat, SDO server access, four
asynchronous current/state TPDOs at 10 Hz, a five-second slow telemetry TPDO,
emergency/error objects and CiA 302-3-style
program download objects. See `CANOPEN_DEVELOPER_GUIDE.md` and the EDS files.

## Firmware identity

Both variants have identical hardware/control behavior and differ in the
standard software-version string:

- A image: `0x100A:00 = "A001"`
- B image: `0x100A:00 = "B001"`

This makes the running image identifiable with one SDO upload. A/B names do
not mean that both images coexist in active flash.

## Flash and update layout

| Region | Address offset | Size |
|---|---:|---:|
| MCUboot | `0x00000` | 64 KiB |
| Active application | `0x10000` | 64 KiB |
| Download staging | `0x20000` | 128 KiB |

MCUboot copies a verified staged image over the active application. This is an
overwrite-only arrangement with no retained previous image and no automatic
rollback.

