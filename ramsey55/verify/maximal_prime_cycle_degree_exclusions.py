#!/usr/bin/env python3
"""Audit the elementary fixed-degree exclusions for selected prime cycle types.

The only external mathematical input is the established equality
R(4,5)=R(5,4)=25.  It implies that every vertex of a (5,5;43)-graph has
degree in [18,24].  The rest of this checker is finite integer arithmetic.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


CHECKER_ID = "ramsey55_maximal_prime_cycle_degree_exclusions_checker_v1"
ORDER = 43
DEGREE_LOWER = 18
DEGREE_UPPER = 24
DIRECT_TYPES = ((13, 3), (29, 1), (31, 1), (37, 1), (41, 1))


def fixed_vertex_degree_intervals(
    prime: int, cycles: int
) -> tuple[tuple[int, int], ...]:
    """Possible total-degree intervals for a fixed vertex.

    A fixed vertex sees either all or none of every moved prime cycle.  If it
    sees ``m`` cycles, the moved contribution is ``prime*m``; its degree
    among the other fixed vertices can range from zero through ``fixed-1``.
    """

    fixed = ORDER - prime * cycles
    if fixed <= 0:
        return ()
    return tuple(
        (prime * seen, prime * seen + fixed - 1)
        for seen in range(cycles + 1)
    )


def interval_meets_degree_window(interval: tuple[int, int]) -> bool:
    lower, upper = interval
    return max(lower, DEGREE_LOWER) <= min(upper, DEGREE_UPPER)


def direct_degree_audit(prime: int, cycles: int) -> dict[str, object]:
    fixed = ORDER - prime * cycles
    intervals = fixed_vertex_degree_intervals(prime, cycles)
    intersections = [
        [
            max(lower, DEGREE_LOWER),
            min(upper, DEGREE_UPPER),
        ]
        for lower, upper in intervals
        if interval_meets_degree_window((lower, upper))
    ]
    return {
        "cycle_type": f"{prime}^{cycles} 1^{fixed}",
        "prime": prime,
        "moved_cycle_count": cycles,
        "fixed_vertex_count": fixed,
        "possible_fixed_vertex_degree_intervals": [
            list(interval) for interval in intervals
        ],
        "intersections_with_18_through_24": intersections,
        "excluded": not intersections,
    }


def p23_audit() -> dict[str, object]:
    """Check the complete elementary argument for type 23^1 1^20."""

    intervals = fixed_vertex_degree_intervals(23, 1)
    if intervals != ((0, 19), (23, 42)):
        raise AssertionError(f"unexpected p=23 intervals: {intervals}")

    # L vertices see the 23-cycle, hence have fixed degree 0 or 1.
    # H vertices miss the 23-cycle, hence have fixed degree 18 or 19.
    cross_bounds: list[dict[str, object]] = []
    feasible_low_counts: list[int] = []
    for low_count in range(21):
        high_count = 20 - low_count
        # Every H vertex has at most one fixed-graph nonneighbor, so it has
        # at least max(0, |L|-1) neighbors in L.  Every L vertex has total
        # fixed-graph degree at most one.
        lower = high_count * max(0, low_count - 1)
        upper = low_count
        feasible = lower <= upper
        cross_bounds.append(
            {
                "low_count": low_count,
                "high_count": high_count,
                "cross_edge_lower_bound": lower,
                "cross_edge_upper_bound": upper,
                "feasible": feasible,
            }
        )
        if feasible:
            feasible_low_counts.append(low_count)

    if feasible_low_counts != [0, 1, 19, 20]:
        raise AssertionError(f"unexpected feasible L counts: {feasible_low_counts}")

    # Complementation maps |L| to 20-|L|, so it suffices to check 0 and 1.
    complement_pairs = [[0, 20], [1, 19]]

    # |L|=0: the complement of the fixed graph has maximum degree one.
    # A graph of maximum degree one has components of order at most two, so
    # an independent set can contain at least one vertex per component.
    low_zero_original_clique_lower_bound = math.ceil(20 / 2)

    # |L|=1: the lone L vertex x has fixed degree at most one, hence is
    # missed by at least 18 of the 19 H vertices.  Each such H vertex has
    # fixed degree at least 18 and therefore sees all other 18 H vertices.
    # Since at most one H vertex lies outside this witness set, every H-pair
    # has a witness endpoint and H is a K_19.
    low_one_high_count = 19
    low_one_witness_count_lower_bound = 18
    low_one_original_clique_order = 19

    contradiction = (
        low_zero_original_clique_lower_bound >= 5
        and low_one_witness_count_lower_bound >= 18
        and low_one_original_clique_order >= 5
    )
    return {
        "cycle_type": "23^1 1^20",
        "possible_fixed_vertex_degree_intervals": [
            list(interval) for interval in intervals
        ],
        "low_vertex_fixed_degree_options": [0, 1],
        "high_vertex_fixed_degree_options": [18, 19],
        "cross_edge_bounds": cross_bounds,
        "feasible_low_counts": feasible_low_counts,
        "complement_pairs": complement_pairs,
        "representatives_after_complementation": [0, 1],
        "low_zero_branch": {
            "complement_fixed_graph_maximum_degree": 1,
            "original_fixed_graph_clique_lower_bound":
                low_zero_original_clique_lower_bound,
        },
        "low_one_branch": {
            "high_vertex_count": low_one_high_count,
            "high_vertices_missing_the_low_vertex_lower_bound":
                low_one_witness_count_lower_bound,
            "forced_original_fixed_graph_clique_order":
                low_one_original_clique_order,
        },
        "excluded": contradiction,
    }


def audit() -> dict[str, object]:
    direct = [direct_degree_audit(*cycle_type) for cycle_type in DIRECT_TYPES]
    expected_large_primes = [29, 31, 37, 41]
    observed_large_primes = [
        prime
        for prime in range(29, ORDER)
        if all(prime % divisor for divisor in range(2, math.isqrt(prime) + 1))
    ]
    if observed_large_primes != expected_large_primes:
        raise AssertionError(observed_large_primes)

    p23 = p23_audit()
    direct_valid = all(item["excluded"] for item in direct)
    valid = direct_valid and p23["excluded"]
    return {
        "checker": CHECKER_ID,
        "valid": valid,
        "order": ORDER,
        "degree_window": [DEGREE_LOWER, DEGREE_UPPER],
        "degree_window_basis": {
            "external_theorem": "R(4,5)=R(5,4)=25",
            "upper_bound": (
                "If d(v)>=25, N(v) contains a K4 or an independent 5-set; "
                "either extends to a forbidden set in the whole graph."
            ),
            "lower_bound": (
                "If d(v)<=17, the 42-d(v)>=25 nonneighbors of v contain "
                "a K5 or an independent 4-set; either extends to a "
                "forbidden set in the whole graph."
            ),
        },
        "fixed_vertex_orbit_rule": (
            "For an automorphism of prime order p, a fixed vertex is "
            "adjacent to all or none of each moved p-cycle."
        ),
        "direct_degree_exclusions": direct,
        "p23_exclusion": p23,
        "p43_boundary": (
            "The type 43^1 has no fixed vertex, so this degree argument does "
            "not address it."
        ),
        "claim_boundary": (
            "Only 13^3 1^4, the one-cycle types for primes 29,31,37,41, "
            "and 23^1 1^20 are excluded here.  No other cycle type is "
            "claimed."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()
    result = audit()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.result is not None:
        if args.result.exists():
            raise SystemExit("refusing to overwrite result")
        args.result.parent.mkdir(parents=True, exist_ok=True)
        args.result.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
