# app/services/payment_service.py

from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date

from app.models.models import Payment, SystemConfig, User, PaymentStatus
from app.repositories.payment_repository import PaymentRepository
from app.schemas.schemas import PaymentCreate, PaymentAttachProof, PaymentReview, PaymentUpdate, SystemConfigUpdate
from app.services.payment_history_service import PaymentHistoryService

# Importa nossos Padrões
from app.patterns.state import PaymentStateFactory
from app.patterns.observer import PaymentSubject, MemberNotificationObserver


class PaymentService:
    def __init__(self, payment_repo: PaymentRepository, history_service: PaymentHistoryService):
        self.payment_repo = payment_repo
        self.history_service = history_service
        self.notifier = PaymentSubject()
        self.notifier.attach(MemberNotificationObserver())

    def get_payment_by_id(self, session: Session, id: int) -> Optional[Payment]:
        return self.payment_repo.get(session, id)

    def get_all_payments(self, session: Session) -> List[Payment]:
        return self.payment_repo.get_all(session)

    def create_payment(self, session: Session, payment_in: PaymentCreate) -> Payment:
        new_payment = self.payment_repo.create(session, payment_in)
        self.history_service.save_payment_history(session, new_payment, "Cobrança Gerada", payment_in.user_id)
        self.notifier.notify(new_payment, "Nova cobrança disponível para pagamento.")
        return new_payment

    def anexar_comprovante(self, session: Session, payment_id: int, data: PaymentAttachProof, user_id: int) -> Payment:
        payment = self.payment_repo.get(session, payment_id)
        if not payment:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pagamento não encontrado")

        state_handler = PaymentStateFactory.get_state(payment.status)
        state_handler.anexar_comprovante(payment, data.link_comprovante)

        session.add(payment)
        session.commit()
        session.refresh(payment)

        self.history_service.save_payment_history(session, payment, "Comprovante Anexado", user_id)
        self.notifier.notify(payment, "Comprovante enviado. Aguardando análise.")
        return payment

    def validar_pagamento(self, session: Session, payment_id: int, review: PaymentReview,
                          tesoureiro_id: int) -> Payment:
        payment = self.payment_repo.get(session, payment_id)
        if not payment:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Pagamento não encontrado")

        state_handler = PaymentStateFactory.get_state(payment.status)
        state_handler.validar(payment, review.aprovado, review.observacao)

        session.add(payment)
        session.commit()
        session.refresh(payment)

        acao_hist = "Aprovado" if review.aprovado else "Rejeitado"
        self.history_service.save_payment_history(session, payment, f"Validação: {acao_hist}", tesoureiro_id)
        msg_notificacao = "Pagamento confirmado!" if review.aprovado else f"Pagamento recusado: {review.observacao}"
        self.notifier.notify(payment, msg_notificacao)
        return payment

    def update_payment(self, session: Session, id: int, payment_in: PaymentUpdate, user_id: int) -> Optional[Payment]:
        db_payment = self.payment_repo.get(session, id)
        if not db_payment:
            return None
        updated_payment = self.payment_repo.update(session, db_obj=db_payment, obj_in=payment_in)
        self.history_service.save_payment_history(session=session, payment=updated_payment,
                                                  action="Dados Atualizados (Admin)", user_id=user_id)
        return updated_payment

    def delete_payment(self, session: Session, id: int, user_id: int) -> bool:
        db_payment = self.payment_repo.get(session, id)
        if not db_payment:
            return False
        deleted = self.payment_repo.delete(session, id)
        return deleted

    def cancelar_pagamento(self, session: Session, id: int, motivo: str, user_id: int) -> Optional[Payment]:
        payment = self.payment_repo.get(session, id)
        if not payment:
            return None
        state_handler = PaymentStateFactory.get_state(payment.status)
        state_handler.cancelar(payment, motivo)
        session.add(payment)
        session.commit()
        session.refresh(payment)
        self.history_service.save_payment_history(session, payment, f"Cancelado: {motivo}", user_id)
        self.notifier.notify(payment, f"Pagamento cancelado. Motivo: {motivo}")
        return payment

    # --- MÉTODOS DE CONFIGURAÇÃO ---

    def get_config(self, session: Session) -> SystemConfig:
        statement = select(SystemConfig)
        config = session.exec(statement).first()
        if not config:
            config = SystemConfig(valor_mensalidade=50.00, dia_vencimento=10)
            session.add(config)
            session.commit()
            session.refresh(config)
        return config

    def update_config(self, session: Session, config_in: SystemConfigUpdate) -> SystemConfig:
        config = self.get_config(session)
        if config_in.valor_mensalidade is not None:
            config.valor_mensalidade = config_in.valor_mensalidade
        if config_in.dia_vencimento is not None:
            config.dia_vencimento = config_in.dia_vencimento
        session.add(config)
        session.commit()
        session.refresh(config)
        return config

    def gerar_mensalidades_lote(self, session: Session, user_id_admin: int) -> dict:
        config = self.get_config(session)
        hoje = date.today()
        try:
            data_vencimento = date(hoje.year, hoje.month, config.dia_vencimento)
        except ValueError:
            data_vencimento = date(hoje.year, hoje.month, 28)

        users = session.exec(select(User).where(User.active == True)).all()
        criados = 0
        ignorados = 0

        for user in users:
            # Verifica duplicidade
            exists = session.exec(
                select(Payment)
                .where(Payment.user_id == user.id)
                .where(Payment.data_vencimento == data_vencimento)
                .where(Payment.valor == config.valor_mensalidade)
            ).first()

            if exists:
                ignorados += 1
                continue

            novo_pagamento = Payment(
                user_id=user.id,
                valor=config.valor_mensalidade,
                data_vencimento=data_vencimento,
                status=PaymentStatus.PENDENTE,
                observacao="Mensalidade Automática"
            )
            session.add(novo_pagamento)
            criados += 1

        session.commit()
        return {
            "mensagem": "Processamento concluído",
            "cobrancas_geradas": criados,
            "usuarios_ignorados_ja_existentes": ignorados,
            "data_vencimento_definida": data_vencimento
        }