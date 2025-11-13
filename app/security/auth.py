# app/security/auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.db.database import get_session # Dependência da Sessão
from app.services.user_service import UserService
from app.dependencies import get_user_service # Dependência do Serviço
from app.security import jwt # Nosso utilitário JWT
from app.models.models import User


# 1. Isto define o "esquema" de segurança.
# O 'tokenUrl' aponta para o endpoint de login que AINDA VAMOS CRIAR.
# É o equivalente a configurar o 'loginProcessingUrl' no Spring Security.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    # 2. Injeta as dependências que precisamos
    token: str = Depends(oauth2_scheme), 
    session: Session = Depends(get_session),
    user_service: UserService = Depends(get_user_service)
) -> User:
    """
    Esta função é a nossa "Dependência de Segurança".
    Ela faz o trabalho do AuthFilterToken e 
    UserDetailServiceImpl combinados.
    """
    
    # 3. Define uma exceção padrão (equivalente ao AuthEntrypointJwt)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 4. Decodifica o token (vem do jwt.py)
    payload = jwt.decode_token(token)
    if payload is None:
        raise credentials_exception
    
    # 5. Pega o 'subject' (username) do token
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    # 6. Busca o usuário no banco (o trabalho do UserDetailServiceImpl)
    user = user_service.get_user_by_login(session, login=username)
    
    # 7. Se não encontrar, lança a exceção
    if user is None:
        raise credentials_exception
        
    # 8. Retorna o objeto User completo
    return user