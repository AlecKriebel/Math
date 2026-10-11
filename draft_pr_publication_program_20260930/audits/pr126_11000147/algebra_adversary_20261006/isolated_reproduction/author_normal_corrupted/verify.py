#!/usr/bin/env python3
"""Exact finite diagnostics for the torus braid triple; standard library only."""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
counts = {}


def check(condition, group):
    if not condition:
        raise AssertionError(group)
    counts[group] = counts.get(group, 0) + 1


def mul(x, y):
    return tuple(tuple(sum(x[i][k] * y[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def det(x):
    return x[0][0] * x[1][1] - x[0][1] * x[1][0]


def inv(x):
    assert det(x) == 1
    return ((x[1][1], -x[0][1]), (-x[1][0], x[0][0]))


def scale(c, x):
    return tuple(tuple(c * z for z in row) for row in x)


def add(x, y):
    return tuple(tuple(x[i][j] + y[i][j] for j in range(2)) for i in range(2))


def act(x, v, modulus):
    return tuple(sum(x[i][j] * v[j] for j in range(2)) % modulus
                 for i in range(2))


def qadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


def qmul(x, y):
    # Coordinates in Q[sqrt(3)].
    return (x[0] * y[0] + 3 * x[1] * y[1],
            x[0] * y[1] + x[1] * y[0])


A = ((3, 1), (2, 1))
B = ((1, -2), (-1, 3))
C = ((8, -11), (4, -4))
I = ((1, 0), (0, 1))
ZERO = ((0, 0), (0, 0))
matrices = (A, B, C)
products = (((0, -1), (1, 0)), ((7, -10), (5, -7)),
            ((5, -13), (2, -5)))

for M in matrices:
    check(det(M) == 1, "matrix_and_dynamics")
    check(M[0][0] + M[1][1] == 4, "matrix_and_dynamics")
    check(mul(M, inv(M)) == I == mul(inv(M), M), "matrix_and_dynamics")
    check(add(add(mul(M, M), scale(-4, M)), I) == ZERO,
          "matrix_and_dynamics")
    for lam in ((2, 1), (2, -1)):
        v = ((M[0][1], 0), qadd(lam, (-M[0][0], 0)))
        mv = tuple(qadd(qmul((M[i][0], 0), v[0]),
                        qmul((M[i][1], 0), v[1])) for i in range(2))
        check(mv == tuple(qmul(lam, z) for z in v), "exact_eigenvectors")
        check(v[0] != (0, 0), "exact_eigenvectors")
check(qmul((2, 1), (2, -1)) == (1, 0), "exact_eigenvectors")
# The rational inequalities 1 < sqrt(3) < 2 imply 0 < 2-sqrt(3) < 1.
check(1**2 < 3 < 2**2, "exact_eigenvectors")
check(C == mul(mul(A, B), inv(A)), "braid_relations")
check(C == mul(mul(inv(B), A), B), "braid_relations")
for (M, N), common in zip(combinations(matrices, 2), products):
    check(M != N, "braid_relations")
    check(mul(M, N) != mul(N, M), "braid_relations")
    check(mul(mul(M, N), M) == common, "braid_relations")
    check(mul(mul(N, M), N) == common, "braid_relations")

# An explicit instance of the referee's x^2=-I, y^3=I pair mechanism.
X = ((0, 1), (-1, 0))
Y = ((-2, -1), (3, 1))
check(mul(X, X) == scale(-1, I), "source_pair_mechanism")
check(mul(mul(Y, Y), Y) == I, "source_pair_mechanism")
check(mul(X, Y) == A and mul(Y, X) == B, "source_pair_mechanism")

# Finite-coordinate controls, not substitutes for identities on the full torus.
for modulus in (2, 3, 5):
    points = list(product(range(modulus), repeat=2))
    for M in matrices:
        check(len({act(M, v, modulus) for v in points}) == len(points),
              "finite_torus_controls")
        for v in points:
            check(act(inv(M), act(M, v, modulus), modulus) == v,
                  "finite_torus_controls")
    for M, N in combinations(matrices, 2):
        for v in points:
            left = act(M, act(N, act(M, v, modulus), modulus), modulus)
            right = act(N, act(M, act(N, v, modulus), modulus), modulus)
            check(left == right, "finite_torus_controls")

# A separate small finite-group diagnostic of the abstract lemma.
def pmul(p, q):
    return tuple(p[q[i]] for i in range(3))


def pinv(p):
    return tuple(p.index(i) for i in range(3))


def braid(p, q):
    return pmul(pmul(p, q), p) == pmul(pmul(q, p), q)


nontrivial_pairs = 0
for p, q in product(list(permutations(range(3))), repeat=2):
    if p != q and braid(p, q):
        nontrivial_pairs += 1
        r = pmul(pmul(p, q), pinv(p))
        check(r == pmul(pmul(pinv(q), p), q), "group_lemma_controls")
        check(len({p, q, r}) == 3, "group_lemma_controls")
        for u, v in combinations((p, q, r), 2):
            check(braid(u, v) and pmul(u, v) != pmul(v, u),
                  "group_lemma_controls")
check(nontrivial_pairs == 6, "group_lemma_controls")

receipt = {
    "status": "PASS",
    "artifact_sha256": sha256((ROOT / "CANDIDATE.md").read_bytes()).hexdigest(),
    "verifier_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    "counts": counts,
    "total_assertions": sum(counts.values()),
    "limitations": "Finite controls supplement the written universal group proof and invariant-foliation argument; they do not establish historical priority.",
}
(ROOT / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
