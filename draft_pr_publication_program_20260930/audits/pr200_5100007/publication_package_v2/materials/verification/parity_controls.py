"""Portable adaptation of the independently authored parity audit; explicit guards survive -O.
No novel independence claim is made for this package adaptation.
"""
"""Independent finite controls; these computations are not the universal proof."""
from pathlib import Path
import sys
import math
import json
from fractions import Fraction
from collections import Counter
import mpmath as mp
import sympy as sp
mp.mp.dps = 100
import argparse
_parser=argparse.ArgumentParser()
_parser.add_argument('--output-dir',default='replay-results')
_parser.add_argument('--self-test-failure',action='store_true')
_args=_parser.parse_args()
ROOT=Path(_args.output_dir).resolve()
ROOT.mkdir(parents=True,exist_ok=True)
if _args.self_test_failure:
    raise RuntimeError('deliberate explicit-guard failure')


def exact_checks():
    kappa, t, S = sp.symbols('kappa t S')
    q = 1 - t
    U, V = (1 - 2 * kappa * t + kappa * t * t, 1 - 2 * t + kappa * t * t)
    expression = (U + kappa * V * S) ** 2 - 4 * kappa * (1 - kappa * t) ** 2 * q * q * S
    if not sp.expand(expression - (1 - kappa * S) * (U * U - kappa * V * V * S)) == 0:
        raise RuntimeError('parity check failed at source-audit line 20: sp.expand(expression - (1 - kappa * S) * (U * U - kappa * V * V * S)) == 0')
    if not sp.expand(U + V - 2 * q * (1 - kappa * t)) == 0:
        raise RuntimeError('parity check failed at source-audit line 21: sp.expand(U + V - 2 * q * (1 - kappa * t)) == 0')
    checked = 0
    for N in range(3, 101):
        for tau in range(1, (N + 1) // 2):
            if math.gcd(N, tau) != 1:
                continue
            delta = Fraction(2 * tau, N)
            L = N // math.gcd(N, 2)
            G = {j * delta % 1 for j in range(L)}
            if not len(G) == L:
                raise RuntimeError('parity check failed at source-audit line 31: len(G) == L')
            half_in_G = Fraction(1, 2) in G
            if not half_in_G == (N % 4 == 0):
                raise RuntimeError('parity check failed at source-audit line 33: half_in_G == (N % 4 == 0)')
            exceptional = delta == Fraction(1, 2)
            if not exceptional == (N == 4):
                raise RuntimeError('parity check failed at source-audit line 35: exceptional == (N == 4)')
            divisor = Counter()
            for j in range(L):
                shift = -j * delta
                divisor[shift % 1] -= 2 if exceptional else 4
                divisor[(Fraction(1, 2) + shift) % 1] += 2
                if not exceptional:
                    divisor[(Fraction(1, 2) + delta + shift) % 1] += 1
                    divisor[(Fraction(1, 2) - delta + shift) % 1] += 1
            divisor = {x: order for x, order in divisor.items() if order}
            if not (not divisor) == (N % 4 == 0):
                raise RuntimeError('parity check failed at source-audit line 45: (not divisor) == (N % 4 == 0)')
            if N % 4:
                if not len(divisor) == 2 * L:
                    raise RuntimeError('parity check failed at source-audit line 47: len(divisor) == 2 * L')
                if not sorted(divisor.values()) == [-4] * L + [4] * L:
                    raise RuntimeError('parity check failed at source-audit line 48: sorted(divisor.values()) == [-4] * L + [4] * L')
            checked += 1
    return {'symbolic_factorization': 'exact zero residual', 'rational_divisor_cases_N_3_to_100': checked}

def geometry(k, N, tau):
    parameter = k * k
    K = mp.ellipk(parameter)
    v = 2 * K * tau / N
    sn = lambda x: mp.ellipfun('sn', x, parameter)
    cn = lambda x: mp.ellipfun('cn', x, parameter)
    dn = lambda x: mp.ellipfun('dn', x, parameter)
    C, D = (cn(v), dn(v))
    alpha, beta = (mp.mpf(1), mp.sqrt(1 - parameter))
    a, b, c = (alpha * D / C, beta / C, k)
    Ao, Bo = (a * D / C, b / C)
    delta = 2 * v
    max_residual = mp.mpf(0)

    def outer(u):
        nonlocal max_residual
        l, r = (u - v, u + v)
        aa, bb, cc, dd = (-sn(l) / a, cn(l) / b, -sn(r) / a, cn(r) / b)
        determinant = aa * dd - bb * cc
        x, y = ((dd - bb) / determinant, (aa - cc) / determinant)
        expected = (-Ao * sn(u), Bo * cn(u))
        scale = max(1, abs(x), abs(y))
        max_residual = max(max_residual, abs(x - expected[0]) / scale, abs(y - expected[1]) / scale)
        return (x, y)

    def products(u):
        lp, lm = (mp.mpf(0), mp.mpf(0))
        for j in range(N):
            x, y = outer(u + j * delta)
            lp += mp.log((x - c) ** 2 + y * y) / 2
            lm += mp.log((x + c) ** 2 + y * y) / 2
        return (lp, lm)
    phases = [K * mp.mpf(i) / 13 for i in range(13)]
    values = [products(u) for u in phases]
    plus = [p for p, _ in values]
    minus = [m for _, m in values]
    spread_p = mp.expm1(max(plus) - min(plus))
    spread_m = mp.expm1(max(minus) - min(minus))
    shifted = products(phases[3] + 2 * K)
    phase_swap_error = max(abs(shifted[0] - values[3][1]), abs(shifted[1] - values[3][0]))
    if N % 4 == 0:
        if not spread_p < mp.mpf('1e-85'):
            raise RuntimeError("parity check failed at source-audit line 97: spread_p < mp.mpf('1e-85')")
        if not spread_m < mp.mpf('1e-85'):
            raise RuntimeError("parity check failed at source-audit line 98: spread_m < mp.mpf('1e-85')")
    else:
        if not spread_p > mp.mpf('1e-70'):
            raise RuntimeError("parity check failed at source-audit line 101: spread_p > mp.mpf('1e-70')")
        if not spread_m > mp.mpf('1e-70'):
            raise RuntimeError("parity check failed at source-audit line 102: spread_m > mp.mpf('1e-70')")
    if not phase_swap_error < mp.mpf('1e-85'):
        raise RuntimeError("parity check failed at source-audit line 103: phase_swap_error < mp.mpf('1e-85')")
    if not max_residual < mp.mpf('1e-85'):
        raise RuntimeError("parity check failed at source-audit line 104: max_residual < mp.mpf('1e-85')")
    return {'k': str(k), 'N': N, 'tau': tau, 'relative_phase_spread_focus_plus': mp.nstr(spread_p, 15), 'relative_phase_spread_focus_minus': mp.nstr(spread_m, 15), 'tangent_formula_max_relative_residual': mp.nstr(max_residual, 8), 'antipodal_phase_swap_max_log_error': mp.nstr(phase_swap_error, 8)}
if __name__ == '__main__':
    results = {'precision_decimal_digits': mp.mp.dps, 'mpmath_version': mp.__version__, 'sympy_version': sp.__version__, 'exact': exact_checks(), 'numeric': []}
    for k_text in ('0.3', '0.8', '0.97'):
        for N in range(3, 17):
            for tau in range(1, (N + 1) // 2):
                if math.gcd(N, tau) == 1:
                    results['numeric'].append(geometry(mp.mpf(k_text), N, tau))
    destination = ROOT / 'parity_controls_results.json'
    destination.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps({'exact': results['exact'], 'numeric_cases': len(results['numeric']), 'result_file': destination.name}, indent=2))
