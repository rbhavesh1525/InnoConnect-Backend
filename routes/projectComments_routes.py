from fastapi import APIRouter

from models.projectCommentSchema import (
    ProjectCommentRequest
)

from services.projectComments_service import (
    add_comment,
    get_project_comments
)

router = APIRouter()


@router.post("/{project_id}")
def add_project_comment(
    project_id: str,
    request: ProjectCommentRequest
):

    return add_comment(
        project_id,
        request.user_id,
        request.comment
    )


@router.get("/{project_id}")
def fetch_project_comments(
    project_id: str
):

    return get_project_comments(
        project_id
    )