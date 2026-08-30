from fastapi import APIRouter, Depends, HTTPException, Request

from app.schemas.device import DeviceCreate
from app.api.auth import get_current_admin
from app.services.device_service import DeviceService


router = APIRouter(prefix="/api/v1/devices", tags=["devices"])


def get_device_service(request: Request) -> DeviceService:
    return request.app.state.device_service


@router.post("/register",response_model=dict)
def register_device(payload: DeviceCreate, service: DeviceService = Depends(get_device_service)):

    try:
        device = service.register_device(payload)

    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    return device


@router.get("",response_model=list[dict])
def list_devices(service: DeviceService = Depends(get_device_service), current_user: dict = Depends(get_current_admin)):
    return service.get_devices()

@router.get("/{device_uuid}", response_model=dict)
def get_device(device_uuid:str, service: DeviceService=Depends(get_device_service), current_user:dict=Depends(get_current_admin)):

    device=service.get_device(device_uuid)

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")


    return device