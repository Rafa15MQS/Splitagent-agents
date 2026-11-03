
import unittest
from decimal import Decimal

from core.calculator import (
    calculate_split,
    validate_split,
    detect_rounding_error
)


class TestCalculator(unittest.TestCase):

    def test_equal_split(self):
        participants = [
            {"name": "Ana"},
            {"name": "Bia"},
            {"name": "Caio"}
        ]

        result = calculate_split("100.00", participants)

        self.assertEqual(
            [item["amount"] for item in result],
            [Decimal("33.33"), Decimal("33.33"), Decimal("33.34")]
        )

    def test_weighted_split(self):
        participants = [
            {"name": "Ana", "weight": 2},
            {"name": "Bia", "weight": 1}
        ]

        result = calculate_split("90.00", participants)

        self.assertEqual(
            [item["amount"] for item in result],
            [Decimal("60.00"), Decimal("30.00")]
        )

    def test_validate_correct_split(self):
        transaction = {
            "total": "100.00",
            "shares": [
                {"name": "Ana", "amount": "50.00"},
                {"name": "Bia", "amount": "50.00"}
            ]
        }

        self.assertTrue(validate_split(transaction))

    def test_detect_rounding_error(self):
        shares = [
            {"name": "Ana", "amount": "40.00"},
            {"name": "Bia", "amount": "40.00"}
        ]

        self.assertTrue(detect_rounding_error(shares, "100.00"))

    def test_invalid_total(self):
        participants = [{"name": "Ana"}]

        with self.assertRaises(ValueError):
            calculate_split("-10.00", participants)

    def test_empty_participants(self):
        with self.assertRaises(ValueError):
            calculate_split("100.00", [])

    def test_inconsistent_weights(self):
        participants = [
            {"name": "Ana", "weight": 2},
            {"name": "Bia"}
        ]

        with self.assertRaises(ValueError):
            calculate_split("100.00", participants)


if __name__ == "__main__":
    unittest.main()
