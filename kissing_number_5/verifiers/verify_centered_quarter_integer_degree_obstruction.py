#!/usr/bin/env python3
"""Verify the centered quarter-grid integer degree-moment obstruction.

The verifier uses only the Python standard library.  Its conclusion is
deliberately narrow: the named pair/triple pseudodistribution is not the
degree-moment shadow of a centered 41-point code on the stated quarter grid.
It does not exclude arbitrary 41-point spherical codes.
"""

from __future__ import annotations

from fractions import Fraction as Q
import argparse
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def row_types() -> list[tuple[int, ...]]:
    """Enumerate all nonnegative integer rows satisfying the exact identities."""
    answer: list[tuple[int, ...]] = []
    for d0 in range(2):
        for d1 in range(41 - d0):
            for d2 in range(41 - d0 - d1):
                for d3 in range(41 - d0 - d1 - d2):
                    remainder = 40 - d0 - d1 - d2 - d3
                    for d5 in range(remainder + 1):
                        twice_d6 = (
                            -4 + 4 * d0 + 3 * d1 + 2 * d2 + d3 - d5
                        )
                        if twice_d6 < 0 or twice_d6 % 2:
                            continue
                        d6 = twice_d6 // 2
                        d4 = remainder - d5 - d6
                        if d4 >= 0:
                            answer.append(
                                (d0, d1, d2, d3, d4, d5, d6)
                            )
    return answer


def pair_moment_matrix(source: dict[str, object]) -> list[list[Q]]:
    alpha = [Q(value) for value in source["alpha"]]
    triples = [tuple(item) for item in source["triple_orbits"]]
    nu = [Q(value) for value in source["nu"]]
    matrix = [[Q(0) for _ in range(7)] for _ in range(7)]
    for index, mass in enumerate(alpha):
        matrix[index][index] += mass
    for triple, mass in zip(triples, nu):
        orbit = sorted(set(itertools.permutations(triple)))
        for i, j, _k in orbit:
            matrix[i][j] += mass / len(orbit)
    return matrix


def verify(
    certificate_path: Path,
    source_path: Path,
) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)

    assert certificate["schema"] == (
        "kissing5.centered_quarter_integer_degree_obstruction.v1"
    )
    assert source["schema"] == (
        "kissing5.centered_quarter_bv_pseudodistribution.v1"
    )
    assert certificate["source_certificate"] == source_path.name
    assert certificate["source_sha256"] == hashlib.sha256(
        source_bytes
    ).hexdigest()
    assert certificate["cardinality"] == source["cardinality"] == 41
    assert certificate["grid_numerators_over_four"] == [
        -4,
        -3,
        -2,
        -1,
        0,
        1,
        2,
    ]
    assert [Q(value) for value in source["grid"]] == [
        Q(value, 4)
        for value in certificate["grid_numerators_over_four"]
    ]

    constraints = certificate["row_type_constraints"]
    assert constraints == {
        "degree_sum": 40,
        "weighted_degree_sum": -4,
        "antipode_degree_upper_bound": 1,
    }

    terms = [
        (tuple(item["indices"]), int(item["coefficient"]))
        for item in certificate["quadratic_terms"]
    ]
    assert terms
    assert len({indices for indices, _coefficient in terms}) == len(terms)
    assert all(
        0 <= i <= j < 7 and coefficient
        for (i, j), coefficient in terms
    )

    types = row_types()
    values = [
        sum(
            coefficient * degree[i] * degree[j]
            for (i, j), coefficient in terms
        )
        for degree in types
    ]
    assert all(value >= 0 for value in values)
    positive_values = [value for value in values if value > 0]
    enumerated = certificate["enumeration"]
    assert len(types) == enumerated["total_row_types"] == 27041
    assert sum(degree[0] == 0 for degree in types) == (
        enumerated["row_types_without_antipode"]
    )
    assert sum(degree[0] == 1 for degree in types) == (
        enumerated["row_types_with_antipode"]
    )
    assert values.count(0) == enumerated["zero_count"]
    assert min(positive_values) == enumerated["minimum_positive_value"]
    assert max(values) == enumerated["maximum_value"]

    alpha = [Q(value) for value in source["alpha"]]
    moments = pair_moment_matrix(source)
    assert all(
        sum(row) == 40 * alpha[index]
        for index, row in enumerate(moments)
    )
    weighted = [Q(value, 4) for value in range(-4, 3)]
    assert all(
        sum(weighted[j] * moments[i][j] for j in range(7))
        == -alpha[i]
        for i in range(7)
    )

    expectation = sum(
        coefficient * moments[i][j]
        for (i, j), coefficient in terms
    )
    assert expectation == Q(certificate["expected_value"])
    assert expectation < 0

    return {
        "scope": (
            "exact obstruction to the named centered quarter-grid "
            "pair/triple witness; not a general kissing-number bound"
        ),
        "row_types_checked": len(types),
        "zero_count": values.count(0),
        "minimum_positive_value": min(positive_values),
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
            / "centered_quarter_integer_degree_obstruction.json"
        ),
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=(
            ROOT
            / "certificates"
            / "centered_quarter_bv_pseudodistribution.json"
        ),
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate, args.source), indent=2))


if __name__ == "__main__":
    main()
