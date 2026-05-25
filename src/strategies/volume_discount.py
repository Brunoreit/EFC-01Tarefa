from src.strategies.discount_strategy import IDiscountStrategy


class VolumeDiscountStrategy(IDiscountStrategy):
    """
    Extensão OCP — desconto progressivo por volume.
    3 ou mais unidades do mesmo item recebem 15% adicional.
    Arquivo novo, zero modificação em classes existentes.
    Usa padrão Decorator: envolve qualquer IDiscountStrategy base.
    """

    THRESHOLD = 3
    ADDITIONAL_DISCOUNT = 0.85  # 15% de desconto adicional

    def __init__(self, base_strategy: IDiscountStrategy) -> None:
        self._base = base_strategy

    def apply(self, preco: float, quantidade: int) -> float:
        base_value = self._base.apply(preco, quantidade)
        if quantidade >= self.THRESHOLD:
            return base_value * self.ADDITIONAL_DISCOUNT
        return base_value
