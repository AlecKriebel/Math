#!/usr/bin/env python3
"""Exact Q(sqrt(3)) verifier for the cap-Hall counterexample."""

from fractions import Fraction
import json
import sys

from support import ROOTS, completion_roots


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


class Quad:
    """An element ``a + b sqrt(3)`` with exact rational coefficients."""

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = Fraction(a)
        self.b = Fraction(b)

    def __add__(self, other):
        other = as_quad(other)
        return Quad(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Quad(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-as_quad(other))

    def __rsub__(self, other):
        return as_quad(other) - self

    def __mul__(self, other):
        other = as_quad(other)
        return Quad(
            self.a * other.a + 3 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    __rmul__ = __mul__

    def sign(self):
        if not self.b:
            return (self.a > 0) - (self.a < 0)
        if not self.a:
            return (self.b > 0) - (self.b < 0)
        if (self.a > 0) == (self.b > 0):
            return 1 if self.a > 0 else -1
        comparison = self.a * self.a - 3 * self.b * self.b
        if comparison > 0:
            return 1 if self.a > 0 else -1
        if comparison < 0:
            return 1 if self.b > 0 else -1
        return 0

    def __le__(self, other):
        return (self - other).sign() <= 0

    def __lt__(self, other):
        return (self - other).sign() < 0

    def __ge__(self, other):
        return (self - other).sign() >= 0

    def __gt__(self, other):
        return (self - other).sign() > 0

    def __eq__(self, other):
        try:
            other = as_quad(other)
        except (TypeError, ValueError):
            return False
        return self.a == other.a and self.b == other.b

    def __repr__(self):
        return "Quad(%r, %r)" % (self.a, self.b)


def as_quad(value):
    if isinstance(value, Quad):
        return value
    return Quad(value)


def dot(left, right):
    return sum(as_quad(a) * as_quad(b) for a, b in zip(left, right))


def verify():
    half = Fraction(1, 2)
    root_three_over_two = Quad(0, half)
    plus = (
        Quad(half),
        -root_three_over_two,
        Quad(0),
        -root_three_over_two,
        Quad(half),
    )
    minus = (
        Quad(-half),
        -root_three_over_two,
        Quad(0),
        -root_three_over_two,
        Quad(-half),
    )
    require(dot(plus, plus) == 2, "plus point has wrong scaled norm")
    require(dot(minus, minus) == 2, "minus point has wrong scaled norm")
    require(dot(plus, minus) == 1, "mutual scaled dot product is not one")

    for point in (plus, minus):
        for root in ROOTS:
            require(dot(root, point) <= 1, "support polar inequality failed")

    completion = completion_roots()
    neighborhoods = []
    full_conflicts = []
    for point in (plus, minus):
        neighborhood = tuple(
            root for root in completion if dot(root, point) >= Fraction(3, 2)
        )
        neighborhoods.append(neighborhood)
        full_conflicts.append(
            tuple(
                index
                for index, root in enumerate(completion)
                if dot(root, point) > 1
            )
        )
    expected_root = (0, -1, 0, -1, 0)
    require(neighborhoods[0] == (expected_root,), "plus neighborhood not singleton")
    require(neighborhoods[1] == (expected_root,), "minus neighborhood not singleton")
    height = dot(expected_root, plus) * half
    require(height == root_three_over_two, "central cap height mismatch")
    require(height > Fraction(3, 4), "central cap height not strictly above 3/4")
    require(
        full_conflicts[0] == (2, 9, 12, 17, 25),
        "plus full conflict set mismatch",
    )
    require(
        full_conflicts[1] == (0, 8, 12, 16, 24),
        "minus full conflict set mismatch",
    )
    require(
        set(full_conflicts[0]) & set(full_conflicts[1]) == {12},
        "full conflict intersection mismatch",
    )
    require(
        len(set(full_conflicts[0]) | set(full_conflicts[1])) == 9,
        "full conflict union mismatch",
    )

    other_maxima = []
    for point in (plus, minus):
        values = [
            dot(root, point)
            for root in completion
            if root != expected_root
        ]
        maximum = values[0]
        for value in values[1:]:
            if value > maximum:
                maximum = value
        require(maximum == Quad(half, half), "unexpected other-root maximum")
        require(maximum < Fraction(3, 2), "another root enters cap neighborhood")
        other_maxima.append(maximum)

    return {
        "status": "PROVED_EXACT_ALGEBRAIC_COUNTEREXAMPLE",
        "mutual_inner_product": "1/2",
        "shared_unique_center": list(expected_root),
        "center_height": "sqrt(3)/2",
        "largest_other_scaled_dot": "(1+sqrt(3))/2",
        "neighborhood_union_size": 1,
        "full_conflict_degrees": [5, 5],
        "full_conflict_intersection_size": 1,
        "full_conflict_union_size": 9,
        "points": 2,
    }


def main(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    require(not arguments, "usage: verify_hall_counterexample.py")
    print(json.dumps(verify(), sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print("VERIFICATION FAILED: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
