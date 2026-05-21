from dataclasses import dataclass
from typing import Literal

ItemType = Literal["normal", "desc10", "desc20", "frete_gratis"]


@dataclass
class OrderItem:
    nome: str
    preco: float
    quantidade: int
    tipo: ItemType

    @classmethod
    def from_dict(cls, d: dict) -> "OrderItem":
        return cls(
            nome=d["nome"],
            preco=d["p"],
            quantidade=d["q"],
            tipo=d["tipo"],
        )

    def to_dict(self) -> dict:
        return {
            "nome": self.nome,
            "p": self.preco,
            "q": self.quantidade,
            "tipo": self.tipo,
        }
