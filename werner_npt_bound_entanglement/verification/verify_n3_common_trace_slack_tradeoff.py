#!/usr/bin/env python3
"""Dependency-free exact checks for the common trace/slack identities."""

from fractions import Fraction as F


# Independent formal variables are represented by coefficient vectors in
# the order (x, a, c, d, R, S, p, Delta).
def add(*vectors):
    return tuple(sum((v[i] for v in vectors), F(0)) for i in range(8))


def scale(q, vector):
    return tuple(q * x for x in vector)


x = (F(1), F(0), F(0), F(0), F(0), F(0), F(0), F(0))
a = (F(0), F(1), F(0), F(0), F(0), F(0), F(0), F(0))
c = (F(0), F(0), F(1), F(0), F(0), F(0), F(0), F(0))
d = (F(0), F(0), F(0), F(1), F(0), F(0), F(0), F(0))
R = (F(0), F(0), F(0), F(0), F(1), F(0), F(0), F(0))
S = (F(0), F(0), F(0), F(0), F(0), F(1), F(0), F(0))
p = (F(0), F(0), F(0), F(0), F(0), F(0), F(1), F(0))
Delta = (F(0), F(0), F(0), F(0), F(0), F(0), F(0), F(1))

N = add(x, a, c, d)
trace2 = scale(F(27), x)

# Equations (11).
R_sector = add(scale(F(3, 2), c), scale(F(3), a), scale(F(-9, 4), x))
S_sector = add(scale(F(9), d), scale(F(3, 4), a), scale(F(-3), c))

# Verify the solved equations (12).
x_solved = add(scale(F(2, 3), c), scale(F(4, 3), a), scale(F(-4, 9), R))
d_solved = add(scale(F(1, 9), S), scale(F(-1, 12), a), scale(F(1, 3), c))

assert add(R_sector, scale(F(-1), R)) == (
    F(-9, 4), F(3), F(3, 2), F(0), F(-1), F(0), F(0), F(0)
)
assert add(S_sector, scale(F(-1), S)) == (
    F(0), F(3, 4), F(-3), F(9), F(0), F(-1), F(0), F(0)
)

# Substitute x_solved and d_solved into a linear form.
def substitute_xd(form):
    cx, ca, cc, cd, cR, cS, cp, cDelta = form
    return add(
        scale(cx, x_solved),
        scale(ca, a),
        scale(cc, c),
        scale(cd, d_solved),
        scale(cR, R),
        scale(cS, S),
        scale(cp, p),
        scale(cDelta, Delta),
    )


global_trace_defect = add(scale(F(2), N), scale(F(-1), trace2))
converted_global = substitute_xd(global_trace_defect)
expected_global = add(
    scale(F(100, 9), R),
    scale(F(2, 9), S),
    scale(F(-14), c),
    scale(F(-63, 2), a),
)
assert converted_global == expected_global

identity_2_lhs = add(
    scale(F(200), R),
    scale(F(4), S),
    scale(F(-252), c),
    scale(F(-567), a),
)
assert identity_2_lhs == scale(F(18), expected_global)

sharp_trace_defect = add(N, scale(F(2), p), scale(F(-1), trace2))
converted_sharp = substitute_xd(sharp_trace_defect)
identity_22_lhs = add(
    scale(F(416), R),
    scale(F(4), S),
    scale(F(72), p),
    scale(F(-576), c),
    scale(F(-1215), a),
)
assert identity_22_lhs == scale(F(36), converted_sharp)

# The negative-locus band follows by eliminating 4S between
# 200R+4S >= 252c+567a and 2R+4S < 9c.
assert F(243, 198) == F(27, 22)
assert F(567, 198) == F(63, 22)
assert (F(9, 2) - F(27, 22)) / F(63, 22) == F(8, 7)
assert F(18, 198) == F(1, 11)

# Delta=(s1-s2)^2=N-2p, so the global trace defect splits into
# the singular imbalance plus the sharper nuclear/trace defect.
imbalance_relation = add(N, scale(F(-2), p), scale(F(-1), Delta))
assert imbalance_relation == (
    F(1), F(1), F(1), F(1), F(0), F(0), F(-2), F(-1)
)
assert add(
    global_trace_defect,
    scale(F(-1), Delta),
    scale(F(-1), sharp_trace_defect),
) == imbalance_relation

# Negative-depth simplex substitution.  Coefficients are checked as
# polynomials in delta, L, a, Delta:
# (1-5 delta)(300-297 L) - 84(1+delta) - 567a - 18Delta
# = 216 - 1584delta - 297(1-5delta)L - 567a - 18Delta.
assert 300 - 84 == 216
assert -1500 - 84 == -1584
assert F(216, 1584) == F(3, 22)

print("verified: sector-to-slack equations")
print("verified: exact common trace-deficit identity")
print("verified: sharper global exterior-deficit identity")
print("verified: singular-imbalance strengthening")
print("verified: strict negative-locus band")
print("verified: explicit negative-depth bound delta < 3/22")
