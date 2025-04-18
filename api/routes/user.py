from fastapi import APIRouter, Depends, Request
from api.controllers.user_controller import get_user_profile, get_online_users, update_user_profile

router = APIRouter(prefix="/users", tags=["User"])

@router.get("/me")
def getMe(user=Depends(get_user_profile)):
    return user

@router.get("/active")
def active_users():
    return get_online_users()

@router.patch("")
async def update_user(request: Request):
    return await update_user_profile(request)