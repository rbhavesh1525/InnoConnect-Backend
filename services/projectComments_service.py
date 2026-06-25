from database.dbconfig import get_supabase_client

supabase = get_supabase_client()


def add_comment(
    project_id: str,
    user_id: str,
    comment: str
):

    try:

        if not comment.strip():

            return {
                "success": False,
                "message": "Comment cannot be empty"
            }

        response = (
            supabase
            .table("project_comments")
            .insert({
                "project_id": project_id,
                "user_id": user_id,
                "comment": comment
            })
            .execute()
        )

        print(
            f"[COMMENT ADDED] User={user_id} Project={project_id}"
        )

        return {
            "success": True,
            "message": "Comment added successfully",
            "data": response.data
        }

    except Exception as e:

        print(
            f"[COMMENT ERROR] {str(e)}"
        )

        return {
            "success": False,
            "message": str(e)
        }


def get_project_comments(
    project_id: str
):

    try:

        response = (
            supabase
            .table("project_comments")
            .select("*")
            .eq("project_id", project_id)
            .order("created_at", desc=True)
            .execute()
        )

        print(
            f"[COMMENTS FETCHED] Project={project_id}"
        )

        return {
            "success": True,
            "count": len(response.data),
            "data": response.data
        }

    except Exception as e:

        print(
            f"[GET COMMENTS ERROR] {str(e)}"
        )

        return {
            "success": False,
            "message": str(e)
        }