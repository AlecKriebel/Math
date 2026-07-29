#!/usr/bin/env python3
"""Exact checks for the abstract two-projection normal form.

This script is only a verifier for the finite block calculations in
notes/track_structural_projection.md.  It is not used as evidence for tensor
locality or for the automatic-partial-trace theorem.
"""

from __future__ import annotations

import sympy as sp


C = sp.Rational(1, 3)
S = sp.sqrt(2) / 3


def direct_sum(blocks: list[sp.Matrix]) -> sp.Matrix:
    return sp.diag(*blocks)


def abstract_pair(a: int, r: int) -> tuple[sp.Matrix, sp.Matrix]:
    """Return the half-rank model with a common-1, a common-0, and r generic blocks."""

    p_blocks: list[sp.Matrix] = []
    q_blocks: list[sp.Matrix] = []

    for _ in range(a):
        p_blocks.append(sp.Matrix([[1]]))
        q_blocks.append(sp.Matrix([[1]]))
    for _ in range(a):
        p_blocks.append(sp.Matrix([[0]]))
        q_blocks.append(sp.Matrix([[0]]))
    for _ in range(r):
        p_blocks.append(sp.Matrix([[1, 0], [0, 0]]))
        q_blocks.append(sp.Matrix([[C, S], [S, 1 - C]]))

    return direct_sum(p_blocks), direct_sum(q_blocks)


def is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def verify_pair(a: int, r: int) -> dict[str, object]:
    p, q = abstract_pair(a, r)
    relation = p * q * p - q * p * q - C * (p - q)
    assert is_zero(p * p - p)
    assert is_zero(q * q - q)
    assert is_zero(p.T - p)
    assert is_zero(q.T - q)
    assert is_zero(relation)
    assert p.rank() == q.rank()

    return {
        "dimension": p.rows,
        "rank_p": p.rank(),
        "rank_q": q.rank(),
        "intersection_dimension": a,
        "generic_block_count": r,
        "trace_pq": sp.simplify(sp.trace(p * q)),
    }


def verify_clifford_block() -> None:
    p = sp.Matrix([[1, 0], [0, 0]])
    q = sp.Matrix([[C, S], [S, 1 - C]])
    u = sp.sqrt(sp.Rational(3, 2)) * (p - q)
    v = sp.sqrt(3) * (p + q - sp.eye(2))
    assert is_zero(u * u - sp.eye(2))
    assert is_zero(v * v - sp.eye(2))
    assert is_zero(u * v + v * u)


def main() -> None:
    verify_clifford_block()

    # All three examples have dimension 8 and both projections have rank 4.
    # Only a=1 has the Markov value Tr(pq)=8/4=2.
    rows = [verify_pair(a=a, r=4 - a) for a in (0, 1, 2)]
    for row in rows:
        print(
            "D={dimension} rank={rank_p} intersection={intersection_dimension} "
            "generic_blocks={generic_block_count} Tr(pq)={trace_pq}".format(**row)
        )
    print("exact block and Clifford checks: PASS")


if __name__ == "__main__":
    main()
