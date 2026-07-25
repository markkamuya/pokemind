"""PokeMind occurrence-weighted matchup schedules."""

from __future__ import annotations

from dataclasses import dataclass
from math import floor


@dataclass(frozen=True)
class MetaEntry:
    name: str
    occurrences: int

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("meta entry name cannot be empty")
        if self.occurrences <= 0:
            raise ValueError("occurrences must be positive")


def allocate_occurrence_counts(
    entries: list[MetaEntry], total_games: int
) -> dict[str, int]:
    """Allocate games with the largest-remainder method."""
    if not entries:
        raise ValueError("at least one meta entry is required")
    if total_games <= 0:
        raise ValueError("total_games must be positive")
    occurrence_total = sum(entry.occurrences for entry in entries)
    exact = [total_games * entry.occurrences / occurrence_total for entry in entries]
    counts = [floor(value) for value in exact]
    remaining = total_games - sum(counts)
    order = sorted(
        range(len(entries)),
        key=lambda index: (
            exact[index] - counts[index],
            entries[index].occurrences,
            entries[index].name,
        ),
        reverse=True,
    )
    for index in order[:remaining]:
        counts[index] += 1
    return {
        entry.name: count for entry, count in zip(entries, counts, strict=True) if count
    }


def interleaved_schedule(entries: list[MetaEntry], total_games: int) -> list[str]:
    """Build a deterministic schedule without long same-matchup blocks."""
    remaining = allocate_occurrence_counts(entries, total_games)
    schedule: list[str] = []
    while remaining:
        for name in sorted(
            remaining,
            key=lambda item: (remaining[item], item),
            reverse=True,
        ):
            schedule.append(name)
            remaining[name] -= 1
        remaining = {name: count for name, count in remaining.items() if count}
    return schedule
