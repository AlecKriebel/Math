"""Stable high-precision boundary controls; exponentials represented by logarithms."""
from decimal import Decimal, getcontext, ROUND_CEILING
from fractions import Fraction
import json
from pathlib import Path
getcontext().prec = 90
D = Decimal

def ceil(x):
    return int(x.to_integral_value(rounding=ROUND_CEILING))

def params(e):
    used = min(e, Fraction(1, 8))
    ed = D(used.numerator) / D(used.denominator)
    h = 6 * used.denominator // used.numerator + 1
    ell = ceil(D(2) / ed * (D(12).ln() + D(h) * D(3).ln()))
    r = h * ell
    N = 12 * r * r
    M = ceil(D(N) * (D(3) * D(N)).ln())
    if not Fraction(h) > 6 / used:
        raise AssertionError('verification failed at original line 19')
    if not M >= 2 * r:
        raise AssertionError('verification failed at original line 20')
    if not -ed * D(ell) / 2 <= -D(12).ln() - D(h) * D(3).ln():
        raise AssertionError('verification failed at original line 22')
    if not Fraction(r * r, N) == Fraction(1, 12):
        raise AssertionError('verification failed at original line 24')
    if not D(N).ln() - D(M) / D(N) <= -D(3).ln():
        raise AssertionError('verification failed at original line 26')
    return dict(epsilon=str(e), used_epsilon=str(used), h=h, ell=ell, r=r, N=N, M=M, log_coupon_failure_bound=str(D(N).ln() - D(M) / D(N)), queries_at_most=M * (M - 1) // 2, total_calls_at_most=M * (M + 1) // 2)
values = [Fraction(1, 8), Fraction(1, 8) - Fraction(1, 10 ** 12), Fraction(1, 8) + Fraction(1, 10 ** 12), Fraction(1, 9), Fraction(1, 16), Fraction(1, 100), Fraction(1, 10 ** 6), Fraction(1, 10 ** 12), Fraction(1), Fraction(2)]
from math import comb
coupon = []
for n in range(1, 11):
    for m in (1, n, 2 * n, 5 * n):
        unseen = 1 - sum((Fraction((-1) ** j * comb(n, j) * (n - j) ** m, n ** m) for j in range(n + 1)))
        bound = n * Fraction((n - 1) ** m, n ** m)
        if not 0 <= unseen <= bound:
            raise AssertionError('verification failed at original line 41')
        coupon.append(dict(n=n, m=m, missing_probability=str(unseen), union_bound=str(bound)))
result = {'parameter_cases': [params(e) for e in values], 'exact_coupon_cases': coupon, 'result': 'PASS'}
Path(__file__).with_name('parameter_results.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: 10 high-precision parameter cases and 40 exact coupon-collector cases')
print('epsilon=1/8:', json.dumps(result['parameter_cases'][0], indent=2))
