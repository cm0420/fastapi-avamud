# app/routers/auth_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.database import get_session
from app.services.auth_service import AuthService
from app.dependencies import get_auth_service
from app.schemas.schemas import AuthRequest, AuthResponse

# 1. Criamos um "Router" (um mini-controlador)
# Isto é o equivalente ao @RequestMapping("/auth") na sua classe
router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"] # Agrupa os endpoints na documentação
)

@router.post("/login", response_model=AuthResponse)
def login(
    auth_data: AuthRequest, # 2. Equivalente ao @RequestBody
    session: Session = Depends(get_session), # 3. Injeta a Sessão
    auth_service: AuthService = Depends(get_auth_service) # 4. Injeta o Serviço
):
    """
    Endpoint de login, equivalente ao /auth/login
    """
    token = auth_service.login(session, auth_data)
    
    if not token:
        # Se o login falhar (serviço retornou None), lança um 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login ou senha incorretos"
        )
        
    return token