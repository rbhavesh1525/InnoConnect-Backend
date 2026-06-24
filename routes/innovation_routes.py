from fastapi import APIRouter
from models.innovation_model import InnovationAssistantRequest, InnovationChatRequest
from services.innovation_service import generate_guidance, chat_with_assistant

router = APIRouter(
    prefix="/innovation",
    tags=["Innovation Assistant"]
)


@router.post("/generate-guidance")
async def generate_guidance_route(request: InnovationAssistantRequest):
    """
    Accept project form data and return AI guidance + similar projects.
    The project does NOT need to be saved to the database first.
    """
    return await generate_guidance(request)


@router.post("/chat")
async def chat_route(request: InnovationChatRequest):
    """
    Single-turn chat with the Innovation Assistant.
    Accepts project form data, similar projects already found, and the
    user's message. Returns a plain-text AI reply.
    No project_id required.
    """
    return await chat_with_assistant(request)