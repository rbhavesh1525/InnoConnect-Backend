from database.dbconfig import get_supabase_client


def get_all_embeddings():
    supabase = get_supabase_client()

    response = (
        supabase.table("project_embeddings")
        .select(
            "project_id, embedding, "
            "projects(id, owner, project_title, description, "
            "problem_statement, solution_overview, industry_category)"
        )
        .execute()
    )

    rows = []
    for item in response.data or []:
        project = item.get("projects") or {}
        rows.append(
            {
                "id": project.get("id") or item.get("project_id"),
                "owner": project.get("owner"),
                "project_title": project.get("project_title"),
                "description": project.get("description"),
                "problem_statement": project.get("problem_statement"),
                "solution_overview": project.get("solution_overview"),
                "industry_category": project.get("industry_category"),
                "embedding": item.get("embedding"),
            }
        )

    return rows


def save_project(project, owner, owner_id):
    supabase = get_supabase_client()

    response = (
        supabase.table("projects")
        .insert(
            {
                "owner": owner,
                "owner_id": owner_id,
                "project_title": project.project_title,
                "description": project.description,
                "problem_statement": project.problem_statement,
                "solution_overview": project.solution_overview,
                "industry_category": project.industry_category,
            }
        )
        .execute()
    )

    if not response.data:
        raise Exception("Failed to save project")

    return response.data[0]["id"]


def save_embedding(project_id, embedding):
    supabase = get_supabase_client()

    response = (
        supabase.table("project_embeddings")
        .insert(
            {
                "project_id": project_id,
                "embedding": embedding.tolist(),
            }
        )
        .execute()
    )

    if not response.data:
        raise Exception("Failed to save project embedding")
