from pydantic import BaseModel
from typing import Any, List


class InnovationAssistantRequest(BaseModel):
    project_title: str
    description: str
    problem_statement: str
    solution_overview: str
    industry_category: str


class InnovationChatRequest(BaseModel):
    project_title: str
    problem_statement: str
    solution_overview: str
    industry_category: str
    similar_projects: List[Any] = []
    message: str