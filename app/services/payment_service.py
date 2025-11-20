from sqlmodel import Session
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status

from app.models.models import Payment, PaymentStatus
from app.repositories.payment_repository import PaymentRepository
from app.schemas.schemas import PaymentCreate, PaymentUpdate, PaymentAttachProof, PaymentReview
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

    def create_payment(self, session: Session, payment_in: PaymentCreate) -> Payment:
        """Gera uma cobrança PENDENTE (Carnê)"""
        # Criação padrão via repositório
        new_payment = self.payment_repo.create(session, payment_in)

        # Histórico
        self.history_service.save_payment_history(
            session=session,
            payment=new_payment,
            action="Cobrança Gerada (Pendente)",
            user_id=payment_in.user_id,
        )
        return new_payment

    def anexar_comprovante(self, session: Session, payment_id: int, data: PaymentAttachProof, user_id: int) -> Payment:
        """MEMBRO: Envia comprovante."""
        payment = self.payment_repo.get(session, payment_id)
        if not payment:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pagamento não encontrado")

        if payment.status not in [PaymentStatus.PENDENTE, PaymentStatus.REJEITADO]:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Não é possível enviar comprovante para este pagamento.")

        # Atualiza para análise
        payment.link_comprovante = data.link_comprovante
        payment.status = PaymentStatus.EM_ANALISE
        payment.data_pagamento = datetime.now()  # Data do envio

        session.add(payment)
        session.commit()
        session.refresh(payment)

        self.history_service.save_payment_history(
            session=session, payment=payment,
            action="Comprovante Anexado", user_id=user_id
        )
        return payment

    def validar_pagamento(self, session: Session, payment_id: int, review: PaymentReview,
                          tesoureiro_id: int) -> Payment:
        """TESOUREIRO: Aprova ou Rejeita."""
        payment = self.payment_repo.get(session, payment_id)
        if not payment:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pagamento não encontrado")

        if payment.status != PaymentStatus.EM_ANALISE:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Este pagamento não está aguardando análise.")

        acao = ""
        if review.aprovado:
            payment.status = PaymentStatus.APROVADO
            acao = "Pagamento APROVADO"
        else:
            payment.status = PaymentStatus.REJEITADO
            payment.observacao = review.observacao
            acao = f"Pagamento REJEITADO: {review.observacao}"

        session.add(payment)
        session.commit()
        session.refresh(payment)

        self.history_service.save_payment_history(
            session=session, payment=payment,
            action=acao, user_id=tesoureiro_id
        )
        return payment

    def update_payment(self, session: Session, id: int, payment_in: PaymentUpdate, user_id: int) -> Optional[Payment]:
        """Atualização administrativa (apenas valores/datas)."""
        db_payment = self.payment_repo.get(session, id)
        if not db_payment:
            return None

        updated_payment = self.payment_repo.update(session, db_obj=db_payment, obj_in=payment_in)

        self.history_service.save_payment_history(
            session=session, payment=updated_payment,
            action="Dados Atualizados (Admin)", user_id=user_id,
        )
        return updated_payment

    def delete_payment(self, session: Session, id: int, user_id: int) -> bool:
        db_payment = self.payment_repo.get(session, id)
        if not db_payment:
            return False

        deleted = self.payment_repo.delete(session, id)
        # Nota: Como o objeto foi deletado, o histórico pode falhar se houver chave estrangeira estrita.
        # Idealmente, usamos Soft Delete. Mas mantendo o padrão do seu código:
        return deleted

