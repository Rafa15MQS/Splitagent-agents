
import unittest

from agents.split_payment import SplitPaymentAgent


class TestSplitPaymentAgent(unittest.TestCase):

    def setUp(self):
        self.agent = SplitPaymentAgent()

    def test_equal_payment(self):
        transaction = {
            "total": "100.00",
            "participants": [
                {"name": "Ana"},
                {"name": "Bia"},
                {"name": "Caio"}
            ]
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["total"], "100.00")
        self.assertEqual(
            [item["amount"] for item in result["shares"]],
            ["33.33", "33.33", "33.34"]
        )

    def test_weighted_payment(self):
        transaction = {
            "total": "90.00",
            "participants": [
                {"name": "Ana", "weight": 2},
                {"name": "Bia", "weight": 1}
            ]
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "ok")
        self.assertEqual(
            [item["amount"] for item in result["shares"]],
            ["60.00", "30.00"]
        )

    def test_missing_total(self):
        transaction = {
            "participants": [{"name": "Ana"}]
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "error")

    def test_missing_participants(self):
        transaction = {"total": "100.00"}

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "error")

    def test_invalid_total(self):
        transaction = {
            "total": "-100.00",
            "participants": [{"name": "Ana"}]
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
