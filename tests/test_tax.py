
import unittest

from agents.tax import TaxAgent


class TestTaxAgent(unittest.TestCase):

    def setUp(self):
        self.agent = TaxAgent()

    def test_service_tax(self):
        transaction = {
            "total": "1000.00",
            "tax_context": {
                "transaction_type": "service",
                "tax_profile": "simples"
            }
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "warning")
        self.assertEqual(result["total_taxes"], "50.00")
        self.assertEqual(result["net_total"], "950.00")

    def test_product_tax(self):
        transaction = {
            "total": "1000.00",
            "tax_context": {
                "transaction_type": "product",
                "tax_profile": "presumido"
            }
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["total_taxes"], "80.00")
        self.assertEqual(result["net_total"], "920.00")

    def test_transfer_without_taxes(self):
        transaction = {
            "total": "1000.00",
            "tax_context": {
                "transaction_type": "transfer",
                "tax_profile": "real"
            }
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["total_taxes"], "0.00")
        self.assertEqual(result["net_total"], "1000.00")

    def test_missing_tax_context(self):
        result = self.agent.process({"total": "1000.00"})

        self.assertEqual(result["status"], "warning")

    def test_invalid_transaction_type(self):
        transaction = {
            "total": "1000.00",
            "tax_context": {
                "transaction_type": "invalid",
                "tax_profile": "simples"
            }
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "error")

    def test_invalid_tax_profile(self):
        transaction = {
            "total": "1000.00",
            "tax_context": {
                "transaction_type": "service",
                "tax_profile": "invalid"
            }
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "error")

    def test_invalid_total(self):
        transaction = {
            "total": "-100.00",
            "tax_context": {
                "transaction_type": "service",
                "tax_profile": "simples"
            }
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "error")

    def test_custom_rate(self):
        custom_rates = {
            "service": {
                "simples": {"ISS": "0.10"}
            },
            "product": {
                "simples": {"TRIBUTO_DEMONSTRATIVO": "0.08"}
            },
            "transfer": {
                "simples": {}
            }
        }

        agent = TaxAgent(rates=custom_rates)

        transaction = {
            "total": "1000.00",
            "tax_context": {
                "transaction_type": "service",
                "tax_profile": "simples"
            }
        }

        result = agent.process(transaction)

        self.assertEqual(result["total_taxes"], "100.00")


if __name__ == "__main__":
    unittest.main()
