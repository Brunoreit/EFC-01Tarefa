from src.strategies.payment_strategy import IPaymentStrategy


class CriptoStrategy(IPaymentStrategy):
    """
    Extensão OCP — pagamento em criptomoeda com taxa de 2%.
    Arquivo novo, zero modificação em classes existentes.
    """

    FEE_RATE = 0.02

    def process(self, valor: float) -> bool:
        fee = valor * self.FEE_RATE
        total = valor + fee
        print("Processando pagamento em criptomoeda...")
        print(f"Taxa de 2%: R${fee:.2f} | Total cobrado: R${total:.2f}")
        print("Transacao blockchain confirmada!")
        return True

    def approves_order(self) -> bool:
        return True
