# app/routers/report_router.py

from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from typing import List
from datetime import datetime

from app.db.database import get_session
from app.security.auth import get_current_user
from app.models.models import User
from app.schemas.schemas import ReportDebtor, ReportRevenue
from app.dependencies import get_report_service # Vamos criar esta dependência já já
from app.services.payment_report_service import PaymentReportService

router = APIRouter(
    prefix="/reports",
    tags=["Relatórios"],
    dependencies=[Depends(get_current_user)] # Apenas logados
)

@router.get("/inadimplencia", response_model=List[ReportDebtor])
def get_inadimplentes(
    session: Session = Depends(get_session),
    service: PaymentReportService = Depends(get_report_service),
    current_user: User = Depends(get_current_user)
):
    """
    Lista membros com pagamentos vencidos.
    (Idealmente restrito a ADMIN/TESOUREIRO)
    """
    return service.gerar_relatorio_inadimplencia(session)

@router.get("/arrecadacao", response_model=List[ReportRevenue])
def get_arrecadacao(
    ano: int = datetime.now().year, # Padrão é o ano atual
    session: Session = Depends(get_session),
    service: PaymentReportService = Depends(get_report_service),
    current_user: User = Depends(get_current_user)
):
    """
    Mostra o total arrecadado por mês no ano selecionado.
    """
    return service.gerar_relatorio_arrecadacao(session, ano)