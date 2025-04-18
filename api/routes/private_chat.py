from fastapi import APIRouter, Request
from api.controllers.private_chat_controller import (
    create_chat, get_chat, add_msg, update_msg, delete_msg
)

router = APIRouter(prefix="/private-chats", tags=["Private Chats"])

@router.post("")
async def create_private_chat(request: Request):
    return await create_chat(request)

@router.get("/{chat_id}")
async def get_private_chat(chat_id: str, request: Request):
    return await get_chat(request, chat_id)

@router.patch("/{chat_id}/messages")
async def add_message_to_chat(chat_id: str, request: Request):
    return await add_msg(request, chat_id)

@router.patch("/{chat_id}/messages/{msg_id}")
async def edit_message_in_chat(chat_id: str, msg_id: str, request: Request):
    return await update_msg(request, chat_id, msg_id)

@router.delete("/{chat_id}/messages/{msg_id}")
async def delete_message_from_chat(chat_id: str, msg_id: str, request: Request):
    return await delete_msg(request, chat_id, msg_id)