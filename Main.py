from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
import time, random
from faker import Faker

app = FastAPI()

# Allow frontend (React) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake = Faker()
devices = []

# Generate initial fake devices

for _ in range(20):
    devices.append({
        "name": fake.word().capitalize(),
        "ip": fake.ipv4_private(),
        "status": random.choice(["secure", "vulnerable", "offline"]),
        "type": random.choice(["Camera", "Router", "Thermostat"]),
        "last_seen": fake.date_time_between(start_date="-7d", end_date="now").isoformat()
    })


# Background thread to update device statuses
def simulate_updates():
    while True:
        time.sleep(5)
        for device in devices:
            device["status"] = random.choice(["secure", "vulnerable", "offline"])
            device["last_seen"] = fake.date_time_between(start_date="-7d", end_date="now").isoformat()


@app.on_event("startup")
def start_simulation():
    Thread(target=simulate_updates, daemon=True).start()

# API endpoint for devices
@app.get("/devices")
def get_devices():
    return devices

# Optional: fake alert data (same idea)
@app.get("/alerts")
def get_alerts():
    return [
        {"type": "Malware Infection", "risk": "HIGH", "device": "Camera 032", "time": "Today, 11:30"},
        {"type": "Vulnerability Detected", "risk": "MEDIUM", "device": "Router 12", "time": "Today, 09:15"},
        {"type": "Unauthorized Access", "risk": "HIGH", "device": "Sensor 07", "time": "Yesterday, 17:20"},
        {"type": "Failed Login Attempt", "risk": "LOW", "device": "Thermostat 2", "time": "Yesterday, 06:45"},
    ]
