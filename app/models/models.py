from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum


# --- Enums para o Status do Pagamento ---
class PaymentStatus(str, Enum):
    PENDENTE = "PENDENTE"  # Aguardando pagamento
    EM_ANALISE = "EM_ANALISE"  # Membro anexou comprovante
    APROVADO = "APROVADO"  # Tesoureiro validou
    REJEITADO = "REJEITADO"  # Tesoureiro recusou


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    cpf: str = Field(unique=True, index=True)
    cnpj: str = Field(unique=True, index=True)
    telefone: str
    email: str = Field(unique=True)
    senha: str
    login: str = Field(unique=True, index=True)
    dataDeEntrada: Optional[datetime] = Field(default_factory=datetime.now)

    addresses: List["Address"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    payments: List["Payment"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    payment_history: List["PaymentHistory"] = Relationship(back_populates="user")


class Address(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rua: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="addresses")


class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Dados Financeiros
    valor: Decimal = Field(max_digits=10, decimal_places=2)
    data_vencimento: datetime = Field(default_factory=datetime.now)  # Data do carnê
    data_pagamento: Optional[datetime] = None  # Data real da baixa

    # Fluxo de Aprovação
    status: PaymentStatus = Field(default=PaymentStatus.PENDENTE)
    link_comprovante: Optional[str] = None
    observacao: Optional[str] = None

    # Relações
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="payments")

    history: List["PaymentHistory"] = Relationship(
        back_populates="payment",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class PaymentHistory(SQLModel, table=True):
    __tablename__ = "payment_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    action: str
    actionDate: datetime = Field(default_factory=datetime.now)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="payment_history")

    payment_id: Optional[int] = Field(default=None, foreign_key="payment.id")
    payment: Optional[Payment] = Relationship(back_populates="history")