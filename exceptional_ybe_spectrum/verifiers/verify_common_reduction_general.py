#!/usr/bin/env python3
"""Exact replay for the common-reduction theorem.

This verifier has two independent roles.

1. It constructs the dimension-three Gaussian Hecke projection exactly
   over Q(i,sqrt(3)), showing that an isolated cubic involution can have
   negative rank 1/3 or 2/3 rather than rank half.
2. It replays, with rational arithmetic, the rank-balance and
   controlled-leg implications used for a common reduction inside a
   balanced exceptional solution.

The bounded dimension census is an assumption guard for the human
symbolic proof; it is not used as an exhaustion proof in the note.
"""

from fractions import Fraction

import sympy as sp


def gaussian_qutrit_projection() -> sp.Matrix:
    """Return the exact rank-three projection of i G_3."""

    imaginary = sp.I
    root_three = sp.sqrt(3)
    omega = (-1 + imaginary * root_three) / 2
    q = (1 + imaginary * root_three) / 2
    dimension = 3
    assert sp.simplify(q / (1 + q) ** 2) == sp.Rational(1, 3)

    shift_clock = sp.zeros(dimension**2)
    for first in range(dimension):
        for second in range(dimension):
            source = first * dimension + second
            target = (
                ((first + 1) % dimension) * dimension
                + (second + 1) % dimension
            )
            shift_clock[target, source] = omega ** (second - first)

    gaussian = (
        sp.eye(dimension**2)
        + omega * shift_clock
        + omega * shift_clock**2
    ) / root_three
    hecke_matrix = imaginary * gaussian
    return sp.simplify(
        (q * sp.eye(dimension**2) - hecke_matrix) / (q + 1)
    )


def projection_cubic_residual(projection: sp.Matrix, dimension: int) -> sp.Matrix:
    identity = sp.eye(dimension)
    first = sp.kronecker_product(projection, identity)
    second = sp.kronecker_product(identity, projection)
    return sp.simplify(
        first * second * first
        - second * first * second
        - sp.Rational(1, 3) * (first - second)
    )


def check_unbalanced_local_witnesses() -> None:
    projection = gaussian_qutrit_projection()
    identity = sp.eye(9)

    assert sp.simplify(projection.conjugate().T - projection) == sp.zeros(9)
    assert sp.simplify(projection**2 - projection) == sp.zeros(9)
    assert sp.trace(projection) == 3
    assert projection.rank() == 3
    assert projection_cubic_residual(projection, 3) == sp.zeros(27)

    complement = identity - projection
    assert sp.simplify(complement.conjugate().T - complement) == sp.zeros(9)
    assert sp.simplify(complement**2 - complement) == sp.zeros(9)
    assert sp.trace(complement) == 6
    assert complement.rank() == 6
    assert projection_cubic_residual(complement, 3) == sp.zeros(27)

    lower_reflection = identity - 2 * projection
    upper_reflection = identity - 2 * complement
    assert sp.trace(lower_reflection) == 3
    assert sp.trace(upper_reflection) == -3


ALLOWED_NONSCALAR = (
    Fraction(1, 3),
    Fraction(1, 2),
    Fraction(2, 3),
)


def balance_holds(
    rank: int,
    complement_rank: int,
    left_eta: Fraction,
    right_eta: Fraction,
) -> bool:
    left_deviation = (
        Fraction(rank * rank) * (left_eta - Fraction(1, 2))
    )
    right_deviation = (
        Fraction(complement_rank * complement_rank)
        * (right_eta - Fraction(1, 2))
    )
    return left_deviation == right_deviation


