# Hardware proof-of-concept

> Educational reference only; not an approved wearable or safe-to-wear electronics enclosure.

## Components for a benchtop experiment

- ESP32 development board (specific model must support the `Wire.begin(21, 22)` configuration, or modify the sketch).
- MPU6050 inertial measurement unit breakout, supported by the **Adafruit MPU6050** Arduino library.
- USB cable, breadboard, jumper wires, computer with Arduino IDE.
- Stable, suitable power supply for the actual breakout and host board.

### Example I2C mapping

| MPU6050 breakout | ESP32 (example) |
| --- | --- |
| VCC | 3V3 (confirm breakout's supply range) |
| GND | GND |
| SDA | GPIO 21 |
| SCL | GPIO 22 |

Do not assume all 'MPU6050' breakout boards have identical regulators, pull-ups or safe supply voltages. Verify the datasheet and voltage-level compatibility before wiring.

## Setup

1. In Arduino IDE, install the ESP32 board platform that supports your exact ESP32 variant.
2. Install **Adafruit MPU6050**, **Adafruit Unified Sensor**, and dependency **Adafruit BusIO** via Library Manager.
3. Connect the sensor with power OFF; check pin assignments.
4. Open `firmware/esp32_mpu6050/esp32_mpu6050.ino`, compile, upload, and open the serial monitor at **115200 baud**.
5. Expect seven CSV fields: `timestamp_ms,ax_g,ay_g,az_g,gx_dps,gy_dps,gz_dps`.

At present the system is **wired via USB**; Bluetooth, low-power operation, charging and wearable enclosure have not been implemented in this sample firmware. Do not place uncovered or powered benchtop electronics against skin, or expose them to sweat or washing. Future electronics should be mechanically secured and evaluated for heat, power, skin contact, breakage, pressure injury and ingress protection.

## Proposed materials to investigate

- Double-sided silicone or equivalent anti-slip tread (bench traction testing needed).
- Washable textile body with breathability and durability targets.
- Compression-inspired weave; avoid declaring medical compression without pressure measurements and suitability screening.
- Thermal layer chosen for local climate, overheating risk and washability.
- Reusable removable electronics enclosure with safe fastening and electrical isolation.
