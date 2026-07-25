#!/usr/bin/env python3
"""Exact verifier for four nested positive-height link bounds."""

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
    return [
        (left[i] if i < len(left) else Q(0))
        + (right[i] if i < len(right) else Q(0))
        for i in range(max(len(left), len(right)))
    ]


def scale(polynomial: list[Q], scalar: Q) -> list[Q]:
    return [scalar * value for value in polynomial]


def multiply(left: list[Q], right: list[Q]) -> list[Q]:
    result = [Q(0)] * (len(left) + len(right) - 1)
    for i, first in enumerate(left):
        for j, second in enumerate(right):
            result[i + j] += first * second
    return result


def linear(root: Q) -> list[Q]:
    return [-root, Q(1)]


def component_polynomial(component: dict[str, object]) -> list[Q]:
    scale_value = Q(component["scale"])
    check(scale_value > 0, "component scale is not positive")
    simple_root = Q(component["simple_root"])
    polynomial = linear(simple_root)
    for value in component["double_roots"]:
        factor = linear(Q(value))
        polynomial = multiply(polynomial, multiply(factor, factor))
    center = Q(component["center"])
    offset = Q(component["offset"])
    check(offset > 0, "quadratic offset is not positive")
    quadratic = multiply(linear(center), linear(center))
    quadratic[0] += offset
    return scale(multiply(polynomial, quadratic), scale_value)


def gegenbauer_basis(maximum_degree: int) -> list[list[Q]]:
    """Normalized Gegenbauer polynomials on S^3."""
    values = [[Q(1)]]
    if maximum_degree:
        values.append([Q(0), Q(1)])
    for degree in range(2, maximum_degree + 1):
        first = [Q(0)] + scale(
            values[-1], Q(2 * degree, degree + 1)
        )
        second = scale(values[-2], Q(-(degree - 1), degree + 1))
        values.append(add(first, second))
    check(
        all(sum(polynomial) == 1 for polynomial in values),
        "Gegenbauer normalization failed",
    )
    return values


def expand_in_basis(polynomial: list[Q]) -> list[Q]:
    basis = gegenbauer_basis(len(polynomial) - 1)
    residual = polynomial[:]
    coefficients = [Q(0)] * len(basis)
    for degree in range(len(basis) - 1, -1, -1):
        coefficients[degree] = (
            residual[degree] / basis[degree][degree]
        )
        for index, value in enumerate(basis[degree]):
            residual[index] -= coefficients[degree] * value
    check(all(value == 0 for value in residual), "basis expansion failed")
    return coefficients


def projected_maximum(height: Q) -> Q:
    return (Q(1, 2) - height * height) / (1 - height * height)


def verify(path: Path) -> dict[str, object]:
    certificate = json.loads(path.read_text())
    check(
        certificate.get("schema")
        == "kissing5.local_positive_height_ladder.v1",
        "wrong schema",
    )
    check(certificate.get("ambient_dimension") == 5, "wrong dimension")
    check(certificate.get("projected_dimension") == 4, "wrong projection")
    expected = {
        Q(3, 10): 22,
        Q(1, 3): 21,
        Q(3, 8): 20,
        Q(2, 5): 19,
    }
    bounds = certificate["bounds"]
    check(len(bounds) == len(expected), "wrong number of bounds")
    seen: set[Q] = set()
    objectives: dict[str, str] = {}
    for entry in bounds:
        height = Q(entry["anchor_height"])
        check(height in expected and height not in seen, "wrong height")
        seen.add(height)
        maximum = projected_maximum(height)
        check(
            maximum == Q(entry["projected_maximum"]),
            "wrong projected maximum",
        )
        polynomial = [Q(0)]
        for component in entry["components"]:
            simple_root = Q(component["simple_root"])
            check(
                simple_root >= maximum,
                "component sign is not certified on the full interval",
            )
            polynomial = add(
                polynomial, component_polynomial(component)
            )
        coefficients = expand_in_basis(polynomial)
        stored = [Q(value) for value in entry["gegenbauer_coefficients"]]
        check(coefficients == stored, "stored coefficient mismatch")
        check(
            all(value > 0 for value in coefficients),
            "nonpositive Gegenbauer coefficient",
        )
        f_at_one = sum(polynomial)
        check(f_at_one == Q(entry["f_at_one"]), "wrong f(1)")
        objective = f_at_one / coefficients[0]
        check(
            objective == Q(entry["delsarte_objective"]),
            "wrong Delsarte objective",
        )
        integer_bound = entry["integer_bound"]
        check(integer_bound == expected[height], "wrong integer bound")
        check(
            objective < integer_bound + 1,
            "objective does not prove the integer bound",
        )
        objectives[str(height)] = str(objective)
    check(seen == set(expected), "missing height")
    return {
        "status": "PASS",
        "integer_bounds": {
            str(height): bound for height, bound in expected.items()
        },
        "objectives": objectives,
        "boundary_scope": "closed heights and contact inequalities",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "certificate",
        nargs="?",
        type=Path,
        default=ROOT / "certificates" / "local_positive_height_ladder.json",
    )
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate), indent=2))


if __name__ == "__main__":
    main()
