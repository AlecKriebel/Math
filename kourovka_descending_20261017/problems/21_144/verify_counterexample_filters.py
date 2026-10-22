"""Exact rational checks supporting, but not proving, the construction filters.

Run with Python 3. No dependencies or floating point arithmetic are used.
The mathematical statements and their unbounded proofs are in
approach_counterexamples.md. This script does not decide the conjecture.
"""

from fractions import Fraction as Q
import json


class PL:
    """Increasing PL map, stored by graph vertices and canonically reduced."""

    def __init__(self, vertices):
        pts = [(Q(x), Q(y)) for x, y in vertices]
        assert pts[0] == (0, 0) and pts[-1] == (1, 1)
        assert all(x < u and y < v for (x, y), (u, v) in zip(pts, pts[1:]))
        reduced = []
        for point in pts:
            reduced.append(point)
            while len(reduced) >= 3:
                (x, y), (u, v), (s, t) = reduced[-3:]
                if (v - y) * (s - u) != (t - v) * (u - x):
                    break
                reduced.pop(-2)
        self.pts = tuple(reduced)

    def __call__(self, x):
        x = Q(x)
        for (a, b), (c, d) in zip(self.pts, self.pts[1:]):
            if a <= x <= c:
                return b + (d - b) * (x - a) / (c - a)
        raise ValueError(x)

    def inv(self):
        return PL([(y, x) for x, y in self.pts])

    def __mul__(self, other):
        """Product is ordinary composition: (self*other)(x)=self(other(x))."""
        pre = other.inv()
        cuts = sorted({x for x, _ in other.pts} | {pre(x) for x, _ in self.pts})
        return PL([(x, self(other(x))) for x in cuts])

    def __pow__(self, n):
        if n < 0:
            return self.inv() ** (-n)
        result = ID
        for _ in range(n):
            result = result * self
        return result

    def __eq__(self, other):
        return self.pts == other.pts

    def breakpoints(self):
        return len(self.pts) - 2

    def dyadic(self):
        def power_two(n):
            return n > 0 and n & (n - 1) == 0

        def dyadic_q(x):
            return power_two(x.denominator)

        slopes = [(d - b) / (c - a) for (a, b), (c, d) in zip(self.pts, self.pts[1:])]
        return all(dyadic_q(x) and dyadic_q(y) for x, y in self.pts) and all(
            power_two(s.numerator) and power_two(s.denominator) for s in slopes
        )


ID = PL([(0, 0), (1, 1)])
X0 = PL([(0, 0), (Q(1, 2), Q(1, 4)), (Q(3, 4), Q(1, 2)), (1, 1)])
X1 = PL([(0, 0), (Q(1, 2), Q(1, 2)), (Q(3, 4), Q(5, 8)),
         (Q(7, 8), Q(3, 4)), (1, 1)])


def comm(a, b):
    return a * b * a.inv() * b.inv()


def certificate(a, b):
    return {
        "first_relator_identity": comm(a * b.inv(), a.inv() * b * a) == ID,
        "second_relator_identity": comm(a * b.inv(), a ** -2 * b * a ** 2) == ID,
        "generator_commutator_nontrivial": comm(a, b) != ID,
    }


def finite_diagonal(count):
    vertices = [(Q(0), Q(0))]
    for n in range(count, 0, -1):
        left, right = Q(1, 2 ** (n + 1)), Q(1, 2 ** n)
        width = right - left
        for x, y in X0.pts:
            point = (left + width * x, left + width * y)
            if vertices[-1] != point:
                vertices.append(point)
    vertices.append((Q(1), Q(1)))
    return PL(vertices)


if __name__ == "__main__":
    assert X0.dyadic() and X1.dyadic()
    assert X0 * X0.inv() == ID and X1.inv() * X1 == ID
    cert = certificate(X0, X1)
    assert all(cert.values())
    commuting = certificate(X0, X0 ** 2)
    assert commuting["first_relator_identity"] and commuting["second_relator_identity"]
    assert not commuting["generator_commutator_nontrivial"]
    diagonal_counts = []
    for n in (1, 2, 3, 8, 16, 32):
        f = finite_diagonal(n)
        assert f.dyadic()
        assert f.breakpoints() == 3 * n + 1
        diagonal_counts.append({"active_cells": n, "slope_breakpoints": f.breakpoints()})
    print(json.dumps({
        "arithmetic": "exact Fraction; no floating point",
        "standard_F_certificate": cert,
        "commuting_pair_rejected": not commuting["generator_commutator_nontrivial"],
        "finite_diagonal_counts": diagonal_counts,
        "scope": "finite exact checks only; infinite claims require the written proofs",
    }, indent=2))
