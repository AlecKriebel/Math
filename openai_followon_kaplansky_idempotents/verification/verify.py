#!/usr/bin/env python3
"""Exact supplemental checks. This is not a group-algebra witness certificate."""
from fractions import Fraction
import json, math

points = set(range(1, 8))
lines = {frozenset((a, b, a ^ b)) for a in points for b in points if a != b}
complements = [points - line for line in lines]
assert len(lines) == 7 and all(len(d) == 4 for d in complements)
assert all(len(complements[i] & complements[j]) == 2 for i in range(7) for j in range(i))
assert all(sum(t in d for d in complements) == 4 for t in points)
assert all(sum(a in d and b in d for d in complements) == 2 for a in points for b in points if a != b)

q, v = 128, 16513
p = Fraction(q+1, v)
ordinary_bound = Fraction(q, q+1) + 7*p*p + Fraction(21, (q+1)**2)
extra_ratio = (Fraction(6, 4) + (v+21)*p*p)/4
contraction = max(ordinary_bound, extra_ratio)
assert contraction < 1
for m in (5, 9, 101, 1001):
    a_m = Fraction(129*m-1, 4)
    b_m = Fraction(129*(m-1), 4)
    assert a_m.denominator == b_m.denominator == 1
    assert 4*a_m+1 == 129*m and 4*b_m == 129*(m-1)

# Infinite polynomial shift operators on F_2[t], evaluated without truncation.
# a deletes a constant coefficient and shifts down; b shifts up; e projects
# to constants. The formulas, rather than these samples, prove the identities.
for x in range(256):
    a = lambda y: y >> 1
    b = lambda y: y << 1
    e = lambda y: y & 1
    assert a(b(x)) == x
    assert x ^ b(a(x)) == e(x)
    assert e(e(x)) == e(x)
    assert a(e(x)) == e(b(x)) == 0
    assert b(a(x)) ^ e(x) == x
assert e(1) == 1 and e(2) != 2

# Boundary test in F_2[C_3]; this is a torsion example, not the target group.
def convolution(x, y):
    z = [0, 0, 0]
    for i, u in enumerate(x):
        for j, w in enumerate(y):
            z[(i+j) % 3] += u*w
    return z
z = convolution([0, 1, 1], [0, 1, 1])
assert z == [2, 1, 1] and [k % 2 for k in z] == [0, 1, 1]

print(json.dumps({'status':'passed','scope':'Fano incidence, exact word-weight contraction, balance identities, abstract shift samples, characteristic boundary; no numerical target-group certificate', 'fano_lines':7,'contraction':str(contraction),'contraction_decimal':float(contraction),'delta_display_only':-math.log(float(contraction))/4,'polynomial_samples':256},indent=2))
