from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections = {}

    async def connect(
        self,
        user_id: str,
        websocket: WebSocket
    ):
        await websocket.accept()

        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):

        self.active_connections.pop(
            user_id,
            None
        )

    def get_connection(
        self,
        user_id: str
    ):
        return self.active_connections.get(
            user_id
        )

    async def send_personal_message(
        self,
        user_id: str,
        data: dict
    ):

        websocket = self.active_connections.get(
            user_id
        )

        if websocket:
            await websocket.send_json(data)


manager = ConnectionManager()