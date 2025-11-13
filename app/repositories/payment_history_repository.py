# app/repositories/payment_history_repository.py

from sqlmodel import Session, select
from typing import List

from app.models.models import PaymentHistory
from app.schemas.schemas import SQLModel # Usamos SQLModel genérico para C/U
from app.repositories.base_repository import BaseRepository

# Note: Não temos Create/Update para History, então podemos usar um genérico
class PaymentHistoryRepository(BaseRepository[PaymentHistory, SQLModel, SQLModel]):
    
    def __init__(self):
        super().__init__(PaymentHistory)

    def find_by_payment_id(self, session: Session, payment_id: int) -> List[PaymentHistory]:
        """
        Equivalente ao findByPaymentId(Long paymentId)
        """
        statement = select(PaymentHistory).where(PaymentHistory.payment_id == payment_id)
        return session.exec(statement).all()