from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from websocket.connection_manager import manager
from utils.auth import verify_token

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    token = websocket.query_params.get("token")

    if not token:
        await websocket.close()
        return

    payload = verify_token(token)

    if not payload:
        await websocket.close()
        return

    user_id = payload["user_id"]

    await manager.connect(
        user_id,
        websocket
    )

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:

        manager.disconnect(user_id)