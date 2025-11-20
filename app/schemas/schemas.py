from sqlmodel import SQLModel
from pydantic import EmailStr, BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models.models import PaymentStatus, Role


# --- Schemas de Autenticação ---
class AuthRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    token: str


# --- Schemas de Address ---
class AddressBase(SQLModel):
    rua: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str


class AddressCreate(AddressBase):
    user_id: int


class AddressRead(AddressBase):
    id: int
    user_id: int


class AddressUpdate(AddressBase):
    pass


# --- Schemas de Payment ---
class PaymentBase(SQLModel):
    valor: Decimal
    data_vencimento: datetime


class PaymentCreate(PaymentBase):
    user_id: int


class PaymentRead(PaymentBase):
    id: int
    user_id: int
    status: PaymentStatus
    link_comprovante: Optional[str]
    observacao: Optional[str]
    data_pagamento: Optional[datetime]
    data_vencimento: datetime
    valor: Decimal


class PaymentUpdate(BaseModel):
    valor: Optional[Decimal] = None
    data_vencimento: Optional[datetime] = None


class PaymentAttachProof(BaseModel):
    link_comprovante: str


class PaymentReview(BaseModel):
    aprovado: bool
    observacao: Optional[str] = None


# --- Schemas de PaymentHistory ---
class PaymentHistoryRead(SQLModel):
    id: int
    action: str
    actionDate: datetime
    user_id: Optional[int]
    payment_id: int


# --- Schemas de User ---
class UserBase(SQLModel):
    nome: str
    cpf: str
    cnpj: str
    telefone: str
    email: EmailStr
    login: str
    role: Role = Role.MEMBER


class UserCreate(UserBase):
    senha: str


class UserRead(UserBase):
    id: int
    dataDeEntrada: datetime
    active: bool

    addresses: List[AddressRead] = []
    payments: List[PaymentRead] = []


class UserUpdate(UserBase):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    login: Optional[str] = None
    senha: Optional[str] = None
    role: Optional[Role] = None
    active: Optional[bool] = None


# --- Schemas de Relatórios ---
class ReportDebtor(BaseModel):
    user_id: int
    nome: str
    email: str
    telefone: str
    total_devido: Decimal
    quantidade_boletos_abertos: int
    dias_atraso_medio: int


class ReportRevenue(BaseModel):
    mes: str
    total_arrecadado: Decimal
    total_pendente: Decimal
    qtd_pagamentos_confirmados: int

# --- Schemas de Configuração ---
class SystemConfigRead(SQLModel):
    valor_mensalidade: Decimal
    dia_vencimento: int

class SystemConfigUpdate(BaseModel):
    valor_mensalidade: Optional[Decimal] = None
    dia_vencimento: Optional[int] = None