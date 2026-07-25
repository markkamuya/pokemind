"""Framework-agnostic counterfactual decision-root utilities."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from hashlib import sha1


@dataclass(frozen=True)
class ActionBranch:
    root_id: str
    action_id: int
    terminal_value: float
    fallback: bool = False

    def __post_init__(self) -> None:
        if not 0 <= self.terminal_value <= 1:
            raise ValueError("terminal_value must be in [0, 1]")


@dataclass(frozen=True)
class SelectionSummary:
    roots: int
    selected_value: float
    fallback_value: float
    oracle_value: float

    @property
    def regret(self) -> float:
        return self.oracle_value - self.selected_value


def episode_is_holdout(episode_id: str, percent: int = 20) -> bool:
    if not 0 <= percent <= 100:
        raise ValueError("percent must be in [0, 100]")
    digest = sha1(episode_id.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % 100 < percent


def summarize_selection(
    branches: Iterable[ActionBranch],
    predicted_scores: dict[tuple[str, int], float],
) -> SelectionSummary:
    grouped: dict[str, list[ActionBranch]] = defaultdict(list)
    for branch in branches:
        grouped[branch.root_id].append(branch)
    if not grouped:
        raise ValueError("at least one branch is required")
    selected_values: list[float] = []
    fallback_values: list[float] = []
    oracle_values: list[float] = []
    for root_id, options in grouped.items():
        fallback = next((item for item in options if item.fallback), None)
        if fallback is None:
            raise ValueError(f"root {root_id!r} has no fallback action")
        selected = max(
            options,
            key=lambda item: (
                predicted_scores[(root_id, item.action_id)],
                item.fallback,
                -item.action_id,
            ),
        )
        selected_values.append(selected.terminal_value)
        fallback_values.append(fallback.terminal_value)
        oracle_values.append(max(item.terminal_value for item in options))
    count = len(grouped)
    return SelectionSummary(
        roots=count,
        selected_value=sum(selected_values) / count,
        fallback_value=sum(fallback_values) / count,
        oracle_value=sum(oracle_values) / count,
    )
