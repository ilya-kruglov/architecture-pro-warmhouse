from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import uvicorn

app = FastAPI(title="Device Management Service", version="1.0.0")


# Модели данных
class Device(BaseModel):
    device_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    device_type: str  # "thermostat", "light", "camera", "sensor"
    location: str
    status: str = "offline"
    metadata: dict = {}
    created_at: datetime = Field(default_factory=datetime.now)
    last_seen: Optional[datetime] = None


class DeviceCreate(BaseModel):
    name: str
    device_type: str
    location: str
    metadata: Optional[dict] = {}


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    metadata: Optional[dict] = None


# In-memory хранилище (для MVP)
devices_db = {}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "device-management"}


@app.get("/devices", response_model=List[Device])
async def get_all_devices():
    return list(devices_db.values())


@app.get("/devices/{device_id}", response_model=Device)
async def get_device(device_id: str):
    if device_id not in devices_db:
        raise HTTPException(status_code=404, detail="Device not found")
    return devices_db[device_id]


@app.post("/devices", response_model=Device, status_code=201)
async def create_device(device: DeviceCreate):
    new_device = Device(
        name=device.name,
        device_type=device.device_type,
        location=device.location,
        metadata=device.metadata or {}
    )
    devices_db[new_device.device_id] = new_device
    return new_device


@app.put("/devices/{device_id}", response_model=Device)
async def update_device(device_id: str, update: DeviceUpdate):
    if device_id not in devices_db:
        raise HTTPException(status_code=404, detail="Device not found")

    device = devices_db[device_id]
    update_data = update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(device, field, value)

    devices_db[device_id] = device
    return device


@app.delete("/devices/{device_id}", status_code=204)
async def delete_device(device_id: str):
    if device_id not in devices_db:
        raise HTTPException(status_code=404, detail="Device not found")

    del devices_db[device_id]
    return


@app.patch("/devices/{device_id}/status")
async def update_device_status(device_id: str, status: str):
    if device_id not in devices_db:
        raise HTTPException(status_code=404, detail="Device not found")

    devices_db[device_id].status = status
    devices_db[device_id].last_seen = datetime.now()

    return {"message":
            "Device status updated",
            "device_id": device_id,
            "status": status
            }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)
