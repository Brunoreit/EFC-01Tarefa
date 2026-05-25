"""
Testes unitários — Sprint 1
Validam camadas de serviços, repositório e notificação.
Os Golden Master em tests/golden_master/ continuam testando legacy.py.
"""
import pytest

from src.models.order import Order
from src.models.order_item import OrderItem
from src.repositories.order_repository import OrderRepository
from src.services.notification_service import ObserverNotificationService as PrintNotificationService
from src.services.order_service import OrderService
from src.services.payment_service import PaymentService
from src.services.report_service import ReportService
from src.services.stock_service import StockService


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    r = OrderRepository()
    yield r
    r.close()


@pytest.fixture
def notification():
    return PrintNotificationService()


@pytest.fixture
def order_service(repo, notification):
    return OrderService(repo, notification)


@pytest.fixture
def payment_service(repo):
    return PaymentService(repo)


# ===========================================================================
# Pessoa 2 — Repository
# ===========================================================================

class TestOrderRepository:

    def test_save_e_find(self, repo):
        order = Order(cliente="Joao", itens=[], tipo="normal", total=100.0)
        oid = repo.save(order)
        found = repo.find_by_id(oid)
        assert found is not None
        assert found.cliente == "Joao"
        assert found.total == pytest.approx(100.0)

    def test_find_inexistente_retorna_none(self, repo):
        assert repo.find_by_id(9999) is None

    def test_update_status(self, repo):
        order = Order(cliente="Joao", itens=[], tipo="normal", total=100.0)
        oid = repo.save(order)
        repo.update_status(oid, "aprovado")
        assert repo.find_by_id(oid).status == "aprovado"

    def test_find_by_customer(self, repo):
        for _ in range(3):
            repo.save(Order(cliente="Joao", itens=[], tipo="normal", total=50.0))
        repo.save(Order(cliente="Maria", itens=[], tipo="vip", total=200.0))
        assert len(repo.find_by_customer("Joao")) == 3

    def test_find_all(self, repo):
        repo.save(Order(cliente="A", itens=[], tipo="normal", total=10.0))
        repo.save(Order(cliente="B", itens=[], tipo="vip", total=20.0))
        assert len(repo.find_all()) == 2


# ===========================================================================
# Pessoa 3 — OrderService + StockService
# ===========================================================================

class TestOrderService:

    def _itens(self, tipo="normal"):
        return [{"nome": "p1", "p": 100, "q": 1, "tipo": tipo}]

    def test_pedido_normal(self, order_service):
        oid = order_service.create_order("Joao", self._itens(), "normal")
        assert order_service.get_order(oid).total == pytest.approx(100.0)

    def test_pedido_desc10(self, order_service):
        oid = order_service.create_order("Joao", self._itens("desc10"), "normal")
        assert order_service.get_order(oid).total == pytest.approx(90.0)

    def test_pedido_desc20(self, order_service):
        oid = order_service.create_order("Joao", self._itens("desc20"), "normal")
        assert order_service.get_order(oid).total == pytest.approx(80.0)

    def test_pedido_frete_gratis(self, order_service):
        oid = order_service.create_order("Joao", self._itens("frete_gratis"), "normal")
        assert order_service.get_order(oid).total == pytest.approx(100.0)

    def test_pedido_vip_desconto_5(self, order_service):
        oid = order_service.create_order("Maria", self._itens(), "vip")
        assert order_service.get_order(oid).total == pytest.approx(95.0)

    def test_pedido_corporativo_desconto_10(self, order_service):
        oid = order_service.create_order("Empresa", self._itens(), "corporativo")
        assert order_service.get_order(oid).total == pytest.approx(90.0)

    def test_status_inicial_pendente(self, order_service):
        oid = order_service.create_order("Joao", self._itens(), "normal")
        assert order_service.get_order(oid).status == "pendente"

    def test_cancelar(self, order_service):
        oid = order_service.create_order("Joao", self._itens(), "normal")
        order_service.cancel_order(oid)
        assert order_service.get_order(oid).status == "cancelado"

    def test_update_enviado(self, order_service):
        oid = order_service.create_order("Joao", self._itens(), "normal")
        order_service.update_status(oid, "enviado")
        assert order_service.get_order(oid).status == "enviado"

    def test_entregue_normal_pontos(self, order_service, capsys):
        oid = order_service.create_order("Joao", self._itens(), "normal")
        capsys.readouterr()
        order_service.update_status(oid, "entregue")
        assert "100 pontos" in capsys.readouterr().out

    def test_entregue_vip_pontos(self, order_service, capsys):
        oid = order_service.create_order("Maria", self._itens(), "vip")
        capsys.readouterr()
        order_service.update_status(oid, "entregue")
        assert "190 pontos" in capsys.readouterr().out

    def test_entregue_corporativo_pontos(self, order_service, capsys):
        oid = order_service.create_order("Empresa", self._itens(), "corporativo")
        capsys.readouterr()
        order_service.update_status(oid, "entregue")
        assert "135 pontos" in capsys.readouterr().out

    def test_total_by_customer(self, order_service):
        order_service.create_order("Joao", self._itens(), "normal")
        order_service.create_order("Joao", self._itens(), "normal")
        assert order_service.total_by_customer("Joao") == pytest.approx(200.0)


