# 🔌 Circuit Diagram | AI-Powered Smart Irrigation System

This document defines the electrical connections between the ESP32, DHT11 temperature/humidity sensor, analog soil-moisture sensor, active-LOW relay module, and irrigation pump.

---

## 📋 Table of Contents

1. [System Circuit Overview](#-system-circuit-overview)
2. [Circuit Block Diagram](#-circuit-block-diagram)
3. [Component List](#-component-list)
4. [ESP32 Pin Connections](#-esp32-pin-connections)
5. [DHT11 Circuit](#-dht11-circuit)
6. [Soil Moisture Sensor Circuit](#-soil-moisture-sensor-circuit)
7. [Relay Circuit](#-relay-circuit)
8. [Water Pump Circuit](#-water-pump-circuit)
9. [Complete Wiring Diagram](#-complete-wiring-diagram)
10. [Power Architecture](#-power-architecture)
11. [Relay Logic](#-relay-logic)
12. [Electrical Safety](#-electrical-safety)
13. [Testing Procedure](#-testing-procedure)
14. [Troubleshooting](#-troubleshooting)

---

# 📐 System Circuit Overview

The hardware consists of four major electrical subsystems:

```text
                    ┌──────────────────────┐
                    │       ESP32          │
                    │                      │
                    │ GPIO 4  ← DHT11      │
                    │ GPIO 34 ← Soil ADC   │
                    │ GPIO 26  → Relay     │
                    │                      │
                    │ 3.3V / GND           │
                    └──────────┬───────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
            ▼                  ▼                  ▼
      ┌──────────┐      ┌──────────────┐   ┌─────────────┐
      │  DHT11   │      │ Soil Sensor  │   │ Relay       │
      │          │      │              │   │ Module      │
      └──────────┘      └──────────────┘   └──────┬──────┘
                                                  │
                                                  ▼
                                            ┌──────────┐
                                            │   Pump   │
                                            └──────────┘
```

The ESP32 is responsible for all low-voltage sensing and relay control. The relay provides the switching interface between the ESP32 control signal and the pump's separate power circuit.

---

# 🧩 Circuit Block Diagram

```text
                         SMART IRRIGATION HARDWARE
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                         LOW-VOLTAGE CONTROL SIDE                             │
│                                                                              │
│   ┌──────────────┐                                                          │
│   │    DHT11     │                                                          │
│   │              │                                                          │
│   │ VCC          │                                                          │
│   │ DATA ──────────────── GPIO 4                                            │
│   │ GND          │                                                          │
│   └──────────────┘                                                          │
│                                                                              │
│   ┌────────────────────┐                                                     │
│   │ Soil Moisture      │                                                     │
│   │ Sensor             │                                                     │
│   │                    │                                                     │
│   │ VCC                │                                                     │
│   │ GND                │                                                     │
│   │ AO ───────────────────── GPIO 34                                        │
│   └────────────────────┘                                                     │
│                                                                              │
│   ┌─────────────────────────────────────┐                                    │
│   │              ESP32                  │                                    │
│   │                                     │                                    │
│   │ GPIO 4  ← DHT11                     │                                    │
│   │ GPIO 34 ← Soil Sensor               │                                    │
│   │ GPIO 26  → Relay IN                 │                                    │
│   │                                     │                                    │
│   └──────────────────┬──────────────────┘                                    │
│                      │                                                       │
│                      │ GPIO 26                                               │
│                      ▼                                                       │
│             ┌──────────────────┐                                             │
│             │ 5V Relay Module  │                                             │
│             │                  │                                             │
│             │ IN               │                                             │
│             │ VCC              │                                             │
│             │ GND              │                                             │
│             │                  │                                             │
│             │ COM              │──────────────┐                              │
│             │ NO               │              │                              │
│             └──────────────────┘              │                              │
│                                               │                              │
└───────────────────────────────────────────────┼──────────────────────────────┘
                                                │
                                                ▼
                                      EXTERNAL PUMP CIRCUIT
```

---

# 🧰 Component List

| Component | Quantity | Purpose |
|---|---:|---|
| ESP32 Dev Module | 1 | Main controller |
| DHT11 | 1 | Temperature/humidity sensing |
| Analog soil-moisture sensor | 1 | Soil moisture measurement |
| 5V single-channel relay | 1 | Pump switching |
| Water pump | 1 | Irrigation actuator |
| External pump power supply | 1 | Pump power |
| Jumper wires | As required | Connections |
| Breadboard / terminal blocks | As required | Low-voltage prototyping |
| Resistor | 1 | DHT11 pull-up if required |

---

# 📍 ESP32 Pin Connections

The project uses the following GPIO assignments:

| ESP32 GPIO | Connected Device | Signal |
|---:|---|---|
| GPIO 4 | DHT11 DATA | Digital input |
| GPIO 34 | Soil Sensor AO | Analog input |
| GPIO 26 | Relay IN | Digital output |
| 3.3V | Sensors | Sensor power where supported |
| GND | Sensors/relay | Common ground |

### Pin Summary

```text
GPIO 4
  └── DHT11 DATA

GPIO 34
  └── Soil Moisture AO

GPIO 26
  └── Relay IN
```

> **Note:** GPIO 34 is input-only on the ESP32, which makes it appropriate for an analog soil-moisture input.

---

# 🌡️ DHT11 Circuit

The DHT11 has three commonly used connections:

```text
DHT11
┌─────────────┐
│             │
│ VCC ────────┼──── ESP32 3.3V
│ DATA ───────┼──── ESP32 GPIO 4
│ GND ────────┼──── ESP32 GND
│             │
└─────────────┘
```

## Connection Table

| DHT11 Pin | ESP32 |
|---|---|
| VCC | 3.3V |
| DATA | GPIO 4 |
| GND | GND |

If using a **bare DHT11 sensor** rather than a breakout module, use the manufacturer's recommended pull-up resistor on the DATA line.

Example:

```text
3.3V
 │
[Pull-up]
 │
 ├──────── DATA → GPIO 4
 │
DHT11
```

---

# 💧 Soil Moisture Sensor Circuit

The analog soil sensor provides an analog voltage.

```text
Soil Moisture Sensor
┌────────────────────┐
│                    │
│ VCC ───────────────┼──── Power
│ GND ───────────────┼──── ESP32 GND
│ AO ────────────────┼──── ESP32 GPIO 34
│                    │
└────────────────────┘
```

Connection:

| Sensor Pin | ESP32 |
|---|---|
| VCC | Appropriate sensor supply |
| GND | GND |
| AO | GPIO 34 |

The ESP32 reads the analog value:

```text
ADC Reading
    ↓
0–4095
    ↓
Calibration
    ↓
Soil Moisture %
```

---

# ⚠️ Soil Sensor Voltage Compatibility

Before connecting the analog output directly to GPIO 34, verify the sensor's output voltage.

The ESP32 ADC input must remain within the electrical limits specified for the particular ESP32 board/chip.

If the sensor can output a voltage higher than the ESP32 ADC input can safely accept, use an appropriate voltage-divider or signal-conditioning circuit.

Do **not** connect an unknown higher-voltage analog output directly to the ESP32.

---

# ⚡ Relay Circuit

The relay module is controlled by GPIO 26.

```text
ESP32                         Relay Module
─────                         ────────────

GPIO 26 ────────────────────→ IN

GND ────────────────────────→ GND

5V supply ──────────────────→ VCC
```

The exact relay power arrangement depends on the relay module and its specifications.

## Connection Table

| Relay Pin | Connection |
|---|---|
| IN | ESP32 GPIO 26 |
| GND | Common low-voltage GND |
| VCC | Suitable 5V relay supply |
| COM | Pump power switching path |
| NO | Pump power switching path |

---

# 🔀 Relay Contact Configuration

The project uses the **Normally Open (NO)** relay contact.

Conceptually:

```text
Relay OFF:

COM ─────/ ───── NO
         OPEN

Pump → OFF
```

When the relay activates:

```text
Relay ON:

COM ──────── NO
         CLOSED

Pump → ON
```

This ensures that the pump's switched circuit is open when the relay is not energized.

---

# 🚰 Water Pump Circuit

The pump should use an **appropriate external power supply** rather than relying on the ESP32's 3.3V output.

Conceptual low-voltage pump arrangement:

```text
External Pump Supply (+)
          │
          │
          ▼
        COM
      ┌───────┐
      │ Relay │
      └───┬───┘
          │
          │ NO
          ▼
      Pump (+)

Pump (-)
   │
   ▼
External Pump Supply (-)
```

For a DC pump, this can be represented as:

```text
SUPPLY (+)
    │
    ▼
  COM
    │
  RELAY
    │
    ▼
   NO
    │
    ▼
 PUMP (+)
 PUMP (-)
    │
    ▼
SUPPLY (-)
```

---

# 🔌 Complete Wiring Diagram

```text
                             ESP32 DEV MODULE
                    ┌───────────────────────────┐
                    │                           │
                    │       ESP32               │
                    │                           │
                    │  3.3V ───────────┐       │
                    │                   │       │
                    │  GND ─────────────┼───┐   │
                    │                   │   │   │
                    │  GPIO 4 ◄─────────┼───┼───┼──── DHT11 DATA
                    │                   │   │   │
                    │  GPIO 34 ◄────────┼───┼─────── Soil Sensor AO
                    │                   │   │   │
                    │  GPIO 26 ─────────┼───┼─────── Relay IN
                    │                   │   │   │
                    └───────────────────┼───┼───┘
                                        │   │
                                        │   │
                         ┌──────────────┘   │
                         │                  │
                         ▼                  ▼
                    ┌─────────┐      ┌───────────────┐
                    │  DHT11  │      │ Soil Sensor   │
                    │         │      │               │
                    │ VCC ────┼──────┤ VCC           │
                    │ DATA ───┼──────┤ AO            │
                    │ GND ────┼──────┤ GND           │
                    └─────────┘      └───────────────┘


                         GPIO 26
                            │
                            ▼
                    ┌─────────────────┐
                    │ 5V RELAY MODULE │
                    │                 │
                    │ IN  ◄───────────┤
                    │ VCC ◄── 5V      │
                    │ GND ◄── GND     │
                    │                 │
                    │ COM ────────────┼──── External
                    │ NO  ────────────┼──── Pump circuit
                    └─────────────────┘
```

---

# 🔋 Power Architecture

The project contains two logical power domains.

```text
                  POWER SYSTEM
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
       CONTROL DOMAIN       PUMP DOMAIN
              │                 │
              ▼                 ▼
           ESP32           Pump Supply
              │                 │
       ┌──────┼──────┐          │
       │      │      │          │
       ▼      ▼      ▼          ▼
     DHT11  Soil   Relay       Pump
           Sensor
```

The pump should have its own appropriately rated supply.

The ESP32 should not be expected to directly supply the pump current.

---

# 🔋 Recommended Power Separation

```text
ESP32 USB / 5V
      │
      ├── ESP32
      │
      ├── DHT11
      │
      └── Sensors

Separate Pump Supply
      │
      └── Relay Contact
              │
              └── Pump
```

This reduces the risk of pump current transients interfering with the ESP32.

---

# 🔄 Relay Logic

The firmware should treat the relay as active-LOW.

| Desired Pump State | GPIO 26 | Relay | Pump |
|---|---:|---|---|
| OFF | HIGH | OFF | OFF |
| ON | LOW | ON | ON |

Conceptually:

```text
relayState = true
       ↓
GPIO.write(LOW)
       ↓
Pump ON
```

and:

```text
relayState = false
       ↓
GPIO.write(HIGH)
       ↓
Pump OFF
```

The firmware should initialize the relay GPIO to the **safe OFF state** before enabling normal operation.

---

# 🛑 Startup Safety

A recommended initialization sequence is:

```text
ESP32 Boot
    ↓
Configure GPIO 26 as OUTPUT
    ↓
Immediately write HIGH
    ↓
Relay OFF
    ↓
Initialize Sensors
    ↓
Connect Wi-Fi
    ↓
Start Control Loop
```

This prevents an unintended pump activation during startup.

---

# 🧯 Electrical Safety

The relay module should be selected according to the pump's voltage, current, and switching requirements.

For higher-power or mains-powered pumps:

- Do not build exposed mains wiring on a breadboard.
- Use an appropriately rated enclosure.
- Use suitable fusing and circuit protection.
- Maintain proper creepage and clearance.
- Use appropriately rated relay/contactors.
- Keep low-voltage control wiring physically separated from hazardous-voltage wiring.
- Ensure proper grounding where applicable.
- Have mains-voltage installation performed by a qualified person.

The ESP32 GPIO must **never** be connected directly to a pump.

The correct architecture is:

```text
ESP32
  ↓
Relay Driver / Relay Module
  ↓
Relay Contacts
  ↓
External Pump Power Circuit
  ↓
Pump
```

---

# 🧪 Circuit Testing Procedure

The hardware should be tested incrementally.

## Step 1 — ESP32

Verify:

```text
ESP32 powers on
Serial monitor works
Wi-Fi connection works
```

---

## Step 2 — DHT11

Verify:

```text
Temperature reading
Humidity reading
```

Expected output:

```text
Temperature: XX.X °C
Humidity: XX.X %
```

---

## Step 3 — Soil Moisture Sensor

Read the ADC value:

```text
ADC = 0–4095
```

Test the sensor under:

```text
Dry soil
Moist soil
Wet soil
```

Record the readings and calibrate the conversion to percentage.

---

## Step 4 — Relay

Test the relay independently.

```text
GPIO 26 = HIGH
→ Relay OFF
```

Then:

```text
GPIO 26 = LOW
→ Relay ON
```

Do this **without connecting the pump initially**.

---

## Step 5 — Pump

After confirming relay operation:

```text
External Supply
      ↓
Relay
      ↓
Pump
```

Verify:

```text
Relay ON  → Pump ON
Relay OFF → Pump OFF
```

---

## Step 6 — Complete System

Finally test:

```text
Sensors
   ↓
ESP32
   ↓
Backend
   ↓
ML
   ↓
Relay
   ↓
Pump
```

---

# 🐛 Troubleshooting

## DHT11 Returns Invalid Data

Check:

```text
DHT11 VCC
DHT11 GND
DHT11 DATA
GPIO 4 configuration
Pull-up resistor if required
```

---

## Soil Moisture Always Reads 0 or 4095

Check:

```text
Sensor power
Sensor GND
AO connection
GPIO 34 configuration
ADC voltage range
Sensor calibration
```

---

## Relay Does Not Activate

Check:

```text
GPIO 26
Relay VCC
Relay GND
Relay trigger logic
Relay module compatibility
```

Remember:

```text
Active LOW:
LOW  = ON
HIGH = OFF
```

---

## Pump Does Not Turn On

Check the pump circuit independently of the ESP32:

```text
External power supply
      ↓
Fuse/protection
      ↓
Relay COM
      ↓
Relay NO
      ↓
Pump
```

Also verify that the relay contacts are rated for the pump's electrical load.

---

## ESP32 Resets When Pump Starts

Possible causes include:

```text
Voltage drop
Power-supply instability
Pump startup current
Electrical noise
Poor grounding
Insufficient power supply
```

Recommended mitigation:

```text
Separate pump and ESP32 power supplies
        +
Proper relay isolation
        +
Adequate power regulation
        +
Appropriate suppression/protection
```

For DC inductive loads, suitable suppression components may be required according to the pump and switching topology.

---

# 📌 Final Pinout

```text
┌─────────────────────────────────────────────┐
│              ESP32 PINOUT                   │
├─────────────────────────────────────────────┤
│                                             │
│ GPIO 4   → DHT11 DATA                      │
│ GPIO 34  ← Soil Moisture Analog Output     │
│ GPIO 26  → Relay IN                        │
│                                             │
│ 3.3V     → Sensor supply where supported  │
│ GND      → Common low-voltage ground      │
│                                             │
└─────────────────────────────────────────────┘
```

---

# 🏁 Complete Hardware Signal Flow

```text
             ENVIRONMENT
                  │
                  ▼
        ┌──────────────────┐
        │      DHT11       │
        │ Temperature      │
        │ Humidity         │
        └────────┬─────────┘
                 │
                 │ GPIO 4
                 ▼
        ┌──────────────────┐
        │                  │
        │      ESP32       │
        │                  │
        └────────┬─────────┘
                 ▲
                 │ GPIO 34
                 │
        ┌────────┴─────────┐
        │ Soil Moisture    │
        │ Sensor           │
        └──────────────────┘

                 ESP32
                   │
                   │ GPIO 26
                   ▼
            ┌─────────────┐
            │   RELAY     │
            └──────┬──────┘
                   │
                   │ NO Contact
                   ▼
            ┌─────────────┐
            │    PUMP     │
            └──────┬──────┘
                   │
                   ▼
                IRRIGATION
                   │
                   ▼
                 SOIL
                   │
                   └──────────→ Next Sensor Reading
```

---

# 🔑 Design Principle

The hardware architecture follows one fundamental principle:

> **The ESP32 handles sensing and low-voltage control; the relay provides the switching interface; the pump operates from its own appropriately rated power circuit.**

This separation makes the hardware architecture suitable for integrating the ESP32 edge node with the backend, machine-learning inference engine, and live irrigation dashboard.
