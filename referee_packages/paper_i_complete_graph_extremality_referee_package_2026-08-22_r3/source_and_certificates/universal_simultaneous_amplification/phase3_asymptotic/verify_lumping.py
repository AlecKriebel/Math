#!/usr/bin/env python3
"""Exact Fraction-based strong-lumpability checks for phase-3 families."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from typing import Callable, Dict, Hashable, List, Sequence, Tuple


class CertificateFailure(RuntimeError):
    """Raised when an explicit certificate check fails."""


def require(condition, detail="certificate check failed"):
    """Raise a failure that remains active under optimized Python."""
    if not condition:
        raise CertificateFailure(str(detail))


F = Fraction
Signature = Hashable


def transition_row(
    weights: Sequence[Sequence[F]], mask: int, r: F, rule: str
) -> Dict[int, F]:
    n = len(weights)
    degrees = [sum(row, F(0)) for row in weights]
    row: Dict[int, F] = defaultdict(F)
    mutant = lambda vertex: bool(mask & (1 << vertex))
    if rule == "Bd":
        fitness = [r if mutant(i) else F(1) for i in range(n)]
        total = sum(fitness, F(0))
        for parent in range(n):
            for target in range(n):
                if not weights[parent][target]:
                    continue
                probability = (
                    fitness[parent]
                    * weights[parent][target]
                    / (total * degrees[parent])
                )
                if mutant(parent):
                    new_mask = mask | (1 << target)
                else:
                    new_mask = mask & ~(1 << target)
                row[new_mask] += probability
    elif rule == "dB":
        for dead in range(n):
            mass = sum(
                (r if mutant(parent) else 1) * weights[parent][dead]
                for parent in range(n)
            )
            for parent in range(n):
                if not weights[parent][dead]:
                    continue
                probability = (
                    (r if mutant(parent) else 1)
                    * weights[parent][dead]
                    / (n * mass)
                )
                if mutant(parent):
                    new_mask = mask | (1 << dead)
                else:
                    new_mask = mask & ~(1 << dead)
                row[new_mask] += probability
    else:
        raise ValueError(rule)
    require(sum(row.values(), F(0)) == 1)
    return dict(row)


def verify_partition(
    weights: Sequence[Sequence[F]],
    signature: Callable[[int], Signature],
    r: F,
    rule: str,
) -> int:
    n = len(weights)
    references: Dict[Signature, Dict[Signature, F]] = {}
    for mask in range(1 << n):
        aggregate: Dict[Signature, F] = defaultdict(F)
        for target, probability in transition_row(weights, mask, r, rule).items():
            aggregate[signature(target)] += probability
        source_signature = signature(mask)
        if source_signature in references:
            require(references[source_signature] == dict(aggregate), (
                source_signature,
                references[source_signature],
                dict(aggregate),
            ))
        else:
            references[source_signature] = dict(aggregate)
    return len(references)


def two_class_weights(
    size_a: int, size_b: int, within_a: F, within_b: F, cross: F
) -> Tuple[List[List[F]], Callable[[int], Tuple[int, int]]]:
    n = size_a + size_b
    weights = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if i < size_a and j < size_a:
                weight = within_a
            elif i >= size_a and j >= size_a:
                weight = within_b
            else:
                weight = cross
            weights[i][j] = weights[j][i] = weight

    def signature(mask: int) -> Tuple[int, int]:
        return (
            sum(bool(mask & (1 << i)) for i in range(size_a)),
            sum(bool(mask & (1 << i)) for i in range(size_a, n)),
        )

    return weights, signature


def windmill_weights(
    modules: int, pair_weight: F
) -> Tuple[List[List[F]], Callable[[int], Tuple[int, int, int]]]:
    n = 2 * modules + 1
    weights = [[F(0) for _ in range(n)] for _ in range(n)]
    for module in range(modules):
        left, right = 1 + 2 * module, 2 + 2 * module
        weights[0][left] = weights[left][0] = F(1)
        weights[0][right] = weights[right][0] = F(1)
        weights[left][right] = weights[right][left] = pair_weight

    def signature(mask: int) -> Tuple[int, int, int]:
        hub = int(bool(mask & 1))
        mixed = 0
        mutant_pairs = 0
        for module in range(modules):
            left, right = 1 + 2 * module, 2 + 2 * module
            count = int(bool(mask & (1 << left))) + int(
                bool(mask & (1 << right))
            )
            mixed += count == 1
            mutant_pairs += count == 2
        return hub, mixed, mutant_pairs

    return weights, signature


def main() -> None:
    examples = [
        ("two_class",) + two_class_weights(3, 4, F(1, 3), F(5, 2), F(7, 4)),
        ("windmill",) + windmill_weights(3, F(11, 3)),
    ]
    for name, weights, signature in examples:
        for rule in ("Bd", "dB"):
            cells = verify_partition(weights, signature, F(7, 3), rule)
            print(f"PASS family={name} rule={rule} cells={cells}")


if __name__ == "__main__":
    main()
