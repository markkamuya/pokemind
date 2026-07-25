"""Public research utilities for PTCG Agent Lab."""

from ptcg_agent_lab.gates import GateCriteria, GateDecision, evaluate_gate
from ptcg_agent_lab.metrics import BinomialResult, compare_counts

__all__ = [
    "BinomialResult",
    "GateCriteria",
    "GateDecision",
    "compare_counts",
    "evaluate_gate",
]

__version__ = "0.1.0"
