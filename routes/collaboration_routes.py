from fastapi import APIRouter, Depends

from dependencies.auth_dependency import get_current_user

from models.collaboration_model import (
    CollaborationRequestCreate
)

from fastapi import HTTPException

from services.collaboration_service import (
    send_collaboration_request,
    get_incoming_requests,
    get_sent_requests,
    get_pending_request_count,
    accept_request,
    reject_request,
    _enrich_request,
)
from services.message_service import send_message, get_unread_counts
from websocket.connection_manager import manager

router = APIRouter(
    prefix="/collaboration",
    tags=["Collaboration"]
)

@router.post("/send")
async def send_request(
    request: CollaborationRequestCreate,
    current_user=Depends(get_current_user)
):
    sender_id = current_user["user_id"]

    result = send_collaboration_request(
        sender_id,
        request.receiver_id,
        request.project_id
    )

    if not result.get("success"):
        return {
            "message": result["message"],
            "data": None,
        }

    created = result["data"][0] if result.get("data") else None
    enriched = _enrich_request(created, "sender_id") if created else None
    pending_count = get_pending_request_count(request.receiver_id)

    if enriched:
        await manager.send_personal_message(
            request.receiver_id,
            {
                "event": "newCollaborationRequest",
                "data": enriched,
                "pending_count": pending_count,
            },
        )

    return {
        "message": "Collaboration request sent",
        "data": enriched or result.get("data"),
    }

@router.get("/incoming/count")
def incoming_request_count(
    current_user=Depends(get_current_user)
):
    count = get_pending_request_count(current_user["user_id"])

    return {
        "success": True,
        "count": count,
    }

@router.get("/incoming")
def incoming_requests(
    current_user=Depends(get_current_user)
):
    return get_incoming_requests(
        current_user["user_id"]
    )


@router.get("/sent")
def sent_requests(
    current_user=Depends(get_current_user)
):
    return get_sent_requests(
        current_user["user_id"]
    )


async def _notify_sender(result: dict, receiver_id: str):
    request = result.get("request")
    notification_message = result.get("notification_message")

    if not request or not notification_message:
        return None

    saved_message = send_message(
        receiver_id,
        request["sender_id"],
        notification_message,
    )

    unread_counts = get_unread_counts(request["sender_id"])

    await manager.send_personal_message(
        request["sender_id"],
        {
            "event": "newMessage",
            "data": saved_message,
            "unread_counts": unread_counts,
        },
    )

    return saved_message


async def _notify_receiver_count_updated(user_id: str):
    pending_count = get_pending_request_count(user_id)

    await manager.send_personal_message(
        user_id,
        {
            "event": "collaborationCountsUpdated",
            "pending_count": pending_count,
        },
    )


@router.post("/accept/{request_id}")
async def accept(
    request_id: str,
    current_user=Depends(get_current_user)
):
    result = accept_request(request_id, current_user["user_id"])

    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result["message"])

    notification = await _notify_sender(result, current_user["user_id"])
    await _notify_receiver_count_updated(current_user["user_id"])

    return {
        "message": "Collaboration request accepted",
        "data": result["data"],
        "notification": notification,
    }


@router.post("/reject/{request_id}")
async def reject(
    request_id: str,
    current_user=Depends(get_current_user)
):
    result = reject_request(request_id, current_user["user_id"])

    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result["message"])

    notification = await _notify_sender(result, current_user["user_id"])
    await _notify_receiver_count_updated(current_user["user_id"])

    return {
        "message": "Collaboration request rejected",
        "data": result["data"],
        "notification": notification,
    }
