from fastapi import APIRouter, Depends

from models.message_model import SendMessageRequest
from dependencies.auth_dependency import get_current_user
from services.message_service import send_message
from services.message_service import get_messages
from websocket.connection_manager import manager


router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)


@router.post("/send")
async def send_message_route(
    request: SendMessageRequest,
    current_user=Depends(get_current_user)
):
    sender_id = current_user["user_id"]

    saved_message = send_message(
        sender_id=sender_id,
        receiver_id=request.receiver_id,
        message=request.message
    )

    await manager.send_personal_message(
        request.receiver_id,
        {
            "event": "newMessage",
            "data": saved_message
        }
    )

    return {
        "success": True,
        "message": saved_message
    }


@router.get("/{user_id}")
def get_conversation(
    user_id: str,
    current_user=Depends(get_current_user)
):
    my_id = current_user["user_id"]

    messages = get_messages(
        my_id,
        user_id
    )

    return {
        "success": True,
        "messages": messages
    }