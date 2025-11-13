from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    cpf: str = Field(unique=True, index=True)
    cnpj: str = Field(unique=True, index=True)
    telefone: str
    email: str = Field(unique=True)
    senha: str  # Armazenará o hash
    login: str = Field(unique=True, index=True)

    dataDeEntrada: Optional[datetime] = Field(default_factory=datetime.now)
    

    adresses: List["Address"] = Relationship(back_populates="user",
                                              sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    
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
    
    # Relação (similar ao @ManyToOne com @JoinColumn)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="addresses")


class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Equivalente ao BigDecimal do Java
    valor: Decimal = Field(max_digits=10, decimal_places=2) 
    dataPagamento: datetime = Field(default_factory=datetime.now)

    # Relação
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="payments")
    
    # Relação
    history: List["PaymentHistory"] = Relationship(
        back_populates="payment", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class PaymentHistory(SQLModel, table=True):
    # Damos um nome explícito para a tabela, igual no @Table(name="...")
    __tablename__ = "payment_history" 
    
    id: Optional[int] = Field(default=None, primary_key=True)
    action: str
    actionDate: datetime = Field(default_factory=datetime.now)

    # Relações
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="payment_history")
    
    payment_id: Optional[int] = Field(default=None, foreign_key="payment.id")
    payment: Optional[Payment] = Relationship(back_populates="history")
