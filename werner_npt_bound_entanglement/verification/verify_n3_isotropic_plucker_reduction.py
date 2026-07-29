#!/usr/bin/env python3
"""Exact audit of the isotropic block-Gram/Pluecker reduction.

Only Python's standard library is used.  A deterministic rational
rank-two factorization checks:

* the direct partial-trace definition of the two-copy block Gram;
* beta^Gamma = G_plus - G_minus;
* the invariant T,S extraction and four-mass identity;
* every common-factor Pluecker identity for the mixed exterior tensor.

The proof in the companion note is symbolic; this is an independent
exact contraction audit.
"""

from fractions import Fraction as F


D = 3
E = D * D
K = 2


def factor_entry(side: int, a: int, i: int, r: int) -> F:
    """Small deterministic integer tensors with no imposed symmetry."""
    value = (
        11
        + 7 * side
        + 5 * a
        + 3 * i
        + 2 * r
        + (a + 1) * (i + 2) * (r + 1)
        + side * (a + 2) * (i % 4 + 1)
    )
    sign = -1 if (side + a + i + r + a * i) % 3 == 0 else 1
    return F(sign * (value % 13 - 6))


x = [
    [[factor_entry(0, a, i, r) for r in range(K)] for i in range(E)]
    for a in range(D)
]
y = [
    [[factor_entry(1, p, i, r) for r in range(K)] for i in range(E)]
    for p in range(D)
]


def block(a: int, p: int):
    return [
        [sum(x[a][i][r] * y[p][j][r] for r in range(K)) for j in range(E)]
        for i in range(E)
    ]


blocks = [[block(a, p) for p in range(D)] for a in range(D)]


def dot_matrix(u, v):
    return sum(u[i][j] * v[i][j] for i in range(len(u)) for j in range(len(u[0])))


def partial_trace(m, site: int):
    out = [[F(0) for _ in range(D)] for _ in range(D)]
    for i in range(D):
        for j in range(D):
            if site == 0:
                out[i][j] = sum(m[D * k + i][D * k + j] for k in range(D))
            else:
                out[i][j] = sum(m[D * i + k][D * j + k] for k in range(D))
    return out


def trace(m):
    return sum(m[i][i] for i in range(len(m)))


def b2(u, v):
    return (
        dot_matrix(u, v)
        - F(1, 2) * dot_matrix(partial_trace(u, 0), partial_trace(v, 0))
        - F(1, 2) * dot_matrix(partial_trace(u, 1), partial_trace(v, 1))
        + F(1, 4) * trace(u) * trace(v)
    )


beta = [
    [
        b2(blocks[a][p], blocks[b][q])
        for b in range(D)
        for q in range(D)
    ]
    for a in range(D)
    for p in range(D)
]


def product_vector(u, v):
    return [[u[i] * v[j] for j in range(E)] for i in range(E)]


def add_vectors(*terms):
    return [
        [sum(coefficient * vector[i][j] for coefficient, vector in terms)
         for j in range(E)]
        for i in range(E)
    ]


def r_inner(z, w):
    """<z,(I-F_0/2)(I-F_1/2)w> on E tensor E."""
    total = F(0)
    for a in range(D):
        for b in range(D):
            i = D * a + b
            for c in range(D):
                for d in range(D):
                    j = D * c + d
                    total += z[i][j] * (
                        w[i][j]
                        - F(1, 2) * w[D * c + b][D * a + d]
                        - F(1, 2) * w[D * a + d][D * c + b]
                        + F(1, 4) * w[j][i]
                    )
    return total


sym = {}
wedge = {}
for a in range(D):
    for p in range(D):
        z00 = product_vector(
            [x[a][i][0] for i in range(E)],
            [y[p][j][0] for j in range(E)],
        )
        z11 = product_vector(
            [x[a][i][1] for i in range(E)],
            [y[p][j][1] for j in range(E)],
        )
        z01 = product_vector(
            [x[a][i][0] for i in range(E)],
            [y[p][j][1] for j in range(E)],
        )
        z10 = product_vector(
            [x[a][i][1] for i in range(E)],
            [y[p][j][0] for j in range(E)],
        )
        # Store the mixed vectors without sqrt(2); their Gram carries 1/2.
        sym[a, p] = (z00, z11, add_vectors((F(1), z01), (F(1), z10)))
        wedge[a, p] = add_vectors((F(1), z01), (F(-1), z10))


