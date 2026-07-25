#!/usr/bin/env python3
"""Exact checks for two harmonic-combination centered-skew rank cuts.

Only standard-library rational arithmetic is used.  The general rank lemma
is proved in ``proofs/harmonic_combination_centered_skew.md``; this program
checks its two stored applications to the degree-four pseudodistribution.
"""

from fractions import Fraction as Q
from math import comb, gcd
import json
from pathlib import Path

try:
    from verifiers.verify_local_hybrid_barrier import zonal_values
except ModuleNotFoundError:  # Direct execution from this directory.
    from verify_local_hybrid_barrier import zonal_values


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "certificates"
    / "harmonic_combination_centered_skew_instances.json"
)


def harmonic_dimension(dimension, degree):
    """Dimension of degree-k spherical harmonics on S^(dimension-1)."""

    first = comb(degree + dimension - 1, dimension - 1)
    second = (
        comb(degree + dimension - 3, dimension - 1)
        if degree >= 2
        else 0
    )
    return first - second


def kernel_traces(
    cardinality,
    nodes,
    ordered_counts,
    triple_counts,
    harmonic_weights,
):
    maximum_degree = max(harmonic_weights)

    def kernel(t):
        values = zonal_values(t, maximum_degree)
        return sum(
            coefficient * values[degree]
            for degree, coefficient in harmonic_weights.items()
        )

    diagonal = kernel(Q(1))
    node_values = tuple(kernel(node) for node in nodes)
    pair_square = sum(
        Q(count) * value**2
        for count, value in zip(ordered_counts, node_values)
    )
    trace_one = cardinality * diagonal
    trace_two = cardinality * diagonal**2 + pair_square
    trace_three = cardinality * diagonal**3 + 3 * diagonal * pair_square
    trace_three += 6 * sum(
        Q(count)
        * node_values[i]
        * node_values[j]
        * node_values[k]
        for (i, j, k), count in triple_counts.items()
    )
    return trace_one, trace_two, trace_three


def load_data():
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert data["schema"] == (
        "harmonic-combination-centered-skew-instances-v1"
    )
    source = ROOT / data["source_pseudodistribution"]
    witness = json.loads(source.read_text(encoding="utf-8"))
    assert witness["schema"] == (
        "local-hybrid-degree4-rank-color-clique-pseudodistribution-v1"
    )
    assert witness["dimension"] == data["dimension"] == 5
    assert witness["cardinality"] == data["cardinality"] == 41
    nodes = tuple(Q(value) for value in witness["nodes"])
    ordered_counts = tuple(witness["ordered_pair_counts"])
    triple_counts = {
        tuple(item["types"]): item["count"]
        for item in witness["triple_counts"]
    }
    assert sum(ordered_counts) == 41 * 40
    assert sum(triple_counts.values()) == comb(41, 3)
    return data, nodes, ordered_counts, triple_counts


def verify():
    data, nodes, ordered_counts, triple_counts = load_data()
    results = {}
    for item in data["instances"]:
        weights = {
            int(degree): Q(coefficient)
            for degree, coefficient in item["harmonic_weights"].items()
        }
        assert all(coefficient != 0 for coefficient in weights.values())
        rank_bound = sum(
            harmonic_dimension(5, degree) for degree in weights
        )
        assert rank_bound == item["rank_bound"]
        traces = kernel_traces(
            41, nodes, ordered_counts, triple_counts, weights
        )
        assert traces == (
            Q(item["expected_trace"]),
            Q(item["expected_trace_square"]),
            Q(item["expected_trace_cube"]),
        )
        trace_one, trace_two, trace_three = traces
        variance = trace_two - trace_one**2 / rank_bound
        centered_third = (
            trace_three
            - Q(3) * trace_one * trace_two / rank_bound
            + Q(2) * trace_one**3 / rank_bound**2
        )
        assert variance == Q(item["expected_centered_variance"])
        assert centered_third == Q(item["expected_centered_third"])

        common_factor = gcd(
            rank_bound * (rank_bound - 1),
            (rank_bound - 2) ** 2,
        )
        third_coefficient = (
            rank_bound * (rank_bound - 1) // common_factor
        )
        variance_coefficient = (
            (rank_bound - 2) ** 2 // common_factor
        )
        residual = (
            variance_coefficient * variance**3
            - third_coefficient * centered_third**2
        )
        assert residual == Q(item["expected_reduced_residual"])
        assert residual < 0

        # The rational band is outside the exact square-root radius, hence
        # |D| <= band is a weaker but valid pair of linear inequalities.
        band = Q(item["outer_linear_band"])
        outer_slack = (
            third_coefficient * band**2
            - variance_coefficient * variance**3
        )
        assert outer_slack > 0
        assert abs(centered_third) > band
        results[item["name"]] = {
            "rank_bound": rank_bound,
            "variance": variance,
            "centered_third": centered_third,
            "rank_residual": residual,
            "outer_band": band,
            "outer_band_slack": outer_slack,
        }

    assert results["(H0+5H1)/6"]["outer_band_slack"] == Q(
        19611647008561, 2985984000000
    )
    assert results["H2"]["outer_band_slack"] == Q(
        47450085131380413914603963850403,
        89915392000000000000000000000000,
    )
    return {
        "instances": results,
        "general_rank_lemma_scope": "all real symmetric rank-r matrices",
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
