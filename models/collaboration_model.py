# models/collaboration_model.py

from pydantic import BaseModel

class CollaborationRequestCreate(BaseModel):
    receiver_id: str
    project_id: int