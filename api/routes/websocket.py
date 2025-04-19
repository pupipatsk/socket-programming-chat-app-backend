from fastapi import APIRouter, Query, WebSocket
from api.controllers.websocket_controller import handle_connection

router = APIRouter()

@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str, user_id: str = Query(...)):
    await handle_connection(websocket, chat_id, user_id)
