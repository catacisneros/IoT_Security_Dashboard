from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
import time, random
from faker import Faker
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Device type templates for more realistic names
device_templates = {
    "Camera": ["Security Camera", "IP Camera", "Surveillance Camera", "PTZ Camera", "Dome Camera"],
    "Router": ["WiFi Router", "Gateway Router", "Edge Router", "Core Router", "Access Router"],
    "Thermostat": ["Smart Thermostat", "WiFi Thermostat", "Learning Thermostat", "Programmable Thermostat"],
    "Sensor": ["Motion Sensor", "Temperature Sensor", "Humidity Sensor", "Pressure Sensor", "Light Sensor"],
    "Light": ["Smart Bulb", "LED Strip", "Smart Switch", "Dimmer Switch", "Motion Light"],
    "Speaker": ["Smart Speaker", "Bluetooth Speaker", "WiFi Speaker", "Home Assistant", "Audio Hub"]
}

# Generate initial fake devices
for _ in range(20):
    device_type = random.choice(list(device_templates.keys()))
    device_name = random.choice(device_templates[device_type])
    devices.append({
        "name": f"{device_name} {fake.building_number()}",
        "ip": fake.ipv4_private(),
        "status": random.choice(["secure", "vulnerable", "offline"]),
        "type": device_type,
        "last_seen": fake.date_time_between(start_date="-7d", end_date="now").isoformat()
    })

# Background thread to update device statuses and add new devices
def simulate_updates():
    while True:
        try:
            time.sleep(5)
            logger.info(f"Updating devices. Current count: {len(devices)}")
            
            # Update statuses of existing devices with weighted probabilities
            for device in devices:
                # 60% secure, 25% vulnerable, 15% offline for more realistic distribution
                weights = [0.6, 0.25, 0.15]
                device["status"] = random.choices(["secure", "vulnerable", "offline"], weights=weights)[0]
                device["last_seen"] = fake.date_time_between(start_date="-7d", end_date="now").isoformat()
            
            # Add a new fake device each cycle if under max
            if len(devices) < MAX_DEVICES:
                device_type = random.choice(list(device_templates.keys()))
                device_name = random.choice(device_templates[device_type])
                new_device = {
                    "name": f"{device_name} {fake.building_number()}",
                    "ip": fake.ipv4_private(),
                    "status": random.choice(["secure", "vulnerable", "offline"]),
                    "type": device_type,
                    "last_seen": fake.date_time_between(start_date="-7d", end_date="now").isoformat()
                }
                devices.append(new_device)
                logger.info(f"Added new device: {new_device['name']} ({new_device['ip']})")
            
        except Exception as e:
            logger.error(f"Error in simulation thread: {e}")

@app.on_event("startup")
def start_simulation():
    Thread(target=simulate_updates, daemon=True).start()
    logger.info("IoT Security Dashboard backend started")

# API endpoint for devices
@app.get("/devices")
def get_devices():
    return devices

# Optional: fake alert data (same idea)
@app.get("/alerts")
def get_alerts():
    alert_types = [
        "Malware Infection", "Vulnerability Detected", "Unauthorized Access", 
        "Failed Login Attempt", "Suspicious Activity", "Data Breach Attempt",
        "DDoS Attack", "Port Scan Detected", "Rogue Device", "Configuration Drift"
    ]
    
    # Generate dynamic alerts based on current device status
    alerts = []
    for device in devices:
        if device["status"] == "vulnerable" and random.random() < 0.3:
            alerts.append({
                "type": random.choice(alert_types),
                "risk": random.choice(["HIGH", "MEDIUM", "LOW"]),
                "device": device["name"],
                "time": fake.date_time_between(start_date="-1d", end_date="now").strftime("%Y-%m-%d %H:%M")
            })
    
    # Ensure we always have some alerts
    if not alerts:
        alerts = [
            {"type": "System Scan", "risk": "LOW", "device": "Network Monitor", "time": "Today, 10:00"},
            {"type": "Routine Check", "risk": "LOW", "device": "Security Scanner", "time": "Today, 09:30"}
        ]
    
    return alerts[:10]  # Return max 10 alerts

@app.get("/metrics")
def get_metrics():
    # Calculate metrics based on current device status
    secure = sum(1 for d in devices if d["status"] == "secure")
    vulnerable = sum(1 for d in devices if d["status"] == "vulnerable")
    offline = sum(1 for d in devices if d["status"] == "offline")
    
    # Generate realistic incident counts
    total_incidents = vulnerable + random.randint(0, 3)
    total_alerts = len([d for d in devices if d["status"] == "vulnerable"]) + random.randint(1, 5)
    
    return {
        "incidents": total_incidents,
        "vulnerabilities": vulnerable,
        "alerts": total_alerts,
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
    # Generate weekly incident data with some variation
    base_incidents = [random.randint(1, 3) for _ in range(7)]
    # Add some weekly pattern (more incidents on weekdays)
    for i in range(7):
        if i < 5:  # Weekdays
            base_incidents[i] += random.randint(0, 2)
        else:  # Weekends
            base_incidents[i] = max(0, base_incidents[i] - 1)
    return base_incidents

@app.get("/health")
def health_check():
    return {"status": "healthy", "device_count": len(devices), "timestamp": time.time()}
