#!/usr/bin/env python3
"""Exact replay for the theta0 repair-1 quintic port-orbit separator.

This is a research-side certificate.  It reconstructs the graph-derived K2P
descriptor without loading either atlas pickle, proves that the displayed
quintic pulls back to zero, and checks that its port orbit separates exactly
the 22 relabelings outside the semi-directed symmetry group.
"""

from __future__ import annotations

if not __debug__:
    raise SystemExit("exact replay requires assertions; do not use python -O")

import hashlib
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "atlas"
sys.path.insert(0, str(ATLAS))

from k2p_atlas_core import (  # noqa: E402
    ct_orbit_rep,
    eval_descriptor,
    model_descriptor_fast2,
    orbit_assignments,
    output_sparse_polynomials,
    relabel_record,
    source_supports,
    sparse_lincomb,
    sparse_mul_many,
)


# Coordinate i is q_h for h=orbit_assignments(4)[i].  F is homogeneous of
# degree 5 and K2P pendant multidegree (2,1,1,1,2,1,1,1).
F = (
    ((0, 0, 11, 17, 35), 1),
    ((0, 0, 11, 25, 35), -1),
    ((0, 0, 17, 19, 28), -2),
    ((0, 0, 19, 25, 28), 2),
    ((0, 1, 11, 14, 35), -2),
    ((0, 1, 13, 24, 33), 2),
    ((0, 1, 14, 19, 28), 4),
    ((0, 1, 21, 24, 26), -2),
    ((0, 2, 10, 21, 32), 2),
    ((0, 2, 11, 17, 33), 1),
    ((0, 2, 11, 21, 29), -2),
    ((0, 2, 11, 23, 33), -2),
    ((0, 2, 11, 25, 33), 1),
    ((0, 2, 14, 21, 27), -2),
    ((0, 4, 10, 11, 35), 2),
    ((0, 4, 10, 19, 28), -4),
    ((0, 4, 12, 13, 33), -2),
    ((0, 4, 12, 21, 26), 2),
    ((0, 5, 11, 13, 33), -2),
    ((0, 5, 11, 21, 26), 2),
    ((0, 7, 11, 17, 28), 1),
    ((0, 7, 11, 25, 28), -1),
    ((0, 9, 10, 13, 32), -2),
    ((0, 9, 11, 13, 29), 2),
    ((0, 9, 11, 17, 26), -1),
    ((0, 9, 11, 23, 26), 2),
    ((0, 9, 11, 25, 26), -1),
    ((0, 9, 13, 14, 27), 2),
    ((1, 7, 11, 14, 28), -2),
    ((2, 3, 11, 11, 33), 2),
    ((3, 9, 11, 11, 26), -2),
    ((4, 7, 10, 11, 28), 2),
)


def inverse(permutation):
    result = [0] * len(permutation)
    for index, image in enumerate(permutation):
        result[image] = index
    return tuple(result)


def coordinate_map(permutation):
    """Map q_h to q_(h o permutation), modulo global C/T exchange."""
    assignments = orbit_assignments(4)
    index = {assignment: offset for offset, assignment in enumerate(assignments)}
    return tuple(
        index[ct_orbit_rep(tuple(assignment[permutation[j]] for j in range(4)))]
        for assignment in assignments
    )


def transform(polynomial, permutation):
    mapping = coordinate_map(permutation)
    return tuple(
        (tuple(sorted(mapping[index] for index in monomial)), coefficient)
        for monomial, coefficient in polynomial
    )


def pullback(polynomial, outputs, product_cache=None):
    cache = {} if product_cache is None else product_cache
    columns = []
    coefficients = []
    for monomial, coefficient in polynomial:
        if monomial not in cache:
            cache[monomial] = sparse_mul_many([outputs[index] for index in monomial])
        columns.append(cache[monomial])
        coefficients.append(coefficient)
    return sparse_lincomb(columns, coefficients)


def digest(value):
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()


def evaluate_coordinate_polynomial(polynomial, coordinates):
    value = Fraction(0)
    for monomial, coefficient in polynomial:
        term = Fraction(coefficient)
        for index in monomial:
            term *= coordinates[index]
        value += term
    return value


