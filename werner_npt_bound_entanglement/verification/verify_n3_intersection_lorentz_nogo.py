#!/usr/bin/env python3
"""Exact rational verification of the intersection-one Lorentz no-go."""

from fractions import Fraction as F


def main() -> None:
    m = F(1, 8)
    a = F(1, 4)

    # Pauli-coordinate coefficients in
    # g(x)=g0*x0^2+g1*x1^2+g2*x2^2+g3*x3^2.
    gram = (F(3, 4), F(1, 4), F(1, 4), F(1, 4))

    # In the Hilbert--Schmidt orthonormal Pauli basis the eigenvalues
    # are gram[mu]/2, so the exact global floor is 1/8.
    hs_eigenvalues = tuple(value / 2 for value in gram)
    assert min(hs_eigenvalues) == m

    # For P_n=(I+n.sigma)/2, g(P_n)=1/4 independently of n.
    projector_energy = gram[0] / 4 + gram[1] / 4
    assert projector_energy == F(1, 4)
    delta_w = a - m
    delta_x = projector_energy - m
    assert delta_w == delta_x == F(1, 8)

    # t(P_n)=(-1+3*n1)/16.  Its exact range is [-1/4,1/8],
    # saturating the shifted lower bound and the sharper orthogonal
    # upper bound.
    t_min = F(-1 - 3, 16)
    t_max = F(-1 + 3, 16)
    assert t_min == F(-1, 4)
    assert t_max == m
    assert t_min == -m - F(1, 8)

    # h(P_n)=3(1+n1)(5-3*n1)/256 is nonnegative on [-1,1].
    # A quadratic concave in n1 attains its minimum at an endpoint.
    def null_defect(n1: F) -> F:
        return F(3, 256) * (1 + n1) * (5 - 3 * n1)

    assert null_defect(F(-1)) == 0
    assert null_defect(F(1)) == F(3, 64)

    # D=|0><1|=(X+iY)/2.
    dyad_energy = gram[1] / 4 + gram[2] / 4
    dyad_cross = F(3, 16)
    defect = a * dyad_energy - dyad_cross * dyad_cross
    assert dyad_energy == m
    assert defect == F(-1, 256)

    # G^Gamma=(I+F)/8 has a zero antisymmetric Rayleigh quotient,
    # so it violates the physical quantitative floor G^Gamma >= I/8.
    # On |01>-|10>, I contributes norm^2=2 and F contributes -2.
    antisymmetric_numerator = F(1, 8) * (2 - 2)
    required_floor_numerator = m * 2
    assert antisymmetric_numerator == 0
    assert required_floor_numerator == F(1, 4)
    assert antisymmetric_numerator < required_floor_numerator

    print("verified: real-null tests pass; complex-null defect = -1/256")


if __name__ == "__main__":
    main()
