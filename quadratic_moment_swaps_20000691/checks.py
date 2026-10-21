"""Finite sanity checks, not an L-moment computation. Python standard library only."""
from fractions import Fraction as F
from math import comb, isqrt
import json, cmath
from pathlib import Path
out = {}
local = []
for k in range(1, 9):
    K = k * (k + 1) // 2
    sign_sum = sum((F(2 ** (k + 1)) * comb(k, 2 * j) / 2 ** j for j in range(k // 2 + 1)))
    E = (1 + sign_sum) / 3
    c2 = comb(k + 3, 4) - K * (K + 3) // 2
    direct = comb(k + 3, 4) - K - K * K + comb(K, 2)
    if not c2 == direct:
        raise AssertionError()
    local.append({'k': k, 'K': K, 'full_over_8_p2': str(E), 'a_p_x2': c2})
if not [v['full_over_8_p2'] for v in local[:3]] == ['5/3', '13/3', '41/3']:
    raise AssertionError()
out['exact_local_factors'] = local
N = 200000
sf = bytearray(b'\x01') * (N + 1)
sf[0] = 0
for p in range(2, isqrt(N) + 1):
    if sf[p]:
        for m in range(p * p, N + 1, p * p):
            sf[m] = 0
for sign in [1, -1]:
    vals = {-1: 0, 0: 0, 1: 0}
    for q in range(1, N + 1):
        D = sign * q
        fundamental = D % 4 == 1 and sf[q] or (D % 4 == 0 and sf[q // 4] and (D // 4 % 4 in [2, 3]))
        if fundamental:
            v = 0 if D % 2 == 0 else 1 if D % 8 in [1, 7] else -1
            vals[v] += 1
    total = sum(vals.values())
    out['positive' if sign == 1 else 'negative'] = {'bound': N, 'counts': vals, 'total': total, 'max_deviation': max((abs(v / total - 1 / 3) for v in vals.values()))}
g = sum(((0 if a == 0 else 1 if a == 1 else -1) * cmath.exp(2j * cmath.pi * a * 2 / 3) for a in range(3)))
if not abs(g + 1j * 3 ** 0.5) < 1e-12:
    raise AssertionError()
out['ordinary_gauss_n3_r2'] = {'real': g.real, 'imag': g.imag, 'exact': '-i sqrt(3)'}
out['long_polynomial_error_exponents_at_eta_k_over_2'] = {str(k): str(F(k, 8) + F(1, 2)) for k in range(1, 7)}
Path(__file__).with_name('EXACT_CHECKS.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
