from fastapi import APIRouter
from services.investor_feed_service import get_investor_feed

router = APIRouter()


@router.get("/{user_id}")
def investor_feed(user_id: str, top_k: int = 10):
    """
    Returns personalised project recommendations for an investor.
    Uses embedding similarity against their preferred_industries
    and startup_stages from the verification request.
    """
    return get_investor_feed(user_id, top_k=top_k)
