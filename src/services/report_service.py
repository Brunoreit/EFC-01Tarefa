from src.repositories.interfaces import IOrderRepository


class ReportService:
    """Responsabilidade única: geração de relatórios (SRP)."""

    def __init__(self, repository: IOrderRepository) -> None:
        self._repository = repository

    def sales_report(self) -> None:
        orders = self._repository.find_all()
        print("=== RELATORIO DE VENDAS ===")
        grand_total = 0.0
        for order in orders:
            print(
                f"Pedido #{order.id} - Cliente: {order.cliente} - "
                f"Total: R${order.total:.2f} - Status: {order.status}"
            )
            grand_total += order.total
        print(f"Total Geral: R${grand_total:.2f}")
        with open("rel_vendas.txt", "w") as f:
            f.write(f"Total de vendas: {grand_total}")

    def customers_report(self) -> None:
        orders = self._repository.find_all()
        seen: dict[str, str] = {}
        for order in orders:
            if order.cliente not in seen:
                seen[order.cliente] = order.tipo

        print("=== RELATORIO DE CLIENTES ===")
        with open("rel_clientes.txt", "w") as f:
            for cliente, tipo in seen.items():
                customer_orders = self._repository.find_by_customer(cliente)
                total = sum(o.total for o in customer_orders)
                print(f"Cliente: {cliente} ({tipo}) - Total gasto: R${total:.2f}")
                f.write(f"{cliente},{tipo}\n")