g_plus = [[F(0) for _ in range(D * D)] for _ in range(D * D)]
g_minus = [[F(0) for _ in range(D * D)] for _ in range(D * D)]
for a in range(D):
    for p in range(D):
        row = D * a + p
        for b in range(D):
            for q in range(D):
                col = D * b + q
                g_plus[row][col] = (
                    r_inner(sym[a, p][0], sym[b, q][0])
                    + r_inner(sym[a, p][1], sym[b, q][1])
                    + F(1, 2) * r_inner(sym[a, p][2], sym[b, q][2])
                )
                g_minus[row][col] = F(1, 2) * r_inner(
                    wedge[a, p], wedge[b, q]
                )


# Partial transpose: (beta^Gamma)_(ap,bq) = beta_(aq,bp).
for a in range(D):
    for p in range(D):
        for b in range(D):
            for q in range(D):
                assert (
                    g_plus[D * a + p][D * b + q]
                    - g_minus[D * a + p][D * b + q]
                    == beta[D * a + q][D * b + p]
                )


def ordinary_trace(m):
    return sum(m[i][i] for i in range(D * D))


def swap_trace(m):
    return sum(m[D * a + p][D * p + a] for a in range(D) for p in range(D))


T = ordinary_trace(beta)
S = sum(
    beta[D * a + a][D * b + b]
    for a in range(D)
    for b in range(D)
)
assert S == swap_trace(
    [[g_plus[i][j] - g_minus[i][j] for j in range(D * D)]
     for i in range(D * D)]
)

# These are the unique isotropic coefficients having the same T,S.
a_iso = (3 * S - T) / 24
b_iso = (3 * T - S) / 24
q = T - S / 2
assert q == F(3, 2) * (5 * b_iso - a_iso)


def parity_mass(g, sign: int):
    # Tr(P_sign g) = (Tr g + sign Tr(Fg))/2.
    return (ordinary_trace(g) + sign * swap_trace(g)) / 2


m_pp = parity_mass(g_plus, +1)
m_mp = parity_mass(g_plus, -1)
m_pm = parity_mass(g_minus, +1)
m_mm = parity_mass(g_minus, -1)
mass_gap = m_pp + 3 * m_mp - m_pm - 3 * m_mm
assert mass_gap == 2 * q
assert mass_gap == 3 * (5 * b_iso - a_iso)

# Schmidt-number boundary mixture:
# E |vec P><vec P| = a |vec I><vec I| + b I has
# trace 2 and maximally-entangled contraction 4.
a_boundary = (3 * F(4) - F(2)) / 24
b_boundary = (3 * F(2) - F(4)) / 24
assert a_boundary == F(5, 12)
assert b_boundary == F(1, 12)
assert a_boundary == 5 * b_boundary


# Full mixed common-factor Pluecker identity, in unnormalized form.
x_full = [
    [x[a][i][r] for r in range(K)]
    for a in range(D)
    for i in range(E)
]
y_full = [
    [y[p][j][r] for r in range(K)]
    for p in range(D)
    for j in range(E)
]


def q_mixed(alpha, beta_index):
    return (
        x_full[alpha][0] * y_full[beta_index][1]
        - x_full[alpha][1] * y_full[beta_index][0]
    )


def p_left(alpha, gamma):
    return (
        x_full[alpha][0] * x_full[gamma][1]
        - x_full[alpha][1] * x_full[gamma][0]
    )


def p_right(beta_index, delta):
    return (
        y_full[beta_index][0] * y_full[delta][1]
        - y_full[beta_index][1] * y_full[delta][0]
    )


for alpha in range(D * E):
    for gamma in range(D * E):
        for beta_index in range(D * E):
            for delta in range(D * E):
                assert (
                    q_mixed(alpha, beta_index) * q_mixed(gamma, delta)
                    - q_mixed(alpha, delta) * q_mixed(gamma, beta_index)
                    == p_left(alpha, gamma) * p_right(beta_index, delta)
                )


print("verified beta^Gamma = G_plus - G_minus exactly")
print("verified invariant A,B extraction and weighted four-mass identity")
print("verified the Schmidt-number-two boundary coefficients A/B = 5")
print("verified all common-factor mixed Pluecker identities")
