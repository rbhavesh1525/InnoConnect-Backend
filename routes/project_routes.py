from fastapi import APIRouter

from models.projectSchema import ProjectSubmission
from app.search import search_project_submission
from app.submit_project import submit_project

router = APIRouter()


@router.post("/similarity")
def similarity(project: ProjectSubmission):
    results = search_project_submission(project)
    return {"results": results}


@router.post("/submit-project")
def submit(project: ProjectSubmission):
    project_id = submit_project(project)
    return {"saved": True, "project_id": project_id}
