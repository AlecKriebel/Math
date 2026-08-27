#!/usr/bin/env python3
"""Reject duplicate object names or syntax errors in every packaged JSON file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON object name: {key}")
        value[key] = item
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    failures: list[dict[str, str]] = []
    count = 0
    for path in sorted(args.root.resolve().rglob("*.json")):
        if ".venv" in path.parts:
            continue
        count += 1
        try:
            json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        except Exception as error:  # an inventory audit must report every bad file
            failures.append(
                {
                    "path": path.relative_to(args.root.resolve()).as_posix(),
                    "error": f"{type(error).__name__}: {error}",
                }
            )
    print(
        json.dumps(
            {
                "json_files_checked": count,
                "failures": failures,
                "status": "PASS" if not failures else "FAIL",
            },
            sort_keys=True,
        )
    )
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
