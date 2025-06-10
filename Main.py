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
MAX_DEVICES = 100

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
        # Update statuses of existing devices
        for device in devices:
            device["status"] = random.choice(["secure", "vulnerable", "offline"])
            device["last_seen"] = fake.date_time_between(start_date="-7d", end_date="now").isoformat()
        # Add a new fake device each cycle
        if len(devices) < MAX_DEVICES:
            devices.append({
                "name": fake.word().capitalize(),
                "ip": fake.ipv4_private(),
                "status": random.choice(["secure", "vulnerable", "offline"]),
                "type": random.choice(["Camera", "Router", "Thermostat", "Sensor", "Light", "Speaker"]),
                "last_seen": fake.date_time_between(start_date="-7d", end_date="now").isoformat()
            })


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

@app.get("/metrics")
def get_metrics():
    # Example metrics, adjust as needed
    secure = sum(1 for d in devices if d["status"] == "secure")
    vulnerable = sum(1 for d in devices if d["status"] == "vulnerable")
    offline = sum(1 for d in devices if d["status"] == "offline")
    return {
        "incidents": 7,  # Example static value
        "vulnerabilities": vulnerable,
        "alerts": 4,  # Example static value
        "secure": secure,
        "offline": offline
    }

@app.get("/device-types")
def get_device_types():
    types = {}
    for d in devices:
        t = d["type"]
        types[t] = types.get(t, 0) + 1
    return types

@app.get("/incidents")
def get_incidents():
    # Example: return a list of incident counts for a week
    return [random.randint(0, 5) for _ in range(7)]
