#!/usr/bin/env python3
"""Exact constant audit for agent_n3_quantitative_high_aaa.md."""

from fractions import Fraction as F


# Elementary radical comparisons used in the proof.
assert F(178) < F(14) ** 2
assert F(30) < F(6) ** 2
assert F(21) < F(5) ** 2
assert F(327) < F(19) ** 2
assert F(1, 6) > F(2, 5) ** 2  # 1/sqrt(6) > 2/5


# The chosen explicit deficit.
den = 10**120
eps0 = F(1, den)

# eps0^(1/8)=10^-15 exactly, while eps0^(1/16)<10^-7.
assert eps0 == F(1, 10**15) ** 8
assert eps0 < F(1, 10**7) ** 16


# Concentration thresholds are overwhelmingly satisfied.
assert F(1928) * eps0 < F(4, 3)
assert F(4, 9) - F(656) * eps0 > F(1, 10)
assert F(4, 3) - F(648) * eps0 > 1


# The plane leakage coefficient: the proof uses the round upper
# bound 340 eps0^(1/8).
assert F(20, 3) * F(51) == F(340)


# From sqrt(340)<19 and sqrt(2)<2,
# (16 sqrt(2)/3) sqrt(340) < 210.
assert F(340) < F(19) ** 2
assert F(16 * 2 * 19, 3) < F(210)


# The perturbation is inside the positive-definite square-root chart.
q_upper = F(210, 10**7)
assert q_upper < F(2, 27)


# Final concurrence margin:
# 18 sqrt(3) q < 36 * 210 * 10^-7 < 4/27.
c2_upper = F(36 * 210, 10**7)
assert c2_upper < F(4, 27)
assert c2_upper + F(8, 27) < F(4, 9)

print("quantitative high-AAA constants: exact")
