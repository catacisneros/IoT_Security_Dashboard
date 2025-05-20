# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/metrics")
def get_metrics():
    return {"incidents": 24, "vulnerabilities": 123, "alerts": 5}

@app.get("/device-types")
def get_device_types():
    return {"Cameras": 35, "Industrial": 25, "Router": 20, "Other": 20}

@app.get("/incidents")
def get_incident_trend():
    return [2, 4, 3, 6, 5, 11, 9]

@app.get("/devices")
def get_devices():
    return {"secure": 1250, "vulnerable": 86, "offline": 12}

@app.get("/alerts")
def get_alerts():
    return [
        {"type": "Malware Infection", "risk": "HIGH", "device": "Camera 032", "time": "Today, 11:30"},
        {"type": "Vulnerability Detected", "risk": "MEDIUM", "device": "Router 12", "time": "Today, 09:15"},
        {"type": "Unauthorized Access", "risk": "HIGH", "device": "Sensor 07", "time": "Yesterday, 17:20"},
        {"type": "Failed Login Attempt", "risk": "LOW", "device": "Thermostat 2", "time": "Yesterday, 06:45"},
    ]
