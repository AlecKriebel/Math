#!/usr/bin/env python3
"""Exact certificates for OPG-37327 partial work. Standard library only.

All geometric decisions use Q(sqrt(2)), never floating point.
This verifies a counterexample to a local lemma, NOT a square covering.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import total_ordering
import json
from pathlib import Path


@total_ordering
@dataclass(frozen=True)
class Q:
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, 'a', F(self.a))
        object.__setattr__(self, 'b', F(self.b))

    @staticmethod
    def of(x):
        return x if isinstance(x, Q) else Q(x)

    def __add__(self, other):
        o = Q.of(other)
        return Q(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self):
        return Q(-self.a, -self.b)

    def __sub__(self, other):
        return self + -Q.of(other)

    def __rsub__(self, other):
        return Q.of(other) - self

    def __mul__(self, other):
        o = Q.of(other)
        return Q(self.a*o.a + 2*self.b*o.b, self.a*o.b + self.b*o.a)

    __rmul__ = __mul__

    def __truediv__(self, other):
        o = Q.of(other)
        norm = o.a*o.a - 2*o.b*o.b
        if not norm:
            raise ZeroDivisionError
        return self * Q(o.a/norm, -o.b/norm)

    def sign(self):
        a, b = self.a, self.b
        if not b:
            return (a > 0) - (a < 0)
        if not a:
            return (b > 0) - (b < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        d = a*a - 2*b*b
        # A nonzero rational cannot have rational ratio sqrt(2).
        assert d
        return (1 if d > 0 else -1) * (1 if a > 0 else -1)

    def __lt__(self, other):
        return (self - other).sign() < 0

    def __eq__(self, other):
        try:
            o = Q.of(other)
            return self.a == o.a and self.b == o.b
        except (TypeError, ValueError):
            return False

    def record(self):
        return {'rational': str(self.a), 'sqrt2_coefficient': str(self.b)}


def sub(p, q):
    return (p[0]-q[0], p[1]-q[1])


def cross(p, q):
    return p[0]*q[1] - p[1]*q[0]


def dot(p, q):
    return p[0]*q[0] + p[1]*q[1]


def clip_segment(poly, start, end):
    """Clip a segment against a CCW convex polygon, returning t interval."""
    lo, hi = Q(0), Q(1)
    direction = sub(end, start)
    for i, p in enumerate(poly):
        edge = sub(poly[(i+1) % len(poly)], p)
        intercept = cross(edge, sub(start, p))
        slope = cross(edge, direction)
        if slope == 0:
            if intercept < 0:
                return None
        elif slope > 0:
            lo = max(lo, -intercept/slope)
        else:
            hi = min(hi, -intercept/slope)
        if lo > hi:
            return None
    return lo, hi


def twice_area(poly):
    return sum((cross(p, poly[(i+1) % len(poly)])
                for i, p in enumerate(poly)), Q())


def clip_y_nonnegative(poly):
    out = []
    for i, p in enumerate(poly):
        q = poly[(i+1) % len(poly)]
        ip, iq = p[1] >= 0, q[1] >= 0
        if ip:
            out.append(p)
        if ip != iq:
            t = -p[1]/(q[1]-p[1])
            out.append((p[0] + t*(q[0]-p[0]), Q(0)))
    return out


def verify_instance(h=F(101, 100), delta=F(1, 100), n=4):
    h, delta = Q(h), Q(delta)
    root2, r = Q(0, 1), Q(0, F(1, 2))
    s, cx, cy = n*h, 2*h, r-delta
    poly = [(cx, cy-r), (cx+r, cy), (cx, cy+r), (cx-r, cy)]
    edges = [sub(poly[(i+1) % 4], poly[i]) for i in range(4)]
    assert all(dot(e, e) == 1 for e in edges)
    assert all(dot(edges[i], edges[(i+1) % 4]) == 0 for i in range(4))
    assert twice_area(poly) == 2
    assert h > 1 and s > n
    intersections = []
    perimeter_hits = []
    total = Q()
    for axis in ('horizontal', 'vertical'):
        for k in range(n+1):
            z = k*h
            start, end = (((Q(), z), (s, z)) if axis == 'horizontal'
                          else ((z, Q()), (z, s)))
            interval = clip_segment(poly, start, end)
            length = Q() if interval is None else s*(interval[1]-interval[0])
            if interval is not None and k in (0, n):
                perimeter_hits.append((axis, k))
            if length > 0:
                intersections.append({'axis': axis, 'index': k, 'length': length.record()})
            total += length
    assert perimeter_hits == [('horizontal', 0)]
    assert [(x['axis'], x['index']) for x in intersections] == [
        ('horizontal', 0), ('horizontal', 1), ('vertical', 2)]
    assert total == 3*root2 - 2*h - delta
    claimed_bound = F(3, 2)*root2
    assert total > claimed_bound
    assert all(Q() < p[0] < s and p[1] < s for p in poly)
    spill = 1 - twice_area(clip_y_nonnegative(poly))/2
    assert spill == delta*delta
    return {
        'n': n, 'h': h.record(), 'delta': delta.record(),
        'side': s.record(),
        'vertices': [[x.record(), y.record()] for x, y in poly],
        'perimeter_intersections': perimeter_hits,
        'nonzero_grid_intersections': intersections,
        'total_grid_length': total.record(),
        'claimed_bound': claimed_bound.record(),
        'strict_excess': (total-claimed_bound).record(),
        'spill_area': spill.record(),
        'unit_square_check': True,
        'single_sided_check': True,
        'strict_violation_check': True,
        'is_original_conjecture_counterexample': False,
    }


def tests():
    # Exact algebra and sign tests, including severe cancellation.
    assert Q(0, 1)*Q(0, 1) == 2
    assert Q(-7, 5) > 0 and Q(-10, 7) < 0
    assert Q(10, -7) > 0 and Q(7, -5) < 0
    assert Q(1, 1)/Q(1, 1) == 1
    assert Q(-1414213562373095, 1000000000000000) > 0
    # Generic clip sanity checks on the axis-aligned unit square.
    p = [(Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(1)), (Q(0), Q(1))]
    assert clip_segment(p, (Q(-1), Q(F(1,2))), (Q(2), Q(F(1,2)))) == (Q(F(1,3)), Q(F(2,3)))
    assert clip_segment(p, (Q(-1), Q(2)), (Q(2), Q(2))) is None
    assert clip_segment(p, (Q(0), Q(0)), (Q(1), Q(0))) == (Q(0), Q(1))
    # Nearby exact parameters; these supplement, not replace, the proof.
    verify_instance(F(100001,100000), F(1,100))
    verify_instance(F(21,20), F(1,100))
    # Analytically invalid parameters must not produce certificates.
    rejected = 0
    for h, d in [(F(6,5), F(1,100)), (F(101,100), F(1,2))]:
        try:
            verify_instance(h, d)
        except AssertionError:
            rejected += 1
    assert rejected == 2
    # Finite smoke checks for the relaxation witnesses described in PROOF.md.
    # Their all-n validity is proved algebraically there, not inferred here.
    for n in range(2, 101):
        s = F(n) + F(1, 4*n)
        N = n*n+1
        assert 0 < N-s*s < 1
        assert (n+1)*(n+1) <= N+2*n
        assert Q(2*(n+1)*s) < 2*Q(0,1)*N
    return {'exact_arithmetic_tests': 'PASS', 'generic_clipping_tests': 'PASS',
            'nearby_parameter_tests': 'PASS', 'negative_controls': 2,
            'relaxation_smoke_range': [2,100]}


def main():
    report = {'schema': 1, 'status': 'PASS',
              'claim': 'Counterexample to the unrestricted local grid-length bound in Lemma 2 of arXiv:2609.15876v1',
              'certificate': verify_instance(), 'tests': tests()}
    target = Path(__file__).with_name('results.json')
    encoded = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if target.exists():
        assert target.read_text() == encoded, 'Committed results differ from recomputation'
    print(encoded, end='')


if __name__ == '__main__':
    main()
