# app/services/address_service.py

from sqlmodel import Session
from typing import List, Optional
from app.models.models import Address
from app.repositories.address_repository import AddressRepository
from app.schemas.schemas import AddressCreate, AddressUpdate

class AddressService:
    def __init__(self, address_repo: AddressRepository):
        self.address_repo = address_repo

    def get_address_by_id(self, session: Session, id: int) -> Optional[Address]:
        return self.address_repo.get(session, id)

    def get_all_addresses(self, session: Session) -> List[Address]:
        return self.address_repo.get_all(session)

    def create_address(self, session: Session, address_in: AddressCreate) -> Address:
        return self.address_repo.create(session, address_in)

    def update_address(
        self, session: Session, id: int, address_in: AddressUpdate
    ) -> Optional[Address]:
        db_address = self.address_repo.get(session, id)
        if not db_address:
            return None
        return self.address_repo.update(session, db_obj=db_address, obj_in=address_in)

    def delete_address(self, session: Session, id: int) -> bool:
        return self.address_repo.delete(session, id)