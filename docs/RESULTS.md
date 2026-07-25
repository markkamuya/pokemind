# Results

## Public leaderboard snapshots

These scores are historical public snapshots from the experiment series. They
are not guarantees of current rank or future performance.

| Version | Observed public score | Outcome |
|---|---:|---|
| V1 | 561.2 | Initial search baseline |
| V2 | 519.8 | Faster but weaker |
| V3 | 668.9 | Strong deck-specific heuristic |
| **V4** | **911 peak / 826 current** | Current submission champion |
| V5 | 762.3 | Did not replace V4 |

## Counterfactual Q branch

| Complete-game gate | Baseline | Candidate | Delta |
|---|---:|---:|---:|
| Grim mirror, two fresh batches | 125/240 | 147/240 | +9.2 pp |
| Alakazam, two fresh batches | 174/240 | 182/240 | +3.3 pp |
| Occurrence-weighted field | 133/240 | 142/240 | +3.8 pp |
| Against V4 | 22/160 | 29/160 | +4.4 pp |

Offline, the residual ranker selected terminal-winning actions on 70.9% of
untouched roots, compared with 60.3% for its actual fallback.

## Failed V4 transfer

At 180 occurrence-weighted games:

- V4 fallback: 134 wins.
- V4 Q transfer: 121 wins.

The test was stopped because the regression was already decisive.

## Interpretation

The Q architecture improved a weak policy but did not clear the project
champion. It is retained as infrastructure, not marketed as a winning agent.

Local opponents use extracted deck lists with reconstructed policies. Private
leaderboard pilots are unavailable, so local win rates should not be converted
directly into expected leaderboard ratings.

Generate this table from the sanitized source data with:

```bash
pokemind summarize examples/benchmark_results.json
```
