from fastapi import APIRouter

from models.userProfileSchema import UpdateProfileModel
from services.profile_services import (
    update_profile,
    get_profile
)

router = APIRouter()

@router.put("/update-profile/{user_id}")
def update_user_profile(
    user_id: str,
    profile: UpdateProfileModel
):
    return update_profile(user_id, profile)

@router.get("/profile/{user_id}")
def fetch_profile(
    user_id: str
):

    return get_profile(user_id)