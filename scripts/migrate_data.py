import json

from database.dbconfig import get_supabase_client
from app.embeddings import generate_embedding


def project_to_text(project):
    return f"""
    Project Title:
    {project['project_title']}

    Description:
    {project['description']}

    Problem Statement:
    {project['problem_statement']}

    Solution Overview:
    {project['solution_overview']}

    Industry:
    {project['industry_category']}
    """


def main():
    supabase = get_supabase_client()

    with open(
        "data/innovation_platform_realistic_100.json",
        "r",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    for item in data:
        personal = item["personal_detail"]
        project = item["project"]

        project_response = (
            supabase.table("projects")
            .insert(
                {
                    "owner": personal["user_name_or_organization"],
                    "project_title": project["project_title"],
                    "description": project["description"],
                    "problem_statement": project["problem_statement"],
                    "solution_overview": project["solution_overview"],
                    "industry_category": project["industry_category"],
                }
            )
            .execute()
        )

        if not project_response.data:
            print(f"Failed to migrate project: {project['project_title']}")
            continue

        project_id = project_response.data[0]["id"]
        text = project_to_text(project)
        embedding = generate_embedding(text)

        supabase.table("project_embeddings").insert(
            {
                "project_id": project_id,
                "embedding": embedding.tolist(),
            }
        ).execute()

        print(f"Migrated project {project_id}: {project['project_title']}")

    print("\nMigration complete")


if __name__ == "__main__":
    main()
