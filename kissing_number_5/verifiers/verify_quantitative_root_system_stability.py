#!/usr/bin/env python3
"""Exact arithmetic checks for quantitative_root_system_stability.md."""

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "certificates" / "quantitative_root_system_stability.json"


def frac(record):
    return Fraction(record["numerator"], record["denominator"])


def main():
    data = json.loads(CERT.read_text())

    eta = frac(data["eta"])
    assert eta == Fraction(1, 7200)

    column_bound = frac(data["determinant_column_norm_bound"])
    difference_factor = frac(data["determinant_difference_column_norm_factor"])
    assert column_bound == Fraction(3001, 1000)
    assert difference_factor == Fraction(49, 20)
    # Actual columns have at most one diagonal 2 and five entries bounded by
    # 1+eta under the rounding contradiction.
    assert column_bound * column_bound > 4 + 5 * (1 + eta) ** 2
    assert difference_factor * difference_factor > 6
    determinant_bound = 6 * difference_factor * column_bound**5
    assert determinant_bound < data["determinant_lipschitz_upper_bound"]
    assert determinant_bound * eta < Fraction(1, 2)

    q_gap = frac(data["root_alphabet_defect_lower_bound"])
    epsilon = frac(data["h_energy_gap"])
    assert q_gap == eta * eta
    assert epsilon == q_gap / 32
    assert epsilon == Fraction(1, 1658880000)

    # Constants in the midpoint-robust estimate:
    # kappa_r=(r-1)/2+(41-2r)/3.
    for r in (16, 17, 18):
        expected = Fraction(r - 1, 2) + Fraction(41 - 2 * r, 3)
        assert frac(data["robust_kappa"][str(r)]) == expected

    # Exact constants used in the collision transfer.
    rounded_lambda_lower = Fraction(1, 6**4)
    actual_lambda_lower = rounded_lambda_lower - 4 * eta
    assert actual_lambda_lower == Fraction(7, 32400)
    assert actual_lambda_lower > Fraction(1, 5000)
    assert 100000 * eta * eta == Fraction(5, 2592)
    assert 100000 * eta * eta < 2

    # Verify the two scalar inequalities on their compact intervals by
    # exact polynomial factorization/reduction.
    #
    # For x in [0,1/4]:
    # x^2(1/4-x^2) >= x^2/8.
    assert Fraction(1, 4) - Fraction(1, 4) ** 2 >= Fraction(1, 8)
    # For x in [1/4,1/2], delta=1/2-x <=1/4:
    # x^2(1/2+x)delta >= (3/64)delta >= delta^2/8.
    assert Fraction(1, 4) ** 2 * Fraction(3, 4) == Fraction(3, 64)
    assert Fraction(3, 64) >= Fraction(1, 4) / 8
    # h'(t)=4t^3-t/2 is increasing on [1/2,1] and h'(1)=7/2.
    assert 12 * Fraction(1, 2) ** 2 - Fraction(1, 2) > 0
    assert 4 - Fraction(1, 2) == Fraction(7, 2)

    print("quantitative root-system stability certificate: PASS")
    print("eta =", eta)
    print("epsilon =", epsilon, "~", float(epsilon))


if __name__ == "__main__":
    main()
