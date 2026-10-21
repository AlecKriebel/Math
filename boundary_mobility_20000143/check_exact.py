"""Finite exact-integer regression checks; not geometric proofs."""
import json, math
from fractions import Fraction
from pathlib import Path
f = lambda s: (s + 1) * (s + 2) // 2
h = lambda r, s: (r + 1) * f(s)
hq = lambda d: (d + 1) * (d + 2) ** 2 * (d + 3) // 12
counts = {}
n = 0
for R in range(1, 41):
    for S in range(1, 41):
        for i in range(R + 1):
            for j in range(S + 1):
                if (i, j) in [(0, 0), (R, S)]:
                    continue
                if not h(i, j) + h(R - i, S - j) <= h(R, S):
                    raise AssertionError()
                n += 1
counts['product_pencil_splits'] = n
n = 0
for d in range(2, 301):
    for e in range(1, d):
        if not hq(e) + hq(d - e) <= hq(d):
            raise AssertionError()
        n += 1
counts['quadric_pencil_splits'] = n
n = 0
for a in range(1, 16):
    for b in range(1, 16):
        for m in range(1, 201):
            s = math.isqrt(m * a)
            r = m * b // (2 * s)
            if r < 1:
                continue
            if not (0 <= m * a - s * s and 0 <= m * b - 2 * r * s):
                raise AssertionError()
            B = h(r, s) - 2 + (m * a - s * s) + 2 * (m * b - 2 * r * s)
            if not B >= 0:
                raise AssertionError()
            n += 1
counts['mixed_rounding_cases'] = n
for a in range(1, 20):
    for b in range(1, 20):
        for d in range(1, 20):
            m = 4 * a * d * d
            r = b * d
            s = 2 * a * d
            if not (s * s == m * a and 2 * r * s == m * b):
                raise AssertionError()
            if not h(r, s) - 2 == (b * d + 1) * f(2 * a * d) - 2:
                raise AssertionError()
counts['square_subsequence_class_checks'] = 19 ** 3
for u in range(1, 31):
    for v in range(1, 31):
        for m in range(1, 101):
            d = math.isqrt(m * min(u, v))
            if not (m * u - d * d >= 0 and m * v - d * d >= 0):
                raise AssertionError()
counts['quadric_rounding_cases'] = 30 * 30 * 100
N = 300
best = [0] * (N + 1)
for m in range(1, N + 1):
    best[m] = max((best[m - d * e] + min(f(d) - 1, f(e) - 1) for d in range(1, m + 1) for e in range(1, m // d + 1)))
    if not best[m] == 2 * m:
        raise AssertionError()
counts['product_component_budget_dp'] = N
out = {'status': 'PASS', 'scope': 'Finite arithmetic checks only. Geometric proofs are in REPORT.md.', 'checks': counts, 'examples': {'mixed_a_b_d_1': h(1, 2) - 2, 'quadric_d_1': hq(1) - 2, 'mixed_m_10000_a_b_1': h(50, 100) - 2}}
Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
