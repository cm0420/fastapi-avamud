# app/repositories/user_repository.py

from sqlmodel import Session, select
from typing import Optional

from app.models.models import User
from app.schemas.schemas import UserCreate, UserUpdate
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    
    def __init__(self):
        # Informa à classe Base que este repositório gerencia o modelo 'User'
        super().__init__(User)

    def get_by_login(self, session: Session, login: str) -> Optional[User]:
        """Equivalente ao findByLogin(login) do JpaRepository."""
        
        # Constrói a query: "SELECT * FROM user WHERE login = :login"
        statement = select(User).where(User.login == login)
        
        # Executa e pega o primeiro resultado (ou None)
        return session.exec(statement).first()

    def get_by_nome(self, session: Session, nome: str) -> Optional[User]:
        """Equivalente ao findByNome(nome) do JpaRepository."""
        statement = select(User).where(User.nome == nome)
        return session.exec(statement).first()