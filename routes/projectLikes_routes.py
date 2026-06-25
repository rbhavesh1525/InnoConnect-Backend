from fastapi import APIRouter

from models.projectLikeSchema import (
    ProjectLikeRequest
)

from services.projectLike_service import (
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