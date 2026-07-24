#!/usr/bin/env python3
"""Exact complement/minimum-degree cover of the global order-43 formula.

For a graph ``G`` of order 43 put

    mu(G) = min(delta(G), delta(complement(G)))
          = min(delta(G), 42 - Delta(G)).

Complementing if necessary and then relabelling a minimum-degree vertex to
vertex 0 gives one of three satisfiable cases:

* degree(0) = 18 and all degrees are in [18, 24];
* degree(0) = 19 and all degrees are in [19, 23];
* degree(0) = 20 and all degrees are in [20, 22].

The only remaining numerical case, ``mu(G) = 21``, would make G 21-regular.
That is impossible on 43 vertices by the handshake lemma.

The existing direct CNF already contains forward threshold counters for
degree range [18, 24].  A stricter bound can therefore be imposed by unit
assumptions on existing auxiliary threshold variables; no new counters or
clauses are needed.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Sequence

from direct_ramsey_cnf import (
    DirectRamseyInstance,
    SequentialCounter,
    build_direct_instance,
    variable_for_edge,
)


ORDER = 43
PRIMARY_VARIABLE_COUNT = math.comb(ORDER, 2)
BASE_DEGREE_LOWER = 18
BASE_DEGREE_UPPER = 24
BRANCH_DEGREES = (18, 19, 20)
ELIMINATED_DEGREE = 21
BASE_CNF_SHA256 = (
    "141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1"
)
BASE_METADATA_SHA256 = (
    "88906686b2554cf1b5b9051eae4a200b878944278ed91682b78d9f40d43cf70c"
)
CATALOG24_SHA256 = (
    "83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0"
)
CATALOG24_RECORD_COUNT = 352_366
SCHEMA = "ramsey55.global_minmax_degree_cover.v1"


def graph_degrees(adjacency: Sequence[int]) -> tuple[int, ...]:
    return tuple(neighbors.bit_count() for neighbors in adjacency)


def complement(adjacency: Sequence[int]) -> list[int]:
    order = len(adjacency)
    mask = (1 << order) - 1
    return [
        mask & ~(neighbors | (1 << vertex))
        for vertex, neighbors in enumerate(adjacency)
    ]


def relabel(adjacency: Sequence[int], old_order: Sequence[int]) -> list[int]:
    order = len(adjacency)
    if sorted(old_order) != list(range(order)):
        raise ValueError("old_order is not a permutation")
    result = [0] * order
    for new_left, old_left in enumerate(old_order):
        for new_right in range(new_left + 1, order):
            old_right = old_order[new_right]
            if (adjacency[old_left] >> old_right) & 1:
                result[new_left] |= 1 << new_right
                result[new_right] |= 1 << new_left
    return result


def minmax_parameter(degrees: Sequence[int], order: int = ORDER) -> int:
    if len(degrees) != order:
        raise ValueError("degree sequence has the wrong order")
    if not degrees:
        raise ValueError("degree sequence is empty")
    return min(min(degrees), order - 1 - max(degrees))


def normalize(adjacency: Sequence[int]) -> tuple[list[int], bool, int]:
    """Orient by complement, choose a minimum-degree vertex, and relabel.

    The returned graph has vertex 0 of degree ``branch`` and its neighbours
    occupy labels 1 through ``branch``.
    """

    if len(adjacency) != ORDER:
        raise ValueError(f"expected a graph of order {ORDER}")
    graph = list(adjacency)
    degrees = graph_degrees(graph)
    if any(not BASE_DEGREE_LOWER <= degree <= BASE_DEGREE_UPPER for degree in degrees):
        raise ValueError("graph does not satisfy the certified global degree bounds")

    original_min = min(degrees)
    complement_min = ORDER - 1 - max(degrees)
    complemented = complement_min < original_min
    if complemented:
        graph = complement(graph)
        degrees = graph_degrees(graph)

    branch = min(degrees)
    if branch == ELIMINATED_DEGREE:
        # This cannot occur for an actual simple graph: it would be
        # 21-regular on an odd number of vertices.
        raise AssertionError("handshake-parity case reached by a simple graph")
    if branch not in BRANCH_DEGREES:
        raise AssertionError(f"unexpected normalized branch degree {branch}")
    if max(degrees) > ORDER - 1 - branch:
        raise AssertionError("complement/minimum-degree interval was not enforced")

    root = degrees.index(branch)
    neighbors = [
        vertex
        for vertex in range(ORDER)
        if vertex != root and (graph[root] >> vertex) & 1
    ]
    nonneighbors = [
        vertex
        for vertex in range(ORDER)
        if vertex != root and not (graph[root] >> vertex) & 1
    ]
    normalized = relabel(graph, (root, *neighbors, *nonneighbors))
    if graph_degrees(normalized)[0] != branch:
        raise AssertionError("root relabelling changed its degree")
    return normalized, complemented, branch


def star_units(degree: int) -> tuple[int, ...]:
    """Fix vertex 0's neighbours to labels 1 through ``degree``."""

    if degree not in BRANCH_DEGREES:
        raise ValueError(f"degree must be one of {BRANCH_DEGREES}")
    return tuple(
        (
            variable_for_edge(ORDER, 0, other)
            if other <= degree
            else -variable_for_edge(ORDER, 0, other)
        )
        for other in range(1, ORDER)
    )


