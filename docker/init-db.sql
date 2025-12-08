-- Minimal Marine Corrosion Database Schema
-- PostgreSQL initialization script

-- Create the main sensor data table
CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    unix_timestamp BIGINT NOT NULL,
    temperature DECIMAL(6, 2),
    relative_humidity DECIMAL(5, 2),
    corrosion_rate DECIMAL(8, 4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for time-based queries (most common query pattern)
CREATE INDEX IF NOT EXISTS idx_sensor_data_timestamp ON sensor_data(timestamp DESC);

-- Confirmation message
DO $$
BEGIN
    RAISE NOTICE 'Marine corrosion database initialized successfully!';
    RAISE NOTICE 'Table created: sensor_data';
END $$;
