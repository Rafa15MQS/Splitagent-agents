
import unittest

from agents.guardian import GuardianAgent


class TestGuardianAgent(unittest.TestCase):

    def setUp(self):
        self.agent = GuardianAgent()

    def valid_transaction(self):
        return {
            "total": "100.00",
            "participants": [
                {"name": "Ana"},
                {"name": "Bia"}
            ]
        }

    def test_valid_transaction(self):
        result = self.agent.process(self.valid_transaction())

        self.assertEqual(result["status"], "ok")

    def test_missing_field(self):
        result = self.agent.process({"total": "100.00"})

        self.assertIn("MISSING_FIELD", result["errors"])

    def test_duplicate_participant(self):
        transaction = {
            "total": "100.00",
            "participants": [
                {"name": "Ana"},
                {"name": "ana"}
            ]
        }

        result = self.agent.process(transaction)

        self.assertIn("DUPLICATE_PARTICIPANT", result["errors"])

    def test_invalid_total(self):
        transaction = self.valid_transaction()
        transaction["total"] = "-100.00"

        result = self.agent.process(transaction)

        self.assertIn("INVALID_TOTAL", result["errors"])

    def test_invalid_participants(self):
        transaction = {
            "total": "100.00",
            "participants": []
        }

        result = self.agent.process(transaction)

        self.assertIn("INVALID_PARTICIPANTS", result["errors"])

    def test_invalid_weight(self):
        transaction = {
            "total": "100.00",
            "participants": [
                {"name": "Ana", "weight": 0},
                {"name": "Bia", "weight": 1}
            ]
        }

        result = self.agent.process(transaction)

        self.assertIn("INVALID_WEIGHT", result["errors"])

    def test_inconsistent_weights(self):
        transaction = {
            "total": "100.00",
            "participants": [
                {"name": "Ana", "weight": 2},
                {"name": "Bia"}
            ]
        }

        result = self.agent.process(transaction)

        self.assertIn("INVALID_WEIGHT", result["errors"])


if __name__ == "__main__":
    unittest.main()
