from pydantic import BaseModel, Field


class OSInfo(BaseModel):
    name: str | None = None
    version: str | None = None
    build: str | None = None


class HardwareInfo(BaseModel):
    cpu: str | None = None
    ram_bytes: int | None = None
    gpu: str | None = None


class NetworkInterface(BaseModel):
    name: str

    mac_address: str | None = None

    ipv4: list[str] = Field(
        default_factory=list
    )

    ipv6: list[str] = Field(
        default_factory=list
    )


class DeviceCreate(BaseModel):
    device_uuid: str
    hostname: str

    serial_number: str | None = None

    os: OSInfo | None = None

    hardware: HardwareInfo | None = None

    network: list[NetworkInterface] = Field(
        default_factory=list
    )


class DeviceResponse(DeviceCreate):
    id: int
    created_at: str | None = None