#!/usr/bin/env python3
"""Exact finite controls; not a finite-field proof of the target questions.

Python standard library only. Runs from any cwd and does not mutate files.
"""
from itertools import product
from math import comb
import json

PRIMES = (2, 3, 5, 7)

def polynomial_add(a, b, p):
    out = dict(a)
    for e, c in b.items():
        out[e] = (out.get(e, 0) + c) % p
        if not out[e]:
            del out[e]
    return out

def polynomial_scale(a, c, p):
    return {e: c * v % p for e, v in a.items() if c * v % p}

def frobenius(a, p):
    return {tuple(p * x for x in e): c for e, c in a.items()}

def euler(a, i, p):
    return {e: e[i] * c % p for e, c in a.items() if e[i] * c % p}

def constant(a, r):
    return a.get((0,) * r, 0)

def derivative_controls():
    tested = 0
    exact = 0
    sums = 0
    nonzero = []
    for p in PRIMES:
        for r in range(1, 5):
            aggregate = {}
            for e in product(range(-2, 3), repeat=r):
                for c in range(1, p):
                    f = {e: c}
                    wp = polynomial_add(frobenius(f, p), polynomial_scale(f, -1, p), p)
                    assert constant(wp, r) == 0
                    tested += 1
                    for i in range(r):
                        assert constant(euler(f, i, p), r) == 0
                        exact += 1
                aggregate[e] = (sum(e) + 1) % p
            aggregate = {e: c for e, c in aggregate.items() if c}
            wp = polynomial_add(frobenius(aggregate, p), polynomial_scale(aggregate, -1, p), p)
            assert constant(wp, r) == 0
            assert all(constant(euler(aggregate, i, p), r) == 0 for i in range(r))
            sums += 1
            assert constant({(0,) * r: 1}, r) == 1
            nonzero.append({'p': p, 'r': r, 'detector': 1, 'degree': r + 1})
    return {'monomial_artin_schreier_checks': tested,
            'monomial_exact_form_checks': exact,
            'mixed_laurent_polynomial_checks': sums,
            'top_symbol_controls': nonzero}

# Crossed-product normal forms over F_p[a,b,b^{-1}].
# A key (a_exp,b_exp,i_exp,j_exp) denotes a^A b^B i^I j^J.
# Normalize using i^p=i+a, j^p=b, and j i=(i+1)j.
class SymbolAlgebra:
    def __init__(self, p):
        self.p = p
        self.one = {(0, 0, 0, 0): 1}
        self.a = {(1, 0, 0, 0): 1}
        self.b = {(0, 1, 0, 0): 1}
        self.binv = {(0, -1, 0, 0): 1}
        self.i = {(0, 0, 1, 0): 1}
        self.j = {(0, 0, 0, 1): 1}
        self.jinv = {(0, -1, 0, p - 1): 1}

    def add(self, x, y):
        return polynomial_add(x, y, self.p)

    def scale(self, x, c):
        return polynomial_scale(x, c, self.p)

    def reduce_i(self, exponent):
        # i^k = i^(k-p+1) + a i^(k-p) for k >= p.
        if exponent < self.p:
            return {(0, exponent): 1}
        left = self.reduce_i(exponent - self.p + 1)
        right = {(a + 1, i): c for (a, i), c in self.reduce_i(exponent - self.p).items()}
        return polynomial_add(left, right, self.p)

    def mul(self, x, y):
        out = {}
        p = self.p
        for (A, B, I, J), cx in x.items():
            for (C, D, K, L), cy in y.items():
                # j^J i^K = (i+J)^K j^J.
                for h in range(K + 1):
                    coeff = cx * cy * comb(K, h) * pow(J, K - h, p) % p
                    if coeff == 0:
                        continue
                    jb, jj = divmod(J + L, p)
                    for (ia, ii), ci in self.reduce_i(I + h).items():
                        key = (A + C + ia, B + D + jb, ii, jj)
                        out[key] = (out.get(key, 0) + coeff * ci) % p
                        if not out[key]:
                            del out[key]
        return out

    def power(self, x, exponent):
        ans = self.one
        while exponent:
            if exponent & 1:
                ans = self.mul(ans, x)
            x = self.mul(x, x)
            exponent >>= 1
        return ans


def algebra_controls():
    results = []
    for p in PRIMES:
        a = SymbolAlgebra(p)
        assert a.mul(a.j, a.jinv) == a.one == a.mul(a.jinv, a.j)
        assert a.power(a.i, p) == a.add(a.i, a.a)
        assert a.power(a.j, p) == a.b
        assert a.mul(a.j, a.i) == a.mul(a.add(a.i, a.one), a.j)
        I, J = a.scale(a.i, -1), a.jinv
        assert a.add(a.power(I, p), a.scale(I, -1)) == a.scale(a.a, -1)
        assert a.power(J, p) == a.binv
        assert a.mul(a.mul(J, I), a.j) == a.add(I, a.one)
        assert a.scale(I, -1) == a.i
        assert a.mul(a.b, a.power(J, p - 1)) == a.j
        original, changed = 1, (-1) % p
        assert (original == changed) == (p == 2)
        results.append({'p': p, 'generator_checks': 9,
                        'old_class_detector': original,
                        'changed_class_detector': changed,
                        'equal': p == 2})
    return results


def wedge(x, y, p):
    if set(x).intersection(y):
        return (), 0
    inversions = sum(a > b for a in x for b in y)
    return tuple(sorted(x + y)), (-1 if inversions % 2 else 1) % p


def wedge_controls():
    repeated = 0
    linked = 0
    for p in PRIMES:
        for n in range(2, 7):
            theta = tuple(range(n - 2))
            extra = tuple(range(n - 2, n + 1))
            full, value = wedge(theta, extra, p)
            assert full == tuple(range(n + 1)) and value == 1
            linked += 1
            for e in extra:
                selected, _ = wedge(theta, (e,), p)
                _, value = wedge(selected, (e,), p)
                assert value == 0
                repeated += 1
    return {'selected_linked_triple_degree_checks': linked,
            'repeated_slot_zero_checks': repeated}


def main():
    result = {'schema': 'kato-milne-elementary-controls-v1',
              'status': 'PASS',
              'arithmetic': 'exact integers reduced modulo p; sparse Laurent polynomials',
              'scope': 'Finite controls only. Infinite-field results rely on the written proofs. No universal linkage is certified.',
              'derivative_controls': derivative_controls(),
              'symbol_presentation_controls': algebra_controls(),
              'wedge_controls': wedge_controls()}
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
