from fastapi import Request, HTTPException
from core.firebase import verify_token
from services.group_service import *

def get_uid(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header.split(" ")[1]
    decoded = verify_token(token)
    if not decoded:
        raise HTTPException(status_code=401, detail="Invalid token")
    return decoded["uid"]

async def create_group_handler(request: Request):
    uid = get_uid(request)
    body = await request.json()
    name = body.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Group name required")
    return create_group(uid, name)

async def get_all_groups_handler(request: Request):
    _ = get_uid(request)  # Still require token
    return get_all_groups_basic()

async def get_group_by_id(request: Request, group_id: str):
    uid = get_uid(request)
    group = get_group_if_member(group_id, uid)
    if not group:
        raise HTTPException(status_code=403, detail="Not a group member")
    return serialize_group(group)

async def join_group_handler(request: Request, group_id: str):
    uid = get_uid(request)
    return join_group(group_id, uid)

async def post_group_message(request: Request, group_id: str):
    uid = get_uid(request)
    body = await request.json()
    content = body.get("content")
    if not content:
        raise HTTPException(status_code=400, detail="Message required")
    msg = add_group_message(group_id, uid, content)
    if not msg:
        raise HTTPException(status_code=403, detail="Not a member")
    msg["_id"] = str(msg["_id"])
    msg["timestamp"] = msg["timestamp"].isoformat()
    return msg

async def patch_group_message(request: Request, group_id: str, msg_id: str):
    uid = get_uid(request)
    body = await request.json()
    content = body.get("content")
    deleted = body.get("deleted")

    msg, err = edit_group_message(group_id, msg_id, uid, content, deleted)
    if err == "unauthorized":
        raise HTTPException(status_code=403, detail="Not message owner")
    elif err == "not_found":
        raise HTTPException(status_code=404, detail="Message not found")

    msg["_id"] = str(msg["_id"])
    msg["timestamp"] = msg["timestamp"].isoformat()
    return msg

async def delete_group_msg(request: Request, group_id: str, msg_id: str):
    uid = get_uid(request)
    msg, err = delete_group_message(group_id, msg_id, uid)
    if err == "unauthorized":
        raise HTTPException(status_code=403, detail="Not message owner")
    elif err == "not_found":
        raise HTTPException(status_code=404, detail="Message not found")
    msg["_id"] = str(msg["_id"])
    msg["timestamp"] = msg["timestamp"].isoformat()
    return {"message": "Deleted", "data": msg}
