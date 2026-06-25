from pydantic import BaseModel


class ProjectCommentRequest(BaseModel):
    user_id: str
    comment: str