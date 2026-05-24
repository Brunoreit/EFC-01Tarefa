from abc import ABC, abstractmethod


class IItemDiscountStrategy(ABC):
    @abstractmethod
    def apply(self, preco: float, quantidade: int) -> float: ...


class ICustomerDiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float: ...


class NormalDiscount(IItemDiscountStrategy):
    def apply(self, preco: float, quantidade: int) -> float:
        return preco * quantidade


class Desc10Discount(IItemDiscountStrategy):
    def apply(self, preco: float, quantidade: int) -> float:
        return preco * quantidade * 0.9


class Desc20Discount(IItemDiscountStrategy):
    def apply(self, preco: float, quantidade: int) -> float:
        return preco * quantidade * 0.8


class FreteGratisDiscount(IItemDiscountStrategy):
    def apply(self, preco: float, quantidade: int) -> float:
        return preco * quantidade


class NormalCustomerDiscount(ICustomerDiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class VipDiscount(ICustomerDiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.95


class CorporativoDiscount(ICustomerDiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.90


ITEM_DISCOUNT_REGISTRY: dict[str, IItemDiscountStrategy] = {
    "normal": NormalDiscount(),
    "desc10": Desc10Discount(),
    "desc20": Desc20Discount(),
    "frete_gratis": FreteGratisDiscount(),
}

CUSTOMER_DISCOUNT_REGISTRY: dict[str, ICustomerDiscountStrategy] = {
    "normal": NormalCustomerDiscount(),
    "vip": VipDiscount(),
    "corporativo": CorporativoDiscount(),
}
