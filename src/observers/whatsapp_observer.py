from src.observers.notification_observer import INotificationObserver


class WhatsAppObserver(INotificationObserver):
    """
    Extensão OCP — canal WhatsApp para todos os tipos de cliente.
    Arquivo novo, zero modificação em classes existentes.
    """

    def notify(self, cliente: str, tipo_cliente: str, evento: str) -> None:
        print(f"WhatsApp enviado para {cliente}: {evento}")
