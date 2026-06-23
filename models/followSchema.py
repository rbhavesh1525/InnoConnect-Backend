
from pydantic import BaseModel

class FollowUserRequest(BaseModel):
    follower_id: str