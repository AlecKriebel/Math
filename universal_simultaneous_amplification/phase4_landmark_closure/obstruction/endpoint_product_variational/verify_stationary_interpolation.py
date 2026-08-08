#!/usr/bin/env python3
"""Exact determinant screens for stationary orientation interpolation.

For ``Q_s=M+sK`` let ``m(s)`` be the stationary mean cardinality.  The
universal statement

    m(s) + m(-s) <= 2 m(0),  0 <= s <= 1,

is open.  This program does not assert it universally.  It constructs the
rooted-tree normalizer and marked normalizer as exact rational polynomials,
checks the conjecture by a Bernstein certificate on several hostile graphs,
and verifies the independently supplied weighted-P3 closed form.
"""

from __future__ import annotations

from math import comb

from flint import fmpq, fmpq_poly

from verify_root_marked_tree_transform import generators, stationary


def rational(value) -> fmpq:
    return fmpq(value.numerator, value.denominator)


def bareiss_determinant(matrix: list[list[fmpq_poly]]) -> fmpq_poly:
    """Fraction-free determinant over Q[x]."""
    work = [row[:] for row in matrix]
    n = len(work)
    previous = fmpq_poly([1])
    sign = 1
    for column in range(n - 1):
        pivot_row = next(
            row for row in range(column, n) if work[row][column]
        )
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign = -sign
        pivot = work[column][column]
        for row in range(column + 1, n):
            lower = work[row][column]
            for j in range(column + 1, n):
                work[row][j] = (
                    work[row][j] * pivot - lower * work[column][j]
                ) / previous
            work[row][column] = fmpq_poly([])
        previous = pivot
    return sign * work[-1][-1]


def tree_polynomials(weights: tuple[tuple[int, ...], ...]):
    """Return T(x),Y(x) for Q_x=(1-x)C+xL.

    The rank-one determinant identity gives T as the total Markov-tree
    weight and Y as the same total with the root cardinality marked.
    """
    left, reverse = generators(weights)
    size = len(left)
    minus_generator = [
        [
            fmpq_poly(
                [
                    -rational(reverse[i][j]),
                    -rational(left[i][j] - reverse[i][j]),
                ]
            )
            for j in range(size)
        ]
        for i in range(size)
    ]
    answer = []
    for mark_rank in (False, True):
        regularized = [row[:] for row in minus_generator]
        for state in range(size):
            mark = (state + 1).bit_count() if mark_rank else 1
            regularized[state][-1] += fmpq_poly([mark])
        answer.append(bareiss_determinant(regularized))
    return tuple(answer)


