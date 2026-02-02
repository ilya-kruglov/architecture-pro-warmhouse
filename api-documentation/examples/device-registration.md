### Пример 1: Регистрация нового устройства
```
POST /api/v1/devices
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "serial_number": "SN-THERMO-001",
  "device_type": "thermostat",
  "name": "Термостат в гостиной",
  "location": "Гостиная",
  "household_id": "123e4567-e89b-12d3-a456-426614174000",
  "metadata": {
    "manufacturer": "WarmHouse",
    "firmware": "2.1.0"
  }
}
```
#### Ответ (201 Created):
```
{
  "device_id": "550e8400-e29b-41d4-a716-446655440000",
  "serial_number": "SN-THERMO-001",
  "name": "Термостат в гостиной",
  "device_type": "thermostat",
  "location": "Гостиная",
  "status": "online",
  "last_seen": "2026-01-15T14:30:00Z",
  "created_at": "2026-01-15T14:30:00Z",
  "household": {
    "household_id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Мой дом"
  }
}
```