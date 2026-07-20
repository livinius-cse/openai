# ForgeAI — Phase 1

ForgeAI turns real-world problems into engineering opportunities. This repository contains the Phase 1 foundation: a polished product shell, authentication UI, FastAPI service skeleton, and local PostgreSQL environment.

> AI analysis and news ingestion are intentionally out of scope for Phase 1.

## Stack

- Frontend: Next.js 15, TypeScript, Tailwind CSS, shadcn-style UI primitives
- Backend: FastAPI, SQLAlchemy
- Data: PostgreSQL (Supabase-compatible)
- Local runtime: Docker Compose

## Repository layout

```
frontend/     Next.js application
backend/      FastAPI application
docker-compose.yml
```

## Run with Docker

1. Copy `.env.example` to `.env`.
2. Copy `backend/.env.example` to `backend/.env`.
3. Start the environment:

   ```bash
   docker compose up --build
   ```

4. Open [http://localhost:3000](http://localhost:3000). The API health endpoint is available at [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health).

## Run locally

### Frontend

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

For a local PostgreSQL instance, use `docker compose up db` and keep the default database URL in `backend/.env`.
