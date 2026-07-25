"""PokeMind command-line interface for public experiment reports."""

from __future__ import annotations

import argparse
from pathlib import Path

from pokemind.results import load_results, render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pokemind")
    subparsers = parser.add_subparsers(dest="command", required=True)
    summarize = subparsers.add_parser(
        "summarize", help="render a sanitized benchmark JSON file"
    )
    summarize.add_argument("results", type=Path)
    summarize.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "summarize":
        report = render_markdown(load_results(args.results))
        if args.output:
            args.output.write_text(report, encoding="utf-8")
        else:
            print(report, end="")
        return 0
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
