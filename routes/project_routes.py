from fastapi import APIRouter, Depends, HTTPException

from models.projectSchema import ProjectSubmission
from app.search import search_project_submission
from app.submit_project import submit_project
from dependencies.auth_dependency import get_current_user

router = APIRouter()


@router.post("/similarity")
def similarity(project: ProjectSubmission):
    results = search_project_submission(project)
    return {"results": results}


@router.post("/submit-project")
def submit(
    project: ProjectSubmission,
    current_user=Depends(get_current_user),
):
    try:
        project_id = submit_project(project, user_id=current_user["user_id"])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"saved": True, "project_id": project_id}
