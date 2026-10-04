#!/usr/bin/env python3
"""Independent, standard-library-only rational interval certificates.

All endpoints are integers divided by SCALE. Arithmetic rounds outward by
integer floor/ceiling. Square roots use isqrt; logarithms use a positive
atanh series with an explicit geometric tail. No floating point, mpmath,
platform logarithm, or original verifier is used in the certificates.
"""
import argparse
import json
from math import isqrt

DIGITS = 50
SCALE = 10**DIGITS
TERMS = 70


def ceildiv(a, b):
    assert b > 0
    return -((-a)//b)


class I:
    def __init__(self, lo, hi=None):
        self.lo = lo
        self.hi = lo if hi is None else hi
        assert self.lo <= self.hi

    @staticmethod
    def integer(n):
        return I(n*SCALE)

    @staticmethod
    def fraction(n, d):
        assert d > 0
        return I((n*SCALE)//d, ceildiv(n*SCALE, d))

    @staticmethod
    def coerce(x):
        return x if isinstance(x, I) else I.integer(x)

    def __add__(self, other):
        other = I.coerce(other)
        return I(self.lo+other.lo, self.hi+other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -I.coerce(other)

    def __rsub__(self, other):
        return I.coerce(other) + -self

    def __mul__(self, other):
        other = I.coerce(other)
        products = [a*b for a in (self.lo, self.hi)
                    for b in (other.lo, other.hi)]
        return I(min(products)//SCALE, ceildiv(max(products), SCALE))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = I.coerce(other)
        assert other.lo > 0 or other.hi < 0, 'division by interval containing 0'
        if other.hi < 0:
            return (-self)/(-other)
        values = [(a*SCALE, b) for a in (self.lo, self.hi)
                  for b in (other.lo, other.hi)]
        return I(min(a//b for a, b in values),
                 max(ceildiv(a, b) for a, b in values))

    def __rtruediv__(self, other):
        return I.coerce(other)/self

    def positive(self):
        return self.lo > 0

    def negative(self):
        return self.hi < 0

    def contains(self, other):
        other = I.coerce(other)
        return self.lo <= other.lo <= other.hi <= self.hi

    def overlaps(self, other):
        return max(self.lo, other.lo) <= min(self.hi, other.hi)

    def as_json(self):
        return {'lower': decimal(self.lo), 'upper': decimal(self.hi)}


def decimal(x):
    s = '-' if x < 0 else ''
    a, b = divmod(abs(x), SCALE)
    return f'{s}{a}.{b:0{DIGITS}d}'


def sqrt_integer(n):
    a = isqrt(n*SCALE*SCALE)
    return I(a, a if a*a == n*SCALE*SCALE else a+1)


def log_unit_ratio(n, d):
    """log(n/d) for 1 <= n/d <= 2 using only rational intervals."""
    assert d <= n <= 2*d
    z = I.fraction(n-d, n+d)
    z2 = z*z
    term = z
    total = I.integer(0)
    for j in range(TERMS):
        total += term/(2*j+1)
        term = term*z2
    # term encloses z^(2*TERMS+1). All remaining terms are positive;
    # denominators >= 2*TERMS+1 give this geometric upper bound.
    tail = (2*term)/((2*TERMS+1)*(1-z2))
    return 2*total + I(0, tail.hi)


LOG2 = log_unit_ratio(2, 1)


def log_scalar_scaled(q):
    assert q > 0
    n, d, k = q, SCALE, 0
    while n > 2*d:
        d *= 2
        k += 1
    while n < d:
        n *= 2
        k -= 1
    return log_unit_ratio(n, d) + k*LOG2


def log_interval(x):
    assert x.lo > 0
    lo, hi = log_scalar_scaled(x.lo), log_scalar_scaled(x.hi)
    return I(lo.lo, hi.hi)


def integrate(x, cutoff):
    """Independent merged-event partition and interval cell integration."""
    assert x.lo > 0 and cutoff >= 1
    left = total = I.integer(0)
    n = m = cells = 0
    end = I.integer(cutoff)
    while True:
        integer_event = I.integer(n+1)
        scaled_event = I.integer(m+1)/x
        if integer_event.hi < scaled_event.lo:
            right, event = integer_event, 'integer'
        elif scaled_event.hi < integer_event.lo:
            right, event = scaled_event, 'scaled'
        elif (integer_event.lo == integer_event.hi ==
              scaled_event.lo == scaled_event.hi):
            right, event = integer_event, 'both'
        else:
            raise ArithmeticError('overlapping events; no guessed ordering')
        if right.lo >= end.hi:
            right, event = end, 'end'
        elif right.hi >= end.lo:
            raise ArithmeticError('uncertified cutoff ordering')
        assert left.hi < right.lo
        if n == m == 0:
            cell = x*right
        else:
            cell = (x*(right-left) - (m+n*x)*log_interval(right/left)
                    + n*m*(1/left-1/right))
        total += cell
        cells += 1
        if event == 'end':
            tail = I.fraction(1, cutoff)
            return total + I(0, tail.hi), cells
        left = right
        n += event in ('integer', 'both')
        m += event in ('scaled', 'both')


def test_interval_core():
    from fractions import Fraction as Q
    # Exact corner tests, including signed divisions and cancellation.
    count = 0
    vals = [I(-5*SCALE, -2*SCALE), I(-SCALE, 3*SCALE),
            I(2*SCALE, 5*SCALE), I.fraction(1, 3), I.fraction(-7, 13)]
    for a in vals:
        for b in vals:
            for op, exact in [(lambda: a+b, lambda x, y: x+y),
                              (lambda: a-b, lambda x, y: x-y),
                              (lambda: a*b, lambda x, y: x*y)]:
                c = op()
                for u in (a.lo, a.hi):
                    for v in (b.lo, b.hi):
                        w = exact(Q(u, SCALE), Q(v, SCALE))
                        assert Q(c.lo, SCALE) <= w <= Q(c.hi, SCALE)
                        count += 1
            if b.lo > 0 or b.hi < 0:
                c = a/b
                for u in (a.lo, a.hi):
                    for v in (b.lo, b.hi):
                        w = Q(u, v)
                        assert Q(c.lo, SCALE) <= w <= Q(c.hi, SCALE)
                        count += 1
    for n in range(1, 200):
        r = sqrt_integer(n)
        assert r.lo*r.lo <= n*SCALE*SCALE <= r.hi*r.hi
        count += 1
    assert log_interval(I.integer(1)).contains(0)
    # Non-transcendental identity controls do not substitute for the tail proof.
    assert log_interval(I.integer(4)).overlaps(2*LOG2)
    assert log_interval(I.fraction(1, 2)).overlaps(-LOG2)
    return count


def run(cutoff):
    out = {'backend': 'Python exact integers, directed fixed-point intervals',
           'scale': f'10^{DIGITS}', 'log_series_terms': TERMS,
           'cutoff': cutoff, 'tail_bound': f'1/{cutoff}',
           'core_exact_corner_tests': test_interval_core(),
           'metallic_reciprocals': []}
    for m in range(1, 12):
        y = (m+sqrt_integer(m*m+4))/2
        # The root and reciprocal relation are certified independently.
        assert (y*y-m*y-1).contains(0)
        ay, cells = integrate(y, cutoff)
        derivative = (ay-log_interval(y))/(1+y)
        expected = 'positive' if m <= 9 else 'negative'
        actual = ('positive' if derivative.positive() else
                  'negative' if derivative.negative() else 'inconclusive')
        assert expected == actual, (m, expected, actual)
        out['metallic_reciprocals'].append({
            'm': m, 'argument': y.as_json(), 'A': ay.as_json(),
            'derivative': derivative.as_json(), 'sign': actual,
            'integration_cells': cells})
    out['reciprocity_controls'] = []
    for m in (1, 3, 10):
        y = (m+sqrt_integer(m*m+4))/2
        a, _ = integrate(y, cutoff)
        b, _ = integrate(1/y, cutoff)
        assert a.overlaps(y*b)
        out['reciprocity_controls'].append({'m': m, 'overlap': True})
    # An independent large-y bound avoids pi and Euler's constant: A(1)
    # is bounded by the integral, and zeta(2)/6 < (1+integral_1^inf t^-2)/6
    # = 1/3. The weaker bound is already enough at y=11.
    a1, cells = integrate(I.integer(1), cutoff)
    large = (1+a1)/2 + I.fraction(1, 3*11) - log_interval(I.integer(11))/2
    assert large.negative()
    out['A_one'] = a1.as_json()
    out['A_one_cells'] = cells
    out['large_y_upper_bound_at_11'] = large.as_json()
    out['large_y_bound_inputs'] = 'A(1) direct integral upper bound; zeta(2)/6 < 1/3 by integral comparison'
    out['all_checks_passed'] = True
    return out


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cutoff', type=int, default=256)
    p.add_argument('--output')
    a = p.parse_args()
    if a.cutoff < 1:
        p.error('cutoff must be positive')
    data = json.dumps(run(a.cutoff), indent=2)+'\n'
    if a.output:
        from pathlib import Path
        Path(a.output).write_text(data)
    else:
        print(data, end='')
