#!/usr/bin/env python3
"""Exact standard-library verifier for A(4, 7/15) <= 23."""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VerificationError(RuntimeError):
    pass


def check(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def add(left: list[Q], right: list[Q]) -> list[Q]:
    size = max(len(left), len(right))
    return [
        (left[index] if index < len(left) else Q(0))
        + (right[index] if index < len(right) else Q(0))
        for index in range(size)
    ]


def scale(polynomial: list[Q], scalar: Q) -> list[Q]:
    return [scalar * coefficient for coefficient in polynomial]


def multiply(left: list[Q], right: list[Q]) -> list[Q]:
    result = [Q(0)] * (len(left) + len(right) - 1)
    for i, first in enumerate(left):
        for j, second in enumerate(right):
            result[i + j] += first * second
    return result


def linear(root: Q) -> list[Q]:
    return [-root, Q(1)]


def normalized_gegenbauer_dimension_four(maximum_degree: int) -> list[list[Q]]:
    """Return P_k with P_k(1)=1 for the unit sphere in R^4."""

    values = [[Q(1)]]
    if maximum_degree:
        values.append([Q(0), Q(1)])
    for degree in range(2, maximum_degree + 1):
        first = [Q(0)] + scale(values[-1], Q(2 * degree, degree + 1))
        second = scale(values[-2], Q(-(degree - 1), degree + 1))
        values.append(add(first, second))
    check(
        all(sum(polynomial) == 1 for polynomial in values),
        "Gegenbauer normalization failed",
    )
    return values


def expand_in_basis(
    polynomial: list[Q], basis: list[list[Q]]
) -> list[Q]:
    residual = polynomial + [Q(0)] * (len(basis) - len(polynomial))
    coefficients = [Q(0)] * len(basis)
    for degree in range(len(basis) - 1, -1, -1):
        coefficients[degree] = (
            residual[degree] / basis[degree][degree]
        )
        for index, value in enumerate(basis[degree]):
            residual[index] -= coefficients[degree] * value
    check(all(value == 0 for value in residual), "basis expansion failed")
    return coefficients


def verify(path: Path) -> dict[str, object]:
    certificate = json.loads(path.read_text())
    check(
        certificate.get("schema") == "kissing5.a4_7_15_delsarte.v1",
        "wrong schema",
    )
    check(certificate.get("ambient_dimension") == 4, "wrong dimension")
    maximum = Q(certificate["maximum_inner_product"])
    check(maximum == Q(7, 15), "wrong maximum inner product")
    factors = certificate["factorization"]
    check(Q(factors["simple_root"]) == maximum, "wrong simple root")
    double_roots = [Q(value) for value in factors["double_roots"]]
    check(
        double_roots == [Q(-179, 200), Q(-67, 125), Q(-223, 1000)],
        "wrong double roots",
    )
    center = Q(factors["positive_quadratic_center"])
    offset = Q(factors["positive_quadratic_offset"])
    check(center == Q(27, 25) and offset == Q(1, 4), "wrong quadratic")
    check(offset > 0, "quadratic factor is not everywhere positive")

    polynomial = linear(maximum)
    for root in double_roots:
        polynomial = multiply(polynomial, multiply(linear(root), linear(root)))
    positive_quadratic = multiply(linear(center), linear(center))
    positive_quadratic[0] += offset
    polynomial = multiply(polynomial, positive_quadratic)
    check(len(polynomial) == 10, "unexpected polynomial degree")

    basis = normalized_gegenbauer_dimension_four(9)
    coefficients = expand_in_basis(polynomial, basis)
    stored_coefficients = [
        Q(value) for value in certificate["gegenbauer_coefficients"]
    ]
    check(coefficients == stored_coefficients, "coefficient mismatch")
    check(all(value > 0 for value in coefficients), "nonpositive coefficient")

    f_at_one = sum(polynomial)
    check(f_at_one == Q(certificate["f_at_one"]), "wrong f(1)")
    objective = f_at_one / coefficients[0]
    check(
        objective == Q(certificate["delsarte_objective"]),
        "wrong Delsarte objective",
    )
    check(objective < 24, "objective does not imply the integer bound")
    check(certificate["integer_bound"] == 23, "wrong integer bound")

    # The stored factorization proves f(t) <= 0 throughout [-1,7/15]:
    # its first factor is nonpositive, every doubled factor is nonnegative,
    # and the final quadratic is at least the positive offset.
    return {
        "status": "PASS",
        "maximum_inner_product": str(maximum),
        "strictly_positive_gegenbauer_coefficients": len(coefficients),
        "delsarte_objective": str(objective),
        "integer_bound": 23,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "certificate",
        nargs="?",
        type=Path,
        default=ROOT / "certificates" / "a4_7_15_delsarte.json",
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate), indent=2))


if __name__ == "__main__":
    main()
