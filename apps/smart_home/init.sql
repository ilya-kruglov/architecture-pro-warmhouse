-- This script runs in the smarthome database (already created by POSTGRES_DB env var)

-- Create the sensors table if it doesn't exist
CREATE TABLE IF NOT EXISTS sensors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    location VARCHAR(100) NOT NULL,
    value FLOAT DEFAULT 0,
    unit VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'inactive',
    last_updated TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_sensors_type ON sensors(type);
CREATE INDEX IF NOT EXISTS idx_sensors_location ON sensors(location);
CREATE INDEX IF NOT EXISTS idx_sensors_status ON sensors(status);

-- Insert some sample data for testing (only if table is empty)
INSERT INTO sensors (name, type, location, unit, status) 
SELECT 'Living Room Temperature', 'temperature', 'Living Room', '°C', 'active'
WHERE NOT EXISTS (SELECT 1 FROM sensors WHERE location = 'Living Room');

INSERT INTO sensors (name, type, location, unit, status) 
SELECT 'Bedroom Temperature', 'temperature', 'Bedroom', '°C', 'active'
WHERE NOT EXISTS (SELECT 1 FROM sensors WHERE location = 'Bedroom');

INSERT INTO sensors (name, type, location, unit, status) 
SELECT 'Kitchen Temperature', 'temperature', 'Kitchen', '°C', 'active'
WHERE NOT EXISTS (SELECT 1 FROM sensors WHERE location = 'Kitchen');