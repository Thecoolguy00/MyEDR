import sys

from agent.api.client import MyEDRClient
from agent.collectors.hardware import get_hardware_info
from agent.collectors.network import get_network_interfaces
from agent.collectors.system import get_device_uuid, get_hostname, get_os_info, get_serial_number
from agent.models.device import Device


def collect_device() -> Device:
    return Device(
        device_uuid=get_device_uuid(),
        hostname=get_hostname(),
        serial_number=get_serial_number(),
        os=get_os_info(),
        hardware=get_hardware_info(),
        network=get_network_interfaces(),
    )


def main() -> int:
    print("MyEDR Agent")
    print("Collecting device information...")

    device = collect_device()

    print(f"Hostname : {device.hostname}")
    print(f"UUID     : {device.device_uuid}")
    print(f"OS       : {device.os.name}")
    print(f"CPU      : {device.hardware.cpu}")
    print(
        f"RAM      : "
        f"{device.hardware.ram_bytes / (1024 ** 3):.2f} GB"
    )
    print(f"GPU      : {device.hardware.gpu}")
    print(f"Interfaces: {len(device.network)}")

    client = MyEDRClient()

    try:
        response = client.register_device(device)

        print()
        print("Device registered successfully.")
        print(f"Server response: {response}")

        return 0

    except Exception as exc:
        print()
        print(f"Failed to register device: {exc}", file=sys.stderr)

        return 1

    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())