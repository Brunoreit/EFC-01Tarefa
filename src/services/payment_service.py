from src.interfaces.i_payment_processor import IPaymentProcessor
from src.repositories.interfaces import IOrderRepository


class CreditCardProcessor(IPaymentProcessor):
    def process(self, amount: float) -> bool:
        print("Processando pagamento com cartao...")
        print("Cartao validado!")
        return True

    def approves_order(self) -> bool:
        return True


class PixProcessor(IPaymentProcessor):
    def process(self, amount: float) -> bool:
        print("Gerando QR Code PIX...")
        print("PIX recebido!")
        return True

    def approves_order(self) -> bool:
        return True


class BoletoProcessor(IPaymentProcessor):
    def process(self, amount: float) -> bool:
        print("Gerando boleto...")
        print("Boleto gerado!")
        return True

    def approves_order(self) -> bool:
        return False


PAYMENT_PROCESSORS: dict = {
    "cartao": CreditCardProcessor,
    "pix": PixProcessor,
    "boleto": BoletoProcessor,
}


class PaymentService:
    """Responsabilidade única: processar pagamentos (SRP)."""

    def __init__(self, repository: IOrderRepository) -> None:
        self._repository = repository

    def process(self, order_id: int, method: str, amount: float) -> bool:
        order = self._repository.find_by_id(order_id)
        if not order:
            return False
        if amount < order.total:
            print("Valor insuficiente!")
            return False

        processor_class = PAYMENT_PROCESSORS.get(method)
        if not processor_class:
            print("Metodo de pagamento invalido!")
            return False

        processor: IPaymentProcessor = processor_class()
        result = processor.process(amount)

        if result and processor.approves_order():
            self._repository.update_status(order_id, "aprovado")

        return result
