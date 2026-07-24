#!/usr/bin/env python3
"""Verify an exact noncentered integer row-degree moment mixture."""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VerificationError(ValueError):
    pass


def check(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def pair_moment_matrix(source: dict[str, object]) -> list[list[Q]]:
    matrix = [[Q(0) for _ in range(7)] for _ in range(7)]
    for index, mass in enumerate(source["alpha"]):
        matrix[index][index] += Q(mass)
    for triple, mass_text in zip(
        source["triples"], source["nu"], strict=True
    ):
        orbit = set(itertools.permutations(triple))
        for first, second, _third in orbit:
            matrix[first][second] += Q(mass_text) / len(orbit)
    return matrix


def complete_row_count() -> int:
    count = 0
    for d0 in range(2):
        for d1 in range(6):
            for d2 in range(41 - d0 - d1):
                for d3 in range(41 - d0 - d1 - d2):
                    if d0 + d1 + d2 + d3 < 7:
                        continue
                    remainder = 40 - d0 - d1 - d2 - d3
                    for d6 in range(min(15, remainder) + 1):
                        count += max(
                            0,
                            remainder
                            - d6
                            - max(0, 6 - d6)
                            + 1,
                        )
    return count


def verify(certificate_path: Path, source_path: Path) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    check(
        certificate["schema"]
        == "kissing5.noncentered_integer_degree_mixture.v1",
        "unexpected mixture schema",
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
        "source hash mismatch",
    )
    check(
        certificate["cardinality"] == source["cardinality"] == 41,
        "cardinality mismatch",
    )
    numerators = certificate["grid_numerators_over_four"]
    check(numerators == [-4, -3, -2, -1, 0, 1, 2], "grid mismatch")
    check(
        [Q(value) for value in source["grid"]]
        == [Q(value, 4) for value in numerators],
        "source grid mismatch",
    )
    expected_constraints = {
        "degree_sum": 40,
        "antipode_degree_upper_bound": 1,
        "negative_degree_lower_bound": 7,
        "positive_degree_lower_bound": 6,
        "contact_degree_upper_bound": 15,
        "minus_three_quarters_degree_upper_bound": 5,
    }
    check(
        certificate["row_type_constraints"] == expected_constraints,
        "row constraints mismatch",
    )
    check(
        certificate["complete_row_type_count"]
        == complete_row_count()
        == 855168,
        "complete row count mismatch",
    )

    atoms = certificate["atoms"]
    degrees = [tuple(atom["degree_vector"]) for atom in atoms]
    weights = [Q(atom["weight"]) for atom in atoms]
    check(len(atoms) == 26, "unexpected positive support size")
    check(len(set(degrees)) == len(degrees), "duplicate row atom")
    check(all(weight > 0 for weight in weights), "nonpositive weight")
    check(sum(weights) == 1, "weights do not sum to one")
    for degree in degrees:
        check(
            len(degree) == 7
            and all(isinstance(value, int) and value >= 0 for value in degree),
            "malformed degree vector",
        )
        check(sum(degree) == 40, "degree sum mismatch")
        check(degree[0] <= 1, "antipode bound violated")
        check(degree[1] <= 5, "minus-three-quarters bound violated")
        check(sum(degree[:4]) >= 7, "negative depth bound violated")
        check(sum(degree[5:]) >= 6, "positive depth bound violated")
        check(degree[6] <= 15, "contact bound violated")

    alpha = [Q(value) for value in source["alpha"]]
    target = pair_moment_matrix(source)
    observed_alpha = [
        sum(
            weight * degree[index]
            for weight, degree in zip(weights, degrees, strict=True)
        )
        for index in range(7)
    ]
    observed_second = [
        [
            sum(
                weight * degree[i] * degree[j]
                for weight, degree in zip(weights, degrees, strict=True)
            )
            for j in range(7)
        ]
        for i in range(7)
    ]
    check(observed_alpha == alpha, "first moments do not match")
    check(observed_second == target, "second moments do not match")
    return {
        "status": "PASS",
        "scope": (
            "exact first/second integer row moments for one pair/triple "
            "witness; not a global code"
        ),
        "positive_atoms": len(atoms),
        "minimum_weight": str(min(weights)),
        "complete_row_types": certificate["complete_row_type_count"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        type=Path,
        default=(
            ROOT
            / "experiments"
            / "noncentered_integer_degree_repair"
            / "integer_row_mixture_6.json"
        ),
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=(
            ROOT
            / "experiments"
            / "noncentered_integer_degree_repair"
            / "candidate_exact_6.json"
        ),
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate, args.source), indent=2))


if __name__ == "__main__":
    main()
