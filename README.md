# EFC 1 — Refatoração Guiada por SOLID, Clean Code e Padrões GoF

**Grupo 02**

Integrantes:
BRUNO REITANO FIGUEROLA 
GABRIEL FLORES BONATTO 
HENRY GABRIEL PIOZZI 
PEDRO XIMENES COSTA 
ROGÉRIO MEDINA 

Refatoração de um sistema legado de gestão de pedidos (`legacy.py`), aplicando princípios SOLID, Clean Code e padrões de projeto GoF. O código original foi mantido intacto como referência; toda a lógica refatorada está em `src/`.

---

## O que o sistema faz

Gerencia pedidos de uma loja com suporte a:

- Três tipos de cliente: normal, VIP e corporativo
- Descontos por item (10%, 20%, frete grátis, volume) e por tipo de cliente
- Pagamentos via cartão, PIX, boleto e criptomoeda
- Notificações de status por e-mail, SMS, gerente de conta e WhatsApp
- Relatórios de vendas e clientes

---

## Estrutura

```
legacy.py                   # Código original — não modificado
src/
  models/                   # Order, OrderItem, Customer
  repositories/             # IOrderRepository + implementação em memória
  services/                 # OrderService, PaymentService, ReportService, StockService
  strategies/               # Descontos e pagamentos (Strategy)
  observers/                # Notificações (Observer/Pub-Sub)
  factories/                # Criação de pedidos por tipo (Factory Method)
  interfaces/               # Interfaces de notificação e pagamento
tests/
  golden_master/            # Testes de caracterização do legado
  test_extensoes.py         # Testes das extensões OCP
docs/
  diagrama.puml             # Diagrama UML de classes (PlantUML)
  analise_sprint0.docx      # Análise inicial das violações SOLID
  grupo02_pas_efc1.pdf      # Documento final
```

---

## Como rodar

```bash
# Instalar dependências de desenvolvimento
pip install pytest pytest-cov mypy ruff radon

# Rodar a aplicação
py src/main.py
```

---

## Testes

```bash
# Rodar todos os testes
py -m pytest

# Com relatório de cobertura
py -m pytest --cov=src --cov-report=term-missing
```

**Resultado esperado:** 84/84 testes passando, 90%+ de cobertura.

---

## Qualidade de código

```bash
# Lint
ruff check src/ tests/

# Tipagem estática
mypy src/ --strict

# Complexidade ciclomática
radon cc src/ -a
```

**Metas:** 0 erros ruff, 0 erros mypy, complexidade média A (≤ 2.0).

---

## Padrões GoF aplicados

| Padrão | Onde |
|---|---|
| Repository | `src/repositories/` |
| Strategy | `src/strategies/` |
| Observer / Pub-Sub | `src/observers/` |
| Factory Method | `src/factories/` |

### Extensões OCP (arquivos novos)

- `src/strategies/crypto_payment.py` — pagamento via criptomoeda
- `src/observers/whatsapp_observer.py` — notificação via WhatsApp
- `src/strategies/volume_discount.py` — desconto por volume de itens

---

## Princípios SOLID

- **SRP** — cada serviço tem uma única responsabilidade
- **OCP** — novas estratégias e observers sem modificar código existente
- **LSP** — violação documentada em `legacy.py` (`PedEspecial`), preservada intencionalmente
- **ISP** — repositório expõe apenas operações de CRUD; relatórios ficam no `ReportService`
- **DIP** — todos os serviços recebem dependências via construtor, programando para interfaces

---

## Tags Git

| Tag | Conteúdo |
|---|---|
| `sprint-0` | Golden Master Tests |
| `sprint-1` | Refatoração SOLID + padrões GoF |
| `sprint-2` | Extensões OCP |
