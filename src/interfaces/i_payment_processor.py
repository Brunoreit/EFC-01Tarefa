from abc import ABC, abstractmethod


class IPaymentProcessor(ABC):
    """Interface abstrata para processadores de pagamento (ISP + DIP)."""

    @abstractmethod
    def process(self, amount: float) -> bool:
        """Processa o pagamento e retorna True se aprovado."""
        ...

    @abstractmethod
    def approves_order(self) -> bool:
        """Retorna True se este método aprova o pedido automaticamente."""
        ...
