from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
from routes.user_routes import router as user_router
from fastapi.middleware.cors import CORSMiddleware

from database.dbconfig import get_supabase_client



origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # specify your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router, prefix="/api/auth")


@app.get("/")
def home():
    return {"message" : "hello world"}