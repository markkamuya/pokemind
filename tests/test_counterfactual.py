import unittest

from pokemind.counterfactual import (
    ActionBranch,
    episode_is_holdout,
    summarize_selection,
)


class CounterfactualTests(unittest.TestCase):
    def test_selection_summary(self) -> None:
        branches = [
            ActionBranch("a", 0, 0.0, fallback=True),
            ActionBranch("a", 1, 1.0),
            ActionBranch("b", 0, 1.0, fallback=True),
            ActionBranch("b", 1, 0.0),
        ]
        scores = {
            ("a", 0): 0.1,
            ("a", 1): 0.9,
            ("b", 0): 0.8,
            ("b", 1): 0.2,
        }
        summary = summarize_selection(branches, scores)
        self.assertEqual(summary.selected_value, 1.0)
        self.assertEqual(summary.fallback_value, 0.5)
        self.assertEqual(summary.regret, 0.0)

    def test_holdout_is_stable(self) -> None:
        first = episode_is_holdout("episode-42")
        second = episode_is_holdout("episode-42")
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
