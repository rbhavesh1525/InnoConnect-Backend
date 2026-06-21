from database.dbconfig import get_supabase_client

supabase = get_supabase_client()


def update_profile(user_id: str,profile_data):

    try:

        response = (
            supabase
            .table("users")
            .update({
                "name": profile_data.name,
                "headline": profile_data.headline,
                "bio": profile_data.bio,
                "linkedin_url": profile_data.linkedin_url,
                "github_url": profile_data.github_url,
                "website_url": profile_data.website_url,
                "profile_image": profile_data.profile_image,
                "cover_image": profile_data.cover_image
            })
            .eq("user_id", user_id)
            .execute()
        )

        return {
            "success": True,
            "message": "Profile updated successfully",
            "data": response.data
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }

def get_profile(user_id: str):

    try:

        response = (
            supabase
            .table("users")
            .select("*")
            .eq("user_id", user_id)
            .single()
            .execute()
        )

        return {
            "success": True,
            "data": response.data
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }