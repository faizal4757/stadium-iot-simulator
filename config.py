import time
import json
import random
import uuid
from datetime import datetime, timezone


# Qatar FIFA World Cup 2022 stadiums
STADIUMS = {
    "LUSAIL": {
        "stadium_name": "Lusail Stadium",
        "city": "Lusail",
        "capacity": 88966
    },
    "AL_BAYT": {
        "stadium_name": "Al Bayt Stadium",
        "city": "Al Khor",
        "capacity": 68895
    },
    "AHMAD_BIN_ALI": {
        "stadium_name": "Ahmad Bin Ali Stadium",
        "city": "Al Rayyan",
        "capacity": 45032
    },
    "AL_JANOUB": {
        "stadium_name": "Al Janoub Stadium",
        "city": "Al Wakrah",
        "capacity": 44325
    },
    "EDUCATION_CITY": {
        "stadium_name": "Education City Stadium",
        "city": "Al Rayyan",
        "capacity": 44667
    },
    "KHALIFA_INTERNATIONAL": {
        "stadium_name": "Khalifa International Stadium",
        "city": "Doha",
        "capacity": 45857
    },
    "STADIUM_974": {
        "stadium_name": "Stadium 974",
        "city": "Doha",
        "capacity": 44089
    },
    "AL_THUMAMA": {
        "stadium_name": "Al Thumama Stadium",
        "city": "Doha",
        "capacity": 44400
    }
}


# Sensor definitions by stadium zone
ZONE_SENSORS = {
    "north_stand": [
        {
            "sensor_type": "temperature",
            "unit": "celsius",
            "min": 24,
            "max": 32,
            "interval": 5
        },
        {
            "sensor_type": "crowd_density",
            "unit": "people_per_m2",
            "min": 0,
            "max": 4,
            "interval": 2
        },
        {
            "sensor_type": "co2",
            "unit": "ppm",
            "min": 400,
            "max": 1200,
            "interval": 10
        }
    ],
    "south_stand": [
        {
            "sensor_type": "temperature",
            "unit": "celsius",
            "min": 24,
            "max": 32,
            "interval": 5
        },
        {
            "sensor_type": "crowd_density",
            "unit": "people_per_m2",
            "min": 0,
            "max": 4,
            "interval": 2
        },
        {
            "sensor_type": "co2",
            "unit": "ppm",
            "min": 400,
            "max": 1200,
            "interval": 10
        }
    ],
    "vip_area": [
        {
            "sensor_type": "temperature",
            "unit": "celsius",
            "min": 22,
            "max": 28,
            "interval": 5
        },
        {
            "sensor_type": "co2",
            "unit": "ppm",
            "min": 400,
            "max": 1000,
            "interval": 10
        }
    ],
    "main_entrance": [
        {
            "sensor_type": "crowd_density",
            "unit": "people_per_m2",
            "min": 0,
            "max": 4,
            "interval": 2
        }
    ],
    "plant_room": [
        {
            "sensor_type": "power",
            "unit": "kw",
            "min": 100,
            "max": 500,
            "interval": 3
        },
        {
            "sensor_type": "vibration",
            "unit": "mm/s",
            "min": 0.5,
            "max": 5,
            "interval": 1
        }
    ]
}


# Generate sensor instances for every stadium and zone
SENSORS = []

for stadium_id in STADIUMS:
    for zone, sensor_definitions in ZONE_SENSORS.items():
        for index, definition in enumerate(sensor_definitions, start=1):
            sensor_type = definition["sensor_type"]

            SENSORS.append({
                "sensor_id": (
                    f"{stadium_id}-{zone.upper()}-"
                    f"{sensor_type.upper()}-{index:03d}"
                ),
                "stadium_id": stadium_id,
                "sensor_type": sensor_type,
                "zone": zone,
                "unit": definition["unit"],
                "min": definition["min"],
                "max": definition["max"],
                "interval": definition["interval"]
            })