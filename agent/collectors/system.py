import platform
import subprocess
import uuid

from agent.models.device import OSInfo


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


def get_device_uuid() -> str:
    """
    Temporary deterministic device identity.

    For Goal 1 this gives the same UUID for the same
    network adapter/MAC identity.

    This will later be replaced with a persistent
    agent-generated identity during installation.
    """

    mac = uuid.getnode()

    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"myedr-device-{mac}"))


def get_os_info() -> OSInfo:
    result = _run_powershell(
        """
        $os = Get-CimInstance Win32_OperatingSystem
        "$($os.Caption)|$($os.Version)|$($os.BuildNumber)"
        """
    )

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
    return _run_powershell(
        """
        (Get-CimInstance Win32_BIOS).SerialNumber
        """
    )