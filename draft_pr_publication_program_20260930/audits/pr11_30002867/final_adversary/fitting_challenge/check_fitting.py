"""Exact, dependency-free adversarial examples for the matrix Fitting criterion.

Run: python3 check_fitting.py
All computations use rational arithmetic, including kernel bases and minors.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations
import json


def rank_and_kernel(columns, n):
    width = len(columns)
    a = [[Q(columns[j][i]) for j in range(width)] for i in range(n)]
    pivots = []
    row = 0
    for col in range(width):
        p = next((i for i in range(row, n) if a[i][col]), None)
        if p is None:
            continue
        a[row], a[p] = a[p], a[row]
        scalar = a[row][col]
        a[row] = [x / scalar for x in a[row]]
        for i in range(n):
            if i != row and a[i][col]:
                scalar = a[i][col]
                a[i] = [x - scalar * y for x, y in zip(a[i], a[row])]
        pivots.append(col)
        row += 1
        if row == n:
            break
    basis = []
    for free in (j for j in range(width) if j not in pivots):
        v = [Q(0)] * width
        v[free] = Q(1)
        for i, col in enumerate(pivots):
            v[col] = -a[i][free]
        basis.append(v)
    return len(pivots), basis


class Algebra:
    def __init__(self, names, unit, products):
        self.names = names
        self.n = len(names)
        self.unit = [Q(x) for x in unit]
        self.products = products

    def basis(self, j):
        return [Q(i == j) for i in range(self.n)]

    def mul(self, a, b):
        out = [Q(0)] * self.n
        for i in range(self.n):
            for j in range(self.n):
                if a[i] and b[j]:
                    for k, val in self.products.get((i, j), {}).items():
                        out[k] += a[i] * b[j] * val
        return out

    def regular_matrix(self, a):
        cols = [self.mul(a, self.basis(j)) for j in range(self.n)]
        return [[cols[j][i] for j in range(self.n)] for i in range(self.n)]

    def recovered_generation_degree(self, coords):
        """Recover B by matrix products after a common shear of the basis.

        This uses no vector in the regular module and no distinguished unit
        vector; the identity matrix is the algebra's identity element.
        """
        n = self.n
        ident = [[Q(i == j) for j in range(n)] for i in range(n)]
        p = [row[:] for row in ident]
        pinv = [row[:] for row in ident]
        if n > 1:
            p[0][1], pinv[0][1] = Q(1), Q(-1)

        def mm(a, b):
            return [[sum(a[i][k]*b[k][j] for k in range(n))
                     for j in range(n)] for i in range(n)]

        mats = [mm(mm(p, self.regular_matrix(x)), pinv) for x in coords]
        basis = [ident]
        degree = 0
        for degree in range(1, n):
            old = basis[:]
            for a in old:
                for x in mats:
                    value = mm(x, a)
                    rank, _ = rank_and_kernel([sum(b, []) for b in basis] + [sum(value, [])], n*n)
                    if rank > len(basis):
                        basis.append(value)
            if len(basis) == n:
                break
        assert len(basis) == n, (self.names, len(basis), n)
        return 0 if n == 1 else degree

    def relation_columns(self, coords, support):
        shifted = [[a - Q(lam) * b for a, b in zip(x, self.unit)]
                   for x, lam in zip(coords, support)]
        columns = [self.mul(x, self.basis(j))
                   for x in shifted for j in range(self.n)]
        rank, kernel = rank_and_kernel(columns, self.n)
        return rank, [[v[i*self.n:(i+1)*self.n] for i in range(len(coords))]
                      for v in kernel]

    def det(self, entries):
        d = len(entries)
        ans = [Q(0)] * self.n
        for p in permutations(range(d)):
            inversions = sum(p[i] > p[j] for i in range(d) for j in range(i+1, d))
            value = self.unit
            for i in range(d):
                value = self.mul(value, entries[i][p[i]])
            ans = [a + (-1)**inversions * b for a, b in zip(ans, value)]
        return ans

    def test(self, name, coords, support, expected):
        rank, cols = self.relation_columns(coords, support)
        d = len(coords)
        nonzero = []
        for chosen in combinations(range(len(cols)), d):
            value = self.det([[cols[j][i] for j in chosen] for i in range(d)])
            if any(value):
                nonzero.append((chosen, value))
        observed = bool(nonzero)
        assert observed == expected, (name, observed, expected)
        return {"case": name, "support": support, "N": self.n, "d": d,
                "generation_degree_after_common_shear": self.recovered_generation_degree(coords),
                "horizontal_rank": rank, "C_kernel_dimension": len(cols),
                "minor_count": len(list(combinations(range(len(cols)), d))),
                "nonzero_minor_count": len(nonzero), "expected_CI": expected,
                "observed_CI": observed,
                "first_nonzero_minor": None if not nonzero else
                  {"columns": nonzero[0][0], "coefficients": [str(v) for v in nonzero[0][1]],
                   "basis": self.names}}


def monomial_algebra(exponents):
    n = len(exponents)
    lookup = {a: i for i, a in enumerate(exponents)}
    products = {}
    for i, a in enumerate(exponents):
        for j, b in enumerate(exponents):
            c = tuple(x + y for x, y in zip(a, b))
            if c in lookup:
                products[i, j] = {lookup[c]: Q(1)}
    return Algebra([str(a) for a in exponents], [1] + [0]*(n-1), products)


results = []
zero_variables = monomial_algebra([()])
results.append(zero_variables.test("d=0: empty determinant is one", [], [], True))
field = monomial_algebra([(0, 0)])
results.append(field.test("reduced singleton with two zero generators", [[0], [0]], [0, 0], True))
dual = monomial_algebra([(0,), (1,)])
results.append(dual.test("dual numbers: algebra determinant is nonzero nilpotent", [[0, 1]], [0], True))
triple = monomial_algebra([(0,), (1,), (2,)])
results.append(triple.test("redundant generators t and t^2", [[0, 1, 0], [0, 0, 1]], [0, 0], True))
ci = monomial_algebra([(0, 0), (1, 0), (0, 1), (1, 1)])
results.append(ci.test("C[x,y]/(x^2,y^2)", [[0, 1, 0, 0], [0, 0, 1, 0]], [0, 0], True))
bad = monomial_algebra([(0, 0), (1, 0), (0, 1)])
results.append(bad.test("C[x,y]/(x,y)^2", [[0, 1, 0], [0, 0, 1]], [0, 0], False))

# A = C[x,y]/(x,y)^2 times C; supports (0,0) and (1,0).
products = dict(bad.products)
products[3, 3] = {3: Q(1)}
mixed = Algebra(["e0", "x0", "y0", "e1"], [1, 0, 0, 1], products)
coords = [[0, 1, 0, 1], [0, 0, 1, 0]]
results.append(mixed.test("mixed supports, selected non-CI factor", coords, [0, 0], False))
results.append(mixed.test("mixed supports, selected reduced field factor", coords, [1, 0], True))

# Gorenstein, but not CI: x^2=y^2=xz=yz=0 and z^2=xy.
products = {}
for i in range(5):
    products[0, i] = products[i, 0] = {i: Q(1)}
products[1, 2] = products[2, 1] = products[3, 3] = {4: Q(1)}
gor = Algebra(["1", "x", "y", "z", "xy=z^2"], [1, 0, 0, 0, 0], products)
results.append(gor.test("Gorenstein non-CI with embedding dimension three",
                        [[0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0]],
                        [0, 0, 0], False))

print(json.dumps(results, indent=2))
