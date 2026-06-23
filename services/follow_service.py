from database.dbconfig import get_supabase_client

supabase = get_supabase_client()


def follow_user(
    follower_id: str,
    following_id: str
):

    try:

        if follower_id == following_id:
            return {
                "success": False,
                "message": "You cannot follow yourself"
            }

        existing_follow = (
            supabase
            .table("user_followers")
            .select("*")
            .eq("follower_id", follower_id)
            .eq("following_id", following_id)
            .execute()
        )

        if existing_follow.data:

            return {
                "success": False,
                "message": "Already following this user"
            }

        response = (
            supabase
            .table("user_followers")
            .insert({
                "follower_id": follower_id,
                "following_id": following_id
            })
            .execute()
        )

        print(
            f"[FOLLOW SUCCESS] {follower_id} -> {following_id}"
        )

        return {
            "success": True,
            "message": "User followed successfully",
            "data": response.data
        }

    except Exception as e:

        print(
            f"[FOLLOW ERROR] {str(e)}"
        )

        return {
            "success": False,
            "message": str(e)
        }


def get_followers(user_id: str):

    try:

        response = (
            supabase
            .table("user_followers")
            .select("*")
            .eq("following_id", user_id)
            .execute()
        )

        print(
            f"[FOLLOWERS FETCHED] user_id={user_id}"
        )

        return {
            "success": True,
            "count": len(response.data),
            "data": response.data
        }

    except Exception as e:

        print(
            f"[GET FOLLOWERS ERROR] {str(e)}"
        )

        return {
            "success": False,
            "message": str(e)
        }


def unfollow_user(
    follower_id: str,
    following_id: str
):

    try:

        response = (
            supabase
            .table("user_followers")
            .delete()
            .eq("follower_id", follower_id)
            .eq("following_id", following_id)
            .execute()
        )

        print(
            f"[UNFOLLOW SUCCESS] {follower_id} -> {following_id}"
        )

        return {
            "success": True,
            "message": "User unfollowed successfully",
            "data": response.data
        }

    except Exception as e:

        print(
            f"[UNFOLLOW ERROR] {str(e)}"
        )

        return {
            "success": False,
            "message": str(e)
        }


def check_follow_status(
    follower_id: str,
    following_id: str
):

    try:

        response = (
            supabase
            .table("user_followers")
            .select("*")
            .eq("follower_id", follower_id)
            .eq("following_id", following_id)
            .execute()
        )

        return {
            "success": True,
            "following": len(response.data) > 0
        }

    except Exception as e:

        print(
            f"[FOLLOW STATUS ERROR] {str(e)}"
        )

        return {
            "success": False,
            "message": str(e)
        }