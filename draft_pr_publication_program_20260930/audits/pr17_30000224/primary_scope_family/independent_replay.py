"""Independent exact arithmetic replay; no imports from the frozen verifier."""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json


def mono(c, *e):
    return {tuple(e): c} if c else {}


def add(*ps):
    out = {}
    for p in ps:
        for e, c in p.items():
            out[e] = out.get(e, 0) + c
    return {e: c for e, c in out.items() if c}


def mul(p, q):
    out = {}
    for a, c in p.items():
        for b, d in q.items():
            e = tuple(x + y for x, y in zip(a, b))
            out[e] = out.get(e, 0) + c * d
    return {e: c for e, c in out.items() if c}


def neg(p):
    return {e: -c for e, c in p.items()}


def vadd(*vs):
    return [add(*(v[i] for v in vs)) for i in range(len(vs[0]))]


def scale(p, v):
    return [mul(p, x) for x in v]


def det2(a, b, c, d):
    return add(mul(a, d), neg(mul(b, c)))


def rank(columns):
    a = [[Fraction(x) for x in row] for row in zip(*columns)]
    m, n = len(a), len(a[0])
    row = 0
    for col in range(n):
        pivot = next((i for i in range(row, m) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        c = a[row][col]
        a[row] = [x / c for x in a[row]]
        for i in range(m):
            if i != row and a[i][col]:
                c = a[i][col]
                a[i] = [x - c * y for x, y in zip(a[i], a[row])]
        row += 1
        if row == m:
            break
    return row


checks = 0


def check(test):
    global checks
    assert test
    checks += 1


# Full quartic Veronese exponent slices omit only exponent 2 in degree one.
generators = {0, 1, 3, 4}
slice_ = {0}
for degree in range(1, 21):
    slice_ = {x + y for x in slice_ for y in generators}
    check(slice_ == (generators if degree == 1 else set(range(4 * degree + 1))))

# The derivative kernel frame consists of cubic columns, hence O(-7)^2.
s3, s2t, st2, t3 = (mono(1, 3, 0), mono(1, 2, 1),
                     mono(1, 1, 2), mono(1, 0, 3))
J = [[mono(4, 3, 0), mono(3, 2, 1), t3, {}],
     [{}, s3, mono(3, 1, 2), mono(4, 0, 3)]]
U = [[mono(2, 0, 3), {}], [mono(-3, 1, 2), t3],
     [s3, mono(-3, 2, 1)], [{}, mono(2, 3, 0)]]
for i in range(2):
    for j in range(2):
        check(not add(*(mul(J[i][k], U[k][j]) for k in range(4))))
check(det2(J[0][0], J[0][1], J[1][0], J[1][1]) == mono(4, 6, 0))
check(det2(J[0][2], J[0][3], J[1][2], J[1][3]) == mono(4, 0, 6))
check(det2(U[0][0], U[0][1], U[1][0], U[1][1]) == mono(2, 0, 6))
check(det2(U[2][0], U[2][1], U[3][0], U[3][1]) == mono(2, 6, 0))

# Koszul first-homology socle certificate for I=(wy,wz,xy,xz).
w, x, y, z = [mono(1, *(int(i == j) for i in range(4))) for j in range(4)]
f = [mul(w, y), mul(w, z), mul(x, y), mul(x, z)]
boundaries = {}
for i, j in combinations(range(4), 2):
    v = [{} for _ in range(4)]
    v[i], v[j] = neg(f[j]), f[i]
    boundaries[i + 1, j + 1] = v
c = [neg(f[3]), f[2], {}, {}]
check(not add(*(mul(a, b) for a, b in zip(c, f))))
d12, d13, d14, d23, d24, d34 = [boundaries[k] for k in boundaries]
check(scale(w, c) == scale(x, d12))
check(scale(x, c) == vadd(scale(x, d14), scale(neg(w), d34), scale(neg(x), d23)))
check(scale(y, c) == vadd(scale(z, d13), scale(neg(y), d23)))
check(scale(z, c) == vadd(scale(z, d14), scale(neg(y), d24)))
rows = sorted({(i, e) for v in [*boundaries.values(), c]
               for i, p in enumerate(v) for e in p})
cols = [[v[i].get(e, 0) for i, e in rows] for v in [*boundaries.values(), c]]
check(rank(cols[:-1]) == 6)
check(rank(cols) == 7)

result = {
    "assertions": checks,
    "boundary_rank": rank(cols[:-1]),
    "boundary_plus_cycle_rank": rank(cols),
    "verdict": "pass",
    "scope": "Exact identities and finite degree slices only; universal deductions are in report.md.",
}
out = Path(__file__).with_name("replay_results.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
