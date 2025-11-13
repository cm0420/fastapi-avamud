# app/routers/user_router.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session
from typing import List

from app.db.database import get_session
from app.services.user_service import UserService
from app.dependencies import get_user_service
from app.security.auth import get_current_user # Nossa dependência de segurança!
from app.models.models import User
from app.schemas.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Usuários"] # Equivalente ao @RequestMapping("/users")
)

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate, # @RequestBody
    session: Session = Depends(get_session),
    user_service: UserService = Depends(get_user_service)
):
    """
    Cria um novo usuário. Endpoint público.
    Equivalente ao @PostMapping
    """
    # Em Python, verificações de "já existe" são feitas no endpoint
    db_user = user_service.get_user_by_login(session, login=user_in.login)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login já cadastrado."
        )
    
    new_user = user_service.create_user(session, user_in)
    return new_user


@router.get("/", response_model=List[UserRead])
def get_all_users(
    session: Session = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
    # SEGURANÇA: Só usuários logados podem listar todos os usuários
    current_user: User = Depends(get_current_user)
):
    """
    Lista todos os usuários. Endpoint protegido.
    Equivalente ao @GetMapping
    """
    return user_service.get_all_users(session)


@router.get("/{id}", response_model=UserRead)
def get_user_by_id(
    id: int, # @PathVariable
    session: Session = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
    # SEGURANÇA: Só usuários logados podem buscar
    current_user: User = Depends(get_current_user)
):
    """
    Busca um usuário pelo ID. Endpoint protegido.
    Equivalente ao @GetMapping("/{id}")
    """
    db_user = user_service.get_user_by_id(session, id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuário não encontrado"
        )
    return db_user


@router.put("/{id}", response_model=UserRead)
def update_user(
    id: int, # @PathVariable
    user_in: UserUpdate, # @RequestBody
    session: Session = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
    # SEGURANÇA: Só usuários logados podem atualizar
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza um usuário. Endpoint protegido.
    Equivalente ao @PutMapping
    """
    # Apenas permitimos que um usuário atualize a si mesmo (exemplo de regra)
    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a atualizar este usuário"
        )
        
    updated_user = user_service.update_user(session, id, user_in)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuário não encontrado"
        )
    return updated_user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int, # @PathVariable
    session: Session = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
    # SEGURANÇA: Só usuários logados podem deletar
    current_user: User = Depends(get_current_user)
):
    """
    Deleta um usuário. Endpoint protegido.
    Equivalente ao @DeleteMapping("/{id}")
    """
    # Regra de negócio: Apenas o próprio usuário pode se deletar
    if id != current_user.id:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a deletar este usuário"
        )
        
    deleted = user_service.delete_user(session, id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuário não encontrado"
        )
    
    # Retorna uma resposta vazia com status 204
    return Response(status_code=status.HTTP_204_NO_CONTENT)