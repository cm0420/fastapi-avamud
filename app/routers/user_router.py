from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session
from typing import List

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
    """Cria um novo usuário. Público."""
    db_user = user_service.get_user_by_login(session, login=user_in.login)
    if db_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Login já cadastrado.")

    return user_service.create_user(session, user_in)


@router.get("/", response_model=List[UserRead])
def get_all_users(
        active_only: bool = False,
        session: Session = Depends(get_session),
        user_service: UserService = Depends(get_user_service),
        current_user: User = Depends(get_current_user)
):
    """Lista todos os usuários. Pode filtrar por ?active_only=true."""
    users = user_service.get_all_users(session)
    if active_only:
        return [u for u in users if u.active]
    return users


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
    return db_user


@router.put("/{id}", response_model=UserRead)
def update_user(
        id: int,
        user_in: UserUpdate,
        session: Session = Depends(get_session),
        user_service: UserService = Depends(get_user_service),
        current_user: User = Depends(get_current_user)
):
    # Apenas Admin ou o próprio dono podem editar
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
    """Inativa usuário (Soft Delete). Apenas ADMIN."""
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
    """Reativa usuário. Apenas ADMIN."""
    if current_user.role != Role.ADMIN:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Apenas Admin pode reativar usuários.")

    user = user_service.reactivate_user(session, id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    return user