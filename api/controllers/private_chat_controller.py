from fastapi import Request, HTTPException
from core.firebase import verify_token
from services.private_chat_service import (
    create_private_chat, get_chat_if_member, serialize_chat,
    add_message, edit_message, delete_message
)

async def create_chat(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header.split(" ")[1]
    decoded = verify_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid token")

    uid = decoded["uid"]
    body = await request.json()
    other_uid = body.get("other_uid")

    if not other_uid:
        raise HTTPException(status_code=400, detail="other_uid is required")

    return create_private_chat(uid, other_uid)

async def get_chat(request: Request, chat_id: str):
    uid = get_uid_from_request(request)
    chat = get_chat_if_member(chat_id, uid)
    if not chat:
        raise HTTPException(status_code=403, detail="Access denied")
    return serialize_chat(chat)

async def add_msg(request: Request, chat_id: str):
    uid = get_uid_from_request(request)
    data = await request.json()
    content = data.get("content")
    if not content:
        raise HTTPException(status_code=400, detail="Missing content")

    msg = add_message(chat_id, uid, content)
    if not msg:
        raise HTTPException(status_code=403, detail="Not a member")
    msg["_id"] = str(msg["_id"])
    msg["timestamp"] = msg["timestamp"].isoformat()
    return msg

async def update_msg(request: Request, chat_id: str, msg_id: str):
    uid = get_uid_from_request(request)
    data = await request.json()
    content = data.get("content")
    deleted = data.get("deleted")

    msg, error = edit_message(chat_id, msg_id, uid, content, deleted)
    if error == "unauthorized":
        raise HTTPException(status_code=403, detail="Not your message")
    elif error == "not_found":
        raise HTTPException(status_code=404, detail="Message not found")

    msg["_id"] = str(msg["_id"])
    msg["timestamp"] = msg["timestamp"].isoformat()
    return msg

async def delete_msg(request: Request, chat_id: str, msg_id: str):
    uid = get_uid_from_request(request)
    msg, error = delete_message(chat_id, msg_id, uid)
    if error == "unauthorized":
        raise HTTPException(status_code=403, detail="Not your message")
    elif error == "not_found":
        raise HTTPException(status_code=404, detail="Message not found")
    msg["_id"] = str(msg["_id"])
    msg["timestamp"] = msg["timestamp"].isoformat()
    return {"message": "Message deleted", "data": msg}

def get_uid_from_request(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header.split(" ")[1]
    decoded = verify_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid token")

    return decoded["uid"]
