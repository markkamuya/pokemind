# Architecture

## Design objective

The system optimizes complete-game outcomes while remaining conservative around
a proven fallback policy. Offline action accuracy is diagnostic only; candidate
promotion depends on fresh seeded games.

## Components

### 1. Deterministic fallback

A deck-aware heuristic supplies every legal decision and acts as the fallback
for learned policies. This keeps the agent functional when a model is missing,
uncertain, or outside its trained contexts.

### 2. Replay-derived meta model

Replays are converted into an occurrence-weighted catalog of opponent deck
archetypes. The catalog determines the evaluation mix and prevents a candidate
from being optimized only against a convenient adversary.

### 3. On-policy state collection

The current agent plays complete games. Eligible decision roots are sampled
from the states that the agent itself visits. This reduces the distribution
shift seen in direct behavior cloning.

### 4. Counterfactual branching

At a sampled root, the seeded simulator branches each legal MAIN action. Each
branch is rolled forward under fixed policies until a terminal win, loss, or
draw. The result becomes an action-value label.

```text
state s
├── action a0 → rollout → loss  (0.0)
├── action a1 → rollout → win   (1.0)
└── action a2 → rollout → draw  (0.5)
```

Actions remain grouped by root. A learning algorithm must rank alternatives
within a root rather than treat unrelated states as interchangeable examples.

### 5. Identity-rich features

The final counterfactual branch replaced small hash buckets with exact
identities for cards observed in the current meta. Features include:

- turn and prize state;
- active and bench identities;
- HP, damage, energy, and tool summaries;
- visible hand, board, discard, and stadium counts;
- action type, card, attack, and target;
- whether an action matches the fallback.

### 6. Grouped action ranker

A gradient-boosted ranker predicts relative action quality. The public
`TreeRanker` implements dependency-free inference for exported LightGBM JSON
trees.

### 7. Simulator-backed policy

For a live MAIN decision:

1. Produce the fallback action.
2. Branch every legal action in the simulator.
3. Roll each branch through one opposing turn.
4. Encode the resulting leaf plus the original action.
5. Rank the alternatives.
6. Choose the best action, with the fallback as the stable tie-break.

### 8. Promotion gates

A candidate must:

- improve aggregate win rate on enough games;
- avoid material matchup regressions;
- reproduce the gain across fresh seed batches;
- pass complete-game tests rather than only offline metrics.

The default public gate requires 500 games, +5 percentage points overall, no
matchup regression worse than 2 points, and three fresh batches. Projects can
configure these values based on submission cost and risk tolerance.

## Why direct imitation was retired

Replay imitation achieved high held-out accuracy in several mechanical
contexts, but action errors compounded during complete games and pushed the
agent outside the replay distribution. Even high-confidence overrides failed
closed-loop gates. Replays remain useful as priors and meta evidence, not as a
standalone policy.
