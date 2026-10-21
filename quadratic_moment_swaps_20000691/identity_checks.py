#!/usr/bin/env python3
"""Exact algebra and finite Gauss tests only; not an analytic proof."""
from fractions import Fraction as F
import cmath
import json
from pathlib import Path

def require(condition, label):
    if not condition:
        raise ValueError(label)

def mul(a, b):
    c = {}
    for i, x in a.items():
        for j, y in b.items():
            c[i+j] = c.get(i+j, F(0)) + x*y
    return c

# T(alpha)=C/(2alpha)+D; T(-alpha) changes the pole sign.
C, D, f0, f1, g1, logX = map(F, [6, 7, 2, 5, 3, 11])
T = {-1: C/2, 0: D}
Tminus = {-1: -C/2, 0: D}
shifted_weight = mul(mul({0: F(1), 1: -logX}, {0: F(1), 1: g1}), {0: f0, 1: -f1})
second = mul(shifted_weight, Tminus)
require(f0*T[-1]+second[-1] == 0, 'shift pole cancellation')
constant = f0*T[0]+second[0]
expected = C/2*(f0*logX+f1-f0*g1)+2*D*f0
require(constant == expected, 'shifted smoothing coefficient')
flat_second = mul(mul({0: F(1), 1: -logX}, {0: F(1), 1: g1}), Tminus)
flat = f0*T[0]+f0*flat_second[0]
require(constant-flat == C*f1/2, 'omitted Mellin derivative')
# Independent exact conductor polynomial substitution, P(t)=t^2+3t+5.
# L and h stand for log Y and log 8; no numerical logarithm used.
L, h = F(13), F(2)
conductor = ((L-h)**2+3*(L-h)+5)/8
require(conductor == (L*L+(3-2*h)*L+h*h-3*h+5)/8, 'conductor rescaling')
# Ordinary Gauss sum is imaginary; CR normalized one is real.
g = sum((0 if a == 0 else (1 if a == 1 else -1))*cmath.exp(2j*cmath.pi*a*2/3) for a in range(3))
normalized = -1j*g
require(abs(normalized + 3**.5) < 1e-12, 'normalized Gauss sign')
# Local p=2 expectation at k=1: a rational calculation independent of binomial code.
p2 = F(1, 3) + F(4, 3)
require(p2 == F(5, 3), 'p2 local normalization')
out = {'scope': 'exact algebra and finite examples, not analytic proof', 'smoothing_constant': str(constant), 'omitted_Mellin_term': str(constant-flat), 'conductor_polynomial': str(conductor), 'normalized_G_2_3': '-sqrt(3)', 'p2_k1': str(p2)}
text = json.dumps(out, indent=2)+'\n'
Path(__file__).with_name('IDENTITY_CHECKS.json').write_text(text)
print(text, end='')
