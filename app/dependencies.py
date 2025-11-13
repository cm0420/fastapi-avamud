# app/dependencies.py

"""
Arquivo central para gerenciar a Injeção de Dependência (DI).
Isto é o coração da nossa arquitetura OOP,
equivalente ao container de DI do Spring (@Autowired, @Bean).
"""

# Importa todas as nossas classes
from app.repositories.user_repository import UserRepository
from app.repositories.address_repository import AddressRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.payment_history_repository import PaymentHistoryRepository

from app.services.user_service import UserService
from app.services.address_service import AddressService
from app.services.payment_service import PaymentService
from app.services.payment_history_service import PaymentHistoryService
from app.services.auth_service import AuthService


# --- PROVEDORES DE REPOSITÓRIOS ---
# Funções simples que apenas retornam uma *instância* da classe.
# O FastAPI vai "cachear" isso por requisição.

def get_user_repo() -> UserRepository:
    return UserRepository()

def get_address_repo() -> AddressRepository:
    return AddressRepository()

def get_payment_repo() -> PaymentRepository:
    return PaymentRepository()

def get_history_repo() -> PaymentHistoryRepository:
    return PaymentHistoryRepository()


# --- PROVEDORES DE SERVIÇOS ---
# Aqui a mágica acontece. Note como injetamos as dependências
# chamando as funções "provedoras" de repositório.

def get_user_service() -> UserService:
    # Instancia o UserService e injeta o UserRepository nele
    return UserService(user_repo=get_user_repo())

def get_address_service() -> AddressService:
    return AddressService(address_repo=get_address_repo())

def get_history_service() -> PaymentHistoryService:
    return PaymentHistoryService(
        history_repo=get_history_repo(),
        user_repo=get_user_repo() # HistoryService também precisa do UserRepo
    )

def get_payment_service() -> PaymentService:
    return PaymentService(
        payment_repo=get_payment_repo(),
        history_service=get_history_service() # Injeta outro serviço
    )

def get_auth_service() -> AuthService:
    return AuthService(user_service=get_user_service())