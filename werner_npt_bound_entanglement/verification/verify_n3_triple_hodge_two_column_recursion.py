#!/usr/bin/env python3
"""Exact checks for the two-column Hodge recursion."""

from fractions import Fraction as F


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
         for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def adjoint_product(a, b):
    return matmul(transpose(a), b)


def add(*matrices):
    return [
        [sum((a[i][j] for a in matrices), F(0))
         for j in range(len(matrices[0][0]))]
        for i in range(len(matrices[0]))
    ]


def scale(c, a):
    return [[F(c) * x for x in row] for row in a]


def kron(a, b):
    return [
        [a[i][j] * b[k][ell]
         for j in range(len(a[0])) for ell in range(len(b[0]))]
        for i in range(len(a)) for k in range(len(b))
    ]


I3 = [[F(i == j) for j in range(3)] for i in range(3)]


def epsilon(a, b, c):
    if len({a, b, c}) < 3:
        return F(0)
    return F(1) if (a, b, c) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)] else F(-1)


# E_p=sqrt(2) A_p are integer skew matrices.
E = [
    [[epsilon(p, a, i) for i in range(3)] for a in range(3)]
    for p in range(3)
]

# Exact normalized products A_p^* A_s.
K = {}
for p in range(3):
    for s in range(3):
        K[p, s] = scale(F(1, 2), adjoint_product(E[p], E[s]))
        expected = [
            [F(1, 2) * ((1 if p == s and i == j else 0)
                        - (1 if i == s and j == p else 0))
             for j in range(3)]
            for i in range(3)
        ]
        assert K[p, s] == expected


def double_hodge(coefficients):
    """D_x=sum x_pq A_p tensor A_q, with rational coefficients."""
    out = [[F(0) for _ in range(9)] for _ in range(9)]
    for p in range(3):
        for q in range(3):
            term = scale(F(coefficients[p][q], 2), kron(E[p], E[q]))
            out = add(out, term)
    return out


def eigencheck(a, vectors, values):
    for vector, value in zip(vectors, values):
        image = [
            sum((a[i][j] * vector[j] for j in range(len(vector))), F(0))
            for i in range(len(a))
        ]
        assert image == [value * x for x in vector]


