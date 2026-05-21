from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Literal, Optional

from src.models.order_item import OrderItem

CustomerType = Literal["normal", "vip", "corporativo"]
OrderStatus = Literal["pendente", "aprovado", "enviado", "entregue", "cancelado"]


@dataclass
class Order:
    cliente: str
    itens: List[OrderItem]
    tipo: CustomerType
    total: float
    status: OrderStatus = "pendente"
    data: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    id: Optional[int] = None
