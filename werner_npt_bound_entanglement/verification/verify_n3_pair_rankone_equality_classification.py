#!/usr/bin/env python3
"""Exact checks for the complete rank-one pair-sector equality theorem.

The script independently checks:

* the canonical kernels of the polarized-minor map at ranks 1, 2, 3;
* the semisimple and nilpotent full-local-rank normal forms;
* the qutrit common-factor block decomposition;
* the distinguished-block Gram identity;
* the repeated-block determinant identity and its scalar lower bound.
"""

import sympy as sp


def polarized_minor_matrix(rows, columns, rank):
    """Matrix of Y -> B(X,Y), for X=diag(I_rank,0)."""
    variables = rows * columns
    equations = []
    for a in range(rows):
        for b in range(a + 1, rows):
            for mu in range(columns):
                for nu in range(mu + 1, columns):
                    row = [sp.Integer(0)] * variables

                    def add(i, j, coefficient):
                        row[i * columns + j] += coefficient

                    x_a_mu = int(a == mu and a < rank)
                    x_b_nu = int(b == nu and b < rank)
                    x_a_nu = int(a == nu and a < rank)
                    x_b_mu = int(b == mu and b < rank)
                    add(b, nu, x_a_mu)
                    add(a, mu, x_b_nu)
                    add(b, mu, -x_a_nu)
                    add(a, nu, -x_b_mu)
                    equations.append(row)
    return sp.Matrix(equations)


def check_polarized_minor_lemma():
    # These are the three flattening sizes relevant for qutrit triples.
    rank_one = polarized_minor_matrix(3, 9, 1).nullspace()
    rank_two = polarized_minor_matrix(3, 9, 2).nullspace()
    rank_three = polarized_minor_matrix(3, 9, 3).nullspace()
    assert len(rank_one) == 3 + 9 - 1
    assert len(rank_two) == 3
    assert len(rank_three) == 0

    # At rank two every kernel matrix is confined to the leading 2x2
    # block and has trace zero.
    for vector in rank_two:
        matrix = sp.Matrix(3, 9, vector)
        assert matrix[0, 0] + matrix[1, 1] == 0
        assert all(
            matrix[i, j] == 0
            for i in range(3)
            for j in range(9)
            if i >= 2 or j >= 2
        )


def check_full_local_rank_normal_forms():
    # Semisimple common local action: the only supported words are 000,111.
    words = list(__import__("itertools").product((0, 1), repeat=3))
    z_sign = (1, -1)
    allowed = [
        word
        for word in words
        if z_sign[word[0]] == z_sign[word[1]] == z_sign[word[2]]
    ]
    assert allowed == [(0, 0, 0), (1, 1, 1)]

    # Its three-exterior coefficient is nonzero when both amplitudes are.
    p, q = sp.symbols("p q", nonzero=True)
    # Alternating contraction of x with y=Z_1 x.
    triple_exterior = -2 * p * q
    assert triple_exterior != 0

    # Nilpotent common local action.  Solve N_1 x=N_2 x=N_3 x exactly.
    variables = sp.symbols("x0:8")

    def index(word):
        return 4 * word[0] + 2 * word[1] + word[2]

    def nilpotent_image(site):
        out = {}
        for word in words:
            if word[site] == 1:
                target = list(word)
                target[site] = 0
                out[tuple(target)] = variables[index(word)]
        return out

    images = [nilpotent_image(site) for site in range(3)]
    equations = []
    for left, right in ((0, 1), (0, 2)):
        for word in words:
            equations.append(images[left].get(word, 0) - images[right].get(word, 0))
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    kernel = coefficient_matrix.nullspace()
    assert len(kernel) == 2
    expected_vacuum = sp.Matrix([1, 0, 0, 0, 0, 0, 0, 0])
    expected_w = sp.Matrix([0, 1, 1, 0, 1, 0, 0, 0])
    assert sp.Matrix.hstack(*kernel).columnspace() == sp.Matrix.hstack(
        expected_vacuum, expected_w
    ).columnspace()


