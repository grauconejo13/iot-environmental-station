# IoT Environmental Station

A local-first environmental monitoring station built around the Libre Computer AML-S905X-CC (Le Potato). The project will collect real sensor readings at the edge, persist them locally, expose them through an API, and visualize trends in a web dashboard.

## Project goals

- Read real environmental data from sensors connected to a Le Potato.
- Keep the station functional without cloud connectivity.
- Store time-series measurements locally.
- Expose sensor data through a small API.
- Build a clean web dashboard for current conditions and historical trends.
- Document wiring, Linux setup, architecture, and hardware decisions publicly.

## Planned v1 hardware

- Libre Computer AML-S905X-CC (Le Potato)
- BME280 temperature / humidity / pressure sensor
- BH1750 ambient light sensor
- Breadboard and jumper wires
- microSD card and stable power supply

Air-quality sensing will be added after the first sensor pipeline is proven.

## Architecture

```text
BME280 + BH1750
       |
       v
   Le Potato
       |
       v
Python sensor collector
       |
       v
Local database
       |
       v
      API
       |
       v
React dashboard
```

The first version is intentionally local-first. Cloud synchronization can be added later without becoming a dependency for basic station operation.

## Repository layout

```text
iot-environmental-station/
├── collector/      # Sensor acquisition and normalization
├── server/         # API and persistence layer
├── dashboard/      # Web dashboard
├── hardware/       # Wiring, pinout, photos, BOM
├── docs/           # Architecture and setup notes
└── README.md
```

## Milestones

### M1 — First real sensor reading

Le Potato boots, I2C is enabled, the BME280 is detected, and a Python script prints a real temperature/humidity/pressure reading.

### M2 — Sensor collector

Create a modular collector that reads BME280 and BH1750 measurements and normalizes them into timestamped records.

### M3 — Local persistence + API

Persist readings locally and expose current and historical measurements through an API.

### M4 — Dashboard

Build a responsive dashboard showing station status, current readings, 24-hour trends, minima/maxima, and sensor health.

### M5 — Air quality

Add one or more dedicated CO2, VOC, or particulate sensors after the core station is stable.

## Status

**Current:** project foundation / hardware bring-up.

Next engineering checkpoint: obtain the first verified BME280 reading from the Le Potato.

## License

License decision pending.
