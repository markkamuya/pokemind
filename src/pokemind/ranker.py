"""PokeMind inference for JSON-exported LightGBM tree ensembles."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TreeRanker:
    trees: tuple[dict[str, Any], ...]

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> TreeRanker:
        trees = tuple(item["tree_structure"] for item in payload["model"]["tree_info"])
        if not trees:
            raise ValueError("payload contains no trees")
        return cls(trees)

    @staticmethod
    def _tree_value(node: dict[str, Any], features: Sequence[float]) -> float:
        while "leaf_value" not in node:
            if node.get("decision_type", "<=") != "<=":
                raise ValueError("categorical LightGBM splits are unsupported")
            feature_index = int(node["split_feature"])
            value = float(features[feature_index])
            node = (
                node["left_child"]
                if value <= float(node["threshold"])
                else node["right_child"]
            )
        return float(node["leaf_value"])

    def predict(self, features: Sequence[float]) -> float:
        return sum(self._tree_value(tree, features) for tree in self.trees)

    def choose(
        self,
        options: Sequence[Sequence[float]],
        *,
        fallback_index: int,
        minimum_advantage: float = 0.0,
    ) -> int:
        if not options:
            raise ValueError("at least one option is required")
        if not 0 <= fallback_index < len(options):
            raise IndexError("fallback_index is out of range")
        scores = [self.predict(option) for option in options]
        best = max(
            range(len(options)),
            key=lambda index: (
                scores[index],
                index == fallback_index,
                -index,
            ),
        )
        if scores[best] - scores[fallback_index] < minimum_advantage:
            return fallback_index
        return best
