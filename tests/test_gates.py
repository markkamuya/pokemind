import unittest

from ptcg_agent_lab.gates import GateCriteria, evaluate_gate
from ptcg_agent_lab.metrics import compare_counts


class GateTests(unittest.TestCase):
    def test_candidate_passes_configured_gate(self) -> None:
        comparisons = {
            "grim": compare_counts(games=300, baseline_wins=150, candidate_wins=174),
            "alakazam": compare_counts(
                games=300, baseline_wins=180, candidate_wins=198
            ),
        }
        decision = evaluate_gate(comparisons, fresh_batches=3)
        self.assertTrue(decision.passed)

    def test_matchup_regression_fails_gate(self) -> None:
        comparisons = {
            "grim": compare_counts(games=300, baseline_wins=150, candidate_wins=190),
            "alakazam": compare_counts(
                games=300, baseline_wins=210, candidate_wins=195
            ),
        }
        decision = evaluate_gate(comparisons, fresh_batches=3)
        self.assertFalse(decision.passed)
        self.assertTrue(
            any("alakazam regressed" in reason for reason in decision.reasons)
        )

    def test_small_experiment_fails_gate(self) -> None:
        criteria = GateCriteria(minimum_games=500)
        comparisons = {
            "field": compare_counts(games=100, baseline_wins=50, candidate_wins=60)
        }
        decision = evaluate_gate(comparisons, fresh_batches=3, criteria=criteria)
        self.assertFalse(decision.passed)


if __name__ == "__main__":
    unittest.main()
