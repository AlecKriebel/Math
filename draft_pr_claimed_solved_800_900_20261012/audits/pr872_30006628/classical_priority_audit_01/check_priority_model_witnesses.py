#!/usr/bin/env python3
"""Exact, bounded law/spectral witnesses for a priority comparison.

This does not prove the asymptotic property-(T) claim or absence of prior work.
No assertions are used as guards, so optimized Python performs the same checks.
"""
from fractions import Fraction as F
from itertools import product
import json


CHECKS = []


def require(name, condition):
    if not condition:
        raise RuntimeError(name)
    CHECKS.append(name)


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def matvec(a, v):
    return [sum(x*y for x, y in zip(row, v)) for row in a]


def power(a, t):
    n = len(a)
    q = [[int(i == j) for j in range(n)] for i in range(n)]
    for _ in range(t):
        q = multiply(q, a)
    return q


def rank(a):
    a = [[F(x) for x in row] for row in a]
    rr = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rr, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rr], a[pivot] = a[pivot], a[rr]
        v = a[rr][col]
        a[rr] = [x/v for x in a[rr]]
        for i in range(len(a)):
            if i != rr and a[i][col]:
                v = a[i][col]
                a[i] = [x-v*y for x, y in zip(a[i], a[rr])]
        rr += 1
        if rr == len(a):
            break
    return rr


def kernel_dimension(a, eigenvalue):
    b = [[F(x)-eigenvalue*int(i == j) for j, x in enumerate(row)]
         for i, row in enumerate(a)]
    return len(a)-rank(b)


def kron(a, b):
    return [[x*y for x in row_a for y in row_b]
            for row_a in a for row_b in b]


def main():
    # Three infinite cyclic factors, two inverse letters per factor.
    colors = [i//2 for i in range(6)]
    a = [[int(colors[i] != colors[j]) for j in range(6)] for i in range(6)]
    b = [[int(j != (i ^ 1)) for j in range(6)] for i in range(6)]
    counts = []
    for t in range(1, 21):
        pa, pb = power(a, t), power(b, t)
        ca = sum(pa[i][i] for i in range(6))
        cb = sum(pb[i][i] for i in range(6))
        require(f'syllable_trace_formula_l{t}', ca == 4**t+2*(-2)**t)
        require(f'free_trace_formula_l{t}', cb == 5**t+3+2*(-1)**t)
        if t <= 6:
            ea = eb = 0
            for word in product(range(6), repeat=t):
                ea += all(a[word[i]][word[(i+1) % t]] for i in range(t))
                eb += all(b[word[i]][word[(i+1) % t]] for i in range(t))
            require(f'independent_cyclic_enumeration_l{t}', (ca, cb) == (ea, eb))
        counts.append({'length': t, 'syllable_count': ca, 'free_count': cb})
    require('reject_identical_sphere_support', counts[1]['syllable_count'] != counts[1]['free_count'])

    # A valid finite-factor example: all nonidentity elements of C7, C2, C2.
    color = [0]*6+[1, 2]
    r = [F(1)]*6+[F(2), F(2)]
    aa = [[int(color[i] != color[j]) for j in range(8)] for i in range(8)]
    require('unequal_Perron_vector', matvec(aa, r) == [4*x for x in r])
    p = [[F(aa[i][j])*r[j]/(4*r[i]) for j in range(8)] for i in range(8)]
    require('P_rows_stochastic', all(sum(row) == 1 for row in p))
    pi = [x*x/F(14) for x in r]
    require('P_reversible', all(pi[i]*p[i][j] == pi[j]*p[j][i] for i in range(8) for j in range(8)))
    expected_p = {F(1): 1, F(0): 5, F(-3, 4): 1, F(-1, 4): 1}
    for v, dim in expected_p.items():
        require(f'P_exact_eigenspace_{v}', kernel_dimension(p, v) == dim)
    q = [[F(1, 2), F(1, 2)], [F(1), F(0)]]
    t = kron(q, p)
    spectrum = {F(1): 1, F(-1, 2): 1, F(0): 10,
                F(-3, 4): 1, F(3, 8): 1, F(-1, 4): 1, F(1, 8): 1}
    for v, dim in spectrum.items():
        require(f'tensor_exact_eigenspace_{v}', kernel_dimension(t, v) == dim)
    require('tensor_spectral_dimensions_complete', sum(spectrum.values()) == len(t))
    second = max(v for v in spectrum if v != 1)
    gap = 1-second
    require('unequal_gap_exact_five_eighths', gap == F(5, 8))
    require('reject_uniform_three_quarter_gap', gap < F(3, 4))
    require('candidate_strict_half_margin_survives', gap > F(1, 2))

    print(json.dumps({'status': 'PASS', 'purpose': 'bounded exact priority-model witnesses only',
                      'checks': len(CHECKS), 'check_names': CHECKS, 'cyclic_counts': counts,
                      'part_sizes': [6, 1, 1], 'Perron_eigenvalue': 4,
                      'P_spectrum': {str(k): v for k, v in expected_p.items()},
                      'tensor_spectrum': {str(k): v for k, v in spectrum.items()},
                      'tensor_gap': str(gap), 'false_shortcuts_rejected':
                      ['identical ordinary/syllable word support', 'uniform 3/4 mean gap'],
                      'not_a_main_theorem_or_novelty_certificate': True}, indent=2))


if __name__ == '__main__':
    main()
