from dataclasses import dataclass, field

@dataclass
class OSInfo:
    name:str | None = None
    version:str | None = None
    build:str | None = None

    def to_dict(self)->dict:
        return {
            "name": self.name,
            "version": self.version,
            "build": self.build
        }


@dataclass
class HardwareInfo:
    cpu:str | None = None
    ram_bytes: int | None = None
    gpu: str | None = None

    def to_dict(self) -> dict:
        return {
            "cpu": self.cpu,
            "ram_bytes": self.ram_bytes,
            "gpu": self.gpu,
        }

@dataclass
class NetworkInterface:
    name:str
    mac_address:str | None = None
    ipv4: list[str] = field(default_factory=list)
    ipv6:list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "mac_address": self.mac_address,
            "ipv4": self.ipv4,
            "ipv6": self.ipv6,
        }

@dataclass
class Device:
    device_uuid:str
    hostname:str
    serial_number: str | None

    os:OSInfo
    hardware: HardwareInfo
    network: list[NetworkInterface]

    def to_dict(self) -> dict:
        return {
            "device_uuid": self.device_uuid,
            "hostname": self.hostname,
            "serial_number": self.serial_number,
            "os": self.os.to_dict(),
            "hardware": self.hardware.to_dict(),
            "network": [
                interface.to_dict()
                for interface in self.network
            ],
        }