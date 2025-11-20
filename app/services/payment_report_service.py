# app/services/payment_report_service.py

from sqlmodel import Session
from typing import List
from app.repositories.payment_report_repository import PaymentReportRepository
from app.schemas.schemas import ReportDebtor, ReportRevenue

class PaymentReportService:
    def __init__(self, report_repo: PaymentReportRepository):
        self.report_repo = report_repo

    def gerar_relatorio_inadimplencia(self, session: Session) -> List[ReportDebtor]:
        """
        Gera o relatório de quem está a dever.
        """
        dados = self.report_repo.get_inadimplentes(session)
        # Aqui poderíamos adicionar lógica extra, como enviar endereço eletrónico de alerta (Should Have)
        # Por enquanto, apenas retorna os dados convertidos para o Schema
        return [ReportDebtor(**d) for d in dados]

    def gerar_relatorio_arrecadacao(self, session: Session, ano: int) -> List[ReportRevenue]:
        """
        Gera o fluxo de caixa do ano.
        """
        dados = self.report_repo.get_arrecadacao_por_periodo(session, ano)
        return [ReportRevenue(**d) for d in dados]

