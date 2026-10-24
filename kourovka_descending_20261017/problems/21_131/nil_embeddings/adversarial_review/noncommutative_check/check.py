#!/usr/bin/env python3
"""Finite noncommutative stress checks, independent of external theorem input.

The coefficient ring is F_p<x,y> / (all words of length 5). These checks do
not prove the general statements; the general algebraic verification is in
REPORT.md. All comparisons are exact, without numerical approximations.
"""

from itertools import permutations


class CheckRing:
    def __init__(self, p, cutoff=5):
        self.p = p
        self.cutoff = cutoff
        self.zero = {}
        self.one = {(): 1}
        self.x = {("x",): 1}
        self.y = {("y",): 1}

    def add(self, a, b):
        out = a.copy()
        for word, coefficient in b.items():
            value = (out.get(word, 0) + coefficient) % self.p
            if value:
                out[word] = value
            else:
                out.pop(word, None)
        return out

    def neg(self, a):
        return {word: (-coefficient) % self.p for word, coefficient in a.items()}

    def mul(self, a, b):
        out = {}
        for w1, c1 in a.items():
            for w2, c2 in b.items():
                word = w1 + w2
                if len(word) < self.cutoff:
                    value = (out.get(word, 0) + c1 * c2) % self.p
                    if value:
                        out[word] = value
                    else:
                        out.pop(word, None)
        return out

    def inverse_one_plus(self, w):
        assert () not in w
        out, term = self.one, self.one
        for _ in range(1, self.cutoff):
            term = self.neg(self.mul(term, w))
            out = self.add(out, term)
        assert self.mul(self.add(self.one, w), out) == self.one
        assert self.mul(out, self.add(self.one, w)) == self.one
        return out

    def identity(self):
        return [[self.one if i == j else self.zero for j in range(3)] for i in range(3)]

    def matrix_mul(self, a, b):
        out = [[{} for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    out[i][j] = self.add(out[i][j], self.mul(a[i][k], b[k][j]))
        return out

    def product(self, *matrices):
        out = self.identity()
        for matrix in matrices:
            out = self.matrix_mul(out, matrix)
        return out

    def e(self, i, j, a):
        assert i != j
        out = self.identity()
        out[i][j] = a
        return out

    def diagonal(self, a, b, c):
        return [[(a, b, c)[i] if i == j else {} for j in range(3)] for i in range(3)]


def check(p):
    r = CheckRing(p)
    x, y = r.x, r.y
    xy, yx = r.mul(x, y), r.mul(y, x)
    assert xy != yx, "This stress ring must genuinely be noncommutative."
    a, b = r.add(x, r.mul(y, y)), r.add(y, xy)
    count = 0
    for i, j, k in permutations(range(3)):
        assert r.product(r.e(i, j, a), r.e(i, j, b)) == r.e(i, j, r.add(a, b))
        count += 1
        lhs = r.product(r.e(i, k, a), r.e(k, j, b), r.e(i, k, r.neg(a)), r.e(k, j, r.neg(b)))
        assert lhs == r.e(i, j, r.mul(a, b))
        count += 1
    u, v = r.add(r.one, a), r.add(r.one, b)
    ui, vi = r.inverse_one_plus(a), r.inverse_one_plus(b)
    uv = r.mul(u, v)
    uvi = r.mul(vi, ui)
    assert r.mul(uv, uvi) == r.one
    assert r.mul(uvi, uv) == r.one
    count += 2
    du, dv, duv = r.diagonal(u, ui, r.one), r.diagonal(v, vi, r.one), r.diagonal(uv, uvi, r.one)
    for unit, inverse, expected in ((u, ui, du), (v, vi, dv), (uv, uvi, duv)):
        lhs = r.product(r.e(0, 1, unit), r.e(1, 0, r.neg(inverse)), r.e(0, 1, unit),
                        r.e(0, 1, r.neg(r.one)), r.e(1, 0, r.one), r.e(0, 1, r.neg(r.one)))
        assert lhs == expected
        count += 1
    defect = r.product(du, dv, r.diagonal(uvi, uv, r.one))
    commutator = r.mul(r.mul(r.mul(ui, vi), u), v)
    assert defect == r.diagonal(r.one, commutator, r.one)
    count += 1
    assert r.product(du, dv) != duv, "The incorrect homomorphism shortcut must fail."
    count += 1
    assert commutator != r.one
    count += 1
    # A scalar elementary conjugator suffices to check coefficient ordering.
    q, qi = r.e(1, 0, r.one), r.e(1, 0, r.neg(r.one))
    conjugate = r.product(q, r.e(0, 1, a), qi)
    c = [[r.add(conjugate[i][j], r.neg(r.one) if i == j else {}) for j in range(3)] for i in range(3)]
    assert r.matrix_mul(c, c) == [[{} for _ in range(3)] for _ in range(3)]
    count += 1
    print(f"p={p}: {count} named exact checks passed (plus supporting assertions); noncommutativity and nontrivial diagonal defect confirmed")
    return count


if __name__ == "__main__":
    total = sum(check(p) for p in (2, 3, 5))
    print(f"TOTAL: {total} named exact checks passed (plus supporting assertions)")
