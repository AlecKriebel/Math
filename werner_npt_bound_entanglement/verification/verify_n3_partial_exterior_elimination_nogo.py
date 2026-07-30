#!/usr/bin/env python3
"""Exact checks for partial-exterior elimination and its scalar no-go."""

from fractions import Fraction as F


# Aggregate conversion in independent variables R,S,c,a,Delta.
# The expression obtained before clearing denominators is
# 12R + (5/2)(2N-Delta) - 5(9x+6a+3c).
# Substitute x=2c/3+4a/3-4R/9,
# d=S/9-a/12+c/3, N=x+a+c+d.
R = F(1)
coef_R = (
    F(12)
    + F(5, 2) * 2 * F(-4, 9)
    - F(5) * F(9) * F(-4, 9)
)
coef_S = F(5, 2) * 2 * F(1, 9)
coef_c = (
    F(5, 2) * 2 * (F(2, 3) + F(1) + F(1, 3))
    - F(5) * (F(9) * F(2, 3) + F(3))
)
coef_a = (
    F(5, 2) * 2 * (F(4, 3) + F(1) - F(1, 12))
    - F(5) * (F(9) * F(4, 3) + F(6))
)
coef_Delta = -F(5, 2)

assert 36 * coef_R == 1072
assert 36 * coef_S == 20
assert 36 * coef_c == -1260
assert 36 * coef_a == -2835
assert 36 * coef_Delta == -90

# Negative-depth substitution.
assert F(1072) * F(3, 2) - F(1260, 3) == F(1188)
assert F(1072) * F(15, 2) + F(1260, 3) == F(8460)
assert F(1072) * F(3, 2) - F(20) * F(3, 4) == F(1593)
assert F(1188, 9) == 132
assert F(8460, 9) == 940
assert F(1593, 9) == 177
assert F(2835, 9) == 315
assert F(90, 9) == 10

# Coefficientwise domination after multiplying the global trace bound
# by 11/18.
assert F(11, 18) * 216 == 132
assert F(11, 18) * 1584 - 940 == 28
assert F(11, 18) * 297 - 177 == F(9, 2)
assert F(11, 18) * 567 - 315 == F(63, 2)
assert F(11, 18) * 18 - 10 == 1

# Exact negative scalar model.
delta = F(1, 10)
L = F(1, 10)
u = (1 - 5 * delta) * L
a = F(1, 24)
Delta = F(0)
c = (1 + delta) / 3
Rsum = F(3, 2) * (1 - 5 * delta) * (1 - L)
Ssum = F(3, 4) * u
x = F(2, 3) * c + F(4, 3) * a - F(4, 9) * Rsum
d = Ssum / 9 - a / 12 + c / 3
N = x + a + c + d
Q = -x / 8 + a / 4 - c / 2 + d
p = (N - Delta) / 2

assert u == F(1, 20)
assert x == 0
assert c == F(11, 30)
assert d == F(59, 480)
assert N == F(17, 32)
assert Rsum == F(27, 40)
assert Ssum == F(3, 80)
assert Q == F(-1, 20)
assert p == F(17, 64)

global_lhs = 1584 * delta + 297 * u + 567 * a + 18 * Delta
partial_lhs = 940 * delta + 177 * u + 315 * a + 10 * Delta
assert global_lhs == F(1575, 8) < 216
assert partial_lhs == F(4639, 40) < 132

ai = a / 3
ci = c / 3
ri = Rsum / 3
si = Ssum / 3
ni = 3 * (2 * ai + ci)
assert ai == F(1, 72)
assert ci == F(11, 90)
assert ri == F(9, 40)
assert si == F(1, 80)
assert ni == F(9, 20)
assert 12 * ri > 5 * ni

print("verified: partial-trace nuclear/exterior conversion")
print("verified: common-plane exterior factor bound constants")
print("verified: aggregate inequality and coefficientwise domination")
print("verified: exact negative scalar no-go model")
