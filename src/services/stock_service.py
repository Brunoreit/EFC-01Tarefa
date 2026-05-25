from typing import Any, List


class StockService:
    """Responsabilidade única: validação de estoque (SRP)."""

    # TODO: integrar com sistema de estoque externo
    _stock: dict[str, int] = {
        "produto1": 100,
        "produto2": 50,
        "produto3": 75,
    }

    def validate(self, itens_raw: List[dict[str, Any]]) -> bool:
        for item in itens_raw:
            if item["nome"] not in self._stock:
                print(f"Produto {item['nome']} nao encontrado!")
                return False
            if self._stock[item["nome"]] < item["q"]:
                print(f"Estoque insuficiente para {item['nome']}!")
                return False
        return True
