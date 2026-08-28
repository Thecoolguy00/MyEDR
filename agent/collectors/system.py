import json
import platform
import subprocess
import uuid
from pathlib import Path

from agent.models.device import OSInfo


AGENT_DATA_DIR = Path.home() / ".myedr"
IDENTITY_FILE = AGENT_DATA_DIR / "identity.json"


def get_device_uuid() -> str:
    """
    Return the persistent MyEDR agent UUID.

    On first run:
    - Generate a UUID.
    - Store it locally.

    On future runs:
    - Load and return the existing UUID.
    """

    try:
        if IDENTITY_FILE.exists():
            with IDENTITY_FILE.open("r", encoding="utf-8") as file:
                identity = json.load(file)

            device_uuid = identity.get("device_uuid")

            if device_uuid:
                return device_uuid

        AGENT_DATA_DIR.mkdir(parents=True, exist_ok=True)

        device_uuid = str(uuid.uuid4())

        with IDENTITY_FILE.open("w", encoding="utf-8") as file:
            json.dump({"device_uuid": device_uuid},file)

        return device_uuid

    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("Failed to create or load MyEDR device identity") from exc


def _run_powershell(command: str) -> str | None:
    try:
        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                command,
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode != 0:
            return None

        output = result.stdout.strip()

        return output or None

    except (subprocess.SubprocessError, OSError):
        return None


def get_hostname() -> str:
    return platform.node()


def get_os_info() -> OSInfo:
    result = _run_powershell("$os = Get-CimInstance Win32_OperatingSystem; $os.Caption + '|' + $os.Version + '|' + $os.BuildNumber")

    if result:
        parts = result.split("|", maxsplit=2)

        return OSInfo(
            name=parts[0] if len(parts) > 0 else None,
            version=parts[1] if len(parts) > 1 else None,
            build=parts[2] if len(parts) > 2 else None,
        )

    return OSInfo(
        name=platform.system(),
        version=platform.version(),
        build=None,
    )


def get_serial_number() -> str | None:
    return _run_powershell("(Get-CimInstance Win32_BIOS).SerialNumber")