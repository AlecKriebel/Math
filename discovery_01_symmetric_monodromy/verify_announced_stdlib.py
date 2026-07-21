#!/usr/bin/env python3
"""Dependency-free exact verification of the announced counterexample.

Polynomials are dictionaries mapping exponent triples to Fraction coefficients.
This deliberately does not use a computer algebra system.
"""

from fractions import Fraction


ZERO = (0, 0, 0)


def const(value):
    value = Fraction(value)
    return {} if value == 0 else {ZERO: value}


def variable(index):
    exponent = [0, 0, 0]
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def add(left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, Fraction(0)) + coefficient
        if out[monomial] == 0:
            del out[monomial]
    return out


def neg(poly):
    return {m: -c for m, c in poly.items()}


def sub(left, right):
    return add(left, neg(right))


def mul(left, right):
    out = {}
    for ml, cl in left.items():
        for mr, cr in right.items():
            monomial = tuple(a + b for a, b in zip(ml, mr))
            out[monomial] = out.get(monomial, Fraction(0)) + cl * cr
    return {m: c for m, c in out.items() if c}


def power(poly, exponent):
    out = const(1)
    base = poly
    while exponent:
        if exponent & 1:
            out = mul(out, base)
        base = mul(base, base)
        exponent //= 2
    return out


def scale(value, poly):
    return mul(const(value), poly)


def derivative(poly, index):
    out = {}
    for monomial, coefficient in poly.items():
        if monomial[index]:
            reduced = list(monomial)
            reduced[index] -= 1
            out[tuple(reduced)] = coefficient * monomial[index]
    return out


def evaluate(poly, point):
    return sum(
        coefficient
        * point[0] ** monomial[0]
        * point[1] ** monomial[1]
        * point[2] ** monomial[2]
        for monomial, coefficient in poly.items()
    )


def det3(matrix):
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return add(
        sub(mul(a, sub(mul(e, i), mul(f, h))),
            mul(b, sub(mul(d, i), mul(f, g)))),
        mul(c, sub(mul(d, h), mul(e, g))),
    )


def main():
    x, y, z = (variable(0), variable(1), variable(2))
    one_plus_xy = add(const(1), mul(x, y))
    four_plus_3xy = add(const(4), scale(3, mul(x, y)))

    first = add(
        mul(power(one_plus_xy, 3), z),
        mul(mul(power(y, 2), one_plus_xy), four_plus_3xy),
    )
    second = add(
        add(y, scale(3, mul(mul(x, power(one_plus_xy, 2)), z))),
        scale(3, mul(mul(mul(x, power(y, 2)), four_plus_3xy), const(1))),
    )
    third = sub(
        sub(scale(2, x), scale(3, mul(power(x, 2), y))),
        mul(power(x, 3), z),
    )
    mapping = (first, second, third)

    jacobian = [[derivative(component, j) for j in range(3)] for component in mapping]
    determinant = det3(jacobian)
    assert determinant == const(-2), determinant

    points = (
        (Fraction(0), Fraction(0), Fraction(-1, 4)),
        (Fraction(1), Fraction(-3, 2), Fraction(13, 2)),
        (Fraction(-1), Fraction(3, 2), Fraction(13, 2)),
    )
    target = (Fraction(-1, 4), Fraction(0), Fraction(0))
    for point in points:
        assert tuple(evaluate(component, point) for component in mapping) == target

    print("Dependency-free exact check passed:")
    print("  det JF = -2")
    print("  all three listed points map to (-1/4, 0, 0)")


if __name__ == "__main__":
    main()