class TestStockService:

    def test_valido(self):
        assert StockService().validate([{"nome": "produto1", "p": 1, "q": 1, "tipo": "normal"}]) is True

    def test_produto_inexistente(self):
        assert StockService().validate([{"nome": "xyz", "p": 1, "q": 1, "tipo": "normal"}]) is False

    def test_quantidade_excessiva(self):
        assert StockService().validate([{"nome": "produto2", "p": 1, "q": 999, "tipo": "normal"}]) is False

    def test_multiplos_validos(self):
        itens = [
            {"nome": "produto1", "p": 1, "q": 1, "tipo": "normal"},
            {"nome": "produto2", "p": 1, "q": 1, "tipo": "normal"},
        ]
        assert StockService().validate(itens) is True


# ===========================================================================
# Pessoa 4 — PaymentService + NotificationService
# ===========================================================================

class TestPaymentService:

    def _itens(self):
        return [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    def test_cartao_aprova(self, order_service, payment_service):
        oid = order_service.create_order("Joao", self._itens(), "normal")
        assert payment_service.process(oid, "cartao", 100) is True
        assert order_service.get_order(oid).status == "aprovado"

    def test_pix_aprova(self, order_service, payment_service):
        oid = order_service.create_order("Joao", self._itens(), "normal")
        assert payment_service.process(oid, "pix", 100) is True
        assert order_service.get_order(oid).status == "aprovado"

    def test_boleto_nao_aprova(self, order_service, payment_service):
        oid = order_service.create_order("Joao", self._itens(), "normal")
        assert payment_service.process(oid, "boleto", 100) is True
        assert order_service.get_order(oid).status == "pendente"

    def test_valor_insuficiente(self, order_service, payment_service):
        oid = order_service.create_order("Joao", self._itens(), "normal")
        assert payment_service.process(oid, "cartao", 50) is False

    def test_metodo_invalido(self, order_service, payment_service):
        oid = order_service.create_order("Joao", self._itens(), "normal")
        assert payment_service.process(oid, "cheque", 100) is False

    def test_pedido_inexistente(self, payment_service):
        assert payment_service.process(9999, "cartao", 500) is False


class TestNotificationService:

    def test_normal_recebe_email(self, capsys):
        PrintNotificationService().notify_order_created("Joao", "normal")
        out = capsys.readouterr().out
        assert "Email enviado para Joao" in out
        assert "SMS" not in out

    def test_vip_recebe_email_e_sms(self, capsys):
        PrintNotificationService().notify_order_created("Maria", "vip")
        out = capsys.readouterr().out
        assert "Email enviado para Maria" in out
        assert "SMS enviado para Maria" in out

    def test_corporativo_recebe_email_e_gerente(self, capsys):
        PrintNotificationService().notify_order_created("Empresa", "corporativo")
        out = capsys.readouterr().out
        assert "Email enviado para Empresa" in out
        assert "gerente de conta" in out

    def test_status_aprovado_notifica(self, capsys):
        PrintNotificationService().notify_status_changed("Joao", "normal", "aprovado")
        assert "Pedido aprovado" in capsys.readouterr().out

    def test_status_aprovado_vip_sms(self, capsys):
        PrintNotificationService().notify_status_changed("Maria", "vip", "aprovado")
        out = capsys.readouterr().out
        assert "SMS enviado para Maria" in out


# ===========================================================================
# Pessoa 5 — ReportService
# ===========================================================================

class TestReportService:

    def test_vendas_cabecalho(self, repo, capsys):
        repo.save(Order(cliente="Joao", itens=[], tipo="normal", total=100.0))
        ReportService(repo).sales_report()
        assert "RELATORIO DE VENDAS" in capsys.readouterr().out

    def test_vendas_grava_arquivo(self, repo, tmp_path):
        repo.save(Order(cliente="Joao", itens=[], tipo="normal", total=100.0))
        ReportService(repo).sales_report()
        assert (tmp_path / "rel_vendas.txt").exists()

    def test_clientes_cabecalho(self, repo, capsys):
        repo.save(Order(cliente="Joao", itens=[], tipo="normal", total=100.0))
        ReportService(repo).customers_report()
        assert "RELATORIO DE CLIENTES" in capsys.readouterr().out
