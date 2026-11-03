
from agents.split_payment import SplitPaymentAgent
from agents.guardian import GuardianAgent
from agents.tax import TaxAgent
from agents.cash import CashAgent
from agents.forecast import ForecastAgent
from agents.credit import CreditAgent
from agents.inclusion import InclusionAgent


class SplitAgentOrchestrator:

    def __init__(self):
        self.split_agent = SplitPaymentAgent()
        self.guardian_agent = GuardianAgent()
        self.tax_agent = TaxAgent()
        self.cash_agent = CashAgent()
        self.forecast_agent = ForecastAgent()
        self.credit_agent = CreditAgent()
        self.inclusion_agent = InclusionAgent()

    def process(self, transaction):

        if not isinstance(transaction, dict):
            return {
                "status": "error",
                "message": "Dados da transação inválidos."
            }

        results = {}

        # 1. Validação da transação
        results["guardian"] = self.guardian_agent.process(transaction)

        if results["guardian"]["status"] == "error":
            return {
                "status": "error",
                "message": "A transação não passou pela validação.",
                "results": results
            }

        # 2. Divisão do pagamento
        results["split_payment"] = self.split_agent.process(transaction)

        # 3. Inclusão dos participantes
        if results["split_payment"]["status"] == "ok":
            inclusion_data = {
                "participants": results["split_payment"]["shares"]
            }
            results["inclusion"] = self.inclusion_agent.process(inclusion_data)

        # 4. Estimativa de tributos
        if "tax_context" in transaction:
            results["tax"] = self.tax_agent.process(transaction)

        # 5. Controle financeiro
        if "movements" in transaction:
            results["cash"] = self.cash_agent.process(
                transaction["movements"]
            )

        # 6. Projeção financeira
        if "forecast_date" in transaction:
            results["forecast"] = self.forecast_agent.process(
                transaction.get("movements", []),
                transaction["forecast_date"],
                transaction.get("opening_balance", "0.00")
            )

        # 7. Análise de crédito
        if "credit_context" in transaction:
            results["credit"] = self.credit_agent.process(transaction)

        statuses = [
            result["status"]
            for result in results.values()
        ]

        if "error" in statuses:
            overall_status = "error"
        elif "warning" in statuses:
            overall_status = "warning"
        else:
            overall_status = "ok"

        return {
            "status": overall_status,
            "message": "Análise da transação concluída.",
            "results": results
        }
