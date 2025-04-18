from fastapi import APIRouter, Request
from api.controllers.group_controller import *

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.post("")
async def create_group(request: Request):
    return await create_group_handler(request)

@router.get("")
async def list_all_groups(request: Request):
    return await get_all_groups_handler(request)

@router.get("/{group_id}")
async def get_group(group_id: str, request: Request):
    return await get_group_by_id(request, group_id)

@router.post("/join/{group_id}")
async def join_group_route(group_id: str, request: Request):
    return await join_group_handler(request, group_id)

@router.patch("/{group_id}/messages")
async def send_group_message(group_id: str, request: Request):
    return await post_group_message(request, group_id)

@router.patch("/{group_id}/messages/{msg_id}")
async def update_group_msg(group_id: str, msg_id: str, request: Request):
    return await patch_group_message(request, group_id, msg_id)

@router.delete("/{group_id}/messages/{msg_id}")
async def remove_group_msg(group_id: str, msg_id: str, request: Request):
    return await delete_group_msg(request, group_id, msg_id)
