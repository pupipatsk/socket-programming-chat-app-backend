from fastapi import Request, HTTPException
from core.firebase import verify_token
from services.user_service import create_user_if_not_exists

async def register_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header.split(" ")[1]
    decoded = verify_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid token")

    uid = decoded["uid"]
    email = decoded.get("email", "")

    body = await request.json()
    name = body.get("name", "")

    return create_user_if_not_exists(uid, email, name)
