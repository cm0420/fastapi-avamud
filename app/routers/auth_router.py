# app/routers/auth_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.database import get_session
from app.services.auth_service import AuthService
from app.dependencies import get_auth_service
from app.schemas.schemas import AuthRequest, AuthResponse, PasswordRecoveryRequest, PasswordResetRequest

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

@router.post("/login", response_model=AuthResponse)
def login(
    auth_data: AuthRequest,
    session: Session = Depends(get_session),
    auth_service: AuthService = Depends(get_auth_service)
):
    token = auth_service.login(session, auth_data)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login ou senha incorretos"
        )
    return token

@router.post("/recover")
def request_password_recovery(
    data: PasswordRecoveryRequest,
    session: Session = Depends(get_session),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Solicita recuperação de senha.
    O sistema vai 'enviar' um código para o email (ver no terminal).
    """
    auth_service.gerar_token_recuperacao(session, data.email)
    return {"message": "Se o email existir, você receberá as instruções."}

@router.post("/reset-password")
def reset_password(
    data: PasswordResetRequest,
    session: Session = Depends(get_session),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Define a nova senha usando o código recebido.
    """
    sucesso = auth_service.reset_password(session, data)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código inválido ou email incorreto."
        )
    return {"message": "Senha alterada com sucesso!"}