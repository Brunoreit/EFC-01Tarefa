from src.interfaces.i_notification_service import INotificationService


class PrintNotificationService(INotificationService):
    """
    Implementação concreta de notificação via print.
    No Sprint 2 será substituída pelo padrão Observer.
    """

    def notify_order_created(self, cliente: str, tipo_cliente: str) -> None:
        print(f"Email enviado para {cliente}: Pedido recebido!")
        if tipo_cliente == "vip":
            print(f"SMS enviado para {cliente}: Pedido VIP recebido!")
        elif tipo_cliente == "corporativo":
            print(f"Notificacao enviada ao gerente de conta de {cliente}")

    def notify_status_changed(self, cliente: str, tipo_cliente: str, status: str) -> None:
        if status == "aprovado":
            print(f"Email enviado para {cliente}: Pedido aprovado!")
            if tipo_cliente == "vip":
                print(f"SMS enviado para {cliente}: Pedido aprovado!")
        elif status == "enviado":
            print(f"Email enviado para {cliente}: Pedido enviado!")
        elif status == "entregue":
            print(f"Email enviado para {cliente}: Pedido entregue!")
