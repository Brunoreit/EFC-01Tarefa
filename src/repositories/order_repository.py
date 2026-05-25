import json
import sqlite3
from typing import Any, List, Optional

from src.models.order import Order
from src.models.order_item import OrderItem
from src.repositories.interfaces import IOrderRepository


class OrderRepository(IOrderRepository):
    """Padrão Repository: isola todo acesso ao SQLite."""

    def __init__(self, db_path: str = "loja.db") -> None:
        self._db = sqlite3.connect(db_path)
        self._cursor = self._db.cursor()
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS ped (
                id    INTEGER PRIMARY KEY,
                cli   TEXT,
                itens TEXT,
                tot   REAL,
                st    TEXT,
                dt    TEXT,
                tp    TEXT
            )"""
        )
        self._db.commit()

    def save(self, order: Order) -> int:
        itens_json = json.dumps([i.to_dict() for i in order.itens])
        self._cursor.execute(
            "INSERT INTO ped (cli, itens, tot, st, dt, tp) VALUES (?, ?, ?, ?, ?, ?)",
            (order.cliente, itens_json, order.total, order.status, order.data, order.tipo),
        )
        self._db.commit()
        return self._cursor.lastrowid  # type: ignore[return-value]

    def find_by_id(self, order_id: int) -> Optional[Order]:
        self._cursor.execute("SELECT * FROM ped WHERE id=?", (order_id,))
        row = self._cursor.fetchone()
        return self._row_to_order(row) if row else None

    def find_by_customer(self, cliente: str) -> List[Order]:
        self._cursor.execute("SELECT * FROM ped WHERE cli=?", (cliente,))
        return [self._row_to_order(r) for r in self._cursor.fetchall()]

    def find_all(self) -> List[Order]:
        self._cursor.execute("SELECT * FROM ped")
        return [self._row_to_order(r) for r in self._cursor.fetchall()]

    def update_status(self, order_id: int, status: str) -> None:
        self._cursor.execute("UPDATE ped SET st=? WHERE id=?", (status, order_id))
        self._db.commit()

    def close(self) -> None:
        self._db.close()

    @staticmethod
    def _row_to_order(row: Any) -> Order:
        itens = [OrderItem.from_dict(i) for i in json.loads(row[2])]
        return Order(
            id=row[0],
            cliente=row[1],
            itens=itens,
            total=row[3],
            status=row[4],
            data=row[5],
            tipo=row[6],
        )
