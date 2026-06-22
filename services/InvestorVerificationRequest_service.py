from database.dbconfig import get_supabase_client

supabase = get_supabase_client()


def submit_verification_request(
    user_id: str,
    data
):

    response = (
        supabase
        .table("investor_verification_requests")
        .insert({
            "user_id": user_id,
            "full_name": data.full_name,
            "organization_name": data.organization_name,
            "designation": data.designation,
            "investor_type": data.investor_type,
            "linkedin_url": data.linkedin_url,
            "organization_website": data.organization_website,
            "preferred_industries": data.preferred_industries,
            "startup_stages": data.startup_stages,
            "min_investment": data.min_investment,
            "max_investment": data.max_investment,
            "open_for_opportunities": data.open_for_opportunities,
            "status": "pending"
        })
        .execute()
    )

    return {
        "success": True,
        "message": "Verification request submitted",
        "data": response.data
    }