"""事件总线 - WebSocket推送"""
import asyncio
from typing import Set
from datetime import datetime
from fastapi import WebSocket

class EventBus:
    def __init__(self):
        self.connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """添加连接"""
        await websocket.accept()
        self.connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        """移除连接"""
        self.connections.discard(websocket)

    async def emit(self, event_type: str, data: dict):
        """推送事件到所有连接"""
        message = {
            'type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }

        disconnected = set()
        for connection in self.connections:
            try:
                await connection.send_json(message)
            except:
                disconnected.add(connection)

        for conn in disconnected:
            self.disconnect(conn)