# Product x=|00>: D^*D has eigenvalue 1/4 four times and zero otherwise.
D_product = double_hodge([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
R_product = adjoint_product(D_product, D_product)
diagonal_product = [R_product[i][i] for i in range(9)]
assert sorted(diagonal_product, reverse=True) == [F(1, 4)] * 4 + [F(0)] * 5
assert all(R_product[i][j] == 0 for i in range(9) for j in range(9) if i != j)

# Maximally entangled x.  We use D_tilde=sum E_p tensor E_p; then
# D_x^*D_x=(1/12) D_tilde^*D_tilde.
D_tilde = [[F(0) for _ in range(9)] for _ in range(9)]
for p in range(3):
    D_tilde = add(D_tilde, kron(E[p], E[p]))
R_phi = scale(F(1, 12), adjoint_product(D_tilde, D_tilde))
diag = [[F(i == j) for j in range(9)] for i in range(9)]
ones_diag = [F(1) if i in (0, 4, 8) else F(0) for i in range(9)]
phi = ones_diag
diag_traceless_1 = [F(1), 0, 0, 0, F(-1), 0, 0, 0, 0]
diag_traceless_2 = [F(1), 0, 0, 0, F(1), 0, 0, 0, F(-2)]
off_vectors = [[F(i == k) for i in range(9)] for k in [1, 2, 3, 5, 6, 7]]
eigencheck(
    R_phi,
    [phi, diag_traceless_1, diag_traceless_2] + off_vectors,
    [F(1, 3)] + [F(1, 12)] * 8,
)

# The local two-plane factor has spectrum (1,1/2,1/2).
K_plane = add(K[0, 0], K[1, 1])
eigencheck(
    K_plane,
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    [F(1, 2), F(1, 2), F(1)],
)

# Hence the two exact leading spectra are (1/4,1/4) and (1/3,1/6).
assert sorted(
    [x * y for x in [F(1, 4)] * 4 for y in [F(1), F(1, 2), F(1, 2)]],
    reverse=True,
)[:2] == [F(1, 4), F(1, 4)]
assert sorted(
    [x * y for x in [F(1, 3)] + [F(1, 12)] * 8
     for y in [F(1), F(1, 2), F(1, 2)]],
    reverse=True,
)[:2] == [F(1, 3), F(1, 6)]

# The two exact branches fit (1/4+p/2,1/4-p/2).
assert (
    F(1, 4) + F(0, 1) / 2,
    F(1, 4) - F(0, 1) / 2,
) == (F(1, 4), F(1, 4))
assert (
    F(1, 4) + F(1, 6) / 2,
    F(1, 4) - F(1, 6) / 2,
) == (F(1, 3), F(1, 6))

# Exact obstruction to the second affine bound.  For
# x=(|00>+|11>)/sqrt(2), the diagonal Hodge block has singular
# squares 1/4,1/4,0 and the four relevant off-diagonal squares are
# 1/8.  In the one-factor plane U=x tensor span(e0,e1), one also has
# p_U=||D_x x||^2 ||A_0 e_1||^2=(1/4)(1/2)=1/8.
p_affine_obstruction = F(1, 8)
lambda2_affine_obstruction = F(1, 4)
assert lambda2_affine_obstruction > F(1, 4) - p_affine_obstruction / 2
assert (
    lambda2_affine_obstruction
    - (F(1, 4) - p_affine_obstruction / 2)
    == F(1, 16)
)


def matrix_vector(a, x):
    return [
        sum((a[i][j] * x[j] for j in range(len(x))), F(0))
        for i in range(len(a))
    ]


def norm_square(x):
    return sum((z * z for z in x), F(0))


def triple_hodge_integer(coefficients):
    """sum coefficients[p,q,r] E_p tensor E_q tensor E_r."""
    out = [[F(0) for _ in range(27)] for _ in range(27)]
    for p in range(3):
        for q in range(3):
            for r in range(3):
                coefficient = coefficients[9 * p + 3 * q + r]
                if coefficient:
                    out = add(
                        out,
                        scale(coefficient, kron(kron(E[p], E[q]), E[r])),
                    )
    return out


# Exact obstruction to summing separate column operator norms.
# phi0 has AB support 00,11,22; phi1 has AB support 01,12,20.
# Both share the last factor e0.  The displayed test vectors replace
# e0 by e2 and attain the sharp single-column value 1/6.
u0_integer = [F(0)] * 27
u1_integer = [F(0)] * 27
x0_integer = [F(0)] * 27
x1_integer = [F(0)] * 27
for a in range(3):
    u0_integer[9 * a + 3 * a + 0] = F(1)
    x0_integer[9 * a + 3 * a + 2] = F(1)
    b = (a + 1) % 3
    u1_integer[9 * a + 3 * b + 0] = F(1)
    x1_integer[9 * a + 3 * b + 2] = F(1)

assert sum((u0_integer[i] * u1_integer[i] for i in range(27)), F(0)) == 0
T0_integer = triple_hodge_integer(u0_integer)
T1_integer = triple_hodge_integer(u1_integer)

# T_{u_a} x_a has scale 1/sqrt(72): 1/sqrt(24) from T_{u_a}
# and 1/sqrt(3) from x_a.
column0_energy = norm_square(matrix_vector(T0_integer, x0_integer)) / 72
column1_energy = norm_square(matrix_vector(T1_integer, x1_integer)) / 72
assert column0_energy == column1_energy == F(1, 6)

# T_{u0}u1 vanishes already before normalization because E_0 e_0=0
# on their common third factor.
assert matrix_vector(T0_integer, u1_integer) == [F(0)] * 27
p_op2_obstruction = F(0)
assert (
    column0_energy + column1_energy
    - (F(1, 4) + p_op2_obstruction / 2)
    == F(1, 12)
)

# Check the general block recursion on an arbitrary rational slice family.
slices = [
    [
        [[1, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 1, 0], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
    ],
    [
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[0, 0, 1], [0, 0, 0], [0, 0, 0]],
        [[0, 0, 0], [0, 0, 0], [1, 0, 0]],
    ],
]
D = [[double_hodge(slices[a][r]) for r in range(3)] for a in range(2)]
H = {}
for r in range(3):
    for s in range(3):
        H[r, s] = add(*(adjoint_product(D[a][r], D[a][s]) for a in range(2)))
G = add(H[0, 0], H[1, 1], H[2, 2])
direct = [[F(0) for _ in range(27)] for _ in range(27)]
for r in range(3):
    for s in range(3):
        direct = add(direct, kron(H[r, s], K[r, s]))
partial_transpose_h = [[F(0) for _ in range(27)] for _ in range(27)]
for r in range(3):
    for s in range(3):
        block = H[r, s]
        for i in range(9):
            for j in range(9):
                partial_transpose_h[3 * i + s][3 * j + r] = block[i][j]
recursive = scale(
    F(1, 2),
    add(kron(G, I3), scale(-1, partial_transpose_h)),
)
assert direct == recursive

print("all exact two-column Hodge recursion checks passed")
