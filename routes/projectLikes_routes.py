from fastapi import APIRouter

from models.projectLikesSchema import (
    ProjectLikeRequest
)

from services.projectLikes_service import (
    like_project
)

router = APIRouter()


@router.post("/{project_id}")
def like_project_route(
    project_id: str,
    request: ProjectLikeRequest
):

    return like_project(
        project_id,
        request.user_id
    )