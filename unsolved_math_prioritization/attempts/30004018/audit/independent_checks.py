#!/usr/bin/env python3
"""Independent, source-free exact checks for the DS/socle diagnostic packet.

This file neither imports nor executes the author checker. Matrices are assembled
from actions on named bases; rank is computed by fraction-free determinants.
The general representation-theoretic imports are checked in the written report,
not proved by this finite executable. No writes; no assert statements.
"""
import argparse
import itertools
import json
import os
import sys


class Failure(Exception):
    pass


COUNT = 0


def require(condition, label):
    global COUNT
    COUNT += 1
    if not condition:
        raise Failure(label)


def event(name, **values):
    print(json.dumps(dict(event=name, **values), sort_keys=True))


def zeros(n, m=None):
    return [[0] * (n if m is None else m) for _ in range(n)]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def compose(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def plus(a, b, c=1):
    return [[a[i][j] + c * b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def diagonal(values):
    return [[x if i == j else 0 for j in range(len(values))]
            for i, x in enumerate(values)]


def determinant(a):
    """Bareiss exact division; unlike the author checker, no permutation sum."""
    a = [row[:] for row in a]
    n = len(a)
    if not n:
        return 1
    sign, previous = 1, 1
    for k in range(n - 1):
        if a[k][k] == 0:
            p = next((i for i in range(k + 1, n) if a[i][k]), None)
            if p is None:
                return 0
            a[p], a[k] = a[k], a[p]
            sign *= -1
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                require(numerator % previous == 0, 'Bareiss exact division')
                a[i][j] = numerator // previous
        for i in range(k + 1, n):
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def rank(a):
    if not a or not a[0]:
        return 0
    for r in range(min(len(a), len(a[0])), 0, -1):
        for rows in itertools.combinations(range(len(a)), r):
            for columns in itertools.combinations(range(len(a[0])), r):
                if determinant([[a[i][j] for j in columns] for i in rows]):
                    return r
    return 0


def action(basis, arrows):
    m = zeros(len(basis))
    for source, target, coefficient in arrows:
        m[basis.index(target)][basis.index(source)] += coefficient
    return m


def cohomology(d, parity):
    n = len(parity)
    require(compose(d, d) == zeros(n), 'square-zero differential')
    require(all(d[i][j] == 0 or parity[i] != parity[j]
                for i in range(n) for j in range(n)), 'odd differential')
    e = [i for i in range(n) if not parity[i]]
    o = [i for i in range(n) if parity[i]]
    r0 = rank([[d[i][j] for j in e] for i in o])
    r1 = rank([[d[i][j] for j in o] for i in e])
    require(rank(d) == r0 + r1, 'rank respects parity blocks')
    return (len(e) - r0 - r1, len(o) - r0 - r1)


def commutator(a, b, odd=False):
    return plus(compose(a, b), compose(b, a), 1 if odd else -1)


def representation(e, f, h1, h2, parity):
    z = zeros(len(parity))
    require(commutator(h1, h2) == z, 'Cartans commute')
    require(commutator(h1, e) == e, '[h1,e]=e')
    require(commutator(h2, e) == plus(z, e, -1), '[h2,e]=-e')
    require(commutator(h1, f) == plus(z, f, -1), '[h1,f]=-f')
    require(commutator(h2, f) == f, '[h2,f]=f')
    require(compose(e, e) == compose(f, f) == z, 'odd generator squares')
    require(commutator(e, f, True) == plus(h1, h2), '[e,f]=h1+h2')
    for d in (e, f):
        require(all(not d[i][j] or parity[i] != parity[j]
                    for i in range(len(parity)) for j in range(len(parity))),
                'representation has correct parity')


def tensor(a, b, parity_a, bad_sign=False):
    n, m = len(a), len(b)
    d = zeros(n * m)
    for i, j in itertools.product(range(n), range(m)):
        for k in range(n):
            d[k * m + j][i * m + j] += a[k][i]
        for l in range(m):
            d[i * m + l][i * m + j] += b[l][j] * (
                1 if bad_sign else (-1) ** parity_a[i])
    return d


def main(mutation):
    event('runtime', uid=os.getuid(), optimize=sys.flags.optimize,
          mutation=mutation, implementation='independent Bareiss-minors rank')
    require(os.getuid() == 1000, 'actual UID must be 1000')
    require(rank([[0, 2], [3, 0]]) == 2, 'rank oracle row-swap control')
    require(rank([[2, 4, 6], [3, 6, 9]]) == 1, 'rank oracle dependent control')
    require(determinant([[2, 3, 1], [1, 4, 0], [0, 2, 5]]) == 27,
            'rank oracle nonsingular control')

    # Exterior multiplication generates the projective, without prescribed matrices.
    basis = [(), (0,), (1,), (0, 1)]
    exterior = []
    for generator in (0, 1):
        d = zeros(4)
        for j, word in enumerate(basis):
            if generator not in word:
                target = tuple(sorted((generator,) + word))
                sign = (-1) ** sum(x < generator for x in word)
                if mutation == 'exterior-sign' and generator == 1 and word == (0,):
                    sign *= -1
                d[basis.index(target)][j] = sign
        exterior.append(d)
    ep, fp = exterior
    parity_p = [len(word) % 2 for word in basis]
    offsets = [sum(1 if x == 0 else -1 for x in word) for word in basis]
    if mutation == 'wrong-weight':
        offsets[1] += 1
    if mutation == 'wrong-parity':
        parity_p[1] = 0
    for a in (-101, -3, 0, 2, 97):
        weights = [a + x for x in offsets]
        representation(ep, fp, diagonal(weights), diagonal([-x for x in weights]), parity_p)
        require(cohomology(ep, parity_p) == cohomology(fp, parity_p) == (0, 0),
                'projective vanishes on both root axes')
    event('projective', basis=['1', 'e', 'f', 'ef'], weights_relative_to_a=offsets,
          parity=parity_p, rank_e=rank(ep), rank_f=rank(fp), both_DS=[0, 0])

    kc = ['v', 'w']
    ek, fk = zeros(2), action(kc, [('v', 'w', 1)])
    for a in (-101, -3, 0, 2, 97):
        representation(ek, fk, diagonal([a, a - 1]), diagonal([-a, 1 - a]), [0, 1])
    he, hf = cohomology(ek, [0, 1]), cohomology(fk, [0, 1])
    require(he == (1, 1) and hf == (0, 0), 'Kac objectwise DS values')
    require(he[0] - he[1] == hf[0] - hf[1] == 0, 'both reduced DS class values')
    if mutation == 'class-implies-object':
        require(he == (0, 0), 'zero reduced class does not imply zero object')
    event('Kac', DS_e=he, DS_f=hf, reduced_DS_e=0, reduced_DS_f=0)

    # Moment identities for every a, as coefficients of polynomials in a.
    # sum c_i (a+offset_i)^j, j=0,1,2, is determined by offset moments.
    pcoeff, kcoeff = [1, -1, -1, 1], [1, -1]
    pmom = [sum(c * (x ** j) for c, x in zip(pcoeff, [0, 1, -1, 0])) for j in range(3)]
    kmom = [sum(c * (x ** j) for c, x in zip(kcoeff, [0, -1])) for j in range(3)]
    require(pmom == [0, 0, -2], 'projective zeroth/first/second offset moments')
    require(kmom[:2] == [0, 1], 'Kac zeroth/first offset moments')
    if mutation == 'wrong-moment':
        require(kmom[1] == 0, 'moment separation rejects Kac membership in projective span')
    event('Laurent_class_separation', projective_moments=pmom, Kac_moments=kmom,
          ideal_projectives='(t-1)^2 R', ideal_common_DS_kernels='(t-1) R')

    bc = ['a', 'b', 'c', 'd']
    u = action(bc, [('a', 'b', 1), ('c', 'd', 1)])
    v = action(bc, [('c', 'b', 1)])
    p, q, parity = [0, 1, 1, 2], [1, 1, 0, 0], [1, 0, 1, 0]
    representation(u, zeros(4), diagonal(p), diagonal([-x for x in p]), parity)
    representation(v, zeros(4), diagonal(q), diagonal([-x for x in q]), parity)
    require(commutator(diagonal(p), v) == commutator(diagonal(q), u) == zeros(4),
            'cross-factor Cartans commute with other odd map')
    require(commutator(u, v, True) == zeros(4), 'cross-factor odd anticommutator')
    total = plus(u, v)
    if mutation == 'drop-total-arrow':
        total[3][2] = 0
    require(cohomology(total, parity) == (0, 0), 'total DS acyclicity')
    require(cohomology(v, parity) == (1, 1), 'first DS has both parities')
    # ker(v)=span(a,b,d), im(v)=span(b); u sends a to b and the rest to 0.
    cycles = [[int(i == j) for j in (0, 1, 3)] for i in range(4)]
    require(compose(v, cycles) == zeros(4, 3), 'explicit quotient cycles')
    require(rank(cycles) == 3 and rank(v) == 1, 'explicit quotient dimension')
    require(rank([v[i] + compose(u, cycles)[i] for i in range(4)]) == 1,
            'induced u on v cohomology is zero')
    require(total[1][0] == total[3][2] == 1, 'nonzero total rank-two minor')
    event('bicomplex', rank_total=rank(total), rank_v=rank(v), total_DS=[0, 0],
          iterated_DS=[1, 1], quotient_representatives=['a', 'd'],
          higher_differential='a -> -d (via the v-preimage c of u(a)=b)')

    # Algebra element rank is tested on the natural representation of the Levi.
    nat = ['even1', 'odd1', 'even2', 'odd2']
    un = action(nat, [('odd1', 'even1', 1)])
    vn = action(nat, [('odd2', 'even2', 1)])
    require(rank(un) == rank(vn) == 1 and rank(plus(un, vn)) == 2,
            'natural rank is separate from action rank on the diagnostic module')
    if mutation == 'action-rank-is-algebra-rank':
        require(rank(u) == rank(un), 'rank-one Lie element can act with rank two')
    event('natural_Levi_ranks', u=rank(un), v=rank(vn), u_plus_v=rank(plus(un, vn)),
          diagnostic_action_rank_u=rank(u))

    z, d = zeros(2), action(['even', 'odd'], [('even', 'odd', 1)])
    tensor_rows = []
    for x, y in itertools.product((z, d), repeat=2):
        td = tensor(x, y, [0, 1], bad_sign=(mutation == 'omit-Koszul-sign'))
        h = cohomology(td, [0, 1, 1, 0])
        hx, hy = cohomology(x, [0, 1]), cohomology(y, [0, 1])
        expected = (hx[0] * hy[0] + hx[1] * hy[1],
                    hx[0] * hy[1] + hx[1] * hy[0])
        require(h == expected, 'Kunneth preserves both parities')
        tensor_rows.append({'factor_ranks': [rank(x), rank(y)], 'DS': h})
    event('tensor_Kunneth', cases=tensor_rows)

    # Work in the square-zero quotient with t_i=1+epsilon_i. Negative powers
    # give (1+epsilon)^a=1+a epsilon for every integer a, including negative a.
    for r in range(1, 9):
        vectors = list(itertools.product((0, 1), repeat=r))
        require(len(vectors) == 2 ** r, 'square-zero quotient basis cardinality')
        require(all(sum(v) <= r for v in vectors), 'square-zero quotient normal form')
    def dual_product(x, y):
        return (x[0] * y[0], x[0] * y[1] + x[1] * y[0])
    def laurent_power(a):
        out = (1, 0)
        unit = (1, 1 if a >= 0 else -1)
        for _ in range(abs(a)):
            out = dual_product(out, unit)
        return out
    require(dual_product((0, 1), (0, 1)) == (0, 0), 'epsilon squared is zero')
    for a, b in itertools.product(range(-20, 21), repeat=2):
        require(dual_product(laurent_power(a), laurent_power(b)) == (1, a + b),
                'Laurent powers in dual numbers')
    event('tensor_ideal', ideal='((t_i-1)^2: 1<=i<=r)', quotient_dimension='2^r',
          all_integer_power_rule='(1+epsilon)^a=1+a*epsilon; epsilon^2=0')

    # Universal complex in C[u,v]/(uv), using the infinite monomial normal form.
    # The finite tests accompany (and do not replace) the written all-degree proof.
    monomials = [(0, 0)] + [(i, 0) for i in range(1, 129)] + [(0, j) for j in range(1, 129)]
    for variable in (0, 1):
        survivors = []
        for a, b in monomials:
            image = (a + (variable == 0), b + (variable == 1))
            dies = bool(image[0] and image[1])
            require(dies == bool(b if variable == 0 else a), 'node-ring annihilator criterion')
            if not dies:
                survivors.append(image)
        require(len(set(survivors)) == len(survivors), 'node-ring images cannot cancel')
    require(cohomology(z, [0, 1]) == (1, 1), 'origin specialization differs from ordinary cohomology')
    event('universal_complex', ann_u='(v)', ann_v='(u)', universal_cohomology=0,
          fiber_at_origin=[1, 1], scope='failure at origin, not a punctured-cone counterexample')
    event('complete', status='PASS', checks=COUNT, uid=os.getuid(), optimize=sys.flags.optimize,
          scope='finite diagnostic identities; no full-conjecture claim')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mutation', default='none', choices=[
        'none', 'exterior-sign', 'wrong-weight', 'wrong-parity',
        'class-implies-object', 'wrong-moment', 'drop-total-arrow',
        'action-rank-is-algebra-rank', 'omit-Koszul-sign'])
    args = parser.parse_args()
    try:
        main(args.mutation)
    except Failure as exc:
        event('complete', status='FAIL', reason=str(exc), checks=COUNT,
              mutation=args.mutation, uid=os.getuid(), optimize=sys.flags.optimize)
        sys.exit(1)
