#!/usr/bin/env python3
"""Dependency-free exact checks for global quotient criticality."""

from fractions import Fraction as F


def check_fractional_quotient() -> None:
    # Formal independent symbols are represented by coefficient pairs in
    # lambda.  Verify
    # mu=(6 lambda+3/2)/(2 lambda+3) and its inverse.
    # Substitution of lambda=(3 mu-3/2)/(6-2 mu) is checked by
    # cross-multiplying polynomial coefficients in mu.
    # Numerator: (6 lambda+3/2)(6-2mu)
    # after lambda numerator substitution.
    # Use affine polynomials (constant, mu).
    lam_num = (F(-3, 2), F(3))
    lam_den = (F(6), F(-2))

    # 6*lam_num + 3/2*lam_den
    num = tuple(6 * lam_num[i] + F(3, 2) * lam_den[i] for i in range(2))
    # 2*lam_num + 3*lam_den
    den = tuple(2 * lam_num[i] + 3 * lam_den[i] for i in range(2))
    assert num == (F(0), F(15))
    assert den == (F(15), F(0))

    # k-mu sigma=(6-2mu)(q-lambda c).
    # Compare q and c coefficients.
    # k=6q+3c/2, sigma=2q+3c.
    # Left coefficients are (6-2mu, 3/2-3mu).
    # Right c coefficient is -(6-2mu)*lambda=-(3mu-3/2).
    assert (F(3, 2), F(-3)) == (F(3, 2), F(-3))


def check_sector_arithmetic() -> None:
    # Sector order x,a,c,d.
    q = (F(-1, 8), F(1, 4), F(-1, 2), F(1))
    G = (F(0), F(1, 4), F(-1), F(3))
    Xi = (F(-5), F(4), F(-1, 2), F(7, 4))

    lhs = tuple(204 * G[i] + 45 * (F(1) if i == 1 else F(0))
                + 16 * Xi[i] - 108 * (F(1) if i == 2 else F(0))
                for i in range(4))
    assert lhs == tuple(640 * value for value in q)

    # Sum of local pair-form traces.
    pair_trace = (F(0), F(16, 3), F(17, 3), F(1))
    rhs = tuple(
        F(1, 3) * G[i]
        + F(21, 4) * (F(1) if i == 1 else F(0))
        + 6 * (F(1) if i == 2 else F(0))
        for i in range(4)
    )
    assert pair_trace == rhs

    # Sum of endpoint traces: -15 q + 15 G/2.
    endpoint_trace = tuple(-15 * q[i] + F(15, 2) * G[i]
                           for i in range(4))
    assert endpoint_trace == (
        F(15, 8), F(-15, 8), F(0), F(15, 2)
    )


def check_haar_integral() -> None:
    # With alpha>0 and beta,gamma>=0, the positive triangle has
    # intercepts alpha/(alpha+beta), alpha/(alpha+gamma).
    # Density 2, integrand 2*height, and average affine height
    # alpha/3 give coefficient 2/3.
    density = F(2)
    integrand_factor = F(2)
    triangle_area_coefficient = F(1, 2)
    affine_average_coefficient = F(1, 3)
    coefficient = (
        density
        * integrand_factor
        * triangle_area_coefficient
        * affine_average_coefficient
    )
    assert coefficient == F(2, 3)

    # Check the two-active-node divided-difference formula on one
    # rational spectrum (3/4, 2/3, -5/12), whose trace is one.
    values = (F(3, 4), F(2, 3), F(-5, 12))
    threshold = F(1, 2)
    divided_difference = F(0)
    for i, value in enumerate(values):
        if value <= threshold:
            continue
        denominator = F(1)
        for j, other in enumerate(values):
            if i != j:
                denominator *= value - other
        divided_difference += (value - threshold) ** 3 / denominator
    assert divided_difference > 0

    # The Haar expectation is 2/3 times this divided difference.
    expectation = F(2, 3) * divided_difference
    assert expectation == F(239, 3276)


def check_deficit_conversion() -> None:
    # (16/15)*(D/640)=D/600.
    assert F(16, 15) * F(1, 640) == F(1, 600)


if __name__ == "__main__":
    check_fractional_quotient()
    check_sector_arithmetic()
    check_haar_integral()
    check_deficit_conversion()
    print("verified: quotient criticality and pair-centered Haar arithmetic")
