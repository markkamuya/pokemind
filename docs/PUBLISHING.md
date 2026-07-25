# Publishing checklist

## Before creating the repository

- Revoke any credential previously exposed in chat, terminal output, or logs.
- Confirm that the folder being published is this sanitized repository—not the
  private competition workspace.
- Run the test and safety suites:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/check_public_repo.py
```

## Initialize locally

```bash
git init
git add .
git status
git commit -m "Initial public release"
```

Inspect `git status` before committing. Expected content includes only source,
tests, documentation, CI configuration, and sanitized JSON examples.

## Create and push

After creating an empty GitHub repository:

```bash
git branch -M main
git remote add origin https://github.com/YOUR_ACCOUNT/pokemind.git
git push -u origin main
```

Recommended repository description:

> Reproducible evaluation, counterfactual action-value learning, and promotion
> gates for turn-based card-game agents.

Recommended topics:

```text
game-ai
agents
reinforcement-learning
imitation-learning
lightgbm
python
```

## Suggested first release

Tag `v0.1.0` after GitHub Actions passes. Do not attach competition submission
archives, simulator libraries, replays, model weights, or datasets to the
release.
