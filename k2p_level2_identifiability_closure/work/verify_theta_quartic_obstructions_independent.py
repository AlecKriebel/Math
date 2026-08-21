#!/usr/bin/env python3
"""Independent exact replay of the remaining theta quartic obstructions.

No atlas pickle is loaded.  Every map is rebuilt from the directed core
grammar, and all polynomial identities are checked in the integer/rational
parameter ring represented by sparse exponent dictionaries.
"""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "package/referee/k2p_offline_sweep_portable/atlas"
sys.path.insert(0, str(ATLAS))

from k2p_atlas_core import (  # noqa: E402
    coordinate_weights,
    ct_orbit_rep,
    eval_descriptor,
    mixed_relation_exact,
    model_descriptor_fast2,
    orbit_assignments,
    output_sparse_polynomials,
    relabel_record,
    source_supports,
    sparse_lincomb,
    sparse_mul_many,
    target_completions,
)


F112 = (
    ((0, 15, 16, 18), 1),
    ((0, 16, 18, 23), 1),
    ((0, 20, 22, 23), -1),
    ((1, 14, 16, 18), 1),
    ((3, 11, 16, 18), -2),
    ((3, 11, 20, 22), 1),
    ((4, 12, 18, 22), -1),
    ((8, 10, 14, 16), -1),
    ((8, 12, 14, 22), 1),
)

F113 = (
    ((0, 16, 17, 29), 1),
    ((0, 16, 23, 29), -1),
    ((0, 17, 22, 31), -1),
    ((0, 22, 23, 31), 1),
    ((1, 14, 16, 29), -1),
    ((1, 14, 22, 31), 1),
    ((3, 11, 16, 29), 2),
    ((3, 11, 22, 31), -1),
    ((3, 14, 16, 27), -1),
    ((5, 11, 22, 29), -1),
    ((5, 14, 22, 27), 1),
)

F48 = (
    ((0, 15, 16, 32), 1),
    ((0, 16, 23, 32), 1),
    ((0, 23, 24, 30), -1),
    ((1, 14, 16, 32), 1),
    ((3, 11, 16, 32), -2),
    ((3, 11, 24, 30), 1),
    ((4, 14, 16, 27), -1),
    ((6, 10, 24, 32), -1),
    ((6, 14, 24, 27), 1),
)


E = (0, 1, 2, 3)
A = (1, 0, 2, 3)  # (0 1), a source-4 symmetry
B = (0, 1, 3, 2)  # (2 3)
H = (1, 0, 3, 2)  # (0 1)(2 3), a target-822 symmetry
TARGET_PERMUTATIONS = (E, B, A, H)


def digest(value):
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()


def transform(polynomial, permutation):
    assignments = orbit_assignments(4)
    index = {assignment: offset for offset, assignment in enumerate(assignments)}
    mapping = tuple(
        index[ct_orbit_rep(tuple(assignment[permutation[j]] for j in range(4)))]
        for assignment in assignments
    )
    return tuple(
        (tuple(sorted(mapping[i] for i in monomial)), coefficient)
        for monomial, coefficient in polynomial
    )


def pullback(polynomial, outputs, cache=None):
    product_cache = {} if cache is None else cache
    columns = []
    coefficients = []
    for monomial, coefficient in polynomial:
        if monomial not in product_cache:
            product_cache[monomial] = sparse_mul_many(
                [outputs[index] for index in monomial]
            )
        columns.append(product_cache[monomial])
        coefficients.append(coefficient)
    return sparse_lincomb(columns, coefficients)


def multidegree(polynomial):
    weights = coordinate_weights(4)
    degrees = {
        tuple(sum(weights[index][slot] for index in monomial) for slot in range(8))
        for monomial, _coefficient in polynomial
    }
    assert len(degrees) == 1
    return next(iter(degrees))


def witness(sparse_polynomial):
    exponent, coefficient = next(
        iter(sorted(sparse_polynomial.items(), key=lambda row: repr(row[0])))
    )
    return {"parameter_exponent": exponent, "coefficient": str(coefficient)}


def evaluate_coordinate_polynomial(polynomial, coordinates):
    value = Fraction(0)
    for monomial, coefficient in polynomial:
        term = Fraction(coefficient)
        for index in monomial:
            term *= coordinates[index]
        value += term
    return value


