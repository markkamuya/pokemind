"""Explicit PokeMind candidate-promotion gates."""

from __future__ import annotations

from dataclasses import dataclass

from pokemind.metrics import CountComparison


@dataclass(frozen=True)
class GateCriteria:
    minimum_games: int = 500
    minimum_overall_delta: float = 0.05
    maximum_matchup_regression: float = 0.02
    minimum_fresh_batches: int = 3


@dataclass(frozen=True)
class GateDecision:
    passed: bool
    reasons: tuple[str, ...]
    total_games: int
    overall_delta: float


def evaluate_gate(
    comparisons: dict[str, CountComparison],
    *,
    fresh_batches: int,
    criteria: GateCriteria | None = None,
) -> GateDecision:
    criteria = criteria or GateCriteria()
    if not comparisons:
        return GateDecision(False, ("no matchup results supplied",), 0, 0.0)
    total_games = sum(item.baseline.games for item in comparisons.values())
    baseline_wins = sum(item.baseline.wins for item in comparisons.values())
    candidate_wins = sum(item.candidate.wins for item in comparisons.values())
    overall_delta = (candidate_wins - baseline_wins) / total_games
    reasons: list[str] = []
    if total_games < criteria.minimum_games:
        reasons.append(f"only {total_games} games; need {criteria.minimum_games}")
    if overall_delta < criteria.minimum_overall_delta:
        reasons.append(
            f"overall delta {overall_delta:+.1%}; "
            f"need {criteria.minimum_overall_delta:+.1%}"
        )
    for name, comparison in sorted(comparisons.items()):
        if comparison.delta < -criteria.maximum_matchup_regression:
            reasons.append(
                f"{name} regressed {comparison.delta:+.1%}; "
                f"limit is {-criteria.maximum_matchup_regression:+.1%}"
            )
    if fresh_batches < criteria.minimum_fresh_batches:
        reasons.append(
            f"only {fresh_batches} fresh batches; need {criteria.minimum_fresh_batches}"
        )
    return GateDecision(
        passed=not reasons,
        reasons=tuple(reasons),
        total_games=total_games,
        overall_delta=overall_delta,
    )
