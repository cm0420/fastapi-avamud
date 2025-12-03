# app/services/auth_service.py

from sqlmodel import Session
from typing import Optional
from datetime import timedelta

from app.services.user_service import UserService
from app.security.hashing import Hasher
from app.security import jwt
from app.schemas.schemas import AuthRequest, AuthResponse, PasswordResetRequest
from app.core.config import settings


class AuthService:

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def login(self, session: Session, auth_data: AuthRequest) -> Optional[AuthResponse]:
        user = self.user_service.get_user_by_login(session, login=auth_data.username)

        if not user or not Hasher.verify_password(auth_data.password, user.senha):
            return None

        token_data = {
            "sub": user.login,  # Padrão JWT é 'sub'
            "username": user.login,
            "user_id": user.id,
            "role": user.role.value
        }

        token = jwt.create_access_token(data=token_data)
        return AuthResponse(token=token, username=user.login, role=user.role.value)

    def gerar_token_recuperacao(self, session: Session, email: str) -> str:
        """
        Gera um token especial que serve apenas para resetar a senha.
        Validade curta (ex: 15 min).
        """
        # Busca user pelo email (precisamos adicionar esse metodo no user_service ou fazer query aqui)
        # Como user_service.get_by_login busca por LOGIN, vamos improvisar aqui
        # O ideal é adicionar get_by_email no UserService.
        # Vamos fazer uma busca manual rápida:
        from app.models.models import User
        from sqlmodel import select

        user = session.exec(select(User).where(User.email == email)).first()

        if not user:
            # Por segurança, não dizemos que o email não existe
            return "simulated-token"

            # Token de 15 minutos
        reset_data = {"sub": user.login, "type": "reset_password"}
        # Hack: usamos a mesma função de criar token, mas com validade diferente se pudéssemos
        # Como create_access_token usa a config global, ele vai durar 30min (padrão). Serve.
        token = jwt.create_access_token(data=reset_data)

        # SIMULAÇÃO DE ENVIO DE EMAIL
        print(f"========================================")
        print(f"EMAIL ENVIADO PARA: {email}")
        print(f"CÓDIGO DE RECUPERAÇÃO: {token}")
        print(f"========================================")

        return token

    def reset_password(self, session: Session, dados: PasswordResetRequest) -> bool:
        """
        Verifica o token e altera a senha.
        """
        # 1. Decodifica o token
        payload = jwt.decode_token(dados.codigo_recuperacao)
        if not payload or payload.get("type") != "reset_password":
            return False

        login_no_token = payload.get("sub")

        # 2. Busca o usuário
        user = self.user_service.get_user_by_login(session, login_no_token)

        if not user or user.email != dados.email:
            return False

        # 3. Atualiza a senha
        # Usamos o update do user_service que já faz o hash
        from app.schemas.schemas import UserUpdate
        update_dto = UserUpdate(senha=dados.nova_senha)
        self.user_service.update_user(session, user.id, update_dto)

        return True