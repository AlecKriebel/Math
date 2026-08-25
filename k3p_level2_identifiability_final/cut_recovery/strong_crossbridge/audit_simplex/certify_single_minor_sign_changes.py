#!/usr/bin/env python3
"""Produce exact rational opposite-sign witnesses for every residue minor.

The output does *not* decide whether the four Fourier blocks can all have rank
one simultaneously.  It decisively tests a narrower proposed route: a single
2x2 cut minor cannot be strictly one-signed if it has two physical D3+ points
with opposite exact values.
"""

from __future__ import annotations

import collections
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import numpy as np

import search_simplex_homogeneous as audit


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "SINGLE_MINOR_SIGN_CHANGE_WITNESSES.json"
BASE_SEED = 9_071_986
LAMBDA_DENOMINATOR = 10_007
WEIGHT_POOL = np.array(
    [
        1,
        2,
        3,
        5,
        8,
        13,
        21,
        34,
        55,
        89,
        144,
        233,
        377,
        610,
        987,
        1597,
        2584,
        4181,
        6765,
        10946,
        17711,
        28657,
        46368,
        75025,
        121393,
    ],
    dtype=np.int64,
)


def rational_values(raw_edge_weights, lambda_numerators):
    values = []
    for raw in raw_edge_weights:
        total = sum(map(int, raw))
        o, c_vertex, g_vertex, t_vertex, u_vertex = map(int, raw)
        del o
        values.extend(
            (
                Fraction(c_vertex + u_vertex, total),
                Fraction(g_vertex + u_vertex, total),
                Fraction(t_vertex + u_vertex, total),
            )
        )
    values.extend(
        Fraction(int(numerator), LAMBDA_DENOMINATOR)
        for numerator in lambda_numerators
    )
    return tuple(values)


def float_values(raw_edge_weights, lambda_numerators):
    raw = raw_edge_weights.astype(np.float64)
    weights = raw / raw.sum(axis=1, keepdims=True)
    spectra = np.column_stack(
        (
            weights[:, 1] + weights[:, 4],
            weights[:, 2] + weights[:, 4],
            weights[:, 3] + weights[:, 4],
        )
    ).reshape(-1)
    lambdas = lambda_numerators.astype(np.float64) / LAMBDA_DENOMINATOR
    return np.concatenate((spectra, lambdas))


def validate_strict_domain(values, edge_count, inheritance_count):
    for edge in range(edge_count):
        c, g, t = values[3 * edge : 3 * edge + 3]
        if not (
            0 < c < 1
            and 0 < g < 1
            and 0 < t < 1
            and 1 + c - g - t > 0
            and 1 - c + g - t > 0
            and 1 - c - g + t > 0
        ):
            raise AssertionError((edge, c, g, t))
    for value in values[3 * edge_count :]:
        if not 0 < value < 1:
            raise AssertionError(value)
    if len(values) != 3 * edge_count + inheritance_count:
        raise AssertionError("parameter width")


def float_evaluate(polynomial, values):
    answer = 0.0
    for exponent, coefficient in polynomial.items():
        answer += float(coefficient) * float(
            np.prod(np.power(values, np.asarray(exponent, dtype=np.int16)))
        )
    return answer


def exact_evaluate(polynomial, values):
    answer = Fraction(0)
    for exponent, coefficient in polynomial.items():
        term = Fraction(coefficient)
        for value, power in zip(values, exponent):
            term *= value**power
        answer += term
    return answer


def compile_minors(descriptor, coordinate_index, pairs):
    outputs = audit.atlas.output_sparse_polynomials(descriptor)
    answer = []
    for character_sum in range(4):
        for rows in pairs:
            for columns in pairs:
                full, coordinates = audit.minor_polynomial(
                    outputs, coordinate_index, character_sum, rows, columns
                )
                if not full:
                    raise AssertionError((character_sum, rows, columns))
                common, reduced = audit.factor_positive_monomial(full)
                answer.append(
                    {
                        "character_sum": character_sum,
                        "rows": rows,
                        "columns": columns,
                        "coordinate_indices": coordinates,
                        "full": full,
                        "common": common,
                        "reduced": reduced,
                    }
                )
    if len(answer) != 144:
        raise AssertionError(len(answer))
    return answer


def sample_payload(raw_edge_weights, lambda_numerators):
    return {
        "edge_barycentric_integer_weights_O_C_G_T_U": [
            list(map(int, row)) for row in raw_edge_weights
        ],
        "inheritance_numerators": list(map(int, lambda_numerators)),
        "inheritance_denominator": LAMBDA_DENOMINATOR,
    }


