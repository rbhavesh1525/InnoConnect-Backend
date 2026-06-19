from database.dbconfig import get_supabase_client

supabase = get_supabase_client()


def send_message(sender_id, receiver_id, message):

    result = (
        supabase.table("messages")
        .insert({
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message": message
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