# IoT Environmental Station

A small ESP32-based environmental monitoring station that collects real sensor readings, sends them over Wi-Fi, stores them through a lightweight API, and visualizes trends in a web dashboard.

## Project goals

- Read temperature, humidity, pressure, and ambient light from physical sensors.
- Use an ESP32 as the edge sensor node.
- Send normalized readings over Wi-Fi to a small API.
- Store time-series measurements locally first.
- Build a clean dashboard for current conditions and historical trends.
- Keep the hardware and software modular so additional sensor nodes can be added later.

## Planned v1 hardware

- ESP-WROOM-32 / ESP32 development board
- BME280 temperature / humidity / pressure sensor
- BH1750 ambient light sensor
- Breadboard and jumper wires
- Micro-USB cable and 5V USB power source

A small OLED display is planned as a later upgrade. Air-quality sensing will be added after the first sensor pipeline is proven.

## Architecture

```text
BME280 + BH1750
       |
       v
     ESP32
       |
     Wi-Fi
       |
       v
   FastAPI API
       |
       v
     SQLite
       |
       v
React dashboard
```

During development, a mock sender stands in for the ESP32 so the API and persistence layer can be built before the hardware arrives.

## Repository layout

```text
iot-environmental-station/
├── firmware/       # ESP32 firmware (added during hardware bring-up)
├── server/         # API, persistence, and mock sensor sender
├── dashboard/      # Web dashboard
├── hardware/       # Wiring, pinout, photos, BOM
├── docs/           # Architecture and setup notes
└── README.md
```

## Milestones

### M1 — Mock telemetry pipeline

Run the local API, send simulated environmental readings, and persist them to SQLite.

### M2 — First real sensor reading

Connect the BME280 and BH1750 to the ESP32 and verify real readings over serial.

### M3 — ESP32 Wi-Fi telemetry

Send real sensor readings from the ESP32 to the API over Wi-Fi.

### M4 — Dashboard

Build a responsive dashboard showing station status, current readings, 24-hour trends, minima/maxima, and sensor health.

### M5 — Physical display and air quality

Add the OLED display and later one or more dedicated CO2, VOC, or particulate sensors.

## Status

**Current:** software pipeline development while hardware is in transit.

Next engineering checkpoint: run the mock sender against the API and confirm readings are persisted in SQLite.

## License

License decision pending.
