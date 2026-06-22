import numpy as np

from app.repository import get_all_embeddings
from app.vector_utils import parse_vector
from app.embeddings import generate_embedding
from app.similarity import find_similar


def project_to_text(project):
    return f"""
    Project Title:
    {project.project_title}

    Description:
    {project.description}

    Problem Statement:
    {project.problem_statement}

    Solution Overview:
    {project.solution_overview}

    Industry:
    {project.industry_category}
    """


def search_project_submission(project, top_k=5):
    rows = get_all_embeddings()

    if not rows:
        return []

    projects = []
    embeddings = []

    for row in rows:
        if row.get("embedding") is None:
            continue

        projects.append(row)
        embeddings.append(parse_vector(row["embedding"]))

    if not embeddings:
        return []

    embeddings = np.array(embeddings)

    query_text = project_to_text(project)
    query_emb = generate_embedding(query_text)

    idxs, scores = find_similar(query_emb, embeddings, top_k)

    results = []

    for idx in idxs:
        p = projects[idx]

        similarity = round(float(scores[idx]), 4)

        if similarity >= 0.75:
            status = "duplicate"
        elif similarity >= 0.50:
            status = "possibly_similar"
        else:
            status = "related"

        collaboration_recommended = similarity >= 0.70
        owner = p["owner"]
        collaboration_message = None

        if collaboration_recommended:
            collaboration_message = (
                f"Similar project found. "
                f"Consider collaborating with {owner}."
            )

        results.append(
            {
                "project_id": p["id"],
                "owner_id": p.get("owner_id"),
                "project_title": p["project_title"],
                "owner": owner,
                "industry": p["industry_category"],
                "similarity": similarity,
                "status": status,
                "collaboration_recommended": collaboration_recommended,
                "collaboration_message": collaboration_message,
            }
        )

    return results
