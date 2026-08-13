#!/usr/bin/env python3
"""Exact independent replay for the proof-first structural obstruction.

This script imports no project Python module.  It reads only the inert locked
core JSON, derives minimum-repair path lengths, and checks an exact rational
two-terminal gauge identity.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
CORE_PATH = PROJECT / "primary" / "certificates" / "core_universe.json"
EXPECTED_CORE_SHA256 = "f7ebe0b0ebc93f58cfa5bc2086f55a518b0ce8774da57667fe4c1f169ff39e10"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_lengths(core: dict, occupied: tuple[int, ...]) -> tuple[int, int, int]:
    lengths = [0, 0, 0]
    occupied_set = set(occupied)
    for index, segment in enumerate(core["segments"]):
        lengths[int(segment["path"])] += 1 + int(index in occupied_set)
    return tuple(lengths)


def triangle_count(lengths: tuple[int, int, int]) -> int:
    return sum(
        lengths[i] + lengths[j] == 3
        for i in range(3)
        for j in range(i + 1, 3)
    )


def triangle_role(core: dict, repair: tuple[int, ...]) -> str | None:
    lengths = path_lengths(core, repair)
    pairs = [
        (i, j)
        for i in range(3)
        for j in range(i + 1, 3)
        if lengths[i] + lengths[j] == 3
    ]
    if not pairs:
        return None
    assert len(pairs) == 1
    short_two = next(path for path in pairs[0] if lengths[path] == 2)
    events = core["path_event_sequences"][short_two]
    repair_on_path = [
        index
        for index in repair
        if int(core["segments"][index]["path"]) == short_two
    ]
    if events:
        assert len(events) == 1 and not repair_on_path
        return str(events[0])
    assert len(repair_on_path) == 1
    return "ordinary-port"


def verify_cores() -> dict:
    if sha256(CORE_PATH) != EXPECTED_CORE_SHA256:
        raise AssertionError("locked core JSON hash changed")
    payload = json.loads(CORE_PATH.read_text())
    cores = {row["id"]: row for row in payload["cores"] if row["id"] != "cycle"}
    expected = {
        "theta-0": {
            (2, 3): ((2, 4, 1), 1, "S"),
            (3, 4): ((2, 3, 2), 0, None),
        },
        "theta-1": {
            (2, 3): ((4, 2, 1), 1, "ordinary-port"),
            (2, 4): ((4, 1, 2), 1, "ordinary-port"),
        },
        "theta-2": {
            (2, 3): ((2, 4, 2), 0, None),
            (2, 5): ((2, 3, 3), 0, None),
            (3, 4): ((2, 3, 3), 0, None),
            (4, 5): ((2, 2, 4), 0, None),
        },
        "theta-3": {
            (2,): ((4, 2, 1), 1, "X"),
            (4,): ((3, 3, 1), 0, None),
        },
    }
    observed = {}
    for core_id, core in cores.items():
        rows = {}
        repairs = {tuple(int(i) for i in row) for row in core["minimum_repairs"]}
        if repairs != set(expected[core_id]):
            raise AssertionError((core_id, repairs, set(expected[core_id])))
        for repair in sorted(repairs):
            lengths = path_lengths(core, repair)
            count = triangle_count(lengths)
            role = triangle_role(core, repair)
            actual = (lengths, count, role)
            if actual != expected[core_id][repair]:
                raise AssertionError((core_id, repair, actual, expected[core_id][repair]))
            rows[str(repair)] = {
                "path_lengths": list(lengths),
                "triangle_count": count,
                "triangle_internal_role": role,
            }
        observed[core_id] = rows
    return observed


def verify_gauge() -> dict:
    # G is represented by integers 0,1,2,3 with xor as group operation.
    group = range(4)
    hidden = [(u, v) for u in group for v in group]
    c = {(u, v): Fraction(2 if u == v else 1) for u, v in hidden}

    # Deterministic positive exact tensors; their particular values are
    # irrelevant because cancellation is termwise.
    a = {
        (y, u, v): Fraction(1 + y + 2 * u + 3 * v)
        for y in group
        for u, v in hidden
    }
    b = {
        (z, u, v): Fraction(2 + 2 * z + 5 * u + 7 * v)
        for z in range(3)
        for u, v in hidden
    }

    def contract(left, right, y, z):
        return sum(left[y, u, v] * right[z, u, v] for u, v in hidden)

    a_scaled = {
        (y, u, v): a[y, u, v] * c[u, v]
        for y in group
        for u, v in hidden
    }
    b_scaled = {
        (z, u, v): b[z, u, v] / c[u, v]
        for z in range(3)
        for u, v in hidden
    }
    comparisons = 0
    for y in group:
        for z in range(3):
            if contract(a, b, y, z) != contract(a_scaled, b_scaled, y, z):
                raise AssertionError((y, z))
            comparisons += 1

    # A product c(u,v)=f(u)g(v) has rank one.  The 0/a minor is nonzero.
    nonzero = 1
    determinant = c[0, 0] * c[nonzero, nonzero] - c[0, nonzero] * c[nonzero, 0]
    if determinant != 3:
        raise AssertionError(determinant)

    # Simultaneous group translation leaves c invariant.
    for u, v in hidden:
        for g in group:
            if c[u ^ g, v ^ g] != c[u, v]:
                raise AssertionError((u, v, g))

    return {
        "exact_contraction_comparisons": comparisons,
        "nonfactorizable_minor_determinant": str(determinant),
        "translation_invariant": True,
        "scope": "ambient equivariant tensor gauge; not asserted to preserve JC factor families",
    }


def main() -> None:
    result = {
        "schema": "proof-first-structural-obstruction-v1",
        "core_sha256": sha256(CORE_PATH),
        "minimum_repair_triangle_audit": verify_cores(),
        "two_terminal_gauge": verify_gauge(),
        "status": "PASS",
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()

