"""Command-line interface for deterministic research artifacts."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

from .artifacts import initialize_run
from .scoring import score_candidates
from .validation import validate_run


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="opportunity-radar")
    commands = parser.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser("init", help="create a standard research run")
    init_parser.add_argument("--output", required=True, type=Path)

    score_parser = commands.add_parser("score", help="score and rank candidates")
    score_parser.add_argument("--run", required=True, type=Path)

    validate_parser = commands.add_parser("validate", help="validate evidence and report traceability")
    validate_parser.add_argument("--run", required=True, type=Path)
    validate_parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "init":
        initialize_run(args.output)
        return 0
    if args.command == "score":
        path = args.run / "candidates.json"
        document = json.loads(path.read_text(encoding="utf-8"))
        scored = score_candidates(document)
        path.write_text(json.dumps(scored, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 0

    issues = validate_run(args.run)
    if args.format == "json":
        print(json.dumps({"valid": not issues, "issues": [asdict(issue) for issue in issues]}))
    elif issues:
        for issue in issues:
            print(f"{issue.code}: {issue.message}")
    else:
        print("valid")
    return 1 if issues else 0
