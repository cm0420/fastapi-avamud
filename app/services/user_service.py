# app/services/user_service.py

from sqlmodel import Session
from typing import List, Optional

from app.models.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.schemas import UserCreate, UserUpdate
from app.security.hashing import Hasher # Importamos nosso "PasswordEncoder"

class UserService:
    """
    Camada de serviço para a lógica de negócios do Usuário.
    Equivalente ao UserService.java
    """
    
    def __init__(self, user_repo: UserRepository):
        """
        O construtor recebe o repositório.
        Isso é o equivalente ao @Autowired private UserRepository...
        """
        self.user_repo = user_repo
    
    def get_user_by_id(self, session: Session, id: int) -> Optional[User]:
        # Lógica de negócios simples: apenas chama o repositório
        return self.user_repo.get(session, id)

    def get_all_users(self, session: Session) -> List[User]:
        return self.user_repo.get_all(session)

    def get_user_by_login(self, session: Session, login: str) -> Optional[User]:
        return self.user_repo.get_by_login(session, login)

    def create_user(self, session: Session, user_in: UserCreate) -> User:
        """
        Equivalente ao seu método criarUser().
        Contém a lógica de negócios de hashing de senha.
        """
        # 1. LÓGICA DE NEGÓCIOS: Fazer o hash da senha
        hashed_password = Hasher.get_password_hash(user_in.senha)
        
        # 2. Cria um novo objeto DTO (UserCreate) com a senha hasheada
        # (Usamos .model_copy() para criar uma cópia segura)
        user_data_db = user_in.model_copy(update={"senha": hashed_password})
        
        # 3. Passa o DTO com a senha segura para o repositório criar
        return self.user_repo.create(session, user_data_db)

    def update_user(
        self, session: Session, id: int, user_in: UserUpdate
    ) -> Optional[User]:
        """Equivalente ao seu método atualizarUser()"""
        
        # 1. Busca o usuário existente no banco
        db_user = self.user_repo.get(session, id)
        if not db_user:
            return None # Usuário não encontrado
        
        # 2. LÓGICA DE NEGÓCIOS: Se a senha foi enviada na atualização,
        #    faz o hash dela. Se não, (user_in.senha é None), 
        #    o update normal (no BaseRepository) vai ignorá-la.
        if user_in.senha:
            user_in.senha = Hasher.get_password_hash(user_in.senha)
            
        # 3. Passa para o repositório atualizar
        return self.user_repo.update(session, db_obj=db_user, obj_in=user_in)

    def delete_user(self, session: Session, id: int) -> bool:
        """Equivalente ao seu método deletarUser()"""
        return self.user_repo.delete(session, id)