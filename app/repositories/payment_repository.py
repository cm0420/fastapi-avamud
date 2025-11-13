# app/repositories/payment_repository.py

from app.models.models import Payment
from app.schemas.schemas import PaymentCreate, PaymentUpdate
from app.repositories.base_repository import BaseRepository

class PaymentRepository(BaseRepository[Payment, PaymentCreate, PaymentUpdate]):
    
    def __init__(self):
        super().__init__(Payment)

# (Similar ao Address, seu PaymentRepository.java não tinha métodos customizados)