#!/usr/bin/env python3
"""Low-memory modular probe for theta0 repair-1 relabeling invariants."""

from __future__ import annotations

import random
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "package/referee/k2p_offline_sweep_portable/atlas"))

from k2p_atlas_core import (  # noqa: E402
    homogeneous_blocks,
    model_descriptor_fast2,
    relabel_record,
    source_supports,
    target_completions,
)


PRIME = 1_000_003


def evaluate(descriptor, edge_pairs, lambdas):
    values = []
    for expression in descriptor.outputs:
        total = 0
        for monomial, lambda_polynomial in expression:
            monomial_value = 1
            for edge_class, sector, exponent in monomial:
                monomial_value *= pow(edge_pairs[edge_class][sector - 1], exponent, PRIME)
                monomial_value %= PRIME
            lambda_value = 0
            for mask, coefficient in lambda_polynomial:
                term = coefficient % PRIME
                for index, value in enumerate(lambdas):
                    if mask >> index & 1:
                        term = term * value % PRIME
                lambda_value = (lambda_value + term) % PRIME
            total = (total + monomial_value * lambda_value) % PRIME
        values.append(total)
    return values


def sample_output(descriptor, rng):
    edges = [
        (rng.randrange(1, PRIME), rng.randrange(1, PRIME))
        for _ in range(descriptor.edge_class_count)
    ]
    lambdas = [rng.randrange(1, PRIME) for _ in range(descriptor.retic_count)]
    return evaluate(descriptor, edges, lambdas)


def monomial_row(output, block):
    row = []
    for indices in block:
        value = 1
        for index in indices:
            value = value * output[index] % PRIME
        row.append(value)
    return row


class RowBasis:
    def __init__(self, width):
        self.width = width
        self.rows = {}

    def reduce(self, row):
        row = list(row)
        for pivot in sorted(self.rows):
            coefficient = row[pivot]
            if not coefficient:
                continue
            basis_row = self.rows[pivot]
            for column in range(pivot, self.width):
                row[column] = (row[column] - coefficient * basis_row[column]) % PRIME
        return row

    def add(self, row):
        row = self.reduce(row)
        pivot = next((index for index, value in enumerate(row) if value), None)
        if pivot is None:
            return False
        inverse = pow(row[pivot], PRIME - 2, PRIME)
        for column in range(pivot, self.width):
            row[column] = row[column] * inverse % PRIME
        self.rows[pivot] = row
        return True


def main():
    permutation = (0, 1, 3, 2)  # source-1 class 25
    source_record = source_supports()[1]
    target_record = relabel_record(target_completions(4, True)[80], permutation)
    source = model_descriptor_fast2(source_record.graph)
    target = model_descriptor_fast2(target_record.graph)

    blocks = homogeneous_blocks(4, 5)
    weight, block = max(blocks, key=lambda row: len(row[1]))
    print({"weight": weight, "block_size": len(block)}, flush=True)

    rng = random.Random(20260821)
    basis = RowBasis(len(block))
    last_growth = 0
    for sample_index in range(1, 801):
        output = sample_output(target, rng)
        if basis.add(monomial_row(output, block)):
            last_growth = sample_index
        if sample_index % 25 == 0:
            print(
                {
                    "target_samples": sample_index,
                    "rank": len(basis.rows),
                    "last_growth": last_growth,
                },
                flush=True,
            )
        if len(basis.rows) == len(block):
            break
        if sample_index - last_growth >= 80:
            break

    for index in range(10):
        output = sample_output(source, rng)
        residue = basis.reduce(monomial_row(output, block))
        print(
            {
                "source_sample": index,
                "residue_nonzero": any(residue),
                "residue_terms": sum(bool(value) for value in residue),
            },
            flush=True,
        )


def scan_small_blocks(cap=10, permutation=(0, 1, 3, 2)):
    source_record = source_supports()[1]
    target_record = relabel_record(target_completions(4, True)[80], permutation)
    source = model_descriptor_fast2(source_record.graph)
    target = model_descriptor_fast2(target_record.graph)
    blocks = [row for row in homogeneous_blocks(4, 5) if 2 <= len(row[1]) <= cap]
    rng = random.Random(2026082101)
    target_outputs = [sample_output(target, rng) for _ in range(cap + 20)]
    source_outputs = [sample_output(source, rng) for _ in range(5)]
    deficient = 0
    for block_index, (weight, block) in enumerate(blocks, 1):
        basis = RowBasis(len(block))
        for output in target_outputs:
            basis.add(monomial_row(output, block))
            if len(basis.rows) == len(block):
                break
        if len(basis.rows) == len(block):
            continue
        deficient += 1
        residues = [basis.reduce(monomial_row(output, block)) for output in source_outputs]
        if any(any(row) for row in residues):
            print(
                {
                    "event": "candidate",
                    "block_index": block_index,
                    "weight": weight,
                    "block_size": len(block),
                    "target_rank": len(basis.rows),
                    "source_residue_terms": [sum(bool(x) for x in row) for row in residues],
                    "block": block,
                },
                flush=True,
            )
            return
        if block_index % 5000 == 0:
            print(
                {"scanned": block_index, "deficient": deficient},
                flush=True,
            )
    print({"event": "none", "scanned": len(blocks), "deficient": deficient}, flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "scan-small":
        chosen = (
            tuple(int(value) for value in sys.argv[3].split(","))
            if len(sys.argv) > 3
            else (0, 1, 3, 2)
        )
        scan_small_blocks(int(sys.argv[2]) if len(sys.argv) > 2 else 10, chosen)
    else:
        main()
