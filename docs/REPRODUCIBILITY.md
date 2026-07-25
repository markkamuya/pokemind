# Reproducibility and competition assets

## Publicly reproducible components

This repository includes:

- statistical comparison utilities;
- occurrence-weighted matchup scheduling;
- explicit promotion gates;
- grouped counterfactual-root evaluation;
- pure-Python inference for exported LightGBM trees;
- sanitized aggregate results and tests.

## User-supplied components

End-to-end competition reproduction requires assets that are intentionally not
redistributed:

- the authorized simulator runtime;
- card metadata obtained under the competition terms;
- episode replays downloaded through the user's account;
- deck lists and generated model weights.

Place those assets outside the Git repository and reference them through
environment variables such as the examples in `.env.example`.

## Recommended private workspace

```text
private-workspace/
├── simulator/
├── data/
├── replays/
├── models/
└── submissions/
```

Do not copy this directory into the public repository.

## Experiment protocol

1. Freeze a baseline policy.
2. Freeze the opponent catalog and training seed panel.
3. Train without using final validation seeds.
4. Evaluate candidate and baseline on identical fresh games.
5. Report every matchup and all stopped runs.
6. Apply the promotion gate before packaging.

## Reporting limitations

Public results should state that:

- replay-derived decks do not reproduce private policies;
- public leaderboard ratings are time-dependent;
- local matches can be correlated by deck, seed, or policy;
- action-prediction accuracy is not a complete-game metric.
