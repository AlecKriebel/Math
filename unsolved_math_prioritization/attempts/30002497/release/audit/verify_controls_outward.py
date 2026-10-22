#!/usr/bin/env python3
"""Corrected outward-export variant of the frozen author interval controls.

The mathematics and in-memory interval operations are unchanged. Only interval
serialization is repaired, and interval backend version is explicitly checked.

Requires mpmath 1.3.0. Uses mpmath interval arithmetic and the analytic tail
0 <= integral_T^infinity {t}{x*t}/t^2 dt <= 1/T. Event order is verified.
"""
import argparse
import json
from pathlib import Path
from mpmath import iv, mp


def bracket(z, digits=None):
    """Serialize every binary endpoint outward as an exact finite decimal.

    mpmath str(iv.mpf) is a nearest-rounded display, not an outward-export API.
    Decoding _mpi_ uses the mpmath 1.3.0 (sign, mantissa, exponent, bitcount)
    representation. This function exports finite endpoints only.
    """
    from fractions import Fraction
    if digits is None:
        digits = iv.dps + 5
    scale = 10**digits
    def endpoint(raw, upper):
        sign, mantissa, exponent, bitcount = raw
        if bitcount < 0:
            raise ValueError('finite interval endpoints required')
        q = Fraction((-1)**sign * mantissa) * Fraction(2)**exponent
        q *= scale
        n = (-((-q.numerator)//q.denominator) if upper
             else q.numerator//q.denominator)
        integer, fraction = divmod(abs(n), scale)
        return ('-' if n < 0 else '') + f'{integer}.{fraction:0{digits}d}'
    return '[' + endpoint(z._mpi_[0], False) + ', ' + endpoint(z._mpi_[1], True) + ']'


def finite_integral(x, T):
    """Enclose integral_0^T, splitting at n and m/x.

    Between events the integrand is x-(m+n*x)/t+n*m/t^2.
    Each event comparison must be unambiguous; otherwise stop, never guess.
    """
    l = iv.mpf(0)
    total = iv.mpf(0)
    n = m = intervals = 0
    while True:
        a = iv.mpf(n + 1)
        b = iv.mpf(m + 1) / x
        if a < b:
            u, event = a, 'n'
        elif b < a:
            u, event = b, 'm'
        elif a == b:  # exact simultaneous event, e.g. the control x=1
            u, event = a, 'both'
        else:
            raise ArithmeticError('event ordering not certified')
        if u >= T:
            u, event = iv.mpf(T), 'end'
        elif not u < T:
            raise ArithmeticError('endpoint ordering not certified')
        if not l < u:
            raise ArithmeticError('nonpositive cell')
        if n == m == 0:
            total += x * u
        else:
            total += x*(u-l) - (m+n*x)*iv.ln(u/l) + n*m*(1/l-1/u)
        intervals += 1
        if event == 'end':
            return total, intervals
        l = u
        if event in ('n', 'both'):
            n += 1
        if event in ('m', 'both'):
            m += 1


def A_bound(x, T):
    val, cells = finite_integral(x, T)
    return val + iv.mpf([0, 1]) / T, cells


def checks(T=2048, dps=40):
    import mpmath
    if mpmath.__version__ != '1.3.0':
        raise RuntimeError('this certificate variant is pinned to mpmath 1.3.0')
    iv.dps = dps
    mp.dps = dps
    # Exact value control. iv.euler and iv.pi carry interval enclosures.
    exact_one = iv.ln(2*iv.pi) - iv.euler
    one, cells = A_bound(iv.mpf(1), T)
    assert one.a <= exact_one.a and exact_one.b <= one.b
    results = {'precision_decimal_digits': dps, 'cutoff': T,
               'tail_bound': f'1/{T}', 'A_one_interval': bracket(one),
               'A_one_exact_interval': bracket(exact_one),
               'A_one_cells': cells, 'metallic_reciprocals': []}
    for m in range(1, 12):
        y = (m + iv.sqrt(m*m + 4)) / 2
        ay, cells = A_bound(y, T)
        derivative = (ay - iv.ln(y)) / (1+y)
        sign = 'positive' if derivative > 0 else 'negative' if derivative < 0 else 'inconclusive'
        assert sign != 'inconclusive'
        results['metallic_reciprocals'].append({
            'm': m, 'y': bracket(y), 'A_interval': bracket(ay),
            'derivative_interval': bracket(derivative), 'sign': sign,
            'integration_cells': cells})
    # Independent finite-integral reciprocity overlaps, including both signs.
    results['reciprocity_controls'] = []
    for m in [1, 3, 10]:
        y = (m + iv.sqrt(m*m + 4)) / 2
        ay, _ = A_bound(y, T)
        ax, _ = A_bound(1/y, T)
        reciprocal = y*ax
        assert ay.a <= reciprocal.b and reciprocal.a <= ay.b
        results['reciprocity_controls'].append({'m': m, 'direct': bracket(ay),
                                                'reciprocal': bracket(reciprocal),
                                                'overlap': True})
    x = iv.sqrt(2)
    h = iv.mpf(1)/10000
    middle, _ = finite_integral(x, 8)
    left, _ = finite_integral(x-h, 8)
    right, _ = finite_integral(x+h, 8)
    convexity = left + right - 2*middle
    assert convexity > 0
    results['finite_cutoff_convexity_control'] = bracket(convexity)
    # For y >= 11: A(y)-log(y) <= C+M/y-0.5*log(y) < 0.
    C = (exact_one + 1)/2
    M = iv.pi**2/36  # zeta(2)/6
    large_bound = C + M/11 - iv.ln(11)/2
    assert large_bound < 0
    results['upper_bound_for_y_at_least_11'] = bracket(large_bound)
    # Symbolic/algebraic identities: check with SymPy if present, otherwise
    # the exact rational-polynomial equality is independently asserted below.
    from fractions import Fraction as Q
    for x in [Q(1,3), Q(2,3), Q(7,3)]:
        A, L, c = Q(2), Q(-1), Q(3)
        phi = ((1-x)*L/2+(1+x)*c/2-A)/(1+x)
        lhs = (A-L/2-c/2+phi)/x
        assert lhs == (A-L)/(1+x)
    results['stationary_identity_rational_algebra_controls'] = 'passed'
    return results


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--cutoff', type=int, default=2048)
    p.add_argument('--dps', type=int, default=40)
    p.add_argument('--output')
    a = p.parse_args()
    if a.cutoff <= 0 or a.dps < 20:
        p.error('positive cutoff and dps >= 20 required')
    result = checks(a.cutoff, a.dps)
    data = json.dumps(result, indent=2) + '\n'
    if a.output:
        Path(a.output).write_text(data)
    else:
        print(data, end='')
