# Roadmap

## 1. Hard-state replay collection

Collect fresh V4 losses and current top-agent episodes. Retain only authorized
data in the private workspace.

## 2. Loss-state mining

Identify V4 decisions whose counterfactual alternatives reverse a terminal
loss. Easy wins should not dominate the learning objective.

## 3. Stronger opponent policies

Train opponent models from their own visited states and validate them in
closed-loop games. Use replay imitation as a prior, not as the final policy.

## 4. Conservative V4 residual

Modify V4 only when an action advantage is stable across multiple hidden-state
hypotheses and validation panels.

## 5. Successive-halving evaluation

Use small paired screens to reject weak candidates, then allocate hundreds of
games only to survivors.

## 6. Submission criterion

Package a new candidate only after:

- at least 500 paired games;
- a minimum five-point aggregate improvement;
- no major Grim, Alakazam, Crustle, or Rocket regression;
- reproduction on three fresh seed batches.
