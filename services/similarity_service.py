# services/similarity_service.py

import numpy as np

from app.repository import get_all_embeddings
from app.vector_utils import parse_vector
from app.embeddings import generate_embedding
from app.similarity import find_similar


def find_similar_projects(text: str, exclude_project_id=None, top_k=3):

    rows = get_all_embeddings()

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

    query_emb = generate_embedding(text)

    idxs, scores = find_similar(
        query_emb,
        embeddings,
        top_k + 5
    )

    results = []

    for idx in idxs:

        p = projects[idx]

        if exclude_project_id and p["id"] == exclude_project_id:
            continue

        similarity = round(float(scores[idx]), 4)

        results.append(
            {
            "project_id": p["id"],
            "project_title": p["project_title"],
            "description": p.get("description"),
            "problem_statement": p.get("problem_statement"),
            "solution_overview": p.get("solution_overview"),
            "industry": p["industry_category"],
            "similarity": similarity
            }
        )

        if len(results) >= top_k:
            break

    return results