def main():
    source_record = source_supports()[1]
    assert source_record.core_id == "theta0" and source_record.repair_index == 1
    source_descriptor = model_descriptor_fast2(source_record.graph)
    source_outputs = output_sparse_polynomials(source_descriptor)
    source_cache = {}

    assert not pullback(F, source_outputs, source_cache)

    identity = (0, 1, 2, 3)
    semidirected_symmetry = (2, 1, 0, 3)
    zero_permutations = []
    rows = []
    for class_id, permutation in enumerate(itertools.permutations(range(4)), 24):
        # If target points are A_P x, a target invariant is
        # f_P=(A_P^*)^{-1}F=A_(P^-1)^*F.
        target_invariant = transform(F, inverse(permutation))
        source_pullback = pullback(target_invariant, source_outputs, source_cache)

        # Independent direct target-side replay.
        target_record = relabel_record(source_record, permutation)
        target_outputs = output_sparse_polynomials(model_descriptor_fast2(target_record.graph))
        assert not pullback(target_invariant, target_outputs)

        if not source_pullback:
            zero_permutations.append(permutation)
        witness = (
            next(iter(sorted(source_pullback.items(), key=lambda row: repr(row[0]))))
            if source_pullback
            else None
        )
        rows.append(
            {
                "class_id": class_id,
                "permutation": permutation,
                "target_pullback_zero": True,
                "source_pullback_terms": len(source_pullback),
                "source_pullback_sha256": digest(
                    sorted(source_pullback.items(), key=lambda row: repr(row[0]))
                )
                if source_pullback
                else None,
                "source_pullback_witness": {
                    "parameter_exponent": witness[0],
                    "coefficient": str(witness[1]),
                }
                if witness
                else None,
            }
        )

    assert zero_permutations == [identity, semidirected_symmetry]

    # One shared strict physical witness separates all 22 port orbits at once.
    edge_pairs = tuple(
        (Fraction(1, 4), Fraction(index + 1, 10))
        for index in range(source_descriptor.edge_class_count)
    )
    lambdas = (Fraction(1, 3), Fraction(2, 3))
    for s_value, g_value in edge_pairs:
        assert 0 < s_value < 1
        assert 0 < g_value < 1
        assert g_value > 2 * s_value - 1
    assert all(0 < value < 1 for value in lambdas)
    coordinates = eval_descriptor(source_descriptor, edge_pairs, lambdas)
    strict_value_rows = []
    strict_zero_permutations = []
    for permutation in itertools.permutations(range(4)):
        target_invariant = transform(F, inverse(permutation))
        value = evaluate_coordinate_polynomial(target_invariant, coordinates)
        if value:
            strict_value_rows.append({"permutation": permutation, "value": str(value)})
        else:
            strict_zero_permutations.append(permutation)
    assert strict_zero_permutations == [identity, semidirected_symmetry]
    assert len(strict_value_rows) == 22
    assert all(Fraction(row["value"]) != 0 for row in strict_value_rows)
    payload = {
        "schema": "k2p-theta0-repair1-quintic-port-orbit-v1",
        "coordinate_assignments": orbit_assignments(4),
        "invariant": F,
        "invariant_sha256": digest(F),
        "invariant_degree": 5,
        "invariant_multidegree": (2, 1, 1, 1, 2, 1, 1, 1),
        "zero_permutations": zero_permutations,
        "semidirected_symmetry_generator": semidirected_symmetry,
        "double_coset_representative_classes": (25, 26, 27, 28, 29, 31),
        "separated_permutation_count": 22,
        "shared_strict_D_plus_witness": {
            "edge_pairs": tuple(
                {"s": str(s_value), "g": str(g_value)}
                for s_value, g_value in edge_pairs
            ),
            "inheritance_probabilities": tuple(str(value) for value in lambdas),
            "all_edge_pairs_verified_in_D_plus": True,
            "ordered_nonzero_value_rows": strict_value_rows,
            "ordered_nonzero_value_rows_canonical_json": {
                "sort_keys": True,
                "separators": [",", ":"],
            },
            "ordered_nonzero_value_rows_sha256": digest(strict_value_rows),
            "independent_review_reported_digest_prefix": "ef9be8",
        },
        "rows": rows,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
