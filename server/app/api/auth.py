from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.auth import CurrentUserResponse, LoginRequest, LoginResponse
from app.services.auth_service import AuthService

router=APIRouter(prefix="/api/v1/auth", tags=["auth"])

security=HTTPBearer()


def get_auth_service(request: Request)->AuthService:
    return request.app.state.auth_service


def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security), service: AuthService=Depends(get_auth_service)):

    try:
        user = service.get_current_user(credentials.credentials)

    except ValueError as exc:
        raise HTTPException(status_code=401,detail=str(exc))

    if not user["is_admin"]:
        raise HTTPException(status_code=403,detail="Admin access required")

    return user

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, service:AuthService=Depends(get_auth_service)):
    try:
        return service.login(
            username=payload.username,
            password=payload.password
        )

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials=Depends(security), service:AuthService=Depends(get_auth_service)):
    try:
        service.logout(credentials.credentials)

        return {"message": "logged out successfully"}

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=CurrentUserResponse)
def get_me(credentials: HTTPAuthorizationCredentials=Depends(security), service:AuthService=Depends(get_auth_service)):
    try:
        return service.get_current_user(credentials.credentials)

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))