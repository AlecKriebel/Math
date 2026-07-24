#!/usr/bin/env python3
"""Verify the noncentered fixed-41 integer degree-moment obstruction."""

from __future__ import annotations

from fractions import Fraction as Q
import argparse
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
    """Enumerate the exact universal local row superset."""

    rows: list[tuple[int, ...]] = []
    for d0 in range(2):
        for d1 in range(6):
            for d2 in range(41 - d0 - d1):
                for d3 in range(41 - d0 - d1 - d2):
                    if d0 + d1 + d2 + d3 < 7:
                        continue
                    remainder = 40 - d0 - d1 - d2 - d3
                    for d6 in range(min(15, remainder) + 1):
                        for d5 in range(
                            max(0, 6 - d6),
                            remainder - d6 + 1,
                        ):
                            d4 = remainder - d5 - d6
                            rows.append((d0, d1, d2, d3, d4, d5, d6))
    return rows


def pair_moment_matrix(source: dict[str, object]) -> list[list[Q]]:
    alpha = [Q(value) for value in source["alpha"]]
    check(
        len(source["triples"]) == len(source["nu"]),
        "triple and mass list lengths differ",
    )
    matrix = [[Q(0) for _ in range(7)] for _ in range(7)]
    for index, mass in enumerate(alpha):
        matrix[index][index] += mass
    for triple, mass_text in zip(source["triples"], source["nu"]):
        mass = Q(mass_text)
        orbit = set(itertools.permutations(triple))
        for first, second, _third in orbit:
            matrix[first][second] += mass / len(orbit)
    return matrix


def verify(certificate_path: Path, source_path: Path) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    check(
        certificate["schema"]
        == "kissing5.fixed41_noncentered_integer_degree_obstruction.v1",
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
    numerators = certificate["grid_numerators_over_four"]
    check(
        numerators == [-4, -3, -2, -1, 0, 1, 2],
        "unexpected quarter grid",
    )
    check(
        [Q(value) for value in source["grid"]]
        == [Q(value, 4) for value in numerators],
        "source grid mismatch",
    )
    check(
        certificate["row_type_constraints"]
        == {
            "degree_sum": 40,
            "antipode_degree_upper_bound": 1,
            "negative_degree_lower_bound": 7,
            "positive_degree_lower_bound": 6,
            "contact_degree_upper_bound": 15,
            "minus_three_quarters_degree_upper_bound": 5,
        },
        "row constraints mismatch",
    )

    rows = row_types()
    check(
        len(rows) == len(set(rows)) == 855168,
        "row enumeration count or uniqueness failed",
    )
    check(
        all(
            sum(row) == 40
            and row[0] <= 1
            and sum(row[:4]) >= 7
            and sum(row[5:]) >= 6
            and row[6] <= 15
            and row[1] <= 5
            for row in rows
        ),
        "enumerated row violates a defining constraint",
    )
    terms = [
        (tuple(item["indices"]), int(item["coefficient"]))
        for item in certificate["quadratic_terms"]
    ]
    check(0 < len(terms) <= 28, "unexpected number of quadratic terms")
    check(
        len({indices for indices, _coefficient in terms}) == len(terms),
        "duplicate quadratic term",
    )
    check(
        all(
            len(indices) == 2
            and 0 <= indices[0] <= indices[1] < 7
            and coefficient
            for indices, coefficient in terms
        ),
        "malformed quadratic term",
    )
    values = [
        sum(
            coefficient * row[i] * row[j]
            for (i, j), coefficient in terms
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

    alpha = [Q(value) for value in source["alpha"]]
    nu = [Q(value) for value in source["nu"]]
    triples = [tuple(row) for row in source["triples"]]
    check(len(alpha) == 7, "source pair vector has wrong length")
    check(len(triples) == len(nu), "source triple vectors have wrong lengths")
    check(sum(alpha) == 40, "source pair mass is not 40")
    check(sum(nu) == 40 * 39, "source triple mass is not 1560")
    for index in range(7):
        check(
            sum(
                mass * Q(triple.count(index), 3)
                for mass, triple in zip(nu, triples, strict=True)
            )
            == 39 * alpha[index],
            f"source marginal identity failed at node {index}",
        )
    moments = pair_moment_matrix(source)
    check(
        all(
            sum(moments[index]) == 40 * alpha[index]
            for index in range(7)
        ),
        "row sums of second moments do not match first moments",
    )
    check(
        all(
            moments[i][j] == moments[j][i]
            for i in range(7)
            for j in range(7)
        ),
        "second-moment matrix is not symmetric",
    )
    expectation = sum(
        coefficient * moments[i][j]
        for (i, j), coefficient in terms
    )
    check(
        expectation == Q(certificate["expected_value"]),
        "stored expected value mismatch",
    )
    check(expectation < 0, "row facet does not separate the source")

    return {
        "status": "PASS",
        "scope": (
            "exact obstruction to the named noncentered quarter-grid "
            "pair/triple witness under universal local row constraints; "
            "not a general code bound"
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
            / "fixed41_noncentered_integer_degree_obstruction.json"
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
