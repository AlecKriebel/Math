#!/usr/bin/env python3
"""Verify an exact degree-13 dual obstruction for one fixed atom table.

The certificate proves infeasibility of a finite pair/triple relaxation
whose eleven pair-inner-product atoms and multiplicities are fixed.  It is
not a universal obstruction to centered tight 41-point codes: general
codes are not required to use this atom table.

The dual PSD matrices are supplied as rational Gram factors.  All remaining
calculations use only Python's standard library and ``fractions.Fraction``.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "fixed_atomic_degree13_dual_certificate.json"
PAIR_SOURCE = (
    HERE.parent
    / "centered_tight_frame_endpoint"
    / "centered_tight_bv_pseudodistribution.json"
)
HELPER_PATH = HERE / "verify_conditional_bv_degree12.py"

SPECIFICATION = importlib.util.spec_from_file_location(
    "verify_conditional_bv_degree12", HELPER_PATH
)
assert SPECIFICATION is not None and SPECIFICATION.loader is not None
helper = importlib.util.module_from_spec(SPECIFICATION)
SPECIFICATION.loader.exec_module(helper)


def expected_complements() -> dict[int, list[int]]:
    complements = {
        0: list(range(3, 12)),
        1: list(range(2, 11)),
        2: list(range(1, 11)),
    }
    complements.update(
        {degree: list(range(11)) for degree in range(3, 14)}
    )
    return complements


def exact_capacity_rows(
    nodes: list[Q],
    alpha: list[Q],
    triples: list[tuple[int, int, int]],
) -> list[tuple[list[Q], Q, dict[str, object]]]:
    """Reconstruct the 48 stratified capacity inequalities."""

    nonpositive = tuple(
        index for index, node in enumerate(nodes) if node <= 0
    )
    positive = tuple(
        index for index, node in enumerate(nodes) if node > 0
    )
    rows = []
    for lower in range(len(nonpositive)):
        for upper in range(lower, len(nonpositive)):
            base_indices = nonpositive[lower : upper + 1]
            base_set = set(base_indices)
            base_upper = nodes[base_indices[-1]]
            for high_index in positive:
                high = nodes[high_index]
                capacity = helper.common_pair_capacity(
                    2 * high * high / (1 + base_upper)
                )
                if capacity is None:
                    continue
                coefficients = [
                    Q(
                        sum(
                            triple[position] in base_set
                            and all(
                                nodes[triple[other]] >= high
                                for other in range(3)
                                if other != position
                            )
                            for position in range(3)
                        )
                    )
                    for triple in triples
                ]
                bound = (
                    3
                    * capacity
                    * sum(alpha[index] for index in base_indices)
                )
                rows.append(
                    (
                        coefficients,
                        bound,
                        {
                            "base_indices": list(base_indices),
                            "high_index": high_index,
                            "capacity": capacity,
                        },
                    )
                )
    assert len(rows) == 48
    return rows


def ordered_orbit_terms(
    nodes: list[Q],
    triples: list[tuple[int, int, int]],
) -> list[tuple[int, int, int, Q, Q, Q]]:
    """Expand each unordered triple orbit into ordered occurrences."""

    index_of = {node: index for index, node in enumerate(nodes)}
    ordered = []
    for orbit_index, triple in enumerate(triples):
        values = tuple(nodes[index] for index in triple)
        orbit = sorted(set(itertools.permutations(values)))
        coefficient = Q(1, len(orbit))
        for u, v, t in orbit:
            area = (1 - u * u) * (1 - v * v)
            displacement = t - u * v
            assert area > 0
            assert area - displacement * displacement >= 0
            ordered.append(
                (
                    orbit_index,
                    index_of[u],
                    index_of[v],
                    coefficient,
                    area,
                    displacement,
                )
            )
    return ordered


def gram_matrix(factors: list[list[Q]]) -> list[list[Q]]:
    """Return the PSD matrix represented by the supplied row factors."""

    assert factors
    size = len(factors[0])
    assert all(len(factor) == size for factor in factors)
    return [
        [
            sum(factor[i] * factor[j] for factor in factors)
            for j in range(size)
        ]
        for i in range(size)
    ]


def dual_coefficients(
    nodes: list[Q],
    alpha: list[Q],
    triples: list[tuple[int, int, int]],
    factors_by_degree: dict[int, list[list[Q]]],
    complements: dict[int, list[int]],
) -> tuple[list[Q], Q]:
    """Compute f_j=sum_k <Q_k,F_kj> and sum_k <Q_k,D_k>."""

    ordered = ordered_orbit_terms(nodes, triples)
    sequences = {
        (area, displacement): helper.normalized_transverse_sequences(
            area, displacement, 7
        )
        for (
            _orbit,
            _i,
            _j,
            _coefficient,
            area,
            displacement,
        ) in ordered
    }
    orbit_coefficients = [Q(0)] * len(triples)
    constant = Q(0)

    for degree, factors in factors_by_degree.items():
        complement = complements[degree]
        local_index = {
            original: index
            for index, original in enumerate(complement)
        }
        dual_matrix = gram_matrix(factors)
        assert len(dual_matrix) == len(complement)

        if degree == 0:
            for i, original_i in enumerate(complement):
                for j, original_j in enumerate(complement):
                    entry = Q(0)
                    if original_i == original_j and original_i < 11:
                        entry += alpha[original_i]
                    if original_i < 11 and original_j == 11:
                        entry += alpha[original_i]
                    if original_i == 11 and original_j < 11:
                        entry += alpha[original_j]
                    if original_i == original_j == 11:
                        entry += 1
                    constant += dual_matrix[i][j] * entry
            for (
                orbit,
                i,
                j,
                coefficient,
                _area,
                _displacement,
            ) in ordered:
                if i in local_index and j in local_index:
                    orbit_coefficients[orbit] += (
                        dual_matrix[local_index[i]][local_index[j]]
                        * coefficient
                    )
            continue

        for i, original in enumerate(complement):
            diagonal = alpha[original]
            if degree % 2:
                diagonal *= 1 - nodes[original] * nodes[original]
            constant += dual_matrix[i][i] * diagonal
        parity = degree % 2
        sequence_index = degree // 2
        for (
            orbit,
            i,
            j,
            coefficient,
            area,
            displacement,
        ) in ordered:
            if i not in local_index or j not in local_index:
                continue
            kernel = sequences[(area, displacement)][parity][
                sequence_index
            ]
            orbit_coefficients[orbit] += (
                dual_matrix[local_index[i]][local_index[j]]
                * coefficient
                * kernel
            )
    return orbit_coefficients, constant


def verify(
    certificate_path: Path = CERTIFICATE,
    pair_source_path: Path = PAIR_SOURCE,
) -> dict[str, object]:
    certificate_bytes = certificate_path.read_bytes()
    certificate = json.loads(certificate_bytes)
    source_bytes = pair_source_path.read_bytes()
    source = json.loads(source_bytes)

    assert certificate["schema"] == (
        "centered-tight-fixed-atomic-degree13-dual-v1"
    )
    assert certificate["status"] == (
        "EXACT DUAL CERTIFICATE FOR A FIXED ATOM TABLE; "
        "NOT A UNIVERSAL CODE OBSTRUCTION"
    )
    assert certificate["maximum_bv_degree"] == 13
    assert certificate["source_pair_certificate"] == pair_source_path.name
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    assert certificate["source_pair_sha256"] == source_hash
    assert certificate["scope_warning"] == (
        "the eleven nodes and their pair multiplicities are assumptions"
    )

    nodes = [Q(value) for value in source["nodes"]]
    alpha = [Q(value) for value in source["alpha"]]
    triples = [tuple(value) for value in source["triple_orbits"]]
    assert nodes == [
        Q(-4, 5),
        Q(-3, 4),
        Q(-1, 2),
        Q(-7, 20),
        Q(-3, 10),
        Q(-1, 4),
        Q(-3, 20),
        Q(-1, 20),
        Q(0),
        Q(3, 10),
        Q(1, 2),
    ]
    assert alpha == [2, 2, 4, 2, 2, 2, 2, 8, 2, 2, 12]
    feasible = []
    for triple in itertools.combinations_with_replacement(
        range(len(nodes)), 3
    ):
        u, v, t = (nodes[index] for index in triple)
        if 1 + 2 * u * v * t - u * u - v * v - t * t >= 0:
            feasible.append(triple)
    assert triples == feasible
    assert len(triples) == 246

    all_conditional_rows = helper.conditional_rows(
        nodes, triples, alpha
    )
    row_indices = [
        int(index) for index in certificate["conditional_row_indices"]
    ]
    assert len(row_indices) == len(set(row_indices)) == 40
    assert all(
        0 <= index < len(all_conditional_rows)
        for index in row_indices
    )
    equality_rows = [
        all_conditional_rows[index] for index in row_indices
    ]
    equality_denominator = int(
        certificate["equality_dual_denominator"]
    )
    equality_dual = [
        Q(int(value), equality_denominator)
        for value in certificate["equality_dual_numerators"]
    ]
    assert equality_denominator > 0
    assert len(equality_dual) == len(equality_rows)

    capacity_rows = exact_capacity_rows(nodes, alpha, triples)
    capacity_denominator = int(
        certificate["capacity_dual_denominator"]
    )
    capacity_dual = [Q(0)] * len(capacity_rows)
    for index_text, numerator in certificate[
        "capacity_dual_numerators"
    ].items():
        index = int(index_text)
        assert 0 <= index < len(capacity_dual)
        capacity_dual[index] = Q(
            int(numerator), capacity_denominator
        )
    assert capacity_denominator > 0
    assert all(value >= 0 for value in capacity_dual)

    complements = expected_complements()
    stored_complements = {
        int(degree): [int(index) for index in indices]
        for degree, indices in certificate["block_complements"].items()
    }
    assert stored_complements == complements
    factor_denominator = int(certificate["factor_denominator"])
    assert factor_denominator > 0
    factors_by_degree = {}
    for degree_text, stored_factors in certificate[
        "block_factor_numerators"
    ].items():
        degree = int(degree_text)
        assert 0 <= degree <= 13
        factors = [
            [
                Q(int(numerator), factor_denominator)
                for numerator in factor
            ]
            for factor in stored_factors
        ]
        assert factors
        assert all(
            len(factor) == len(complements[degree])
            for factor in factors
        )
        factors_by_degree[degree] = factors
    assert set(factors_by_degree) == {
        0,
        1,
        2,
        3,
        4,
        5,
        7,
        8,
        9,
        13,
    }
    assert sum(len(value) for value in factors_by_degree.values()) == 18

    radial_coefficients, radial_constant = dual_coefficients(
        nodes,
        alpha,
        triples,
        factors_by_degree,
        complements,
    )
    capacity_coefficients = [
        sum(
            capacity_dual[index] * capacity_rows[index][0][orbit]
            for index in range(len(capacity_rows))
        )
        for orbit in range(len(triples))
    ]
    equality_coefficients = [
        sum(
            equality_dual[index] * equality_rows[index][0][orbit]
            for index in range(len(equality_rows))
        )
        for orbit in range(len(triples))
    ]
    orbit_slacks = [
        capacity_coefficients[orbit]
        - radial_coefficients[orbit]
        + equality_coefficients[orbit]
        for orbit in range(len(triples))
    ]
    assert all(slack > 0 for slack in orbit_slacks)

    capacity_constant = sum(
        dual * row[1]
        for dual, row in zip(capacity_dual, capacity_rows)
    )
    equality_constant = sum(
        dual * row[1]
        for dual, row in zip(equality_dual, equality_rows)
    )
    dual_objective = (
        radial_constant + capacity_constant + equality_constant
    )
    assert dual_objective < 0

    active_capacity_indices = [
        index
        for index, value in enumerate(capacity_dual)
        if value > 0
    ]
    assert active_capacity_indices == [27, 33, 38, 42, 43, 45]
    return {
        "status": "PASS",
        "scope": (
            "infeasibility of the fixed eleven-node pair/triple "
            "relaxation; not a universal centered-code obstruction"
        ),
        "certificate_sha256": hashlib.sha256(
            certificate_bytes
        ).hexdigest(),
        "source_pair_sha256": source_hash,
        "conditional_rows_used": len(equality_rows),
        "capacity_rows_available": len(capacity_rows),
        "active_capacity_indices": active_capacity_indices,
        "bv_degrees_with_nonzero_dual_blocks": sorted(
            factors_by_degree
        ),
        "dual_gram_factors": sum(
            len(value) for value in factors_by_degree.values()
        ),
        "minimum_orbit_slack": str(min(orbit_slacks)),
        "dual_objective": str(dual_objective),
        "conclusion": (
            "no nonnegative triple-orbit measure on this fixed atom "
            "table satisfies the selected conditional equations, "
            "stratified capacities, and radial BV blocks through degree 13"
        ),
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
