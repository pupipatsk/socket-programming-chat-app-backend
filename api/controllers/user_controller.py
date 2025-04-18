from fastapi import Request, HTTPException, status
from core.firebase import verify_token
from services.user_service import get_user_by_uid, get_users_by_status, update_user_fields

def get_user_profile(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header.split(" ")[1]
    decoded = verify_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid token")

    return get_user_by_uid(decoded["uid"])

def get_online_users():
    return get_users_by_status("Online")

async def update_user_profile(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header.split(" ")[1]
    decoded = verify_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid token")

    uid = decoded["uid"]
    body = await request.json()

    name = body.get("name")
    status = body.get("status")

    if not name and not status:
        raise HTTPException(status_code=400, detail="Nothing to update")

    updated_user = update_user_fields(uid, name=name, status=status)
    return {"message": "User updated", "user": updated_user}
