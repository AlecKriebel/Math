#!/usr/bin/env python3
"""Verify the universal coarse-bin row facet and its fixed-source separation.

The finite enumeration is a proof of the integer quadratic inequality once
the five universal row-count bounds are supplied.  Their geometric proofs,
including all endpoint conventions, are recorded in
``proofs/coarse_bin_integer_degree_facet.md``.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VerificationError(ValueError):
    """Raised when an exact certificate check fails."""


def check(condition: bool, message: str) -> None:
    """Proof-critical check that remains active under ``python -O``."""

    if not condition:
        raise VerificationError(message)


def row_types() -> list[tuple[int, ...]]:
    """Enumerate all five-bin rows satisfying the universal bounds."""

    rows: list[tuple[int, ...]] = []
    for deep in range(6):
        for negative in range(41 - deep):
            for central in range(41 - deep - negative):
                remainder = 40 - deep - negative - central
                for contact in range(min(15, remainder) + 1):
                    positive = remainder - contact
                    if deep + negative < 7 or positive + contact < 6:
                        continue
                    rows.append(
                        (deep, negative, central, positive, contact)
                    )
    return rows


def fine_pair_moment_matrix(
    source: dict[str, object],
) -> list[list[Q]]:
    """Return E[d_i d_j] for the seven source atoms."""

    alpha = [Q(value) for value in source["alpha"]]
    triples = [tuple(item) for item in source["triples"]]
    nu = [Q(value) for value in source["nu"]]
    check(len(alpha) == 7, "source pair vector has wrong length")
    check(len(triples) == len(nu), "source triple vectors have wrong lengths")
    matrix = [[Q(0) for _ in range(7)] for _ in range(7)]
    for index, mass in enumerate(alpha):
        matrix[index][index] += mass
    for triple, mass in zip(triples, nu, strict=True):
        orbit = set(itertools.permutations(triple))
        check(bool(orbit), "empty permutation orbit")
        for first, second, _third in orbit:
            matrix[first][second] += mass / len(orbit)
    return matrix


def aggregate_matrix(
    fine: list[list[Q]], mapping: list[int]
) -> list[list[Q]]:
    """Aggregate seven-node second moments into the five threshold bins."""

    coarse = [[Q(0) for _ in range(5)] for _ in range(5)]
    for first in range(7):
        for second in range(7):
            coarse[mapping[first]][mapping[second]] += fine[first][second]
    return coarse


def verify(certificate_path: Path, source_path: Path) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)

    check(
        certificate["schema"]
        == "kissing5.fixed41_coarse_bin_integer_degree_obstruction.v1",
        "unexpected certificate schema",
    )
    check(
        source["schema"]
        == "fixed41-bv-fullradial-k16-pseudodistribution-v1",
        "unexpected source schema",
    )
    check(
        certificate["source_certificate"] == source_path.name,
        "source filename mismatch",
    )
    check(
        certificate["source_sha256"]
        == hashlib.sha256(source_bytes).hexdigest(),
        "source SHA-256 mismatch",
    )
    check(
        certificate["cardinality"] == source["cardinality"] == 41,
        "cardinality mismatch",
    )
    check(
        certificate["bins"]
        == [
            {"name": "A", "interval": "[-1,-3/4]"},
            {"name": "B", "interval": "(-3/4,-1/300)"},
            {"name": "C", "interval": "[-1/300,1/300]"},
            {"name": "D", "interval": "(1/300,1/2)"},
            {"name": "E", "interval": "{1/2}"},
        ],
        "bin endpoints or names differ from the proved partition",
    )
    check(
        certificate["row_type_constraints"]
        == {
            "degree_sum": 40,
            "deep_bin_upper_bound": 5,
            "negative_tail_lower_bound": 7,
            "positive_tail_lower_bound": 6,
            "contact_bin_upper_bound": 15,
        },
        "row constraints mismatch",
    )

    rows = row_types()
    check(
        len(rows) == len(set(rows)) == 32136,
        "row enumeration count or uniqueness failed",
    )
    check(
        all(
            sum(row) == 40
            and row[0] <= 5
            and row[0] + row[1] >= 7
            and row[3] + row[4] >= 6
            and row[4] <= 15
            for row in rows
        ),
        "enumerated row violates a defining constraint",
    )
    terms = [
        (tuple(item["indices"]), int(item["coefficient"]))
        for item in certificate["quadratic_terms"]
    ]
    expected_pairs = [
        (first, second)
        for first in range(5)
        for second in range(first, 5)
    ]
    check(
        [indices for indices, _coefficient in terms] == expected_pairs,
        "quadratic terms are not the complete lexicographic upper triangle",
    )
    check(
        all(coefficient for _indices, coefficient in terms),
        "zero quadratic coefficient is not allowed",
    )
    values = [
        sum(
            coefficient * row[first] * row[second]
            for (first, second), coefficient in terms
        )
        for row in rows
    ]
    positive = [value for value in values if value > 0]
    check(min(values) == 0, "row polynomial is negative or has no zero")
    check(bool(positive), "row polynomial has no positive value")
    check(
        certificate["enumeration"]
        == {
            "total_row_types": len(rows),
            "zero_count": values.count(0),
            "minimum_positive_value": min(positive),
            "maximum_value": max(values),
        },
        "stored row-enumeration statistics mismatch",
    )

    grid = [Q(value) for value in source["grid"]]
    check(
        grid
        == [
            Q(-1),
            Q(-3, 4),
            Q(-1, 2),
            Q(-1, 4),
            Q(0),
            Q(1, 4),
            Q(1, 2),
        ],
        "source is not on the certified seven-node grid",
    )
    mapping = certificate["source_grid_bin_map"]
    check(mapping == [0, 0, 1, 1, 2, 3, 4], "source bin map mismatch")
    alpha = [Q(value) for value in source["alpha"]]
    nu = [Q(value) for value in source["nu"]]
    triples = [tuple(item) for item in source["triples"]]
    check(sum(alpha) == 40, "source pair mass is not 40")
    check(sum(nu) == 40 * 39, "source triple mass is not 1560")
    for index in range(7):
        check(
            sum(
                mass * Q(triple.count(index), 3)
                for triple, mass in zip(triples, nu, strict=True)
            )
            == 39 * alpha[index],
            f"source marginal identity failed at node {index}",
        )
    fine = fine_pair_moment_matrix(source)
    check(
        all(
            fine[first][second] == fine[second][first]
            for first in range(7)
            for second in range(7)
        ),
        "fine second-moment matrix is not symmetric",
    )
    check(
        all(
            sum(fine[index]) == 40 * alpha[index]
            for index in range(7)
        ),
        "fine second-moment row sums do not match first moments",
    )
    coarse = aggregate_matrix(fine, mapping)
    expectation = sum(
        coefficient * coarse[first][second]
        for (first, second), coefficient in terms
    )
    check(
        expectation == Q(certificate["expected_value"]),
        "stored expected value mismatch",
    )
    check(expectation < 0, "coarse row facet does not separate the source")

    return {
        "status": "PASS",
        "scope": (
            "universal five-bin integer row inequality plus exact "
            "separation of the named pair/triple witness; not a general "
            "kissing-number upper bound"
        ),
        "row_types_checked": len(rows),
        "zero_count": values.count(0),
        "minimum_positive_value": min(positive),
        "expected_value": str(expectation),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        type=Path,
        default=(
            ROOT
            / "certificates"
            / "fixed41_coarse_bin_integer_degree_obstruction.json"
        ),
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=(
            ROOT
            / "certificates"
            / "fixed41_bv_fullradial_k16_pseudodistribution.json"
        ),
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate, args.source), indent=2))


if __name__ == "__main__":
    main()
