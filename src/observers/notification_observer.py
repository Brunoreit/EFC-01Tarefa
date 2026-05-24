from abc import ABC, abstractmethod
from typing import List


class INotificationObserver(ABC):
    """Interface Observer para canais de notificação."""

    @abstractmethod
    def notify(self, cliente: str, tipo_cliente: str, evento: str) -> None:
        ...


class EmailObserver(INotificationObserver):
    def notify(self, cliente: str, tipo_cliente: str, evento: str) -> None:
        print(f"Email enviado para {cliente}: {evento}")


class SmsObserver(INotificationObserver):
    """Notifica apenas clientes VIP."""
    def notify(self, cliente: str, tipo_cliente: str, evento: str) -> None:
        if tipo_cliente == "vip":
            print(f"SMS enviado para {cliente}: {evento}")


class GerenteObserver(INotificationObserver):
    """Notifica gerente de conta apenas para clientes corporativos."""
    def notify(self, cliente: str, tipo_cliente: str, evento: str) -> None:
        if tipo_cliente == "corporativo":
            print(f"Notificacao enviada ao gerente de conta de {cliente}")


class NotificationPublisher:
    """Pub/Sub: mantém lista de observers e despacha eventos."""

    def __init__(self) -> None:
        self._observers: List[INotificationObserver] = []

    def subscribe(self, observer: INotificationObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: INotificationObserver) -> None:
        self._observers.remove(observer)

    def publish(self, cliente: str, tipo_cliente: str, evento: str) -> None:
        for observer in self._observers:
            observer.notify(cliente, tipo_cliente, evento)


def build_publisher(tipo_cliente: str) -> NotificationPublisher:
    """Factory de publishers: monta os observers corretos por tipo de cliente."""
    publisher = NotificationPublisher()
    publisher.subscribe(EmailObserver())
    publisher.subscribe(SmsObserver())
    publisher.subscribe(GerenteObserver())
    return publisher
