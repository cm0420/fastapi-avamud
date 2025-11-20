from sqlmodel import Session
from typing import List, Optional
from app.models.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.schemas import UserCreate, UserUpdate
from app.security.hashing import Hasher


class UserService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user_by_id(self, session: Session, id: int) -> Optional[User]:
        return self.user_repo.get(session, id)

    def get_all_users(self, session: Session) -> List[User]:
        return self.user_repo.get_all(session)

    def get_user_by_login(self, session: Session, login: str) -> Optional[User]:
        return self.user_repo.get_by_login(session, login)

    def create_user(self, session: Session, user_in: UserCreate) -> User:
        # Garante hash da senha ao criar
        hashed_password = Hasher.get_hash_password(user_in.senha)
        user_data_db = user_in.model_copy(update={"senha": hashed_password})
        return self.user_repo.create(session, user_data_db)

    def update_user(
            self, session: Session, id: int, user_in: UserUpdate
    ) -> Optional[User]:
        db_user = self.user_repo.get(session, id)
        if not db_user:
            return None

        # Se vier senha nova, faz hash
        if user_in.senha:
            user_in.senha = Hasher.get_hash_password(user_in.senha)

        return self.user_repo.update(session, db_obj=db_user, obj_in=user_in)

    def delete_user(self, session: Session, id: int) -> bool:
        """
        Soft Delete: Inativa o usuário em vez de apagar.
        """
        db_user = self.user_repo.get(session, id)
        if not db_user:
            return False

        db_user.active = False
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return True

    def reactivate_user(self, session: Session, id: int) -> Optional[User]:
        """
        Reativa um usuário inativado.
        """
        db_user = self.user_repo.get(session, id)
        if not db_user:
            return None

        db_user.active = True
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user