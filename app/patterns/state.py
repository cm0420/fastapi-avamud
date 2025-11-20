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
        pass

    @abstractmethod
    def validar(self, payment: Payment, aprovado: bool, observacao: str = None):
        """Tenta validar (Aprovar/Rejeitar)"""
        pass

    @abstractmethod
    def cancelar(self, payment: Payment, motivo: str):
        """Tenta cancelar o pagamento"""
        pass


# 2. Estados Concretos

class PendenteState(PaymentState):
    def anexar_comprovante(self, payment: Payment, link: str):
        # De Pendente -> Em Análise
        payment.link_comprovante = link
        payment.status = PaymentStatus.EM_ANALISE
        payment.data_pagamento = datetime.now()

    def validar(self, payment: Payment, aprovado: bool, observacao: str = None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível validar um pagamento sem comprovante (Pendente)."
        )

    def cancelar(self, payment: Payment, motivo: str):
        # Pode cancelar se estiver pendente
        payment.status = PaymentStatus.CANCELADO
        payment.motivo_cancelamento = motivo
        payment.observacao = f"Cancelado: {motivo}"


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

    def cancelar(self, payment: Payment, motivo: str):
        # Pode cancelar se estiver em análise
        payment.status = PaymentStatus.CANCELADO
        payment.motivo_cancelamento = motivo
        payment.observacao = f"Cancelado: {motivo}"


class AprovadoState(PaymentState):
    def anexar_comprovante(self, payment: Payment, link: str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pagamento já aprovado. Não pode ser alterado."
        )

    def validar(self, payment: Payment, aprovado: bool, observacao: str = None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pagamento já está finalizado (Aprovado)."
        )

    def cancelar(self, payment: Payment, motivo: str):
        # Regra de negócio: Pode cancelar pagamento aprovado? (Estorno)
        # Vamos permitir para simplificar
        payment.status = PaymentStatus.CANCELADO
        payment.motivo_cancelamento = motivo
        payment.observacao = f"Cancelado (Estorno): {motivo}"


class RejeitadoState(PaymentState):
    def anexar_comprovante(self, payment: Payment, link: str):
        # Permite reenviar para tentar aprovar de novo
        payment.link_comprovante = link
        payment.status = PaymentStatus.EM_ANALISE
        payment.observacao = None  # Limpa a rejeição anterior
        payment.data_pagamento = datetime.now()

    def validar(self, payment: Payment, aprovado: bool, observacao: str = None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pagamento rejeitado deve receber novo comprovante antes de validar."
        )

    def cancelar(self, payment: Payment, motivo: str):
        # Pode cancelar se estiver rejeitado
        payment.status = PaymentStatus.CANCELADO
        payment.motivo_cancelamento = motivo
        payment.observacao = f"Cancelado: {motivo}"


class CanceladoState(PaymentState):
    def anexar_comprovante(self, payment: Payment, link: str):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Pagamento cancelado.")

    def validar(self, payment: Payment, aprovado: bool, observacao: str = None):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Pagamento cancelado.")

    def cancelar(self, payment: Payment, motivo: str):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Pagamento já está cancelado.")


# 3. Factory
class PaymentStateFactory:
    @staticmethod
    def get_state(status: PaymentStatus) -> PaymentState:
        mapping = {
            PaymentStatus.PENDENTE: PendenteState(),
            PaymentStatus.EM_ANALISE: EmAnaliseState(),
            PaymentStatus.APROVADO: AprovadoState(),
            PaymentStatus.REJEITADO: RejeitadoState(),
            PaymentStatus.CANCELADO: CanceladoState()
        }
        return mapping.get(status, PendenteState())