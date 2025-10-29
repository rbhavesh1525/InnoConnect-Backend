import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
load_dotenv()

# print("DEBUG: SUPABASE_URL =", repr(os.getenv("SUPABASE_URL")))
# print("DEBUG: SUPABASE_SERVICE_ROLE_KEY =", repr(os.getenv("SUPABASE_SERVICE_ROLE_KEY")))


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_SERVICE_ROLE_KEY or not SUPABASE_URL:
    raise Exception("Supabase URL or Service Role Key is not set in environment variables.")

def get_supabase_client() -> Client:
    """
    Returns a Supabase client using the service role key.
    This should only be used on the backend.
    """
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Quick connection test
try:
    supabase = get_supabase_client()
    # If the client is created without error, consider it connected
    print("Supabase Connection successfull")
except Exception as e:
    print("Error connecting Supabase", e)
