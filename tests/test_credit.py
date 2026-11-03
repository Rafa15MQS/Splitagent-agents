
import unittest

from agents.credit import CreditAgent


class TestCreditAgent(unittest.TestCase):

    def setUp(self):
        self.agent = CreditAgent()

    def test_credit_available(self):
        transaction = {
            "total": "100.00",
            "credit_context": {
                "credit_limit": "1000.00",
                "current_debt": "200.00"
            }
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "ok")

    def test_insufficient_credit(self):
        transaction = {
            "total": "900.00",
            "credit_context": {
                "credit_limit": "1000.00",
                "current_debt": "200.00"
            }
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "warning")

    def test_missing_credit_context(self):
        result = self.agent.process({"total": "100.00"})

        self.assertEqual(result["status"], "error")

    def test_invalid_credit_limit(self):
        transaction = {
            "total": "100.00",
            "credit_context": {
                "credit_limit": "-100.00",
                "current_debt": "0.00"
            }
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "error")

    def test_invalid_transaction(self):
        result = self.agent.process(None)

        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
