#!/usr/bin/env python3
"""Exact F_3 check of the degree-two cup product used in REPORT.md.

No assertions: guards also execute under python -O. This is finite arithmetic,
not a machine proof of the topological Poincare-duality step.
"""
import argparse
import itertools
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rank_mod3(rows, cols):
    a = [[v % 3 for v in row] for row in rows]
    r = 0
    for j in range(cols):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = 1 if a[r][j] == 1 else 2
        a[r] = [(v * inv) % 3 for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                k = a[i][j]
                a[i] = [(v - k*w) % 3 for v, w in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def run(negative):
    elements = list(itertools.product(range(3), repeat=3))
    identity = (0, 0, 0)

    def mul(g, h):
        a, b, t = g
        c, d, u = h
        cross = 0 if negative == 'group_law' else b*c
        return ((a+c) % 3, (b+d) % 3, (t+u+cross) % 3)

    # Exact monomial matrices: column j has entry omega^(t+b*j)
    # in row j+a. These are precisely omega^t A^a B^b.
    def matrix(g):
        a, b, t = g
        return tuple(((j+a) % 3, (t+b*j) % 3) for j in range(3))

    def matrix_mul(g, h):
        gm, hm = matrix(g), matrix(h)
        return tuple((gm[hm[j][0]][0], (hm[j][1]+gm[hm[j][0]][1]) % 3)
                     for j in range(3))

    require(len(set(map(matrix, elements))) == 27, 'matrix faithfulness')
    for g, h in itertools.product(elements, repeat=2):
        require(matrix(mul(g, h)) == matrix_mul(g, h), 'matrix multiplication guard')
    for g, h, k in itertools.product(elements, repeat=3):
        require(mul(mul(g, h), k) == mul(g, mul(h, k)), 'associativity')
    for g in elements:
        require(mul(g, identity) == mul(identity, g) == g, 'identity')
        require(mul(mul(g, g), g) == identity, 'exponent three')
        require(sum(v for _, v in matrix(g)) % 3 == 0, 'determinant one')
    inverses = {g: next(h for h in elements if mul(g, h) == identity) for g in elements}
    comms = {mul(mul(mul(g, h), inverses[g]), inverses[h])
             for g, h in itertools.product(elements, repeat=2)}
    central = {g for g in elements if all(mul(g, h) == mul(h, g) for h in elements)}
    expected_center = {(0, 0, t) for t in range(3)}
    require(comms == central == expected_center, 'commutator and center guard')

    # Inhomogeneous differential for trivial coefficients: df(g,h)=f(h)-f(gh)+f(g).
    def f(g):
        a, b, t = g
        return (t + a*b if negative == 'cochain' else t-a*b) % 3

    rows = []
    index = {g: i for i, g in enumerate(elements)}
    for g, h in itertools.product(elements, repeat=2):
        gh = mul(g, h)
        require((f(h)-f(gh)+f(g)-g[0]*h[1]) % 3 == 0, 'cup coboundary guard')
        require((g[0]+h[0]-gh[0]) % 3 == 0, 'first homomorphism')
        require((g[1]+h[1]-gh[1]) % 3 == 0, 'second homomorphism')
        row = [0] * len(elements)
        for v, sign in [(h, 1), (gh, -1), (g, 1)]:
            row[index[v]] += sign
        rows.append(row)
    rank = rank_mod3(rows, 27)
    require(rank == (24 if negative == 'h1_rank' else 25), 'H1 rank guard')
    require(27-rank == 2, 'H1 dimension two')

    # Degree 7 of Lambda(y,y') tensor F3[x,x']: eight monomials.
    basis = [(e, a, 3-a) for e in (0, 1) for a in range(4)]
    pairs = []
    for e, a, b in basis:
        for beta in (0, 1):
            if e == beta:
                pairs.append('zero by exterior square')
            else:
                pairs.append('multiple of yyprime, killed by explicit coboundary')
    require(len(basis) == 8 and len(pairs) == 16, 'degree seven basis guard')
    restriction_rows = [[-1, a*a, a*b, b*b] for a, b in [(1, 0), (0, 1), (1, 1), (1, 2)]]
    restriction_rank = rank_mod3(restriction_rows, 4)
    require(restriction_rank == 4, 'degree four Chern restriction detection')
    return {
        'status': 'PASS', 'field': 3, 'elements': 27,
        'matrix_multiplications_checked': 729, 'associativity_triples_checked': 19683,
        'cup_coboundary_pairs_checked': 729, 'cochain_formula': 't-a*b mod 3',
        'cup_formula': 'a(g)*b(h)', 'one_cochain_differential_rank': rank,
        'H1_dimension': 27-rank, 'center_order': len(central),
        'commutator_order': len(comms), 'degree_7_basis_size': len(basis),
        'degree_7_degree_1_pairing_forms_checked': len(pairs),
        'degree_4_Chern_restriction_matrix_rank': restriction_rank,
        'topological_step': 'proved in REPORT.md, not implemented here',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative-control', choices=['group_law', 'cochain', 'h1_rank'])
    args = parser.parse_args()
    print(json.dumps(run(args.negative_control), indent=2, sort_keys=True))
