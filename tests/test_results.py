import unittest

from ptcg_agent_lab.results import render_markdown


class ResultsTests(unittest.TestCase):
    def test_markdown_contains_delta(self) -> None:
        payload = {
            "leaderboard": [
                {
                    "version": "V4",
                    "public_score": 826.0,
                    "peak_score": 911.0,
                    "approach": "Search",
                }
            ],
            "comparisons": [
                {
                    "name": "field",
                    "games": 100,
                    "baseline_wins": 50,
                    "candidate_wins": 55,
                }
            ],
        }
        report = render_markdown(payload)
        self.assertIn("826.0", report)
        self.assertIn("911.0", report)
        self.assertIn("+5.0 pp", report)


if __name__ == "__main__":
    unittest.main()
