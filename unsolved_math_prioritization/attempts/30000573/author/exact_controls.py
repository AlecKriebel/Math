#!/usr/bin/env python3
"""Finite diagnostic controls. These do not prove the infinite-dimensional claims."""
from fractions import Fraction as Q
from itertools import product
import json


def need(condition, label):
    if not condition:
        raise ValueError(label)


def rank(rows):
    a = [[Q(x) for x in row] for row in rows]
    if not a:
        return 0
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        p = a[r][col]
        a[r] = [x / p for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][col]:
                c = a[i][col]
                a[i] = [x - c * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def factor_equations(t, block_dim, length, boundary=True):
    d = len(t)
    variables = length * d * block_dim

    def ix(j, row, col):
        return (j * d + row) * block_dim + col

    equations = []
    for j in range(length + (1 if boundary else 0)):
        for row in range(d):
            for col in range(block_dim):
                eq = [Q(0)] * variables
                if j > 0:
                    eq[ix(j - 1, row, col)] += 1
                if j < length:
                    for a in range(d):
                        eq[ix(j, a, col)] -= t[row][a]
                equations.append(eq)
    return equations, variables


class Cyclotomic:
    """Exact Q[z]/(z^degree+1), with degree a power of two."""

    def __init__(self, degree):
        self.d = degree
        self.zero = (Q(0),) * degree
        self.one = (Q(1),) + (Q(0),) * (degree - 1)

    def monomial(self, exponent):
        q, r = divmod(exponent, self.d)
        out = list(self.zero)
        out[r] = Q(-1 if q % 2 else 1)
        return tuple(out)

    def add(self, a, b):
        return tuple(x + y for x, y in zip(a, b))

    def scale(self, a, c):
        return tuple(c * x for x in a)

    def sub(self, a, b):
        return self.add(a, self.scale(b, -1))

    def mul(self, a, b):
        out = list(self.zero)
        for i, x in enumerate(a):
            if not x:
                continue
            for j, y in enumerate(b):
                if y:
                    q, r = divmod(i + j, self.d)
                    out[r] += (-1 if q % 2 else 1) * x * y
        return tuple(out)

    def power(self, a, n):
        out = self.one
        while n:
            if n % 2:
                out = self.mul(out, a)
            a = self.mul(a, a)
            n //= 2
        return out

    def prod(self, seq):
        out = self.one
        for x in seq:
            out = self.mul(out, x)
        return out


def run():
    counts = {}
    blocks = [p for n in range(1, 4) for p in product((-1, 0, 1), repeat=n)]
    coding = 0
    for u in blocks:
        for v in blocks:
            for gap in range(3):
                start = len(u) + gap
                x = u + (0,) * gap + v
                need(x[:len(u)] == u and x[start:start+len(v)] == v, 'block coding')
                coding += 1
    counts['disjoint_block_coding'] = coding

    periodic = 0
    for length in range(1, 6):
        for word in product((-1, 0, 1), repeat=length):
            x = word * 7
            need(x[:6*length] == x[length:7*length], 'periodic block')
            periodic += 1
    counts['periodic_block_identities'] = periodic

    exponents = 0
    for r, n, m, k in product(range(15), range(1, 16), range(6), range(6)):
        telescoping = sum(2**j for j in range(r+1, r+n+1))
        need(telescoping == 2**(r+n+1)-2**(r+1), 'telescoping exponent')
        lhs = k*2**r + m*telescoping - (k+2*m+1)*2**(r+n)
        need(lhs <= -2**n, 'strong stability exponent bound')
        exponents += 1
    counts['strong_stability_exponent_cases'] = exponents

    decay = 0
    for c in range(11):
        for n in range(max(c+1, 4), 51):
            need(2**n >= n*n and c*n-2**n <= -n, 'decay bound')
            decay += 1
    counts['integer_decay_bounds'] = decay

    factors = 0
    for d, b, length in product(range(1, 4), range(1, 4), range(1, 5)):
        matrices = [
            [[Q(i == j) for j in range(d)] for i in range(d)],
            [[Q(2*(i == j)) for j in range(d)] for i in range(d)],
            [[Q(j == i+1) for j in range(d)] for i in range(d)],
            [[Q((i+2*j)%3-1) for j in range(d)] for i in range(d)],
        ]
        for t in matrices:
            eq, nv = factor_equations(t, b, length)
            need(rank(eq) == nv, 'full-boundary factor rank')
            factors += 1
    counts['full_boundary_intertwiner_rank_cases'] = factors
    eq, nv = factor_equations([[Q(0)]], 1, 3, boundary=False)
    need(rank(eq) < nv, 'missing-boundary negative diagnostic')
    counts['missing_boundary_detected'] = 1

    eigens = roots = lefts = 0
    for top in range(1, 5):
        degree = 2**(top+1)
        ring = Cyclotomic(degree)
        minus = ring.scale(ring.one, -1)
        lam = [minus] + [ring.monomial(2**(top-j)) for j in range(1, top+1)]
        weights = [Q(0)] + [Q(1, 2**(4**j)) for j in range(1, top+1)]
        for a in range(top+1):
            for b in range(a):
                need(lam[a] != lam[b], 'distinct roots')
        for n in range(top+1):
            period = 2 if n == 0 else 2**(n+2)
            need(ring.power(lam[n], period) == ring.one, 'root order divides period')
            roots += 1
            v = []
            for j in range(n+1):
                scalar = Q(1)
                for t in range(j+1, n+1):
                    scalar *= weights[t]
                diffs = [ring.sub(lam[n], lam[t]) for t in range(j)]
                v.append(ring.scale(ring.prod(diffs), scalar))
            need(v[-1] != ring.zero, 'nonzero triangular diagonal')
            for j in range(n+1):
                tx = ring.mul(lam[j], v[j])
                if j < n:
                    tx = ring.add(tx, ring.scale(v[j+1], weights[j+1]))
                need(tx == ring.mul(lam[n], v[j]), 'exact triangular eigenvector')
                eigens += 1
        # Denominator-cleared finite restrictions of the continuous eigenfunctional.
        c = []
        for j in range(top+1):
            scalar = Q(1)
            for t in range(1, j+1):
                scalar *= weights[t]
            diffs = [ring.sub(minus, lam[t]) for t in range(j+1, top+1)]
            c.append(ring.scale(ring.prod(diffs), scalar))
        need(c[0] != ring.zero, 'nonzero eigenfunctional normalization')
        for j in range(top+1):
            left = ring.mul(lam[j], c[j])
            if j:
                left = ring.add(left, ring.scale(c[j-1], weights[j]))
            need(left == ring.scale(c[j], -1), 'exact left eigenfunctional')
            lefts += 1
    counts['cyclotomic_eigenvector_coordinate_identities'] = eigens
    counts['cyclotomic_period_identities'] = roots
    counts['cyclotomic_left_eigenfunctional_identities'] = lefts
    return {
        'problem_id': 30000573,
        'status': 'PASS_FINITE_DIAGNOSTIC_CONTROLS',
        'scope': 'Finite exact arithmetic supplements PROOFS.md; no finite test proves the general Fréchet claims.',
        'arithmetic': 'Python standard library integer and Fraction arithmetic; cyclotomic quotient rings.',
        'counts': counts,
        'total_primary_cases': sum(counts.values()),
    }


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
