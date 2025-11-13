# app/services/auth_service.py

from sqlmodel import Session
from typing import Optional
from app.services.user_service import UserService
from app.security.hashing import Hasher
from app.security import jwt
from app.schemas.schemas import AuthRequest, AuthResponse

class AuthService:
    """
    Equivalente ao AuthService.java
    """
    
    def __init__(self, user_service: UserService):
        """Recebe o UserService por injeção"""
        self.user_service = user_service

    def login(self, session: Session, auth_data: AuthRequest) -> Optional[AuthResponse]:
        """
        Verifica as credenciais e retorna um token.
        """
        
        # 1. Busca o usuário pelo login (username)
        user = self.user_service.get_user_by_login(
            session, login=auth_data.username
        )
        
        # 2. Verifica se o usuário existe E se a senha bate
        if not user or not Hasher.verify_password(auth_data.password, user.senha):
            return None # Retorna None se a autenticação falhar
            
        # 3. Cria o payload do token
        token_data = {
            "username": user.login,
            "user_id": user.id
            # Você pode adicionar outros dados aqui (ex: roles)
        }
        
        # 4. Gera o token JWT
        token = jwt.create_access_token(data=token_data)
        
        return AuthResponse(token=token)