def mutation_audit(name, polynomial, target_outputs):
    assert not pullback(polynomial, target_outputs)
    coefficient_survivors = []
    for term_index, (monomial, coefficient) in enumerate(polynomial):
        mutation = list(polynomial)
        mutation[term_index] = (monomial, coefficient + 1)
        if not pullback(mutation, target_outputs):
            coefficient_survivors.append(term_index)

    index_survivors = []
    for term_index, (monomial, coefficient) in enumerate(polynomial):
        for factor_index in range(4):
            mutated_monomial = list(monomial)
            mutated_monomial[factor_index] = (mutated_monomial[factor_index] + 1) % 36
            mutation = list(polynomial)
            mutation[term_index] = (tuple(sorted(mutated_monomial)), coefficient)
            if not pullback(mutation, target_outputs):
                index_survivors.append((term_index, factor_index))

    assert not coefficient_survivors
    assert not index_survivors
    return {
        "name": name,
        "coefficient_mutations": len(polynomial),
        "coefficient_mutation_survivors": coefficient_survivors,
        "index_mutations": 4 * len(polynomial),
        "index_mutation_survivors": index_survivors,
    }


def main():
    sources = source_supports()
    source_records = {2: sources[2], 3: sources[3], 4: sources[4]}
    assert (sources[2].core_id, sources[2].repair_index) == ("theta1", 0)
    assert (sources[3].core_id, sources[3].repair_index) == ("theta1", 1)
    assert (sources[4].core_id, sources[4].repair_index) == ("theta3", 0)

    target_base = target_completions(4, True)[822]
    assert (target_base.core_id, target_base.repair_index, target_base.dummy_labels) == (
        "theta3",
        1,
        (),
    )

    # Independent topology/symmetry audit.
    assert mixed_relation_exact(sources[2].graph, sources[3].graph) == "isomorphic"
    assert model_descriptor_fast2(sources[2].graph) == model_descriptor_fast2(
        sources[3].graph
    )
    assert (
        mixed_relation_exact(sources[4].graph, relabel_record(sources[4], A).graph)
        == "isomorphic"
    )
    assert (
        mixed_relation_exact(target_base.graph, relabel_record(target_base, H).graph)
        == "isomorphic"
    )

    source_outputs = {
        index: output_sparse_polynomials(model_descriptor_fast2(record.graph))
        for index, record in source_records.items()
    }
    source_caches = {index: {} for index in source_outputs}
    target_outputs = {
        permutation: output_sparse_polynomials(
            model_descriptor_fast2(relabel_record(target_base, permutation).graph)
        )
        for permutation in TARGET_PERMUTATIONS
    }

    expected_weights = {
        "F112": (3, 0, 2, 1, 1, 1, 2, 1),
        "F113": (2, 1, 3, 0, 1, 1, 2, 1),
        "F48": (2, 1, 3, 0, 2, 1, 1, 1),
    }
    polynomials = {"F112": F112, "F113": F113, "F48": F48}
    for name, polynomial in polynomials.items():
        assert multidegree(polynomial) == expected_weights[name]

    # The fourth source-4 obstruction is obtained only by the proven source
    # symmetry A; its multidegree is the corresponding port permutation.
    F48_A = transform(F48, A)
    assert multidegree(F48_A) == (3, 0, 2, 1, 2, 1, 1, 1)

    coverage = []
    for source_index in (2, 3):
        # Target automorphism H pairs E with H and B with A.
        for class_id, permutation, polynomial_name, polynomial in (
            (112, E, "F112", F112),
            (113, B, "F113", F113),
            (114, A, "F113", F113),
            (115, H, "F112", F112),
        ):
            target_pullback = pullback(polynomial, target_outputs[permutation])
            source_pullback = pullback(
                polynomial, source_outputs[source_index], source_caches[source_index]
            )
            assert not target_pullback
            assert source_pullback
            coverage.append(
                {
                    "source_index": source_index,
                    "class_id": class_id,
                    "target_permutation": permutation,
                    "polynomial": polynomial_name,
                    "target_pullback_zero": True,
                    "source_pullback_terms": len(source_pullback),
                    "source_pullback_sha256": digest(
                        sorted(source_pullback.items(), key=lambda row: repr(row[0]))
                    ),
                    "source_pullback_witness": witness(source_pullback),
                }
            )

    # Source-4 automorphism A and target automorphism H give one double coset.
    for class_id, permutation, polynomial_name, polynomial in (
        (8, E, "F48", F48),
        (9, B, "A_A^*F48", F48_A),
        (10, A, "A_A^*F48", F48_A),
        (11, H, "F48", F48),
    ):
        target_pullback = pullback(polynomial, target_outputs[permutation])
        source_pullback = pullback(polynomial, source_outputs[4], source_caches[4])
        assert not target_pullback
        assert source_pullback
        coverage.append(
            {
                "source_index": 4,
                "class_id": class_id,
                "target_permutation": permutation,
                "polynomial": polynomial_name,
                "target_pullback_zero": True,
                "source_pullback_terms": len(source_pullback),
                "source_pullback_sha256": digest(
                    sorted(source_pullback.items(), key=lambda row: repr(row[0]))
                ),
                "source_pullback_witness": witness(source_pullback),
            }
        )

    assert len(coverage) == 12

    # A single canonical rule gives a strict-D+ rational witness on each
    # source descriptor: edge class i gets (1/4,(i+1)/10), and both
    # inheritance probabilities are strictly between zero and one.
    strict_edge_pairs = tuple(
        (Fraction(1, 4), Fraction(index + 1, 10)) for index in range(8)
    )
    strict_lambdas = (Fraction(1, 3), Fraction(2, 3))
    for s_value, g_value in strict_edge_pairs:
        assert 0 < s_value < 1
        assert 0 < g_value < 1
        assert g_value > 2 * s_value - 1
    assert all(0 < value < 1 for value in strict_lambdas)
    strict_coordinates = {}
    for source_index, record in source_records.items():
        descriptor = model_descriptor_fast2(record.graph)
        assert descriptor.edge_class_count == len(strict_edge_pairs)
        strict_coordinates[source_index] = eval_descriptor(
            descriptor, strict_edge_pairs, strict_lambdas
        )
    strict_case_polynomial = {
        (2, 112): F112,
        (2, 113): F113,
        (2, 114): F113,
        (2, 115): F112,
        (3, 112): F112,
        (3, 113): F113,
        (3, 114): F113,
        (3, 115): F112,
        (4, 8): F48,
        (4, 9): F48_A,
        (4, 10): F48_A,
        (4, 11): F48,
    }
    strict_value_rows = []
    for row in coverage:
        key = (row["source_index"], row["class_id"])
        value = evaluate_coordinate_polynomial(
            strict_case_polynomial[key], strict_coordinates[key[0]]
        )
        assert value
        strict_value_rows.append(
            {
                "source_index": key[0],
                "class_id": key[1],
                "value": str(value),
            }
        )
    assert len(strict_value_rows) == 12
    assert all(Fraction(row["value"]) != 0 for row in strict_value_rows)

    mutation_results = (
        mutation_audit("F112", F112, target_outputs[E]),
        mutation_audit("F113", F113, target_outputs[B]),
        mutation_audit("F48", F48, target_outputs[E]),
    )

    payload = {
        "schema": "k2p-theta-quartic-obstruction-independent-replay-v1",
        "coordinate_assignments": orbit_assignments(4),
        "polynomials": polynomials,
        "polynomial_sha256": {
            name: digest(polynomial) for name, polynomial in polynomials.items()
        },
        "multidegrees": expected_weights,
        "transported_F48_A": F48_A,
        "transported_F48_A_sha256": digest(F48_A),
        "symmetries": {
            "source2_source3_same_descriptor": True,
            "source4_generator": A,
            "target822_generator": H,
        },
        "bridge_multihomogeneous": True,
        "shared_strict_D_plus_witness": {
            "edge_pairs": tuple(
                {"s": str(s_value), "g": str(g_value)}
                for s_value, g_value in strict_edge_pairs
            ),
            "inheritance_probabilities": tuple(
                str(value) for value in strict_lambdas
            ),
            "all_edge_pairs_verified_in_D_plus": True,
            "ordered_nonzero_value_rows": strict_value_rows,
            "ordered_nonzero_value_rows_canonical_json": {
                "sort_keys": True,
                "separators": [",", ":"],
            },
            "ordered_nonzero_value_rows_sha256": digest(strict_value_rows),
        },
        "coverage": coverage,
        "covered_record_count": len(coverage),
        "mutations": mutation_results,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
