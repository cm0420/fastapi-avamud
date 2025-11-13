# app/services/payment_history_service.py

from sqlmodel import Session
from typing import List
from app.models.models import PaymentHistory, Payment
from app.repositories.payment_history_repository import PaymentHistoryRepository
from app.repositories.user_repository import UserRepository

class PaymentHistoryService:
    def __init__(self, 
                 history_repo: PaymentHistoryRepository, 
                 user_repo: UserRepository):
        self.history_repo = history_repo
        self.user_repo = user_repo

    def get_history_by_payment_id(self, session: Session, payment_id: int) -> List[PaymentHistory]:
        return self.history_repo.find_by_payment_id(session, payment_id)

    def get_all_history(self, session: Session) -> List[PaymentHistory]:
        return self.history_repo.get_all(session)

    def save_payment_history(
        self, session: Session, payment: Payment, action: str, user_id: int
    ) -> PaymentHistory:
        """
        Equivalente ao savePaymentHistory(Payment payment, String action, Long userId)
        """
        
        # Busca o usuário para associar ao histórico
        user = self.user_repo.get(session, user_id)
        if not user:
            # Em um app real, poderíamos lançar uma exceção
            # Aqui, apenas não associamos o usuário
            print(f"Usuário {user_id} não encontrado para o histórico")

        history = PaymentHistory(
            action=action,
            payment=payment,
            user=user,
            user_id=user_id,
            payment_id=payment.id
        )
        session.add(history)
        session.commit()
        session.refresh(history)
        return history