from pydantic import BaseModel


class ProjectSubmission(BaseModel):
    project_title: str
    description: str
    problem_statement: str
    solution_overview: str
    industry_category: str
