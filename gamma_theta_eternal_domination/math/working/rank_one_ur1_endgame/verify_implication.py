#!/usr/bin/env python3
"""Independent finite bookkeeping audit for rank-one ur=1 normalization.

This checker does not re-prove C-010, C-064, C-108, or C-150.  It checks
the proof's named incidence tables, collisions, one-guard successors,
unoccupied targets, independent ridge paths, composite permutations, and
terminal missed vertices using ordinary Python sets.
"""

from __future__ import annotations

import itertools
import json


def edge(left: str, right: str) -> frozenset[str]:
    assert left != right
    return frozenset((left, right))


def adjacent(edges: set[frozenset[str]], left: str, right: str) -> bool:
    return left != right and edge(left, right) in edges


def successor(state: frozenset[str], guard: str, target: str) -> frozenset[str]:
    assert guard in state
    assert target not in state
    return (state - {guard}) | {target}


def movers(
    edges: set[frozenset[str]], state: frozenset[str], target: str
) -> tuple[str, ...]:
    assert target not in state
    return tuple(sorted(guard for guard in state if adjacent(edges, guard, target)))


def misses(
    edges: set[frozenset[str]], state: frozenset[str], target: str
) -> bool:
    assert target not in state
    return not any(adjacent(edges, guard, target) for guard in state)


def independent(edges: set[frozenset[str]], state: frozenset[str]) -> bool:
    return all(
        not adjacent(edges, left, right)
        for left, right in itertools.combinations(state, 2)
    )


def transposition(left: str, right: str) -> dict[str, str]:
    return {left: right, right: left}


def apply(permutation: dict[str, str], vertex: str) -> str:
    return permutation.get(vertex, vertex)


def compose(
    after: dict[str, str], before: dict[str, str], universe: set[str]
) -> dict[str, str]:
    return {
        vertex: apply(after, apply(before, vertex))
        for vertex in universe
        if apply(after, apply(before, vertex)) != vertex
    }


def audit_ridge_path(
    edges: set[frozenset[str]],
    states: list[frozenset[str]],
    attack_targets: list[str],
    expected_movers: list[str],
    universe: set[str],
) -> dict[str, str]:
    assert len(states) == len(attack_targets) + 1
    permutation: dict[str, str] = {}
    for source, target_state, target, expected in zip(
        states, states[1:], attack_targets, expected_movers
    ):
        assert independent(edges, source)
        assert independent(edges, target_state)
        assert target not in source
        assert movers(edges, source, target) == (expected,)
        assert successor(source, expected, target) == target_state
        entering = next(iter(target_state - source))
        departing = next(iter(source - target_state))
        step = transposition(departing, entering)
        permutation = compose(step, permutation, universe)
    return permutation


def base_edges(case: str, *, collision: bool) -> set[frozenset[str]]:
    result = {
        edge("u", "x"),
        edge("u", "r"),
        edge("p", "r"),
        edge("q", "r"),
        edge("p", "b"),
        edge("q", "c"),
    }
    if case == "AQ1":
        result.add(edge("x", "r"))
        result.add(edge("u", "a"))
        result.add(edge("x", "a"))
    elif collision:
        # a is represented by x, so no loop is inserted.
        pass
    else:
        result.add(edge("u", "a"))
        result.add(edge("x", "a"))
    return result


def add_fresh_private_saturation(edges: set[frozenset[str]]) -> None:
    edges.update(
        {
            edge("a", "b"),
            edge("a", "c"),
            edge("x", "b"),
            edge("x", "c"),
            edge("b", "c"),
            edge("u", "p"),
            edge("u", "q"),
        }
    )


def audit_aq_marker_paths() -> int:
    universe = set("uxpqrabc")
    audited = 0

    # Retained b -> a branch under the counterassumption ac = 0.
    edges = base_edges("AQ1", collision=False)
    edges.add(edge("a", "b"))
    states = [
        frozenset(("r", "a", "c")),
        frozenset(("p", "a", "c")),
        frozenset(("p", "a", "q")),
        frozenset(("p", "x", "q")),
    ]
    permutation = audit_ridge_path(
        edges, states, ["p", "q", "x"], ["r", "c", "a"], universe
    )
    assert apply(permutation, "r") == "p"
    assert apply(permutation, "b") == "b"
    assert not adjacent(edges, "r", "b")
    audited += 1

    # Retained c -> a branch under the counterassumption ab = 0.
    edges = base_edges("AQ1", collision=False)
    edges.add(edge("a", "c"))
    states = [
        frozenset(("r", "a", "b")),
        frozenset(("q", "a", "b")),
        frozenset(("q", "a", "p")),
        frozenset(("q", "x", "p")),
    ]
    permutation = audit_ridge_path(
        edges, states, ["q", "p", "x"], ["r", "b", "a"], universe
    )
    assert apply(permutation, "r") == "q"
    assert apply(permutation, "c") == "c"
    assert not adjacent(edges, "r", "c")
    audited += 1
    return audited


