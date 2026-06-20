# InnoConnect Backend

Unified FastAPI backend for InnoConnect — auth and project similarity/submission, all on **Supabase**.

## Features

- **Auth:** `POST /api/auth/signup`, `POST /api/auth/login`
- **Projects:** `POST /similarity`, `POST /submit-project`

## Prerequisites

- Python 3.10+
- Supabase project

## Setup

### 1. Python environment

```bash
cd InnoConnect-Backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Supabase database schema

Open the **Supabase SQL Editor** and run the full script in `supabase/schema.sql`.

This creates:
- `users` — user profiles
- `projects` — project details
- `project_embeddings` — 768-dim vectors for similarity search

### 3. Environment variables

Copy `.env.example` to `.env` and fill in your Supabase credentials:

```bash
copy .env.example .env
```

| Variable | Where to find it |
|----------|------------------|
| `SUPABASE_URL` | Project Settings → API |
| `SUPABASE_SERVICE_ROLE_KEY` | Project Settings → API (service_role key) |
| `SUPABASE_JWT_SECRET` | Project Settings → API → JWT Settings |

### 4. Seed sample projects (optional)

```bash
python scripts/migrate_data.py
```

### 5. Run the API

```bash
uvicorn main:app --reload
```

Server: http://127.0.0.1:8000  
API docs: http://127.0.0.1:8000/docs

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| POST | `/api/auth/signup` | Register user |
| POST | `/api/auth/login` | Login user |
| POST | `/similarity` | Check for similar projects |
| POST | `/submit-project` | Submit a new project |

### Project submission body

```json
{
  "project_title": "AI Tutor",
  "description": "Adaptive learning system for students",
  "problem_statement": "Students learn at different speeds",
  "solution_overview": "AI recommends personalized study plans",
  "industry_category": "EdTech"
}
```

## Frontend

Point the frontend to this single backend:

```
VITE_API_URL=http://127.0.0.1:8000
```

Auth and project APIs both run on port 8000. No local Docker/PostgreSQL required.
