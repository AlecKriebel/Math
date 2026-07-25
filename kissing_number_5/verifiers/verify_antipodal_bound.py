#!/usr/bin/env python3
"""Exact standard-library checks for the antipodal dimension-five bound."""

from fractions import Fraction as Q


def add(a: tuple[Q, ...], b: tuple[Q, ...]) -> tuple[Q, ...]:
    n = max(len(a), len(b))
    return tuple(
        (a[i] if i < len(a) else Q(0))
        + (b[i] if i < len(b) else Q(0))
        for i in range(n)
    )


def scale(a: tuple[Q, ...], c: Q) -> tuple[Q, ...]:
    return tuple(c * x for x in a)


def shift(a: tuple[Q, ...]) -> tuple[Q, ...]:
    return (Q(0),) + a


def normalized_gegenbauer(degree: int) -> list[tuple[Q, ...]]:
    """Return P_0,...,P_degree as coefficient tuples in ascending powers."""

    if degree < 0:
        raise ValueError("degree must be nonnegative")
    p = [(Q(1),)]
    if degree == 0:
        return p
    p.append((Q(0), Q(1)))
    for k in range(2, degree + 1):
        numerator = add(
            scale(shift(p[k - 1]), Q(2 * k + 1)),
            scale(p[k - 2], Q(-(k - 1))),
        )
        p.append(scale(numerator, Q(1, k + 2)))
    return p


def dot(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x * y for x, y in zip(a, b, strict=True))


def d5_line_representatives() -> tuple[tuple[int, ...], ...]:
    """Integer numerators for (e_i +/- e_j)/sqrt(2), one per line."""

    rows = []
    for i in range(5):
        for j in range(i + 1, 5):
            for sign in (-1, 1):
                row = [0] * 5
                row[i] = 1
                row[j] = sign
                rows.append(tuple(row))
    return tuple(rows)


def verify() -> dict[str, object]:
    p = normalized_gegenbauer(4)
    assert p[0] == (Q(1),)
    assert p[2] == (Q(-1, 4), Q(0), Q(5, 4))
    assert p[4] == (Q(1, 8), Q(0), Q(-7, 4), Q(0), Q(21, 8))

    # f(t) = t^4 - t^2/4.
    f = (Q(0), Q(0), Q(-1, 4), Q(0), Q(1))
    expansion = add(
        add(scale(p[0], Q(1, 28)), scale(p[2], Q(1, 3))),
        scale(p[4], Q(8, 21)),
    )
    assert expansion == f
    f_one = sum(f, Q(0))
    assert f_one == Q(3, 4)
    assert f_one / Q(1, 28) == 21

    def evaluate(poly: tuple[Q, ...], t: Q) -> Q:
        value = Q(0)
        for coefficient in reversed(poly):
            value = value * t + coefficient
        return value

    assert evaluate(f, Q(-1, 2)) == 0
    assert evaluate(f, Q(0)) == 0
    assert evaluate(f, Q(1, 2)) == 0
    # Since f=t^2(t^2-1/4), these endpoint/root checks accompany the exact
    # factored sign proof in the manuscript; no numerical grid is used.

    assert evaluate(p[2], Q(1)) == 1
    assert evaluate(p[2], Q(0)) == Q(-1, 4)
    assert evaluate(p[2], Q(1, 2)) == Q(1, 16)
    assert evaluate(p[2], Q(-1, 2)) == Q(1, 16)
    row_numerators = [
        Q(1) + Q(b, 16) - Q(20 - b, 4)
        for b in range(21)
    ]
    assert all(value != 0 for value in row_numerators)
    assert Q(64, 5).denominator != 1

    lines = d5_line_representatives()
    assert len(lines) == 20
    assert len(set(lines)) == 20
    assert all(dot(row, row) == 2 for row in lines)
    maximum_abs_integer_dot = max(
        abs(dot(lines[i], lines[j]))
        for i in range(len(lines))
        for j in range(i + 1, len(lines))
    )
    assert maximum_abs_integer_dot == 1

    return {
        "line_upper_bound_before_equality_elimination": 21,
        "forbidden_row_count": Q(64, 5),
        "d5_line_count": len(lines),
        "maximum_absolute_inner_product": Q(maximum_abs_integer_dot, 2),
        "antipodal_point_count": 2 * len(lines),
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
