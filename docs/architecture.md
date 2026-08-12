# Architecture

## Design principle

The environmental station is local-first: sensor acquisition, storage, and local viewing should continue to work when internet connectivity is unavailable.

## Planned data flow

```text
Physical environment
       |
       v
BME280 / BH1750
       |
       v
I2C on Le Potato
       |
       v
Python collector
       |
       +--> local persistence
       |
       v
API
       |
       v
Web dashboard
```

## Components

### Collector
Owns hardware communication, sensor polling, validation, timestamps, and normalized readings.

### Persistence
Stores timestamped measurements locally. The initial implementation should favor simplicity; the storage choice will be finalized when the collector is working on real hardware.

### API
Provides current station status and historical measurements without exposing hardware-specific details to the dashboard.

### Dashboard
Displays current readings, trends, station health, and eventually air-quality information.

## Future extension

Optional cloud synchronization may replicate selected readings for a remotely accessible public demo, while the physical station remains independently functional.
