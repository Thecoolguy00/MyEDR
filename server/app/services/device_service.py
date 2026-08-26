import json
from typing import Any

from app.db.postgres import PostgresStore
from app.schemas.device import DeviceCreate


class DeviceService:

    def __init__(self, db: PostgresStore):
        self.db = db

    def register_device(self, device: DeviceCreate) -> dict[str, Any]:

        existing = self.db.fetch_one(
            "SELECT id FROM devices WHERE device_uuid = %s", 
            (device.device_uuid)
        )

        if existing:
            raise ValueError("Device already registered")

        os_info = device.os
        hardware = device.hardware

        result = self.db.execute(
            """
            INSERT INTO devices (
                device_uuid,
                hostname,
                serial_number,

                os_name,
                os_version,
                os_build,

                cpu,
                ram_bytes,
                gpu,

                network_interfaces
            )
            VALUES (
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s
            )
            RETURNING *
            """,
            (
                device.device_uuid,
                device.hostname,
                device.serial_number,

                os_info.name if os_info else None,
                os_info.version if os_info else None,
                os_info.build if os_info else None,

                hardware.cpu if hardware else None,
                hardware.ram_bytes if hardware else None,
                hardware.gpu if hardware else None,

                json.dumps([
                    interface.model_dump()
                    for interface in device.network
                ]),
            ),
        )

        return result["row"]

    def get_devices(self) -> list[dict[str, Any]]:
        return self.db.fetch_all("SELECT * FROM devices ORDER BY created_at DESC")

    def get_device(self, device_uuid: str) -> dict[str, Any] | None:

        return self.db.fetch_one("SELECT * FROM devices WHERE device_uuid = %s",(device_uuid))