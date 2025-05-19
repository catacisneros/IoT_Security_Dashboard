from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine, Session, select
from typing import Optional, List

app = FastAPI()

# Define the Device table
class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    ip: str
    location: str

# Create database engine
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

# Create the table if not exists
SQLModel.metadata.create_all(engine)

# Routes

@app.post("/devices")
def create_device(device: Device):
    with Session(engine) as session:
        session.add(device)
        session.commit()
        session.refresh(device)
        return device

@app.get("/devices", response_model=List[Device])
def read_devices():
    with Session(engine) as session:
        return session.exec(select(Device)).all()
