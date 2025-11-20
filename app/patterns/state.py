# app/patterns/state.py

from abc import ABC, abstractmethod
from fastapi import HTTPException, status
from datetime import datetime

from app.models.models import Payment, PaymentStatus


# 1. Interface do Estado (Define o contrato)
class PaymentState(ABC):

    @abstractmethod
    def anexar_comprovante(self, payment: Payment, link: str):
        """Tenta anexar comprovante"""
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não é possível anexar comprovante no status atual."
        )

    @abstractmethod
    def validar(self, payment: Payment, aprovado: bool, observacao: str = None):
        """Tenta validar (Aprovar/Rejeitar)"""
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não é possível validar pagamento no status atual."
        )

    @abstractmethod
    def cancelar(self, payment: Payment, motivo: str):
        """Tenta cancelar"""
        # Lógica padrão: quase todos podem cancelar, exceto se já cancelado
        payment.status = PaymentStatus.CANCELADO
        payment.motivo_cancelamento = motivo
        payment.observacao = f"Cancelado: {motivo}"


# 2. Estados Concretos

class PendenteState(PaymentState):
    def anexar_comprovante(self, payment: Payment, link: str):
        # Lógica: De Pendente -> Vai para Em Análise
        payment.link_comprovante = link
        payment.status = PaymentStatus.EM_ANALISE
        payment.data_pagamento = datetime.now()

    def validar(self, payment: Payment, aprovado: bool, observacao: str = None):
        raise HTTPException(400, "Não é possível validar um pagamento sem comprovante (Pendente).")


class EmAnaliseState(PaymentState):
    def anexar_comprovante(self, payment: Payment, link: str):
        # Permite reenviar (correção rápida antes da análise)
        payment.link_comprovante = link
        payment.data_pagamento = datetime.now()

    def validar(self, payment: Payment, aprovado: bool, observacao: str = None):
        if aprovado:
            payment.status = PaymentStatus.APROVADO
        else:
            payment.status = PaymentStatus.REJEITADO
            payment.observacao = observacao


class AprovadoState(PaymentState):
    def anexar_comprovante(self, payment: Payment, link: str):
        raise HTTPException(400, "Pagamento já aprovado. Não pode ser alterado.")

    def validar(self, payment: Payment, aprovado: bool, observacao: str = None):
        raise HTTPException(400, "Pagamento já está finalizado (Aprovado).")

    def cancelar(self, payment: Payment, motivo: str):
        # Regra de negócio: Pode cancelar pagamento aprovado? Geralmente precisa de estorno.
        # Vamos permitir com ressalva.
        super().cancelar(payment, motivo)


class RejeitadoState(PaymentState):
    def anexar_comprovante(self, payment: Payment, link: str):
        # Permite reenviar para tentar aprovar de novo
        payment.link_comprovante = link
        payment.status = PaymentStatus.EM_ANALISE
        payment.observacao = None  # Limpa a rejeição anterior
        payment.data_pagamento = datetime.now()

    def validar(self, payment: Payment, aprovado: bool, observacao: str = None):
        raise HTTPException(400, "Pagamento rejeitado deve receber novo comprovante antes de validar.")


# 3. Factory (Para recuperar a classe certa baseada no Enum do Banco)
class PaymentStateFactory:
    @staticmethod
    def get_state(status: PaymentStatus) -> PaymentState:
        mapping = {
            PaymentStatus.PENDENTE: PendenteState(),
            PaymentStatus.EM_ANALISE: EmAnaliseState(),
            PaymentStatus.APROVADO: AprovadoState(),
            PaymentStatus.REJEITADO: RejeitadoState(),
            PaymentStatus.CANCELADO: AprovadoState()  # Usa lógica restritiva do aprovado ou cria um CanceladoState
        }
        return mapping.get(status, PendenteState())
