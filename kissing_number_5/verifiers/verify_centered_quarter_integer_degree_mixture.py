#!/usr/bin/env python3
"""Exact verifier for the repaired integer row-degree moment mixture."""

from __future__ import annotations

from fractions import Fraction as Q
import argparse
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def pair_moment_matrix(source: dict[str, object]) -> list[list[Q]]:
    alpha = [Q(value) for value in source["alpha"]]
    matrix = [[Q(0) for _ in range(7)] for _ in range(7)]
    for index, mass in enumerate(alpha):
        matrix[index][index] += mass
    for triple, mass_text in zip(source["triple_orbits"], source["nu"]):
        mass = Q(mass_text)
        orbit = set(itertools.permutations(triple))
        for i, j, _k in orbit:
            matrix[i][j] += mass / len(orbit)
    return matrix


def verify(certificate_path: Path, source_path: Path) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    assert certificate["schema"] == (
        "kissing5.centered_quarter_integer_degree_mixture.v1"
    )
    assert source["schema"] == (
        "kissing5.centered_quarter_bv_pseudodistribution.v1"
    )
    assert certificate["source_certificate"] == source_path.name
    assert certificate["source_sha256"] == hashlib.sha256(
        source_bytes
    ).hexdigest()
    assert certificate["cardinality"] == source["cardinality"] == 41
    numerators = certificate["grid_numerators_over_four"]
    assert numerators == [-4, -3, -2, -1, 0, 1, 2]
    assert [Q(value) for value in source["grid"]] == [
        Q(value, 4) for value in numerators
    ]

    atoms = certificate["atoms"]
    assert len(atoms) == certificate["positive_atom_count"] == 18
    degrees = [tuple(atom["degree_vector"]) for atom in atoms]
    weights = [Q(atom["weight"]) for atom in atoms]
    assert len(set(degrees)) == len(degrees)
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1
    for degree in degrees:
        assert len(degree) == 7
        assert all(isinstance(value, int) and value >= 0 for value in degree)
        assert sum(degree) == 40
        assert sum(value * count for value, count in zip(numerators, degree)) == -4
        assert degree[0] <= 1

    alpha = [Q(value) for value in source["alpha"]]
    target = pair_moment_matrix(source)
    observed_alpha = [
        sum(weight * degree[i] for weight, degree in zip(weights, degrees))
        for i in range(7)
    ]
    observed_moments = [
        [
            sum(
                weight * degree[i] * degree[j]
                for weight, degree in zip(weights, degrees)
            )
            for j in range(7)
        ]
        for i in range(7)
    ]
    assert observed_alpha == alpha
    assert observed_moments == target

    return {
        "status": "PASS",
        "scope": (
            "exact first/second integer row-degree moments for one "
            "pair/triple witness; not a global code"
        ),
        "positive_atoms": len(atoms),
        "minimum_weight": str(min(weights)),
        "exact_pair_moment_match": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        type=Path,
        default=(
            ROOT
            / "certificates"
            / "centered_quarter_integer_degree_mixture.json"
        ),
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=(
            ROOT
            / "experiments"
            / "centered_integer_degree_moments"
            / "repaired_pair_triple_local_3.json"
        ),
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate, args.source), indent=2))


if __name__ == "__main__":
    main()
