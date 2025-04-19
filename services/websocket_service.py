from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = list()
        self.chat_connections: Dict[str, List[WebSocket]] = dict()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def connect_chat(self, chat_id: str, websocket: WebSocket):
        await websocket.accept()
        if websocket not in self.active_connections:
            self.active_connections.append(websocket)
        if chat_id in self.chat_connections:
            self.chat_connections[chat_id].append(websocket)
        else:
            self.chat_connections.setdefault(chat_id, []).append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    def disconnect_chat(self, chat_id: str, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if chat_id in self.chat_connections and websocket in self.chat_connections[chat_id]:
            self.chat_connections[chat_id].remove(websocket)

    async def send_message(self, chat_id: str, message: str):
        if chat_id in self.chat_connections:
            for ws in self.chat_connections[chat_id]:
                await ws.send_text(message)

    async def boardcast(self, message: str):
        for ws in self.active_connections:
            await ws.send_text(message)

manager = ConnectionManager()
