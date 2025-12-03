# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
import logging

from app.models import models
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import create_db_and_tables
# Importa todos os routers, incluindo o novo report_router
from app.routers import auth_router, user_router, address_router, payment_router, report_router, document_router

logger = logging.getLogger("avamud")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

# --- CORS (permitir chamadas do dev server do frontend) ---
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Registro de Rotas (Endpoints) ---
app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(user_router.router, prefix="/api/v1")
app.include_router(address_router.router, prefix="/api/v1")
app.include_router(payment_router.router, prefix="/api/v1")
app.include_router(report_router.router, prefix="/api/v1") # <--- Novo módulo de Relatórios

app.include_router(document_router.router, prefix="/api/v1")

# --- Integração de Frontend (Static Files) ---
# NOTE: O endpoint GET / foi removido para permitir que StaticFiles sirva o index.html na raiz.
# Se precisar de um endpoint de healthcheck/status, use /api/v1/health ou similar.
# Busca por um `dist` build do frontend em ../frontend/dist
project_root = Path(__file__).resolve().parents[1]
frontend_dist = project_root / ".." / "frontend" / "dist"
frontend_dist = frontend_dist.resolve()

if frontend_dist.exists() and frontend_dist.is_dir():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
    logger.info(f"Mounted frontend from: {frontend_dist}")
else:
    logger.warning("No frontend build found. To serve the SPA, build the frontend into '../frontend/dist' using 'npm run build'.")

