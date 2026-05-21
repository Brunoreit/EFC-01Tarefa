from abc import ABC, abstractmethod


class INotificationService(ABC):
    """Interface abstrata para serviços de notificação (ISP + DIP)."""

    @abstractmethod
    def notify_order_created(self, cliente: str, tipo_cliente: str) -> None:
        ...

    @abstractmethod
    def notify_status_changed(self, cliente: str, tipo_cliente: str, status: str) -> None:
        ...
