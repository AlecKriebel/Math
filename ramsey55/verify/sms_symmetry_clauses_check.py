#!/usr/bin/env python3
"""Check SMS row-lex symmetry clauses against their permutation witnesses.

Current SMS emits JSON records ``[[literals],[permutation]]`` where each
literal is ``[sign,u,v]``.  This checker independently verifies the standard
row-major lex-leader pattern for every record.  It deliberately rejects the
experimental colex format and directed graphs.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from datetime import datetime, timezone
from pathlib import Path


CHECKER_ID = "independent_sms_row_lex_witness_checker_v1"


def normalized_pair(value: object, order: int) -> tuple[int, int]:
    if (
        not isinstance(value, list)
        or len(value) != 3
        or value[0] not in (-1, 1)
        or not isinstance(value[1], int)
        or not isinstance(value[2], int)
    ):
        raise ValueError("malformed signed-edge record")
    left, right = value[1], value[2]
    if not 0 <= left < order or not 0 <= right < order or left == right:
        raise ValueError("signed edge is outside the graph")
    return min(left, right), max(left, right)


def check_record(record: object, order: int) -> None:
    if not isinstance(record, list) or len(record) != 2:
        raise ValueError("malformed clause/witness record")
    literals, permutation = record
    if not isinstance(literals, list) or len(literals) < 2:
        raise ValueError("symmetry clause has fewer than two literals")
    if (
        not isinstance(permutation, list)
        or any(not isinstance(value, int) for value in permutation)
        or sorted(permutation) != list(range(order))
    ):
        raise ValueError("witness is not a vertex permutation")

    remaining = list(literals)
    terminal_seen = False
    for left, right in itertools.combinations(range(order), 2):
        image = normalized_pair(
            [-1, permutation[left], permutation[right]], order
        )
        normal = (left, right)
        if normal == image:
            continue
        if len(remaining) == 2:
            if remaining[0][0] != -1 or remaining[1][0] != 1:
                raise ValueError("terminal lex comparison has wrong signs")
            if normalized_pair(remaining[0], order) != normal:
                raise ValueError("terminal negative literal is not normal edge")
            if normalized_pair(remaining[1], order) != image:
                raise ValueError("terminal positive literal is not image edge")
            remaining.clear()
            terminal_seen = True
            break

        literal = remaining.pop(0)
        sign = literal[0]
        expected = normal if sign == -1 else image
        if normalized_pair(literal, order) != expected:
            raise ValueError("lex-prefix literal does not match its witness")
    if remaining or not terminal_seen:
        raise ValueError("symmetry clause has no valid terminal comparison")


def check(path: Path, order: int) -> dict[str, object]:
    raw = path.read_bytes()
    document = json.loads(raw)
    if not isinstance(document, dict) or set(document) != {"sym_clauses"}:
        raise ValueError("unexpected symmetry JSON schema")
    records = document["sym_clauses"]
    if not isinstance(records, list):
        raise ValueError("sym_clauses is not an array")
    for record in records:
        check_record(record, order)
    return {
        "schema": "ramsey55.sms_symmetry_check.v1",
        "checker": CHECKER_ID,
        "checked_utc": datetime.now(timezone.utc).isoformat(),
        "valid": True,
        "order": order,
        "symmetry_clause_count": len(records),
        "symmetry_path": str(path.resolve()),
        "symmetry_bytes": len(raw),
        "symmetry_sha256": hashlib.sha256(raw).hexdigest(),
        "scope": (
            "standard undirected row-major lex-leader witnesses; "
            "experimental colex mode is excluded"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("symmetry_json", type=Path)
    parser.add_argument("--order", type=int, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    try:
        result = check(args.symmetry_json, args.order)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        result = {
            "schema": "ramsey55.sms_symmetry_check.v1",
            "checker": CHECKER_ID,
            "valid": False,
            "error": str(error),
        }
    result["runtime_seconds"] = time.monotonic() - started
    result["checker_source_sha256"] = hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, sort_keys=True))
    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
