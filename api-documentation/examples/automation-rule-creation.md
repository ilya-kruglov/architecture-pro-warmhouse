### Пример 2: Создание правила автоматизации
```
POST /api/v1/rules
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "name": "Включить свет при движении",
  "description": "Включать свет в коридоре при обнаружении движения",
  "household_id": "123e4567-e89b-12d3-a456-426614174000",
  "triggers": [
    {
      "type": "device",
      "device_id": "sensor-001",
      "event_type": "motion_detected"
    }
  ],
  "actions": [
    {
      "type": "device_command",
      "target": "light-001",
      "command": "turn_on",
      "delay_seconds": 0
    }
  ],
  "is_active": true
}
```