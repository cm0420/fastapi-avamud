# app/repositories/payment_report_repository.py

from sqlmodel import Session, select, func, col, case
from datetime import datetime
from typing import List, Dict, Any
from app.models.models import Payment, User, PaymentStatus


class PaymentReportRepository:

    def get_inadimplentes(self, session: Session) -> List[Dict[str, Any]]:
        """
        Retorna lista de usuários com pagamentos vencidos e não pagos.
        """
        # Regra: Status não é APROVADO e data_vencimento < hoje
        hoje = datetime.now()

        statement = (
            select(
                User.id,
                User.nome,
                User.email,
                User.telefone,
                func.sum(Payment.valor).label("total_devido"),
                func.count(Payment.id).label("qtd_boletos"),
                # Calcula média de dias de atraso (aproximado)
                func.avg(func.datediff(hoje, Payment.data_vencimento)).label("dias_atraso")
            )
            .join(Payment)
            .where(Payment.status != PaymentStatus.APROVADO)
            .where(Payment.data_vencimento < hoje)
            .group_by(User.id, User.nome, User.email, User.telefone)
            .order_by(col("total_devido").desc())
        )

        results = session.exec(statement).all()

        # Converte o resultado (Row) para dicionário para o Service processar
        return [
            {
                "user_id": r[0],
                "nome": r[1],
                "email": r[2],
                "telefone": r[3],
                "total_devido": r[4],
                "quantidade_boletos_abertos": r[5],
                "dias_atraso_medio": int(r[6]) if r[6] else 0
            }
            for r in results
        ]

    def get_arrecadacao_por_periodo(self, session: Session, ano: int) -> List[Dict[str, Any]]:
        """
        Retorna o total arrecadado vs pendente agrupado por mês do ano informado.
        """
        # Extrai o mês da data de vencimento ou pagamento
        mes_col = func.extract('month', Payment.data_vencimento).label('mes')

        statement = (
            select(
                mes_col,
                # Soma valor SE status == APROVADO
                func.sum(case((Payment.status == PaymentStatus.APROVADO, Payment.valor), else_=0)).label(
                    "total_arrecadado"),
                # Soma valor SE status != APROVADO
                func.sum(case((Payment.status != PaymentStatus.APROVADO, Payment.valor), else_=0)).label(
                    "total_pendente"),
                func.count(Payment.id).label("qtd_total")
            )
            .where(func.extract('year', Payment.data_vencimento) == ano)
            .group_by(mes_col)
            .order_by(mes_col)
        )

        results = session.exec(statement).all()

        return [
            {
                "mes": f"{ano}-{int(r[0]):02d}",  # Formato YYYY-MM
                "total_arrecadado": r[1] or 0,
                "total_pendente": r[2] or 0,
                "qtd_pagamentos_confirmados": r[3]
            }
            for r in results
        ]