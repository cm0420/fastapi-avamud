# app/services/payment_service.py

from sqlmodel import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.models.models import Payment
from app.repositories.payment_repository import PaymentRepository
from app.schemas.schemas import PaymentCreate, PaymentAttachProof, PaymentReview, PaymentUpdate
from app.services.payment_history_service import PaymentHistoryService

# --- Importação dos Padrões de Projeto (Observer e State) ---
from app.patterns.state import PaymentStateFactory
from app.patterns.observer import PaymentSubject, MemberNotificationObserver


class PaymentService:
    def __init__(
            self,
            payment_repo: PaymentRepository,
            history_service: PaymentHistoryService,
    ):
        self.payment_repo = payment_repo
        self.history_service = history_service

        # Configuração do Observer (Notificações)
        # Aqui registramos quem deve ser avisado quando um pagamento muda de estado
        self.notifier = PaymentSubject()
        self.notifier.attach(MemberNotificationObserver())
        # Poderíamos adicionar outros: self.notifier.attach(EmailAdminObserver())

    def get_payment_by_id(self, session: Session, id: int) -> Optional[Payment]:
        return self.payment_repo.get(session, id)

    def get_all_payments(self, session: Session) -> List[Payment]:
        return self.payment_repo.get_all(session)

    def create_payment(self, session: Session, payment_in: PaymentCreate) -> Payment:
        """
        Cria uma nova cobrança (Carnê).
        Nasce com status PENDENTE (definido no Model).
        """
        new_payment = self.payment_repo.create(session, payment_in)

        # Registra no histórico
        self.history_service.save_payment_history(
            session, new_payment, "Cobrança Gerada", payment_in.user_id
        )

        # OBSERVER: Notifica que uma nova cobrança foi gerada
        self.notifier.notify(new_payment, "Nova cobrança disponível para pagamento.")

        return new_payment

    def anexar_comprovante(self, session: Session, payment_id: int, data: PaymentAttachProof, user_id: int) -> Payment:
        """
        Usa o STATE PATTERN para gerenciar a transição para EM_ANALISE.
        """
        payment = self.payment_repo.get(session, payment_id)
        if not payment:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pagamento não encontrado")

        # 1. Recupera o Estado Atual (Polimorfismo: PendenteState, RejeitadoState, etc.)
        state_handler = PaymentStateFactory.get_state(payment.status)

        # 2. Delega a lógica para a classe do estado (pode lançar erro se a transição for inválida)
        state_handler.anexar_comprovante(payment, data.link_comprovante)

        # 3. Persiste as mudanças no banco
        session.add(payment)
        session.commit()
        session.refresh(payment)

        # 4. Histórico
        self.history_service.save_payment_history(
            session, payment, "Comprovante Anexado", user_id
        )

        # 5. OBSERVER: Notifica interessados
        self.notifier.notify(payment, "Comprovante enviado. Aguardando análise do tesoureiro.")

        return payment

    def validar_pagamento(self, session: Session, payment_id: int, review: PaymentReview,
                          tesoureiro_id: int) -> Payment:
        """
        Usa o STATE PATTERN para transitar para APROVADO ou REJEITADO.
        """
        payment = self.payment_repo.get(session, payment_id)
        if not payment:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pagamento não encontrado")

        # 1. Recupera o Estado Atual
        state_handler = PaymentStateFactory.get_state(payment.status)

        # 2. Executa a validação via State
        state_handler.validar(payment, review.aprovado, review.observacao)

        # 3. Persiste
        session.add(payment)
        session.commit()
        session.refresh(payment)

        # 4. Histórico
        acao_hist = "Aprovado" if review.aprovado else "Rejeitado"
        self.history_service.save_payment_history(
            session, payment, f"Validação: {acao_hist}", tesoureiro_id
        )

        # 5. OBSERVER: Notifica o membro sobre o resultado
        msg_notificacao = "Pagamento confirmado!" if review.aprovado else f"Pagamento recusado: {review.observacao}"
        self.notifier.notify(payment, msg_notificacao)

        return payment

    def update_payment(self, session: Session, id: int, payment_in: PaymentUpdate, user_id: int) -> Optional[Payment]:
        """
        Atualização administrativa (valores/datas).
        """
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
        """
        Remove o pagamento fisicamente (Admin).
        """
        db_payment = self.payment_repo.get(session, id)
        if not db_payment:
            return False

        deleted = self.payment_repo.delete(session, id)

        # Nota: Se deletado, não há como passar o objeto 'payment' para o histórico
        # ou observer, pois ele não existe mais no banco.
        return deleted

    def cancelar_pagamento(self, session: Session, id: int, motivo: str, user_id: int) -> Optional[Payment]:
        """
        Cancelamento lógico usando o State Pattern.
        """
        payment = self.payment_repo.get(session, id)
        if not payment:
            return None

        state_handler = PaymentStateFactory.get_state(payment.status)
        state_handler.cancelar(payment, motivo)

        session.add(payment)
        session.commit()
        session.refresh(payment)

        self.history_service.save_payment_history(
            session, payment, f"Cancelado: {motivo}", user_id
        )
        self.notifier.notify(payment, f"Pagamento cancelado. Motivo: {motivo}")

        return payment