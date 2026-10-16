#!/usr/bin/env python3
"""Exact algebra/group checks and explicitly numerical geometry controls.

Dependencies: mpmath 1.3.0 and SymPy 1.14.0. An optional --runtime PATH adds
a third-party dependency directory; no report or other audit code is read.
Run with -B to avoid bytecode writes. This script writes only its requested
JSON output, and never invokes Git or a network service.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from math import gcd
from pathlib import Path
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--runtime')
parser.add_argument('--output', required=True)
args = parser.parse_args()
if args.runtime:
    sys.path.insert(0, args.runtime)
import mpmath as mp
import sympy as sp

mp.mp.dps = 70


def exact_checks():
    k, t, s = sp.symbols('k t s')
    q = 1-t
    A = (1-k*k*t)/q
    B2 = (1-k*k)/(q*q)
    M, L = B2+k*k, A*A-B2
    cd = (1-2*t+k*k*t*t)/(1-2*k*k*t+k*k*t*t)
    residual = sp.factor(M-2*A*k*s+L*s*s-M*(1-k*s)*(1-k*cd*s))
    assert residual == 0
    focal_root = sp.factor((A-k*k)**2-B2*(1-k*k))
    assert focal_root == 0
    count = 0
    for n in range(3, 201):
        for r in range(1, (n+1)//2):
            if gcd(r, n) != 1:
                continue
            delta = Fraction(r, n)  # K is 1/4 of the real period.
            coeffs = Counter()
            if n == 4:
                seeds = [(Fraction(1, 4), 2), (Fraction(0), -1),
                         (Fraction(1, 2), -1)]
            else:
                seeds = [(Fraction(1, 4), 2),
                         (Fraction(1, 4)+delta, 1),
                         (Fraction(1, 4)-delta, 1),
                         (Fraction(0), -2), (Fraction(1, 2), -2)]
            for j in range(n):
                for x, multiplicity in seeds:
                    coeffs[(x-j*delta) % 1] += multiplicity
            cancels = all(value == 0 for value in coeffs.values())
            assert cancels == (n % 4 == 0), (n, r, coeffs)
            count += 1
    return {
        'one_focus_factorization_residual': str(residual),
        'isotropic_focal_root_residual': str(focal_root),
        'exact_primitive_divisor_cases_N_3_through_200': count,
        'divisor_cancellation_iff_N_divisible_by_4': True,
        'status': 'Exact symbolic algebra and rational group arithmetic; these finite checks supplement the proof.'
    }


def geometry_case(k_text, n, r, scale_text='1'):
    k, scale = mp.mpf(k_text), mp.mpf(scale_text)
    parameter = k*k
    sn = lambda x: mp.ellipfun('sn', x, parameter)
    cn = lambda x: mp.ellipfun('cn', x, parameter)
    dn = lambda x: mp.ellipfun('dn', x, parameter)
    K = mp.ellipk(parameter)
    v = 2*K*r/n
    delta = 2*v
    C, D = cn(v), dn(v)
    alpha, beta, c = scale, scale*mp.sqrt(1-parameter), scale*k
    a, b = alpha*D/C, beta/C
    A, B = a*D/C, b/C
    M = B*B+c*c
    caustic_lambda = a*a-alpha*alpha
    phases = [mp.mpf('0'), K, K/7, -K/3, 2*K+K/11, v, K+v]
    max_intersection_error = mp.mpf(0)
    max_chord_error = mp.mpf(0)
    max_factor_error = mp.mpf(0)
    min_scaled_det = mp.inf
    logs_plus, logs_minus = [], []
    for phase in phases:
        log_plus = mp.mpf(0)
        log_minus = mp.mpf(0)
        for j in range(n):
            u = phase+j*delta
            wm, wp = u-v, u+v
            p0 = (a*sn(wm), b*cn(wm))
            p1 = (a*sn(wp), b*cn(wp))
            nx0, ny0 = p0[0]/(a*a), p0[1]/(b*b)
            nx1, ny1 = p1[0]/(a*a), p1[1]/(b*b)
            determinant = nx0*ny1-nx1*ny0
            min_scaled_det = min(min_scaled_det, abs(determinant*a*b))
            qx, qy = (ny1-ny0)/determinant, (nx0-nx1)/determinant
            expected = (A*sn(u), B*cn(u))
            max_intersection_error = max(max_intersection_error,
                abs(qx-expected[0])/max(a, b),
                abs(qy-expected[1])/max(a, b))
            # Independent support-function test of the actual chord line.
            chord_x, chord_y = p1[1]-p0[1], p0[0]-p1[0]
            chord_c = chord_x*p0[0]+chord_y*p0[1]
            tangency = alpha*alpha*chord_x*chord_x+beta*beta*chord_y*chord_y
            max_chord_error = max(max_chord_error,
                abs(tangency-chord_c*chord_c)/max(abs(tangency), abs(chord_c*chord_c)))
            fp = (qx-c)**2+qy*qy
            fm = (qx+c)**2+qy*qy
            factor = M*(1-k*sn(u))*(1-k*cn(delta)/dn(delta)*sn(u))
            max_factor_error = max(max_factor_error, abs(fp-factor)/fp)
            assert fp > 0 and fm > 0 and determinant != 0
            log_plus += mp.log(fp)/2
            log_minus += mp.log(fm)/2
        logs_plus.append(log_plus)
        logs_minus.append(log_minus)
    spread = max(logs_plus)-min(logs_plus)
    foci_error = max(abs(x-y) for x, y in zip(logs_plus, logs_minus))
    if n % 4 == 0:
        assert spread < mp.mpf('1e-40'), (k_text, n, r, spread)
        assert foci_error < mp.mpf('1e-40')
    assert max_intersection_error < mp.mpf('1e-40')
    assert max_chord_error < mp.mpf('1e-40')
    assert max_factor_error < mp.mpf('1e-40')
    assert 0 < caustic_lambda < b*b
    out = {
        'k': k_text, 'N': n, 'primitive_rotation': r, 'scale': scale_text,
        'phase_count': len(phases), 'positive_finite_distances': True,
        'log_product_plus_at_phase_0': mp.nstr(logs_plus[0], 36),
        'log_product_phase_spread': mp.nstr(spread, 8),
        'max_same_phase_two_focus_log_difference': mp.nstr(foci_error, 8),
        'max_direct_tangent_intersection_relative_error': mp.nstr(max_intersection_error, 8),
        'max_direct_caustic_tangency_relative_error': mp.nstr(max_chord_error, 8),
        'max_one_focus_factor_relative_error': mp.nstr(max_factor_error, 8),
        'min_absolute_tangent_determinant_times_ab': mp.nstr(min_scaled_det, 8),
        'lambda_over_b_squared': mp.nstr(caustic_lambda/(b*b), 16),
    }
    if n == 4:
        exact_value = 4*a*a*b*b
        out['N4_product_relative_error_against_4_a_squared_b_squared'] = mp.nstr(
            abs(mp.exp(logs_plus[0])-exact_value)/exact_value, 8)
        assert abs(mp.exp(logs_plus[0])-exact_value)/exact_value < mp.mpf('1e-40')
    return out


result = {
    'created_utc': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
    'versions': {'mpmath': mp.__version__, 'sympy': sp.__version__, 'decimal_digits': mp.mp.dps},
    'classification': 'Exact finite algebra/group checks plus unvalidated high-precision numerical controls. Numerical values are not interval certificates or a proof.',
    'exact': exact_checks(),
    'positive_cases': [],
    'negative_parity_controls': [],
}
for n in [4, 8, 12, 16, 20, 24]:
    for r in range(1, n//2):
        if gcd(r, n) != 1:
            continue
        for k in ['0.2', '0.8', '0.9999']:
            result['positive_cases'].append(geometry_case(k, n, r))
for k, n, r in [('0.000000000001', 8, 3),
                ('0.99999999999999999999', 12, 5)]:
    result['positive_cases'].append(geometry_case(k, n, r))
for scale in ['1e-20', '1e20']:
    result['positive_cases'].append(geometry_case('0.8', 8, 3, scale))
for n, r in [(3, 1), (5, 1), (5, 2), (6, 1), (7, 3), (10, 3), (14, 5)]:
    item = geometry_case('0.8', n, r)
    assert mp.mpf(item['log_product_phase_spread']) > mp.mpf('1e-15')
    result['negative_parity_controls'].append(item)
result['counts'] = {'positive_cases': len(result['positive_cases']),
                    'negative_parity_controls': len(result['negative_parity_controls'])}
Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'counts': result['counts'], 'exact': result['exact']}, indent=2))
