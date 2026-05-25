"""
Testes das três extensões obrigatórias — Sprint 2.
Cada extensão foi implementada em arquivo novo, sem modificar classes existentes (OCP).
"""
import pytest

from src.observers.whatsapp_observer import WhatsAppObserver
from src.strategies.crypto_payment import CriptoStrategy
from src.strategies.discount_strategy import NormalDiscount
from src.strategies.volume_discount import VolumeDiscountStrategy


# ---------------------------------------------------------------------------
# Extensão 1: Pagamento em criptomoeda (CriptoStrategy)
# ---------------------------------------------------------------------------

class TestCriptoStrategy:

    def test_aprova_pagamento(self):
        estrategia = CriptoStrategy()
        assert estrategia.process(100.0) is True

    def test_aprova_pedido_automaticamente(self):
        assert CriptoStrategy().approves_order() is True

    def test_imprime_taxa_2_porcento(self, capsys):
        CriptoStrategy().process(100.0)
        out = capsys.readouterr().out
        assert "2%" in out or "2.00" in out

    def test_total_cobrado_inclui_taxa(self, capsys):
        CriptoStrategy().process(200.0)
        out = capsys.readouterr().out
        # taxa = 4.00, total = 204.00
        assert "204.00" in out


# ---------------------------------------------------------------------------
# Extensão 2: Notificação WhatsApp (WhatsAppObserver)
# ---------------------------------------------------------------------------

class TestWhatsAppObserver:

    def test_envia_para_cliente_normal(self, capsys):
        obs = WhatsAppObserver()
        obs.notify("Joao", "normal", "Pedido recebido!")
        assert "WhatsApp" in capsys.readouterr().out

    def test_envia_para_cliente_vip(self, capsys):
        obs = WhatsAppObserver()
        obs.notify("Maria", "vip", "Pedido recebido!")
        assert "WhatsApp" in capsys.readouterr().out

    def test_envia_para_cliente_corporativo(self, capsys):
        obs = WhatsAppObserver()
        obs.notify("Empresa", "corporativo", "Pedido recebido!")
        assert "WhatsApp" in capsys.readouterr().out

    def test_mensagem_contem_nome_cliente(self, capsys):
        obs = WhatsAppObserver()
        obs.notify("Joao Silva", "normal", "Pedido enviado!")
        assert "Joao Silva" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Extensão 3: Desconto progressivo por volume (VolumeDiscountStrategy)
# ---------------------------------------------------------------------------

class TestVolumeDiscountStrategy:

    def test_sem_desconto_abaixo_do_limite(self):
        estrategia = VolumeDiscountStrategy(NormalDiscount())
        # 2 unidades a 100 = 200, sem desconto adicional
        assert estrategia.apply(100.0, 2) == pytest.approx(200.0)

    def test_desconto_15_porcento_com_3_unidades(self):
        estrategia = VolumeDiscountStrategy(NormalDiscount())
        # 3 unidades a 100 = 300 * 0.85 = 255
        assert estrategia.apply(100.0, 3) == pytest.approx(255.0)

    def test_desconto_15_porcento_com_mais_de_3(self):
        estrategia = VolumeDiscountStrategy(NormalDiscount())
        # 5 unidades a 50 = 250 * 0.85 = 212.50
        assert estrategia.apply(50.0, 5) == pytest.approx(212.50)

    def test_compoe_com_desconto_base(self):
        from src.strategies.discount_strategy import Desc10Discount
        estrategia = VolumeDiscountStrategy(Desc10Discount())
        # 3 unidades a 100 com desc10: 100*3*0.9 = 270 * 0.85 = 229.50
        assert estrategia.apply(100.0, 3) == pytest.approx(229.50)
