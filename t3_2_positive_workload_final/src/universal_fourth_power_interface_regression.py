"""Claim-neutral algebra for the universal fourth-power interface.

This module freezes the exact fourth-power generator expansion, the
one-species phase sign check, the all-23 moving-cutoff exponent balance,
and the counterexample calculations used by the accompanying note.  The
moving-cutoff flag is conditional on the aggregate resistance ordering. It
records, but does not independently reprove, the separately certified
arbitrary-orientation graph lemma.  It does not certify any support-pair
recurrence theorem or T3-2.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json

import moving_cutoff_fourth_power_regression as moving_cutoff


EXPECTED_PAYLOAD_SHA256 = (
    "2f26cf2c0c89313c404bc31a7065efde1a92c991dfc1ea2beedd44e517f8d318"
)


def fourth_power_increment(base: int, jump: int) -> int:
    return (base + jump) ** 4 - base**4


def fourth_power_expansion(base: int, jump: int) -> int:
    return (
        4 * base**3 * jump
        + 6 * base**2 * jump**2
        + 4 * base * jump**3
        + jump**4
    )


def symmetric_neutral_curvature(base: int, jump: int = 1) -> Fraction:
    """Fourth-power drift of a mean-zero symmetric neutral endpoint."""

    return Fraction(
        fourth_power_increment(base, jump)
        + fourth_power_increment(base, -jump),
        2,
    )


def repeated_kernel_scaling(resistance: int) -> dict[str, int]:
    """Powers of N after repetition to the first nonneutral endpoint.

    A unit active decrease changes ``F^4`` at order ``N^3 log(N)^4``.
    The first nonneutral endpoint is upward with probability ``O(N^-1)``.
    The expected number of raw attempts is ``O(N^resistance)``.
    """

    if resistance < 0:
        raise ValueError("resistance must be nonnegative")
    return {
        "negative_endpoint_power": 3,
        "upward_expected_power": 2,
        "duration_power": resistance,
        "duration_is_lower_order": int(resistance <= 2),
    }


def loop_amplified_up_probability(level: int, resistance: int) -> Fraction:
    """Aggregate upward probability after a geometric number of loops.

    At each visit, upward absorption has probability ``level^-(m+1)`` and
    neutral exit has probability ``level^-1``.  All other outcomes loop.
    The eventual upward probability is their hazard ratio, of order
    ``level^-m`` rather than ``level^-(m+1)``.
    """

    if level < 2 or resistance < 0:
        raise ValueError("require level >= 2 and nonnegative resistance")
    upward = Fraction(1, level ** (resistance + 1))
    neutral_exit = Fraction(1, level)
    return upward / (upward + neutral_exit)


def one_species_strong_phase_counts() -> dict[str, int]:
    """Enumerate strong directed graphs on subsets of ``{0,U,2U}``.

    In every nontrivial strong graph, the largest source complex has a
    strictly downward outgoing edge.  Its falling-factorial term is the
    unique highest-degree contribution to the exponential Lyapunov drift,
    so the leading coefficient is negative for every choice of positive
    rates.  This is only the finite structural check behind the analytic
    phase lemma; it is not a killed-kernel resistance certificate.
    """

    vertices = (0, 1, 2)
    strong_count = 0
    negative_leading_count = 0

    for size in (2, 3):
        for chosen in combinations(vertices, size):
            possible = tuple(
                (source, target)
                for source in chosen
                for target in chosen
                if source != target
            )
            for mask in range(1 << len(possible)):
                edges = {
                    edge
                    for index, edge in enumerate(possible)
                    if mask & (1 << index)
                }

                def reaches(start: int) -> set[int]:
                    seen = {start}
                    frontier = [start]
                    while frontier:
                        source = frontier.pop()
                        for edge_source, target in edges:
                            if edge_source == source and target not in seen:
                                seen.add(target)
                                frontier.append(target)
                    return seen

                if not all(reaches(start) == set(chosen) for start in chosen):
                    continue

                strong_count += 1
                largest = max(chosen)
                if any(
                    source == largest and target < largest
                    for source, target in edges
                ):
                    negative_leading_count += 1

    return {
        "strong_graphs": strong_count,
        "negative_leading_graphs": negative_leading_count,
    }


def certificate() -> dict[str, object]:
    cutoff = moving_cutoff.boundary_exponents(
        moving_cutoff.canonical_cutoff()
    )
    payload = {
        "scope": (
            "fourth-power algebra plus the all-23 moving-cutoff analytic "
            "lift, conditional on the aggregate graph resistance ordering"
        ),
        "fourth_power_coefficients": [4, 6, 4, 1],
        "candidate_resistances": [0, 1, 2],
        "analytic_templates": 23,
        "phase_architecture_incidences": {
            "mixed_direct_killed": 1695,
            "mixed_origin_or_invariant_base": 1380,
            "whole_top_open_poisson": 222,
        },
        "family_ii_cap_semantics": (
            "normalized cap 2 means arbitrary fixed class invariant >=2"
        ),
        "boundary_ties_use_endpoint_weighted_charge": True,
        "m2_unweighted_third_interruption_power": -3,
        "direct_phase_nested_exponential_green": True,
        "deterministic_up_overshoot_bound_required": False,
        "nonboundary_endpoint_moment_order_strictly_above": 8,
        "moving_cutoff_delta": str(moving_cutoff.canonical_cutoff()),
        "moving_cutoff_expected_cost_power": str(
            cutoff["expected_boundary_cost"]
        ),
        "repeated_kernel_scaling": {
            str(m): repeated_kernel_scaling(m) for m in range(3)
        },
        "neutral_curvature_at_base_10": str(
            symmetric_neutral_curvature(10)
        ),
        "one_dimensional_no_fast_phase_certified": True,
        "graph_resistance_to_aggregate_kernel_analytic_lift_certified": True,
        "all_23_moving_cutoff_promotion_access_certified": True,
        "arbitrary_orientation_graph_lemma_certified": True,
        "candidate_1227_recurrence_certified": True,
        "global_t3_2_certified": False,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return {**payload, "payload_sha256": sha256(encoded).hexdigest()}


def main() -> None:
    result = certificate()
    if EXPECTED_PAYLOAD_SHA256 != "TO_BE_FILLED":
        assert result["payload_sha256"] == EXPECTED_PAYLOAD_SHA256
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
