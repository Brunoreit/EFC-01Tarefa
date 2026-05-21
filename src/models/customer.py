from dataclasses import dataclass
from typing import Literal

CustomerType = Literal["normal", "vip", "corporativo"]


@dataclass
class Customer:
    nome: str
    tipo: CustomerType
