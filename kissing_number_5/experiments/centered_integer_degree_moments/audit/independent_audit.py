#!/usr/bin/env python3
"""Independent exact audit of the centered integer degree separators.

This deliberately does not import the production verifier or its row
enumerator.  It uses a recursive bounded-composition enumeration and derives
the second degree moments by explicitly permuting the three vertices of a
triangle.
"""

from __future__ import annotations

from fractions import Fraction as Q
import argparse
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
WEIGHTS = (-4, -3, -2, -1, 0, 1, 2)


def centered_rows() -> tuple[tuple[int, ...], ...]:
    """Enumerate bounded compositions by recursive weight-range pruning."""

    rows: list[tuple[int, ...]] = []

    def visit(
        position: int,
        remaining_count: int,
        remaining_weight: int,
        prefix: tuple[int, ...],
    ) -> None:
        if position == len(WEIGHTS) - 1:
            if WEIGHTS[position] * remaining_count == remaining_weight:
                rows.append(prefix + (remaining_count,))
            return

        upper = min(remaining_count, 1) if position == 0 else remaining_count
        low_weight = WEIGHTS[position + 1]
        high_weight = WEIGHTS[-1]
        for count in range(upper + 1):
            next_count = remaining_count - count
            next_weight = remaining_weight - WEIGHTS[position] * count
            if low_weight * next_count <= next_weight <= high_weight * next_count:
                visit(
                    position + 1,
                    next_count,
                    next_weight,
                    prefix + (count,),
                )

    visit(0, 40, -4, ())
    return tuple(rows)


def vertex_permuted_edge_pairs(
    triple: tuple[int, int, int],
) -> tuple[tuple[int, int], ...]:
    """Return the two base-incident edge labels for all six vertex orders."""

    edge = {
        frozenset((0, 1)): triple[0],
        frozenset((0, 2)): triple[1],
        frozenset((1, 2)): triple[2],
    }
    result = []
    for base, first, second in itertools.permutations(range(3)):
        result.append(
            (
                edge[frozenset((base, first))],
                edge[frozenset((base, second))],
            )
        )
    return tuple(result)


def degree_moments(source: dict[str, object]) -> tuple[list[Q], list[list[Q]]]:
    """Derive E[d_i] and E[d_i d_j] from ordered triangle incidences."""

    alpha = [Q(value) for value in source["alpha"]]
    triples = [tuple(int(value) for value in row) for row in source["triple_orbits"]]
    nu = [Q(value) for value in source["nu"]]
    assert len(triples) == len(nu)

    second = [[Q(0) for _ in WEIGHTS] for _ in WEIGHTS]
    for index, mass in enumerate(alpha):
        # The repeated-neighbor choices y=z in d_i^2.
        second[index][index] += mass
    for triple, mass in zip(triples, nu):
        for first, second_index in vertex_permuted_edge_pairs(triple):
            second[first][second_index] += mass / 6
    return alpha, second


def audit_one(certificate_path: Path, source_path: Path) -> dict[str, object]:
    certificate = json.loads(certificate_path.read_text())
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)

    assert certificate["schema"] == (
        "kissing5.centered_quarter_integer_degree_obstruction.v1"
    )
    assert certificate["source_certificate"] == source_path.name
    assert certificate["source_sha256"] == hashlib.sha256(source_bytes).hexdigest()
    assert certificate["cardinality"] == source["cardinality"] == 41
    assert certificate["grid_numerators_over_four"] == list(WEIGHTS)
    assert certificate["row_type_constraints"] == {
        "degree_sum": 40,
        "weighted_degree_sum": -4,
        "antipode_degree_upper_bound": 1,
    }

    rows = centered_rows()
    assert len(rows) == len(set(rows)) == 27041
    assert all(sum(row) == 40 for row in rows)
    assert all(sum(w * d for w, d in zip(WEIGHTS, row)) == -4 for row in rows)
    assert all(row[0] <= 1 and min(row) >= 0 for row in rows)

    terms = [
        (tuple(int(index) for index in item["indices"]), int(item["coefficient"]))
        for item in certificate["quadratic_terms"]
    ]
    assert terms and len(terms) == len({indices for indices, _ in terms})
    values = [
        sum(coefficient * row[i] * row[j] for (i, j), coefficient in terms)
        for row in rows
    ]
    positive = [value for value in values if value > 0]
    assert min(values) == 0
    assert certificate["enumeration"] == {
        "total_row_types": len(rows),
        "row_types_with_antipode": sum(row[0] == 1 for row in rows),
        "row_types_without_antipode": sum(row[0] == 0 for row in rows),
        "zero_count": values.count(0),
        "minimum_positive_value": min(positive),
        "maximum_value": max(values),
    } or all(
        certificate["enumeration"][key] == value
        for key, value in {
            "total_row_types": len(rows),
            "row_types_with_antipode": sum(row[0] == 1 for row in rows),
            "row_types_without_antipode": sum(row[0] == 0 for row in rows),
            "zero_count": values.count(0),
            "minimum_positive_value": min(positive),
            "maximum_value": max(values),
        }.items()
    )

    alpha, moments = degree_moments(source)
    triples = [tuple(int(value) for value in row) for row in source["triple_orbits"]]
    nu = [Q(value) for value in source["nu"]]
    assert sum(alpha) == 40
    assert sum(nu) == 40 * 39
    for index in range(7):
        triangle_marginal = sum(
            mass * Q(triple.count(index), 3)
            for triple, mass in zip(triples, nu)
        )
        assert triangle_marginal == 39 * alpha[index]
        assert sum(moments[index]) == 40 * alpha[index]
        assert (
            sum(Q(WEIGHTS[j], 4) * moments[index][j] for j in range(7))
            == -alpha[index]
        )
    assert all(
        moments[i][j] == moments[j][i]
        for i in range(7)
        for j in range(7)
    )

    expected = sum(
        coefficient * moments[i][j]
        for (i, j), coefficient in terms
    )
    assert expected == Q(certificate["expected_value"]) < 0

    zero_rows = [row for row, value in zip(rows, values) if value == 0]
    return {
        "certificate": certificate_path.name,
        "source": source_path.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "row_count": len(rows),
        "without_antipode": sum(row[0] == 0 for row in rows),
        "with_antipode": sum(row[0] == 1 for row in rows),
        "polynomial_terms": len(terms),
        "zero_count": len(zero_rows),
        "zero_rows": [list(row) for row in zero_rows],
        "minimum_positive_value": min(positive),
        "maximum_value": max(values),
        "expected_value": str(expected),
        "conclusion": (
            "this named pair/triple moment point is outside the exact integer "
            "row-moment cone; no universal quarter-grid or spherical-code "
            "nonexistence conclusion follows"
        ),
    }


