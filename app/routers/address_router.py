# app/routers/address_router.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session
from typing import List

from app.db.database import get_session
from app.services.address_service import AddressService
from app.dependencies import get_address_service
from app.security.auth import get_current_user
from app.models.models import User
from app.schemas.schemas import AddressCreate, AddressRead, AddressUpdate

router = APIRouter(
    prefix="/addresses",
    tags=["Endereços"], # Equivalente ao @RequestMapping("/addresses")
    dependencies=[Depends(get_current_user)] # Protege TODOS os endpoints neste router
)

@router.post("/", response_model=AddressRead, status_code=status.HTTP_201_CREATED)
def create_address(
    address_in: AddressCreate,
    session: Session = Depends(get_session),
    address_service: AddressService = Depends(get_address_service),
    current_user: User = Depends(get_current_user) # Pega o usuário logado
):
    """
    Cria um novo endereço para o usuário logado.
    Equivalente ao @PostMapping
    """
    # Regra de Negócio: Garante que o endereço criado pertence ao usuário logado
    if address_in.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a criar endereço para outro usuário"
        )
    
    return address_service.create_address(session, address_in)


@router.get("/", response_model=List[AddressRead])
def get_all_addresses(
    session: Session = Depends(get_session),
    address_service: AddressService = Depends(get_address_service)
):
    """
    Lista todos os endereços (ADMIN endpoint - no futuro)
    Equivalente ao @GetMapping
    """
    # Nota: Idealmente, isto devia retornar apenas os endereços do usuário logado
    return address_service.get_all_addresses(session)


@router.get("/{id}", response_model=AddressRead)
def get_address_by_id(
    id: int,
    session: Session = Depends(get_session),
    address_service: AddressService = Depends(get_address_service)
):
    """
    Busca um endereço pelo ID.
    Equivalente ao @GetMapping("/{id}")
    """
    db_address = address_service.get_address_by_id(session, id)
    if db_address is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Endereço não encontrado")
    return db_address


@router.put("/{id}", response_model=AddressRead)
def update_address(
    id: int,
    address_in: AddressUpdate,
    session: Session = Depends(get_session),
    address_service: AddressService = Depends(get_address_service)
):
    """
    Atualiza um endereço.
    Equivalente ao @PutMapping("/{id}")
    """
    updated_address = address_service.update_address(session, id, address_in)
    if updated_address is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Endereço não encontrado")
    return updated_address


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    id: int,
    session: Session = Depends(get_session),
    address_service: AddressService = Depends(get_address_service)
):
    """
    Apaga um endereço.
    Equivalente ao @DeleteMapping("/{id}")
    """
    deleted = address_service.delete_address(session, id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Endereço não encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)