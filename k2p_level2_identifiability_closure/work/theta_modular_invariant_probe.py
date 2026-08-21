#!/usr/bin/env python3
"""Low-memory modular search for an exact theta target invariant.

The modular stage is only a candidate generator.  A candidate is promoted only
after characteristic-zero sparse expansion proves that it vanishes identically
on the target and pulls back nontrivially to the source.
"""

from __future__ import annotations

import argparse
import importlib.util
import math
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
SPEC = importlib.util.spec_from_file_location("k2p_theta_modular_core", CORE)
assert SPEC is not None and SPEC.loader is not None
atlas = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = atlas
SPEC.loader.exec_module(atlas)


def evaluate_sparse_mod(polynomials, points, prime):
    values = np.empty((len(points), len(polynomials)), dtype=np.int64)
    for row, point in enumerate(points):
        for column, polynomial in enumerate(polynomials):
            value = 0
            for exponent, coefficient in polynomial.items():
                term = coefficient % prime
                for parameter, power in zip(point, exponent):
                    if power:
                        term = (term * pow(int(parameter), int(power), prime)) % prime
                value = (value + term) % prime
            values[row, column] = value
    return values


def block_evaluations(coordinates, block, prime):
    result = np.ones((coordinates.shape[0], len(block)), dtype=np.int64)
    for column, indices in enumerate(block):
        for index in indices:
            result[:, column] = (result[:, column] * coordinates[:, index]) % prime
    return result


def modular_nullspace(matrix, prime):
    work = np.asarray(matrix, dtype=np.int64).copy() % prime
    rows, columns = work.shape
    pivots = []
    pivot_row = 0
    for column in range(columns):
        candidates = np.flatnonzero(work[pivot_row:, column])
        if not len(candidates):
            continue
        chosen = pivot_row + int(candidates[0])
        if chosen != pivot_row:
            work[[pivot_row, chosen]] = work[[chosen, pivot_row]]
        inverse = pow(int(work[pivot_row, column]), prime - 2, prime)
        work[pivot_row] = (work[pivot_row] * inverse) % prime
        factors = work[:, column].copy()
        factors[pivot_row] = 0
        work = (work - factors[:, None] * work[pivot_row][None, :]) % prime
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    free = [column for column in range(columns) if column not in pivots]
    basis = []
    for free_column in free:
        vector = np.zeros(columns, dtype=np.int64)
        vector[free_column] = 1
        for row, pivot in reversed(list(enumerate(pivots))):
            vector[pivot] = -sum(
                int(work[row, column]) * int(vector[column]) for column in free
            ) % prime
        basis.append(vector)
    return basis


def centered_primitive(vector, prime):
    values = [int(value) if int(value) <= prime // 2 else int(value) - prime for value in vector]
    divisor = 0
    for value in values:
        divisor = math.gcd(divisor, abs(value))
    if divisor:
        values = [value // divisor for value in values]
    first = next((value for value in values if value), 1)
    if first < 0:
        values = [-value for value in values]
    return tuple(values)


def exact_certificate(source, target, block, coefficients):
    source_outputs = atlas.output_sparse_polynomials(source)
    target_outputs = atlas.output_sparse_polynomials(target)
    source_columns = [atlas.sparse_mul_many([source_outputs[i] for i in indices]) for indices in block]
    target_columns = [atlas.sparse_mul_many([target_outputs[i] for i in indices]) for indices in block]
    target_pullback = atlas.sparse_lincomb(target_columns, coefficients)
    source_pullback = atlas.sparse_lincomb(source_columns, coefficients)
    return target_pullback, source_pullback


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("s2-id", "s2-swap", "s4-id"), required=True)
    parser.add_argument("--degree", type=int, default=4)
    parser.add_argument("--min-block", type=int, default=2)
    parser.add_argument("--max-block", type=int, default=196)
    parser.add_argument("--prime", type=int, default=1_000_003)
    parser.add_argument("--samples", type=int, default=210)
    parser.add_argument("--seed", type=int, default=20260820)
    args = parser.parse_args()

    sources = atlas.source_supports()
    target_record = atlas.target_completions(4, True)[822]
    if args.case == "s2-id":
        source_graph, target_graph = sources[2].graph, target_record.graph
    elif args.case == "s2-swap":
        source_graph = sources[2].graph
        target_graph = atlas.relabel_record(target_record, (0, 1, 3, 2)).graph
    else:
        source_graph, target_graph = sources[4].graph, target_record.graph
    source = atlas.model_descriptor_fast2(source_graph)
    target = atlas.model_descriptor_fast2(target_graph)
    source_polynomials = atlas.output_sparse_polynomials(source)
    target_polynomials = atlas.output_sparse_polynomials(target)

    rng = np.random.default_rng(args.seed)
    target_points = rng.integers(1, args.prime, size=(args.samples, 18), dtype=np.int64)
    source_points = rng.integers(1, args.prime, size=(24, 18), dtype=np.int64)
    target_values = evaluate_sparse_mod(target_polynomials, target_points, args.prime)
    source_values = evaluate_sparse_mod(source_polynomials, source_points, args.prime)
    blocks = sorted(atlas.homogeneous_blocks(4, args.degree), key=lambda row: (-len(row[1]), row[0]))
    tested = 0
    for weight, block in blocks:
        if not args.min_block <= len(block) <= args.max_block:
            continue
        tested += 1
        target_matrix = block_evaluations(target_values, block, args.prime)
        basis = modular_nullspace(target_matrix, args.prime)
        if not basis:
            continue
        source_matrix = block_evaluations(source_values, block, args.prime)
        for modular_vector in basis:
            if not np.any(source_matrix @ modular_vector % args.prime):
                continue
            coefficients = centered_primitive(modular_vector, args.prime)
            # A one-prime centered lift is useful only when coefficients are
            # genuinely small.  Otherwise another-prime reconstruction is needed.
            if max(map(abs, coefficients), default=0) > 10_000:
                print("modular candidate needs reconstruction", weight, len(block), flush=True)
                continue
            print("candidate", weight, len(block), coefficients, flush=True)
            target_pullback, source_pullback = exact_certificate(source, target, block, coefficients)
            if not target_pullback and source_pullback:
                print({
                    "case": args.case,
                    "degree": args.degree,
                    "weight": weight,
                    "block": block,
                    "coefficients": coefficients,
                    "source_nonzero_terms": len(source_pullback),
                    "source_witness": next(iter(source_pullback.items())),
                    "tested_blocks": tested,
                })
                return 0
            print("centered lift was not an exact characteristic-zero certificate", flush=True)
        if tested % 100 == 0:
            print("tested", tested, "last_block", len(block), flush=True)
    print("no exact certificate", {"tested_blocks": tested})
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
