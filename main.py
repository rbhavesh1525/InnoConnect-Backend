from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.project_routes import router as project_router
from routes.user_routes import router as user_router
from routes.InvestorVerificationRequest_routes import router as investor_verification_router
from routes.profile_routes import router as profile_router
from routes.follow_routes import router as follow_router
from routes.message_routes import router as message_router
from routes.projectLikes_routes import router as project_like_router
from routes.projectComments_routes import router as project_comments_router

from websocket.websocket_routes import router as websocket_router

from routes.collaboration_routes import (
    router as collaboration_router
)
from routes.innovation_routes import router as innovation_router



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
app.include_router(
    profile_router,
    prefix="/api/user"
)
app.include_router(project_router)
app.include_router(message_router)
app.include_router(websocket_router)
app.include_router(collaboration_router)
app.include_router(innovation_router)


app.include_router(
    investor_verification_router,
    prefix="/api/investor-verification",
    tags=["Investor Verification"]
)

app.include_router(
    follow_router,
    prefix="/api/follow",
    tags=["Follow"]
)

app.include_router(
    project_like_router,
    prefix="/api/project-likes",
    tags=["Project Likes"]
)

app.include_router(
    project_comments_router,
    prefix="/api/project-comments",
    tags=["Project Comments"]
)

@app.get("/")
def home():
    return {
        "message": "InnoConnect API Running",
        "services": ["auth", "similarity", "projects"],
        "database": "supabase",
    }
