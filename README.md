# Stadium IoT Sensor Simulator

A Python-based simulator that generates synthetic IoT sensor readings for eight stadiums in Qatar. It simulates sensor activity across different stadium zones and continuously prints generated readings as JSON events.

## Overview

The simulator generates synthetic telemetry for stadium environments, including:

* Temperature
* Crowd density
* CO₂ levels
* Power consumption
* Vibration

Each reading includes details such as the stadium, sensor, zone, timestamp, measurement value, unit, and anomaly indicator.

## Stadiums

The simulator includes the following eight stadiums:

* Lusail Stadium
* Al Bayt Stadium
* Ahmad Bin Ali Stadium
* Al Janoub Stadium
* Education City Stadium
* Khalifa International Stadium
* Stadium 974
* Al Thumama Stadium

## Sensor Zones

Sensors are assigned to different zones within each stadium:

| Zone          | Sensor Types                    |
| ------------- | ------------------------------- |
| North Stand   | Temperature, Crowd Density, CO₂ |
| South Stand   | Temperature, Crowd Density, CO₂ |
| VIP Area      | Temperature, CO₂                |
| Main Entrance | Crowd Density                   |
| Plant Room    | Power, Vibration                |

Each stadium has 11 sensor instances, for a total of 88 simulated sensors across all eight stadiums.

## Project Structure

```text
stadium-iot-simulator/
├── config.py
├── sensor_generator.py
├── main.py
├── .gitignore
└── README.md
```

| File                  | Description                                                  |
| --------------------- | ------------------------------------------------------------ |
| `config.py`           | Defines stadiums, zones, sensor types, ranges, and intervals |
| `sensor_generator.py` | Generates synthetic sensor readings                          |
| `main.py`             | Runs the simulation and prints generated readings            |
| `.gitignore`          | Specifies files Git should ignore                            |

## Requirements

* Python 3.10 or later
* No external Python packages required

## Run the Simulator

Clone the repository:

```bash
git clone https://github.com/faizal4757/stadium-iot-simulator.git
```

Navigate to the project directory:

```bash
cd stadium-iot-simulator
```

Run the simulator:

```bash
python main.py
```

On Windows, you can also use:

```powershell
py main.py
```

The simulator runs continuously until stopped with `Ctrl+C`.

## Sample Output

Each sensor reading is printed as a JSON event.

```json
{
  "event_id": "a1b2c3d4-5678-4abc-9def-123456789abc",
  "stadium_id": "LUSAIL",
  "stadium_name": "Lusail Stadium",
  "sensor_id": "LUSAIL-NORTH_STAND-TEMPERATURE-001",
  "sensor_type": "temperature",
  "zone": "north_stand",
  "timestamp": "2026-10-03T08:30:00+00:00",
  "value": 27.45,
  "unit": "C",
  "is_anomaly": false
}
```

*Values and timestamps are illustrative.*

## Simulation Behaviour

* Generates readings for sensors across all configured stadiums and zones.
* Uses configurable sensor measurement ranges and generation intervals.
* Simulates relationships between crowd density, temperature, and CO₂ levels.
* Generates occasional anomalous readings and marks them with `is_anomaly`.
* Prints each reading as a JSON event to the console.

## Technology

* **Language:** Python
* **Data format:** JSON
* **Dependencies:** Python standard library

## Scope

This repository is limited to synthetic stadium sensor data generation. It does not connect to physical sensors, stream data to external services, store readings in a database, or perform downstream data processing.

The generated data is intended for learning, experimentation, and development of data engineering projects. It is not real stadium telemetry and is not intended for operational or safety-critical use.

## Author

**Faizal Ahmed**

GitHub: https://github.com/faizal4757
