from database.dbconfig import get_supabase_client
from dotenv import load_dotenv
from jose import jwt
import os

supabase = get_supabase_client()
load_dotenv()

JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
ALGORITHM = "HS256"


def signup_user(
    name: str,
    email: str,
    phone: str,
    password: str,
    confirmpassword: str,
    role: str
):
    """Handles user signup with validations."""

    if password != confirmpassword:
        return {
            "success": False,
            "message": "Passwords do not match"
        }

    if len(password) < 8:
        return {
            "success": False,
            "message": "Password must be at least 8 characters long"
        }

    if role not in ["innovator", "investor"]:
        return {
            "success": False,
            "message": "Invalid role selected"
        }

    try:

        user_data = supabase.auth.admin.create_user({
            "email": email.lower(),
            "password": password,
            "email_confirm": True
        })

        if not user_data.user:
            return {
                "success": False,
                "message": "User creation failed"
            }

        user_id = user_data.user.id

        res = supabase.table("users").insert({
            "user_id": user_id,
            "name": name,
            "email": email.lower(),
            "phone": phone,
            "role": role
        }).execute()

        if not res.data:
            return {
                "success": False,
                "message": "Failed to create profile"
            }

        return {
            "success": True,
            "message": "User created successfully",
            "user_id": user_id
        }

    except Exception as e:

        print("SIGNUP ERROR => ", str(e))

        return {
        "success": False,
        "message": str(e)
    }

def login_user(email: str, password: str):
    """Handles user login."""
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": email.lower(),
            "password": password
        })

        if not auth_response.user:
            # Wrong credentials
            return {"success": False, "message": "Invalid email or password"}

        user_id = auth_response.user.id
        token = jwt.encode({"user_id": user_id}, JWT_SECRET, algorithm=ALGORITHM)

        # Fetch role and verification_status from users table
        user_record = (
            supabase.table("users")
            .select("role, verification_status, name")
            .eq("user_id", user_id)
            .single()
            .execute()
        )

        user_data = user_record.data or {}

        return {
            "success": True,
            "message": "Login successful",
            "token": token,
            "user_id": user_id,
            "user": {
                "role": user_data.get("role", ""),
                "name": user_data.get("name", ""),
                "verification_status": user_data.get("verification_status", False),
            }
        }

    except Exception as e:
        # If Supabase throws any error (like invalid credentials)
        error_message = str(e)
        if "Invalid login credentials" in error_message or "Email not found" in error_message:
            return {"success": False, "message": "Invalid email or password"}
        else:
            return {"success": False, "message": "Login failed. Please try again later."}



def get_user_by_id(user_id: str):
    result = (
        supabase.table("users")
        .select("user_id,name,email")
        .eq("user_id", user_id)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]


def get_users_except_me(my_id: str):
    
    result = (
        supabase.table("users")
        .select("user_id,name,email")
        .neq("user_id", my_id)
        .execute()
    )

    return result.data


def get_admin_stats():
    """Returns dashboard stats for admin panel."""
    try:
        total_users = (
            supabase.table("users")
            .select("user_id", count="exact")
            .execute()
        )

        total_investors = (
            supabase.table("users")
            .select("user_id", count="exact")
            .eq("role", "investor")
            .execute()
        )

        pending_requests = (
            supabase.table("investor_verification_requests")
            .select("id", count="exact")
            .eq("status", "pending")
            .execute()
        )

        approved_investors = (
            supabase.table("investor_verification_requests")
            .select("id", count="exact")
            .eq("status", "approved")
            .execute()
        )

        return {
            "success": True,
            "total_users":         total_users.count or 0,
            "total_investors":     total_investors.count or 0,
            "pending_requests":    pending_requests.count or 0,
            "approved_investors":  approved_investors.count or 0,
        }

    except Exception as e:
        return {"success": False, "message": str(e)}