# app/patterns/observer.py

from abc import ABC, abstractmethod
from app.models.models import Payment

# 1. Interface do Observer
class PaymentObserver(ABC):
    @abstractmethod
    def update(self, payment: Payment, message: str):
        pass

# 2. Implementação Concreta (Simulando Envio de Email/Notificação)
class MemberNotificationObserver(PaymentObserver):
    def update(self, payment: Payment, message: str):
        # Aqui entraria a lógica real de enviar email/whatsapp
        # Simulação:
        print(f"--- [OBSERVER] Notificando Membro (ID {payment.user_id}) ---")
        print(f"Assunto: Atualização no Pagamento #{payment.id}")
        print(f"Status Novo: {payment.status}")
        print(f"Mensagem: {message}")
        print("-----------------------------------------------------------")

# 3. Subject (Gerenciador de Assinaturas)
class PaymentSubject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: PaymentObserver):
        self._observers.append(observer)

    def notify(self, payment: Payment, message: str):
        for observer in self._observers:
            observer.update(payment, message)