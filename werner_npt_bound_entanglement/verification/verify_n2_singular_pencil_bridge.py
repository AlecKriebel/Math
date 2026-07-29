#!/usr/bin/env python3
"""Dependency-free exact checks for the n=2 singular-pencil reduction.

This checks finite algebraic identities and the explicit rational equality
example.  It does not attempt to verify the conjectural uniform positivity
of the 9x9 residual.
"""

from fractions import Fraction as F


def zeros(m, n):
    return [[F(0) for _ in range(n)] for _ in range(m)]


def eye(n):
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def add(a, b):
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def sub(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def flatten(a):
    return [x for row in a for x in row]


def hs_inner(a, b):
    return sum(x * y for x, y in zip(flatten(a), flatten(b)))


def hs_norm2(a):
    return hs_inner(a, a)


def tr0(a):
    n = len(a)
    return sub(a, scale(trace(a) / n, eye(n)))


def matrix_unit(i, j, n=3):
    out = zeros(n, n)
    out[i][j] = F(1)
    return out


def s_matrix(x):
    """Matrix of S_X(Y)=((YX^T)_0,(X^TY)_0), real convention."""
    xt = transpose(x)
    out = zeros(18, 9)
    for col in range(9):
        y = matrix_unit(col // 3, col % 3)
        vals = flatten(tr0(matmul(y, xt))) + flatten(tr0(matmul(xt, y)))
        for row, value in enumerate(vals):
            out[row][col] = value
    return out


def cross_matrix(x):
    """Matrix of C_X(Y)=Y x X in the real exact convention."""
    out = zeros(9, 9)
    for col in range(9):
        values = flatten(cross(matrix_unit(col // 3, col % 3), x))
        for row, value in enumerate(values):
            out[row][col] = value
    return out


def as_column(values):
    return [[value] for value in values]


# Tiny dependency-free polynomial helper for the universal identity (70).
# A polynomial in (x1,x2,x3) is a dict exponent_tuple -> rational coefficient.
def poly_add(*polynomials):
    out = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            out[monomial] = out.get(monomial, F(0)) + coefficient
            if out[monomial] == 0:
                del out[monomial]
    return out


def poly_scale(coefficient, polynomial):
    return {
        monomial: coefficient * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def poly_mul(first, second):
    out = {}
    for left_monomial, left_coefficient in first.items():
        for right_monomial, right_coefficient in second.items():
            monomial = tuple(
                left + right
                for left, right in zip(left_monomial, right_monomial)
            )
            out[monomial] = (
                out.get(monomial, F(0))
                + left_coefficient * right_coefficient
            )
    return {monomial: value for monomial, value in out.items() if value}


def determinant(a):
    a = [row[:] for row in a]
    n = len(a)
    ans = F(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j] != 0), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            ans = -ans
        p = a[j][j]
        ans *= p
        for i in range(j + 1, n):
            q = a[i][j] / p
            for k in range(j + 1, n):
                a[i][k] -= q * a[j][k]
    return ans


def inverse(a):
    n = len(a)
    aug = [a[i][:] + eye(n)[i] for i in range(n)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if aug[i][j] != 0)
        aug[j], aug[pivot] = aug[pivot], aug[j]
        p = aug[j][j]
        aug[j] = [x / p for x in aug[j]]
        for i in range(n):
            if i == j:
                continue
            q = aug[i][j]
            aug[i] = [x - q * y for x, y in zip(aug[i], aug[j])]
    return [row[n:] for row in aug]


def block(a, b, c, d):
    return [ar + br for ar, br in zip(a, b)] + [
        cr + dr for cr, dr in zip(c, d)
    ]


def cross(x, y):
    def eps(i, j, k):
        if len({i, j, k}) < 3:
            return F(0)
        return F(1) if (i, j, k) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else F(-1)

    out = zeros(3, 3)
    for i in range(3):
        for alpha in range(3):
            out[i][alpha] = sum(
                eps(i, j, k)
                * eps(alpha, beta, gamma)
                * x[j][beta]
                * y[k][gamma]
                for j in range(3)
                for k in range(3)
                for beta in range(3)
                for gamma in range(3)
            )
    return out


SIGMAS = (
    [[F(1), F(0)], [F(0), F(1)]],
    [[F(0), F(1)], [F(1), F(0)]],
    [[F(1), F(0)], [F(0), F(-1)]],
    [[F(0), F(1)], [F(-1), F(0)]],
)


def channel(frame, pair, sigma):
    """Return (L,R,C,t) in the real exact convention of equations (34)."""
    left = zeros(3, 3)
    right = zeros(3, 3)
    hodge = zeros(3, 3)
    for r in range(2):
        for s in range(2):
            coefficient = sigma[r][s]
            left = add(
                left,
                scale(coefficient, matmul(pair[r], transpose(frame[s]))),
            )
            right = add(
                right,
                scale(coefficient, matmul(transpose(frame[s]), pair[r])),
            )
            hodge = add(
                hodge,
                scale(coefficient, cross(pair[r], frame[s])),
            )
    return left, right, hodge, trace(left)


def channel_a(frame, pair, sigma):
    left, right, hodge, scalar = channel(frame, pair, sigma)
    return (
        hs_norm2(hodge)
        + hs_norm2(left)
        + hs_norm2(right)
        - scalar * scalar
    )


def main():
    a, b = F(3, 5), F(4, 5)
    d = [[a, F(0), F(0)], [F(0), b, F(0)], [F(0), F(0), F(0)]]
    z = [[b, F(0), F(0)], [F(0), -a, F(0)], [F(0), F(0), F(0)]]

    assert hs_norm2(d) == 1
    assert hs_norm2(z) == 1
    assert hs_inner(d, z) == 0

    sd, sz = s_matrix(d), s_matrix(z)
    gd = sub(scale(F(2), eye(9)), matmul(transpose(sd), sd))

    # Formula (18).
    expected = zeros(9, 9)
    diagonal = [
        F(2) - F(4, 3) * a * a,
        F(1),
        F(1) + b * b,
        F(1),
        F(2) - F(4, 3) * b * b,
        F(1) + a * a,
        F(1) + b * b,
        F(1) + a * a,
        F(2),
    ]
    for i, value in enumerate(diagonal):
        expected[i][i] = value
    expected[0][4] = expected[4][0] = F(2, 3) * a * b
    assert gd == expected

    det_formula = (
        F(8, 3)
        * (1 + a * a * b * b)
        * (1 + a * a) ** 2
        * (1 + b * b) ** 2
    )
    assert determinant(gd) == det_formula
    gd_inv = inverse(gd)
    assert matmul(gd, gd_inv) == eye(9)

    # Exact block Schur congruence for formula (21).
    c = scale(F(-1), matmul(transpose(sd), sz))
    h = sub(scale(F(2), eye(9)), matmul(transpose(sz), sz))
    full = block(gd, c, transpose(c), h)
    residual = sub(h, matmul(matmul(transpose(c), gd_inv), c))
    left = block(eye(9), zeros(9, 9), scale(F(-1), matmul(transpose(c), gd_inv)), eye(9))
    right = transpose(left)
    diagonalized = matmul(matmul(left, full), right)
    assert diagonalized == block(gd, zeros(9, 9), zeros(9, 9), residual)

    # Exact equality and the obstruction to a gap proportional to ||D x Z||^2.
    h0 = [[F(-1, 2), F(0), F(0)], [F(0), F(1, 2), F(0)], [F(0), F(0), F(0)]]
    ld = add(matmul(h0, d), matmul(d, h0))
    lz = add(matmul(h0, z), matmul(z, h0))
    assert 2 * (hs_norm2(h0) + hs_norm2(h0)) == 2
    assert hs_norm2(ld) + hs_norm2(lz) == 2
    dz = cross(d, z)
    assert dz == [[F(0), F(0), F(0)], [F(0), F(0), F(0)], [F(0), F(0), F(7, 25)]]
    assert hs_norm2(dz) == F(49, 625)

    # Both flattening volumes vanish on this common 2x2 support.
    rho_l = add(matmul(d, transpose(d)), matmul(z, transpose(z)))
    rho_r = add(matmul(transpose(d), d), matmul(transpose(z), z))
    assert rho_l == [[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(0)]]
    assert rho_r == rho_l
    assert determinant(rho_l) == determinant(rho_r) == 0

    # Exact four-channel Hodge--Fierz identity (36)--(40).
    # The frame is the same rational orthonormal pair (d,z); the test pair
    # is intentionally nonsymmetric and nondiagonal.
    y1 = [
        [F(1, 3), F(-2, 5), F(1, 7)],
        [F(2, 9), F(1, 4), F(-3, 8)],
        [F(1, 6), F(5, 11), F(-2, 7)],
    ]
    y2 = [
        [F(-1, 5), F(3, 7), F(2, 9)],
        [F(4, 11), F(-2, 3), F(1, 8)],
        [F(-3, 10), F(1, 6), F(5, 12)],
    ]
    frame = (d, z)
    pair = (y1, y2)
    channel_values = [
        channel_a(frame, pair, sigma) for sigma in SIGMAS
    ]
    assert channel_values[0] == channel_values[3]
    assert channel_values[1] == channel_values[2]
    pair_norm = hs_norm2(y1) + hs_norm2(y2)
    assert sum(channel_values) == 4 * pair_norm

    l0, r0, c0, t0 = channel(frame, pair, SIGMAS[0])
    l1, r1, c1, t1 = channel(frame, pair, SIGMAS[1])
    defect_direct = (
        2 * pair_norm - hs_norm2(tr0(l0)) - hs_norm2(tr0(r0))
    )
    defect_fierz = (
        hs_norm2(c0)
        + hs_norm2(c1)
        + hs_norm2(tr0(l1))
        + hs_norm2(tr0(r1))
        - (t0 * t0 + t1 * t1) / 3
    )
    assert defect_direct == defect_fierz

    # Exact polarized Hodge identity (57) and one-scalar collapse (58).
    # The real rational check is coefficientwise and therefore also checks
    # the corresponding complex sesquilinear identity after polarization.
    y = y1
    w = y2
    p_scalar = hs_inner(d, y)
    q_scalar = hs_inner(z, w)
    polarized_products = (
        hs_inner(tr0(matmul(y, transpose(d))), tr0(matmul(w, transpose(z))))
        + hs_inner(tr0(matmul(transpose(d), y)), tr0(matmul(transpose(z), w)))
    )
    polarized_hodge = (
        p_scalar * q_scalar / 3
        - hs_inner(cross(y, z), cross(w, d))
    )
    assert polarized_products == polarized_hodge

    defect_48 = (
        2 * hs_norm2(cross(y, d))
        + 2 * hs_norm2(cross(w, z))
        + hs_norm2(
            tr0(sub(matmul(y, transpose(d)), matmul(w, transpose(z))))
        )
        + hs_norm2(
            tr0(sub(matmul(transpose(d), y), matmul(transpose(z), w)))
        )
        - F(2, 3) * (p_scalar * p_scalar + q_scalar * q_scalar)
    )
    defect_58 = (
        hs_norm2(y)
        + hs_norm2(w)
        + hs_norm2(cross(y, d))
        + hs_norm2(cross(w, z))
        + 2 * hs_inner(cross(y, z), cross(w, d))
        - (p_scalar + q_scalar) ** 2 / 3
    )
    assert defect_48 == defect_58

    # Exact obstruction (62): D=y=E11 and Z=E22 gives 5/3 <= 1.
    e11 = matrix_unit(0, 0)
    e22 = matrix_unit(1, 1)
    obstruction_lhs = (
        hs_norm2(cross(e11, e22))
        - hs_norm2(cross(e11, e11))
        + F(2, 3) * hs_inner(e11, e11) ** 2
    )
    assert obstruction_lhs == F(5, 3)
    assert hs_norm2(e11) == 1

    # Exact scalar certificates used in Theorem 11.1.  Choose Schmidt
    # coefficients (4/5,3/5,2/5); normalization is irrelevant.
    schmidt = (F(4, 5), F(3, 5), F(2, 5))
    x1, x2, x3 = (value * value for value in schmidt)
    total = x1 + x2 + x3
    h_schmidt = [
        [
            schmidt[i] * schmidt[j]
            - (2 * (x1, x2, x3)[i] if i == j else 0)
            for j in range(3)
        ]
        for i in range(3)
    ]
    shifted = add(h_schmidt, scale(total, eye(3)))
    # The one-, two-, and three-dimensional principal-minor formulas.
    xs = (x1, x2, x3)
    for i in range(3):
        assert shifted[i][i] == total - xs[i]
    for i, j, k in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
        principal_two = (
            shifted[i][i] * shifted[j][j]
            - shifted[i][j] * shifted[j][i]
        )
        assert principal_two == xs[k] * total
    assert determinant(shifted) == 4 * x1 * x2 * x3

    m_small = x2 + x3
    exact_rank_one_remainder = (
        x1 * (x2 - x3) ** 2 + 2 * (x2 + x3) ** 3
    ) / (
        (2 * x1 + x2 + x3)
        * (3 * x2 + x3)
        * (x2 + 3 * x3)
    )
    secular_remainder = 1 - sum(
        value / (m_small + 2 * value) for value in xs
    )
    assert secular_remainder == exact_rank_one_remainder
    assert exact_rank_one_remainder > 0

    # Universal cross-multiplied form of (70), not just the sample above.
    px1 = {(1, 0, 0): F(1)}
    px2 = {(0, 1, 0): F(1)}
    px3 = {(0, 0, 1): F(1)}
    denominator_1 = poly_add(poly_scale(2, px1), px2, px3)
    denominator_2 = poly_add(poly_scale(3, px2), px3)
    denominator_3 = poly_add(px2, poly_scale(3, px3))
    common_denominator = poly_mul(
        poly_mul(denominator_1, denominator_2), denominator_3
    )
    secular_numerator = poly_add(
        common_denominator,
        poly_scale(-1, poly_mul(px1, poly_mul(denominator_2, denominator_3))),
        poly_scale(-1, poly_mul(px2, poly_mul(denominator_1, denominator_3))),
        poly_scale(-1, poly_mul(px3, poly_mul(denominator_1, denominator_2))),
    )
    difference_x2_x3 = poly_add(px2, poly_scale(-1, px3))
    sum_x2_x3 = poly_add(px2, px3)
    manifest_numerator = poly_add(
        poly_mul(px1, poly_mul(difference_x2_x3, difference_x2_x3)),
        poly_scale(
            2,
            poly_mul(sum_x2_x3, poly_mul(sum_x2_x3, sum_x2_x3)),
        ),
    )
    assert secular_numerator == manifest_numerator

    # Exact mixed-Lagrange bridge from Theorem 11.1 to the cross-product
    # row contraction, for a nonsymmetric rational test U.
    test_u = [
        [F(2, 7), F(-1, 3), F(4, 9)],
        [F(3, 8), F(1, 5), F(-2, 11)],
        [F(-1, 6), F(5, 13), F(3, 10)],
    ]
    cross_row_energy = hs_norm2(cross(test_u, d)) + hs_norm2(cross(test_u, z))
    product_loss = (
        hs_norm2(matmul(test_u, transpose(d)))
        + hs_norm2(matmul(transpose(test_u), d))
        + hs_norm2(matmul(test_u, transpose(z)))
        + hs_norm2(matmul(transpose(test_u), z))
        - hs_inner(test_u, d) ** 2
        - hs_inner(test_u, z) ** 2
    )
    assert 2 * hs_norm2(test_u) - cross_row_energy == product_loss

    # Exact operator algebra in the strong reversed-Hodge completion
    # (74)--(80).  Positivity of row_defect is Theorem 11.1; every other
    # step below is checked as an exact rational matrix identity.
    cd = cross_matrix(d)
    cz = cross_matrix(z)
    a_op = matmul(transpose(cd), cd)
    b_op = matmul(transpose(cz), cz)
    k_op = matmul(transpose(cz), cd)
    one_minus_a = sub(eye(9), a_op)
    row_defect = sub(
        scale(F(2), eye(9)),
        add(matmul(cd, transpose(cd)), matmul(cz, transpose(cz))),
    )
    contraction_remainder = sub(
        sub(eye(9), matmul(transpose(k_op), k_op)),
        matmul(one_minus_a, one_minus_a),
    )
    assert contraction_remainder == matmul(
        matmul(transpose(cd), row_defect), cd
    )

    d_column = as_column(flatten(d))
    z_column = as_column(flatten(z))
    r_column = sub(
        z_column, matmul(transpose(k_op), d_column)
    )
    assert r_column == matmul(one_minus_a, z_column)
    z_projection = matmul(z_column, transpose(z_column))
    rank_one_remainder = sub(
        matmul(one_minus_a, one_minus_a),
        matmul(r_column, transpose(r_column)),
    )
    assert rank_one_remainder == matmul(
        matmul(one_minus_a, sub(eye(9), z_projection)),
        one_minus_a,
    )
    r_op = sub(
        add(eye(9), b_op),
        matmul(transpose(k_op), k_op),
    )
    assert sub(r_op, matmul(r_column, transpose(r_column))) == add(
        b_op, add(contraction_remainder, rank_one_remainder)
    )

    y_column = as_column(flatten(y))
    w_column = as_column(flatten(w))
    y_plus_kw = add(y_column, matmul(k_op, w_column))
    completed_base = (
        hs_norm2(y_plus_kw)
        + hs_norm2(matmul(cd, y_column))
        + hs_inner(w_column, matmul(r_op, w_column))
    )
    direct_base = (
        hs_norm2(y)
        + hs_norm2(w)
        + hs_norm2(cross(y, d))
        + hs_norm2(cross(w, z))
        + 2 * hs_inner(cross(y, z), cross(w, d))
    )
    assert completed_base == direct_base
    split_scalar = (
        hs_inner(d_column, y_plus_kw)
        + hs_inner(r_column, w_column)
    )
    assert split_scalar == p_scalar + q_scalar
    # The full scalar-dual defect is base - |t|^2/2: one third comes
    # from the traceless projections and one sixth from z/sqrt(6).
    assert defect_58 - (p_scalar + q_scalar) ** 2 / 6 == (
        direct_base - (p_scalar + q_scalar) ** 2 / 2
    )

    # Exact algebra behind the diagonal determinant-gap theorem.
    # q=(0,9/25,16/25) is the squared Naimark-complement vector of the
    # rational Parseval frame [(1,0,0),(0,4/5,-3/5)].
    q0, q1, q2 = F(0), F(9, 25), F(16, 25)
    e2 = q0 * q1 + q0 * q2 + q1 * q2
    e3 = q0 * q1 * q2
    determinant_rho = (1 - q0) * (1 - q1) * (1 - q2)
    assert determinant_rho == e2 - e3
    # If nu is a root of 3 nu^2 - 2 nu + e2=0, then formally
    # 2 nu - det(rho) = 3 nu^2 + e3.  The coefficient vector of the
    # difference (constant, linear, quadratic) is exactly the negative of
    # the defining polynomial, so no algebraic-number package is needed.
    claimed_difference = (
        -determinant_rho - e3,
        F(2),
        F(-3),
    )
    negative_defining_polynomial = (-e2, F(2), F(-3))
    assert claimed_difference == negative_defining_polynomial

    print("verified exact n=2 tangent/singular-pencil identities")
    print("verified exact 9x9 Schur reduction at a=3/5, b=4/5")
    print("verified equality with nonzero full mixed Hodge cross product")
    print("verified exact four-channel Hodge--Fierz reduction")
    print("verified exact polarized Hodge one-scalar collapse")
    print("verified exact obstruction to the decoupled one-variable bound")
    print("verified exact rank-two qutrit reduction certificates")
    print("verified universal polynomial identity in the qutrit spectral proof")
    print("verified exact mixed-Lagrange row-contraction bridge")
    print("verified exact strong reversed-Hodge operator factorization")
    print("verified exact full scalar-dual normalization")
    print("verified exact diagonal determinant-gap algebra")


if __name__ == "__main__":
    main()
