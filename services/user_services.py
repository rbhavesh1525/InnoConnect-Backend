from database.dbconfig import get_supabase_client
from dotenv import load_dotenv
from jose import jwt
import os 
supabase = get_supabase_client()

load_dotenv() 

JWT_SECRET  = os.getenv("SUPABASE_JWT_SECRET")
ALGORITHM = "HS256"

def signup_user(name: str, email: str, password: str, confirmpassword: str, interests: list):
    if password != confirmpassword:
        raise Exception("Passwords do not match")

    user_data = supabase.auth.admin.create_user({
        "email": email.lower(),
        "password": password,
        "email_confirm": True,
    })

    if user_data.user is None:
        raise Exception("User creation failed")

    user_id = user_data.user.id

    res = supabase.table("users").insert({
        "user_id": user_id,
        "name": name,
        "email": email.lower(),
        "interests": interests
    }).execute()

    if not res.data:
        raise Exception(f"Failed to insert user profile: {res.data}")



    return {"message": "User created successfully", "user_id": user_id}

def login_user(email:str,password:str):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": email.lower(),
            "password": password
        })

        if auth_response.user is None:
            raise Exception("Invalid email or password")

        user_id = auth_response.user.id

        token = jwt.encode({"user_id":user_id},JWT_SECRET,algorithm=ALGORITHM)
        return {"token": token, "user_id": user_id}

    except Exception as e:
        raise Exception(f"Login failed: {str(e)}")