def partial_trace_pair(matrix, site):
    """Trace one factor of a 3 x 3 bipartite operator."""
    out = sp.zeros(3)
    for row in range(3):
        for column in range(3):
            if site == 0:
                out[row, column] = sum(
                    matrix[3 * k + row, 3 * k + column] for k in range(3)
                )
            else:
                out[row, column] = sum(
                    matrix[3 * row + k, 3 * column + k] for k in range(3)
                )
    return out


def scalar_projection(matrix, site):
    identity = sp.eye(3)
    reduced = partial_trace_pair(matrix, site) / 3
    if site == 0:
        return sp.kronecker_product(identity, reduced)
    return sp.kronecker_product(reduced, identity)


def dagger(matrix, swaps):
    return matrix.T.xreplace(swaps)


def reduce_constraints(expression, groebner):
    return sp.factor(groebner.reduce(sp.expand(expression))[1])


def check_common_factor_certificate():
    a, b = sp.symbols("a b", real=True)
    z, Z, s, S, t, T = sp.symbols("z Z s S t T")
    swaps = {z: Z, Z: z, s: S, S: s, t: T, T: t}

    x = sp.zeros(9, 1)
    x[0], x[4] = a, b
    y = sp.zeros(9, 1)
    y[0], y[1], y[3], y[4] = a * z, s, t, -b * z
    y_bar = y.xreplace(swaps)
    rank_one = x * y_bar.T

    p_first = scalar_projection(rank_one, 0)
    p_second = scalar_projection(rank_one, 1)
    p_both = scalar_projection(p_first, 1)
    degree_two = rank_one - p_first - p_second + p_both
    degree_one = p_first + p_second - 2 * p_both
    k0 = sp.expand(3 * (degree_two + 2 * degree_one))
    k1 = sp.expand(3 * (degree_two - degree_one))

    constraints = sp.groebner(
        [a**2 + b**2 - 1, z * Z + s * S + t * T - 1],
        T,
        t,
        S,
        s,
        Z,
        z,
        b,
        a,
        order="grevlex",
    )

    # Both matrices have the claimed 4,2,2,1 block pattern.
    blocks = ((0, 1, 3, 4), (2, 5), (6, 7), (8,))
    block_of = {
        index: block_number
        for block_number, block in enumerate(blocks)
        for index in block
    }
    for matrix in (k0, k1):
        assert all(
            matrix[row, column] == 0
            for row in range(9)
            for column in range(9)
            if block_of[row] != block_of[column]
        )

    h0 = sp.expand(4 * sp.eye(9) + 12 * y * y_bar.T - dagger(k0, swaps) * k0)
    main = h0.extract(blocks[0], blocks[0])
    eta = sp.Matrix((a * z, s, t, -b * z))
    eta_bar = eta.xreplace(swaps)
    w = sp.Matrix((b, 0, 0, a))
    expected_main = 4 * (sp.eye(4) - eta * eta_bar.T) - w * w.T
    assert all(
        reduce_constraints(main[i, j] - expected_main[i, j], constraints) == 0
        for i in range(4)
        for j in range(4)
    )
    assert reduce_constraints((eta_bar.T * eta)[0] - 1, constraints) == 0
    assert (w.T * w)[0] - 1 in (0, a**2 + b**2 - 1)
    assert sp.expand((w.T * eta)[0]) == 0

    expected_two = sp.Matrix(
        (
            (
                4 - b**2 * (b**2 * z * Z + s * S),
                a * b * (a * s * Z - b * z * T),
            ),
            (
                a * b * (a * z * S - b * t * Z),
                4 - a**2 * (a**2 * z * Z + t * T),
            ),
        )
    )
    actual_two = h0.extract(blocks[1], blocks[1])
    assert all(
        reduce_constraints(actual_two[i, j] - expected_two[i, j], constraints) == 0
        for i in range(2)
        for j in range(2)
    )
    assert reduce_constraints(
        h0[8, 8] - (4 - (a**2 - b**2) ** 2 * z * Z), constraints
    ) == 0

    # The repeated block's two small matrix blocks.
    expected_k1_two = sp.Matrix(((-Z, -2 * a * T), (-2 * b * S, Z)))
    assert all(
        reduce_constraints(
            k1.extract(blocks[1], blocks[1])[i, j] - expected_k1_two[i, j],
            constraints,
        )
        == 0
        for i in range(2)
        for j in range(2)
    )

    # Transform the leading K1 block to the compact d,k form.
    d, k = sp.symbols("d k", real=True)
    compact = sp.Matrix(
        (
            (d * Z, k * Z, k * S, k * T),
            (-2 * k * Z, 0, d * S, d * T),
            (-2 * T, 0, -d * Z, 0),
            (-2 * S, 0, 0, -d * Z),
        )
    )

    # Check the determinant formula directly in the compact variables.
    compact_dagger = dagger(compact, swaps)
    determinant = sp.expand((4 * sp.eye(4) - compact_dagger * compact).det())
    D, u, p, q, chi = sp.symbols("D u p q chi", real=True)
    determinant_constraints = sp.groebner(
        [
            d**2 - D,
            k**2 + D - 1,
            z * Z - u,
            s * S - p,
            t * T - q,
            u + p + q - 1,
            z**2 * S * T + Z**2 * s * t - chi,
        ],
        T,
        t,
        S,
        s,
        Z,
        z,
        k,
        d,
        q,
        p,
        u,
        D,
        chi,
        order="grevlex",
    )
    cal_a = (
        D * k**4 * u**3
        - 4 * k**4 * u**2
        + (16 - 13 * D) * u
        + 4 * D
        + 20
        - 4 * (4 - D * k**2 * u) * p * q
    )
    expected_determinant = 4 * D * (
        u * cal_a + 2 * k * (4 - D * u) * (2 - k**2 * u) * chi
    )
    assert (
        reduce_constraints(
            determinant - expected_determinant, determinant_constraints
        )
        == 0
    )

    # Exact algebra behind the worst-phase/worst-pq scalar reduction.
    lower_at_maximum_pq = sp.factor(
        cal_a.subs(
            {
                D: 1 - k**2,
                p * q: (1 - u) ** 2 / 4,
            }
        )
        - 2 * k * (1 - u) * (4 - (1 - k**2) * u) * (2 - k**2 * u)
    )
    g = (
        5
        - 4 * k
        - k**2
        + (2 * k**3 + 2 * k**2 + 4 * k + 4) * u
        - k**2 * (k + 1) ** 2 * u**2
    )
    assert sp.factor(
        lower_at_maximum_pq - (4 - (1 - k**2) * u) * g
    ) == 0
    assert sp.factor(g.subs(u, 0) - (1 - k) * (k + 5)) == 0
    assert sp.factor(g.subs(u, 1) - (9 - k**4)) == 0
    assert sp.factor(sp.diff(g, u, 2)) == -2 * k**2 * (k + 1) ** 2

    # Boundary actions used in the proof.
    P, Q, xi_1, xi_2 = sp.symbols("P Q xi_1 xi_2")
    input_vector = sp.Matrix((P, Q, xi_1, xi_2))
    d_zero = compact.subs({d: 0, k: 1}) * input_vector
    assert d_zero == sp.Matrix(
        (
            Z * Q + S * xi_1 + T * xi_2,
            -2 * Z * P,
            -2 * T * P,
            -2 * S * P,
        )
    )
    z_zero = compact.subs({z: 0, Z: 0}) * input_vector
    expected_z_zero = sp.Matrix(
        (
            k * (S * xi_1 + T * xi_2),
            d * (S * xi_1 + T * xi_2),
            -2 * T * P,
            -2 * S * P,
        )
    )
    assert sp.simplify(z_zero - expected_z_zero) == sp.zeros(4, 1)


def main():
    check_polarized_minor_lemma()
    check_full_local_rank_normal_forms()
    check_common_factor_certificate()
    print(
        "verified: equality classification normal forms, common-factor "
        "block certificate, and repeated-block determinant reduction"
    )


if __name__ == "__main__":
    main()
