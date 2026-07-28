#!/usr/bin/env python3
"""Independent finite bookkeeping audit for the rank-one QQ0/AQ0 proof.

This script does not search for a graph and does not re-prove C-010,
C-108, or C-150.  It enumerates every optional named graph edge and
checks the literal one-guard attacks in the symbolic contradiction.
"""

from __future__ import annotations

import itertools
import json


VERTICES = ("u", "x", "p", "q", "r", "y", "z")
ROWS = {
    "QQ0": False,  # xr is absent
    "AQ0": True,   # xr is present
}
OPTIONAL = (("u", "p"), ("u", "q"), ("x", "y"), ("x", "z"), ("y", "z"))


def pair(left: str, right: str) -> tuple[str, str]:
    assert left != right
    return tuple(sorted((left, right)))  # type: ignore[return-value]


def state(*vertices: str) -> frozenset[str]:
    result = frozenset(vertices)
    assert len(result) == 3
    return result


def build_edges(row: str, bits: tuple[bool, ...]) -> set[tuple[str, str]]:
    edges = {
        pair("u", "x"),
        pair("p", "r"),
        pair("q", "r"),
        pair("p", "y"),
        pair("q", "z"),
    }
    if ROWS[row]:
        edges.add(pair("x", "r"))
    for names, present in zip(OPTIONAL, bits, strict=True):
        if present:
            edges.add(pair(*names))
    return edges


def adjacent(
    edges: set[tuple[str, str]], left: str, right: str
) -> bool:
    return pair(left, right) in edges


def successors(
    edges: set[tuple[str, str]],
    source: frozenset[str],
    target: str,
) -> dict[str, frozenset[str]]:
    assert target not in source
    return {
        guard: (source - {guard}) | {target}
        for guard in sorted(source)
        if adjacent(edges, guard, target)
    }


def missed_by(
    edges: set[tuple[str, str]],
    guards: frozenset[str],
    target: str,
) -> bool:
    assert target not in guards
    return all(not adjacent(edges, guard, target) for guard in guards)


def main() -> None:
    forced_nonedges = {
        pair("x", "p"),
        pair("x", "q"),
        pair("p", "q"),
        pair("u", "r"),
        pair("u", "y"),
        pair("r", "y"),
        pair("q", "y"),
        pair("u", "z"),
        pair("r", "z"),
        pair("p", "z"),
    }

    assignment_count = 0
    original_attack_successors = 0
    original_attack_histogram = {"1": 0, "2": 0, "3": 0}
    x_branch_count = 0
    z_branch_count = 0
    x_branch_no_u_response = 0
    x_branch_terminal_response = 0

    # Symbolic audit of both branches of the private-witness transfer.
    # The direct completion has s=t.  In the external branch, x and y_g
    # miss t while the retained state dominates t, forcing the unique
    # edge s--t and the one-guard move s->t.
    transfer_branches = []
    for g, t, witness in (("p", "q", "y"), ("q", "p", "z")):
        direct = state("x", witness, t)
        expected = state(*({"x", "p", "q"} - {g}), witness)
        assert direct == expected
        transfer_branches.append((g, "direct"))

        external_edges = {pair("s", t)}
        external_source = state("x", witness, "s")
        external_successors = successors(external_edges, external_source, t)
        assert external_successors == {"s": expected}
        transfer_branches.append((g, "external_unique_attack"))

    for row in ROWS:
        for bits in itertools.product((False, True), repeat=len(OPTIONAL)):
            edges = build_edges(row, bits)
            assert not (edges & forced_nonedges)
            assignment_count += 1

            m_q = state("x", "p", "z")
            assert "y" not in m_q
            first = successors(edges, m_q, "y")
            assert "p" in first
            assert set(first) <= {"x", "p", "z"}
            original_attack_successors += len(first)
            original_attack_histogram[str(len(first))] += 1

            # z->y, when eligible, gives A={x,p,y}, which misses q.
            if "z" in first:
                z_branch_count += 1
                assert first["z"] == state("x", "p", "y")
                assert missed_by(edges, first["z"], "q")

            # p->y gives W={x,y,z}.  At u only x can move, and its
            # successor H={u,y,z} misses r.
            w_state = first["p"]
            assert w_state == state("x", "y", "z")
            w_at_u = successors(edges, w_state, "u")
            h_state = state("u", "y", "z")
            assert w_at_u == {"x": h_state}
            assert missed_by(edges, h_state, "r")

            # x->y, when eligible, gives X={p,y,z}.  At u there is
            # either no mover or only p, again landing in H.
            if "x" in first:
                x_branch_count += 1
                x_state = first["x"]
                assert x_state == state("p", "y", "z")
                x_at_u = successors(edges, x_state, "u")
                assert set(x_at_u) <= {"p"}
                if x_at_u:
                    x_branch_terminal_response += 1
                    assert x_at_u == {"p": h_state}
                else:
                    x_branch_no_u_response += 1

            # Every eligible first successor is now excluded by one of
            # the three literal certificates above.
            assert set(first) == (
                {"p"}
                | ({"x"} if adjacent(edges, "x", "y") else set())
                | ({"z"} if adjacent(edges, "z", "y") else set())
            )

    result = {
        "schema": "rank-one-QQ0-AQ0-implication-audit-v1",
        "classification": "FINITE_BOOKKEEPING_AUDIT_OF_SYMBOLIC_PROOF",
        "rows": sorted(ROWS),
        "optional_pairs": ["".join(names) for names in OPTIONAL],
        "assignments_checked": assignment_count,
        "transfer_branches_checked": [list(item) for item in transfer_branches],
        "original_attack_successors_checked": original_attack_successors,
        "original_attack_successor_count_histogram": original_attack_histogram,
        "conditional_z_branches_checked": z_branch_count,
        "conditional_x_branches_checked": x_branch_count,
        "x_branch_no_u_response": x_branch_no_u_response,
        "x_branch_terminal_response": x_branch_terminal_response,
        "common_terminal_state": sorted(state("u", "y", "z")),
        "common_terminal_missed_vertex": "r",
        "verdict": "PASS",
        "scope": (
            "Checks named incidence, collision-free set operations, "
            "unoccupied targets, and one-guard successors only; accepted "
            "C-010/C-108/C-150 remain dependencies."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
