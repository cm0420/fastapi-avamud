# app/services/payment_service.py

from sqlmodel import Session
from typing import List, Optional
from app.models.models import Payment
from app.repositories.payment_repository import PaymentRepository
from app.schemas.schemas import PaymentCreate, PaymentUpdate
from app.services.payment_history_service import PaymentHistoryService

class PaymentService:
    def __init__(
        self,
        payment_repo: PaymentRepository,
        history_service: PaymentHistoryService,
    ):
        self.payment_repo = payment_repo
        self.history_service = history_service

    def get_payment_by_id(self, session: Session, id: int) -> Optional[Payment]:
        return self.payment_repo.get(session, id)

    def get_all_payments(self, session: Session) -> List[Payment]:
        return self.payment_repo.get_all(session)

    def create_payment(
        self, session: Session, payment_in: PaymentCreate
    ) -> Payment:
        """
        Cria um pagamento e salva o histórico.
        """
        # Cria o pagamento
        new_payment = self.payment_repo.create(session, payment_in)
        
        # Lógica de Negócios: Salva o histórico
        self.history_service.save_payment_history(
            session=session,
            payment=new_payment,
            action="Criado",
            user_id=payment_in.user_id,
        )
        return new_payment

    def update_payment(
        self, session: Session, id: int, payment_in: PaymentUpdate, user_id: int
    ) -> Optional[Payment]:
        """
        Atualiza um pagamento e salva o histórico.
        """
        db_payment = self.payment_repo.get(session, id)
        if not db_payment:
            return None
        
        updated_payment = self.payment_repo.update(
            session, db_obj=db_payment, obj_in=payment_in
        )
        
        # Lógica de Negócios: Salva o histórico
        self.history_service.save_payment_history(
            session=session,
            payment=updated_payment,
            action="Atualizado",
            user_id=user_id,
        )
        return updated_payment

    def delete_payment(self, session: Session, id: int, user_id: int) -> bool:
        """
        Deleta um pagamento e salva o histórico.
        """
        # Precisamos buscar o objeto antes de deletar para ter a referência
        db_payment = self.payment_repo.get(session, id)
        if not db_payment:
            return False

        deleted = self.payment_repo.delete(session, id)
        
        if deleted:
            # Lógica de Negócios: Salva o histórico
            self.history_service.save_payment_history(
                session=session,
                payment=db_payment, # Passa o objeto que foi deletado
                action="Deletado",
                user_id=user_id,
            )
        return deleted