def _threshold_false_unit(
    counter: SequentialCounter, threshold: int
) -> int:
    """Return a unit saying the final count is strictly below threshold."""

    if threshold < 1 or not counter.rows:
        raise ValueError("counter has no requested threshold")
    final = counter.rows[-1]
    if threshold > len(final):
        raise ValueError("requested threshold exceeds the allocated counter")
    return -final[threshold - 1]


def direct_instance() -> DirectRamseyInstance:
    instance = build_direct_instance(ORDER)
    if (
        instance.degree_lower != BASE_DEGREE_LOWER
        or instance.degree_upper != BASE_DEGREE_UPPER
        or instance.primary_variable_count != PRIMARY_VARIABLE_COUNT
        or len(instance.counters) != 2 * ORDER
    ):
        raise AssertionError("unexpected direct-instance layout")
    return instance


def additional_degree_units(
    degree: int, instance: DirectRamseyInstance | None = None
) -> tuple[int, ...]:
    """Auxiliary units narrowing every degree to [degree, 42-degree]."""

    if degree not in BRANCH_DEGREES:
        raise ValueError(f"degree must be one of {BRANCH_DEGREES}")
    if degree == BASE_DEGREE_LOWER:
        return ()
    if instance is None:
        instance = direct_instance()
    threshold = ORDER - degree
    units: list[int] = []
    for vertex in range(ORDER):
        edge_counter = instance.counters[2 * vertex]
        nonedge_counter = instance.counters[2 * vertex + 1]
        if not edge_counter.label.startswith(f"vertex_{vertex}_edges_"):
            raise AssertionError("edge-counter ordering changed")
        if not nonedge_counter.label.startswith(f"vertex_{vertex}_nonedges_"):
            raise AssertionError("nonedge-counter ordering changed")
        units.append(_threshold_false_unit(edge_counter, threshold))
        units.append(_threshold_false_unit(nonedge_counter, threshold))
    if len(set(map(abs, units))) != 2 * ORDER:
        raise AssertionError("strict-bound units are not on distinct variables")
    return tuple(units)


def branch_units(
    degree: int, instance: DirectRamseyInstance | None = None
) -> tuple[int, ...]:
    return star_units(degree) + additional_degree_units(degree, instance)


def units_sha256(units: Sequence[int]) -> str:
    rendered = "".join(f"{literal} 0\n" for literal in units).encode("ascii")
    return hashlib.sha256(rendered).hexdigest()


def build_plan() -> dict[str, object]:
    instance = direct_instance()
    branches: list[dict[str, object]] = []
    for degree in BRANCH_DEGREES:
        star = star_units(degree)
        strict = additional_degree_units(degree, instance)
        all_units = star + strict
        branches.append(
            {
                "degree": degree,
                "degree_interval": [degree, ORDER - 1 - degree],
                "star_unit_count": len(star),
                "additional_degree_unit_count": len(strict),
                "total_assumption_count": len(all_units),
                "star_units_sha256": units_sha256(star),
                "additional_degree_units_sha256": units_sha256(strict),
                "all_units_sha256": units_sha256(all_units),
            }
        )
    return {
        "schema": SCHEMA,
        "status": "EXACT_COVER_PLAN_NO_SOLVE_CLAIM",
        "order": ORDER,
        "base_cnf_sha256": BASE_CNF_SHA256,
        "base_metadata_sha256": BASE_METADATA_SHA256,
        "base_variable_count": instance.variable_count,
        "base_clause_count": instance.clause_count,
        "base_primary_variable_count": instance.primary_variable_count,
        "base_degree_interval": [
            instance.degree_lower,
            instance.degree_upper,
        ],
        "cover_parameter": "min(delta(G),42-Delta(G))",
        "complement_and_relabel_equivalence": (
            "Every order-43 Ramsey(5,5) graph is isomorphic, after optional "
            "complementation, to a model of one listed branch."
        ),
        "branches": branches,
        "parity_elimination": {
            "parameter": ELIMINATED_DEGREE,
            "forced_degree_sequence": [ELIMINATED_DEGREE] * ORDER,
            "degree_sum": ORDER * ELIMINATED_DEGREE,
            "reason": (
                "mu=21 forces all 43 degrees to equal 21, but the degree "
                "sum 903 is odd, contradicting the handshake lemma"
            ),
        },
        "optional_degree18_catalog_split": {
            "scope": (
                "For degree 18, the complement of the induced graph on the "
                "24 nonneighbours of vertex 0 lies in R(4,5,24)."
            ),
            "catalog_sha256": CATALOG24_SHA256,
            "catalog_record_count": CATALOG24_RECORD_COUNT,
            "fixed_star_primary_variables": ORDER - 1,
            "fixed_antineighborhood_primary_variables": math.comb(24, 2),
            "remaining_primary_variables_per_catalog_cube": (
                PRIMARY_VARIABLE_COUNT - (ORDER - 1) - math.comb(24, 2)
            ),
            "claim_limit": (
                "This is an exact secondary split only when using the "
                "complete 352366-class R(4,5,24) catalog."
            ),
        },
        "claim_limit": (
            "This artifact certifies an exhaustive decomposition only. "
            "It contains no SAT model and no UNSAT certificate."
        ),
    }


def main() -> int:
    print(json.dumps(build_plan(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
