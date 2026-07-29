#!/usr/bin/env python3
"""Exact replay for the quadratic-subproduct parity audit.

This verifier has two independent finite models.

1. A rank-two projection Q on C^2 tensor C^2 has
       dim E_1,E_2,E_3,E_4 = 2,2,1,0.
   Spectator amplification by C^s therefore has the exceptional-shaped
   dimensions 2s,2s^2,s^3,0 for every s.  Q has only one scalar
   partial trace and is not an exceptional Yang--Baxter solution.

2. A rank-eight projection P on C^4 tensor C^4 has both scalar partial
   traces, dim E_3=2 (not divisible by 4), and E_4=0.  It too is not an
   exceptional Yang--Baxter solution.

All arithmetic is exact over Q(sqrt(2), i).
"""

from __future__ import annotations

import sympy as sp


I = sp.I
SQRT2 = sp.sqrt(2)


def kron(*factors: sp.Matrix) -> sp.Matrix:
    out = factors[0]
    for factor in factors[1:]:
        out = sp.kronecker_product(out, factor)
    return out


def hs_norm_squared(matrix: sp.Matrix) -> sp.Expr:
    return sp.simplify(sp.trace(matrix.H * matrix))


def partial_trace_two_site(
    matrix: sp.Matrix, local_dimension: int, traced_site: int
) -> sp.Matrix:
    """Unnormalized partial trace of a two-site operator."""

    d = local_dimension
    out = sp.zeros(d)
    if traced_site == 2:
        for i in range(d):
            for j in range(d):
                out[i, j] = sp.simplify(
                    sum(matrix[d * i + k, d * j + k] for k in range(d))
                )
    elif traced_site == 1:
        for i in range(d):
            for j in range(d):
                out[i, j] = sp.simplify(
                    sum(matrix[d * k + i, d * k + j] for k in range(d))
                )
    else:
        raise ValueError("traced_site must be 1 or 2")
    return out


def intersection_dimension(projections: list[sp.Matrix]) -> int:
    """Dimension of the common range of exact orthogonal projections."""

    ambient = projections[0].rows
    constraints = sp.Matrix.vstack(
        *(sp.eye(ambient) - projection for projection in projections)
    )
    return ambient - constraints.rank()


def base_one_sided_model() -> tuple[sp.Matrix, list[int], sp.Expr]:
    ket0 = sp.Matrix([1, 0])
    ket1 = sp.Matrix([0, 1])
    ket_plus = (ket0 + ket1) / SQRT2

    # W = span{|0>|1>, |+>|0>}.
    inclusion = sp.Matrix.hstack(kron(ket0, ket1), kron(ket_plus, ket0))
    assert sp.simplify(inclusion.H * inclusion) == sp.eye(2)
    projection = sp.simplify(inclusion * inclusion.H)
    assert sp.simplify(projection.H - projection) == sp.zeros(4)
    assert sp.simplify(projection * projection - projection) == sp.zeros(4)
    assert projection.rank() == 2

    marginal_first = partial_trace_two_site(projection, 2, 1)
    marginal_second = partial_trace_two_site(projection, 2, 2)
    expected_nonscalar = sp.Matrix(
        [[sp.Rational(3, 2), sp.Rational(1, 2)],
         [sp.Rational(1, 2), sp.Rational(1, 2)]]
    )
    assert marginal_first == sp.eye(2)
    assert marginal_second == expected_nonscalar

    p12 = kron(projection, sp.eye(2))
    p23 = kron(sp.eye(2), projection)
    e3_dimension = intersection_dimension([p12, p23])

    p1 = kron(projection, sp.eye(4))
    p2 = kron(sp.eye(2), projection, sp.eye(2))
    p3 = kron(sp.eye(4), projection)
    e4_dimension = intersection_dimension([p1, p2, p3])

    dimensions = [1, 2, projection.rank(), e3_dimension, e4_dimension]
    assert dimensions == [1, 2, 2, 1, 0]

    residual = sp.simplify(
        p12 * p23 * p12
        - p23 * p12 * p23
        - sp.Rational(1, 3) * (p12 - p23)
    )
    residual_squared = hs_norm_squared(residual)
    assert residual_squared == sp.Rational(13, 36)
    return projection, dimensions, residual_squared


