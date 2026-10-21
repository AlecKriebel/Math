"""Exact rational checks of rejection certificates; no floating point.

Run with Python 3. These checks supplement the general arguments in
approach_constructive.md; they do not test or establish a quasi-isometry.
"""

from bisect import bisect_right
from fractions import Fraction as Q
import json


class PL:
    def __init__(self, points):
        pts = [(Q(x), Q(y)) for x, y in points]
        assert pts[0] == (0, 0) and pts[-1] == (1, 1)
        clean = []
        for pt in pts:
            clean.append(pt)
            while len(clean) >= 3:
                (a, u), (b, v), (c, w) = clean[-3:]
                if (v-u)*(c-b) != (w-v)*(b-a):
                    break
                clean.pop(-2)
        assert all(a < b and u < v for (a,u),(b,v) in zip(clean, clean[1:]))
        self.points = tuple(clean)
        self.xs = tuple(x for x, _ in clean)

    def __call__(self, x):
        x = Q(x)
        assert 0 <= x <= 1
        i = min(bisect_right(self.xs, x)-1, len(self.points)-2)
        a, u = self.points[i]
        b, v = self.points[i+1]
        return u + (x-a)*(v-u)/(b-a)

    def inverse(self):
        return PL([(y, x) for x, y in self.points])

    def __mul__(self, other):
        # Product is composition, self after other.
        oi = other.inverse()
        xs = set(other.xs) | {oi(x) for x in self.xs}
        return PL([(x, self(other(x))) for x in sorted(xs)])

    def __pow__(self, n):
        if n < 0:
            return self.inverse() ** (-n)
        out = ID
        base = self
        while n:
            if n % 2:
                out = out * base
            base = base * base
            n //= 2
        return out

    def slopes(self):
        return [(v-u)/(b-a) for (a,u),(b,v) in zip(self.points, self.points[1:])]


def lg2(q):
    q = Q(q)
    a, b = q.numerator, q.denominator
    assert a > 0 and a & (a-1) == 0 and b & (b-1) == 0
    return a.bit_length() - b.bit_length()


def depth(q):
    q = Q(q)
    b = q.denominator
    assert b & (b-1) == 0
    return b.bit_length()-1


def clone_right(f):
    return PL([(0,0)] + [(Q(1,2)+x/2, Q(1,2)+y/2) for x,y in f.points])


ID = PL([(0,0), (1,1)])
X0 = PL([(0,0), (Q(1,2),Q(1,4)), (Q(3,4),Q(1,2)), (1,1)])
X1 = clone_right(X0)
gens = [X0, X0.inverse(), X1, X1.inverse()]

dyadic_checks = 0
for d in range(1, 12):
    for m in range(1, 2**d, 2):
        q = Q(m,2**d)
        for s in gens:
            assert depth(s(q)) <= d+1
            dyadic_checks += 1

rows = []
for n in range(1,41):
    h = X1**n
    f = h*X0
    assert f(Q(1,2)) == Q(1,4)
    assert lg2(h.slopes()[-1]) == n
    assert lg2(f.slopes()[-1]) == n+1
    w = h.inverse()*X0*h
    assert max(map(lg2,w.slopes())) == 2*n+1
    q = 1-Q(1,2**(n+2))
    assert q in w.xs and w(q) == Q(1,2)
    j = w.xs.index(q)
    assert lg2(w.slopes()[j]) == 2*n+1
    escape = X0**(-n)
    assert escape.inverse()(Q(1,2)) == Q(1,2**(n+1))
    conjugate = (X0**(-n))*X1*(X0**n)
    assert max(depth(x) for x in conjugate.xs[1:-1]) == n+3
    rows.append({"n":n, "cb_output_distance":2*n+1,
                 "height_vertical_output_distance":2*n+1,
                 "right_height_breakpoint_depth":n+3,
                 "stabilizer_distance":n})

print(json.dumps({"arithmetic":"fractions.Fraction", "dyadic_generator_checks":dyadic_checks,
                  "certificate_checks":len(rows), "sample_rows":rows[:3]+rows[-2:]}, indent=2))