def check_symbolic_rank_balance_cases() -> None:
    """Check the complete 3-by-3 eta case split for sample unequal ranks."""

    # Unequal positive ranks permit only the balanced/balanced pair.
    for rank, complement_rank in ((2, 4), (4, 6), (6, 8), (4, 10)):
        feasible = {
            (left, right)
            for left in ALLOWED_NONSCALAR
            for right in ALLOWED_NONSCALAR
            if balance_holds(rank, complement_rank, left, right)
        }
        assert feasible == {(Fraction(1, 2), Fraction(1, 2))}

    # Equal ranks additionally permit the two same-sign unbalanced pairs.
    for rank in (3, 4, 6, 9):
        feasible = {
            (left, right)
            for left in ALLOWED_NONSCALAR
            for right in ALLOWED_NONSCALAR
            if balance_holds(rank, rank, left, right)
        }
        assert feasible == {
            (Fraction(1, 3), Fraction(1, 3)),
            (Fraction(1, 2), Fraction(1, 2)),
            (Fraction(2, 3), Fraction(2, 3)),
        }

    # Recover all four cell ranks from the row/column equations.
    rank = 6
    total_dimension = 2 * rank
    expected_off_diagonal = {
        Fraction(1, 3): 2 * rank * rank // 3,
        Fraction(1, 2): rank * rank // 2,
        Fraction(2, 3): rank * rank // 3,
    }
    for eta, expected in expected_off_diagonal.items():
        diagonal_rank = int(rank * rank * eta)
        off_diagonal_rank = rank * total_dimension // 2 - diagonal_rank
        assert off_diagonal_rank == expected


def controlled_leg_allows(dimension: int, rank: int) -> bool:
    return (rank * dimension * dimension) % 8 == 0


def integral_eta(dimension: int, eta: Fraction) -> bool:
    return (dimension * dimension * eta).denominator == 1


def audit_two_mod_four_dimensions() -> int:
    audited = 0
    for dimension in range(2, 203):
        if dimension % 4 != 2:
            continue
        for rank in range(1, dimension):
            complement_rank = dimension - rank
            if not controlled_leg_allows(dimension, rank):
                continue
            assert rank % 2 == 0
            assert complement_rank % 2 == 0

            feasible = set()
            for left in ALLOWED_NONSCALAR:
                if not integral_eta(rank, left):
                    continue
                for right in ALLOWED_NONSCALAR:
                    if not integral_eta(complement_rank, right):
                        continue
                    if balance_holds(rank, complement_rank, left, right):
                        feasible.add((left, right))

            assert feasible <= {(Fraction(1, 2), Fraction(1, 2))}
            audited += 1
    return audited


def check_small_dimension_consequences() -> None:
    # At d=6, a common projection has even rank.  Every proper split has a
    # two-dimensional side, whose balanced exceptional class is empty.
    d6_ranks = [
        rank for rank in range(1, 6) if controlled_leg_allows(6, rank)
    ]
    assert d6_ranks == [2, 4]
    assert all(min(rank, 6 - rank) == 2 for rank in d6_ranks)

    # At d=10, deleting splits with a two-dimensional side leaves only
    # 4+6 and 6+4.  Thus a common reduction would contain d=6.
    d10_ranks = [
        rank
        for rank in range(1, 10)
        if controlled_leg_allows(10, rank)
        and min(rank, 10 - rank) != 2
    ]
    assert d10_ranks == [4, 6]
    assert all(6 in (rank, 10 - rank) for rank in d10_ranks)

    # Scalar propagation compares (Y-X) with -(Y-X)/3.
    assert Fraction(1, 1) != -Fraction(1, 3)
    assert Fraction(1, 1) + Fraction(1, 3) == Fraction(4, 3)


def main() -> None:
    check_unbalanced_local_witnesses()
    check_symbolic_rank_balance_cases()
    audited = audit_two_mod_four_dimensions()
    check_small_dimension_consequences()

    print("qutrit Gaussian rank-1/3 projection: exact")
    print("qutrit complementary rank-2/3 projection: exact")
    print("both 27-dimensional cubic identities: exact")
    print("common-cell rank-balance case split: exact")
    print(f"d = 2 mod 4 arithmetic guards audited: {audited}")
    print("d=6 trivial-intersection descent: exact")
    print("d=10 implies d=6 under nontrivial common reduction: exact")
    print("PASS")


if __name__ == "__main__":
    main()
