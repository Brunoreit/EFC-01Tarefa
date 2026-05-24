from src.interfaces.i_notification_service import INotificationService
from src.observers.notification_observer import build_publisher


class ObserverNotificationService(INotificationService):
    """
    Implementação de notificação usando padrão Observer/Pub-Sub.
    Despacha eventos para os observers registrados (OCP).
    """

    def notify_order_created(self, cliente: str, tipo_cliente: str) -> None:
        publisher = build_publisher(tipo_cliente)
        publisher.publish(cliente, tipo_cliente, "Pedido recebido!")

    def notify_status_changed(self, cliente: str, tipo_cliente: str, status: str) -> None:
        publisher = build_publisher(tipo_cliente)
        eventos = {
            "aprovado": "Pedido aprovado!",
            "enviado": "Pedido enviado!",
            "entregue": "Pedido entregue!",
        }
        evento = eventos.get(status)
        if evento:
            publisher.publish(cliente, tipo_cliente, evento)
