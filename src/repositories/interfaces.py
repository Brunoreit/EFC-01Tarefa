from abc import ABC, abstractmethod
from typing import List, Optional

from src.models.order import Order


class IOrderRepository(ABC):
    """Interface abstrata para persistência de pedidos (ISP + DIP)."""

    @abstractmethod
    def save(self, order: Order) -> int:
        ...

    @abstractmethod
    def find_by_id(self, order_id: int) -> Optional[Order]:
        ...

    @abstractmethod
    def find_by_customer(self, cliente: str) -> List[Order]:
        ...

    @abstractmethod
    def find_all(self) -> List[Order]:
        ...

    @abstractmethod
    def update_status(self, order_id: int, status: str) -> None:
        ...
