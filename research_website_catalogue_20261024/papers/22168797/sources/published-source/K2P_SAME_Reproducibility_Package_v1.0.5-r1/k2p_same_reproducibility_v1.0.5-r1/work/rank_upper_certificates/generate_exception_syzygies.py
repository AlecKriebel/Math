#!/usr/bin/env python3
"""Generate and replay primitive polynomial log-kernels for orbit exceptions."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import pickle
import time
from collections import defaultdict
from pathlib import Path

import sympy as sp
from sympy.polys.matrices import DomainMatrix

from k2p_atlas_core import (
    default_exact_point,
    descriptor_jacobian,
    exact_rank_pivots,
    output_sparse_polynomials,
)
from select_missing_supports import base_evaluated_vectors, q


WORK = Path(__file__).resolve().parent
CERT_DIR = WORK / "exception_syzygies"


def descriptor_digest(desc):
    payload = json.dumps(
        [
            desc.k,
            desc.retic_count,
            desc.edge_class_count,
            desc.outputs,
            desc.edge_signatures,
        ],
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def stripped_log_matrix(desc, support):
    p = 2 * desc.edge_class_count + desc.retic_count
    symbols = sp.symbols(f"x:{p}")
    rows = []
    output_indices = []
    for output_index, polynomial in enumerate(output_sparse_polynomials(desc)):
        entries = [
            {
                exponent: coefficient * exponent[column]
                for exponent, coefficient in polynomial.items()
                if exponent[column]
            }
            for column in support
        ]
        terms = [(exponent, coefficient) for entry in entries for exponent, coefficient in entry.items()]
        if not terms:
            continue
        minimum = [min(exponent[j] for exponent, _ in terms) for j in range(p)]
        coefficient_gcd = 0
        for _, coefficient in terms:
            coefficient_gcd = math.gcd(coefficient_gcd, abs(coefficient))
        row = []
        for entry in entries:
            expression = sp.S.Zero
            for exponent, coefficient in entry.items():
                monomial = sp.S.One
                for j in range(p):
                    power = exponent[j] - minimum[j]
                    if power:
                        monomial *= symbols[j] ** power
                expression += (coefficient // coefficient_gcd) * monomial
            row.append(expression)
        rows.append(row)
        output_indices.append(output_index)
    return symbols, sp.Matrix(rows), tuple(output_indices)


def expression_to_sparse(expression, symbols):
    polynomial = sp.Poly(expression, *symbols, domain=sp.ZZ)
    return {
        tuple(int(power) for power in exponent): int(coefficient)
        for exponent, coefficient in polynomial.terms()
        if coefficient
    }


def normalize_vector(vector):
    coefficient_gcd = 0
    for polynomial in vector:
        for coefficient in polynomial.values():
            coefficient_gcd = math.gcd(coefficient_gcd, abs(coefficient))
    if coefficient_gcd > 1:
        vector = [
            {exponent: coefficient // coefficient_gcd for exponent, coefficient in polynomial.items()}
            for polynomial in vector
        ]
    first = next(
        coefficient
        for polynomial in vector
        for _, coefficient in sorted(polynomial.items())
        if coefficient
    )
    if first < 0:
        vector = [
            {exponent: -coefficient for exponent, coefficient in polynomial.items()}
            for polynomial in vector
        ]
    return vector


def sparse_multiply(left, right):
    answer = defaultdict(int)
    for a, ca in left.items():
        for b, cb in right.items():
            answer[tuple(x + y for x, y in zip(a, b))] += ca * cb
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def verify_log_syzygy(desc, support, vector):
    for output_index, polynomial in enumerate(output_sparse_polynomials(desc)):
        residual = defaultdict(int)
        for column, multiplier in zip(support, vector):
            derivative = {
                exponent: coefficient * exponent[column]
                for exponent, coefficient in polynomial.items()
                if exponent[column]
            }
            for exponent, coefficient in sparse_multiply(derivative, multiplier).items():
                residual[exponent] += coefficient
        residual = {exponent: coefficient for exponent, coefficient in residual.items() if coefficient}
        if residual:
            raise AssertionError((output_index, len(residual), next(iter(residual.items()))))


def evaluate_sparse(polynomial, values):
    answer = sp.S.Zero
    for exponent, coefficient in polynomial.items():
        term = sp.Integer(coefficient)
        for value, power in zip(values, exponent):
            if power:
                term *= value ** power
        answer += term
    return answer


def generate_one(desc, support):
    symbols, matrix, output_indices = stripped_log_matrix(desc, support)
    # Select a square-rank 9-row seed deterministically at the exact interior
    # point.  Its cofactor/nullspace vector is then checked against every row
    # of the full symbolic matrix.  Selection is not an upper-bound claim: the
    # exact coefficientwise full-row replay below is the certificate.
    edge_pairs, lambdas = default_exact_point(desc)
    xs = tuple(value for pair in edge_pairs for value in pair)
    jacobian = descriptor_jacobian(desc, edge_pairs, lambdas)
    numeric_log = [
        [jacobian[output_index][column] * xs[column] for column in support]
        for output_index in output_indices
    ]
    target_rank = len(support) - 1
    numeric_rank, _, _ = exact_rank_pivots(numeric_log)
    if numeric_rank != target_rank:
        raise AssertionError((support, numeric_rank))
    # Low-complexity independent rows make the cofactor calculation orders of
    # magnitude smaller while leaving the subsequent full identity replay
    # unchanged.
    complexity_order = sorted(
        range(matrix.rows),
        key=lambda i: (
            sum(sp.count_ops(matrix[i, j]) for j in range(matrix.cols)),
            sum(bool(matrix[i, j]) for j in range(matrix.cols)),
            i,
        ),
    )
    chosen = []
    chosen_rank = 0
    for row_index in complexity_order:
        trial = chosen + [row_index]
        trial_rank, _, _ = exact_rank_pivots([numeric_log[i] for i in trial])
        if trial_rank > chosen_rank:
            chosen.append(row_index)
            chosen_rank = trial_rank
            if chosen_rank == target_rank:
                break
    if chosen_rank != target_rank:
        raise AssertionError((support, chosen_rank, target_rank))
    pivot_rows = tuple(chosen)
    seed = matrix[list(pivot_rows), :]
    started = time.monotonic()
    raw = DomainMatrix.from_Matrix(seed).nullspace()
    if raw.shape != (1, len(support)):
        raise AssertionError((support, matrix.shape, raw.shape))
    _, primitive = raw.primitive()
    row = primitive.to_Matrix().row(0)
    vector = normalize_vector([expression_to_sparse(expression, symbols) for expression in row])
    verify_log_syzygy(desc, support, vector)
    return (
        vector,
        time.monotonic() - started,
        matrix.shape,
        tuple(output_indices[i] for i in pivot_rows),
    )


def json_vector(vector):
    return [
        [
            {"exponents": list(exponent), "coefficient": coefficient}
            for exponent, coefficient in sorted(polynomial.items())
        ]
        for polynomial in vector
    ]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-support", type=int)
    parser.add_argument("--min-support", type=int, default=0)
    parser.add_argument("--orbit", type=int, action="append")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    CERT_DIR.mkdir(exist_ok=True)

    with (WORK / "exception_orbit_representatives.pkl").open("rb") as handle:
        representatives = pickle.load(handle)
    ledger = json.loads((WORK / "exception_orbits.json").read_text())
    selected_orbits = set(args.orbit) if args.orbit else None

    for desc, orbit in zip(representatives, ledger["orbits"]):
        orbit_index = orbit["orbit_index"]
        supports = [tuple(row) for row in orbit["selected_missing_edge_supports"]]
        if selected_orbits is not None and orbit_index not in selected_orbits:
            continue
        if args.max_support is not None and max(map(len, supports)) > args.max_support:
            continue
        if min(map(len, supports)) < args.min_support:
            continue
        path = CERT_DIR / f"orbit_{orbit_index:03d}.json"
        if path.exists() and not args.force:
            print(f"skip existing orbit {orbit_index}", flush=True)
            continue
        fields = []
        for support in supports:
            print(f"orbit {orbit_index} support={support}: start", flush=True)
            vector, elapsed, shape, seed_outputs = generate_one(desc, support)
            fields.append(
                {
                    "support": list(support),
                    "stripped_log_matrix_shape": list(shape),
                    "cofactor_seed_output_indices": list(seed_outputs),
                    "generation_seconds": elapsed,
                    "component_term_counts": [len(polynomial) for polynomial in vector],
                    "log_multipliers": json_vector(vector),
                }
            )
            print(
                f"orbit {orbit_index} support={support}: exact terms="
                f"{[len(polynomial) for polynomial in vector]} elapsed={elapsed:.2f}s",
                flush=True,
            )

        # Recheck that the exact polynomial fields, together with the base
        # ansatz, are independent at one exact interior point.
        edge_pairs, lambdas = default_exact_point(desc)
        values = tuple(q(value) for pair in edge_pairs for value in pair) + tuple(q(x) for x in lambdas)
        evars = 2 * desc.edge_class_count
        added = []
        for field in fields:
            vector = []
            for component_terms in field["log_multipliers"]:
                polynomial = {
                    tuple(term["exponents"]): term["coefficient"] for term in component_terms
                }
                vector.append(polynomial)
            column = sp.zeros(evars + desc.retic_count, 1)
            for parameter, polynomial in zip(field["support"], vector):
                column[parameter] = values[parameter] * evaluate_sparse(polynomial, values)
            added.append(column)
        combined = base_evaluated_vectors(desc)
        if added:
            combined = sp.Matrix.hstack(combined, *added)
        combined_rank = combined.rank()
        required = (evars + desc.retic_count) - orbit["lower_rank"]
        if combined_rank != required:
            raise AssertionError((orbit_index, combined_rank, required))

        certificate = {
            "schema": "k2p-primitive-polynomial-log-syzygy-v1",
            "orbit_index": orbit_index,
            "representative_descriptor_sha256": descriptor_digest(desc),
            "parameter_count": evars + desc.retic_count,
            "lower_rank": orbit["lower_rank"],
            "base_evaluated_field_rank": orbit["base_evaluated_field_rank"],
            "combined_evaluated_field_rank": combined_rank,
            "certified_rank_upper": (evars + desc.retic_count) - combined_rank,
            "fields": fields,
            "coefficientwise_residual": "zero for every field and all 36 outputs",
        }
        path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
