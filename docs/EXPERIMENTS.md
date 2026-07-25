# Experiment history

## V1–V2: search versus speed

The first agents compared shallow forward search with a fast heuristic. Search
was more expensive and did not automatically translate to a stronger public
score. This established the need for complete-game evaluation rather than
assuming more computation is better.

## V3–V4: deck-specific sequencing

A tournament and playoff process selected a Cinderace/Mega Starmie deck.
Deck-specific energy distribution and sequencing produced the strongest public
submission. V4 later reached a 911 observed public-score peak and currently
sits near 826.

## V5: replay-derived patches

Replay analysis motivated targeted board guards and disruption. The resulting
agent scored 762.3, below V4. Local fixes did not generalize strongly enough.

## V6: copying the leading deck

The public leader's exact Grim/Froslass/Munkidori deck was reproduced, but the
submission performed poorly. This was decisive evidence that pilot quality—not
deck list alone—was the main gap.

## Replay imitation

Sequence forests and a semantic LightGBM ranker were trained from hundreds of
leader replays. Held-out action prediction improved substantially, including
very high accuracy for several mechanical contexts.

Complete-game performance degraded. Strict confidence gates reduced the damage
but did not beat the deterministic fallback. Direct imitation was retired.

## On-policy evolution

A linear MAIN policy was optimized through terminal game outcomes. It was the
first branch to improve multiple fresh local gates, but only by roughly one to
two points—too small for the underlying weak baseline.

## Counterfactual Q search

The next architecture generated terminal labels for every legal action at
states visited by the current policy. A grouped ranker improved untouched
counterfactual-root selection from 60.3% to 70.9%.

Fresh complete-game tests improved the Grim mirror, Alakazam, the
occurrence-weighted field, and the weak baseline's V4 matchup. The policy still
lost 131 of 160 games against V4, so it was not submitted.

## V4 Q transfer

The same architecture was transferred to V4. Ordinary local training states
were saturated because V4 already solved most games against available local
opponents. Adversarial state collection created harder examples, but the
full-game candidate reached only 121 wins after 180 games versus V4's 134.

The run was stopped early and the candidate was retired.

## General lesson

Increasing architectural complexity is useful only when the training
distribution contains mistakes the model can learn to fix. The next bottleneck
is stronger opponent-state data, not a larger model.
