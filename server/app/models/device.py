CREATE_DEVICES_TABLE = """
CREATE TABLE IF NOT EXISTS devices (
    id BIGSERIAL PRIMARY KEY,

    device_uuid UUID NOT NULL UNIQUE,

    hostname TEXT NOT NULL,

    serial_number TEXT,

    os_name TEXT,
    os_version TEXT,
    os_build TEXT,

    cpu TEXT,
    ram_bytes BIGINT,
    gpu TEXT,

    network_interfaces JSONB NOT NULL DEFAULT '[]'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""