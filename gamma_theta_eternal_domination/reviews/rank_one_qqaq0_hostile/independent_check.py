#!/usr/bin/env python3
"""Clean-room incidence audit for the rank-one QQ0/AQ0 contradiction.

This checker does not import the candidate checker or search code.  It
enumerates all 2^21 simple graphs on the seven named vertices, filters the
literal QQ0/AQ0 hypotheses, and verifies each one-guard branch used by the
proof.  Accepted eternal-family dependencies remain mathematical inputs.
"""

from itertools import combinations
import json


VERTICES = ("u", "x", "p", "q", "r", "y", "z")
INDEX = {v: i for i, v in enumerate(VERTICES)}
PAIRS = tuple(combinations(VERTICES, 2))
PAIR_INDEX = {frozenset(pair): i for i, pair in enumerate(PAIRS)}


def bit(a: str, b: str) -> int:
    return 1 << PAIR_INDEX[frozenset((a, b))]


def adjacent(mask: int, a: str, b: str) -> bool:
    if a == b:
        return False
    return bool(mask & bit(a, b))


def successors(mask: int, source: frozenset[str], target: str):
    assert target not in source
    return {
        guard: (source - {guard}) | {target}
        for guard in source
        if adjacent(mask, guard, target)
    }


def misses(mask: int, source: frozenset[str], target: str) -> bool:
    assert target not in source
    return not any(adjacent(mask, guard, target) for guard in source)


def all_distinct(*names: str) -> bool:
    return len(set(names)) == len(names)


def main() -> None:
    required_edges = (
        ("u", "x"),
        ("p", "r"),
        ("q", "r"),
        ("p", "y"),
        ("q", "z"),
    )
    required_nonedges = (
        ("x", "p"),
        ("x", "q"),
        ("p", "q"),
        ("u", "r"),
        ("u", "y"),
        ("r", "y"),
        ("q", "y"),
        ("u", "z"),
        ("r", "z"),
        ("p", "z"),
    )
    present = sum(bit(*edge) for edge in required_edges)
    absent = sum(bit(*edge) for edge in required_nonedges)
    assert not present & absent

    row_counts = {"AQ0": 0, "QQ0": 0}
    first_mover_sets: dict[str, int] = {}
    named_completion_checks = 0
    direct_completion_checks = 0
    external_completion_checks = 0
    branch_checks = {"x": 0, "p": 0, "z": 0}

    for mask in range(1 << len(PAIRS)):
        if mask & present != present or mask & absent:
            continue

        row = "AQ0" if adjacent(mask, "x", "r") else "QQ0"
        row_counts[row] += 1

        # Collision-free labels stand for the seven vertices whose
        # distinctness is proved separately from the same incidences.
        assert all_distinct(*VERTICES)

        # Audit every possible collision of the independent-completion
        # vertex s with an already named vertex.  The completion for
        # {u,witness} may use s=t directly.  It can never use s=g because
        # witness--g is a private edge.  Every other allowed named s is
        # the unique possible responder at t from {x,witness,s}.
        for g, t, witness in (("p", "q", "y"), ("q", "p", "z")):
            assert not adjacent(mask, "u", witness)
            assert not adjacent(mask, t, witness)
            assert adjacent(mask, g, witness)
            for s in VERTICES:
                if s in {"u", witness}:
                    continue
                if adjacent(mask, "u", s) or adjacent(mask, witness, s):
                    continue
                named_completion_checks += 1
                assert s != g
                if s == t:
                    direct_completion_checks += 1
                    assert frozenset(("x", witness, s)) == frozenset(
                        ("x", witness, t)
                    )
                    continue
                external_completion_checks += 1
                source = frozenset(("x", witness, s))
                assert t not in source
                at_t = successors(mask, source, t)
                assert at_t == {
                    s: frozenset(("x", witness, t))
                }

        # The retained mixed state M_q={x,p,z} is attacked at y.  There
        # are exactly three possible guards, and p is always eligible.
        source = frozenset(("x", "p", "z"))
        assert "y" not in source
        first = successors(mask, source, "y")
        assert "p" in first
        key = "".join(sorted(first))
        first_mover_sets[key] = first_mover_sets.get(key, 0) + 1

        for mover, successor in first.items():
            branch_checks[mover] += 1
            if mover == "z":
                assert successor == frozenset(("x", "p", "y"))
                assert misses(mask, successor, "q")
            elif mover == "p":
                assert successor == frozenset(("x", "y", "z"))
                assert "u" not in successor
                at_u = successors(mask, successor, "u")
                terminal = frozenset(("u", "y", "z"))
                assert at_u == {"x": terminal}
                assert misses(mask, terminal, "r")
            elif mover == "x":
                assert successor == frozenset(("p", "y", "z"))
                assert "u" not in successor
                at_u = successors(mask, successor, "u")
                terminal = frozenset(("u", "y", "z"))
                assert set(at_u) <= {"p"}
                if at_u:
                    assert at_u == {"p": terminal}
                    assert misses(mask, terminal, "r")
            else:
                raise AssertionError(f"unexpected first mover {mover}")

    assert row_counts == {"AQ0": 32, "QQ0": 32}
    assert sum(row_counts.values()) == 64
    assert branch_checks == {"x": 32, "p": 64, "z": 32}

    result = {
        "schema": "rank-one-QQ0-AQ0-hostile-clean-room-v1",
        "verdict": "PASS",
        "enumeration": {
            "all_seven_vertex_graphs_scanned": 1 << len(PAIRS),
            "named_pairs": len(PAIRS),
            "hypothesis_assignments": sum(row_counts.values()),
            "row_counts": row_counts,
            "first_mover_sets": dict(sorted(first_mover_sets.items())),
            "branch_checks": branch_checks,
        },
        "completion_collision_audit": {
            "named_completion_checks": named_completion_checks,
            "direct_s_equals_t_checks": direct_completion_checks,
            "external_unique_response_checks": external_completion_checks,
            "s_equals_g_allowed": False,
        },
        "scope": (
            "Finite named-incidence and one-guard bookkeeping only; "
            "C-010, C-108, C-150, and greatest-family rank semantics "
            "were reviewed mathematically."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
