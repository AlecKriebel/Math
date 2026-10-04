#!/usr/bin/env python3
"""Independent finite audit: sparse row spaces versus symbolic restrictions.

No author verifier is imported or executed. This recreates its deterministic
sample list but builds sparse relations in a different monomial order, uses
incremental sparse elimination, and predicts every degree through an explicit
linear-coordinate restriction of the hypersurface. All arithmetic is exact.
These finite checks do not prove the all-N theorem or Zariski genericity.
"""
from fractions import Fraction
from itertools import product
from math import comb
import json
import random


def norm(a, p):
    return a % p if p else Fraction(a)


def inverse(a, p):
    return pow(a, -1, p) if p else 1 / a


def clean(row, p):
    return {j: norm(c, p) for j, c in row.items() if norm(c, p)}


def sparse_rank(rows, p):
    pivots = {}
    for raw in rows:
        row = clean(raw, p)
        while row:
            j = min(row)
            if j not in pivots:
                scale = inverse(row[j], p)
                pivots[j] = clean({i: c * scale for i, c in row.items()}, p)
                break
            c = row[j]
            base = pivots[j]
            row = clean({i: row.get(i, 0) - c * base.get(i, 0)
                         for i in row.keys() | base.keys()}, p)
    return len(pivots)


def mons(m):
    if m < 0:
        return []
    return [(m-b-c, b, c) for c in range(m, -1, -1)
            for b in range(m-c, -1, -1)]


def relations(N, m, pair):
    basis = mons(m)
    indices = {exp: i for i, exp in enumerate(basis)}
    rows = []
    for coefficients in pair:
        for exponent in mons(m-1):
            row = {}
            for variable in range(3):
                target = list(exponent)
                target[variable] += 1
                row[indices[tuple(target)]] = coefficients[variable]
            rows.append(row)
    for exponent in mons(m-N):
        first = (exponent[0]+N, exponent[1], exponent[2])
        second = (exponent[0], exponent[1]+N-1, exponent[2]+1)
        rows.append({indices[first]: 1, indices[second]: -1})
    return len(basis), rows


def linear_restrictions(pair, p):
    """Return images of x,y,z in the quotient by the two linear forms."""
    rows = [[norm(c, p) for c in row] for row in pair]
    pivot_columns = []
    for column in range(3):
        start = len(pivot_columns)
        found = next((i for i in range(start, 2) if rows[i][column]), None)
        if found is None:
            continue
        rows[start], rows[found] = rows[found], rows[start]
        scale = inverse(rows[start][column], p)
        rows[start] = [norm(c*scale, p) for c in rows[start]]
        for i in range(2):
            if i != start:
                c = rows[i][column]
                rows[i] = [norm(u-c*v, p) for u, v in zip(rows[i], rows[start])]
        pivot_columns.append(column)
        if len(pivot_columns) == 2:
            break
    free = [j for j in range(3) if j not in pivot_columns]
    s = len(free)
    units = [tuple(int(i == j) for i in range(s)) for j in range(s)]
    images = [None] * 3
    for i, variable in enumerate(free):
        images[variable] = {units[i]: norm(1, p)}
    for i, variable in enumerate(pivot_columns):
        images[variable] = {units[j]: norm(-rows[i][free[j]], p)
                            for j in range(s) if rows[i][free[j]]}
    return len(pivot_columns), s, images


def multiply(a, b, p):
    result = {}
    for e, c in a.items():
        for f, d in b.items():
            exponent = tuple(u+v for u, v in zip(e, f))
            result[exponent] = result.get(exponent, 0) + c*d
    return clean(result, p)


def power(a, n, s, p):
    result = {(0,)*s: norm(1, p)}
    for _ in range(n):
        result = multiply(result, a, p)
    return result


def restriction_is_nonzero(N, s, images, p):
    a = power(images[0], N, s, p)
    b = multiply(power(images[1], N-1, s, p), images[2], p)
    return bool(clean({e: a.get(e, 0)-b.get(e, 0) for e in a.keys() | b.keys()}, p))


def polynomial_hilbert(m, s):
    return 0 if m < 0 else comb(m+s-1, s-1)


def samples(p):
    if p == 2:
        return [(row[:3], row[3:]) for row in product(range(2), repeat=6)]
    result = [((0,1,0),(0,0,1)), ((1,0,0),(0,1,0)),
              ((1,0,0),(2,0,0)), ((0,0,0),(0,0,0)),
              ((1,2,3),(3,1,4)), ((1,1,0),(0,1,1))]
    rng = random.Random(1242+p)
    for _ in range(6 if p == 0 else 12):
        result.append(tuple(tuple(rng.randrange(-3,4) for _ in range(3))
                            for _ in range(2)))
    return result


def main():
    matrices = 0
    pair_N_cases = 0
    categories = {'generic_rank_two': 0, 'exceptional_rank_two': 0,
                  'rank_one': 0, 'rank_zero': 0}
    fields = []
    for p in (0,2,3,5,7):
        before = matrices
        Ns = list(range(2, 5 if p == 0 else 7))
        pairs = samples(p)
        for N in Ns:
            for pair in pairs:
                pair_N_cases += 1
                r, s, images = linear_restrictions(pair, p)
                assert r == sparse_rank([dict(enumerate(row)) for row in pair], p)
                nonzero = restriction_is_nonzero(N, s, images, p)
                if r == 2:
                    key = 'generic_rank_two' if nonzero else 'exceptional_rank_two'
                else:
                    key = 'rank_one' if r == 1 else 'rank_zero'
                categories[key] += 1
                for m in range(N+2):
                    width, rows = relations(N, m, pair)
                    actual = width-sparse_rank(rows, p)
                    expected = polynomial_hilbert(m, s)
                    if nonzero:
                        expected -= polynomial_hilbert(m-N, s)
                    assert actual == expected, (p, N, m, pair, actual, expected)
                    if m < N:
                        assert actual > 0
                    if r == 2 and nonzero:
                        assert actual == int(m < N)
                    matrices += 1
        fields.append({'characteristic': p, 'N_values': Ns,
                       'pairs_per_N': len(pairs), 'degree_matrices': matrices-before})
    assert matrices == 3720
    assert pair_N_cases == 626
    assert categories['generic_rank_two'] == 324
    assert categories['exceptional_rank_two'] == 136
    assert categories['rank_one'] + categories['rank_zero'] == 166
    result = {'problem_id': 30001242, 'result': 'PASS',
              'degree_matrices': matrices, 'pair_N_cases': pair_N_cases,
              'categories': categories, 'fields': fields,
              'method': 'Independent sparse elimination checked against explicit symbolic restriction of F_N to S/(l_1,l_2).',
              'scope': 'Exact finite controls only; no genericity or all-N theorem is inferred from the computation.'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
