#!/usr/bin/env python3
"""New exact formal-series and finite rearrangement controls; not a proof certificate.

Distinct from shipped disk/quadrature/scalar-mesh programs: a bivariate formal
algebra checks which quasiconformal theorem gives the exact infinitesimal
coefficient, a rational logarithm-series enclosure checks the far kernel, and
exhaustive finite removal budgets check the direction of the sharpness exchange.
Universal analytic reasoning remains necessary. No numerical third-party code.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path

N = 5


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def add(a, b):
    out = dict(a)
    for key, value in b.items():
        out[key] = out.get(key, Q(0)) + value
    return {key: value for key, value in out.items() if value}


def scale(a, value):
    return {key: value * coefficient for key, coefficient in a.items()
            if value * coefficient}


def mul(a, b):
    out = {}
    for (r, ell), c in a.items():
        for (s, m), d in b.items():
            if r + s <= N:
                key = r + s, ell + m
                out[key] = out.get(key, Q(0)) + c * d
    return {key: value for key, value in out.items() if value}


def exp_zero(a):
    require((0, 0) not in a, 'formal exponential needs zero constant')
    out, power = {(0, 0): Q(1)}, {(0, 0): Q(1)}
    for k in range(1, N + 1):
        power = mul(power, a)
        out = add(out, scale(power, Q(1, math.factorial(k))))
    return out


def first(a):
    return {ell: c for (r, ell), c in a.items() if r == 1}


def serial(a):
    return {str(r) + ',' + str(ell): str(c) for (r, ell), c in sorted(a.items())}


def log_bounds(q, terms):
    require(0 <= q < 1 and terms > 0, 'log series domain')
    lo = sum((q**k / k for k in range(1, terms + 1)), Q(0))
    hi = lo + q**(terms + 1) / ((terms + 1) * (1 - q))
    return lo, hi


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mutant', choices=['none', 'general_coefficient',
                                            'missing_angular_factor', 'wrong_budget'],
                        default='none')
    args = parser.parse_args()
    # K=(1+r)/(1-r), inverse K=(1-r)/(1+r), ell=log(pi/a).
    inverse_k = {(0, 0): Q(1)}
    inverse_k.update({(j, 0): Q(2 * (-1)**j) for j in range(1, N + 1)})
    k = {(0, 0): Q(1)}
    k.update({(j, 0): Q(2) for j in range(1, N + 1)})
    require(mul(k, inverse_k) == {(0, 0): Q(1)}, 'K inverse identity')
    one_minus_inverse = add({(0, 0): Q(1)}, scale(inverse_k, -1))
    special_log = {(r, ell + 1): c for (r, ell), c in one_minus_inverse.items()}
    special = exp_zero(special_log)
    log_k = {(j, 0): Q(2, j) for j in range(1, N + 1, 2)}
    general_original = mul(k, special)
    general_corrected = mul(exp_zero(mul(inverse_k, log_k)), special)
    require(first(general_original) == {0: Q(2), 1: Q(2)}, 'original combined coefficient')
    require(first(general_corrected) == {0: Q(2), 1: Q(2)}, 'corrected combined coefficient')
    oracle = {1: Q(2)}
    if args.mutant == 'general_coefficient':
        oracle = first(general_corrected)
    require(first(special) == oracle, 'special conformal-on-E coefficient has no extra area term')
    # Cross-check the whole formal exponential by its differential equation.
    derivative = {(r - 1, ell): r * c for (r, ell), c in special.items() if r}
    log_derivative = {(r - 1, ell): r * c for (r, ell), c in special_log.items() if r}
    rhs = {key: value for key, value in mul(special, log_derivative).items() if key[0] < N}
    require(derivative == rhs, 'formal exponential derivative identity')

    # Far kernel divided by pi equals sum q^k/k, q=R^2/rho^2.
    # Expanding angular |1-s exp(it)|^-2 gives only paired powers; radial
    # integration changes coefficient 2/(2j+2) into 1/(j+1).
    for j in range(40):
        angular_factor = Q(1) if args.mutant == 'missing_angular_factor' else Q(2)
        require(angular_factor / (2*j+2) == Q(1, j+1), 'angular/radial coefficient normalization')
    kernel = []
    for q in [Q(0), Q(1, 10**30), Q(1, 16), Q(1, 4), Q(1, 2)]:
        lo, hi = log_bounds(q, 96)
        coarse_lo, coarse_hi = log_bounds(q, 48)
        require(coarse_lo <= lo <= hi <= coarse_hi, 'nested rational logarithm bounds')
        require(hi - lo <= Q(1, 10**29), 'far series remainder too large')
        # q<=1/2 makes every coefficient no greater than at q=1/2.
        require(lo <= log_bounds(Q(1, 2), 96)[0], 'far cutoff monotonicity')
        kernel.append({'q': str(q), 'lower': str(lo), 'upper': str(hi)})

    # A finite exact rearrangement model: eight unit-area inner cells have
    # density >=1, eight outer cells density <=1. Remove at most eight cells.
    # The inner-disk choice minimizes remaining weight, even for disconnected
    # removed sets. This finite model does not establish the continuum theorem.
    inner = [Q(9-i, 8-i) for i in range(8)]
    outer = [Q(8-i, 9-i) for i in range(8)]
    values = inner + outer
    inner_total = sum(inner, Q(0))
    budget = 9 if args.mutant == 'wrong_budget' else 8
    tested, minimum_margin = 0, None
    for size in range(budget + 1):
        for subset in itertools.combinations(range(16), size):
            removed = sum((values[j] for j in subset), Q(0))
            margin = inner_total - removed
            require(margin >= 0, 'sharpness exact-area removal budget')
            tested += 1
            minimum_margin = margin if minimum_margin is None else min(minimum_margin, margin)
    require(minimum_margin == 0, 'sharpness equality at inner choice')
    print(json.dumps({'status': 'PASS', 'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'formal_order': N, 'special_expansion': serial(special),
                      'general_corrected_expansion': serial(general_corrected),
                      'kernel_series_terms': 96, 'kernel_cases': kernel,
                      'finite_removal_configurations': tested, 'minimum_margin': str(minimum_margin),
                      'limitations': 'Exact finite arithmetic checks; universal analytic proof and imported theorems still required.'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