def standard_rank_nondivisibility_model() -> tuple[sp.Matrix, int, int, sp.Expr]:
    ket0 = sp.Matrix([1, 0])
    ket1 = sp.Matrix([0, 1])
    ket_plus = (ket0 + ket1) / SQRT2
    colors = [ket0, ket1]

    pauli_x = sp.Matrix([[0, 1], [1, 0]])
    pauli_y = sp.Matrix([[0, -I], [I, 0]])
    pauli_z = sp.diag(1, -1)
    identity = sp.eye(2)

    c_reflection = (pauli_x + pauli_z) / SQRT2
    k_reflection = (
        pauli_y + (pauli_x - pauli_z) / SQRT2
    ) / SQRT2
    left_rotation = (identity - I * pauli_x) / SQRT2

    assert sp.simplify(c_reflection * c_reflection) == identity
    assert sp.simplify(k_reflection * k_reflection) == identity
    assert sp.simplify(
        k_reflection * c_reflection + c_reflection * k_reflection
    ) == sp.zeros(2)
    assert sp.simplify(left_rotation.H * left_rotation) == identity

    unitaries = [
        [identity, k_reflection],
        [left_rotation, sp.simplify(left_rotation * k_reflection)],
    ]

    # Local ordering is color tensor qubit.  In color block (a,b), use
    # (U_ab tensor I)W, where W is the base rank-two subspace.
    columns: list[sp.Matrix] = []
    for a in range(2):
        for b in range(2):
            u_ab = unitaries[a][b]
            columns.append(
                kron(colors[a], u_ab * ket0, colors[b], ket1)
            )
            columns.append(
                kron(colors[a], u_ab * ket_plus, colors[b], ket0)
            )

    inclusion = sp.Matrix.hstack(*columns)
    assert sp.simplify(inclusion.H * inclusion) == sp.eye(8)
    projection = sp.simplify(inclusion * inclusion.H)
    assert sp.simplify(projection.H - projection) == sp.zeros(16)
    assert sp.simplify(projection * projection - projection) == sp.zeros(16)
    assert projection.rank() == 8

    marginal_first = partial_trace_two_site(projection, 4, 1)
    marginal_second = partial_trace_two_site(projection, 4, 2)
    assert marginal_first == 2 * sp.eye(4)
    assert marginal_second == 2 * sp.eye(4)

    p12 = kron(projection, sp.eye(4))
    p23 = kron(sp.eye(4), projection)
    e3_dimension = intersection_dimension([p12, p23])
    assert e3_dimension == 2
    assert e3_dimension % 4 != 0

    p1 = kron(projection, sp.eye(16))
    p2 = kron(sp.eye(4), projection, sp.eye(4))
    p3 = kron(sp.eye(16), projection)
    e4_dimension = intersection_dimension([p1, p2, p3])
    assert e4_dimension == 0

    residual = sp.simplify(
        p12 * p23 * p12
        - p23 * p12 * p23
        - sp.Rational(1, 3) * (p12 - p23)
    )
    residual_squared = hs_norm_squared(residual)
    assert residual_squared == sp.Rational(95, 36)
    return projection, e3_dimension, e4_dimension, residual_squared


def koszul_series_audit() -> list[sp.Expr]:
    s = sp.symbols("s", positive=True, integer=True)
    # Coefficients of 1 / (1 - 2 s t + 2 s^2 t^2 - s^3 t^3).
    coefficients = [sp.Integer(1)]
    for n in range(1, 7):
        value = 2 * s * coefficients[n - 1]
        if n >= 2:
            value -= 2 * s**2 * coefficients[n - 2]
        if n >= 3:
            value += s**3 * coefficients[n - 3]
        coefficients.append(sp.factor(value))
    expected = [
        1,
        2 * s,
        2 * s**2,
        s**3,
        0,
        0,
        s**6,
    ]
    assert coefficients == expected
    return coefficients


def main() -> None:
    _, base_dimensions, base_residual = base_one_sided_model()
    _, e3_dimension, e4_dimension, standard_residual = (
        standard_rank_nondivisibility_model()
    )
    koszul_coefficients = koszul_series_audit()

    print("PASS exact one-sided-standard quadratic subproduct model")
    print(f"base Hilbert dimensions E_0..E_4 = {base_dimensions}")
    print(
        "spectator dimensions = "
        "1, 2s, 2s^2, s^3, 0 for every positive integer s"
    )
    print(f"base exceptional-cubic residual squared = {base_residual}")
    print("PASS exact fully standard rank-nondivisibility model")
    print(f"d = 4, rank(P) = 8, dim(E_3) = {e3_dimension}")
    print(f"dim(E_4) = {e4_dimension}")
    print(f"exceptional-cubic residual squared = {standard_residual}")
    print("PASS exact Koszul-series obstruction")
    print(f"coefficients through degree 6 = {koszul_coefficients}")


if __name__ == "__main__":
    main()
