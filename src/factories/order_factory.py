from abc import ABC, abstractmethod
from typing import List, Type

from src.models.order import CustomerType, Order
from src.models.order_item import OrderItem
from src.strategies.discount_strategy import (
    CUSTOMER_DISCOUNT_REGISTRY,
    ITEM_DISCOUNT_REGISTRY,
    NormalCustomerDiscount,
    NormalDiscount,
)


class IOrderFactory(ABC):
    """Factory Method: define o esqueleto de criação de pedidos."""

    @abstractmethod
    def customer_type(self) -> CustomerType:
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
            strategy = ITEM_DISCOUNT_REGISTRY.get(item.tipo, NormalDiscount())
            total += strategy.apply(item.preco, item.quantidade)
        customer_strategy = CUSTOMER_DISCOUNT_REGISTRY.get(
            self.customer_type(), NormalCustomerDiscount()
        )
        return customer_strategy.apply(total)


class NormalOrderFactory(IOrderFactory):
    def customer_type(self) -> CustomerType:
        return "normal"


class VipOrderFactory(IOrderFactory):
    def customer_type(self) -> CustomerType:
        return "vip"


class CorporativoOrderFactory(IOrderFactory):
    def customer_type(self) -> CustomerType:
        return "corporativo"


ORDER_FACTORY_MAP: dict[str, Type[IOrderFactory]] = {
    "normal": NormalOrderFactory,
    "vip": VipOrderFactory,
    "corporativo": CorporativoOrderFactory,
}


def get_order_factory(tipo: str) -> IOrderFactory:
    factory_class = ORDER_FACTORY_MAP.get(tipo)
    if factory_class is None:
        raise ValueError(f"Tipo de cliente desconhecido: {tipo}")
    return factory_class()
