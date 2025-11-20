# app/routers/user_router.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session
from typing import List, Optional

from app.db.database import get_session
from app.services.user_service import UserService
from app.dependencies import get_user_service
from app.security.auth import get_current_user
from app.models.models import User, Role
from app.schemas.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Usuários"]
)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
        user_in: UserCreate,
        session: Session = Depends(get_session),
        user_service: UserService = Depends(get_user_service)
):
    db_user = user_service.get_user_by_login(session, login=user_in.login)
    if db_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Login já cadastrado.")
    return user_service.create_user(session, user_in)


@router.get("/", response_model=List[UserRead])
def get_all_users(
        active_only: bool = False,
        financial_status: Optional[str] = None,  # Novo Filtro: REGULAR ou IRREGULAR
        session: Session = Depends(get_session),
        user_service: UserService = Depends(get_user_service),
        current_user: User = Depends(get_current_user)
):
    """
    Lista usuários com status financeiro calculado.
    Filtros:
    - active_only=true: Apenas ativos.
    - financial_status=IRREGULAR: Apenas quem deve.
    """
    # Usamos o novo metodo inteligente do serviço
    return user_service.get_users_with_status(
        session, active_only=active_only, status_filter=financial_status
    )


@router.get("/{id}", response_model=UserRead)
def get_user_by_id(
        id: int,
        session: Session = Depends(get_session),
        user_service: UserService = Depends(get_user_service),
        current_user: User = Depends(get_current_user)
):
    db_user = user_service.get_user_by_id(session, id)
    if db_user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    # Pequeno hack para retornar o status calculado no get by id também
    from datetime import date
    from app.models.models import PaymentStatus

    status_calc = "REGULAR"
    for p in db_user.payments:
        if p.status in [PaymentStatus.PENDENTE, PaymentStatus.REJEITADO] and p.data_vencimento.date() < date.today():
            status_calc = "IRREGULAR"
            break

    # Converte para dict para inserir o campo extra
    user_dict = db_user.model_dump()
    user_dict["status_financeiro"] = status_calc
    user_dict["addresses"] = db_user.addresses
    user_dict["payments"] = db_user.payments

    return user_dict


@router.put("/{id}", response_model=UserRead)
def update_user(
        id: int,
        user_in: UserUpdate,
        session: Session = Depends(get_session),
        user_service: UserService = Depends(get_user_service),
        current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.ADMIN and current_user.id != id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Não autorizado.")

    updated_user = user_service.update_user(session, id, user_in)
    if updated_user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return updated_user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def inactivate_user(
        id: int,
        session: Session = Depends(get_session),
        user_service: UserService = Depends(get_user_service),
        current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Apenas Admin pode inativar usuários.")

    deleted = user_service.delete_user(session, id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{id}/reactivate", response_model=UserRead)
def reactivate_user(
        id: int,
        session: Session = Depends(get_session),
        user_service: UserService = Depends(get_user_service),
        current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.ADMIN:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Apenas Admin pode reativar usuários.")

    user = user_service.reactivate_user(session, id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user