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

# Criação de pedidos
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
    
#Pagamentos
class TestPagamentoLegado:

    def test_cartao_aprova(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Joao", itens, "normal")
        assert sis.proc_pag(id_ped, "cartao", 100) is True
        assert sis.get_ped(id_ped)["st"] == "aprovado"

    def test_pix_aprova(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Joao", itens, "normal")
        assert sis.proc_pag(id_ped, "pix", 100) is True
        assert sis.get_ped(id_ped)["st"] == "aprovado"

    def test_boleto_nao_aprova(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Joao", itens, "normal")
        assert sis.proc_pag(id_ped, "boleto", 100) is True
        assert sis.get_ped(id_ped)["st"] == "pendente"

    def test_valor_insuficiente(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Joao", itens, "normal")
        assert sis.proc_pag(id_ped, "cartao", 50) is False

    def test_metodo_invalido(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Joao", itens, "normal")
        assert sis.proc_pag(id_ped, "cheque", 100) is False

    def test_pedido_inexistente(self, sis):
        assert sis.proc_pag(9999, "cartao", 500) is False

    def test_valor_exato_aceito(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Joao", itens, "normal")
        assert sis.proc_pag(id_ped, "cartao", 100.0) is True

# Status
class TestStatusLegado:

    def test_aprovado(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Joao", itens, "normal")
        sis.upd_st(id_ped, "aprovado")
        assert sis.get_ped(id_ped)["st"] == "aprovado"

    def test_enviado(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Joao", itens, "normal")
        sis.upd_st(id_ped, "enviado")
        assert sis.get_ped(id_ped)["st"] == "enviado"

    def test_entregue_normal_pontos(self, sis, capsys):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Joao", itens, "normal")
        sis.upd_st(id_ped, "entregue")
        assert "100 pontos" in capsys.readouterr().out

    def test_entregue_vip_pontos(self, sis, capsys):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Maria", itens, "vip")
        sis.upd_st(id_ped, "entregue")
        assert "190 pontos" in capsys.readouterr().out

    def test_entregue_corporativo_pontos(self, sis, capsys):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Empresa", itens, "corporativo")
        sis.upd_st(id_ped, "entregue")
        assert "135 pontos" in capsys.readouterr().out

    def test_pedido_inexistente_sem_excecao(self, sis):
        sis.upd_st(9999, "aprovado")

#Cancelamento
class TestCancelamentoLegado:

    def test_cancelar(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Joao", itens, "normal")
        sis.cancelar_pedido(id_ped)
        assert sis.get_ped(id_ped)["st"] == "cancelado"

    def test_cancelar_aprovado(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        id_ped = sis.add_ped("Joao", itens, "normal")
        sis.proc_pag(id_ped, "cartao", 100)
        sis.cancelar_pedido(id_ped)
        assert sis.get_ped(id_ped)["st"] == "cancelado"

#Relatorio
class TestRelatoriosLegado:

    def test_vendas_cabecalho(self, sis, capsys):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        sis.add_ped("Joao", itens, "normal")
        sis.gerar_rel("vendas")
        assert "RELATORIO DE VENDAS" in capsys.readouterr().out

    def test_vendas_arquivo(self, sis, tmp_path):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        sis.add_ped("Joao", itens, "normal")
        sis.gerar_rel("vendas")
        assert (tmp_path / "rel_vendas.txt").exists()
        assert "Total de vendas" in (tmp_path / "rel_vendas.txt").read_text()

    def test_clientes_cabecalho(self, sis, capsys):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        sis.add_ped("Joao", itens, "normal")
        sis.gerar_rel("clientes")
        assert "RELATORIO DE CLIENTES" in capsys.readouterr().out

    def test_clientes_arquivo(self, sis, tmp_path):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        sis.add_ped("Joao", itens, "normal")
        sis.gerar_rel("clientes")
        assert (tmp_path / "rel_clientes.txt").exists()

    def test_calc_tot_cli(self, sis):
        itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]
        sis.add_ped("Joao", itens, "normal")
        sis.add_ped("Joao", itens, "normal")
        assert sis.calc_tot_cli("Joao") == pytest.approx(200.0)

    def test_calc_tot_cli_inexistente(self, sis):
        assert sis.calc_tot_cli("Ninguem") == pytest.approx(0.0)
