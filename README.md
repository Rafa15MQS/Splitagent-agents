# SplitAgent — Módulos de Agentes

## Sobre o projeto

O SplitAgent é um projeto acadêmico desenvolvido no contexto da parceria Fatec e IBM SkillsBuild. Seu objetivo é analisar transações e apoiar a divisão de pagamentos por meio de módulos de agentes em Python.

Este repositório contém os módulos de agentes e seus testes automatizados. A integração com o frontend e o backend será realizada pelo restante da equipe.

## Estrutura do projeto

- `agents/`: contém os módulos dos agentes.
- `core/`: contém a lógica de cálculo da divisão.
- `tests/`: contém os testes automatizados.

## Agentes implementados

| Módulo | Responsabilidade |
|---|---|
| SplitPaymentAgent | Processa a divisão de pagamentos. |
| GuardianAgent | Valida os dados das transações. |
| TaxAgent | Realiza estimativas demonstrativas de tributos. |
| CashAgent | Calcula entradas, saídas e saldo financeiro. |
| ForecastAgent | Projeta o saldo com base nas movimentações informadas. |
| CreditAgent | Analisa o limite de crédito disponível. |
| InclusionAgent | Verifica valores atribuídos aos participantes. |
| SplitAgentOrchestrator | Coordena a execução dos agentes. |

## Requisitos

- Python 3 instalado.

## Como executar os testes

Abra o terminal na pasta principal do projeto e execute:

```bash
python -m unittest discover -s tests -v
```

Os testes verificam o funcionamento dos módulos individualmente e a coordenação entre os agentes.

## Observação

As estimativas tributárias são simulações acadêmicas e não substituem consultoria fiscal ou cálculo oficial de tributos.

As análises financeiras são baseadas nas regras implementadas nos módulos e nos dados fornecidos.

## Tecnologias

- Python
- Programação orientada a objetos
- Testes automatizados com unittest