from src.repositories.order_repository import OrderRepository
from src.services.notification_service import PrintNotificationService
from src.services.order_service import OrderService
from src.services.payment_service import PaymentService
from src.services.report_service import ReportService
from src.services.stock_service import StockService


def main() -> None:
    # Injeção de dependência explícita (DIP)
    repo = OrderRepository()
    notification = PrintNotificationService()
    order_service = OrderService(repo, notification)
    payment_service = PaymentService(repo)
    report_service = ReportService(repo)
    stock_service = StockService()

    its1 = [
        {"nome": "produto1", "p": 100, "q": 2, "tipo": "normal"},
        {"nome": "produto2", "p": 50,  "q": 1, "tipo": "desc10"},
    ]
    if stock_service.validate(its1):
        id1 = order_service.create_order("Joao Silva", its1, "normal")
        print(f"Pedido {id1} criado!")
        payment_service.process(id1, "cartao", 250)
        order_service.update_status(id1, "enviado")
        order_service.update_status(id1, "entregue")

    its2 = [{"nome": "produto3", "p": 200, "q": 1, "tipo": "desc20"}]
    if stock_service.validate(its2):
        id2 = order_service.create_order("Maria Santos", its2, "vip")
        payment_service.process(id2, "pix", 160)

    its3 = [{"nome": "produto1", "p": 100, "q": 5, "tipo": "normal"}]
    if stock_service.validate(its3):
        id3 = order_service.create_order("Empresa XYZ", its3, "corporativo")
        payment_service.process(id3, "boleto", 500)

    report_service.sales_report()
    print()
    report_service.customers_report()


if __name__ == "__main__":
    main()
