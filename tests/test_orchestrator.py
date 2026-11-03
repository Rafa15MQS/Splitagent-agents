
import unittest

from agents.orchestrator import SplitAgentOrchestrator


class TestOrchestrator(unittest.TestCase):

    def setUp(self):
        self.agent = SplitAgentOrchestrator()

    def test_valid_transaction(self):
        transaction = {
            "total": "100.00",
            "participants": [
                {"name": "Ana"},
                {"name": "Carlos"}
            ]
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "ok")
        self.assertIn("split_payment", result["results"])
        self.assertIn("guardian", result["results"])

    def test_invalid_transaction(self):
        result = self.agent.process(None)

        self.assertEqual(result["status"], "error")

    def test_missing_total(self):
        transaction = {
            "participants": [
                {"name": "Ana"}
            ]
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "error")

    def test_transaction_with_tax(self):
        transaction = {
            "total": "100.00",
            "participants": [
                {"name": "Ana"},
                {"name": "Carlos"}
            ],
            "tax_context": {
                "transaction_type": "service",
                "tax_profile": "simples"
            }
        }

        result = self.agent.process(transaction)

        self.assertIn("tax", result["results"])

    def test_transaction_with_credit(self):
        transaction = {
            "total": "100.00",
            "participants": [
                {"name": "Ana"}
            ],
            "credit_context": {
                "credit_limit": "1000.00",
                "current_debt": "200.00"
            }
        }

        result = self.agent.process(transaction)

        self.assertIn("credit", result["results"])

    def test_all_agents_together(self):
        transaction = {
            "total": "100.00",
            "participants": [
                {"name": "Ana"},
                {"name": "Carlos"}
            ],
            "tax_context": {
                "transaction_type": "service",
                "tax_profile": "simples"
            },
            "credit_context": {
                "credit_limit": "1000.00",
                "current_debt": "200.00"
            },
            "movements": [
                {
                    "type": "income",
                    "amount": "500.00",
                    "date": "2026-11-01"
                },
                {
                    "type": "expense",
                    "amount": "100.00",
                    "date": "2026-11-02"
                }
            ],
            "forecast_date": "2026-11-02",
            "opening_balance": "0.00"
        }

        result = self.agent.process(transaction)

        self.assertIn("guardian", result["results"])
        self.assertIn("split_payment", result["results"])
        self.assertIn("inclusion", result["results"])
        self.assertIn("tax", result["results"])
        self.assertIn("cash", result["results"])
        self.assertIn("forecast", result["results"])
        self.assertIn("credit", result["results"])

        self.assertEqual(result["status"], "warning")


if __name__ == "__main__":
    unittest.main()
