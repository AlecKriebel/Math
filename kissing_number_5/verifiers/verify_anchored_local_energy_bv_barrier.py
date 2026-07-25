#!/usr/bin/env python3
"""Exact moment check for the anchored local-energy BV barrier.

This small verifier does not re-prove the imported all-harmonic BV
positivity theorem.  It pins that separately certified pseudo-distribution
by SHA-256 and checks exactly the mass, support, marginals, and second moment
used by the barrier argument.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = (
    ROOT / "certificates" / "fixed41_bv_fullradial_k16_pseudodistribution.json"
)
ALL_HARMONICS_PATH = (
    ROOT / "certificates" / "fixed41_bv_all_harmonics_certificate.json"
)
EXPECTED_SOURCE_SHA256 = (
    "8c016c5ab1770f930d3f31f5448ffef7731616dd7025b29c43828760064b4d88"
)
EXPECTED_OFF_DIAGONAL_SECOND_MOMENT = Q(
    5767796592200083, 800000000000000
)
EXPECTED_STRICT_EXCESS = Q(7796592200083, 800000000000000)


def verify(
    source_path: Path = SOURCE_PATH,
    all_harmonics_path: Path = ALL_HARMONICS_PATH,
) -> dict[str, object]:
    source_bytes = source_path.read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    source = json.loads(source_bytes)
    all_harmonics = json.loads(all_harmonics_path.read_text())

    assert source_hash == EXPECTED_SOURCE_SHA256
    assert all_harmonics["schema"] == "fixed41-bv-all-harmonics-v1"
    assert all_harmonics["source_certificate"] == source_path.name
    assert all_harmonics["source_sha256"] == source_hash
    assert all_harmonics["conclusion"] == (
        "All W_k are positive semidefinite and all ordinary two-point "
        "Gegenbauer moments are positive."
    )
    assert (
        source["schema"]
        == "fixed41-bv-fullradial-k16-pseudodistribution-v1"
    )
    assert source["dimension"] == 5
    assert source["cardinality"] == 41
    assert Q(source["maximum_inner_product"]) == Q(1, 2)

    grid = [Q(value) for value in source["grid"]]
    alpha = [Q(value) for value in source["alpha"]]
    triples = [tuple(indices) for indices in source["triples"]]
    nu = [Q(value) for value in source["nu"]]
    assert grid == [
        Q(-1),
        Q(-3, 4),
        Q(-1, 2),
        Q(-1, 4),
        Q(0),
        Q(1, 4),
        Q(1, 2),
    ]
    assert all(weight > 0 for weight in alpha + nu)
    assert sum(alpha) == 40
    assert sum(nu) == 40 * 39

    for triple in triples:
        assert tuple(sorted(triple)) == triple
        u, v, t = (grid[index] for index in triple)
        assert u <= Q(1, 2) and v <= Q(1, 2) and t <= Q(1, 2)
        assert 1 + 2 * u * v * t - u * u - v * v - t * t >= 0
    for index in range(len(grid)):
        marginal = sum(
            weight * triple.count(index) / 3
            for triple, weight in zip(triples, nu, strict=True)
        )
        assert marginal == 39 * alpha[index]

    off_diagonal_second_moment = sum(
        weight * value * value
        for value, weight in zip(grid, alpha, strict=True)
    )
    assert off_diagonal_second_moment == (
        EXPECTED_OFF_DIAGONAL_SECOND_MOMENT
    )
    strict_excess = off_diagonal_second_moment - Q(36, 5)
    assert strict_excess == EXPECTED_STRICT_EXCESS
    assert strict_excess > 0

    row_second_moment = Q(1) + off_diagonal_second_moment
    assert row_second_moment - Q(41, 5) == strict_excess

    return {
        "status": "PASS",
        "source_sha256": source_hash,
        "pair_mass": sum(alpha),
        "ordered_triple_mass": sum(nu),
        "off_diagonal_second_moment": off_diagonal_second_moment,
        "target_threshold": Q(36, 5),
        "strict_excess": strict_excess,
        "row_second_moment": row_second_moment,
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
