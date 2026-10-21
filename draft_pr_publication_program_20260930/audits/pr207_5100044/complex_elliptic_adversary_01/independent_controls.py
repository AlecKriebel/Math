#!/usr/bin/env python3
"""Independent diagnostics; no submitted checker is imported or read.

Requires sympy==1.14.0 and mpmath==1.3.0. Exact controls check local algebra
and finite lattice indexing. Floating controls cannot certify the theorem.
"""
from datetime import datetime, timezone
from fractions import Fraction
from math import gcd
from pathlib import Path
import hashlib
import json
import platform
import sympy as sp
import mpmath as mp


def exact_controls():
    k, t, s, x, y = sp.symbols('k t s x y')
    q = 1-t
    d2 = 1-k*k*t
    D = 1-k*k*t*s*s
    U = 1-2*k*k*t+k*k*t*t
    V = 1-2*t+k*k*t*t
    W = 1-k*k*t*t
    checks = {
        'distance_product_factorization': sp.expand(
            d2*D+2*k*s*q*d2+k*k*q*(s*s-t)
            -(1+k*s)*(U+k*V*s)),
        'sum_U_V': sp.expand(U+V-2*q*d2),
        'difference_U_V': sp.expand(U-V-2*t*(1-k*k)),
        'positive_discriminant': sp.expand(U*U-k*k*V*V-(1-k*k)*W*W),
        'antipodal_fraction_addition': sp.cancel(
            1/((1+k*s)*(U+k*V*s)**2)
            +1/((1-k*s)*(U-k*V*s)**2)
            -2*(U*U+k*k*V*(V+2*U)*s*s)
            /((1-k*k*s*s)*(U*U-k*k*V*V*s*s)**2)),
        'shifted_denominator_factor': sp.expand(
            (1-k*k*y)*(1-x)-(1-y)*(1-k*k*x)
            -(1-k*k)*(y-x)),
        'N4_decomposition': sp.expand(
            1-k*k*t*s*s-((1-t)+t*(1-k*k*s*s))),
    }
    assert all(value == 0 for value in checks.values()), checks
    # Finite indexing only: the proof of arbitrary order is the modular argument
    # in DERIVATION.md. These controls target accidental pole coalescence.
    cases = 0
    for N in range(4, 401, 4):
        m = N//2
        for tau in range(1, N//2):
            if gcd(tau, N) != 1:
                continue
            cases += 1
            assert tau % 2 == 1 and gcd(tau, m) == 1
            assert sorted((j*tau) % m for j in range(m)) == list(range(m))
            assert (Fraction(m+tau, 2) % 1) == Fraction(1, 2)
            exceptional = 2*tau == m
            assert exceptional == (N == 4 and tau == 1)
            if not exceptional:
                assert len({0, 1, m-1}) == 3
                assert [(j*tau) % m for j in range(m)].count(tau % m) == 1
                assert [(j*tau) % m for j in range(m)].count((-tau) % m) == 1
    return {'polynomial_and_rational_identities': list(checks),
            'cyclic_index_cases': cases, 'cyclic_index_max_N': 400}


def shoelace(points):
    return mp.fsum(points[i][0]*points[(i+1) % len(points)][1]
                   -points[i][1]*points[(i+1) % len(points)][0]
                   for i in range(len(points)))/2


def diagnostic(N, tau, k_text, phases=('0', '0.037', '0.219', '0.583')):
    k = mp.mpf(k_text)
    K = mp.ellipk(k*k)
    v = 2*K*tau/N
    sn = lambda z: mp.ellipfun('sn', z, k*k)
    cn = lambda z: mp.ellipfun('cn', z, k*k)
    dn = lambda z: mp.ellipfun('dn', z, k*k)
    alpha = mp.mpf('1.371')
    beta = alpha*mp.sqrt(1-k*k)
    a, b, c = alpha*dn(v)/cn(v), beta/cn(v), alpha*k
    delta = 2*v
    h, q = sn(v), cn(v)**2
    U, V = 1-2*k*k*h*h+k*k*h**4, 1-2*h*h+k*k*h**4
    C = b*h*dn(v)*q*q/alpha**3
    C_A = a*b*sn(v)*cn(v)/dn(v)
    B = lambda u: 2*C*(1-k*k*h*h*sn(u)**2)*(U*U+k*k*V*(V+2*U)*sn(u)**2)/(dn(u)*(U*U-k*k*V*V*sn(u)**2)**2)
    m = N//2
    S = lambda u: mp.fsum(dn(u+j*delta) for j in range(m))
    R = lambda u: mp.fsum(B(u+j*delta) for j in range(m))
    products, focus_errors, area_errors, inverse_errors, ratio_values = [], [], [], [], []
    for phase in phases:
        w = 4*K*mp.mpf(phase)
        pts = [(-a*sn(w+j*delta), b*cn(w+j*delta)) for j in range(N)]
        area = shoelace(pts)
        inv_areas = []
        for focus in (c, -c):
            inverse = []
            for px, py in pts:
                dist2 = (px-focus)**2+py*py
                inverse.append(((px-focus)/dist2, py/dist2))
            inv_area = shoelace(inverse)
            assert abs(shoelace(list(reversed(inverse)))+inv_area) < mp.mpf('1e-75')*max(1, abs(inv_area))
            inv_areas.append(inv_area)
        products.append(area*inv_areas[0])
        focus_errors.append(abs(inv_areas[0]-inv_areas[1])/max(1, abs(inv_areas[0])))
        area_errors.append(abs(area-2*C_A*S(w))/max(1, abs(area)))
        inverse_errors.append(abs(inv_areas[0]-R(w+v))/max(1, abs(inv_areas[0])))
        ratio_values.append(R(w)/S(w+K))
    spread = (max(products)-min(products))/max(1, max(abs(p) for p in products))
    ratio_spread = (max(ratio_values)-min(ratio_values))/max(1, max(abs(p) for p in ratio_values))
    return {
        'N': N, 'tau': tau, 'k': k_text, 'primitive': gcd(N,tau)==1,
        'sample_product': mp.nstr(products[0], 30),
        'relative_product_spread': mp.nstr(spread, 8),
        'max_relative_focus_error': mp.nstr(max(focus_errors), 8),
        'max_relative_area_formula_error': mp.nstr(max(area_errors), 8),
        'max_relative_inverse_formula_error': mp.nstr(max(inverse_errors), 8),
        'relative_proportionality_spread': mp.nstr(ratio_spread, 8),
    }


def laurent_diagnostic(N, tau, k_text):
    k = mp.mpf(k_text)
    K, Kp = mp.ellipk(k*k), mp.ellipk(1-k*k)
    p, r = 1j*Kp, K+1j*Kp
    v, delta, m = 2*K*tau/N, 4*K*tau/N, N//2
    sn = lambda z: mp.ellipfun('sn', z, k*k)
    cn = lambda z: mp.ellipfun('cn', z, k*k)
    dn = lambda z: mp.ellipfun('dn', z, k*k)
    t, q = sn(v)**2, cn(v)**2
    U, V = 1-2*k*k*t+k*k*t*t, 1-2*t+k*k*t*t
    # Common positive scale C is immaterial to the divisor and cancellation.
    if N == 4:
        B = lambda u: 2/U**2*(q/dn(u)+t*dn(u))
    else:
        B = lambda u: 2*(1-k*k*t*sn(u)**2)*(U*U+k*k*V*(V+2*U)*sn(u)**2)/(dn(u)*(U*U-k*k*V*V*sn(u)**2)**2)
    R = lambda u: mp.fsum(B(u+j*delta) for j in range(m))
    S = lambda u: mp.fsum(dn(u+j*delta) for j in range(m))
    eps = mp.mpf('1e-12')
    second = lambda f,a: eps**2*(f(a+eps)+f(a-eps))/2
    first = lambda f,a: eps*(f(a+eps)-f(a-eps))/2
    Rsecond = second(R,r)
    Sres = first(lambda u:S(u+K),r)
    assert abs(Rsecond) < mp.mpf('1e-20')
    assert abs(Sres+1j) < mp.mpf('1e-20')
    row = {'N':N,'tau':tau,'k':k_text,'epsilon':str(eps),
           'R_symmetric_second_coefficient':mp.nstr(Rsecond,15),
           'S_shifted_residue':mp.nstr(Sres,15)}
    if N != 4:
        plus, minus = second(B,r+delta), second(B,r-delta)
        residue_error = abs(first(B,r+delta)-first(B,r-delta))
        assert abs(plus+minus) < mp.mpf('1e-60')*max(1,abs(plus))
        assert residue_error < mp.mpf('1e-60')
        row.update({'B_plus_second_coefficient':mp.nstr(plus,15),
                    'B_minus_second_coefficient':mp.nstr(minus,15),
                    'double_coefficient_cancellation_error':mp.nstr(abs(plus+minus),8),
                    'residue_matching_error':mp.nstr(residue_error,8)})
    return row


def main():
    mp.mp.dps = 100
    specs = [(4,1,'0.7'), (8,1,'0.7'), (8,3,'0.7'),
             (12,5,'0.7'), (20,3,'0.93'), (20,9,'0.93'),
             (28,13,'0.999999'), (40,19,'0.000001'),
             (60,29,'0.9999')]
    cases = [diagnostic(*spec) for spec in specs]
    for row in cases:
        assert mp.mpf(row['relative_product_spread']) < mp.mpf('1e-70'), row
        assert mp.mpf(row['relative_proportionality_spread']) < mp.mpf('1e-70'), row
        for field in ('max_relative_focus_error', 'max_relative_area_formula_error',
                      'max_relative_inverse_formula_error'):
            assert mp.mpf(row[field]) < mp.mpf('1e-70'), row
    # Wrong parity and a repeated shorter orbit are outside the theorem.
    controls = [diagnostic(6,1,'0.93'), diagnostic(12,2,'0.93')]
    assert all(mp.mpf(row['relative_product_spread']) > mp.mpf('1e-5') for row in controls)
    data = {'utc': datetime.now(timezone.utc).isoformat(),
            'python': platform.python_version(), 'sympy': sp.__version__,
            'mpmath': mp.__version__, 'mpmath_dps': mp.mp.dps,
            'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'exact': exact_controls(), 'diagnostic_cases': cases,
            'laurent_diagnostics': [laurent_diagnostic(N,tau,'0.7')
                                    for N,tau in [(4,1),(8,1),(8,3),(12,5)]],
            'negative_controls': controls,
            'interpretation': 'Exact local controls and noncertified high precision diagnostics; universal justification is DERIVATION.md.'}
    target = Path(__file__).with_name('independent_output.json')
    target.write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
