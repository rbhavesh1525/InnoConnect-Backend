from pydantic import BaseModel

class ProjectLikeRequest(BaseModel):
    user_id: str