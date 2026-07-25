#!/usr/bin/env python3
"""Exact centered-skew audit of the common-pair-capacity witness.

The imported object is already certified elsewhere.  This script does not
reverify its BV or common-pair properties; it uses exact rational arithmetic
to test a broader deterministic family of C065 kernel combinations.
"""

from __future__ import annotations

from fractions import Fraction as Q
import json
from pathlib import Path

from experiments.continuous_rank_bv_search.search import (
    N,
    Kernel,
    default_kernels,
    qstr,
)


def exact_rank_values(
    kernel: Kernel,
    nodes: tuple[Q, ...],
    alpha: tuple[Q, ...],
    triples: dict[tuple[int, int, int], Q],
) -> tuple[Q, Q, Q]:
    values = kernel.values(nodes)
    diagonal = kernel.diagonal
    rank = kernel.rank
    trace_one = Q(N) * diagonal
    trace_two = Q(N) * diagonal**2 + Q(N) * sum(
        mass * value**2 for mass, value in zip(alpha, values)
    )
    trace_three = (
        Q(N) * diagonal**3
        + Q(3 * N) * diagonal * sum(
            mass * value**2 for mass, value in zip(alpha, values)
        )
        + Q(6)
        * sum(
            count * values[i] * values[j] * values[k]
            for (i, j, k), count in triples.items()
        )
    )
    variance = trace_two - trace_one**2 / rank
    centered = (
        trace_three
        - Q(3) * trace_one * trace_two / rank
        + Q(2) * trace_one**3 / rank**2
    )
    residual = (
        Q((rank - 2) ** 2) * variance**3
        - Q(rank * (rank - 1)) * centered**2
    )
    return variance, centered, residual


def audit(source_path: Path) -> dict[str, object]:
    source = json.loads(source_path.read_text())
    assert source["schema"] == (
        "common-pair-capacity-degree4-pseudodistribution-v1"
    )
    assert source["cardinality"] == N
    nodes = tuple(Q(value) for value in source["nodes"])
    ordered = tuple(source["ordered_pair_counts"])
    alpha = tuple(Q(value, N) for value in ordered)
    triples = {
        tuple(item["types"]): Q(item["count"])
        for item in source["triple_counts"]
    }
    assert sum(alpha) == N - 1
    assert sum(triples.values()) == Q(N * (N - 1) * (N - 2), 6)
    for index in range(len(nodes)):
        incidence = sum(
            count * triple.count(index)
            for triple, count in triples.items()
        )
        assert incidence == Q((N - 2) * ordered[index], 2)

    results = {}
    for kernel in default_kernels("rich"):
        variance, centered, residual = exact_rank_values(
            kernel, nodes, alpha, triples
        )
        results[kernel.name] = {
            "rank": kernel.rank,
            "weights": {
                str(degree): qstr(coefficient)
                for degree, coefficient in kernel.weights
            },
            "variance": qstr(variance),
            "centered_third": qstr(centered),
            "sharp_residual": qstr(residual),
            "passes": residual >= 0,
        }
    return {
        "schema": "common-pair-rich-centered-skew-audit-v1",
        "source": source_path.name,
        "arithmetic": "fractions.Fraction only",
        "kernel_count": len(results),
        "all_pass": all(item["passes"] for item in results.values()),
        "minimum_residual_kernel": min(
            results, key=lambda name: Q(results[name]["sharp_residual"])
        ),
        "results": results,
        "scope": (
        "Exact audit of the listed 27 kernels only; not a proof for all "
            "real harmonic combinations and not a code realization"
        ),
    }


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    source = (
        project_root
        / "certificates"
        / "common_pair_capacity_degree4_pseudodistribution.json"
    )
    result = audit(source)
    output = Path(__file__).resolve().parent / "results" / (
        "common_pair_rich_rank_audit.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
