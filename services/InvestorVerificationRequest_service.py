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

def get_all_verification_requests():

    try:

        print(
            "[INVESTOR REQUESTS] Fetching all requests..."
        )

        response = (
            supabase
            .table("investor_verification_requests")
            .select("*")
            .execute()
        )

        print(
            f"[INVESTOR REQUESTS] Found {len(response.data)} requests"
        )

        return {
            "success": True,
            "count": len(response.data),
            "data": response.data
        }

    except Exception as e:

        print(
            f"[INVESTOR REQUESTS ERROR] {str(e)}"
        )

        return {
            "success": False,
            "message": str(e)
        }


def approve_investor_request(
    request_id: int
):

    try:

        request = (
            supabase
            .table(
                "investor_verification_requests"
            )
            .select("*")
            .eq("id", request_id)
            .single()
            .execute()
        )

        if not request.data:

            return {
                "success": False,
                "message": "Request not found"
            }

        user_id = request.data["user_id"]

        (
            supabase
            .table(
                "investor_verification_requests"
            )
            .update({
                "status": "approved"
            })
            .eq("id", request_id)
            .execute()
        )

        (
            supabase
            .table("users")
            .update({
                "verification_status": True
            })
            .eq("user_id", user_id)
            .execute()
        )

        print(
            f"[APPROVED] Request={request_id} User={user_id}"
        )

        return {
            "success": True,
            "message": "Investor approved successfully"
        }

    except Exception as e:

        print(
            f"[APPROVE ERROR] {str(e)}"
        )

        return {
            "success": False,
            "message": str(e)
        }

def reject_investor_request(
    request_id: int
):

    try:

        request = (
            supabase
            .table(
                "investor_verification_requests"
            )
            .select("*")
            .eq("id", request_id)
            .single()
            .execute()
        )

        if not request.data:

            return {
                "success": False,
                "message": "Request not found"
            }

        user_id = request.data["user_id"]

        (
            supabase
            .table(
                "investor_verification_requests"
            )
            .update({
                "status": "rejected"
            })
            .eq("id", request_id)
            .execute()
        )

        (
            supabase
            .table("users")
            .update({
                "verification_status": False
            })
            .eq("user_id", user_id)
            .execute()
        )

        print(
            f"[REJECTED] Request={request_id} User={user_id}"
        )

        return {
            "success": True,
            "message": "Investor request rejected"
        }

    except Exception as e:

        print(
            f"[REJECT ERROR] {str(e)}"
        )

        return {
            "success": False,
            "message": str(e)
        }