#!/usr/bin/env python3
"""Exact, bounded controls. No network, external packages, or source corpus required."""
import argparse
from collections import Counter, defaultdict
from itertools import combinations, product
import json
from pathlib import Path


def monomials(n, d):
    if n == 1:
        return [(d,)]
    return [(i,) + q for i in range(d + 1) for q in monomials(n - 1, d - i)]


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def divides(a, b):
    return all(x <= y for x, y in zip(a, b))


def rank(rows, p, n=None):
    a = [[x % p for x in row] for row in rows]
    if not a:
        return 0
    n = len(a[0]) if n is None else n
    k = 0
    for j in range(n):
        pivot = next((i for i in range(k, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        inv = pow(a[k][j], -1, p)
        a[k] = [(x * inv) % p for x in a[k]]
        for i in range(len(a)):
            if i != k and a[i][j]:
                c = a[i][j]
                a[i] = [(x - c * y) % p for x, y in zip(a[i], a[k])]
        k += 1
        if k == len(a):
            break
    return k


def subspaces(n, r, p):
    """One unique RREF matrix for every r-dimensional subspace of F_p^n."""
    for pivots in combinations(range(n), r):
        free = [(i, j) for i, pi in enumerate(pivots)
                for j in range(pi + 1, n) if j not in pivots]
        for values in product(range(p), repeat=len(free)):
            rows = [[0] * n for _ in range(r)]
            for i, pi in enumerate(pivots):
                rows[i][pi] = 1
            for (i, j), value in zip(free, values):
                rows[i][j] = value
            yield rows


def gaussian(n, r, q):
    if r < 0 or r > n:
        return 0
    num = den = 1
    for i in range(r):
        num *= q ** (n - i) - 1
        den *= q ** (r - i) - 1
    return num // den


def projective(n, p):
    for first in range(n):
        for tail in product(range(p), repeat=n - first - 1):
            yield (0,) * first + (1,) + tail


def degree_two_check(weights, r, s, p):
    n = len(weights)
    linear = [tuple(int(i == j) for i in range(n))
              for j in range(n) if weights[j] == 1]
    second = [tuple(int(i == j) for i in range(n))
              for j in range(n) if weights[j] == 2]
    second += [m for m in monomials(n, 2)
               if sum(i * w for i, w in zip(m, weights)) == 2]
    idx = {m: i for i, m in enumerate(second)}
    m, N = len(linear), len(second)
    total = 0
    fibers = []
    for kernel1 in subspaces(m, m - r, p):
        multiples = []
        for v in linear:
            for row in kernel1:
                out = [0] * N
                for a, coefficient in zip(linear, row):
                    out[idx[add(a, v)]] = coefficient
                multiples.append(out)
        assert rank(multiples, p) == N - (weights.count(2) + r * (r + 1) // 2)
        count = 0
        for kernel2 in subspaces(N, N - s, p):
            if rank(kernel2 + multiples, p) == N - s:
                count += 1
        fibers.append(count)
        total += count
    E = weights.count(2) + r * (r + 1) // 2
    expected = gaussian(m, r, p) * gaussian(E, s, p)
    assert total == expected
    assert set(fibers) == {gaussian(E, s, p)}
    return dict(weights=weights, h=[1, r, s], prime=p, enumerated=total,
                grassmann_formula=expected, uniform_fiber_count=fibers[0])


def cubic_controls():
    quad = monomials(3, 2)
    cubic = monomials(3, 3)
    index = {m: i for i, m in enumerate(cubic)}
    units = monomials(3, 1)
    result = []
    all_binary = []
    for p in (2, 3):
        counts = Counter()
        for F in projective(len(cubic), p):
            rows = [[F[index[add(v, q)]] for q in quad] for v in units]
            ell = rank(rows, p)
            assert ell >= 1  # multiplication spans all cubics, including in small char
            counts[ell] += 1
            if p == 2:
                all_binary.append(tuple(sum(x << j for j, x in enumerate(row)) for row in rows))
        expected1 = gaussian(3, 1, p)
        expected2 = gaussian(3, 2, p) * ((p**4 - 1)//(p - 1) - (p + 1))
        assert counts[1] == expected1
        assert counts[2] == expected2
        assert sum(counts.values()) == (p**10 - 1)//(p - 1)
        totals = {s: sum(count * gaussian(6 - ell, s - ell, p)
                          for ell, count in counts.items() if ell <= s)
                  for s in range(1, 7)}
        result.append(dict(prime=p, projective_cubics=sum(counts.values()),
                           contraction_rank_counts=dict(sorted(counts.items())),
                           incidence_counts=totals))
    # Direct independent incidence enumeration for h=(1,3,2,1), F_2.
    direct = 0
    for U in subspaces(6, 2, 2):
        a, b = [sum(x << j for j, x in enumerate(row)) for row in U]
        span = {0, a, b, a ^ b}
        direct += sum(all(row in span for row in rows) for rows in all_binary)
    assert direct == result[0]['incidence_counts'][2] == 301
    result[0]['direct_quadratic_subspace_enumeration_h1321'] = direct
    return result


def finer_degree(m):
    x, y, z = m
    return (x + y, y + z)


def haiman_controls():
    forced = [(3,0,0),(1,2,0),(2,1,0),(0,3,0),(0,2,1),(0,0,2)]
    bounds = (3, 3, 2)
    basis = list(product(*(range(x) for x in bounds)))
    groups = defaultdict(list)
    for m in basis:
        groups[finer_degree(m)].append(m)
    target = {(0,0):1,(1,0):1,(0,1):1,(2,0):1,(1,1):2,
              (2,1):1,(1,2):1,(2,2):1}
    result = []
    for p in (2, 3, 5):
        good = bad = 0
        boundaries = []
        for a in projective(2, p):
            for b in projective(2, p):
                relations = [[(m, 1)] for m in forced]
                relations += [[((2,0,1),a[0]),((1,1,0),-a[1])],
                              [((1,1,1),b[0]),((0,2,0),-b[1])]]
                rows_by_degree = defaultdict(list)
                for rel in relations:
                    for mult in basis:
                        terms = [(add(m, mult), c % p) for m, c in rel if c % p]
                        if not terms:
                            continue
                        d = finer_degree(terms[0][0])
                        if d not in groups:
                            continue
                        lookup = {m:i for i,m in enumerate(groups[d])}
                        row = [0] * len(lookup)
                        for m, c in terms:
                            if m in lookup:
                                row[lookup[m]] = (row[lookup[m]] + c) % p
                        rows_by_degree[d].append(row)
                computed = {d:len(ms)-rank(rows_by_degree[d],p)
                            for d,ms in groups.items()}
                correct = all(computed[d] == target.get(d,0) for d in computed)
                equation = a[1]*b[1] % p == 0
                assert correct == equation
                if correct:
                    good += 1
                    if all(sum(c % p != 0 for _, c in rel) == 1 for rel in relations):
                        boundaries.append([a,b])
                else:
                    bad += 1
        assert good == 2*p + 1
        assert len(boundaries) == 3
        result.append(dict(prime=p, valid_parameter_points=good,
                           excluded_parameter_points=bad,
                           checked_multidegrees=len(groups),
                           monomial_boundary_points=boundaries))
    return result


def minimal_generators(gens):
    gens = sorted(set(gens))
    return [a for a in gens if not any(b != a and divides(b,a) for b in gens)]


def intersection(gens1, gens2):
    return minimal_generators(tuple(max(x,y) for x,y in zip(a,b))
                              for a in gens1 for b in gens2)


def bidegree_count(gens, u, v, nx=3):
    return sum(not any(divides(g,m) for g in gens)
               for X in monomials(nx,u) for Y in monomials(2,v)
               for m in [X+Y])


def cid_ruiz_controls():
    result = []
    for a in range(2,6):
        I1=[(1,0,0,0,0),(0,a,0,2*a,0)]
        I2=[(2*a,0,0,0,0),(1,0,0,1,0),(0,a,0,1,0)]
        J=[(1,0,0,0,0),(0,a,0,0,0)]
        K=[(2*a,0,0,0,0),(0,0,0,1,0)]
        assert intersection(J,K) == minimal_generators(I2)
        stable=[]
        for u in range(2*a,2*a+4):
            for v in range(2*a,2*a+4):
                values=[bidegree_count(I,u,v) for I in (I1,I2)]
                polynomial=2*a*u+a*v+3*a-2*a*a
                assert values == [polynomial,polynomial]
                stable.append([u,v,polynomial])
        low=[bidegree_count(I,1,0) for I in (I1,I2)]
        assert low == [2,3]
        # Both x_2 and y_1 are absent from the generators; dehomogenize them.
        dehom=[[tuple(g[i] for i in (0,1,3)) for g in I] for I in (I1,I2)]
        degree10=[sum(not any(divides(g,m) for g in I)
                      for m in [(1,0,0),(0,1,0)]) for I in dehom]
        assert degree10 == [1,2]
        result.append(dict(a=a, intersection_verified=True, stable_rectangle=stable,
                           original_h10=low, dehomogenized_h10=degree10))
    return result


def multiplication_rank_control():
    units=monomials(3,1)
    examples=[[(2,0,0),(0,2,0),(0,0,2)],[(2,0,0),(1,1,0),(1,0,1)]]
    counts=[len({add(m,v) for m in gens for v in units}) for gens in examples]
    assert counts == [9,6]
    return dict(quadratic_kernel_dimensions=[3,3], cubic_product_dimensions=counts,
                cubic_quotient_dimensions=[10-c for c in counts])


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    # Cross-check RREF enumeration before using it in the controls.
    for p in (2,3):
        for n in range(1,5):
            for r in range(n+1):
                assert sum(1 for _ in subspaces(n,r,p)) == gaussian(n,r,p)
    result={
        'status':'PASS',
        'arithmetic':'integer and prime finite-field arithmetic; no floating point',
        'scope':'bounded exact controls; not an exhaustive connectedness search',
        'weight_two':[
            degree_two_check([1,1,1],2,2,2),
            degree_two_check([1,1,2],1,1,2),
            degree_two_check([1,1,2],1,2,2),
            degree_two_check([1,1,2],2,2,2),
            degree_two_check([1,1,2],1,1,3)],
        'cubic_contraction':cubic_controls(),
        'haiman_sturmfels':haiman_controls(),
        'cid_ruiz':cid_ruiz_controls(),
        'rank_jump':multiplication_rank_control(),
    }
    encoded=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded,end='')


if __name__=='__main__':
    main()
