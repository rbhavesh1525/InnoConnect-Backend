import json

from services.similarity_service import find_similar_projects
from services.llm_service import generate_innovation_guidance, generate_innovation_chat


def _build_search_text(project) -> str:
    """Combine form fields into a single string for embedding search."""
    return (
        f"{project.project_title}\n"
        f"{project.problem_statement}\n"
        f"{project.solution_overview}"
    )


async def generate_guidance(request):
    """
    Generate AI guidance for an unsaved project idea.

    Accepts form data directly — no DB fetch required.
    Finds similar existing projects via embedding search, then
    passes everything to the LLM to produce structured guidance.
    """

    # Build a plain dict so it works both with Pydantic model and raw dict
    project = {
        "project_title": request.project_title,
        "description": request.description,
        "problem_statement": request.problem_statement,
        "solution_overview": request.solution_overview,
        "industry_category": request.industry_category,
    }

    # Similarity search against all saved projects (no exclusion needed
    # since this project has not been saved yet)
    search_text = _build_search_text(request)
    similar_projects = find_similar_projects(
        text=search_text,
        exclude_project_id=None,
        top_k=3
    )

    # Generate structured guidance from the LLM
    guidance_text = generate_innovation_guidance(project, similar_projects)

    try:
        cleaned = guidance_text.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "")
            cleaned = cleaned.replace("```", "").strip()

        guidance = json.loads(cleaned)

    except Exception:
        guidance = {"raw_response": guidance_text}

    return {
        "similar_projects": similar_projects,
        "guidance": guidance,
    }


async def chat_with_assistant(request):
    """
    Single-turn chat with the Innovation Assistant.

    Accepts the current project form data, the already-found similar
    projects (from a prior similarity check), and the user's message.
    No project_id or database fetch required.
    """

    project = {
        "project_title": request.project_title,
        "problem_statement": request.problem_statement,
        "solution_overview": request.solution_overview,
        "industry_category": request.industry_category,
    }

    reply = generate_innovation_chat(
        project=project,
        similar_projects=request.similar_projects,
        user_message=request.message,
    )

    return {"reply": reply}