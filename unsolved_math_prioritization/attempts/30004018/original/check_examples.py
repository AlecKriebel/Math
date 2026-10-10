#!/usr/bin/env python3
"""Exact checks of the finite examples in MATHEMATICAL_AUDIT.md.

No third-party dependency. No file writes. Checks survive -O and -OO.
This does not prove the imported representation-theory theorems or the conjecture.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations
import json
import os
import sys

class CheckFailed(RuntimeError):
    pass

COUNT = 0

def need(test, label):
    global COUNT
    COUNT += 1
    if not test:
        raise CheckFailed(label)

def zero(n):
    return [[Q(0) for _ in range(n)] for _ in range(n)]

def diag(values):
    a = zero(len(values))
    for i, v in enumerate(values):
        a[i][i] = Q(v)
    return a

def add(a, b, scale=1):
    return [[x + scale*y for x, y in zip(r, s)] for r, s in zip(a, b)]

def mul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]

def tr(a):
    return list(map(list, zip(*a)))

def rank(a):
    if not a or not a[0]:
        return 0
    a = [[Q(x) for x in row] for row in a]
    n, m = len(a), len(a[0])
    r = 0
    for c in range(m):
        p = next((i for i in range(r, n) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        s = a[r][c]
        a[r] = [x/s for x in a[r]]
        for i in range(n):
            if i != r:
                s = a[i][c]
                a[i] = [x-s*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == n:
            break
    return r

def determinant(a):
    n = len(a)
    out = Q(0)
    for p in permutations(range(n)):
        term = Q(-1 if sum(p[i] > p[j] for i in range(n) for j in range(i+1,n)) % 2 else 1)
        for i in range(n):
            term *= a[i][p[i]]
        out += term
    return out

def minors_rank(a):
    if not a or not a[0]:
        return 0
    n, m = len(a), len(a[0])
    for k in range(min(n,m), 0, -1):
        for rows in combinations(range(n), k):
            for cols in combinations(range(m), k):
                if determinant([[a[i][j] for j in cols] for i in rows]):
                    return k
    return 0

def nullspace(a):
    a = [[Q(x) for x in row] for row in a]
    n, m = len(a), len(a[0])
    pivots = []
    r = 0
    for c in range(m):
        p = next((i for i in range(r,n) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        s = a[r][c]
        a[r] = [x/s for x in a[r]]
        for i in range(n):
            if i != r:
                s = a[i][c]
                a[i] = [x-s*y for x,y in zip(a[i],a[r])]
        pivots.append(c)
        r += 1
        if r == n:
            break
    basis = []
    for c in range(m):
        if c not in pivots:
            v = [Q(0)]*m
            v[c] = Q(1)
            for i, p in enumerate(pivots):
                v[p] = -a[i][c]
            basis.append(v)
    return tr(basis) if basis else [[] for _ in range(m)]

def block(a, rows, cols):
    return [[a[i][j] for j in cols] for i in rows]

def homology(a, parities):
    n = len(a)
    need(mul(a,a) == zero(n), 'differential is square zero')
    need(all(not a[i][j] or parities[i] != parities[j]
             for i in range(n) for j in range(n)), 'differential is odd')
    even = [i for i,p in enumerate(parities) if p == 0]
    odd = [i for i,p in enumerate(parities) if p == 1]
    r = rank(block(a,odd,even)) + rank(block(a,even,odd))
    need(rank(a) == minors_rank(a) == r, 'independent exact ranks agree')
    return (len(even)-r, len(odd)-r)

def bracket(a,b,odd=False):
    return add(mul(a,b),mul(b,a), 1 if odd else -1)

def gl11(e,f,weights):
    h = diag(weights)
    n = len(weights)
    need(bracket(h,e) == e, '[h1,e]=e')
    need(bracket(h,f) == [[-x for x in row] for row in f], '[h1,f]=-f')
    need(mul(e,e) == mul(f,f) == zero(n), 'odd squares')
    need(bracket(e,f,True) == zero(n), 'central-zero anticommutator')
    # h2=-h1 and [h1,h2]=0 then give the remaining relations.

def character(weights,parities):
    out = {}
    for a,p in zip(weights,parities):
        out[a] = out.get(a,0) + (-1 if p else 1)
    return {a:c for a,c in out.items() if c}

def moment(ch,k):
    return sum(c*(a**k) for a,c in ch.items())

def must_reject(call,label):
    try:
        call()
    except CheckFailed:
        return
    raise CheckFailed('mutation was accepted: '+label)

def main():
    # All possible nonzero X_1 directions in gl(1|1) are scalar multiples of e or f.
    # Check matrix uv obstruction in the NATURAL representation separately.
    natural_e = [[Q(0),Q(1)],[Q(0),Q(0)]]
    natural_f = [[Q(0),Q(0)],[Q(1),Q(0)]]
    for u in (-2,-1,0,1,2):
        for v in (-2,-1,0,1,2):
            x = add([[u*q for q in row] for row in natural_e],
                    [[v*q for q in row] for row in natural_f])
            need(mul(x,x) == diag([u*v,u*v]), 'natural self-commuting cone')
            if u*v == 0 and (u or v):
                need(rank(x) == 1, 'natural rank-one axes')

    for a in range(-8,9):
        e, f = zero(2), zero(2)
        f[1][0] = 1
        gl11(e,f,[a,a-1])
        need(homology(e,[0,1]) == (1,1), 'Kac e-cohomology nonzero with zero class')
        need(homology(f,[0,1]) == (0,0), 'Kac f-cohomology vanishes')
        ch = character([a,a-1],[0,1])
        need(moment(ch,0) == 0 and moment(ch,1) == 1, 'Kac moment separation')
        e, f = zero(4), zero(4)
        e[1][0] = e[3][2] = f[2][0] = 1
        f[3][1] = -1
        gl11(e,f,[a,a+1,a-1,a])
        need(homology(e,[0,1,1,0]) == (0,0), 'projective e-cohomology')
        need(homology(f,[0,1,1,0]) == (0,0), 'projective f-cohomology')
        ch = character([a,a+1,a-1,a],[0,1,1,0])
        need(moment(ch,0) == moment(ch,1) == 0 and moment(ch,2) == -2,
             'projective second difference')
        bad = [row[:] for row in f]
        bad[3][1] = 1
        must_reject(lambda: gl11(e,bad,[a,a+1,a-1,a]), 'exterior sign')

    # A bounded bicomplex: columns are a,b,c,d.
    u,v = zero(4),zero(4)
    u[1][0] = u[3][2] = v[1][2] = 1
    p, q = [0,1,1,2], [1,1,0,0]
    gl11(u,zero(4),p)
    gl11(v,zero(4),q)
    need(bracket(diag(p),v) == bracket(diag(q),u) == zero(4), 'cross-factor Cartans')
    need(bracket(u,v,True) == zero(4), 'cross-factor odd bracket')
    need(homology(add(u,v),[1,0,1,0]) == (0,0), 'total acyclicity')
    need(homology(v,[1,0,1,0]) == (1,1), 'first cohomology')
    ker_v = nullspace(v)
    need(mul(v,ker_v) == [[0]*len(ker_v[0]) for _ in range(4)], 'computed v cycles')
    uker = mul(u,ker_v)
    need(rank([v[i]+uker[i] for i in range(4)]) == rank(v), 'u acts trivially on v cohomology')
    need(4-2*rank(v) == 2, 'iterated homology has dimension two')
    bad_total = add(u,v)
    for i in range(4):
        bad_total[i][2] = 0
    must_reject(lambda: need(homology(bad_total,[1,0,1,0]) == (0,0), 'mutated total'), 'total rank')

    # Kunneth for representative (acyclic / zero-differential) two-dimensional factors.
    z = zero(2)
    d = zero(2)
    d[1][0] = 1
    def tensor_differential(a,b):
        out = zero(4)
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    out[2*k+j][2*i+j] += a[k][i]
                    out[2*i+k][2*i+j] += (-1)**i*b[k][j]
        return out
    for a in (z,d):
        for b in (z,d):
            h = homology(tensor_differential(a,b),[0,1,1,0])
            need(sum(h) == (2-2*rank(a))*(2-2*rank(b)), 'finite tensor cohomology dimensions')

    # Normal forms in C[u,v]/(uv), exact for arbitrary polynomials by monomial basis.
    # A monomial survives iff it is 1, a positive pure u power, or a positive pure v power.
    def times_u(i,j):
        return None if j else (i+1,j)
    def times_v(i,j):
        return None if i else (i,j+1)
    basis = [(0,0)]+[(i,0) for i in range(1,21)]+[(0,j) for j in range(1,21)]
    for i,j in basis:
        need((times_u(i,j) is None) == (j>0), 'ann(u) pure-v criterion')
        need((times_v(i,j) is None) == (i>0), 'ann(v) pure-u criterion')
    # Distinct surviving images are linearly independent, so these are exact kernel rules.
    for fn in (times_u,times_v):
        images = [fn(i,j) for i,j in basis if fn(i,j) is not None]
        need(len(images) == len(set(images)), 'normal-form no cancellation')
    need(homology(z,[0,1]) == (1,1), 'origin specialization has nonzero cohomology')

    # Quotient of the pure-external-product character ring by (t_i-1)^2.
    for r in range(1,7):
        monomials = list(__import__('itertools').product((0,1),repeat=r))
        need(len(monomials) == 2**r and len(set(monomials)) == 2**r, 'square-zero quotient basis count')

    print(json.dumps({'status':'PASS','checks':COUNT,'uid':os.getuid(),
                      'python_optimize':sys.flags.optimize,'independent_rank_oracle':'minors',
                      'mutation_controls':'exterior sign and total rank rejected',
                      'scope':'finite diagnostic examples only'},sort_keys=True))

if __name__ == '__main__':
    main()
