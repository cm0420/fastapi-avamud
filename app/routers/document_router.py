# app/routers/document_router.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session
from datetime import date

from app.db.database import get_session
from app.services.document_service import DocumentService
from app.services.payment_service import PaymentService
from app.services.user_service import UserService
from app.dependencies import get_document_service, get_payment_service, get_user_service
from app.security.auth import get_current_user
from app.models.models import User, PaymentStatus

router = APIRouter(
    prefix="/documents",
    tags=["Documentos (PDF)"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/receipt/{payment_id}")
def download_receipt(
        payment_id: int,
        session: Session = Depends(get_session),
        doc_service: DocumentService = Depends(get_document_service),
        payment_service: PaymentService = Depends(get_payment_service),
        current_user: User = Depends(get_current_user)
):
    payment = payment_service.get_payment_by_id(session, payment_id)
    if not payment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pagamento não encontrado")

    # Regra: Só gera recibo se estiver APROVADO
    if payment.status != PaymentStatus.APROVADO:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Recibo disponível apenas para pagamentos APROVADOS.")

    # Regra: Apenas o dono ou admin pode baixar
    if current_user.role != "ADMIN" and current_user.id != payment.user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Não autorizado.")

    pdf_bytes = doc_service.gerar_recibo_pdf(payment, current_user)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=recibo_{payment_id}.pdf"}
    )


@router.get("/declaration/regularity")
def download_declaration(
        session: Session = Depends(get_session),
        doc_service: DocumentService = Depends(get_document_service),
        current_user: User = Depends(get_current_user)
):
    """Baixa a Declaração de Regularidade do usuário logado."""

    if not current_user.active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Membro inativo não pode emitir declaração.")

    # --- BLOQUEIO DE INADIMPLÊNCIA ---
    hoje = date.today()
    for p in current_user.payments:
        # Se tem boleto Pendente/Rejeitado vencido
        if p.status in [PaymentStatus.PENDENTE, PaymentStatus.REJEITADO] and p.data_vencimento.date() < hoje:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Declaração bloqueada: Existem mensalidades em atraso. Regularize sua situação."
            )
    # ----------------------------------

    pdf_bytes = doc_service.gerar_declaracao_regularidade(current_user)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=declaracao_{current_user.id}.pdf"}
    )