def audit_mixture(certificate_path: Path, source_path: Path) -> dict[str, object]:
    """Independently verify an exact convex combination of integer rows."""

    certificate = json.loads(certificate_path.read_text())
    source_bytes = source_path.read_bytes()
    source = json.loads(source_bytes)
    assert certificate["schema"] == (
        "kissing5.centered_quarter_integer_degree_mixture.v1"
    )
    assert certificate["source_certificate"] == source_path.name
    assert certificate["source_sha256"] == hashlib.sha256(source_bytes).hexdigest()
    assert certificate["grid_numerators_over_four"] == list(WEIGHTS)

    admissible = set(centered_rows())
    atoms = certificate["atoms"]
    degrees = [tuple(atom["degree_vector"]) for atom in atoms]
    weights = [Q(atom["weight"]) for atom in atoms]
    assert len(atoms) == certificate["positive_atom_count"]
    assert len(degrees) == len(set(degrees))
    assert all(degree in admissible for degree in degrees)
    assert all(weight > 0 for weight in weights)
    assert sum(weights) == 1

    alpha, moments = degree_moments(source)
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
    assert observed_moments == moments

    separator_values: dict[str, str] = {}
    for separator_path, _old_source_path in default_pairs():
        separator = json.loads(separator_path.read_text())
        terms = [
            (
                tuple(int(index) for index in item["indices"]),
                int(item["coefficient"]),
            )
            for item in separator["quadratic_terms"]
        ]
        value = sum(
            coefficient * moments[i][j]
            for (i, j), coefficient in terms
        )
        assert value >= 0
        separator_values[separator_path.name] = str(value)

    return {
        "certificate": certificate_path.name,
        "source": source_path.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "positive_atoms": len(atoms),
        "minimum_weight": str(min(weights)),
        "exact_first_moment_match": True,
        "exact_second_moment_match": True,
        "prior_separator_values": separator_values,
        "conclusion": (
            "this repaired pair/triple point lies in the full exact integer "
            "row first/second-moment cone; this is still only a mixture of "
            "row types and not a globally consistent code"
        ),
    }


def default_pairs() -> list[tuple[Path, Path]]:
    certificate_dir = ROOT / "certificates"
    experiment_dir = ROOT / "experiments" / "centered_integer_degree_moments"
    pairs = [
        (
            certificate_dir / "centered_quarter_integer_degree_obstruction.json",
            certificate_dir / "centered_quarter_bv_pseudodistribution.json",
        ),
        (
            certificate_dir / "centered_quarter_integer_degree_obstruction_2.json",
            experiment_dir / "repaired_pair_triple_local.json",
        ),
        (
            certificate_dir / "centered_quarter_integer_degree_obstruction_3.json",
            experiment_dir / "repaired_pair_triple_local_2.json",
        ),
    ]
    return [(certificate, source) for certificate, source in pairs if certificate.exists()]


def default_mixture_pair() -> tuple[Path, Path] | None:
    certificate = ROOT / "certificates" / "centered_quarter_integer_degree_mixture.json"
    source = (
        ROOT
        / "experiments"
        / "centered_integer_degree_moments"
        / "repaired_pair_triple_local_3.json"
    )
    if certificate.exists() and source.exists():
        return certificate, source
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    mixture_pair = default_mixture_pair()
    report = {
        "schema": "kissing5.centered_integer_degree_independent_audit.v1",
        "arithmetic": "exact Python integers and fractions",
        "row_enumerator": "independent recursive bounded compositions",
        "triangle_normalization": "six explicit vertex permutations",
        "results": [
            audit_one(certificate, source)
            for certificate, source in default_pairs()
        ],
        "repaired_mixture": (
            audit_mixture(*mixture_pair) if mixture_pair is not None else None
        ),
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
