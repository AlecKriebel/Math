"""Independent symbolic reconstruction of the weighted-triangle claim.

This file does not import or execute any code from the delivered package.
"""

import sympy as sp


a, b, c, r = sp.symbols("a b c r")
w = {
    (0, 1): a,
    (1, 0): a,
    (0, 2): b,
    (2, 0): b,
    (1, 2): c,
    (2, 1): c,
}


def edge(i, j):
    return w[(i, j)]


def other(i, j):
    return 3 - i - j


def u(i, j):
    k = other(i, j)
    return r * edge(i, j) / (r * edge(i, j) + edge(j, k))


def v(i, j):
    k = other(i, j)
    return edge(i, j) / (r * edge(j, k) + edge(i, j))


# Unknown order F_0,F_1,F_2,G_0,G_1,G_2.  Reconstruct the six equations.
M = sp.zeros(6)
rhs = sp.zeros(6, 1)
for i in range(3):
    j, k = [z for z in range(3) if z != i]
    M[i, i] = 1 + u(i, j) + u(i, k)
    M[i, 3 + k] = -u(i, j)
    M[i, 3 + j] = -u(i, k)

    M[3 + i, 3 + i] = 1 + v(i, j) + v(i, k)
    M[3 + i, k] = -v(i, j)
    M[3 + i, j] = -v(i, k)
    rhs[3 + i] = 1

print("triangle_matrix_built", flush=True)
solution = M.inv(method="DM") * rhs
print("triangle_reduced_chain_solved", flush=True)
rho = sp.cancel(sum(solution[i] for i in range(3)) / 3)
baseline = 2 * r / (3 * (r + 1))
delta = sp.cancel(rho - baseline)

s1 = a + b + c
s2 = a * b + a * c + b * c
s3 = a * b * c
A = 3 * s3 * (s1 * s2 - 9 * s3)
D = 12 * s1**3 * s3 - 45 * s1 * s2 * s3 + 4 * s2**3 - 27 * s3**2
E = 4 * s2 * (3 * s1**2 * s2 - 3 * s1 * s3 - 8 * s2**2)
H = A * (r - 1) ** 4 + D * r * (r - 1) ** 2 + E * r**2
L = sp.prod(r * p + q for p in (a, b, c) for q in (a, b, c) if p != q)
P = sp.cancel(L * M.det(method="domain-ge") / 3)

assert sp.cancel(delta + r * (r - 1) * H / (3 * (r + 1) * P)) == 0
assert sp.denom(P) == 1

# Check all centered identities rather than assuming the displayed SOS.
U = s1**2 - 3 * s2
V = s2**2 - 3 * s1 * s3
W = s1 * s2 - 9 * s3
Z = s2**3 - 27 * s3**2
X, Y, Z0 = a * b, a * c, b * c
assert sp.expand(2 * U - ((a - b) ** 2 + (a - c) ** 2 + (b - c) ** 2)) == 0
assert sp.expand(2 * V - ((X - Y) ** 2 + (X - Z0) ** 2 + (Y - Z0) ** 2)) == 0
assert sp.expand(W - (c * (a - b) ** 2 + b * (a - c) ** 2 + a * (b - c) ** 2)) == 0
assert sp.expand(
    Z - (s2 * V + 3 * (Z0 * (X - Y) ** 2 + Y * (X - Z0) ** 2 + X * (Y - Z0) ** 2))
) == 0
assert sp.expand(A - 3 * s3 * W) == 0
assert sp.expand(D - (12 * s1 * s3 * U + 3 * s2 * V + Z)) == 0
assert sp.expand(E - 4 * s2 * (3 * s2 * U + V)) == 0

# An independently generated full subset chain must give the same singleton values.
states = [frozenset(S) for S in ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2))]
index = {S: z for z, S in enumerate(states)}
Q = sp.zeros(6)
fix = sp.zeros(6, 1)
for S in states:
    row = index[S]
    for target in range(3):
        mutant_weight = sum(edge(source, target) for source in S if source != target)
        resident_weight = sum(edge(source, target) for source in range(3) if source not in S and source != target)
        mutant_parent = sp.cancel(r * mutant_weight / (r * mutant_weight + resident_weight))
        outcomes = ((True, mutant_parent), (False, 1 - mutant_parent))
        for becomes_mutant, probability in outcomes:
            new = set(S)
            if becomes_mutant:
                new.add(target)
            else:
                new.discard(target)
            transition = sp.cancel(probability / 3)
            new = frozenset(new)
            if len(new) == 3:
                fix[row] += transition
            elif len(new) != 0:
                Q[row, index[new]] += transition

# To keep this second route independent and computationally modest, compare
# exact rational solutions at several nonsymmetric points instead of asking a
# second symbolic inverse to rediscover the already established identity.
for values in (
    {a: sp.Rational(2), b: sp.Rational(3), c: sp.Rational(5), r: sp.Rational(7, 3)},
    {a: sp.Rational(1), b: sp.Rational(4), c: sp.Rational(9), r: sp.Rational(2)},
    {a: sp.Rational(7), b: sp.Rational(2), c: sp.Rational(6), r: sp.Rational(11, 5)},
):
    Qv = Q.subs(values)
    fixv = fix.subs(values)
    full_solution = (sp.eye(6) - Qv).inv() * fixv
    reduced_solution = solution.subs(values)
    for i in range(3):
        assert full_solution[index[frozenset((i,))]] == reduced_solution[i]

print("triangle_identity=PASS")
print("triangle_full_chain_crosscheck=PASS")
print("triangle_P_polynomial=PASS")
print("triangle_centered_SOS_identities=PASS")
print("triangle_P_total_degree=", sp.Poly(P, a, b, c, r).total_degree())
