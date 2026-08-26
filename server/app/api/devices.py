from fastapi import APIRouter, HTTPException

from app.schemas.device import DeviceCreate
from app.services.device_service import DeviceService


router = APIRouter(prefix="/api/v1/devices", tags=["devices"])


def get_service() -> DeviceService:
    from app.main import device_service

    if device_service is None:
        raise HTTPException(status_code=503, detail="Service is not ready")

    return device_service


@router.post("/register",response_model=dict)
def register_device(payload: DeviceCreate):
    service = get_service()

    try:
        device = service.register_device(payload)

    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    return device


@router.get("",response_model=list[dict])
def list_devices():
    return get_service().get_devices()


@router.get("/{device_uuid}", response_model=dict)
def get_device(device_uuid: str):
    device = get_service().get_device(device_uuid)

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device