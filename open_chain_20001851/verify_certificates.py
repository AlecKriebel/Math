#!/usr/bin/env python3
"""Exact rational checks and outward-rounded algebraic interval checks.

Run with Python 3 standard library only. Finite checks support, but do not
replace, the proofs in ATTEMPT_1.md through ATTEMPT_5.md. In particular the
eight-bar length *equalities* follow from the construction formulas; interval
containment of one is only a consistency check for those equalities.
"""
from fractions import Fraction as F
from itertools import product
from math import isqrt
import json


def add(a, b): return tuple(x + y for x, y in zip(a, b))
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def scale(c, a): return tuple(c * x for x in a)
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return a[0] * b[1] - a[1] * b[0]
def orient(a, b, c): return cross(sub(b, a), sub(c, a))


def on_segment(a, b, p):
    return orient(a, b, p) == 0 and all(min(x, y) <= z <= max(x, y)
                                      for x, y, z in zip(a, b, p))


def intersects(a, b, c, d):
    signs = [orient(a, b, c), orient(a, b, d),
             orient(c, d, a), orient(c, d, b)]
    if signs[0] * signs[1] < 0 and signs[2] * signs[3] < 0:
        return True
    return (on_segment(a, b, c) or on_segment(a, b, d)
            or on_segment(c, d, a) or on_segment(c, d, b))


def check_simple_projection(points):
    n = len(points) - 1
    directions = [sub(b, a) for a, b in zip(points, points[1:])]
    assert all(dot(v, v) > 0 for v in directions)
    for a, b in zip(directions, directions[1:]):
        assert cross(a, b) != 0 or dot(a, b) > 0
    pairs = 0
    for i in range(n):
        for j in range(i + 2, n):
            assert not intersects(points[i], points[i + 1], points[j], points[j + 1])
            pairs += 1
    return pairs


def interval_order_checks():
    count = 0
    for n in range(4, 7):
        for x in product(range(4), repeat=n + 1):
            intervals = [(min(x[i:i+2]), max(x[i:i+2])) for i in range(n)]
            old = all(intervals[i][1] < intervals[j][0]
                      or intervals[j][1] < intervals[i][0]
                      for i in range(n) for j in range(i + 2, n))
            def ordered(y):
                return (all(y[i] < y[i+1] for i in range(1, n-1))
                        and y[0] < y[2] and y[n] > y[n-2])
            new = ordered(x) or ordered(tuple(-z for z in x))
            assert old == new, (n, x)
            count += 1
    return count


def rational_witness_checks():
    five = [tuple(map(F, p)) for p in [
        (0,-1,0), (0,0,0), (1,0,0), (F(2,5),F(4,5),0),
        (F(-1,5),0,0), (F(-6,5),0,0)]]
    six = [tuple(map(F, p)) for p in [
        (0,-1,0), (0,0,0), (F(24,25),0,F(-7,25)),
        (F(48,125),F(96,125),F(-14,25)),
        (F(-24,125),0,F(-21,25)), (F(-24,125),0,F(4,25)),
        (F(-149,125),0,F(4,25))]]
    edges = lambda p: [sub(b, a) for a, b in zip(p, p[1:])]
    d5, d6 = edges(five), edges(six)
    assert all(dot(d, d) == 1 for d in d5 + d6)
    assert all(sum(w * d[k] for w, d in zip([6,5,5], d5[1:4])) == 0
               for k in range(3))
    assert all(sum(w * d[k] for w, d in zip([150,125,125,112], d6[1:5])) == 0
               for k in range(3))
    a, b, c = d6[1], d6[2], d6[4]
    determinant = (a[0]*(b[1]*c[2]-b[2]*c[1])
                   -a[1]*(b[0]*c[2]-b[2]*c[0])
                   +a[2]*(b[0]*c[1]-b[1]*c[0]))
    assert determinant != 0
    p5 = [(x, y) for x, y, z in five]
    p6 = [(x-z/10, y) for x, y, z in six]
    expected = [(0,-1),(0,0),(F(247,250),0),(F(11,25),F(96,125)),
                (F(-27,250),0),(F(-26,125),0),(F(-151,125),0)]
    assert p6 == expected
    pairs = check_simple_projection(p5) + check_simple_projection(p6)
    return {"exact_unit_lengths": 11, "exact_positive_dependencies": 2,
            "six_bar_independence_determinant": str(determinant),
            "exact_nonadjacent_projected_pairs": pairs}


