
import unittest

from agents.inclusion import InclusionAgent


class TestInclusionAgent(unittest.TestCase):

    def setUp(self):
        self.agent = InclusionAgent()

    def test_all_participants_have_positive_amounts(self):
        transaction = {
            "participants": [
                {"name": "Ana", "amount": "50.00"},
                {"name": "Carlos", "amount": "50.00"}
            ]
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "ok")

    def test_participant_with_zero_amount(self):
        transaction = {
            "participants": [
                {"name": "Ana", "amount": "50.00"},
                {"name": "Carlos", "amount": "0.00"}
            ]
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "warning")

    def test_participant_with_negative_amount(self):
        transaction = {
            "participants": [
                {"name": "Ana", "amount": "-10.00"}
            ]
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "warning")

    def test_empty_participants(self):
        result = self.agent.process({"participants": []})

        self.assertEqual(result["status"], "error")

    def test_invalid_transaction(self):
        result = self.agent.process(None)

        self.assertEqual(result["status"], "error")

    def test_invalid_amount(self):
        transaction = {
            "participants": [
                {"name": "Ana", "amount": "abc"}
            ]
        }

        result = self.agent.process(transaction)

        self.assertEqual(result["status"], "error")


if __name__ == "__main__":
    unittest.main()
