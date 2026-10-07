"""Preserved targeted Python check executed during the upstream adversarial audit.

Reformatted from the tool command after execution; this receipt was not rerun.
No source writes are performed by this script. The finite local sums use
floating-complex arithmetic, so this is consistency evidence, not a proof.
"""

import json, hashlib, pathlib, cmath
from fractions import Fraction as F

root = pathlib.Path('/Users/alec/Desktop/math')
manifest = json.loads(pathlib.Path('/Users/alec/Documents/Math/openai_followon_finite_fields/sources/SOURCE_MANIFEST.json').read_text())
paths = [e for e in manifest['files'] if 'Prime-Fields-October-4-2026/build/' in e['path'] or 'integer-base-October-4-2026/build/sections/' in e['path'] or e['path'] == 'lean/docs/003.md']
miss = []
for e in paths:
    if hashlib.sha256((root / e['path']).read_bytes()).hexdigest() != e['sha256']:
        miss.append(e['path'])
print({'manifest_source_hashes_checked': len(paths), 'mismatches': miss})

Q = 13
gen = 2
logs = {pow(gen, k, Q): k for k in range(Q - 1)}


def chi(x, j):
    x %= Q
    return cmath.exp(2j * cmath.pi * (logs[x] * j % 6) / 6) if x else 0j


def psi(x):
    return cmath.exp(-2j * cmath.pi * x)


def T(v, y):
    return sum(chi(x, v) * psi((y * x % Q) / Q) for x in range(Q))


def brute(t, k, J):
    out = 0j
    for d in range(Q ** k):
        if (Q ** J - Q ** t * d) % (Q ** k):
            continue
        dc = chi(d, k) if k else 1
        if not dc:
            continue
        for v in range(Q ** t):
            vc = chi(v, t) if t else 1
            if vc:
                out += dc * vc * psi(((Q ** J - Q ** t * d) * v % Q ** (k + t)) / Q ** (k + t))
    return out


checks = []
for t in [0, 1, 3]:
    for k in range(3):
        for J in range(6):
            if t == 0:
                expected = 1 if k == 0 or J == 0 else 0
            elif k == 0:
                expected = Q ** (t - 1) * T(t, Q ** (J - t + 1)) if J >= t - 1 else 0
            elif k == 1:
                expected = T(1, 1) * Q ** (t - 1) * T(t - 1, Q ** (J - t)) if J >= t else 0
            else:
                expected = 0
            actual = brute(t, k, J)
            checks.append((t, k, J, abs(actual - expected)))
print({'C_local_direct_cases': len(checks), 'max_absolute_error': max(x[3] for x in checks), 'bad_cases': [x for x in checks if x[3] > 1e-8]})

a = F(9, 10)
b = F(133, 1000)
h = F(1, 10)
principal = F(7, 15)
E = lambda xi, w, z: a / 2 + xi - 1 + h * z + b * (w - 1)
print({'reflection_margin': str((2 * (a + b) - 1 - b) / 2 - principal), 'good_row_margin': str(E(F(998, 1000), F(3, 1000), F(4, 10)) + F(10001, 100000) * F(11, 10) - principal), 'far_row_margin': str(F(3849, 1000) + h * 350000 + F(10001, 100000) * (1 - 350000) - principal)})
