#!/usr/bin/env python3
"""Exact finite certificate checks; Python 3 standard library only.

This checks a supplied rational basis, not positive definiteness of an arbitrary
input form and not the universal existence theorem. See the paper for that proof.
Input monomials are ordinary coefficients; tensor entries divide by multinomials.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial
from pathlib import Path
import argparse
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def compositions(n, m):
    if m == 1:
        yield (n,)
    else:
        for k in range(n + 1):
            for tail in compositions(n - k, m - 1):
                yield (k,) + tail


def multinomial(alpha):
    value = factorial(sum(alpha))
    for k in alpha:
        value //= factorial(k)
    return value


def mul(p, q):
    out = {}
    for a, c in p.items():
        for b, e in q.items():
            key = tuple(x + y for x, y in zip(a, b))
            out[key] = out.get(key, F(0)) + c * e
    return {a: c for a, c in out.items() if c}


def power(p, n, m):
    out = {(0,) * m: F(1)}
    for _ in range(n):
        out = mul(out, p)
    return out


def determinant(matrix):
    a = [list(row) for row in matrix]
    det = F(1)
    for k in range(len(a)):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            a[pivot], a[k] = a[k], a[pivot]
            det = -det
        q = a[k][k]
        det *= q
        for i in range(k + 1, len(a)):
            scale = a[i][k] / q
            for j in range(k + 1, len(a)):
                a[i][j] -= scale * a[k][j]
    return det


def evaluate(p, x):
    return sum(c * prod(xi ** ai for xi, ai in zip(x, a))
               for a, c in p.items())


def prod(items):
    out = F(1)
    for item in items:
        out *= item
    return out


def polarization(p, vectors):
    """Independent inclusion-exclusion polarization, exponential in degree."""
    d, m = len(vectors), len(vectors[0])
    total = F(0)
    for mask in product((0, 1), repeat=d):
        point = [sum(mask[i] * vectors[i][j] for i in range(d))
                 for j in range(m)]
        total += (-1) ** (d - sum(mask)) * evaluate(p, point)
    return total / factorial(d)


def check_certificate(data, cross_check=True):
    m, d = data['dimension'], data['degree']
    require(type(m) is int and m >= 1, 'dimension must be positive')
    require(type(d) is int and d >= 2 and d % 2 == 0, 'degree must be positive even')
    p = {}
    for term in data['monomials']:
        a = tuple(term['powers'])
        require(len(a) == m and all(type(i) is int and i >= 0 for i in a)
                and sum(a) == d, 'invalid monomial')
        c = F(str(term['coefficient']))
        p[a] = p.get(a, F(0)) + c
    matrix = [[F(str(c)) for c in row] for row in data['basis_rows']]
    require(len(matrix) == m and all(len(row) == m for row in matrix), 'invalid matrix')
    det = determinant(matrix)
    require(det != 0, 'singular basis')
    units = [tuple(int(i == j) for i in range(m)) for j in range(m)]
    linear = [{units[j]: matrix[i][j] for j in range(m) if matrix[i][j]}
              for i in range(m)]
    transformed = {}
    for alpha, c in p.items():
        term = {(0,) * m: c}
        for i, k in enumerate(alpha):
            term = mul(term, power(linear[i], k, m))
        for a, b in term.items():
            transformed[a] = transformed.get(a, F(0)) + b
    diagonal = [transformed.get(tuple(d * x for x in u), F(0)) for u in units]
    require(all(x > 0 for x in diagonal), 'nonpositive diagonal')
    checked = mixed = cross = 0
    min_gap = None
    for alpha in compositions(d, m):
        a = transformed.get(alpha, F(0)) / multinomial(alpha)
        gap = prod(diagonal[i] ** alpha[i] for i in range(m)) - a ** d
        pure = max(alpha) == d
        require(a > 0, 'coefficient is not strictly positive')
        require(gap == 0 if pure else gap > 0, 'coefficient inequality failed')
        if not pure:
            mixed += 1
            min_gap = gap if min_gap is None else min(min_gap, gap)
        if cross_check and d <= 6:
            vectors = [[matrix[j][i] for j in range(m)]
                       for i in range(m) for _ in range(alpha[i])]
            require(polarization(p, vectors) == a, 'polarization cross-check failed')
            cross += 1
        checked += 1
    return {'name': data.get('name', 'unnamed'), 'determinant': str(det),
            'coefficient_classes': checked, 'strict_mixed_classes': mixed,
            'polarization_cross_checks': cross,
            'smallest_power_gap': str(min_gap) if min_gap is not None else None}


def formal_quadratic_identity(d):
    """Coefficient-by-coefficient identity in independent symmetric Q_rs symbols.

    prod p(y_r) - A(y_1,...,y_d)^d has epsilon^2 coefficient
    d(d-1)/2 sum Q_rr - d sum_{r<s} Q_rs
    = d/2 sum_{r<s}(Q_rr+Q_ss-2 Q_rs), for tangent directions.
    """
    left = {(r, r): F(d * (d - 1), 2) for r in range(d)}
    right = {}
    for r, s in combinations(range(d), 2):
        left[r, s] = F(-d)
        for key, value in (((r, r), F(d, 2)), ((s, s), F(d, 2)), ((r, s), F(-d))):
            right[key] = right.get(key, F(0)) + value
    require(left == right, 'quadratic symbolic identity failed')


def demos():
    # p = ||x||^d + sum_{i<m} x_i^d >= ||x||^d > 0 away from 0.
    # v=e_m is a sphere minimizer, columns are v+(1/8)e_i and v.
    for m, d in ((1, 2), (1, 8), (2, 2), (3, 2), (2, 4),
                 (3, 4), (4, 4), (2, 6), (3, 6), (2, 8)):
        p = {tuple(2 * k for k in a): F(multinomial(a))
             for a in compositions(d // 2, m)}
        for i in range(m - 1):
            a = tuple(d if j == i else 0 for j in range(m))
            p[a] = p.get(a, F(0)) + 1
        basis = [[F(1, 8) if i == j else F(0) for j in range(m)] for i in range(m)]
        basis[-1] = [F(1)] * m
        yield {'name': f'radial-plus-transverse-m{m}-d{d}', 'dimension': m, 'degree': d,
               'monomials': [{'powers': a, 'coefficient': str(c)} for a, c in p.items()],
               'basis_rows': [[str(c) for c in row] for row in basis]}
    # Nonconvex positive form: (x^2-y^2)^2+x^2*y^2.
    yield {'name': 'nonconvex-quartic', 'dimension': 2, 'degree': 4,
           'monomials': [{'powers': [4, 0], 'coefficient': '1'},
                         {'powers': [2, 2], 'coefficient': '-1'},
                         {'powers': [0, 4], 'coefficient': '1'}],
           'basis_rows': [['5/4', '1'], ['3/4', '1']]}
    # Positive form violating the desired bound in the original coordinates.
    yield {'name': 'quartic-needing-change', 'dimension': 2, 'degree': 4,
           'monomials': [{'powers': [4, 0], 'coefficient': '1'},
                         {'powers': [2, 2], 'coefficient': '12'},
                         {'powers': [0, 4], 'coefficient': '1'}],
           'basis_rows': [['1', '1'], ['1/8', '0']]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, help='check one JSON certificate')
    parser.add_argument('--write-examples', type=Path, help='write built-in rational examples')
    args = parser.parse_args()
    if args.input:
        result = check_certificate(json.loads(args.input.read_text()))
        print(json.dumps({'status': 'PASS', 'certificate': result}, indent=2))
        return
    certificates = list(demos())
    results = [check_certificate(c) for c in certificates]
    for d in range(2, 25):
        formal_quadratic_identity(d)
    # Falsification controls: original bad basis and a singular replacement.
    for bad_basis, expected in (([['1', '0'], ['0', '1']], 'coefficient inequality failed'),
                                ([['1', '1'], ['0', '0']], 'singular basis')):
        bad = dict(certificates[-1], basis_rows=bad_basis)
        bad['monomials'] = list(bad['monomials']) + [
            {'powers': [3, 1], 'coefficient': '1'},
            {'powers': [1, 3], 'coefficient': '1'}]
        try:
            check_certificate(bad)
        except ValueError as exc:
            require(str(exc) == expected, f'unexpected rejection: {exc}')
        else:
            raise ValueError('negative control was accepted')
    # A fixed-coordinate violation: tensor A1122=12/6=2 > (1*1*1*1)^(1/4).
    require(F(12, multinomial((2, 2))) == 2, 'coefficient convention control failed')
    if args.write_examples:
        args.write_examples.mkdir(parents=True, exist_ok=True)
        for c in certificates:
            (args.write_examples / (c['name'] + '.json')).write_text(json.dumps(c, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'scope': 'finite exact checks, not a formal proof',
                      'formal_identity_degrees': [2, 24], 'negative_controls': 2,
                      'certificates': results,
                      'total_coefficient_classes': sum(r['coefficient_classes'] for r in results),
                      'total_polarization_cross_checks': sum(r['polarization_cross_checks'] for r in results)}, indent=2))


if __name__ == '__main__':
    main()
