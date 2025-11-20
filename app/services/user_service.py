# app/services/user_service.py

from sqlmodel import Session
from typing import List, Optional
from datetime import date

from app.models.models import User, PaymentStatus
from app.repositories.user_repository import UserRepository
from app.schemas.schemas import UserCreate, UserUpdate
from app.security.hashing import Hasher


class UserService:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user_by_id(self, session: Session, id: int) -> Optional[User]:
        return self.user_repo.get(session, id)

    def get_user_by_login(self, session: Session, login: str) -> Optional[User]:
        return self.user_repo.get_by_login(session, login)

    def create_user(self, session: Session, user_in: UserCreate) -> User:
        hashed_password = Hasher.get_hash_password(user_in.senha)
        user_data_db = user_in.model_copy(update={"senha": hashed_password})
        return self.user_repo.create(session, user_data_db)

    def update_user(
            self, session: Session, id: int, user_in: UserUpdate
    ) -> Optional[User]:
        db_user = self.user_repo.get(session, id)
        if not db_user:
            return None

        if user_in.senha:
            user_in.senha = Hasher.get_hash_password(user_in.senha)

        return self.user_repo.update(session, db_obj=db_user, obj_in=user_in)

    def delete_user(self, session: Session, id: int) -> bool:
        db_user = self.user_repo.get(session, id)
        if not db_user:
            return False
        db_user.active = False
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return True

    def reactivate_user(self, session: Session, id: int) -> Optional[User]:
        db_user = self.user_repo.get(session, id)
        if not db_user:
            return None
        db_user.active = True
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    # --- NOVO MeTODO: Logica de Regularidade ---
    def get_users_with_status(
            self, session: Session, active_only: bool = False, status_filter: str = None
    ) -> List[dict]:
        """
        Retorna usuários com campo extra 'status_financeiro'.
        """
        users = self.user_repo.get_all(session)
        if active_only:
            users = [u for u in users if u.active]

        results = []
        hoje = date.today()

        for user in users:
            is_irregular = False
            # Verifica se tem boleto vencido
            for p in user.payments:
                # Se está pendente ou rejeitado E a data já passou
                if p.status in [PaymentStatus.PENDENTE, PaymentStatus.REJEITADO] and p.data_vencimento.date() < hoje:
                    is_irregular = True
                    break

            status_calc = "IRREGULAR" if is_irregular else "REGULAR"

            # Filtro opcional (ex: quero ver só os IRREGULARES)
            if status_filter and status_filter.upper() != status_calc:
                continue

            # Converte para dict para injetar o campo calculado
            user_dict = user.model_dump()
            user_dict["status_financeiro"] = status_calc
            # Recoloca as listas (model_dump às vezes remove relações dependendo da config)
            user_dict["addresses"] = user.addresses
            user_dict["payments"] = user.payments

            results.append(user_dict)

        return results