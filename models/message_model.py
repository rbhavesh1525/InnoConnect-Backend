from pydantic import BaseModel

class SendMessageRequest(BaseModel):
    receiver_id: str
    message: str