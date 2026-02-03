from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uuid
from datetime import datetime
from enum import Enum
import uvicorn

app = FastAPI(title="Telemetry Service", version="1.0.0")


# Модели данных
class MetricType(str, Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    POWER = "power"
    MOTION = "motion"
    LIGHT = "light"


class TelemetryData(BaseModel):
    telemetry_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    device_id: str
    metric_type: MetricType
    value: float
    unit: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Dict = {}


class TelemetryQuery(BaseModel):
    device_id: Optional[str] = None
    metric_type: Optional[MetricType] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


# In-memory хранилище (для MVP)
telemetry_db = []


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "telemetry"}


@app.post("/telemetry", status_code=201)
async def create_telemetry(data: TelemetryData):
    telemetry_db.append(data)
    return {
        "message": "Telemetry data created",
        "telemetry_id": data.telemetry_id,
        "device_id": data.device_id
    }


@app.get("/telemetry", response_model=List[TelemetryData])
async def get_telemetry(
    device_id: Optional[str] = None,
    metric_type: Optional[str] = None,
    limit: int = 100
):
    results = telemetry_db

    if device_id:
        results = [t for t in results if t.device_id == device_id]

    if metric_type:
        results = [t for t in results if t.metric_type.value == metric_type]

    # Сортировка по времени (новые первыми)
    results.sort(key=lambda x: x.timestamp, reverse=True)

    return results[:limit]


@app.get("/telemetry/{device_id}/latest")
async def get_latest_telemetry(device_id: str):
    device_data = [t for t in telemetry_db if t.device_id == device_id]

    if not device_data:
        raise HTTPException(
            status_code=404, detail="No telemetry data found for device"
            )

    # Группируем по типу метрики
    latest_by_type = {}
    for data in device_data:
        metric_type = data.metric_type

        if metric_type not in latest_by_type:
            latest_by_type[metric_type] = data
        elif data.timestamp > latest_by_type[metric_type].timestamp:
            latest_by_type[metric_type] = data

    return {
        "device_id": device_id,
        "latest": {k.value: v for k, v in latest_by_type.items()}
    }


@app.get("/telemetry/{device_id}/stats")
async def get_telemetry_stats(device_id: str, metric_type: str):
    device_data = [
        t for t in telemetry_db
        if t.device_id == device_id and t.metric_type.value == metric_type
    ]

    if not device_data:
        raise HTTPException(status_code=404, detail="No data found")

    values = [t.value for t in device_data]

    return {
        "device_id": device_id,
        "metric_type": metric_type,
        "count": len(values),
        "average": sum(values) / len(values),
        "min": min(values),
        "max": max(values),
        "latest": device_data[0].value if device_data else None
    }


@app.post("/telemetry/bulk", status_code=201)
async def create_bulk_telemetry(data: List[TelemetryData]):
    telemetry_db.extend(data)
    return {
        "message": f"Created {len(data)} telemetry records",
        "count": len(data)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8083)
