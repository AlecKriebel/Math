#!/usr/bin/env python3
"""Independent finite bookkeeping audit for the rank-one XQ1 proof.

The script does not re-prove C-064 or C-150.  It independently checks the
complete named pair partition, every named collision used in the proof, the
three ridge transpositions, the transported response singleton, the six
retained grid states, and both possible completion cases s=q and s external.
"""

from __future__ import annotations

import hashlib
import itertools
import json


NAMED = ("u", "x", "p", "q", "r", "y", "z")

FIXED_EDGES = {
    frozenset(pair)
    for pair in (
        ("u", "x"),
        ("u", "r"),
        ("u", "z"),
        ("x", "r"),
        ("x", "y"),
        ("x", "z"),
        ("p", "r"),
        ("p", "y"),
        ("y", "z"),
    )
}

FIXED_NONEDGES = {
    frozenset(pair)
    for pair in (
        ("u", "y"),
        ("x", "p"),
        ("x", "q"),
        ("p", "q"),
        ("p", "z"),
        ("q", "r"),
        ("q", "y"),
        ("q", "z"),
        ("r", "y"),
        ("r", "z"),
    )
}

OPTIONAL = {
    frozenset(("u", "p")),
    frozenset(("u", "q")),
}


def state(*vertices: str) -> frozenset[str]:
    return frozenset(vertices)


def apply_transposition(
    vertices: frozenset[str], left: str, right: str
) -> frozenset[str]:
    def image(vertex: str) -> str:
        if vertex == left:
            return right
        if vertex == right:
            return left
        return vertex

    return frozenset(image(vertex) for vertex in vertices)


def adjacent(
    left: str,
    right: str,
    optional_edges: set[frozenset[str]],
) -> bool:
    pair = frozenset((left, right))
    if pair in FIXED_EDGES:
        return True
    if pair in FIXED_NONEDGES:
        return False
    if pair in OPTIONAL:
        return pair in optional_edges
    raise AssertionError(f"unclassified named pair {left}-{right}")


def main() -> None:
    all_pairs = {
        frozenset(pair) for pair in itertools.combinations(NAMED, 2)
    }
    assert not (FIXED_EDGES & FIXED_NONEDGES)
    assert not (FIXED_EDGES & OPTIONAL)
    assert not (FIXED_NONEDGES & OPTIONAL)
    assert FIXED_EDGES | FIXED_NONEDGES | OPTIONAL == all_pairs

    j_y = state("y", "r", "q")
    j_z = state("z", "r", "q")
    k_z = state("z", "p", "q")
    t = state("x", "p", "q")
    ladder = (j_y, j_z, k_z, t)
    swaps = (("y", "z"), ("r", "p"), ("z", "x"))
    for before, after, swap in zip(ladder, ladder[1:], swaps):
        assert apply_transposition(before, *swap) == after

    # The starting list is physical and exact at J_z: r,y and q,y are
    # nonedges, while z,y is an edge and J_y is retained.
    first_eligible = {
        guard
        for guard in j_z
        if frozenset((guard, "y")) in FIXED_EDGES
    }
    assert first_eligible == {"z"}

    transported_target = state("y")
    transported_list = state("z")
    covariance_trace = []
    for source, target_state, (left, right) in zip(
        ladder[1:], ladder[2:], swaps[1:]
    ):
        next_target = apply_transposition(
            transported_target, left, right
        )
        next_list = apply_transposition(transported_list, left, right)
        covariance_trace.append(
            {
                "source": sorted(source),
                "target_state": sorted(target_state),
                "swap": [left, right],
                "attack_before": next(iter(transported_target)),
                "list_before": sorted(transported_list),
                "attack_after": next(iter(next_target)),
                "list_after": sorted(next_list),
            }
        )
        transported_target = next_target
        transported_list = next_list
    assert transported_target == {"y"}
    assert transported_list == {"x"}

    omitted = state("x", "y", "q")
    retained_grid = {
        state("x", "p", "q"),
        state("x", "r", "q"),
        state("y", "p", "q"),
        state("y", "r", "q"),
        state("z", "p", "q"),
        state("z", "r", "q"),
    }
    assert omitted not in retained_grid
    assert t - {"p"} | {"y"} == omitted
    assert t - {"x"} | {"y"} == state("y", "p", "q")

    collision_rows = []
    optional_pairs = sorted(
        OPTIONAL, key=lambda pair: tuple(sorted(pair))
    )
    for mask in range(1 << len(optional_pairs)):
        optional_edges = {
            pair
            for index, pair in enumerate(optional_pairs)
            if mask >> index & 1
        }
        named_completions = [
            candidate
            for candidate in NAMED
            if candidate not in ("u", "y")
            and not adjacent("u", candidate, optional_edges)
            and not adjacent("y", candidate, optional_edges)
        ]
        expected = [] if adjacent("u", "q", optional_edges) else ["q"]
        assert named_completions == expected

        # In the external case, x and y miss q.  Domination forces sq,
        # making s the unique eligible mover at the unoccupied attack q.
        external_source = state("x", "y", "s")
        external_eligible = {
            guard
            for guard in external_source
            if (
                guard == "s"
                or frozenset((guard, "q")) in FIXED_EDGES
            )
        }
        assert "q" not in external_source
        assert external_eligible == {"s"}
        assert external_source - {"s"} | {"q"} == omitted

        # In the only named collision, s=q, the active successor is
        # already the omitted state.
        assert state("x", "y", "q") == omitted
        collision_rows.append(
            {
                "optional_edge_mask": mask,
                "optional_edges": [
                    sorted(pair) for pair in sorted(
                        optional_edges, key=lambda pair: tuple(sorted(pair))
                    )
                ],
                "named_completion_candidates": named_completions,
                "external_unique_mover_at_q": "s",
            }
        )

    result = {
        "schema": "rank-one-XQ1-implication-audit-v1",
        "verdict": "PASS",
        "named_vertices": list(NAMED),
        "pair_partition": {
            "fixed_edges": sorted(
                (sorted(pair) for pair in FIXED_EDGES)
            ),
            "fixed_nonedges": sorted(
                (sorted(pair) for pair in FIXED_NONEDGES)
            ),
            "optional_pairs": sorted(
                (sorted(pair) for pair in OPTIONAL)
            ),
            "counts": {
                "fixed_edges": len(FIXED_EDGES),
                "fixed_nonedges": len(FIXED_NONEDGES),
                "optional_pairs": len(OPTIONAL),
                "total": len(all_pairs),
            },
        },
        "ladder": [sorted(facet) for facet in ladder],
        "covariance_trace": covariance_trace,
        "transported_exact_list": {
            "base": sorted(t),
            "attack": "y",
            "list": ["x"],
        },
        "omitted_state": sorted(omitted),
        "retained_grid": sorted(sorted(grid_state) for grid_state in retained_grid),
        "completion_collision_rows": collision_rows,
        "scope": (
            "Finite bookkeeping audit of the symbolic proof; accepted "
            "C-064 covariance and C-150 ladder are dependencies."
        ),
    }
    canonical = json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    result["sha256_without_this_field"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
