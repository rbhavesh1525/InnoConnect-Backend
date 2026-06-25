from database.dbconfig import get_supabase_client

supabase = get_supabase_client()


def like_project(
    project_id: str,
    user_id: str
):

    try:

        existing_like = (
            supabase
            .table("project_likes")
            .select("*")
            .eq("project_id", project_id)
            .eq("user_id", user_id)
            .execute()
        )

        if existing_like.data:

            return {
                "success": False,
                "message": "Project already liked"
            }

        response = (
            supabase
            .table("project_likes")
            .insert({
                "project_id": project_id,
                "user_id": user_id
            })
            .execute()
        )

        print(
            f"[PROJECT LIKE] User={user_id} Project={project_id}"
        )

        return {
            "success": True,
            "message": "Project liked successfully",
            "data": response.data
        }

    except Exception as e:

        print(
            f"[PROJECT LIKE ERROR] {str(e)}"
        )

        return {
            "success": False,
            "message": str(e)
        }