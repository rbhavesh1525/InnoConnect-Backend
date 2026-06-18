from app.repository import save_project, save_embedding
from app.embeddings import generate_embedding
from app.search import project_to_text


def submit_project(project, owner="Website User"):
    project_id = save_project(project, owner=owner)

    text = project_to_text(project)
    embedding = generate_embedding(text)

    save_embedding(project_id, embedding)

    return project_id
