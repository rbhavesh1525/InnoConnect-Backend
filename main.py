from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.project_routes import router as project_router
from routes.user_routes import router as user_router

from routes.message_routes import router as message_router

from websocket.websocket_routes import router as websocket_router


app = FastAPI(title="InnoConnect API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/auth")
app.include_router(project_router)
app.include_router(message_router)
app.include_router(websocket_router)


@app.get("/")
def home():
    return {
        "message": "InnoConnect API Running",
        "services": ["auth", "similarity", "projects"],
        "database": "supabase",
    }