def audit_qq_collision_markers() -> int:
    universe = set("uxpqrbca")
    audited = 0

    # Counterassumption xb = 0; closure at x from R forces c -> x.
    edges = base_edges("QQ1", collision=True)
    edges.add(edge("x", "c"))
    states = [
        frozenset(("r", "b", "x")),
        frozenset(("q", "b", "x")),
        frozenset(("q", "p", "x")),
    ]
    permutation = audit_ridge_path(
        edges, states, ["q", "p"], ["r", "b"], universe
    )
    assert apply(permutation, "r") == "q"
    assert apply(permutation, "c") == "c"
    assert not adjacent(edges, "r", "c")
    audited += 1

    # Counterassumption xc = 0; closure at x from R forces b -> x.
    edges = base_edges("QQ1", collision=True)
    edges.add(edge("x", "b"))
    states = [
        frozenset(("r", "c", "x")),
        frozenset(("p", "c", "x")),
        frozenset(("p", "q", "x")),
    ]
    permutation = audit_ridge_path(
        edges, states, ["p", "q"], ["r", "c"], universe
    )
    assert apply(permutation, "r") == "p"
    assert apply(permutation, "b") == "b"
    assert not adjacent(edges, "r", "b")
    audited += 1
    return audited


def audit_w_exclusion() -> dict[str, object]:
    # AQ1: every successor at a has a displayed missed named vertex.
    edges = base_edges("AQ1", collision=False)
    add_fresh_private_saturation(edges)
    w_state = frozenset(("x", "b", "c"))
    expected = {
        "x": ("r", frozenset(("a", "b", "c"))),
        "b": ("p", frozenset(("x", "a", "c"))),
        "c": ("q", frozenset(("x", "a", "b"))),
    }
    assert movers(edges, w_state, "a") == ("b", "c", "x")
    for guard, (missed, state) in expected.items():
        assert successor(w_state, guard, "a") == state
        assert misses(edges, state, missed)

    # QQ1 collision: x,b,c directly miss r.
    qq_edges = base_edges("QQ1", collision=True)
    qq_edges.update({edge("x", "b"), edge("x", "c"), edge("b", "c")})
    assert misses(qq_edges, w_state, "r")
    return {
        "AQ1_successors_checked": len(expected),
        "QQ1_direct_missed_vertex": "r",
    }


def audit_short_attack_trees() -> dict[str, int]:
    counts = {
        "AQ1_x_side_counterassumptions": 0,
        "side_witness_counterassumptions": 0,
        "reverse_side_counterassumptions": 0,
    }

    # AQ1: once ab and ac are present, xb = 0 leaves only the W successor
    # and a successor missing q.  Enumerate the optional bc edge.
    for absent_guard, root, target, other_guard, missed in (
        ("b", frozenset(("x", "p", "c")), "b", "c", "q"),
        ("c", frozenset(("x", "b", "q")), "c", "b", "p"),
    ):
        for side_edge in (False, True):
            edges = base_edges("AQ1", collision=False)
            edges.update({edge("a", "b"), edge("a", "c")})
            if side_edge:
                edges.add(edge("b", "c"))
            if absent_guard == "b":
                eligible = movers(edges, root, target)
                assert "p" in eligible and "x" not in eligible
                if "c" in eligible:
                    assert misses(
                        edges, successor(root, "c", target), missed
                    )
            else:
                eligible = movers(edges, root, target)
                assert "q" in eligible and "x" not in eligible
                if "b" in eligible:
                    assert misses(
                        edges, successor(root, "b", target), missed
                    )
            counts["AQ1_x_side_counterassumptions"] += 1

    # If bc = 0, U is independent and its active u -> x successor is W.
    for case in ("QQ1", "AQ1"):
        edges = base_edges(case, collision=(case == "QQ1"))
        if case == "AQ1":
            edges.update(
                {
                    edge("a", "b"),
                    edge("a", "c"),
                    edge("x", "b"),
                    edge("x", "c"),
                }
            )
        else:
            edges.update({edge("x", "b"), edge("x", "c")})
        u_state = frozenset(("u", "b", "c"))
        assert independent(edges, u_state)
        assert successor(u_state, "u", "x") == frozenset(("x", "b", "c"))
        counts["side_witness_counterassumptions"] += 1

    # If up = 0, all b-attack successors from Mq are excluded.  The
    # uq = 0 proof is symmetric.
    for case in ("QQ1", "AQ1"):
        collision = case == "QQ1"
        edges = base_edges(case, collision=collision)
        if collision:
            edges.update(
                {
                    edge("x", "b"),
                    edge("x", "c"),
                    edge("b", "c"),
                    edge("u", "q"),
                }
            )
        else:
            add_fresh_private_saturation(edges)
            edges.discard(edge("u", "p"))
        root = frozenset(("x", "p", "c"))
        assert movers(edges, root, "b") == ("c", "p", "x")
        assert misses(edges, successor(root, "x", "b"), "u")
        assert successor(root, "p", "b") == frozenset(("x", "b", "c"))
        assert misses(edges, successor(root, "c", "b"), "q")
        counts["reverse_side_counterassumptions"] += 1
    return counts


