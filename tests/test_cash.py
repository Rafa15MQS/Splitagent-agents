
import unittest

from agents.cash import CashAgent


class TestCashAgent(unittest.TestCase):

    def setUp(self):
        self.agent = CashAgent()

    def test_valid_movements(self):
        movements = [
            {"type": "income", "amount": "1000.00"},
            {"type": "income", "amount": "500.00"},
            {"type": "expense", "amount": "300.00"},
            {"type": "expense", "amount": "200.00"}
        ]

        result = self.agent.process(movements)

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["total_income"], "1500.00")
        self.assertEqual(result["total_expense"], "500.00")
        self.assertEqual(result["balance"], "1000.00")

    def test_negative_balance(self):
        movements = [
            {"type": "income", "amount": "100.00"},
            {"type": "expense", "amount": "200.00"}
        ]

        result = self.agent.process(movements)

        self.assertEqual(result["balance"], "-100.00")

    def test_empty_movements(self):
        result = self.agent.process([])

        self.assertEqual(result["status"], "error")

    def test_invalid_type(self):
        movements = [
            {"type": "unknown", "amount": "100.00"}
        ]

        result = self.agent.process(movements)

        self.assertEqual(result["status"], "error")

    def test_invalid_amount(self):
        movements = [
            {"type": "income", "amount": "-100.00"}
        ]

        result = self.agent.process(movements)

        self.assertEqual(result["status"], "error")

    def test_invalid_description(self):
        movements = [
            {
                "type": "income",
                "amount": "100.00",
                "description": 123
            }
        ]

        result = self.agent.process(movements)

        self.assertEqual(result["status"], "error")

    def test_invalid_movement(self):
        result = self.agent.process(["invalid"])

        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
