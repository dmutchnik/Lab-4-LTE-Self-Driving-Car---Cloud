import json
import random
from datetime import datetime, timedelta

def generate_sensor_data(device_id: int) -> dict:
    locations = [
        "kitchen", "bedroom", "garage", "office", "bathroom",
        "attic", "basement", "garden", "balcony", "hallway"
    ]
    location = random.choice(locations)
    status = random.choice(["active", "inactive"])

    # Generate two timestamps, one hour apart
    base_time = datetime(2023, 10, 1, 10, 0)
    timestamps = [base_time.isoformat() + "Z", (base_time + timedelta(hours=1)).isoformat() + "Z"]

    readings = [
        {
            "timestamp": timestamps[0],
            "temperature": round(random.uniform(15, 25), 1),
            "humidity": random.randint(40, 80)
        },
        {
            "timestamp": timestamps[1],
            "temperature": round(random.uniform(15, 25), 1),
            "humidity": random.randint(40, 80)
        }
    ]

    return {
        "device": {
            "id": str(device_id),
            "type": "sensor",
            "location": location
        },
        "readings": readings,
        "status": status
    }

def generate_data(count: int = 500) -> list:
    return [generate_sensor_data(12346 + i) for i in range(count)]

if __name__ == "__main__":
    data = generate_data(500)

    with open("sample_data.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Generated 500 records and saved to sample_data.json")