def audit_new_activity() -> int:
    # Enumerate every optional combination of s-a and s-q.  The s and b
    # successors at target a are always excluded, leaving x -> a.
    audited = 0
    for sa, sq in itertools.product((False, True), repeat=2):
        edges = base_edges("AQ1", collision=False)
        add_fresh_private_saturation(edges)
        if sa:
            edges.add(edge("s", "a"))
        if sq:
            edges.add(edge("s", "q"))
        j_state = frozenset(("x", "b", "s"))
        target = "a"
        eligible = set(movers(edges, j_state, target))
        assert {"x", "b"} <= eligible
        if sa:
            s_successor = successor(j_state, "s", target)
            assert misses(edges, s_successor, "q")
        b_successor = successor(j_state, "b", target)
        if sq:
            assert movers(edges, b_successor, "q") == ("s",)
            terminal = successor(b_successor, "s", "q")
            assert misses(edges, terminal, "p")
        else:
            assert misses(edges, b_successor, "q")
        assert successor(j_state, "x", target) == frozenset(("a", "b", "s"))
        audited += 1
    return audited


def audit_completion_paths() -> int:
    universe = set("uxpqrbcd")
    audited = 0
    edges = {
        edge("p", "r"),
        edge("q", "r"),
        edge("p", "b"),
        edge("q", "c"),
    }

    # d hits p only.
    p_only = set(edges)
    p_only.add(edge("d", "p"))
    states = [
        frozenset(("a", "p", "q")),
        frozenset(("a", "d", "q")),
        frozenset(("a", "d", "r")),
    ]
    permutation = audit_ridge_path(
        p_only, states, ["d", "r"], ["p", "q"], universe
    )
    assert apply(permutation, "q") == "r"
    assert apply(permutation, "c") == "c"
    assert not adjacent(p_only, "r", "c")
    audited += 1

    # d hits q only.
    q_only = set(edges)
    q_only.add(edge("d", "q"))
    states = [
        frozenset(("a", "p", "q")),
        frozenset(("a", "p", "d")),
        frozenset(("a", "r", "d")),
    ]
    permutation = audit_ridge_path(
        q_only, states, ["d", "r"], ["q", "p"], universe
    )
    assert apply(permutation, "p") == "r"
    assert apply(permutation, "b") == "b"
    assert not adjacent(q_only, "r", "b")
    audited += 1
    return audited


def complement_core() -> dict[str, object]:
    vertices = ("u", "x", "p", "q", "r", "b", "c")
    g_edges = {
        edge("u", "x"),
        edge("u", "p"),
        edge("u", "q"),
        edge("u", "r"),
        edge("p", "r"),
        edge("q", "r"),
        edge("p", "b"),
        edge("q", "c"),
        edge("x", "b"),
        edge("x", "c"),
        edge("b", "c"),
    }
    h_edges = {
        edge(left, right)
        for left, right in itertools.combinations(vertices, 2)
        if edge(left, right) not in g_edges
    }
    expected = {
        edge("x", "p"),
        edge("x", "q"),
        edge("p", "q"),
        edge("x", "r"),
        edge("r", "b"),
        edge("b", "u"),
        edge("u", "c"),
        edge("c", "r"),
        edge("p", "c"),
        edge("q", "b"),
    }
    assert h_edges == expected
    nonroot = expected - {edge("x", "p"), edge("x", "q"), edge("p", "q")}
    for candidate in nonroot:
        left, right = tuple(candidate)
        common = [
            vertex
            for vertex in vertices
            if vertex not in candidate
            and edge(left, vertex) in h_edges
            and edge(right, vertex) in h_edges
        ]
        assert common == []
    return {
        "vertices": list(vertices),
        "H_edges": sorted(sorted(item) for item in h_edges),
        "root_triangle": ["xp", "xq", "pq"],
        "bottom_cycle": ["rb", "bu", "uc", "cr"],
        "matching_spokes": ["xr", "pc", "qb"],
        "nonroot_edges_without_core_triangle": len(nonroot),
    }


def main() -> None:
    result = {
        "schema": "rank-one-ur1-normalization-audit-v1",
        "scope": (
            "Finite bookkeeping audit only; accepted C-010/C-064/C-108/"
            "C-150 remain dependencies."
        ),
        "AQ1_marker_paths": audit_aq_marker_paths(),
        "QQ1_collision_marker_paths": audit_qq_collision_markers(),
        "W_exclusion": audit_w_exclusion(),
        "short_attack_trees": audit_short_attack_trees(),
        "new_activity_optional_assignments": audit_new_activity(),
        "completion_marker_paths": audit_completion_paths(),
        "complement_core": complement_core(),
        "verdict": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
