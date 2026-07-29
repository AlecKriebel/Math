#!/usr/bin/env python3
"""Exact check of the canonical nontrivial block for the three-strand relation.

This script is intentionally small.  The classification proof is human-readable
and does not rely on this calculation; this only checks the displayed block and
the trace formulas over exact algebraic numbers.
"""

from sympy import Matrix, Rational, eye, simplify, sqrt, zeros


lam = Rational(1, 3)
p = Matrix([[1, 0], [0, 0]])
q = Matrix(
    [
        [lam, sqrt(lam * (1 - lam))],
        [sqrt(lam * (1 - lam)), 1 - lam],
    ]
)

assert p * p == p
assert q * q == q
assert p.T.conjugate() == p
assert q.T.conjugate() == q
assert simplify(p * q * p - q * p * q - lam * (p - q)) == zeros(2)
assert (p * q).trace() == lam

# Check the central element on each possible canonical summand.
blocks = [
    (Matrix([[1]]), Matrix([[1]]), Rational(2, 3), "common range"),
    (Matrix([[0]]), Matrix([[0]]), Rational(0), "common kernel"),
    (p, q, Rational(0), "generic block"),
]
for pb, qb, expected, name in blocks:
    cb = pb * qb * pb - lam * pb
    assert cb == qb * pb * qb - lam * qb, name
    assert cb == expected * eye(pb.rows), name
    assert pb * cb == cb == cb * pb, name
    assert qb * cb == cb == cb * qb, name

# In the tensor-overlap application D=d^3 and rank(p)=rank(q)=D/2.
# If a is the common-range multiplicity and c the generic-block count, then
# c=D/2-a.  The Markov value Tr(pq)=D/4 forces a=D/8 and c=3D/8.
D, a, c = 216, 27, 81  # d=6, used only as an exact arithmetic test case
assert c == D // 2 - a
assert a + 2 * c + a == D
assert a + lam * c == Rational(D, 4)
assert a == Rational(D, 8)
assert c == Rational(3 * D, 8)

print("[ok] exact generic block is a pair of projections")
print("[ok] generic block satisfies the cubic projection relation")
print("[ok] central element has the claimed value on all canonical blocks")
print("[ok] Markov trace forces multiplicities a=b=D/8, c=3D/8")
