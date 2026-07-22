#!/usr/bin/env python3
"""Primary exact SymPy verifier for Discovery 06."""

from __future__ import annotations

from math import comb, factorial

import sympy as sp

from construction import build_construction, evaluate, homogeneous_companion, map_T


def main() -> None:
    data = build_construction()
    x, y, z = data.base_variables
    assert len(data.variables) == len(data.g) == len(data.xi_variables) == 14
    assert data.B.shape == (3, 11) and data.N.shape == (11, 11)
    assert data.N**5 == sp.zeros(11)
    polynomial = sp.Poly(data.A, *(data.xi_variables + data.variables))
    assert len(polynomial.terms()) == 24 and polynomial.total_degree() == 8
    assert data.B.rank() == 3 and data.N.rank() == 8
    print("[1/8] construction: 14 pairs, chain lengths 2/4/5, A has 24 terms and degree 8")

    # The source map is the normalized announced map (F3/2,F2,F1).
    u = 1 + x * y
    source = (
        sp.expand((2 * x - 3 * x**2 * y - x**3 * z) / 2),
        sp.expand(y + 3 * x * u**2 * z + 3 * x * y**2 * (4 + 3 * x * y)),
        sp.expand(u**3 * z + y**2 * u * (4 + 3 * x * y)),
    )
    assert all(sp.expand(left - right) == 0 for left, right in zip(data.phi, source))
    assert sp.factor(sp.Matrix(data.phi).jacobian(data.base_variables).det()) == 1
    print("[2/8] source: Phi=(F3/2,F2,F1), det(JPhi)=1")

    # Exact Schur-complement polynomial-matrix identity.  The inverse is a
    # finite sum because N^5=0.
    s = sp.Symbol("s")
    jh2 = sp.Matrix(data.homogeneous_parts[0]).jacobian(data.base_variables)
    jc = data.C.jacobian(data.base_variables)
    jacobian = sp.Matrix(data.g).jacobian(data.variables)
    inverse = sum((s**power * data.N**power for power in range(5)), sp.zeros(11))
    full_pencil = sp.eye(14) + s * jacobian
    assert full_pencil[:3, :3] == sp.eye(3) + s * jh2
    assert full_pencil[:3, 3:] == s * data.B
    assert full_pencil[3:, :3] == -s * jc
    assert full_pencil[3:, 3:] == sp.eye(11) - s * data.N
    assert (sp.eye(11) - s * data.N) * inverse == sp.eye(11)
    assert (sp.eye(11) - s * data.N).det() == 1
    schur = sp.eye(3) + s * jh2 + s**2 * data.B * inverse * jc
    scaled = {variable: s * variable for variable in data.base_variables}
    target = sp.Matrix(data.phi).jacobian(data.base_variables).subs(scaled, simultaneous=True)
    assert all(sp.expand(entry) == 0 for entry in schur - target)
    print("[3/8] determinant pencil: det(I+s*Jg)=det(JPhi(sX))=1")

    images = [evaluate(map_T(data), data.variables, point) for point in data.collision_points]
    expected = (0, 0, sp.Rational(-1, 4)) + (0,) * 11
    assert len(set(data.collision_points)) == 3
    assert images == [expected] * 3
    assert tuple(point[0] for point in data.collision_points) == (0, 1, -1)
    print("[4/8] collision: three rational points map to (0,0,-1/4,0,...,0)")

    # Cayley--Hamilton applied to the already certified determinant pencil
    # gives (Jg)^14=0.  A single targeted row computation proves sharpness
    # without expanding fourteen full symbolic matrix powers.
    power_row = sp.zeros(1, 14)
    power_row[0, 0] = 1
    for _ in range(13):
        power_row = (power_row * jacobian).applyfunc(sp.factor)
    assert sp.factor(power_row[0, 4]) == -3 * x**6 * y**4 * z
    print("[5/8] regular nilpotency: Cayley-Hamilton gives (Jg)^14=0; (Jg)^13 != 0")

    # SIC coefficient certificate.  If tau+t*tau^3=t/2 and q(t) is the
    # specialization of b at the inverse, the three summands tau', -3*tau,
    # and -(tau'-1/2)/t occupy distinct residue classes modulo three.
    def coefficient(m: int) -> sp.Rational:
        if m % 3 == 0:
            k = m // 3
            return sp.Rational((-1) ** k * comb(3 * k + 1, k), 2 ** (2 * k + 1))
        if m % 3 == 1:
            k = (m - 1) // 3
            return sp.Rational(
                (-1) ** (k + 1) * 3 * comb(3 * k + 1, k),
                (3 * k + 1) * 2 ** (2 * k + 1),
            )
        k = (m - 2) // 3
        return sp.Rational(
            (-1) ** k * comb(3 * k + 4, k + 1), 2 ** (2 * k + 3)
        )

    t = sp.Symbol("t")
    order = 25
    tau = sp.S.Zero
    # t-adic fixed-point iteration doubles as an implementation-independent
    # check of the Lagrange-inversion formulas through order 24.
    for _ in range(order):
        tau = sp.series(t * (sp.Rational(1, 2) - tau**3), t, 0, order + 2).removeO()
    assert sp.series(tau + t * tau**3 - t / 2, t, 0, order + 1).removeO() == 0
    q = sp.diff(tau, t) - 3 * tau - (sp.diff(tau, t) - sp.Rational(1, 2)) / t
    for m in range(order + 1):
        assert sp.expand(q).coeff(t, m) == coefficient(m)
        assert coefficient(m) != 0
        assert factorial(m) * coefficient(m) != 0
    print("[6/8] SIC(14): explicit q_m is nonzero in every residue class for all m>=0")

    # Minimality inside the stated constant-state realization ansatz.  Treat
    # every tail monomial as an independent input and form the finite block
    # Hankel matrices of its exact coefficient matrices.
    tail_parts = data.homogeneous_parts[1:]
    monomials = []
    for part in tail_parts:
        for component in part:
            for monomial, coefficient_value in sp.Poly(component, *data.base_variables).terms():
                if coefficient_value != 0 and monomial not in monomials:
                    monomials.append(monomial)
    assert len(monomials) == 11
    markov = []
    for part in tail_parts:
        matrix = sp.zeros(3, len(monomials))
        for row, component in enumerate(part):
            coefficients = dict(sp.Poly(component, *data.base_variables).terms())
            for column, monomial in enumerate(monomials):
                matrix[row, column] = coefficients.get(monomial, 0)
        markov.append(matrix)
    markov.extend([sp.zeros(3, len(monomials))] * 5)
    hankel_ranks = []
    leading_hankel = None
    for shift in range(5):
        block_count = 5 - shift
        hankel = sp.Matrix.vstack(
            *[
                sp.Matrix.hstack(
                    *[markov[shift + row + column] for column in range(block_count)]
                )
                for row in range(block_count)
            ]
        )
        if shift == 0:
            leading_hankel = hankel
        hankel_ranks.append(hankel.rank())
    assert hankel_ranks == [11, 8, 5, 3, 1]
    selected_rows = [0, 1, 2, 3, 4, 5, 7, 8, 10, 11, 14]
    assert leading_hankel is not None
    assert leading_hankel.extract(selected_rows, list(range(11))).det() == 275562
    print("[7/8] ansatz optimality: coefficient-Hankel ranks 11,8,5,3,1")

    h_variables, h = homogeneous_companion(data)
    assert len(h_variables) == len(h) == 15
    h_poly = [sp.Poly(component, *h_variables) for component in h if component != 0]
    assert all(poly.is_homogeneous and poly.total_degree() == 7 for poly in h_poly)
    assert sum(len(poly.terms()) for poly in h_poly) == 24
    jh = sp.Matrix(h).jacobian(h_variables)
    h13_row = sp.zeros(1, 15)
    h13_row[0, 0] = 1
    for _ in range(13):
        h13_row = (h13_row * jh).applyfunc(sp.factor)
    assert sp.factor(h13_row[0, 4]) == -3 * h_variables[-1] ** 67 * x**6 * y**4 * z
    lifted = [point + (sp.Rational(1),) for point in data.collision_points]
    lifted_map = tuple(v + component for v, component in zip(h_variables, h))
    lifted_images = [evaluate(lifted_map, h_variables, point) for point in lifted]
    assert lifted_images == [expected + (1,)] * 3
    print("[8/8] homogeneous companion: 15D, degree 7, 24 terms, index >=14, same collision")
    print("All exact symbolic checks passed.")


if __name__ == "__main__":
    main()
