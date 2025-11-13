# app/schemas/schemas.py

from sqlmodel import SQLModel
from pydantic import EmailStr, BaseModel  # BaseModel é um DTO puro
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# --- Schemas de Autenticação (AuthDto, AcessDto) ---
# Como estes não refletem uma tabela, usamos BaseModel

class AuthRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    token: str

# --- Schemas de Address (AddressDto) ---

class AddressBase(SQLModel):
    # DTO base com campos comuns
    rua: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str

class AddressCreate(AddressBase):
    # DTO para criar (tem o user_id)
    user_id: int

class AddressRead(AddressBase):
    # DTO para ler (tem o id)
    id: int
    user_id: int
    
class AddressUpdate(AddressBase):
    # DTO para atualizar (só os campos base)
    pass

# --- Schemas de Payment (PaymentDto) ---

class PaymentBase(SQLModel):
    valor: Decimal
    dataPagamento: Optional[datetime] = None

class PaymentCreate(PaymentBase):
    user_id: int

class PaymentRead(PaymentBase):
    id: int
    user_id: int

class PaymentUpdate(PaymentBase):
    pass

# --- Schemas de PaymentHistory (PaymentHistoryDto) ---

class PaymentHistoryRead(SQLModel):
    id: int
    action: str
    actionDate: datetime
    user_id: Optional[int]
    payment_id: int

# --- Schemas de User (UserDto) ---

class UserBase(SQLModel):
    nome: str
    cpf: str
    cnpj: str
    telefone: str
    email: EmailStr # Valida o email automaticamente
    login: str

class UserCreate(UserBase):
    senha: str # Senha em texto plano, vamos fazer o hash no serviço

class UserRead(UserBase):
    id: int
    dataDeEntrada: datetime
    
    # Mostra os endereços e pagamentos aninhados na resposta
    # Igual ao @JsonManagedReference / @JsonBackReference
    addresses: List[AddressRead] = []
    payments: List[PaymentRead] = []

class UserUpdate(UserBase):
    # Campos que podem ser atualizados
    nome: Optional[str] = None
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    login: Optional[str] = None
    senha: Optional[str] = None # Permite atualização de senha opcional