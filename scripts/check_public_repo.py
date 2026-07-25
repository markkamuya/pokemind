"""Fail if public-repository safety boundaries are violated."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_BYTES = 1_000_000
IGNORED_DIRECTORIES = {".git", ".ruff_cache", ".pytest_cache", "__pycache__"}
ALLOWED_BINARY_ASSETS = {
    Path("assets/pokemind-social-preview.jpg"): b"\xff\xd8\xff",
    Path("assets/v4-vs-alakazam.gif"): b"GIF89a",
}
BANNED_SUFFIXES = {
    ".dylib",
    ".so",
    ".dll",
    ".pdf",
    ".npz",
    ".npy",
    ".pkl",
    ".pickle",
    ".joblib",
    ".zip",
    ".tar",
    ".gz",
}
BANNED_NAMES = {
    "access_token",
    "kaggle.json",
    ".env",
}
SECRET_PATTERNS = {
    "Kaggle API token": re.compile(r"\bKGAT_[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(r"\b(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "bearer credential": re.compile(
        r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}\b", re.IGNORECASE
    ),
}


def public_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not IGNORED_DIRECTORIES.intersection(path.parts)
    )


def main() -> int:
    problems: list[str] = []
    for path in public_files():
        relative = path.relative_to(ROOT)
        if path.name in BANNED_NAMES:
            problems.append(f"{relative}: banned credential filename")
        if any("".join(path.suffixes).endswith(suffix) for suffix in BANNED_SUFFIXES):
            problems.append(f"{relative}: banned binary/data suffix")
        if path.stat().st_size > MAX_FILE_BYTES:
            problems.append(
                f"{relative}: {path.stat().st_size} bytes exceeds {MAX_FILE_BYTES}"
            )
        if path.is_symlink():
            target = path.resolve()
            if ROOT not in target.parents and target != ROOT:
                problems.append(f"{relative}: symlink escapes repository")
            continue
        if relative in ALLOWED_BINARY_ASSETS:
            if not path.read_bytes().startswith(ALLOWED_BINARY_ASSETS[relative]):
                problems.append(f"{relative}: invalid allowlisted media signature")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            problems.append(f"{relative}: unexpected binary file")
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                problems.append(f"{relative}: possible {label}")
    if problems:
        print("Public repository safety check failed:", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        return 1
    print(f"Public repository safety check passed ({len(public_files())} files).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
