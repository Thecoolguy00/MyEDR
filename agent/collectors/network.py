import socket

import psutil

from agent.models.device import NetworkInterface


def get_network_interfaces() -> list[NetworkInterface]:
    interfaces: list[NetworkInterface] = []

    addresses = psutil.net_if_addrs()

    for interface_name, address_list in addresses.items():

        mac_address: str | None = None
        ipv4: list[str] = []
        ipv6: list[str] = []

        for address in address_list:

            if address.family == psutil.AF_LINK:
                mac_address = address.address

            elif address.family == socket.AF_INET:
                ipv4.append(address.address)

            elif address.family == socket.AF_INET6:
                ipv6.append(address.address)

        interfaces.append(
            NetworkInterface(
                name=interface_name,
                mac_address=mac_address,
                ipv4=ipv4,
                ipv6=ipv6,
            )
        )

    return interfaces