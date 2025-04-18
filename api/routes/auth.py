from fastapi import APIRouter, Request
from api.controllers.auth_controller import register_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(request: Request):
    return await register_user(request)
