from abc import ABC, abstractmethod


class IPaymentStrategy(ABC):
    """Interface Strategy para métodos de pagamento."""

    @abstractmethod
    def process(self, valor: float) -> bool:
        """Processa o pagamento. Retorna True se bem-sucedido."""
        ...

    @abstractmethod
    def approves_order(self) -> bool:
        """Retorna True se este método aprova o pedido automaticamente."""
        ...


class CartaoStrategy(IPaymentStrategy):
    def process(self, valor: float) -> bool:
        print("Processando pagamento com cartao...")
        print("Cartao validado!")
        return True

    def approves_order(self) -> bool:
        return True


class PixStrategy(IPaymentStrategy):
    def process(self, valor: float) -> bool:
        print("Gerando QR Code PIX...")
        print("PIX recebido!")
        return True

    def approves_order(self) -> bool:
        return True


class BoletoStrategy(IPaymentStrategy):
    def process(self, valor: float) -> bool:
        print("Gerando boleto...")
        print("Boleto gerado!")
        return True

    def approves_order(self) -> bool:
        return False


PAYMENT_STRATEGY_MAP: dict = {
    "cartao": CartaoStrategy,
    "pix": PixStrategy,
    "boleto": BoletoStrategy,
}
