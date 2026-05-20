import pytest
from legacy import Sis, PedEspecial

@pytest.fixture
def sis(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    s = Sis()
    yield s
    s.close()


@pytest.fixture
def ped_especial(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    s = PedEspecial()
    yield s
    s.close()

class TestCriacaoPedidosLegado:

    def test_pedido_normal_calcula_total(self, sis):
        itens = [
            {"nome": "produto1", "p": 100, "q": 2, "tipo": "normal"},
            {"nome": "produto2", "p": 50,  "q": 1, "tipo": "desc10"},
        ]
        id_ped = sis.add_ped("Joao Silva", itens, "normal")
        p = sis.get_ped(id_ped)
        assert p["tot"] == pytest.approx(245.0)
        assert p["st"] == "pendente"
        assert p["tp"] == "normal"
        assert p["cli"] == "Joao Silva"

    def test_pedido_normal_desc20(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "desc20"}]
        id_ped = sis.add_ped("Joao", itens, "normal")
        assert sis.get_ped(id_ped)["tot"] == pytest.approx(80.0)

    def test_pedido_normal_frete_gratis(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 2, "tipo": "frete_gratis"}]
        id_ped = sis.add_ped("Joao", itens, "normal")
        assert sis.get_ped(id_ped)["tot"] == pytest.approx(200.0)

    def test_pedido_vip_desconto_5(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Maria VIP", itens, "vip")
        assert sis.get_ped(id_ped)["tot"] == pytest.approx(95.0)

    def test_pedido_vip_desconto_acumulado(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "desc10"}]
        id_ped = sis.add_ped("Maria", itens, "vip")
        assert sis.get_ped(id_ped)["tot"] == pytest.approx(85.5)

    def test_pedido_corporativo_desconto_10(self, sis):
        itens = [{"nome": "p1", "p": 200, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Empresa", itens, "corporativo")
        assert sis.get_ped(id_ped)["tot"] == pytest.approx(180.0)

    def test_pedido_retorna_id_crescente(self, sis):
        itens = [{"nome": "p1", "p": 10, "q": 1, "tipo": "normal"}]
        id1 = sis.add_ped("A", itens, "normal")
        id2 = sis.add_ped("B", itens, "normal")
        assert id2 > id1

    def test_pedido_inexistente_retorna_none(self, sis):
        assert sis.get_ped(9999) is None

    def test_pedido_persiste_itens_como_lista(self, sis):
        itens = [
            {"nome": "p1", "p": 10, "q": 1, "tipo": "normal"},
            {"nome": "p2", "p": 20, "q": 2, "tipo": "desc10"},
        ]
        id_ped = sis.add_ped("Joao", itens, "normal")
        assert isinstance(sis.get_ped(id_ped)["itens"], list)
        assert len(sis.get_ped(id_ped)["itens"]) == 2