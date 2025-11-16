# app/services/payment_service.py

from sqlmodel import Session
from typing import List, Optional
# (NOVO) Importar para lançar erros de regra de negócio
from fastapi import HTTPException, status
from app.models.models import Payment
from app.repositories.payment_repository import PaymentRepository
# (NOVO) Importar os schemas que criamos
from app.schemas.schemas import (
    PaymentCreate, PaymentUpdate, PaymentStatus, PaymentStatusUpdate
)
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




    def approve_payment(
            self, session: Session, id: int, user_id: int
    ) -> Optional[Payment]:
        """Aprova um pagamento pendente e salva o histórico."""

        db_payment = self.payment_repo.get(session, id)
        if not db_payment:
            return None

        # Lógica de Negócios: Só pode aprovar se estiver PENDENTE
        if db_payment.status != PaymentStatus.PENDENTE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Pagamento não está pendente (Status atual: {db_payment.status})"
            )

        # Prepara o DTO de atualização de status
        status_update_dto = PaymentStatusUpdate(status=PaymentStatus.APROVADO)

        # Usa o repositório base para atualizar o objeto
        updated_payment = self.payment_repo.update(
            session, db_obj=db_payment, obj_in=status_update_dto
        )

        # Lógica de Negócios: Salva o histórico (como você já fazia)
        self.history_service.save_payment_history(
            session=session,
            payment=updated_payment,
            action=PaymentStatus.APROVADO.value,  # "Aprovado"
            user_id=user_id,
        )
        return updated_payment


    def cancel_payment(
            self, session: Session, id: int, user_id: int
    ) -> Optional[Payment]:
        """Cancela um pagamento e salva o histórico."""

        db_payment = self.payment_repo.get(session, id)
        if not db_payment:
            return None

        # Lógica de Negóto: Não pode cancelar um pagamento já aprovado
        if db_payment.status == PaymentStatus.APROVADO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível cancelar um pagamento já aprovado"
            )
        # Se já estiver cancelado, apenas retorne
        if db_payment.status == PaymentStatus.CANCELADO:
            return db_payment

        status_update_dto = PaymentStatusUpdate(status=PaymentStatus.CANCELADO)

        updated_payment = self.payment_repo.update(
            session, db_obj=db_payment, obj_in=status_update_dto
        )

        self.history_service.save_payment_history(
            session=session,
            payment=updated_payment,
            action=PaymentStatus.CANCELADO.value,  # "Cancelado"
            user_id=user_id,
        )
        return updated_payment

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
                payment=db_payment,  # Passa o objeto que foi deletado
                action="Deletado",
                user_id=user_id,
            )
        return deleted

