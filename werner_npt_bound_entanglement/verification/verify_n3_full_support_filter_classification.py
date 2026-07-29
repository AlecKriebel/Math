#!/usr/bin/env python3
"""Exact checks for the full-support filter classification note.

Only Python's standard library is used.  The script verifies:

1. the sharp uniform one-site counterexample at f=1;
2. the rank-two equality filter diag(1,1,0);
3. the minimum-eigenvalue filter arithmetic for a nonuniform rho;
4. the degree coefficients in the common-origin Gram trace identity.
"""

from fractions import Fraction as F


c = F(2, 3)


def q_uniform(entries, trace, f=F(1)):
    """q for rho=I/3, tau=1."""
    hs2 = sum(abs(x) ** 2 for x in entries)
    return c * hs2 / 3 - f * abs(trace) ** 2 / 9


# A=I: the unique scalar direction is negative.
I_entries = [F(1), F(1), F(1)]
assert q_uniform(I_entries, F(3)) == F(-1, 3)

# A=diag(1,1,0): rank two and exact equality.
P2_entries = [F(1), F(1)]
assert q_uniform(P2_entries, F(2)) == 0

# On the traceless hyperplane the same form is strictly positive.
B_entries = [F(1), F(-1)]
assert q_uniform(B_entries, F(0)) == F(4, 9)

# The rank-two trace estimate makes the whole certificate exact:
# q(A) >= (2/9 - 2/9)||A||^2 = 0 at f=1.
assert c / 3 - F(2, 9) == 0


# Nonuniform minimum-eigenvalue filter.
lambdas = [F(1, 2), F(1, 3), F(1, 6)]
tau = sum(lambdas)
m = min(lambdas)
f = F(4, 5)
assert tau == 1
assert f * (tau - m) == c * tau  # sharp admissibility boundary

# For P_min and I-P_min, the rank-two-complement bound is sharp.
r = m
bound_rank1 = r * (c - f * r / tau)
bound_rank2 = (tau - r) * (c - f * (tau - r) / tau)
assert bound_rank1 == F(4, 45)
assert bound_rank2 == 0
# The minimum in the note is therefore zero.
assert min(bound_rank1, bound_rank2) == 0


# Common-origin Gram-trace coefficients.
# A pattern is a 3-bit tuple: 1=traceless, 0=scalar.
def site_coefficient(pattern, site):
    degree_off_site = sum(pattern[j] for j in range(3) if j != site)
    if degree_off_site == 2:
        return F(1, 3)   # local scalar projection
    if degree_off_site == 1:
        return F(8, 3)   # local traceless projection
    return F(0)


expected = {
    0: F(0),
    1: F(16, 3),
    2: F(17, 3),
    3: F(1),
}

for pattern_as_int in range(8):
    pattern = tuple((pattern_as_int >> j) & 1 for j in range(3))
    degree = sum(pattern)
    coefficient = sum(site_coefficient(pattern, i) for i in range(3))
    assert coefficient == expected[degree], (pattern, coefficient)


# The trace identity plus matrix-unit q>=0 gives only a weak bound:
# at w1=w3=0, f=3/4 it is strictly feasible, so no contradiction is
# accidentally claimed.
f_test = F(3, 4)
gram_trace_sum = F(17, 3) * f_test
assert gram_trace_sum == F(17, 4)
assert gram_trace_sum < 6

print("PASS: exact full-support filter classification checks")
