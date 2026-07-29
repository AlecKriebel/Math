#!/usr/bin/env python3
"""Exact low-strand arithmetic for the (3,6) Jones--Wenzl quotient.

The simple H_n(3,6)-modules are indexed by partitions lambda of n with
at most three rows and lambda_1-lambda_3 <= 3.  Their dimensions are the
numbers of paths to lambda in the corresponding admissible Young lattice.

For the eta=1/2 Markov trace, a minimal projection in the lambda block has
trace D(lambda)/2**n, where D(lambda) is the SU(3)_3 quantum dimension.
Consequently, in a d-dimensional ordinary tensor-space representation, the
multiplicity of that simple block must be

    multiplicity(lambda, n, d) = D(lambda) * (d/2)**n.

All computations below use Python integers and fractions only.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from typing import Dict, Iterable, Tuple

Partition = Tuple[int, int, int]


QUANTUM_DIMENSIONS = {
    (0, 0): 1,
    (1, 0): 2,
    (0, 1): 2,
    (2, 0): 2,
    (0, 2): 2,
    (1, 1): 3,
    (3, 0): 1,
    (0, 3): 1,
    (2, 1): 2,
    (1, 2): 2,
}


def admissible(partition: Partition) -> bool:
    """Return whether a three-row partition is (3,6)-admissible."""

    first, second, third = partition
    return (
        first >= second >= third >= 0
        and first - third <= 3
    )


def successors(partition: Partition) -> Iterable[Partition]:
    """Admissible diagrams obtained by adding one box."""

    for row in range(3):
        candidate = list(partition)
        candidate[row] += 1
        result = tuple(candidate)
        if admissible(result):
            yield result


def dynkin_label(partition: Partition) -> Tuple[int, int]:
    """The SU(3)_3 alcove label attached to a three-row diagram."""

    first, second, third = partition
    return first - second, second - third


def quantum_dimension(partition: Partition) -> int:
    return QUANTUM_DIMENSIONS[dynkin_label(partition)]


def path_tables(max_strand: int) -> Dict[int, Dict[Partition, int]]:
    """Admissible path counts, hence simple-module dimensions."""

    tables: Dict[int, Dict[Partition, int]] = {
        0: {(0, 0, 0): 1}
    }
    for strand in range(max_strand):
        following: Dict[Partition, int] = defaultdict(int)
        for partition, count in tables[strand].items():
            for candidate in successors(partition):
                following[candidate] += count
        tables[strand + 1] = dict(following)
    return tables


def check_quantum_dimension_recursion(
    tables: Dict[int, Dict[Partition, int]]
) -> None:
    """Check 2 D(lambda) = sum D(mu) over admissible successors."""

    for strand in range(max(tables)):
        for partition in tables[strand]:
            left = 2 * quantum_dimension(partition)
            right = sum(
                quantum_dimension(candidate)
                for candidate in successors(partition)
            )
            assert left == right, (partition, left, right)


def markov_minimal_weight(partition: Partition, strand: int) -> Fraction:
    """Trace of a minimal projection in the corresponding simple block."""

    return Fraction(quantum_dimension(partition), 2**strand)


def markov_central_weight(
    partition: Partition, path_count: int, strand: int
) -> Fraction:
    """Trace of the block's central identity."""

    return path_count * markov_minimal_weight(partition, strand)


def required_multiplicity(
    partition: Partition, strand: int, local_dimension: int
) -> Fraction:
    """Multiplicity of the simple module in (C^d)^{tensor strand}."""

    return Fraction(
        quantum_dimension(partition) * local_dimension**strand,
        2**strand,
    )


def check_level(
    partitions: Dict[Partition, int], strand: int, local_dimension: int
) -> None:
    """Verify all trace, dimension, and integrality identities at one level."""

    central_weight_sum = sum(
        (
            markov_central_weight(partition, path_count, strand)
            for partition, path_count in partitions.items()
        ),
        Fraction(0),
    )
    assert central_weight_sum == 1

    represented_dimension = sum(
        (
            path_count
            * required_multiplicity(partition, strand, local_dimension)
            for partition, path_count in partitions.items()
        ),
        Fraction(0),
    )
    assert represented_dimension == local_dimension**strand


def divisibility_survivors(
    tables: Dict[int, Dict[Partition, int]], maximum_d: int
) -> list[int]:
    """Dimensions passing every exact multiplicity test in the tables."""

    survivors = []
    for local_dimension in range(1, maximum_d + 1):
        passed = True
        for strand, partitions in tables.items():
            for partition in partitions:
                if required_multiplicity(
                    partition, strand, local_dimension
                ).denominator != 1:
                    passed = False
                    break
            if not passed:
                break
        if passed:
            survivors.append(local_dimension)
    return survivors


def format_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-strand", type=int, default=12)
    parser.add_argument("--test-d-through", type=int, default=24)
    args = parser.parse_args()

    tables = path_tables(args.max_strand)
    check_quantum_dimension_recursion(tables)

    print("Exact H_n(3,6) low-strand arithmetic")
    print(f"levels: 0..{args.max_strand}")
    print("[ok] admissible quantum-dimension recursion")
    print()
    print(
        "n | lambda | simple_dim | qdim | "
        "minimal_trace | central_trace | required_multiplicity"
    )
    print(
        "--|--------|------------|------|"
        "---------------|---------------|----------------------"
    )
    for strand, partitions in tables.items():
        for partition, path_count in sorted(partitions.items()):
            qdim = quantum_dimension(partition)
            minimal = markov_minimal_weight(partition, strand)
            central = markov_central_weight(
                partition, path_count, strand
            )
            print(
                f"{strand} | {partition} | {path_count} | {qdim} | "
                f"{format_fraction(minimal)} | "
                f"{format_fraction(central)} | "
                f"{qdim}*(d/2)^{strand}"
            )
        check_level(partitions, strand, 2)
        check_level(partitions, strand, 4)
        check_level(partitions, strand, 6)

    survivors = divisibility_survivors(tables, args.test_d_through)
    expected = list(range(2, args.test_d_through + 1, 2))
    assert survivors == expected
    print()
    print("[ok] central Markov weights sum to 1 at every level")
    print("[ok] block dimensions sum to d^n for d = 2, 4, 6")
    print(
        "[ok] exact block multiplicities through d = "
        f"{args.test_d_through} are integral exactly for even d"
    )
    print(
        "Conclusion: the full multiplicity formula imposes only 2 | d; "
        "it cannot force 4 | d at any strand."
    )


if __name__ == "__main__":
    main()
