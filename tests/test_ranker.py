import unittest

from pokemind.ranker import TreeRanker


class RankerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ranker = TreeRanker.from_payload(
            {
                "model": {
                    "tree_info": [
                        {
                            "tree_structure": {
                                "split_feature": 0,
                                "threshold": 0.5,
                                "decision_type": "<=",
                                "left_child": {"leaf_value": -1.0},
                                "right_child": {"leaf_value": 1.0},
                            }
                        }
                    ]
                }
            }
        )

    def test_prediction(self) -> None:
        self.assertEqual(self.ranker.predict([0.0]), -1.0)
        self.assertEqual(self.ranker.predict([1.0]), 1.0)

    def test_conservative_choice(self) -> None:
        options = [[0.0], [1.0]]
        self.assertEqual(self.ranker.choose(options, fallback_index=0), 1)
        self.assertEqual(
            self.ranker.choose(options, fallback_index=0, minimum_advantage=3.0),
            0,
        )


if __name__ == "__main__":
    unittest.main()
