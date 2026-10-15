#!/usr/bin/env python3
"""Small exact algebraic controls; no geometric realization is asserted."""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
checks = 0


def check(statement):
    global checks
    assert statement
    checks += 1


def apply(a, w):
    return tuple(sum(Q(x) * y for x, y in zip(row, w)) for row in a)


def normalize(w):
    mass = sum(w)
    assert mass > 0
    return tuple(x / mass for x in w)


def characteristic2(a):
    return (1, -a[0][0] - a[1][1],
            a[0][0] * a[1][1] - a[0][1] * a[1][0])


a = ((2, 1), (0, 1))
u = ((1, 1), (0, 1))
e1 = (Q(1), Q(0))
check(apply(a, e1) == (2, 0))
check(characteristic2(a) == (1, -3, 2))
check(apply(u, e1) == e1)
check(characteristic2(u) == (1, -2, 1))
check(u != ((1, 0), (0, 1)))

# At positive y, eigenvalue 1 is forced by the second coordinate.
# The displayed difference in the first coordinate cannot then vanish.
positive_controls = 0
for x in range(1, 5):
    for y in range(1, 5):
        w = (Q(x), Q(y))
        aw = apply(a, w)
        check(aw[1] == w[1])
        check(aw[0] - w[0] == x + y > 0)
        positive_controls += 1

# An independent branch-equation example: C={(x,y,z)>=0: x+y=z}.
# This is an algebraic cone, not a claimed embedded carrier.
branch_map = ((1, 1, 0), (1, 0, 0), (2, 1, 0))
identity3 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
cone_controls = 0
for x in range(5):
    for y in range(5):
        if x == y == 0:
            continue
        w = normalize((Q(x), Q(y), Q(x + y)))
        aw = apply(branch_map, w)
        f = normalize(aw)
        check(all(t >= 0 for t in aw))
        check(aw[0] + aw[1] == aw[2])
        check(sum(aw) > 0)
        check(sum(f) == 1 and f[0] + f[1] == f[2])
        check(normalize(apply(branch_map, tuple(7 * t for t in w))) == f)
        check(normalize(apply(identity3, w)) == w)
        cone_controls += 1

# Nonidentity alone gives no exponential eigenvalue: exact unipotent iterates.
for k in range(10):
    w = (Q(2), Q(3))
    for _ in range(k):
        w = apply(u, w)
    check(w == (2 + 3 * k, 3))

print(json.dumps({
    "status": "PASS",
    "exact_assertions": checks,
    "positive_matrix_controls": positive_controls,
    "branch_cone_controls": cone_controls,
    "unipotent_iterates": 10,
    "scope": "Algebraic consistency only; not a self-splitting recognition test",
    "artifact_sha256": hashlib.sha256((HERE / "OBSTRUCTION.md").read_bytes()).hexdigest(),
    "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}, indent=2))
