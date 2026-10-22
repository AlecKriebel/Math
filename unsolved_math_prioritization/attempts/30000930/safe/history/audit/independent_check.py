#!/usr/bin/env python3
"""Independent exact tensor audit; no imports from the author's verifier.

The mixed Gysin maps are DERIVED as adjoints of restriction with respect to
Poincare duality, using linear algebra. Both weights remain indeterminates.
The only geometric inputs are the surface intersection forms and restriction.
"""
from fractions import Fraction as F
from itertools import product
import json


def solve(matrix, rhs):
    n = len(matrix)
    aug = [[F(x) for x in row] + [F(rhs[i])] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if aug[i][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        c = aug[col][col]
        aug[col] = [x / c for x in aug[col]]
        for row in range(n):
            if row != col:
                c = aug[row][col]
                aug[row] = [x - c*y for x, y in zip(aug[row], aug[col])]
    return [row[-1] for row in aug]


# Diagonal basis: 1, two divisor classes, positively oriented point class.
# The middle matrices are intersection pairings of divisors.
INTERSECTION = {'A': [[0, 1], [1, 0]], 'B': [[0, 1], [1, -2]]}
RESTRICTION = {'A': [[1, 0], [0, 1], [0, 1], [0, 0]],
               'B': [[1, 0], [0, 1], [0, -2], [0, 0]]}
NAMES = ['1_A', 'x', 'y', 'xy', '1_B', 'h', 's', 'hs', 'u', 'tu', 'v', 'tv']
LABELS = [('A', 'A')]*4 + [('B', 'B')]*4 + [('A', 'B')]*2 + [('B', 'A')]*2
LOCAL = list(range(4))*2 + list(range(2))*2
OFFSETS = {('A', 'A'): 0, ('B', 'B'): 4, ('A', 'B'): 8, ('B', 'A'): 10}
DEGREES = [0, 2, 2, 4]*2 + [1, 3]*2


def poincare(obj):
    q = INTERSECTION[obj]
    return [[0, 0, 0, 1], [0, q[0][0], q[0][1], 0],
            [0, q[1][0], q[1][1], 0], [1, 0, 0, 0]]


# P_G * G = R^T * P_C. P_C exchanges the two coordinates.
GYSIN = {obj: [solve(poincare(obj), [r[1-j] for r in RESTRICTION[obj]])
                for j in range(2)] for obj in 'AB'}
assert GYSIN['A'] == [[0, 1, 1, 0], [0, 0, 0, 1]]
assert GYSIN['B'] == [[0, 0, 1, 0], [0, 0, 0, 1]]


def diagonal_cup(obj, i, j):
    if i == 0:
        return {j: 1}
    if j == 0:
        return {i: 1}
    if i < 3 and j < 3:
        c = INTERSECTION[obj][i-1][j-1]
        return {3: c} if c else {}
    return {}


def curve_cup(a, b):
    return [a[0]*b[0], a[0]*b[1] + a[1]*b[0]]


# Tensor entry (output, power of lambda_A, power of lambda_B) -> rational.
def tensor_entry(i, j):
    left, mid = LABELS[i]
    mid2, right = LABELS[j]
    if mid != mid2:
        return {}
    oi, oj = LOCAL[i], LOCAL[j]
    offset = OFFSETS[left, right]
    if left == mid == right:
        return {(offset+k, 0, 0): F(v) for k, v in diagonal_cup(left, oi, oj).items()}
    a = RESTRICTION[left][oi] if left == mid else [int(oi == 0), int(oi == 1)]
    b = RESTRICTION[right][oj] if mid == right else [int(oj == 0), int(oj == 1)]
    c = curve_cup(a, b)
    if left != right:
        return {(offset+k, 0, 0): F(v) for k, v in enumerate(c) if v}
    push = [sum(c[j]*GYSIN[left][j][i] for j in range(2)) for i in range(4)]
    ea, eb = int(left == 'A'), int(left == 'B')
    return {(offset+k, ea, eb): v for k, v in enumerate(push) if v}


TENSOR = [[tensor_entry(i, j) for j in range(12)] for i in range(12)]


def associator(i, j, k):
    ans = {}
    for (middle, a, b), c in TENSOR[i][j].items():
        for (out, aa, bb), d in TENSOR[middle][k].items():
            key = out, a+aa, b+bb
            ans[key] = ans.get(key, F(0)) + c*d
    for (middle, a, b), c in TENSOR[j][k].items():
        for (out, aa, bb), d in TENSOR[i][middle].items():
            key = out, a+aa, b+bb
            ans[key] = ans.get(key, F(0)) - c*d
    return {k: v for k, v in ans.items() if v}


def evaluate(poly, a, b, prime=None):
    ans = {}
    for (out, x, y), coefficient in poly.items():
        ans[out] = ans.get(out, F(0)) + coefficient*a**x*b**y
    if prime:
        ans = {out: (v.numerator * pow(v.denominator, -1, prime)) % prime
               for out, v in ans.items()}
    return {NAMES[out]: int(v) if F(v).denominator == 1 else str(v)
            for out, v in sorted(ans.items()) if v}


def main():
    # Verify all 144 products preserve the codimension-shifted grading.
    assert all(DEGREES[o] == DEGREES[i] + DEGREES[j]
               for i, j in product(range(12), repeat=2) for o, a, b in TENSOR[i][j])
    # Verify two-sided unit, with symbolic weights.
    for i in range(12):
        for left in (False, True):
            ans = {}
            for e in (0, 4):
                for key, v in (TENSOR[e][i] if left else TENSOR[i][e]).items():
                    ans[key] = ans.get(key, 0) + v
            assert {k: v for k, v in ans.items() if v} == {(i, 0, 0): F(1)}
    all_defects = {(i, j, k): associator(i, j, k) for i, j, k in product(range(12), repeat=3)}
    nonzero = {ijk: p for ijk, p in all_defects.items() if p}
    assert nonzero == {(8, 10, 8): {(9, 1, 0): F(2), (9, 0, 1): F(2)},
                       (10, 8, 10): {(11, 1, 0): F(-2), (11, 0, 1): F(-2)}}
    scenarios = {}
    for name, a, b, prime in [('natural', 1, 1, None), ('opposite_sign', 1, -1, None),
                              ('zero_pairing', 0, 0, None), ('characteristic_2', 1, 1, 2),
                              ('characteristic_3', 1, 1, 3), ('characteristic_5', 1, 1, 5)]:
        defects = []
        for ijk, poly in all_defects.items():
            result = evaluate(poly, a, b, prime)
            if result:
                defects.append({'triple': [NAMES[i] for i in ijk], 'associator': result})
        scenarios[name] = {'basis_triples_checked': 1728, 'defect_count': len(defects), 'defects': defects}
    assert scenarios['natural']['defect_count'] == 2
    assert all(scenarios[x]['defect_count'] == 0 for x in ['opposite_sign', 'zero_pairing', 'characteristic_2'])
    assert all(scenarios[x]['defect_count'] == 2 for x in ['characteristic_3', 'characteristic_5'])
    report = {'status': 'PASS', 'implementation': 'Independent Poincare-duality adjoint and symbolic tensor contraction',
              'arithmetic': 'Exact Q[lambda_A,lambda_B]', 'basis': NAMES,
              'derived_gysin_columns': {o: [[int(x) for x in col] for col in GYSIN[o]] for o in 'AB'},
              'symbolic_associators': [
                  {'triple': ['u', 'v', 'u'], 'value': '2*(lambda_A+lambda_B)*tu'},
                  {'triple': ['v', 'u', 'v'], 'value': '-2*(lambda_A+lambda_B)*tv'}],
              'symbolic_triples_checked': 1728, 'all_other_symbolic_associators': 0,
              'unit_verified': True, 'grading_verified': True, 'scenarios': scenarios,
              'scope': 'Exact finite cohomological model; no coherent-sheaf Yoneda computation.'}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
