"""Exact integer checks for the authored orbit/lift and quotient-basis formulas.
No topological theorem is inferred from these finite checks.
"""
from itertools import combinations, product
from math import comb
import json

def add(x, y, scale=1):
    z = dict(x)
    for k, v in y.items():
        z[k] = z.get(k, 0) + scale * v
        if not z[k]:
            del z[k]
    return z

def wedge3(x, y, z):
    out = {}
    for i, u in x.items():
        for j, v in y.items():
            for k, w in z.items():
                if len({i, j, k}) != 3:
                    continue
                sign = (-1) ** ((i > j) + (i > k) + (j > k))
                out = add(out, {tuple(sorted((i, j, k))): sign * u * v * w})
    return out

def unit(i):
    return {i: 1}

def mon(i, j, k):
    return wedge3(unit(i), unit(j), unit(k))

def action(M, v):
    out = {}
    for (i, j, k), c in v.items():
        out = add(out, wedge3(M[i], M[j], M[k]), c)
    return out

def ident(g):
    return [unit(i) for i in range(2 * g)]

def U(g, i, j):
    M = ident(g)
    M[j] = add(M[j], unit(i))
    M[g + i] = add(M[g + i], unit(g + j), -1)
    return M

def T(g, i):
    M = ident(g)
    M[g + i] = add(M[g + i], unit(i))
    return M

def comm(M, v):
    return add(action(M, v), v, -1)

def D(g, i, j):
    return mon(i, g + i, g + j)

def B(g, i, j, k):
    if i == j:
        return D(g, j, k)
    if i == k:
        return {s: -v for s, v in D(g, k, j).items()}
    return comm(U(g, i, j), D(g, j, k))

def A(g, i, j, k):
    if k != j:
        return comm(T(g, j), B(g, i, j, k))
    return {s: -v for s, v in comm(T(g, i), B(g, j, i, j)).items()}

def C(g, i, j, k):
    return comm(T(g, k), A(g, i, j, k))

def rels(g):
    return [sum_dicts((mon(x, j, g + j) for j in range(g))) for x in range(2 * g)]

def sum_dicts(it):
    out = {}
    for v in it:
        out = add(out, v)
    return out

def pivots(g):
    return [tuple(sorted((x, (x % g + 1) % g, g + (x % g + 1) % g))) for x in range(2 * g)]

def reduce_vec(v, rs, ps):
    out = dict(v)
    for r, p in zip(rs, ps):
        out = add(out, r, -out.get(p, 0) * r[p])
    return out

def verify(g):
    lift_checks = 0
    for i, j, k in product(range(g), repeat=3):
        if j == k:
            continue
        if not B(g, i, j, k) == mon(i, g + j, g + k):
            raise RuntimeError('Exact supplementary check failed')
        lift_checks += 1
    for i, j in combinations(range(g), 2):
        for k in range(g):
            if not A(g, i, j, k) == mon(i, j, g + k):
                raise RuntimeError('Exact supplementary check failed')
            lift_checks += 1
    for i, j, k in combinations(range(g), 3):
        if not C(g, i, j, k) == mon(i, j, k):
            raise RuntimeError('Exact supplementary check failed')
        lift_checks += 1
    rs, ps = (rels(g), pivots(g))
    if not len(set(ps)) == 2 * g:
        raise RuntimeError('Exact supplementary check failed')
    for idx, (r, p) in enumerate(zip(rs, ps)):
        if not abs(r[p]) == 1:
            raise RuntimeError('Exact supplementary check failed')
        if not all((p not in rr for j, rr in enumerate(rs) if j != idx)):
            raise RuntimeError('Exact supplementary check failed')
        if not reduce_vec(r, rs, ps) == {}:
            raise RuntimeError('Exact supplementary check failed')
    W = [t for t in combinations(range(2 * g), 3) if t[0] < g]
    basis = [t for t in W if t not in ps]
    if not len(basis) == comb(2 * g, 3) - comb(g, 3) - 2 * g:
        raise RuntimeError('Exact supplementary check failed')
    for t in basis:
        if not reduce_vec({t: 1}, rs, ps) == {t: 1}:
            raise RuntimeError('Exact supplementary check failed')
    for t in W:
        v = reduce_vec({t: 1}, rs, ps)
        if not all((k in basis for k in v)):
            raise RuntimeError('Exact supplementary check failed')
        if not reduce_vec(v, rs, ps) == v:
            raise RuntimeError('Exact supplementary check failed')
    matrices = [T(g, i) for i in range(g)] + [U(g, i, j) for i in range(g) for j in range(g) if i != j]
    for M in matrices:
        for r in rs:
            if not reduce_vec(action(M, r), rs, ps) == {}:
                raise RuntimeError('Exact supplementary check failed')
        for t in W:
            if not all((s[0] < g for s in action(M, {t: 1}))):
                raise RuntimeError('Exact supplementary check failed')
    return {'g': g, 'rank_W': len(W), 'rank_Q': 2 * g, 'rank_L': len(basis), 'lift_identities_checked': lift_checks, 'parabolic_matrices_checked': len(matrices), 'status': 'PASS'}
if __name__ == '__main__':
    out = {'arithmetic': 'exact Python integers', 'scope': 'finite sanity checks, not substitutes for uniform proofs or topology', 'results': [verify(g) for g in range(3, 9)]}
    print(json.dumps(out, indent=2))
