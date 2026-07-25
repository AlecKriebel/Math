#!/usr/bin/env python3
"""Fail-closed bookkeeping checks for the candidate quartic taxonomy."""

from __future__ import annotations

import json
from pathlib import Path


path = Path(__file__).with_name("candidate_manifest.json")
data = json.loads(path.read_text(encoding="utf-8"))

assert data["status"] == "candidate-not-frozen"
rows = data["rows"]
assert len(rows) == data["leading_row_count"] == 14
assert len({row["id"] for row in rows}) == 14
assert rows[0]["id"] == "Q1" and rows[0]["rank"] == 1
assert all(row["rank"] == 2 for row in rows[1:])
assert sum(row["leaf_count"] for row in rows) == data["structural_leaf_count"] == 68
assert sum(row["current_status"] == "excluded-audited" for row in rows) == 7
assert sum(row["current_status"] == "open" for row in rows) == 7

expected_rank_two = {
    (0, 4, 1, 1, 1),
    (0, 2, 2, 1, 2),
    (0, 2, 2, 2, 1),
    (0, 1, 4, 1, 4),
    (0, 1, 4, 2, 2),
    (0, 1, 4, 4, 1),
    (1, 3, 1, 1, 1),
    (1, 1, 3, 1, 3),
    (1, 1, 3, 3, 1),
    (2, 2, 1, 1, 1),
    (2, 1, 2, 1, 2),
    (2, 1, 2, 2, 1),
    (3, 1, 1, 1, 1),
}


def parse(identifier: str) -> tuple[int, int, int, int, int]:
    pieces = identifier.split("-")
    assert pieces[0] == "Q2"
    return tuple(int(piece[1:]) for piece in pieces[1:])  # type: ignore[return-value]


assert {parse(row["id"]) for row in rows[1:]} == expected_rank_two
assert all(e + a * b == 4 and b == delta * nu for e, a, b, delta, nu in expected_rank_two)

print("PASS 14 unique leading rows")
print("PASS 13 rank-two tuples exhaust e+ab=4 and b=delta*nu")
print("PASS candidate structural denominator is 68 leaves")
print("PASS candidate row score is 7 excluded / 14 total")
