"""Small, dependency-free statistical helpers for policy evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class BinomialResult:
    wins: int
    games: int
    draws: int = 0

    def __post_init__(self) -> None:
        if self.games <= 0:
            raise ValueError("games must be positive")
        if min(self.wins, self.draws) < 0:
            raise ValueError("wins and draws cannot be negative")
        if self.wins + self.draws > self.games:
            raise ValueError("wins plus draws cannot exceed games")

    @property
    def win_rate(self) -> float:
        return self.wins / self.games

    @property
    def score_rate(self) -> float:
        return (self.wins + 0.5 * self.draws) / self.games

    def wilson_interval(self, z: float = 1.96) -> tuple[float, float]:
        """Wilson score interval over wins; draws are not counted as wins."""
        rate = self.win_rate
        denominator = 1 + z * z / self.games
        center = (rate + z * z / (2 * self.games)) / denominator
        radius = (
            z
            * sqrt(
                rate * (1 - rate) / self.games + z * z / (4 * self.games * self.games)
            )
            / denominator
        )
        return max(0.0, center - radius), min(1.0, center + radius)


@dataclass(frozen=True)
class CountComparison:
    baseline: BinomialResult
    candidate: BinomialResult

    def __post_init__(self) -> None:
        if self.baseline.games != self.candidate.games:
            raise ValueError("baseline and candidate must use the same game count")

    @property
    def delta(self) -> float:
        return self.candidate.win_rate - self.baseline.win_rate

    @property
    def delta_percentage_points(self) -> float:
        return 100 * self.delta


def compare_counts(
    *,
    games: int,
    baseline_wins: int,
    candidate_wins: int,
    baseline_draws: int = 0,
    candidate_draws: int = 0,
) -> CountComparison:
    return CountComparison(
        baseline=BinomialResult(baseline_wins, games, baseline_draws),
        candidate=BinomialResult(candidate_wins, games, candidate_draws),
    )
