
import unittest

from agents.forecast import ForecastAgent


class TestForecastAgent(unittest.TestCase):

    def setUp(self):
        self.agent = ForecastAgent()

    def test_valid_forecast(self):
        movements = [
            {"type": "income", "amount": "1000.00", "date": "2026-11-02"},
            {"type": "income", "amount": "500.00", "date": "2026-11-05"},
            {"type": "expense", "amount": "300.00", "date": "2026-11-08"},
            {"type": "expense", "amount": "200.00", "date": "2026-11-15"}
        ]

        result = self.agent.process(
            movements,
            "2026-11-10"
        )

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["total_income"], "1500.00")
        self.assertEqual(result["total_expense"], "300.00")
        self.assertEqual(result["projected_balance"], "1200.00")
        self.assertEqual(result["movements_considered"], 3)

    def test_opening_balance(self):
        movements = [
            {"type": "income", "amount": "500.00", "date": "2026-11-05"}
        ]

        result = self.agent.process(
            movements,
            "2026-11-10",
            "1000.00"
        )

        self.assertEqual(result["projected_balance"], "1500.00")

    def test_negative_projected_balance(self):
        movements = [
            {"type": "expense", "amount": "500.00", "date": "2026-11-05"}
        ]

        result = self.agent.process(
            movements,
            "2026-11-10"
        )

        self.assertEqual(result["projected_balance"], "-500.00")

    def test_empty_movements(self):
        result = self.agent.process([], "2026-11-10")

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["projected_balance"], "0.00")

    def test_invalid_date(self):
        result = self.agent.process([], "data-invalida")

        self.assertEqual(result["status"], "error")

    def test_invalid_amount(self):
        movements = [
            {"type": "income", "amount": "-100.00", "date": "2026-11-05"}
        ]

        result = self.agent.process(movements, "2026-11-10")

        self.assertEqual(result["status"], "error")

    def test_invalid_movement_type(self):
        movements = [
            {"type": "unknown", "amount": "100.00", "date": "2026-11-05"}
        ]

        result = self.agent.process(movements, "2026-11-10")

        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
