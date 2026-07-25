"""Load sanitized experiment results and render a Markdown summary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ptcg_agent_lab.metrics import compare_counts


def load_results(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if "comparisons" not in payload or "leaderboard" not in payload:
        raise ValueError("results require leaderboard and comparisons")
    return payload


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Experiment summary",
        "",
        "## Leaderboard snapshots",
        "",
        "| Version | Current score | Observed peak | Approach |",
        "|---|---:|---:|---|",
    ]
    for row in payload["leaderboard"]:
        lines.append(
            f"| {row['version']} | {row['public_score']:.1f} | "
            f"{row.get('peak_score', row['public_score']):.1f} | "
            f"{row['approach']} |"
        )
    lines.extend(
        [
            "",
            "## Local complete-game gates",
            "",
            "| Gate | Baseline | Candidate | Delta |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in payload["comparisons"]:
        comparison = compare_counts(
            games=row["games"],
            baseline_wins=row["baseline_wins"],
            candidate_wins=row["candidate_wins"],
            baseline_draws=row.get("baseline_draws", 0),
            candidate_draws=row.get("candidate_draws", 0),
        )
        lines.append(
            f"| {row['name']} | {row['baseline_wins']}/{row['games']} | "
            f"{row['candidate_wins']}/{row['games']} | "
            f"{comparison.delta_percentage_points:+.1f} pp |"
        )
    if payload.get("notes"):
        lines.extend(["", "## Notes", ""])
        lines.extend(f"- {note}" for note in payload["notes"])
    return "\n".join(lines) + "\n"
