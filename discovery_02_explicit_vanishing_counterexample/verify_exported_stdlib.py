#!/usr/bin/env python3
"""Dependency-free exact check of the exported polynomial and collision.

This checker deliberately does not import SymPy or construction.py.  It reads
only the two JSON certificates, differentiates the sparse polynomial, and
evaluates Z-gradient(P) at both points using Gaussian rationals.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def gaussian(real=0, imag=0):
    return Fraction(real), Fraction(imag)


def parse_gaussian(data):
    return Fraction(data["real"]), Fraction(data["imag"])


def add(left, right):
    return left[0] + right[0], left[1] + right[1]


def neg(value):
    return -value[0], -value[1]


def sub(left, right):
    return add(left, neg(right))


def mul(left, right):
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def scale(integer, value):
    return integer * value[0], integer * value[1]


def power(value, exponent):
    result = gaussian(1)
    base = value
    while exponent:
        if exponent & 1:
            result = mul(result, base)
        base = mul(base, base)
        exponent //= 2
    return result


def gradient(terms, point, number_of_variables):
    result = [gaussian() for _ in range(number_of_variables)]
    for term in terms:
        coefficient = parse_gaussian(term["coefficient"])
        powers = dict(term["powers"])
        for differentiated_variable, exponent in powers.items():
            value = scale(exponent, coefficient)
            for variable, variable_exponent in powers.items():
                remaining = variable_exponent - (variable == differentiated_variable)
                value = mul(value, power(point[variable], remaining))
            result[differentiated_variable] = add(
                result[differentiated_variable], value
            )
    return result


def main():
    sparse = json.loads((ROOT / "output" / "potential_sparse.json").read_text())
    collision = json.loads((ROOT / "output" / "collision.json").read_text())

    assert sparse["field"] == "Q(i)"
    assert sparse["degree"] == 4
    assert sparse["number_of_terms"] == 598 == len(sparse["terms"])
    assert all(sum(exponent for _, exponent in term["powers"]) == 4
               for term in sparse["terms"])
    assert collision["variables"] == sparse["variables"]
    number_of_variables = len(sparse["variables"])
    assert number_of_variables == 54

    points = [
        [parse_gaussian(coordinate) for coordinate in point]
        for point in collision["points"]
    ]
    assert len(points) == 2 and points[0] != points[1]

    images = []
    for point in points:
        derivative = gradient(sparse["terms"], point, number_of_variables)
        images.append([sub(point[j], derivative[j]) for j in range(54)])
    assert images[0] == images[1]

    print("Dependency-free exported-certificate check passed:")
    print("  homogeneous quartic in 54 variables with 598 terms")
    print("  two distinct exact Q(i)-points collide under Z-gradient(P)")


if __name__ == "__main__":
    main()

