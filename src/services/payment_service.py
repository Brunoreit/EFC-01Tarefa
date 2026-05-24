from src.repositories.interfaces import IOrderRepository
from src.strategies.payment_strategy import PAYMENT_STRATEGY_MAP, IPaymentStrategy


class PaymentService:
    """Responsabilidade única: processar pagamentos usando Strategy (OCP)."""

    def __init__(self, repository: IOrderRepository) -> None:
        self._repository = repository

    def process(self, order_id: int, method: str, amount: float) -> bool:
        order = self._repository.find_by_id(order_id)
        if not order:
            return False
        if amount < order.total:
            print("Valor insuficiente!")
            return False

        strategy_class = PAYMENT_STRATEGY_MAP.get(method)
        if not strategy_class:
            print("Metodo de pagamento invalido!")
            return False

        strategy: IPaymentStrategy = strategy_class()
        result = strategy.process(amount)

        if result and strategy.approves_order():
            self._repository.update_status(order_id, "aprovado")

        return result