def even_gap_polynomial(weights: tuple[tuple[int, ...], ...]):
    """Return the cleared numerator in y=s^2 and its Bernstein coefficients."""
    tree_x, marked_x = tree_polynomials(weights)
    # x=(1+s)/2.
    x_of_s = fmpq_poly([fmpq(1, 2), fmpq(1, 2)])
    tree = tree_x(x_of_s)
    marked = marked_x(x_of_s)
    minus_s = fmpq_poly([0, -1])
    tree_minus = tree(minus_s)
    marked_minus = marked(minus_s)
    midpoint_mean = marked(fmpq(0)) / tree(fmpq(0))
    numerator_s = (
        2 * midpoint_mean * tree * tree_minus
        - marked * tree_minus
        - marked_minus * tree
    )
    coefficients_s = numerator_s.coeffs()
    assert all(
        index % 2 == 0 or coefficient == 0
        for index, coefficient in enumerate(coefficients_s)
    )
    coefficients_y = [
        coefficients_s[2 * degree]
        if 2 * degree < len(coefficients_s)
        else fmpq(0)
        for degree in range(numerator_s.degree() // 2 + 1)
    ]
    numerator_y = fmpq_poly(coefficients_y)
    degree = numerator_y.degree()
    bernstein = [
        sum(
            (
                coefficients_y[j]
                * fmpq(comb(k, j), comb(degree, j))
                for j in range(k + 1)
            ),
            fmpq(0),
        )
        for k in range(degree + 1)
    ]
    return tree, marked, numerator_s, numerator_y, bernstein


def polynomial(coefficients: list[int]) -> fmpq_poly:
    return fmpq_poly(coefficients)


def exact_skew_ground_state_check(
    weights: tuple[tuple[int, ...], ...], interpolation
) -> None:
    """Check the skew/defect split and geometric-product orthogonality."""
    from fractions import Fraction as F

    left, reverse = generators(weights)
    size = len(left)
    n = len(weights)
    degree = [sum(row) for row in weights]
    p = [[F(weights[i][j], degree[i]) for j in range(n)] for i in range(n)]
    q_vertex = [
        F(1) - sum((p[j][i] for j in range(n)), F(0)) for i in range(n)
    ]
    mu = [F(1, 2) ** state.bit_count() for state in range(1, size + 1)]
    normalizer = sum(mu, F(0))
    mu = [value / normalizer for value in mu]
    midpoint = [
        [(left[i][j] + reverse[i][j]) / 2 for j in range(size)]
        for i in range(size)
    ]
    defect = [
        [(left[i][j] - reverse[i][j]) / 2 for j in range(size)]
        for i in range(size)
    ]
    potential = [
        F(3, 2)
        * sum(
            (q_vertex[i] for i in range(n) if (state >> i) & 1), F(0)
        )
        for state in range(1, size + 1)
    ]

    def adjoint(matrix):
        return [
            [mu[j] * matrix[j][i] / mu[i] for j in range(size)]
            for i in range(size)
        ]

    defect_adjoint = adjoint(defect)
    skew = [row[:] for row in defect]
    for i in range(size):
        skew[i][i] -= potential[i] / 2
    skew_adjoint = adjoint(skew)
    for i in range(size):
        for j in range(size):
            expected = -defect[i][j] + (potential[i] if i == j else 0)
            assert defect_adjoint[i][j] == expected
            assert skew_adjoint[i][j] == -skew[i][j]

    plus = [
        [midpoint[i][j] + interpolation * defect[i][j] for j in range(size)]
        for i in range(size)
    ]
    minus = [
        [midpoint[i][j] - interpolation * defect[i][j] for j in range(size)]
        for i in range(size)
    ]
    density_plus = [
        stationary(plus)[i] / mu[i] for i in range(size)
    ]
    density_minus = [
        stationary(minus)[i] / mu[i] for i in range(size)
    ]

    def apply(matrix, vector):
        return [
            sum((matrix[i][j] * vector[j] for j in range(size)), F(0))
            for i in range(size)
        ]

    ground_plus = [row[:] for row in midpoint]
    ground_minus = [row[:] for row in midpoint]
    for i in range(size):
        for j in range(size):
            ground_plus[i][j] -= interpolation * skew[i][j]
            ground_minus[i][j] += interpolation * skew[i][j]
        ground_plus[i][i] += interpolation * potential[i] / 2
        ground_minus[i][i] -= interpolation * potential[i] / 2
    assert apply(ground_plus, density_plus) == [F(0)] * size
    assert apply(ground_minus, density_minus) == [F(0)] * size

    def inner(first, second):
        return sum(
            (mu[i] * first[i] * second[i] for i in range(size)), F(0)
        )

    product_orthogonality = sum(
        (
            mu[i]
            * potential[i]
            * density_plus[i]
            * density_minus[i]
            for i in range(size)
        ),
        F(0),
    )
    assert product_orthogonality == 0

    midpoint_plus = apply(midpoint, density_plus)
    midpoint_minus = apply(midpoint, density_minus)
    energy_plus = -inner(density_plus, midpoint_plus)
    energy_minus = -inner(density_minus, midpoint_minus)
    potential_square_plus = sum(
        (mu[i] * potential[i] * density_plus[i] ** 2 for i in range(size)),
        F(0),
    )
    potential_square_minus = sum(
        (mu[i] * potential[i] * density_minus[i] ** 2 for i in range(size)),
        F(0),
    )
    assert energy_plus == interpolation * potential_square_plus / 2
    assert energy_minus == -interpolation * potential_square_minus / 2
    assert energy_plus >= 0 and energy_minus >= 0


def main() -> None:
    from fractions import Fraction as F

    path = (
        (0, 0, 1),
        (0, 0, 1),
        (1, 1, 0),
    )
    four_star = tuple(
        tuple(1 if (i == 3) != (j == 3) else 0 for j in range(4))
        for i in range(4)
    )
    five_star = tuple(
        tuple(1 if (i == 4) != (j == 4) else 0 for j in range(5))
        for i in range(5)
    )
    sparse_k4 = (
        (0, 1, 1, 1),
        (1, 0, 0, 0),
        (1, 0, 0, 3),
        (1, 0, 3, 0),
    )
    all_mark_witness = (
        (0, 1000, 1, 0, 10),
        (1000, 0, 0, 1000, 10000),
        (1, 0, 0, 1, 1000),
        (0, 1000, 1, 0, 1),
        (10, 10000, 1000, 1, 0),
    )

    for name, weights in (
        ("P3", path),
        ("K1,3", four_star),
        ("sparse K4", sparse_k4),
        ("K1,4", five_star),
        ("all-mark witness", all_mark_witness),
    ):
        tree, _, numerator_s, _, bernstein = even_gap_polynomial(weights)
        assert tree(fmpq(1)) > 0 and tree(fmpq(-1)) > 0
        assert bernstein[0] == 0
        assert all(coefficient >= 0 for coefficient in bernstein)
        assert numerator_s(fmpq(1)) > 0
        print(f"PASS: exact Bernstein interpolation certificate on {name}")

    exact_skew_ground_state_check(sparse_k4, F(2, 3))
    print("PASS: exact skew split, Dirichlet squares, and <V f_s f_-s>=0")

    # First-order stochastic domination of the entire rank law is too
    # strong.  At s=1/5 this integer graph has a positive excess at the full
    # set, although its mean cardinality still has the conjectured deficit.
    tail_witness = (
        (0, 2, 227000, 0, 0),
        (2, 0, 536000, 5, 85),
        (227000, 536000, 0, 941000, 650000),
        (0, 5, 941000, 0, 1),
        (0, 85, 650000, 1, 0),
    )
    tail_left, tail_reverse = generators(tail_witness)
    tail_s = F(1, 5)
    tail_midpoint = [
        [(tail_left[i][j] + tail_reverse[i][j]) / 2 for j in range(31)]
        for i in range(31)
    ]
    tail_defect = [
        [(tail_left[i][j] - tail_reverse[i][j]) / 2 for j in range(31)]
        for i in range(31)
    ]
    tail_plus = [
        [tail_midpoint[i][j] + tail_s * tail_defect[i][j] for j in range(31)]
        for i in range(31)
    ]
    tail_minus = [
        [tail_midpoint[i][j] - tail_s * tail_defect[i][j] for j in range(31)]
        for i in range(31)
    ]
    tail_average = [
        (first + second) / 2
        for first, second in zip(stationary(tail_plus), stationary(tail_minus))
    ]
    tail_mu = [F(1, 2) ** state.bit_count() for state in range(1, 32)]
    tail_mu = [value / sum(tail_mu, F(0)) for value in tail_mu]
    full_set_excess = tail_average[-1] - tail_mu[-1]
    mean_deficit = sum(
        (
            (tail_mu[state - 1] - tail_average[state - 1])
            * state.bit_count()
            for state in range(1, 32)
        ),
        F(0),
    )
    assert F(4, 1_000_000) < full_set_excess < F(5, 1_000_000)
    assert F(3, 1000) < mean_deficit < F(4, 1000)
    print("PASS: exact cumulative-tail counterexample with positive mean deficit")

    # Weighted path with edge weights 1 and 17.  This independently checks
    # the supplied closed form by cross multiplication rather than sampling.
    weighted_path = (
        (0, 0, 1),
        (0, 0, 17),
        (1, 17, 0),
    )
    tree, marked, gap_numerator, _, bernstein = even_gap_polynomial(weighted_path)
    s = fmpq_poly([0, 1])
    mean_numerator = 9 * polynomial(
        [-378102375, 226502325, 37489390, -10128106, 127993, 6069]
    )
    mean_denominator = (
        (s - 15)
        * polynomial([-12635, 804, 119])
        * polynomial([-12635, 6564, 119])
    )
    assert marked * mean_denominator == tree * mean_numerator

    positive_even_factor = polynomial(
        [
            512931826072509375,
            -26138588919354700,
            294010589876522,
            -836686233964,
            257829327,
        ]
    )(s * s)
    reduced_gap_numerator = -72 * s * s * positive_even_factor
    reduced_gap_denominator = 19 * (s - 15) * (s + 15)
    for linear in (804, 6564):
        reduced_gap_denominator *= polynomial([-12635, linear, 119])
        reduced_gap_denominator *= polynomial([-12635, -linear, 119])
    tree_minus = tree(fmpq_poly([0, -1]))
    assert (
        gap_numerator * reduced_gap_denominator
        == reduced_gap_numerator * tree * tree_minus
    )
    assert all(coefficient >= 0 for coefficient in bernstein)
    # On 0<=y<=1, the constant term alone exceeds the magnitudes of both
    # negative coefficients, so the displayed quartic factor is positive.
    assert (
        fmpq(512931826072509375)
        - fmpq(26138588919354700)
        - fmpq(836686233964)
        > 0
    )
    print("PASS: exact weighted-P3 rational formula and interval sign")
    print("STATUS: universal stationary interpolation inequality remains OPEN")


if __name__ == "__main__":
    main()
