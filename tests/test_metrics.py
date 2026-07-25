import unittest

from pokemind.metrics import BinomialResult, compare_counts


class MetricsTests(unittest.TestCase):
    def test_rates_and_interval(self) -> None:
        result = BinomialResult(wins=60, games=100, draws=4)
        self.assertEqual(result.win_rate, 0.6)
        self.assertEqual(result.score_rate, 0.62)
        low, high = result.wilson_interval()
        self.assertLess(low, 0.6)
        self.assertGreater(high, 0.6)

    def test_count_comparison(self) -> None:
        comparison = compare_counts(
            games=240,
            baseline_wins=133,
            candidate_wins=142,
        )
        self.assertAlmostEqual(comparison.delta_percentage_points, 3.75)

    def test_rejects_invalid_counts(self) -> None:
        with self.assertRaises(ValueError):
            BinomialResult(wins=10, games=5)


if __name__ == "__main__":
    unittest.main()
