#!/usr/bin/env python3
"""Dependency-free exact check of the exported 44D collision certificate."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def parse_number(data):
    return Fraction(data["real"]), Fraction(data["imag"])


def add(left, right):
    return left[0] + right[0], left[1] + right[1]


def sub(left, right):
    return left[0] - right[0], left[1] - right[1]


def mul(left, right):
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def scale(integer, value):
    return integer * value[0], integer * value[1]


def power(value, exponent):
    result = (Fraction(1), Fraction(0))
    base = value
    while exponent:
        if exponent & 1:
            result = mul(result, base)
        base = mul(base, base)
        exponent //= 2
    return result


def gradient(terms, point, dimension):
    result = [(Fraction(0), Fraction(0)) for _ in range(dimension)]
    for term in terms:
        coefficient = parse_number(term["coefficient"])
        powers = dict(term["powers"])
        for variable, exponent in powers.items():
            value = scale(exponent, coefficient)
            for factor, factor_exponent in powers.items():
                value = mul(value, power(point[factor], factor_exponent - (factor == variable)))
            result[variable] = add(result[variable], value)
    return result


def hessian_at_origin(terms, dimension):
    origin = [(Fraction(0), Fraction(0)) for _ in range(dimension)]
    result = [[(Fraction(0), Fraction(0)) for _ in range(dimension)] for _ in range(dimension)]
    for term in terms:
        coefficient = parse_number(term["coefficient"])
        powers = dict(term["powers"])
        for first in powers:
            for second in powers:
                remaining = dict(powers)
                factor = remaining[first]
                remaining[first] -= 1
                second_factor = remaining.get(second, 0)
                if second_factor == 0:
                    continue
                factor *= second_factor
                remaining[second] -= 1
                value = scale(factor, coefficient)
                for variable, exponent in remaining.items():
                    value = mul(value, power(origin[variable], exponent))
                result[first][second] = add(result[first][second], value)
    return result


def main():
    meng_sparse = json.loads(
        (ROOT / "output" / "symmetric_potential_sparse.json").read_text()
    )
    meng_collision = json.loads(
        (ROOT / "output" / "symmetric_collision.json").read_text()
    )
    sparse = json.loads((ROOT / "output" / "potential_sparse.json").read_text())
    collision = json.loads((ROOT / "output" / "collision.json").read_text())

    assert meng_sparse["field"] == "Q(i)"
    assert meng_sparse["degree"] == 8
    assert meng_sparse["number_of_terms"] == 204 == len(meng_sparse["terms"])
    assert len(meng_sparse["variables"]) == 6
    assert meng_collision["variables"] == meng_sparse["variables"]
    meng_points = [
        [parse_number(value) for value in point]
        for point in meng_collision["points"]
    ]
    assert len(meng_points) == 3 and len(set(map(tuple, meng_points))) == 3
    meng_images = [gradient(meng_sparse["terms"], point, 6) for point in meng_points]
    assert meng_images[0] == meng_images[1] == meng_images[2]
    meng_hessian_origin = hessian_at_origin(meng_sparse["terms"], 6)
    assert meng_hessian_origin == [
        [(Fraction(i == j), Fraction(0)) for j in range(6)] for i in range(6)
    ]

    assert sparse["field"] == "Q(i)"
    assert sparse["degree"] == 4
    assert sparse["number_of_terms"] == 538 == len(sparse["terms"])
    assert len(sparse["variables"]) == 44
    assert all(
        sum(exponent for _, exponent in term["powers"]) == 4
        for term in sparse["terms"]
    )
    assert collision["variables"] == sparse["variables"]

    points = [[parse_number(value) for value in point] for point in collision["points"]]
    assert len(points) == 2 and points[0] != points[1]
    images = []
    for point in points:
        derivative = gradient(sparse["terms"], point, 44)
        images.append([sub(point[index], derivative[index]) for index in range(44)])
    assert images[0] == images[1]

    print("Dependency-free exported-certificate checks passed:")
    print("  degree-8 potential in 6 variables with 204 terms")
    print("  identity linear part and exact Q(i) three-point gradient fiber")
    print("  homogeneous quartic in 44 variables with 538 terms")
    print("  two distinct exact Q(i)-points collide under Z-gradient(P)")


if __name__ == "__main__":
    main()
