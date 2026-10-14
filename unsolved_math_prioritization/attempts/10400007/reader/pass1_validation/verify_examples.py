#!/usr/bin/env python3
"""Exact finite checks for the scoped Jones validation report.

No CAS or external knot package is used. Laurent polynomials are exponent->integer
maps. Jones calculations use independent DSU state enumeration and TL_2 algebra.
These calculations validate finite examples, not the general topological lemmas.
"""
from itertools import product
import json


def check(condition):
    if not condition:
        raise RuntimeError("Exact validation failed")


def clean(p):
    return {k: v for k, v in p.items() if v}

def add(a, b):
    r = a.copy()
    for k, v in b.items(): r[k] = r.get(k, 0) + v
    return clean(r)

def scale(p, c): return clean({k: c*v for k, v in p.items()})
def shift(p, n): return {k+n: v for k, v in p.items()}
def mul(a, b):
    r = {}
    for i, u in a.items():
        for j, v in b.items(): r[i+j] = r.get(i+j, 0) + u*v
    return clean(r)
def power(a, n):
    check(n >= 0)
    r = {0: 1}
    for _ in range(n): r = mul(r, a)
    return r

def reciprocal(p): return {-k: v for k, v in p.items()}

def display(p, var):
    return ' + '.join(f'{v}*{var}^{k}' for k, v in sorted(p.items())) or '0'

DELTA_A = {2: -1, -2: -1}


def bracket_dsu(word):
    m = len(word)
    total = {}
    for state in product((0, 1), repeat=m):
        parent = list(range(2*(m+1)))
        def root(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        def join(x, y): parent[root(x)] = root(y)
        exp = 0
        for j, (s, smoothing) in enumerate(zip(word, state)):
            check(s in (-1, 1))
            exp += s * (1 - 2*smoothing)
            if smoothing == 0:
                join(2*j, 2*j+2); join(2*j+1, 2*j+3)
            else:
                join(2*j, 2*j+1); join(2*j+2, 2*j+3)
        join(0, 2*m); join(1, 2*m+1)
        loops = len({root(j) for j in range(2*(m+1))})
        total = add(total, shift(power(DELTA_A, loops-1), exp))
    return total


def bracket_tl2(word):
    # A crossing is A^s I + A^(-s) E, and E^2=delta E.
    a, b = {0: 1}, {}
    for s in word:
        a, b = shift(a, s), add(shift(a, -s), add(shift(b, s), shift(mul(b, DELTA_A), -s)))
    return add(mul(a, DELTA_A), b)


def jones_z(word):
    # z=t^(1/2), A=t^(-1/4), (-A^3)^(-w) normalization.
    p = scale(shift(bracket_dsu(word), -3*sum(word)), (1 if sum(word) % 2 == 0 else -1))
    check(all(k % 2 == 0 for k in p))
    return {-k//2: int(v) for k, v in p.items()}


def jones_t(word):
    p = jones_z(word)
    check(all(k % 2 == 0 for k in p))
    return {k//2: v for k, v in p.items()}


def main():
    # Exhaustive finite algorithm cross-check and inverse-generator cancellation.
    cases = 0
    for n in range(9):
        for w in product((-1, 1), repeat=n):
            check(bracket_dsu(w) == bracket_tl2(w))
            check(jones_z(w + (1, -1)) == jones_z(w))
            cases += 1
    check(jones_z(()) == {-1: -1, 1: -1}) # 2-component unlink.
    check(jones_t((1,)) == jones_t((-1,)) == {0: 1})
    # Source skein convention: z^-2 V+ - z^2 V- = (z-z^-1)V0.
    skein_cases = 0
    for n in range(7):
        for rest in product((-1, 1), repeat=n):
            lhs = add(shift(jones_z((1,)+rest), -2), scale(shift(jones_z((-1,)+rest), 2), -1))
            rhs = mul({1: 1, -1: -1}, jones_z(rest))
            check(lhs == rhs)
            skein_cases += 1
    right = jones_t((1, 1, 1))
    left = jones_t((-1, -1, -1))
    check(right == {1: 1, 3: 1, 4: -1})
    check(left == {-1: 1, -3: 1, -4: -1} == reciprocal(right))
    check(right != left)
    # Seifert matrix S=((1,0),(-1,1)); mirror S'=-S^T.
    # tS-S^T=((t-1,1),(-t,t-1)); determinant=(t-1)^2+t.
    alex_det = add(power({1: 1, 0: -1}, 2), {1: 1})
    check(alex_det == {2: 1, 1: -1, 0: 1})
    alex = shift(alex_det, -1)
    # For -S^T determinant is the same; a unit off-diagonal entry gives
    # the cyclic Alexander module Lambda/(t^2-t+1) in each case.
    mirror_det = add(power({0: 1, 1: -1}, 2), {1: 1})
    check(mirror_det == alex_det)
    granny, square = mul(right, right), mul(right, left)
    check(granny != square)
    # Independently sum source-described five trefoil generator gradings.
    aqm = [(-1,3,-2), (0,3,-1), (1,3,0), (2,3,1), (2,4,0)]
    omega_jones, omega_alex = {}, {}
    for a, q, m in aqm:
        omega_alex = add(omega_alex, {a: (1 if m % 2 == 0 else -1)})
        omega_jones = add(omega_jones, {a-q: (1 if (m+q) % 2 == 0 else -1)})
    check(omega_alex == alex)
    check(omega_jones == left)
    # Trefoil Rees differential a->Vb: B(a)=B(b)=3, C(a)=0,C(b)=-1.
    gauge_a, gauge_b = (-3,0), (-3,1)
    coefficient = (0,1)
    check(tuple(gauge_a[i]+coefficient[i] for i in range(2)) == gauge_b)
    ja, jb = 2-3, 2-4
    check(ja-gauge_a[0]+gauge_a[1] == jb-gauge_b[0]+gauge_b[1] == 2)
    result = {
        'status': 'all exact checks passed',
        'algorithm_crosschecks': cases,
        'skein_cases': skein_cases,
        'normalization': 'V_unknot=1; t^-1 V_plus - t V_minus=(t^1/2-t^-1/2)V_smoothing',
        'right_trefoil_jones': display(right, 't'),
        'left_trefoil_jones': display(left, 't'),
        'both_trefoil_alexander': display(alex, 't'),
        'both_trefoil_alexander_module': 'Z[t,t^-1]/(t^2-t+1)',
        'granny_jones': display(granny, 't'),
        'square_jones': display(square, 't'),
        'both_composite_alexander': display(mul(alex, alex), 't'),
        'AJ_trefoil_Euler_at_d_1': display(omega_alex, 'x'),
        'AJ_trefoil_Euler_at_d_minus_xinv': display(omega_jones, 'x'),
        'AJ_trefoil_rees_pair': 'd(a)=V*b; localized basis e_a=U^-3*a, e_b=U^-3*V*b gives d(e_a)=e_b',
        'general_topology_tested_computationally': False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__': main()
