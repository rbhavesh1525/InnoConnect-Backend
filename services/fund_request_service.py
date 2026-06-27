from database.dbconfig import get_supabase_client

supabase = get_supabase_client()


def _resolve_request_id(req: dict):
    return req.get("request_id") or req.get("id")


def _get_project_title(project_id: int) -> str:
    project = (
        supabase.table("projects")
        .select("project_title")
        .eq("id", project_id)
        .execute()
    )
    if project.data:
        return project.data[0]["project_title"]
    return "Unknown Project"


def _enrich_request(req: dict, other_user_field: str):
    other_user_id = req[other_user_field]
    other_user = (
        supabase.table("users")
        .select("name, email")
        .eq("user_id", other_user_id)
        .execute()
    )
    project_title = _get_project_title(req["project_id"])

    return {
        **req,
        "request_id": _resolve_request_id(req),
        f"{other_user_field.replace('_id', '')}_name": (
            other_user.data[0]["name"] if other_user.data else "Unknown"
        ),
        f"{other_user_field.replace('_id', '')}_email": (
            other_user.data[0]["email"] if other_user.data else ""
        ),
        "project_title": project_title,
    }

def send_fund_request(sender_id, receiver_id, project_id):

    existing = (
        supabase.table("fund_requests")
        .select("*")
        .eq("sender_id", sender_id)
        .eq("receiver_id", receiver_id)
        .eq("project_id", project_id)
        .execute()
    )

    if existing.data:
        return {
            "success": False,
            "message": "Request already exists"
        }

    response = (
        supabase.table("fund_requests")
        .insert({
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "project_id": project_id
        })
        .execute()
    )

    return {
        "success": True,
        "message": "Fund request sent",
        "data": response.data
    }


def get_incoming_requests(user_id: str):
    response = (
        supabase.table("fund_requests")
        .select("*")
        .eq("receiver_id", user_id)
        .eq("status", "pending")
        .execute()
    )

    requests = response.data or []
    return [_enrich_request(req, "sender_id") for req in requests]


def get_pending_request_count(user_id: str) -> int:
    return len(get_incoming_requests(user_id))


def get_sent_requests(user_id: str):
    response = (
        supabase.table("fund_requests")
        .select("*")
        .eq("sender_id", user_id)
        .execute()
    )

    requests = response.data or []
    return [_enrich_request(req, "receiver_id") for req in requests]


def _get_request_for_receiver(request_id: str, receiver_id: str):
    response = (
        supabase.table("fund_requests")
        .select("*")
        .eq("receiver_id", receiver_id)
        .execute()
    )

    for req in response.data or []:
        if str(_resolve_request_id(req)) == str(request_id):
            return req

    return None


def _update_request_status(request: dict, status: str):
    resolved_id = _resolve_request_id(request)
    id_column = "request_id" if request.get("request_id") is not None else "id"

    return (
        supabase.table("fund_requests")
        .update({"status": status})
        .eq(id_column, resolved_id)
        .execute()
    )


def accept_request(request_id: str, receiver_id: str):
    request = _get_request_for_receiver(request_id, receiver_id)
    if not request:
        return {"success": False, "message": "Request not found"}

    project_title = _get_project_title(request["project_id"])
    response = _update_request_status(request, "accepted")

    return {
        "success": True,
        "data": response.data,
        "request": request,
        "notification_message": (
            f'I accepted your fund request for "{project_title}".'
        ),
    }


def reject_request(request_id: str, receiver_id: str):
    request = _get_request_for_receiver(request_id, receiver_id)
    if not request:
        return {"success": False, "message": "Request not found"}

    project_title = _get_project_title(request["project_id"])
    response = _update_request_status(request, "rejected")

    return {
        "success": True,
        "data": response.data,
        "request": request,
        "notification_message": (
            f'I declined your fund request for "{project_title}".'
        ),
    }
