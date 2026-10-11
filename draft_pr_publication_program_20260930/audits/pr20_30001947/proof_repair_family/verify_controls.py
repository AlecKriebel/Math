#!/usr/bin/env python3
"""Exact finite cochain controls, not a universal proof of the target theorem.

RP3 cellular cochains have d1=2.  For Y=Sigma RP3, Deligne cohomology
at the two vertices is represented by the homotopy fiber of
tau_{<=p} C(RP3) + tau_{<=p} C(RP3) -> C(RP3).
The chosen models are good truncations, NOT brutal truncations.
All integer kernels below have integral unit-pivot bases; this is checked.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import gcd
from pathlib import Path
import json


def rref(a):
    a = [[Q(x) for x in row] for row in a]
    if not a:
        return a, []
    pivots, r = [], 0
    for c in range(len(a[0])):
        pivot = next((k for k in range(r, len(a)) if a[k][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][c]
        a[r] = [x / v for x in a[r]]
        for k in range(len(a)):
            if k != r and a[k][c]:
                v = a[k][c]
                a[k] = [x - v * y for x, y in zip(a[k], a[r])]
        pivots.append(c)
        r += 1
        if r == len(a):
            break
    return a, pivots


def integer_kernel(a, n):
    rr, piv = rref(a)
    free = [k for k in range(n) if k not in piv]
    basis = []
    for k in free:
        v = [Q(0)] * n
        v[k] = 1
        for row, pivot in enumerate(piv):
            v[pivot] = -rr[row][k]
        assert all(Q(x).denominator == 1 for x in v)
        basis.append([int(x) for x in v])
    # The free coordinates are identity, so the basis spans the full Z kernel.
    return basis, free


def determinant(a):
    if not a:
        return 1
    a = [[Q(x) for x in row] for row in a]
    v = Q(1)
    for k in range(len(a)):
        p = next((p for p in range(k, len(a)) if a[p][k]), None)
        if p is None:
            return 0
        if p != k:
            a[k], a[p] = a[p], a[k]
            v = -v
        z = a[k][k]
        v *= z
        for j in range(k + 1, len(a)):
            q = a[j][k] / z
            a[j] = [x - q * y for x, y in zip(a[j], a[k])]
    assert v.denominator == 1
    return int(v)


def smith_invariants(a):
    if not a or not a[0]:
        return []
    rank = len(rref(a)[1])
    divisors = [1]
    for k in range(1, rank + 1):
        d = 0
        for rows in combinations(range(len(a)), k):
            for cols in combinations(range(len(a[0])), k):
                d = gcd(d, abs(determinant([[a[r][c] for c in cols] for r in rows])))
        assert d
        divisors.append(d)
    return [divisors[k] // divisors[k - 1] for k in range(1, len(divisors))]


def rank2(a):
    if not a:
        return 0
    a = [[x % 2 for x in row] for row in a]
    r = 0
    for c in range(len(a[0])):
        p = next((p for p in range(r, len(a)) if a[p][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        for k in range(len(a)):
            if k != r and a[k][c]:
                a[k] = [x ^ y for x, y in zip(a[k], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def fiber(cutoff, mod2=False):
    # At the cutoff, good truncation uses ker d, not the whole cochain group.
    ad = [k for k in range(4) if k <= cutoff and
          not (k == cutoff == 1 and not mod2)]
    labels = {k: ([('N', k), ('S', k)] if k in ad else []) +
              ([('L', k - 1)] if 0 <= k - 1 <= 3 else [])
              for k in range(6)}
    d = {}
    for k in range(5):
        rows, cols = labels[k + 1], labels[k]
        matrix = [[0] * len(cols) for _ in rows]
        for j, (place, degree) in enumerate(cols):
            if place in ('N', 'S'):
                if (place, degree + 1) in rows and degree == 1:
                    matrix[rows.index((place, degree + 1))][j] = 0 if mod2 else 2
                matrix[rows.index(('L', degree))][j] = 1 if place == 'N' else -1
            elif degree == 1:
                matrix[rows.index(('L', degree + 1))][j] = 0 if mod2 else -2
        d[k] = matrix
    for k in range(4):
        for row in d[k + 1]:
            for col in zip(*d[k]):
                assert sum(x * y for x, y in zip(row, col)) == 0
    return labels, d


def ih_integer(cutoff):
    lab, d = fiber(cutoff)
    out = []
    for k in range(5):
        basis, free = integer_kernel(d[k], len(lab[k]))
        incoming = d[k - 1] if k else [[] for _ in lab[k]]
        rel = [incoming[j] for j in free]
        # Verify every incoming column is reconstructed by its kernel coordinates.
        for col in range(len(incoming[0]) if incoming else 0):
            coordinates = [incoming[j][col] for j in free]
            reconstructed = [sum(basis[j][i] * coordinates[j] for j in range(len(basis)))
                             for i in range(len(lab[k]))]
            assert reconstructed == [row[col] for row in incoming]
        inv = smith_invariants(rel)
        out.append({'free_rank': len(basis) - len(inv), 'torsion': [x for x in inv if x > 1]})
    return out


def ih_mod2(cutoff):
    lab, d = fiber(cutoff, True)
    return [len(lab[k]) - rank2(d[k]) - (rank2(d[k - 1]) if k else 0)
            for k in range(5)]


def reduction_rank(cutoff, degree):
    zlab, zd = fiber(cutoff)
    flab, fd = fiber(cutoff, True)
    basis, _ = integer_kernel(zd[degree], len(zlab[degree]))
    reduced = [[0] * len(basis) for _ in flab[degree]]
    for j, b in enumerate(basis):
        for i, label in enumerate(zlab[degree]):
            reduced[flab[degree].index(label)][j] = b[i] % 2
    boundaries = fd[degree - 1] if degree else [[] for _ in flab[degree]]
    combined = [a + b for a, b in zip(boundaries, reduced)]
    return rank2(combined) - rank2(boundaries)


def main():
    integer = ih_integer(1)
    f2 = ih_mod2(1)
    assert integer == [
        {'free_rank': 1, 'torsion': []}, {'free_rank': 0, 'torsion': []},
        {'free_rank': 0, 'torsion': []}, {'free_rank': 0, 'torsion': [2]},
        {'free_rank': 1, 'torsion': []}]
    assert f2 == [1, 1, 0, 1, 1]
    reduction = reduction_rank(1, 3) + reduction_rank(1, 1)
    assert reduction == 1 and f2[3] + f2[1] == 2
    assert integer[4] == {'free_rank': 1, 'torsion': []}
    top = ih_mod2(2)[4]  # X degree six = Y degree four tensor S2 degree two.
    loose = ih_mod2(3)[4]
    assert top == 1 and loose == 0
    bounds = []
    for j in range(1, 9):
        for c in range(2, 33):
            m, t = (c - 2) // 2, c - 2
            r = min(4 * m, 2 * m + 1, m + 2 * j + 1)
            bounds.append({'j': j, 'codimension': c, 'm': m, 'top': t, 'Adem_destination': r})
    assert next(x for x in bounds if x['j'] == 1 and x['codimension'] == 4)['Adem_destination'] == 3
    H = [[0, 1], [1, 0]]
    assert all(sum(v[i] * H[i][k] * v[k] for i in range(2) for k in range(2)) % 2 == 0
               for v in ((0, 0), (0, 1), (1, 0), (1, 1)))
    result = {
        'scope': 'finite Mayer-Vietoris good-truncation cochain controls; no universal theorem proof',
        'Y': 'Sigma RP3', 'X': 'Y times S2',
        'Y_IH_lower_middle_Z': integer, 'Y_IH_lower_middle_F2_dimensions': f2,
        'X_IH3_Z': {'free_rank': 0, 'torsion': [2]}, 'X_IH3_F2_dimension': 2,
        'X_IH4_Z': {'free_rank': 1, 'torsion': []}, 'X_middle_reduction_rank': reduction,
        'X_top_IH6_F2_dimension': top, 'X_loose_r4_equals3_IH6_F2_dimension': loose,
        'X_middle_pairing_analytic_product_duality': H,
        'universal_same_middle_lift_control': 'fails',
        'generic_top_to_loose_comparison_injectivity_control': 'fails',
        'target_theorem_counterexample': False,
        'perversity_bound_controls': bounds, 'all_checks_passed': True}
    Path(__file__).with_name('CONTROL_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'perversity_bound_controls'}, indent=2))


if __name__ == '__main__':
    main()
