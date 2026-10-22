#!/usr/bin/env python3
"""Exact rational PL verification of the standard finite F certificate.

This verifies an explicit witness in the known PL model. It does not infer
that arbitrary groups satisfying the 21.140 hypotheses have such a witness.
Only Python's standard library is used; no numerical tolerances occur.
"""

from fractions import Fraction as Q
from bisect import bisect_right
import json


class PL:
    def __init__(self, points):
        pts = [(Q(x), Q(y)) for x, y in points]
        assert pts[0] == (0, 0) and pts[-1] == (1, 1)
        assert all(x0 < x1 and y0 < y1
                   for (x0, y0), (x1, y1) in zip(pts, pts[1:]))
        reduced = []
        for p in pts:
            reduced.append(p)
            while len(reduced) >= 3:
                (x0, y0), (x1, y1), (x2, y2) = reduced[-3:]
                if (y1-y0)*(x2-x1) != (y2-y1)*(x1-x0):
                    break
                del reduced[-2]
        self.points = tuple(reduced)

    def __call__(self, x):
        x = Q(x)
        assert 0 <= x <= 1
        index = min(bisect_right([p[0] for p in self.points], x)-1,
                    len(self.points)-2)
        x0, y0 = self.points[index]
        x1, y1 = self.points[index+1]
        return y0 + (x-x0)*(y1-y0)/(x1-x0)

    def inverse(self):
        return PL([(y, x) for x, y in self.points])

    def __mul__(self, other):
        """The product f*g is f composed with g."""
        preimage = other.inverse()
        xs = {x for x, _ in other.points}
        xs.update(preimage(x) for x, _ in self.points)
        return PL([(x, self(other(x))) for x in sorted(xs)])

    def __eq__(self, other):
        return self.points == other.points

    def as_json(self):
        return [[str(x), str(y)] for x, y in self.points]


def commutator(f, g):
    return f.inverse()*g.inverse()*f*g


identity = PL([(0, 0), (1, 1)])
a = PL([(0, 0), (Q(1, 2), Q(1, 4)),
        (Q(3, 4), Q(1, 2)), (1, 1)])
b = PL([(0, 0), (Q(1, 2), Q(1, 2)),
        (Q(3, 4), Q(5, 8)), (Q(7, 8), Q(3, 4)), (1, 1)])
c = a*b.inverse()
d1 = a.inverse()*b*a
d2 = a.inverse()*a.inverse()*b*a*a
r1, r2, noncomm = commutator(c, d1), commutator(c, d2), commutator(a, b)

assert r1 == identity, "First F defining relator failed"
assert r2 == identity, "Second F defining relator failed"
assert noncomm != identity, "The generating pair unexpectedly commutes"
assert a*a.inverse() == identity and b*b.inverse() == identity

# A finite rational witness for the inequality [a,b] != 1.
witness = next((x, y) for x, y in noncomm.points if x != y)
report = {
    "arithmetic": "exact fractions; no floating point",
    "multiplication": "f*g means f composed with g",
    "relator_1_identity": r1 == identity,
    "relator_2_identity": r2 == identity,
    "commutator_nonidentity": noncomm != identity,
    "noncommutation_witness": {"x": str(witness[0]),
                               "commutator_x": str(witness[1])},
    "a": a.as_json(),
    "b": b.as_json(),
    "commutator": noncomm.as_json(),
    "scope": "Known PL model only; no proof of Kourovka 21.140",
}
print(json.dumps(report, indent=2))
