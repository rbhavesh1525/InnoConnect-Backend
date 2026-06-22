from database.dbconfig import get_supabase_client

supabase = get_supabase_client()


def send_message(sender_id, receiver_id, message):

    result = (
        supabase.table("messages")
        .insert({
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message": message,
            "is_read": False,
        })
        .execute()
    )

    return result.data[0]


def get_messages(user1_id: str, user2_id: str):

    result = (
        supabase.table("messages")
        .select("*")
        .or_(
            f"and(sender_id.eq.{user1_id},receiver_id.eq.{user2_id}),"
            f"and(sender_id.eq.{user2_id},receiver_id.eq.{user1_id})"
        )
        .order("created_at")
        .execute()
    )

    return result.data


def mark_messages_as_read(user_id: str, other_user_id: str):
    (
        supabase.table("messages")
        .update({"is_read": True})
        .eq("receiver_id", user_id)
        .eq("sender_id", other_user_id)
        .eq("is_read", False)
        .execute()
    )


def get_unread_counts(user_id: str):
    result = (
        supabase.table("messages")
        .select("sender_id")
        .eq("receiver_id", user_id)
        .eq("is_read", False)
        .execute()
    )

    by_user = {}
    for row in result.data or []:
        sender_id = row["sender_id"]
        by_user[sender_id] = by_user.get(sender_id, 0) + 1

    return {
        "by_user": by_user,
        "total": sum(by_user.values()),
    }
