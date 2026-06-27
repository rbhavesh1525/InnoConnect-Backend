from pydantic import BaseModel

class FundRequestCreate(BaseModel):
    receiver_id: str
    project_id: int
