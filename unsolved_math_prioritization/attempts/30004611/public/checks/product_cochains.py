#!/usr/bin/env python3
# Reader edition: explicit runtime checks; results go only to stdout.
"""Independent full derivation-sheaf cochains for xyz(x+y+z)[w].

No source programs or earlier test routines are used. Each stalk is built
directly as the kernel of polynomial divisibility constraints. The normalized
poset differential uses coefficients at the final vertex of a strict chain.
"""
from itertools import combinations, product
from math import comb
import json

def monomials(n, d):
    if n == 1:
        return [(d,)]
    return [(i,) + a for i in range(d + 1) for a in monomials(n - 1, d - i)]

def rref(a, p, ncols):
    a = [[v % p for v in row] for row in a]
    rank = 0
    pivots = []
    for j in range(ncols):
        k = next((k for k in range(rank, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[rank], a[k] = (a[k], a[rank])
        inv = pow(a[rank][j], -1, p)
        a[rank] = [v * inv % p for v in a[rank]]
        for k in range(len(a)):
            if k != rank and a[k][j]:
                q = a[k][j]
                a[k] = [(v - q * w) % p for v, w in zip(a[k], a[rank])]
        pivots.append(j)
        rank += 1
        if rank == len(a):
            break
    return (a[:rank], pivots)

def nullspace(a, p, ncols):
    rows, pivots = rref(a, p, ncols)
    free = [j for j in range(ncols) if j not in pivots]
    basis = []
    for j in free:
        v = [0] * ncols
        v[j] = 1
        for row, k in zip(rows, pivots):
            v[k] = -row[j] % p
        basis.append(v)
    return (basis, free)

def quotient_monomial(a, linear, p):
    pivot = next((i for i, v in enumerate(linear) if v % p))
    terms = {(0,) * len(a): 1}
    for i, degree in enumerate(a):
        for _ in range(degree):
            next_terms = {}
            variables = [(i, 1)] if i != pivot else [(j, -linear[j] * pow(linear[pivot], -1, p) % p) for j in range(len(a)) if j != pivot and linear[j] % p]
            for exponent, value in terms.items():
                for j, c in variables:
                    e = list(exponent)
                    e[j] += 1
                    e = tuple(e)
                    next_terms[e] = (next_terms.get(e, 0) + value * c) % p
            terms = {e: c for e, c in next_terms.items() if c}
    return terms

def stalk(active, normals, degree, p):
    n = len(normals[0])
    mons = monomials(n, degree)
    ambient = n * len(mons)
    constraints = []
    for h in active:
        linear = normals[h]
        residues = [quotient_monomial(a, linear, p) for a in mons]
        outputs = sorted({b for r in residues for b in r})
        for b in outputs:
            constraints.append([linear[i] * residue.get(b, 0) % p for i in range(n) for residue in residues])
    return nullspace(constraints, p, ambient)

def gf2_rank(rows):
    pivots = {}
    for row in rows:
        while row:
            col = row.bit_length() - 1
            if col in pivots:
                row ^= pivots[col]
            else:
                pivots[col] = row
                break
    return len(pivots)

def sparse_rank(rows, p):
    pivots = {}
    for row in rows:
        row = dict(row)
        while row:
            col = max(row)
            if col not in pivots:
                inv = pow(row[col], -1, p)
                pivots[col] = {j: v * inv % p for j, v in row.items()}
                break
            q = row[col]
            for j, v in pivots[col].items():
                new = (row.get(j, 0) - q * v) % p
                if new:
                    row[j] = new
                else:
                    row.pop(j, None)
    return len(pivots)

def run(n, degree, p):
    normals = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]
    flats = [frozenset()] + [frozenset(c) for k in (1, 2) for c in combinations(range(4), k)] + [frozenset(range(4))]
    if n == 4:
        normals = [a + (0,) for a in normals] + [(0, 0, 0, 1)]
        flats = [s | t for s in flats for t in (frozenset(), frozenset({4}))]
    poset = sorted((s for s in flats if len(s) != len(normals)), key=lambda s: (-len(s), tuple(s)))
    found = set()
    for mask in range(1 << len(normals)):
        eqs = [normals[h] for h in range(len(normals)) if mask >> h & 1]
        kernel, _ = nullspace(eqs, p, n)
        found.add(frozenset((h for h, a in enumerate(normals) if all((sum((x * y for x, y in zip(a, v))) % p == 0 for v in kernel)))))
    if not found == set(flats):
        raise RuntimeError('Check failed at accepted-source line 144')
    data = [stalk(active, normals, degree, p) for active in poset]
    dimensions = [len(basis) for basis, _ in data]
    inclusions = {}
    for x, ax in enumerate(poset):
        for y, ay in enumerate(poset):
            if ay < ax:
                source, _ = data[x]
                target, free = data[y]
                matrix = [[v[j] for v in source] for j in free]
                for k, v in enumerate(source):
                    recovered = [sum((matrix[j][k] * target[j][i] for j in range(len(target)))) % p for i in range(len(v))]
                    if not recovered == v:
                        raise RuntimeError('Check failed at accepted-source line 160')
                inclusions[x, y] = matrix
    chains = [[(i,) for i in range(len(poset))]]
    while True:
        nxt = [c + (j,) for c in chains[-1] for j in range(len(poset)) if poset[j] < poset[c[-1]]]
        if not nxt:
            break
        chains.append(nxt)
    offsets = []
    cochain_dimensions = []
    for level in chains:
        off = {}
        total = 0
        for c in level:
            off[c] = total
            total += dimensions[c[-1]]
        offsets.append(off)
        cochain_dimensions.append(total)
    differential_ranks = []
    differentials = []
    for k in range(len(chains) - 1):
        rows = []
        for c in chains[k + 1]:
            target_dim = dimensions[c[-1]]
            for j in range(target_dim):
                row = {}
                for i in range(k + 1):
                    source_chain = c[:i] + c[i + 1:]
                    col = offsets[k][source_chain] + j
                    row[col] = (row.get(col, 0) + (-1) ** i) % p
                source_chain = c[:-1]
                inc = inclusions[c[-2], c[-1]]
                for z, value in enumerate(inc[j]):
                    col = offsets[k][source_chain] + z
                    row[col] = (row.get(col, 0) + (-1) ** (k + 1) * value) % p
                rows.append({col: value for col, value in row.items() if value})
        if k:
            prev = differentials[-1]
            for row in rows:
                composite = {}
                for j, value in row.items():
                    for col, v in prev[j].items():
                        composite[col] = (composite.get(col, 0) + value * v) % p
                if not not any(composite.values()):
                    raise RuntimeError('Check failed at accepted-source line 204')
        differentials.append(rows)
        rank = gf2_rank((sum((1 << col for col in row), 0) for row in rows)) if p == 2 else sparse_rank(rows, p)
        differential_ranks.append(rank)
    betti = [d - (differential_ranks[k - 1] if k else 0) - (differential_ranks[k] if k < len(differential_ranks) else 0) for k, d in enumerate(cochain_dimensions)]
    global_dimension = len(stalk(frozenset(range(len(normals))), normals, degree, p)[0])
    if not betti[0] == global_dimension:
        raise RuntimeError('Check failed at accepted-source line 212')

    def hd(a):
        return comb(a + n - 1, n - 1) if a >= 0 else 0
    expected_global = (1 if n == 3 else 2) * hd(degree - 1) + 3 * hd(degree - 2) - hd(degree - 3)
    if not global_dimension == expected_global:
        raise RuntimeError('Check failed at accepted-source line 216')
    expected = [global_dimension] + [0] * (len(betti) - 1)
    if n == 3 and degree == 0:
        expected[1] = 1
    if not betti == expected:
        raise RuntimeError((n, degree, p, betti, expected))
    return dict(variables=n, degree=degree, characteristic=p, flats=len(poset), strict_chain_counts=list(map(len, chains)), cochain_dimensions=cochain_dimensions, differential_ranks=differential_ranks, cohomology_dimensions=betti, global_module_dimension=global_dimension, differential_squared_zero=True, inclusion_reconstruction=True)
if __name__ == '__main__':
    results = []
    for p in (2, 3, 5, 7):
        for n in (3, 4):
            for d in range(4 if p == 2 else 2):
                result = run(n, d, p)
                results.append(result)
    print(json.dumps(dict(method='Independent full stalk kernels and normalized strict-chain cochains', passed=len(results), results=results), indent=2))
