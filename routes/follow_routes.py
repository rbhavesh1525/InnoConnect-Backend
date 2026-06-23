from fastapi import APIRouter

from models.followSchema import (
    FollowUserRequest
)

from services.follow_service import (
    follow_user,
    get_followers,
    unfollow_user,
    check_follow_status
)

router = APIRouter()


@router.post("/{following_id}")
def follow(
    following_id: str,
    request: FollowUserRequest
):

    return follow_user(
        request.follower_id,
        following_id
    )


@router.get("/followers/{user_id}")
def fetch_followers(
    user_id: str
):

    return get_followers(user_id)


@router.delete("/{following_id}")
def unfollow(
    following_id: str,
    request: FollowUserRequest
):

    return unfollow_user(
        request.follower_id,
        following_id
    )


@router.get(
    "/status/{follower_id}/{following_id}"
)
def follow_status(
    follower_id: str,
    following_id: str
):

    return check_follow_status(
        follower_id,
        following_id
    )