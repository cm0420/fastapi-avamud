# app/repositories/address_repository.py

from app.models.models import Address
from app.schemas.schemas import AddressCreate, AddressUpdate
from app.repositories.base_repository import BaseRepository

class AddressRepository(BaseRepository[Address, AddressCreate, AddressUpdate]):
    
    def __init__(self):
        # Informa à classe Base que este repositório gerencia 'Address'
        super().__init__(Address)

# Nota: Como seu AddressRepository.java não tinha métodos
# customizados (como findBy...), este arquivo fica bem simples.