class Interval:
    """Closed rational interval, no binary floating-point arithmetic."""
    def __init__(self, lo, hi=None):
        self.lo = F(lo)
        self.hi = F(lo if hi is None else hi)
        assert self.lo <= self.hi
    @staticmethod
    def coerce(x): return x if isinstance(x, Interval) else Interval(x)
    def __add__(self, other):
        q = self.coerce(other)
        return Interval(self.lo + q.lo, self.hi + q.hi)
    __radd__ = __add__
    def __neg__(self): return Interval(-self.hi, -self.lo)
    def __sub__(self, other): return self + (-self.coerce(other))
    def __rsub__(self, other): return self.coerce(other) - self
    def __mul__(self, other):
        q = self.coerce(other)
        values = [self.lo*q.lo, self.lo*q.hi, self.hi*q.lo, self.hi*q.hi]
        return Interval(min(values), max(values))
    __rmul__ = __mul__
    def __truediv__(self, other):
        q = self.coerce(other)
        assert q.lo > 0 or q.hi < 0
        return self * Interval(1/q.hi, 1/q.lo)
    def __rtruediv__(self, other): return self.coerce(other) / self
    def square(self):
        lo = 0 if self.lo <= 0 <= self.hi else min(self.lo*self.lo, self.hi*self.hi)
        return Interval(lo, max(self.lo*self.lo, self.hi*self.hi))
    def sqrt(self):
        assert self.lo >= 0
        scale = 10**30
        lower = isqrt(self.lo.numerator * scale * scale // self.lo.denominator)
        upper = isqrt(self.hi.numerator * scale * scale // self.hi.denominator) + 1
        result = Interval(F(lower, scale), F(upper, scale))
        assert result.lo*result.lo <= self.lo
        assert result.hi*result.hi >= self.hi
        return result


def rounded_lower(x):
    """A human-readable certified rational lower bound, rounded down."""
    return str(F(x.lo.numerator * 10**8 // x.lo.denominator, 10**8))


def barrier_checks():
    I = Interval
    h, t = I(F(1,4)), I(F(99,100))
    root5 = I(5).sqrt()
    R2 = (5 + root5)/10
    R = R2.sqrt()
    co72, si72 = (root5-1)/4, (10+2*root5).sqrt()/4
    co144, si144 = -(root5+1)/4, (10-2*root5).sqrt()/4
    q0 = (R, I(0), h)
    q1 = (R*co72, R*si72, h)
    q2 = (R*co144, R*si144, h)
    q3 = (R*co144, -R*si144, h)
    q5 = scale(t, q0)
    A, B = q3[:2], q5[:2]
    D = sub(B, A)
    L2 = sum(x.square() for x in D)
    r2 = 1 - h.square()*(1-t).square()
    alpha = (r2-1+L2)/(2*L2)
    beta2 = r2/L2-alpha.square()
    beta = beta2.sqrt()
    JD = (-D[1],D[0])
    Q = sub(add(A,scale(alpha,D)),scale(beta,JD))
    q4 = (*Q,t*h)
    ring = [q0,q1,q2,q3,q4,q5]
    rho2 = R2+h.square()
    c = rho2/(2*R)
    s = (1-c.square()).sqrt()
    b = (c,s,I(0))
    points = [(I(0),I(0),I(1)),(I(0),I(0),I(0)),b]+ring
    # Equality checks are enclosures only; the exact identities are proved
    # symbolically from the construction in ATTEMPT_5.md.
    lengths = [sum(x.square() for x in sub(v,u)) for u,v in zip(points,points[1:])]
    assert len(lengths) == 8
    assert all(x.lo <= 1 <= x.hi for x in lengths)
    margins = []
    def positive(name, x):
        assert x.lo > 0, (name, x.lo, x.hi)
        margins.append((name,rounded_lower(x)))
    positive("circle_center_distance_squared",L2)
    positive("circle_height_squared",r2)
    positive("circle_intersection_radicand",beta2)
    positive("stem_x",c)
    positive("stem_y",s)
    positive("ring_plane_gap",h-t*h)
    positive("negative_q3_y",-q3[1])
    positive("negative_q4_y",-q4[1])
    radius_slacks = [1-sum(x.square() for x in q) for q in ring]
    for k,x in enumerate(radius_slacks): positive(f"unit_ball_slack_{k}",x)
    for k,q in enumerate(ring): positive(f"positive_height_{k}",q[2])
    polygon = [(q[0]/q[2],q[1]/q[2]) for q in ring[:5]]
    origin_margins, convex_margins = [], []
    for i in range(5):
        j=(i+1)%5
        v=cross(polygon[i],polygon[j])
        positive(f"origin_left_of_edge_{i}",v)
        origin_margins.append(v)
        for k in range(5):
            if k not in (i,j):
                v=orient(polygon[i],polygon[j],polygon[k])
                positive(f"vertex_{k}_left_of_edge_{i}",v)
                convex_margins.append(v)
    return {"parameter": "99/100", "outward_sqrt_scale": "10^30",
            "certified_strict_inequalities": len(margins),
            "unit_length_equality_enclosure_smoke_checks": 8,
            "equalities_proved_by_formulas_not_intervals": True,
            "minimum_unit_ball_slack_lower_bound": rounded_lower(min(radius_slacks,key=lambda x:x.lo)),
            "minimum_origin_interior_margin_lower_bound": rounded_lower(min(origin_margins,key=lambda x:x.lo)),
            "minimum_convexity_margin_lower_bound": rounded_lower(min(convex_margins,key=lambda x:x.lo)),
            "geometry_margins": dict(margins)}


def main():
    result = {"status": "PASS", "original_problem": "UNSOLVED",
              "proof_attempts": 5,
              "scalar_interval_equivalence_cases": interval_order_checks(),
              "rational_witnesses": rational_witness_checks(),
              "eight_bar_fixed_tail_barrier": barrier_checks(),
              "limitations": ["No exact component computation was performed.",
                              "The eight-bar barrier fixes seven tail bars and is not a locking proof.",
                              "Finite and interval checks do not replace the written general proofs."]}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