def certify_target(target_index, target, coordinate_index, pairs, max_samples):
    descriptor = target["descriptor"]
    minors = compile_minors(descriptor, coordinate_index, pairs)
    rng = np.random.default_rng(BASE_SEED + 1_000_003 * target_index)
    witnesses = [[None, None] for _ in minors]  # negative, positive
    samples = {}
    used_sample_ids = set()
    sample_index = -1
    for sample_index in range(max_samples):
        raw_weights = rng.choice(
            WEIGHT_POOL, size=(descriptor.edge_class_count, 5), replace=True
        )
        lambda_numerators = rng.integers(
            1, LAMBDA_DENOMINATOR, size=descriptor.retic_count, dtype=np.int64
        )
        float_parameters = float_values(raw_weights, lambda_numerators)
        rational_parameters = None
        for minor_index, minor in enumerate(minors):
            approximate = float_evaluate(minor["reduced"], float_parameters)
            sign_index = 1 if approximate > 1e-13 else (0 if approximate < -1e-13 else None)
            if sign_index is None or witnesses[minor_index][sign_index] is not None:
                continue
            if rational_parameters is None:
                rational_parameters = rational_values(raw_weights, lambda_numerators)
                validate_strict_domain(
                    rational_parameters,
                    descriptor.edge_class_count,
                    descriptor.retic_count,
                )
            reduced_value = exact_evaluate(minor["reduced"], rational_parameters)
            exact_sign_index = 1 if reduced_value > 0 else (0 if reduced_value < 0 else None)
            if exact_sign_index != sign_index:
                continue
            full_value = exact_evaluate(minor["full"], rational_parameters)
            if not full_value or (full_value > 0) != (reduced_value > 0):
                raise AssertionError((minor_index, reduced_value, full_value))
            witnesses[minor_index][sign_index] = {
                "sample_id": sample_index,
                "reduced_value": str(reduced_value),
                "full_minor_value": str(full_value),
            }
            used_sample_ids.add(sample_index)
        if all(negative is not None and positive is not None for negative, positive in witnesses):
            break
        # Keep only used samples, but record them at the time they are first used.
        if sample_index in used_sample_ids:
            samples[sample_index] = sample_payload(raw_weights, lambda_numerators)
    else:
        missing = [
            index
            for index, (negative, positive) in enumerate(witnesses)
            if negative is None or positive is None
        ]
        raise RuntimeError((target_index, "missing opposite signs", missing))

    # The terminal sample may have completed the collection after the in-loop
    # storage point.
    if sample_index in used_sample_ids and sample_index not in samples:
        samples[sample_index] = sample_payload(raw_weights, lambda_numerators)

    public_minors = []
    for minor, (negative, positive) in zip(minors, witnesses):
        if negative is None or positive is None:
            raise AssertionError("incomplete")
        public_minors.append(
            {
                "character_sum": minor["character_sum"],
                "rows": list(minor["rows"]),
                "columns": list(minor["columns"]),
                "coordinate_indices": list(minor["coordinate_indices"]),
                "positive_monomial_exponent": list(minor["common"]),
                "full_polynomial_sha256": audit.polynomial_digest(minor["full"]),
                "reduced_polynomial_sha256": audit.polynomial_digest(minor["reduced"]),
                "negative_witness": negative,
                "positive_witness": positive,
            }
        )
    return {
        "target_index": target_index,
        "record_id": target["record_id"],
        "old_split": target["old_split"],
        "old_order": target["old_order"],
        "descriptor_sha256": audit.cross.digest(audit.cross.descriptor_payload(descriptor)),
        "sample_count_examined": sample_index + 1,
        "stored_sample_count": len(samples),
        "samples": {str(key): value for key, value in sorted(samples.items())},
        "minor_count": len(public_minors),
        "minors_with_exact_opposite_sign_witnesses": len(public_minors),
        "minors": public_minors,
    }


def main():
    upstream = json.loads(audit.UPSTREAM_REPORT.read_text())
    unresolved = tuple(upstream["unsolved_target_indices"])
    _, _, _, targets = audit.cross.build_universes()
    assignments = audit.atlas.k3p_assignments(4)
    coordinate_index = {
        assignment: index for index, assignment in enumerate(assignments)
    }
    pairs = tuple(itertools.combinations(range(4), 2))
    records = []
    for target_index in unresolved:
        record = certify_target(
            target_index,
            targets[target_index],
            coordinate_index,
            pairs,
            max_samples=2_000,
        )
        records.append(record)
        print(
            json.dumps(
                {
                    "target_index": target_index,
                    "record_id": record["record_id"],
                    "samples": record["sample_count_examined"],
                    "minors": record["minor_count"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
    payload = {
        "schema": "k3p-d3plus-single-cut-minor-sign-change-witnesses-v1",
        "status": "EXACT_COMPLETE",
        "claim": (
            "Every one of the 144 Fourier-block 2x2 minors for each of the 24 "
            "residue target directions takes both signs at strict rational D3+ "
            "edge spectra and strict rational inheritance parameters."
        ),
        "scope_warning": (
            "This rules out every universal strictly signed single-minor proof. "
            "It does not exhibit a point where all minors vanish simultaneously."
        ),
        "domain_parameterization": (
            "positive integer weights on O,C,G,T,U normalized independently per edge"
        ),
        "base_seed": BASE_SEED,
        "weight_pool": list(map(int, WEIGHT_POOL)),
        "inheritance_denominator": LAMBDA_DENOMINATOR,
        "target_count": len(records),
        "minor_count_per_target": 144,
        "total_minors_with_opposite_sign_witnesses": sum(
            record["minors_with_exact_opposite_sign_witnesses"] for record in records
        ),
        "inputs": {
            "upstream_report_sha256": audit.sha_file(audit.UPSTREAM_REPORT),
            "crossbridge_compiler_sha256": audit.sha_file(
                audit.PARENT / "explore_crossbridge_atlas.py"
            ),
            "k3p_compiler_sha256": audit.sha_file(audit.cross.ATLAS_PATH),
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "targets": payload["target_count"],
                "opposite_sign_minors": payload[
                    "total_minors_with_opposite_sign_witnesses"
                ],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
