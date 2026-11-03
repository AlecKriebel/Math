"""Reproducible exact polynomial identities and numeric checks; not a full unit enumeration."""
import json, math
from pathlib import Path
import sympy as s
import mpmath as mp
x = s.symbols('x')
results = []
for n in [1, 2, 3, 4, 6, 12, 156]:
    f = s.Poly(x ** (2 * n) - x ** n - 1, x)
    rem = lambda p: s.rem(s.Poly(p, x), f).is_zero
    if not rem(x * (x ** (2 * n - 1) - x ** (n - 1)) - 1):
        raise AssertionError()
    divs = s.divisors(n)
    for m in divs:
        q = n // m
        t = x ** m
        S = sum((t ** j for j in range(q)))
        if not rem((t - 1) * x ** n * S - 1):
            raise AssertionError()
        if q % 2:
            A = sum(((-1) ** j * t ** j for j in range(q)))
            if not rem((1 + t) * (x ** n - 1) ** 2 * A - 1):
                raise AssertionError()
        else:
            A = sum(((-1) ** (q - 1 - j) * t ** j for j in range(q)))
            if not rem((1 + t) * x ** n * A - 1):
                raise AssertionError()
    results.append({'n': n, 'inverse_identity': True, 'divisor_units_verified': 2 * len(divs)})
mp.mp.dps = 80
n = 156
a = mp.log((1 + mp.sqrt(5)) / 2)
vals = {'n': n, 'degree': 2 * n, 'unit_rank': n, 'a': a, 'house': mp.exp(a / n), 'height': a / (2 * n), 'Mahler': mp.exp(a), 'Minkowski_length': mp.sqrt(2 * n * mp.cosh(2 * a / n)), 'torsion_Minkowski_length': mp.sqrt(2 * n), 'Minkowski_baseline_ratio': mp.sqrt(mp.cosh(2 * a / n)), 'sqrt2_log_length': mp.sqrt(2 * n) * a / n, 'weight2_log_length': mp.sqrt(4 * n - 2) * a / n}
vals = {k: mp.nstr(v, 65) if isinstance(v, mp.mpf) else v for k, v in vals.items()}
checks = []
for n in [1, 2, 3, 4, 6]:
    alpha = ((1 + s.sqrt(5)) / 2) ** s.Rational(1, n)
    for k in range(1, n + 2):
        actual = s.degree(s.minpoly(alpha ** k, x), x)
        expected = 2 * n // math.gcd(n, k)
        if not actual == expected:
            raise AssertionError((n, k, actual, expected))
        checks.append({'n': n, 'k': k, 'degree': int(actual)})
out = {'symbolic_identity_checks': results, 'numeric_values_not_interval_certificates': vals, 'small_degree_power_checks': checks, 'scope': 'Exact identities and sample degrees plus high precision approximations; not an all-unit shortest-vector or maximal-order computation.'}
p = Path(__file__).with_name('exact_checks.json')
p.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
