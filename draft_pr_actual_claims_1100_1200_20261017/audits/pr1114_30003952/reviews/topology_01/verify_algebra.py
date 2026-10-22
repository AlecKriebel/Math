"""Independent exact controls; Python standard library only, no candidate code.

Run: python3 verify_algebra.py
This checks algebra and ribbon data, not equality of analytic functions.
"""
from fractions import Fraction
import json


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def power(a, n):
    out = ((1, 0), (0, 1))
    for _ in range(n):
        out = mul(out, a)
    return out


def inv(a):
    d = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return ((Fraction(a[1][1], d), Fraction(-a[0][1], d)),
            (Fraction(-a[1][0], d), Fraction(a[0][0], d)))


# Normal form z^m times a reduced word in C2*C3, for z=X^2=Y^3.
# Centrality follows from the defining relation; z has infinite order since
# X->3,Y->2 is a homomorphism to Z and z->6.
def normal(word):
    central, stack = 0, []
    for name, exponent in word:
        if stack and stack[-1][0] == name:
            exponent += stack.pop()[1]
        q, residue = divmod(exponent, 2 if name == "X" else 3)
        central += q
        if residue:
            stack.append((name, residue))
    return central, tuple(stack)


def inverse_word(word):
    return [(g, -e) for g, e in reversed(word)]


U, V = ((1, 1), (0, 1)), ((1, 0), (-1, 1))
Q, R = mul(mul(U, V), U), mul(U, V)
minus_I, I = ((-1, 0), (0, -1)), ((1, 0), (0, 1))
matrix_checks = {
    "UVU_equals_VUV": Q == mul(mul(V, U), V),
    "Q_squared_minus_I": power(Q, 2) == minus_I,
    "R_cubed_minus_I": power(R, 3) == minus_I,
    "Q_fourth_I": power(Q, 4) == I,
    "R_sixth_I": power(R, 6) == I,
    "R_inverse_Q_U": mul(inv(R), Q) == U,
    "Q_inverse_R_squared_V": mul(inv(Q), power(R, 2)) == V,
    "braid_center_not_in_SL_kernel": power(R, 3) != I,
}
assert all(matrix_checks.values())

A, B = [("Y", -1), ("X", 1)], [("X", -1), ("Y", 2)]
formal_checks = {
    "AB_Y": normal(A + B) == normal([("Y", 1)]),
    "ABA_X": normal(A + B + A) == normal([("X", 1)]),
    "BAB_X": normal(B + A + B) == normal([("X", 1)]),
    "braid": normal(A + B + A) == normal(B + A + B),
    "simultaneous_inversion": normal(inverse_word(A) + inverse_word(B) + inverse_word(A))
        == normal(inverse_word(B) + inverse_word(A) + inverse_word(B)),
    "AB_sixth_z_squared": normal((A + B) * 6) == (2, ()),
}
assert all(formal_checks.values())
bad_B = [("X", -1), ("Y", 1)]
assert normal(A + bad_B + A) != normal(bad_B + A + bad_B)

# No bounded search is needed: 1+12k=epsilon has these exact rational roots.
offset_roots = {str(e): str(Fraction(e - 1, 12)) for e in [-1, 1]}
assert offset_roots == {"-1": "-1/6", "1": "0"}

# Boundary cycles of the ribbon graph for one transverse intersection.
sigma, tau = [1, 2, 3, 0], [2, 3, 0, 1]
boundary_permutation = [sigma[tau[i]] for i in range(4)]
seen, cycles = set(), []
for i in range(4):
    if i not in seen:
        c, j = [], i
        while j not in seen:
            seen.add(j)
            c.append(j)
            j = boundary_permutation[j]
        cycles.append(c)
assert len(cycles) == 1
# v-e=-1 and b=1: 2-2g-b=-1, hence g=1.
assert (2 - len(cycles) - (1 - 2)) // 2 == 1

print(json.dumps({
    "matrix_checks": matrix_checks,
    "formal_group_checks": formal_checks,
    "negative_control_wrong_B_rejected": True,
    "offset_roots": offset_roots,
    "ribbon_boundary_cycles": cycles,
    "annular_inner_outer_turns": [1, 0],
    "annular_absolute_winding": 1,
    "result": "PASS exact finite algebra controls; analytic equality and topology require the report derivations",
}, indent=2))
