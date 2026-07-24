#!/usr/bin/env python3
"""Independent in-memory audit of the order-3 maximal-cycle search formula."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from collections import Counter
from pathlib import Path


AUDIT_ID = "ramsey55_order3_maxcycle_independent_audit_v1"
N = 43
P = 3
MOVED_CYCLES = 14
FIXED_VERTEX = 42
EXPECTED_VARIABLES = 301
EXPECTED_SIGNATURES = 320_593
EXPECTED_CLAUSES = 641_186
EXPECTED_DIMACS_SHA256 = (
    "2cb249c2d09d00bd199be27711fc344873785b9e9756dc1cafad8f756084a5e5"
)
EXPECTED_SIGNATURE_HISTOGRAM = Counter(
    {5: 91, 6: 182, 7: 91, 8: 3_276, 9: 19_656, 10: 297_297}
)
EXPECTED_SIDE_COUNTS = {
    6: {"variables": 51, "four_signatures": 990, "five_signatures": 2_841},
    7: {"variables": 70, "four_signatures": 1_953, "five_signatures": 6_762},
    8: {"variables": 92, "four_signatures": 3_486, "five_signatures": 14_140},
}


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def shifted_vertex(vertex: int, shift: int, moved_order: int) -> int:
    if vertex >= moved_order:
        return vertex
    cycle, phase = divmod(vertex, P)
    return P * cycle + (phase + shift) % P


def independent_edge_partition(
    order: int, cycle_count: int
) -> tuple[
    dict[tuple[int, int], int],
    tuple[tuple[tuple[int, int], ...], ...],
]:
    """Build each orbit algebraically from all three group elements."""
    moved_order = P * cycle_count
    if order not in (moved_order, moved_order + 1):
        raise ValueError("expected 3*c moved vertices and at most one fixed point")
    representative_of: dict[tuple[int, int], tuple[int, int]] = {}
    orbit_by_representative: dict[
        tuple[int, int], tuple[tuple[int, int], ...]
    ] = {}
    for edge in itertools.combinations(range(order), 2):
        orbit = tuple(
            sorted(
                {
                    tuple(
                        sorted(
                            (
                                shifted_vertex(edge[0], shift, moved_order),
                                shifted_vertex(edge[1], shift, moved_order),
                            )
                        )
                    )
                    for shift in range(P)
                }
            )
        )
        representative = orbit[0]
        representative_of[edge] = representative
        previous = orbit_by_representative.setdefault(representative, orbit)
        if previous != orbit:
            raise AssertionError("representative collision between distinct orbits")
    representatives = sorted(orbit_by_representative)
    variable_of = {
        representative: variable
        for variable, representative in enumerate(representatives, start=1)
    }
    table = {
        edge: variable_of[representative]
        for edge, representative in representative_of.items()
    }
    orbits = tuple(orbit_by_representative[rep] for rep in representatives)
    if len(table) != math.comb(order, 2):
        raise AssertionError("edge table is incomplete")
    return table, orbits


def signatures(
    order: int, size: int, edge_variable: dict[tuple[int, int], int]
) -> tuple[tuple[int, ...], ...]:
    patterns: set[tuple[int, ...]] = set()
    for vertices in itertools.combinations(range(order), size):
        variables: set[int] = set()
        for left_offset in range(size):
            for right_offset in range(left_offset + 1, size):
                variables.add(
                    edge_variable[
                        (vertices[left_offset], vertices[right_offset])
                    ]
                )
        patterns.add(tuple(sorted(variables)))
    return tuple(sorted(patterns))


def dimacs_hash(
    variable_count: int, five_signatures: tuple[tuple[int, ...], ...]
) -> str:
    state = hashlib.sha256()
    state.update(
        f"p cnf {variable_count} {2 * len(five_signatures)}\n".encode("ascii")
    )
    for signature in five_signatures:
        positive = " ".join(str(variable) for variable in signature) + " 0\n"
        negative = " ".join(str(-variable) for variable in signature) + " 0\n"
        state.update(positive.encode("ascii"))
        state.update(negative.encode("ascii"))
    return state.hexdigest()


def audit(search_source: Path) -> dict[str, object]:
    started = time.monotonic()
    edge_variable, orbits = independent_edge_partition(N, MOVED_CYCLES)
    five_signatures = signatures(N, 5, edge_variable)
    formula_sha256 = dimacs_hash(len(orbits), five_signatures)
    orbit_histogram = Counter(map(len, orbits))
    signature_histogram = Counter(map(len, five_signatures))
    incident_variables = [
        edge_variable[(P * cycle, FIXED_VERTEX)]
        for cycle in range(MOVED_CYCLES)
    ]
    side_results: dict[int, dict[str, object]] = {}
    side_valid = True
    for cycle_count, expected in EXPECTED_SIDE_COUNTS.items():
        side_order = P * cycle_count
        side_table, side_orbits = independent_edge_partition(
            side_order, cycle_count
        )
        four_signatures = signatures(side_order, 4, side_table)
        local_five_signatures = signatures(side_order, 5, side_table)
        observed = {
            "variables": len(side_orbits),
            "four_signatures": len(four_signatures),
            "five_signatures": len(local_five_signatures),
        }
        valid = observed == expected
        side_valid &= valid
        side_results[cycle_count] = {
            **observed,
            "expected": expected,
            "valid": valid,
            "orbit_size_histogram": dict(
                sorted(Counter(map(len, side_orbits)).items())
            ),
        }

    # R(4,5)=25 bounds the fixed degree to 18..24.  It is a multiple
    # of three, so only 18,21,24 occur.  Complementation sends d to 42-d.
    allowed_degrees = [
        degree for degree in range(18, 25) if degree % P == 0
    ]
    allowed_t = [degree // P for degree in allowed_degrees]
    complement_map = {
        t_case: (N - 1) // P - t_case for t_case in allowed_t
    }
    normalization_valid = (
        allowed_degrees == [18, 21, 24]
        and allowed_t == [6, 7, 8]
        and complement_map == {6: 8, 7: 7, 8: 6}
        and len(set(incident_variables)) == MOVED_CYCLES
    )
    fixed_counts = {}
    for t_case in (6, 7):
        side_a_variables = EXPECTED_SIDE_COUNTS[t_case]["variables"]
        side_b_variables = EXPECTED_SIDE_COUNTS[MOVED_CYCLES - t_case][
            "variables"
        ]
        fixed = MOVED_CYCLES + side_a_variables + side_b_variables
        free = EXPECTED_VARIABLES - fixed
        expected_free = 3 * t_case * (MOVED_CYCLES - t_case)
        valid = free == expected_free
        normalization_valid &= valid
        fixed_counts[t_case] = {
            "fixed_variables": fixed,
            "free_cross_variables": free,
            "expected_cross_variables": expected_free,
            "valid": valid,
        }

    formula_valid = (
        len(edge_variable) == math.comb(N, 2)
        and len(orbits) == EXPECTED_VARIABLES
        and orbit_histogram == Counter({P: EXPECTED_VARIABLES})
        and len(five_signatures) == EXPECTED_SIGNATURES
        and 2 * len(five_signatures) == EXPECTED_CLAUSES
        and signature_histogram == EXPECTED_SIGNATURE_HISTOGRAM
        and formula_sha256 == EXPECTED_DIMACS_SHA256
    )
    valid = formula_valid and normalization_valid and side_valid
    return {
        "audit": AUDIT_ID,
        "valid": valid,
        "formula_valid": formula_valid,
        "normalization_valid": normalization_valid,
        "side_formulas_valid": side_valid,
        "cycle_type": "3^14 1^1",
        "order": N,
        "edge_count": len(edge_variable),
        "variable_count": len(orbits),
        "edge_orbit_size_histogram": dict(sorted(orbit_histogram.items())),
        "unique_signature_count": len(five_signatures),
        "clause_count": 2 * len(five_signatures),
        "signature_size_histogram": dict(sorted(signature_histogram.items())),
        "dimacs_sha256_without_materialization": formula_sha256,
        "fixed_vertex_incident_variables": incident_variables,
        "degree_reduction": {
            "degree_bound_from_R_4_5_equals_25": [18, 24],
            "allowed_degrees": allowed_degrees,
            "allowed_neighbor_cycle_counts": allowed_t,
            "complement_map": complement_map,
            "searched_representatives": [6, 7],
            "cycle_relabeling_group": "S14",
        },
        "gluing_variable_counts": fixed_counts,
        "side_formulas": side_results,
        "search_source": str(search_source.resolve()),
        "search_source_sha256": sha256_file(search_source),
        "runtime_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--search-source",
        type=Path,
        default=Path("src/automorphism3_maxcycle_search.py"),
    )
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.search_source)
    args.result.parent.mkdir(parents=True, exist_ok=True)
    if args.result.exists():
        raise FileExistsError(f"refusing to overwrite {args.result}")
    args.result.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
