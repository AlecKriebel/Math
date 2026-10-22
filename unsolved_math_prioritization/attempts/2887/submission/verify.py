#!/usr/bin/env python3
"""Exact finite algebraic controls for KP-4.11. Not a topology/gauge-theory verifier."""
from fractions import Fraction
from itertools import product
import json


def transpose(a):
    return [list(x) for x in zip(*a)]


def matmul(a, b):
    assert len(a[0]) == len(b)
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def congruence(q, p):
    return matmul(transpose(p), matmul(q, p))


def determinant(a):
    if not a:
        return 1
    if len(a) == 1:
        return a[0][0]
    return sum((-1)**j*a[0][j]*determinant([r[:j]+r[j+1:] for r in a[1:]]) for j in range(len(a)))


def rank(a):
    if not a:
        return 0
    b = [[Fraction(x) for x in r] for r in a]
    row = 0
    for col in range(len(b[0])):
        pivot = next((i for i in range(row, len(b)) if b[i][col]), None)
        if pivot is None:
            continue
        b[row], b[pivot] = b[pivot], b[row]
        d = b[row][col]
        b[row] = [v/d for v in b[row]]
        for i in range(len(b)):
            if i != row:
                d = b[i][col]
                b[i] = [x-d*y for x, y in zip(b[i], b[row])]
        row += 1
        if row == len(b):
            break
    return row


def square(q, v):
    return sum(v[i]*q[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))


checks = {}
# Negative control: no numerical tolerance, Q0 is even while Q1 has an odd vector.
q0 = [[0, 1], [1, 0]]
q1 = [[0, 1], [1, 1]]
assert determinant(q0) == determinant(q1) == -1
for x, y in product(range(-25, 26), repeat=2):
    assert square(q0, (x, y)) == 2*x*y
    assert square(q1, (x, y)) == 2*x*y+y*y
    assert square(q0, (x, y)) % 2 == 0
assert square(q1, (0, 1)) == 1
checks['rank_two_negative_control'] = {
    'integer_vectors_checked': 51**2,
    'Q0_even_on_samples': True,
    'Q1_odd_witness': [0, 1],
    'both_determinants': -1,
    'scope': 'Algebraic control only; the all-vector parity proof is in the text.'}

# D -> D+rF gives k -> k+2r.
count = 0
for k, r in product(range(-30, 31), repeat=2):
    q = [[0, 1], [1, k]]
    p = [[1, r], [0, 1]]
    assert determinant(p) == 1
    assert congruence(q, p) == [[0, 1], [1, k+2*r]]
    count += 1
checks['bundle_form_shear_identities'] = {'exact_instances': count}

# Explicit odd stabilization basis. This is not a smooth cancellation theorem.
q_stable = [[0, 1, 0], [1, 0, 0], [0, 0, 1]]
p_stable = [[1, 0, 1], [0, 1, -1], [1, -1, 1]]
assert determinant(p_stable) == -1
stable_result = congruence(q_stable, p_stable)
assert stable_result == [[1, 0, 0], [0, 1, 0], [0, 0, -1]]
p_odd = [[0, 1], [1, -1]]
assert determinant(p_odd) == -1
assert congruence(q1, p_odd) == [[1, 0], [0, -1]]
checks['odd_stabilization'] = {'basis_columns': transpose(p_stable), 'determinant': -1,
                             'result': stable_result}

# Mayer-Vietoris ranks, AFTER the geometric input maps are justified in the text.
for n in range(65):
    a2 = [[0] for _ in range(n)] + [[1]]
    a1 = [[1]]
    h2_union = n+1-rank(a2) + 1-rank(a1)
    assert h2_union == n
checks['null_homologous_MV_rank_controls'] = {
    'H2_exterior_ranks_checked': [0, 64],
    'all_H2_union_ranks_preserved': True,
    'scope': 'Checks only the asserted matrices, not a manifold or embedding.'}

# The S4 knot exterior and tubular-neighbourhood homology input.
boundary = {0: 1, 1: 1, 2: 1, 3: 1, 4: 0}
pieces = {0: 2, 1: 1, 2: 1, 3: 0, 4: 0}
map_ranks = {0: 1, 1: 1, 2: 1, 3: 0, 4: 0}
union_betti = [pieces[i]-map_ranks[i]+boundary.get(i-1, 0)-map_ranks.get(i-1, 0) for i in range(5)]
assert union_betti == [1, 0, 0, 0, 1]
checks['local_Gluck_sphere_MV_ranks'] = {'betti': union_betti,
    'scope': 'Only rational ranks; integral isomorphism arguments are textual.'}

# Formal exceptional-class algebra; never evaluates a gauge invariant.
y_form = [[2, 1, 0], [1, 2, 0], [0, 0, -1]]
for a, b, c in product(range(-8, 9), repeat=3):
    for sign in (-1, 1):
        pairing = -sign*c
        assert (pairing == 0) == (c == 0)
    assert square(y_form, (a, b, 1)) == square(y_form, (a, b, -1))
    assert square(y_form, (a, b, 1)) == 2*a*a+2*a*b+2*b*b-1
checks['exceptional_class_algebra'] = {'integer_vectors_checked': 17**3,
    'both_signs_same_orthogonal_complement': True,
    'no_SW_invariant_computed': True}

# Expected SW dimension expression remains unchanged under K -> K +/- e.
for k2, chi, sigma in product(range(-8, 9), repeat=3):
    d_before = Fraction(k2-(2*chi+3*sigma), 4)
    d_after = Fraction((k2-1)-(2*(chi+1)+3*(sigma-1)), 4)
    assert d_before == d_after
checks['blowup_dimension_algebra'] = {'integer_triples_checked': 17**3,
    'scope': 'Formal dimension identity, not the gauge-theoretic blowup theorem.'}

print(json.dumps({'problem_id': 2887, 'result': 'PASS', 'arithmetic': 'exact integers and fractions',
    'checks': checks, 'limit': 'Finite algebraic controls only. No existence, homeomorphism, diffeomorphism, or gauge invariant is certified by this program.'}, indent=2, sort_keys=True))
