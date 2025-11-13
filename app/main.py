from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.models import models
from app.db.database import create_db_and_tables
from app.routers import auth_router, user_router, address_router, payment_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_db_and_tables()
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(user_router.router, prefix="/api/v1")
app.include_router(address_router.router, prefix="/api/v1") # <-- ADICIONE ESTA LINHA
app.include_router(payment_router.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Bem vindo à API AVAMUD!"}
