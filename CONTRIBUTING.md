# Contributing

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
ruff check .
pytest
```

## Experiment contributions

Every performance change should include:

- the frozen baseline;
- opponent mix and game count;
- seed or split protocol;
- aggregate and per-matchup results;
- promotion-gate outcome;
- known limitations.

Do not commit competition assets, raw replays, credentials, trained private
weights, or simulator binaries.
