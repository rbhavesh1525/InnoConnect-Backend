from app.repository import save_project, save_embedding
from app.embeddings import generate_embedding
from app.search import project_to_text
from services.user_services import get_user_by_id


def submit_project(project, user_id):
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")

    project_id = save_project(project, owner=user["name"], owner_id=user_id)

    text = project_to_text(project)
    embedding = generate_embedding(text)

    save_embedding(project_id, embedding)

    return project_id
