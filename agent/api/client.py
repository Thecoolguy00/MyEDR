import httpx

from agent.config import REGISTER_ENDPOINT, REQUEST_TIMEOUT
from agent.models.device import Device


class MyEDRClient:

    def __init__(self):
        self.client = httpx.Client(timeout=REQUEST_TIMEOUT)

    def register_device(self, device: Device) -> dict:
        response = self.client.post(REGISTER_ENDPOINT, json=device.to_dict())

        response.raise_for_status()

        return response.json()

    def close(self) -> None:
        self.client.close()