import psutil

from agent.collectors.system import _run_powershell
from agent.models.device import HardwareInfo


def get_cpu() -> str | None:
    return _run_powershell(
        """
        (Get-CimInstance Win32_Processor |
        Select-Object -First 1 -ExpandProperty Name)
        """
    )


def get_gpu() -> str | None:
    return _run_powershell(
        """
        (Get-CimInstance Win32_VideoController |
        Select-Object -ExpandProperty Name) -join ", "
        """
    )


def get_hardware_info() -> HardwareInfo:
    memory = psutil.virtual_memory()

    return HardwareInfo(
        cpu=get_cpu(),
        ram_bytes=memory.total,
        gpu=get_gpu(),
    )