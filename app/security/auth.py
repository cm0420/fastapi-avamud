# app/security/auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  # <--- Mudança aqui
from sqlmodel import Session

from app.db.database import get_session
from app.services.user_service import UserService
from app.dependencies import get_user_service
from app.security import jwt
from app.models.models import User

# Usamos HTTPBearer para aparecer uma caixa de texto simples no Swagger
security = HTTPBearer()


def get_current_user(
        auth: HTTPAuthorizationCredentials = Depends(security),  # <--- O token vem aqui dentro
        session: Session = Depends(get_session),
        user_service: UserService = Depends(get_user_service)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extrai o token da credencial (O Swagger envia "Bearer <token>")
    token = auth.credentials

    # Decodifica o token
    payload = jwt.decode_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")  # No jwt.py usamos "sub" ou "username"? Vamos conferir.
    # ATENÇÃO: No seu jwt.py você usou 'username' no payload, não 'sub'.
    # Vou ajustar para garantir que funcione com o seu jwt.py atual.
    if username is None:
        username = payload.get("username")  # Tenta pegar pelo campo username

    if username is None:
        raise credentials_exception

    user = user_service.get_user_by_login(session, login=username)

    if user is None:
        raise credentials_exception

    return user