from fastapi import APIRouter, Depends, Query

from app.service.auth_service import AuthService
from app.utils.deps import get_auth_service
from app.utils.schemas.response import ResponseUserSchema

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", response_model=ResponseUserSchema)
async def register(
        username: str = Query(..., min_length=3),
        auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.register(username)

@router.post("/login", response_model=ResponseUserSchema)
async def login(
        username: str = Query(..., min_length=3),
        auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.login(username)

@router.get("/refresh", response_model=ResponseUserSchema)
async def refresh(
        username: str = Query(..., min_length=3),
        auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.login(username)