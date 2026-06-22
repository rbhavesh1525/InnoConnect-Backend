from fastapi import APIRouter, Depends

from models.message_model import SendMessageRequest
from dependencies.auth_dependency import get_current_user
from services.message_service import send_message
from services.message_service import get_messages
from services.message_service import mark_messages_as_read
from services.message_service import get_unread_counts
from websocket.connection_manager import manager


router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)


@router.get("/unread/counts")
def unread_counts(current_user=Depends(get_current_user)):
    counts = get_unread_counts(current_user["user_id"])

    return {
        "success": True,
        "unread_counts": counts,
    }


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

    unread_counts = get_unread_counts(request.receiver_id)

    await manager.send_personal_message(
        request.receiver_id,
        {
            "event": "newMessage",
            "data": saved_message,
            "unread_counts": unread_counts,
        }
    )

    return {
        "success": True,
        "message": saved_message
    }


@router.post("/{user_id}/read")
async def mark_conversation_read(
    user_id: str,
    current_user=Depends(get_current_user)
):
    my_id = current_user["user_id"]

    mark_messages_as_read(my_id, user_id)
    unread_counts = get_unread_counts(my_id)

    await manager.send_personal_message(
        my_id,
        {
            "event": "unreadCountsUpdated",
            "data": unread_counts,
        }
    )

    return {
        "success": True,
        "unread_counts": unread_counts,
    }


@router.get("/{user_id}")
async def get_conversation(
    user_id: str,
    current_user=Depends(get_current_user)
):
    my_id = current_user["user_id"]

    messages = get_messages(
        my_id,
        user_id
    )

    mark_messages_as_read(my_id, user_id)
    unread_counts = get_unread_counts(my_id)

    await manager.send_personal_message(
        my_id,
        {
            "event": "unreadCountsUpdated",
            "data": unread_counts,
        }
    )

    return {
        "success": True,
        "messages": messages,
        "unread_counts": unread_counts,
    }
