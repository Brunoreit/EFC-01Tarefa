from abc import ABC, abstractmethod
from typing import List

from src.models.order import Order
from src.models.order_item import OrderItem
from src.strategies.discount_strategy import CUSTOMER_DISCOUNT_MAP, ITEM_DISCOUNT_MAP


class IOrderFactory(ABC):
    """Factory Method: define o esqueleto de criação de pedidos."""

    @abstractmethod
    def customer_type(self) -> str:
        ...

    def create(self, cliente: str, itens: List[OrderItem]) -> Order:
        total = self._calculate_total(itens)
        return Order(
            cliente=cliente,
            itens=itens,
            tipo=self.customer_type(),
            total=total,
        )

    def _calculate_total(self, itens: List[OrderItem]) -> float:
        total = 0.0
        for item in itens:
            strategy_class = ITEM_DISCOUNT_MAP.get(item.tipo, ITEM_DISCOUNT_MAP["normal"])
            total += strategy_class().apply(item.preco, item.quantidade)
        multiplier = CUSTOMER_DISCOUNT_MAP.get(self.customer_type(), 1.0)
        return total * multiplier


class NormalOrderFactory(IOrderFactory):
    def customer_type(self) -> str:
        return "normal"


class VipOrderFactory(IOrderFactory):
    def customer_type(self) -> str:
        return "vip"


class CorporativoOrderFactory(IOrderFactory):
    def customer_type(self) -> str:
        return "corporativo"


ORDER_FACTORY_MAP: dict = {
    "normal": NormalOrderFactory,
    "vip": VipOrderFactory,
    "corporativo": CorporativoOrderFactory,
}


def get_order_factory(tipo: str) -> IOrderFactory:
    factory_class = ORDER_FACTORY_MAP.get(tipo)
    if factory_class is None:
        raise ValueError(f"Tipo de cliente desconhecido: {tipo}")
    return factory_class()
