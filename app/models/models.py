from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Numeric


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    nome: str
    cpf: Optional[str] = Field(default=None, unique=True, index=True)
    cnpj: Optional[str] = Field(default=None, unique=True, index=True)
    telefone: str
    email: str = Field(unique=True)
    senha: str
    login: str = Field(unique=True, index=True)

    dataDeEntrada: Optional[datetime] = Field(default_factory=datetime.now)

    # Correção: "addresses"
    addresses: List["Address"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    payments: List["Payment"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    payment_history: List["PaymentHistory"] = Relationship(
        back_populates="user"
    )


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

    # Correção: Numeric(10, 2) para Decimal
    valor: Decimal = Field(
        sa_column=Column(Numeric(10, 2), nullable=False)
    )

    dataPagamento: datetime = Field(default_factory=datetime.now)

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
