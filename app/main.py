# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.models import models
from app.db.database import create_db_and_tables
# Importa todos os routers, incluindo o novo report_router
from app.routers import auth_router, user_router, address_router, payment_router, report_router, document_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

# --- Registro de Rotas (Endpoints) ---
app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(user_router.router, prefix="/api/v1")
app.include_router(address_router.router, prefix="/api/v1")
app.include_router(payment_router.router, prefix="/api/v1")
app.include_router(report_router.router, prefix="/api/v1") # <--- Novo módulo de Relatórios

app.include_router(document_router.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Bem vindo à API AVAMUD!"}

