from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session
from typing import List

from app.db.database import get_session
from app.services.payment_service import PaymentService
from app.services.payment_history_service import PaymentHistoryService
from app.dependencies import get_payment_service, get_history_service
from app.security.auth import get_current_user
from app.models.models import User
from app.schemas.schemas import (
    PaymentCreate, PaymentRead, PaymentUpdate,
    PaymentHistoryRead, PaymentAttachProof, PaymentReview
)

router = APIRouter(
    prefix="/payments",
    tags=["Pagamentos"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment(
        payment_in: PaymentCreate,
        session: Session = Depends(get_session),
        payment_service: PaymentService = Depends(get_payment_service),
        current_user: User = Depends(get_current_user)
):
    """Gera uma nova cobrança (Carnê)."""
    return payment_service.create_payment(session, payment_in)


@router.post("/{id}/comprovante", response_model=PaymentRead)
def upload_comprovante(
        id: int,
        proof_data: PaymentAttachProof,
        session: Session = Depends(get_session),
        service: PaymentService = Depends(get_payment_service),
        current_user: User = Depends(get_current_user)
):
    """Membro: Anexa o link do comprovante."""
    # Validação extra: só o próprio usuário deve anexar (ou admin)
    payment = service.get_payment_by_id(session, id)
    if payment and payment.user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Não autorizado a mexer neste pagamento.")

    return service.anexar_comprovante(session, id, proof_data, current_user.id)


@router.post("/{id}/validar", response_model=PaymentRead)
def validar_pagamento(
        id: int,
        review_data: PaymentReview,
        session: Session = Depends(get_session),
        service: PaymentService = Depends(get_payment_service),
        current_user: User = Depends(get_current_user)
):
    """Tesoureiro: Aprova ou Rejeita o pagamento."""
    return service.validar_pagamento(session, id, review_data, current_user.id)


@router.get("/", response_model=List[PaymentRead])
def get_all_payments(
        session: Session = Depends(get_session),
        payment_service: PaymentService = Depends(get_payment_service)
):
    return payment_service.get_all_payments(session)


@router.get("/{id}", response_model=PaymentRead)
def get_payment_by_id(
        id: int,
        session: Session = Depends(get_session),
        payment_service: PaymentService = Depends(get_payment_service)
):
    db_payment = payment_service.get_payment_by_id(session, id)
    if db_payment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pagamento não encontrado")
    return db_payment


@router.put("/{id}", response_model=PaymentRead)
def update_payment(
        id: int,
        payment_in: PaymentUpdate,
        session: Session = Depends(get_session),
        payment_service: PaymentService = Depends(get_payment_service),
        current_user: User = Depends(get_current_user)
):
    updated_payment = payment_service.update_payment(
        session, id, payment_in, user_id=current_user.id
    )
    if updated_payment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pagamento não encontrado")
    return updated_payment


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(
        id: int,
        session: Session = Depends(get_session),
        payment_service: PaymentService = Depends(get_payment_service),
        current_user: User = Depends(get_current_user)
):
    deleted = payment_service.delete_payment(session, id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pagamento não encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- Endpoints de Histórico ---

@router.get("/history", response_model=List[PaymentHistoryRead])
def get_all_payment_history(
        session: Session = Depends(get_session),
        history_service: PaymentHistoryService = Depends(get_history_service)
):
    return history_service.get_all_history(session)


@router.get("/{payment_id}/history", response_model=List[PaymentHistoryRead])
def get_payment_history(
        payment_id: int,
        session: Session = Depends(get_session),
        history_service: PaymentHistoryService = Depends(get_history_service)
):
    return history_service.get_history_by_payment_id(session, payment_id)

