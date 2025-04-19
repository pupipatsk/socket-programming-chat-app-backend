from fastapi import WebSocket, WebSocketDisconnect
from services.websocket_service import manager

async def handle_connection(websocket: WebSocket, chat_id: str, user_id: str):
    await manager.connect_chat(chat_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(chat_id, f"{user_id}: {data}")
            
    except WebSocketDisconnect:
        manager.disconnect_chat(chat_id, websocket)
        await manager.send_message(chat_id, f"{user_id} has left the chat.")
