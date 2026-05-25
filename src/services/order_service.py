from typing import Any, List, Optional, cast

from src.interfaces.i_notification_service import INotificationService
from src.models.order import CustomerType, Order, OrderStatus
from src.models.order_item import OrderItem
from src.repositories.interfaces import IOrderRepository
from src.strategies.discount_strategy import (
    CUSTOMER_DISCOUNT_REGISTRY,
    ITEM_DISCOUNT_REGISTRY,
    NormalCustomerDiscount,
    NormalDiscount,
)


class OrderService:
    """
    Orquestra criação, atualização e cancelamento de pedidos (SRP).
    Recebe dependências via construtor (DIP).
    """

    def __init__(
        self,
        repository: IOrderRepository,
        notification_service: INotificationService,
    ) -> None:
        self._repository = repository
        self._notification = notification_service

    def create_order(self, cliente: str, itens_raw: List[dict[str, Any]], tipo: str) -> int:
        itens = [OrderItem.from_dict(i) for i in itens_raw]
        total = self._calculate_total(itens, tipo)
        order = Order(cliente=cliente, itens=itens, tipo=cast(CustomerType, tipo), total=total)
        order_id = self._repository.save(order)
        order.id = order_id
        self._notification.notify_order_created(cliente, tipo)
        return order_id

    def get_order(self, order_id: int) -> Optional[Order]:
        return self._repository.find_by_id(order_id)

    def update_status(self, order_id: int, status: str) -> None:
        order = self._repository.find_by_id(order_id)
        if not order:
            return
        self._repository.update_status(order_id, status)
        order.status = cast(OrderStatus, status)
        self._notification.notify_status_changed(order.cliente, order.tipo, status)
        if status == "entregue":
            self._award_points(order)

    def cancel_order(self, order_id: int) -> None:
        self._repository.update_status(order_id, "cancelado")
        print(f"Pedido {order_id} cancelado")

    def total_by_customer(self, cliente: str) -> float:
        orders = self._repository.find_by_customer(cliente)
        return sum(o.total for o in orders)

    # ------------------------------------------------------------------
    # Métodos privados
    # ------------------------------------------------------------------

    def _calculate_total(self, itens: List[OrderItem], tipo: str) -> float:
        total = 0.0
        for item in itens:
            strategy = ITEM_DISCOUNT_REGISTRY.get(item.tipo, NormalDiscount())
            total += strategy.apply(item.preco, item.quantidade)
        customer_strategy = CUSTOMER_DISCOUNT_REGISTRY.get(tipo, NormalCustomerDiscount())
        return customer_strategy.apply(total)

    def _award_points(self, order: Order) -> None:
        if order.tipo == "vip":
            pts = int(order.total * 2)
            print(f"Cliente VIP ganhou {pts} pontos!")
        elif order.tipo == "corporativo":
            pts = int(order.total * 1.5)
            print(f"Cliente corporativo ganhou {pts} pontos!")
        else:
            pts = int(order.total)
            print(f"Cliente ganhou {pts} pontos!")
