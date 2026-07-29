#!/usr/bin/env python3
"""Exact constrained-Hessian audit at a nonnormal Q3=0 boundary point.

This is discovery/verification code, not a proof of global n=3 positivity.
It uses only dyadic rational arithmetic after constructing the tangent
coordinates.  The base partial isometry is

    |000><110| + |001><111|
      = |0><1| tensor |0><1| tensor (|0><0|+|1><1|).

The chart consists of independent horizontal Stiefel variations of its
left and right two-frames, together with four relative logical rotations.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product
import os


String = tuple[int, int, int]
Unit = tuple[String, String]
SparseMatrix = dict[Unit, complex]
FrameVariation = dict[tuple[String, int], complex]

D = int(os.environ.get("N3_LOCAL_DIMENSION", "3"))
assert D >= 2
N = 3
STRINGS = list(product(range(D), repeat=N))
U0 = [(0, 0, 0), (0, 0, 1)]
V0 = [(1, 1, 0), (1, 1, 1)]


def unit_pairing(first: Unit, second: Unit) -> Fraction:
    """Return B3(E_ab,E_cd) exactly."""

    a, b = first
    c, e = second
    answer = Fraction(0)
    for size in range(N + 1):
        for traced in combinations(range(N), size):
            if not all(a[i] == b[i] and c[i] == e[i] for i in traced):
                continue
            kept = tuple(i for i in range(N) if i not in traced)
            if all(a[i] == c[i] and b[i] == e[i] for i in kept):
                answer += Fraction(-1, 2) ** size
    return answer


PAIRING_CACHE: dict[tuple[Unit, Unit], Fraction] = {}


def pairing(first: SparseMatrix, second: SparseMatrix) -> complex:
    answer = 0j
    for e, x in first.items():
        for f, y in second.items():
            key = (e, f)
            if key not in PAIRING_CACHE:
                PAIRING_CACHE[key] = unit_pairing(e, f)
            answer += x.conjugate() * y * PAIRING_CACHE[key]
    return answer


def add_term(matrix: defaultdict[Unit, complex], unit: Unit, value: complex):
    matrix[unit] += value
    if matrix[unit] == 0:
        del matrix[unit]


BASE: defaultdict[Unit, complex] = defaultdict(complex)
BASE[(U0[0], V0[0])] = 1
BASE[(U0[1], V0[1])] = 1


def coordinate_list():
    coordinates: list[tuple[FrameVariation, FrameVariation]] = []
    labels: list[tuple] = []
    for side, frame in (("U", U0), ("V", V0)):
        for row in STRINGS:
            if row in frame:
                continue
            for column in range(2):
                for phase, phase_name in ((1, "real"), (1j, "imag")):
                    left: defaultdict[tuple[String, int], complex] = defaultdict(
                        complex
                    )
                    right: defaultdict[tuple[String, int], complex] = defaultdict(
                        complex
                    )
                    (left if side == "U" else right)[row, column] = phase
                    coordinates.append((left, right))
                    labels.append((side, row, column, phase_name))

    # A basis of u(2), placed on the left frame.  A simultaneous logical
    # rotation of both frames is gauge, so these are the four relative
    # logical directions.
    logical = (
        ((1j, 0), (0, 0)),
        ((0, 0), (0, 1j)),
        ((0, 1), (-1, 0)),
        ((0, 1j), (1j, 0)),
    )
    for number, generator in enumerate(logical):
        left = defaultdict(complex)
        for row in range(2):
            for column in range(2):
                if generator[row][column]:
                    left[U0[row], column] += generator[row][column]
        coordinates.append((left, defaultdict(complex)))
        labels.append(("logical", number))
    return coordinates, labels


COORDINATES, LABELS = coordinate_list()


def quadratic_coefficient(indices: tuple[int, ...]) -> Fraction:
    """Coefficient of t^2 in Q3 for the polar-retracted tangent sum."""

    left: defaultdict[tuple[String, int], complex] = defaultdict(complex)
    right: defaultdict[tuple[String, int], complex] = defaultdict(complex)
    for index in indices:
        for key, value in COORDINATES[index][0].items():
            left[key] += value
        for key, value in COORDINATES[index][1].items():
            right[key] += value

    left_gram = [[0j] * 2 for _ in range(2)]
    right_gram = [[0j] * 2 for _ in range(2)]
    for (row, a), x in left.items():
        for (other_row, b), y in left.items():
            if row == other_row:
                left_gram[a][b] += x.conjugate() * y
    for (row, a), x in right.items():
        for (other_row, b), y in right.items():
            if row == other_row:
                right_gram[a][b] += x.conjugate() * y

    first: defaultdict[Unit, complex] = defaultdict(complex)
    second: defaultdict[Unit, complex] = defaultdict(complex)
    for (row, logical), value in left.items():
        add_term(first, (row, V0[logical]), value)
    for (row, logical), value in right.items():
        add_term(first, (U0[logical], row), value.conjugate())

    # The polar Stiefel retraction is
    # (U0+tX)(I+t^2 X^*X)^(-1/2).  These are precisely its second-order
    # normalization terms, followed by the mixed X Y^* term.
    for a in range(2):
        for b in range(2):
            add_term(
                second,
                (U0[a], V0[b]),
                -0.5 * (left_gram[a][b] + right_gram[a][b]),
            )
    for (row, a), x in left.items():
        for (column, b), y in right.items():
            if a == b:
                add_term(second, (row, column), x * y.conjugate())

    value = (pairing(first, first) + 2 * pairing(BASE, second)).real
    # Every entry is dyadic; conversion through an exactly represented
    # binary float is safe here and independently checked below.
    rational = Fraction(value).limit_denominator(8)
    assert float(rational) == value
    return rational


def hessian():
    size = len(COORDINATES)
    diagonal = [quadratic_coefficient((i,)) for i in range(size)]
    matrix = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for i, value in enumerate(diagonal):
        matrix[i][i] = value
    for i in range(size):
        for j in range(i):
            value = (
                quadratic_coefficient((i, j)) - diagonal[i] - diagonal[j]
            ) / 2
            matrix[i][j] = matrix[j][i] = value
    return matrix


def connected_components(matrix):
    size = len(matrix)
    adjacency = [[] for _ in range(size)]
    for i in range(size):
        for j in range(i):
            if matrix[i][j]:
                adjacency[i].append(j)
                adjacency[j].append(i)
    seen: set[int] = set()
    output: list[list[int]] = []
    for start in range(size):
        if start in seen:
            continue
        seen.add(start)
        stack = [start]
        component = []
        while stack:
            current = stack.pop()
            component.append(current)
            for other in adjacency[current]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        output.append(component)
    return output


def kernel_basis(matrix, components):
    """Return a sparse exact basis of the Hessian kernel."""

    output: list[dict[int, Fraction]] = []
    for component in components:
        pivot = max(component, key=lambda i: matrix[i][i])
        pivot_value = matrix[pivot][pivot]
        for index in component:
            if index == pivot:
                continue
            output.append(
                {
                    index: Fraction(1),
                    pivot: -matrix[pivot][index] / pivot_value,
                }
            )
    return output


def multiply_right(frame, logical):
    output = defaultdict(complex)
    for (row, a), value in frame.items():
        for b in range(2):
            add_term(output, (row, b), value * logical[a][b])
    return output


def logical_product(first, second):
    return [
        [
            sum(first[i][k] * second[k][j] for k in range(2))
            for j in range(2)
        ]
        for i in range(2)
    ]


def frame_gram(frame):
    output = [[0j] * 2 for _ in range(2)]
    for (row, a), x in frame.items():
        for (other_row, b), y in frame.items():
            if row == other_row:
                output[a][b] += x.conjugate() * y
    return output


def frame_series(base_strings, tangent, order: int = 4):
    base = defaultdict(complex)
    base[(base_strings[0], 0)] = 1
    base[(base_strings[1], 1)] = 1
    gram = frame_gram(tangent)
    powers = [[[1, 0], [0, 1]]]
    for _ in range(1, order // 2 + 1):
        powers.append(logical_product(powers[-1], gram))

    # Coefficients of (I+t^2 G)^(-1/2):
    # c_k=(-1)^k binom(2k,k)/4^k.
    coefficients = [Fraction(1)]
    for k in range(1, order // 2 + 1):
        coefficients.append(
            -coefficients[-1] * Fraction(2 * k - 1, 2 * k)
        )

    output = []
    for degree in range(order + 1):
        power = degree // 2
        source = base if degree % 2 == 0 else tangent
        output.append(
            {
                key: coefficients[power] * value
                for key, value in multiply_right(
                    source, powers[power]
                ).items()
            }
        )
    return tuple(output)


def frame_outer(left, right):
    output = defaultdict(complex)
    for (row, a), x in left.items():
        for (column, b), y in right.items():
            if a == b:
                add_term(output, (row, column), x * y.conjugate())
    return output


def q_series(coordinates: dict[int, Fraction], order: int = 4):
    """Return the exact Q3 Taylor coefficients through ``order``."""

    left = defaultdict(complex)
    right = defaultdict(complex)
    for index, coefficient in coordinates.items():
        for key, value in COORDINATES[index][0].items():
            left[key] += coefficient * value
        for key, value in COORDINATES[index][1].items():
            right[key] += coefficient * value

    left_series = frame_series(U0, left, order)
    right_series = frame_series(V0, right, order)
    coefficient_matrices = []
    for degree in range(order + 1):
        matrix = defaultdict(complex)
        for left_degree in range(degree + 1):
            right_degree = degree - left_degree
            if left_degree >= len(left_series) or right_degree >= len(
                right_series
            ):
                continue
            for key, value in frame_outer(
                left_series[left_degree], right_series[right_degree]
            ).items():
                add_term(matrix, key, value)
        coefficient_matrices.append(matrix)

    output = []
    for degree in range(order + 1):
        value = sum(
            pairing(coefficient_matrices[j], coefficient_matrices[degree - j])
            for j in range(degree + 1)
        ).real
        rational = Fraction(value).limit_denominator(1 << 30)
        assert float(rational) == value
        output.append(rational)
    return tuple(output)


def rank_one_certificate(block) -> Fraction:
    """Verify a symmetric rational block is PSD of rank one."""

    pivot = max(block[i][i] for i in range(len(block)))
    assert pivot > 0
    pivot_index = next(i for i in range(len(block)) if block[i][i] == pivot)
    for i in range(len(block)):
        for j in range(len(block)):
            assert (
                pivot * block[i][j]
                == block[i][pivot_index] * block[pivot_index][j]
            )
    return pivot


def add_directions(*directions):
    output: defaultdict[int, Fraction] = defaultdict(Fraction)
    for direction in directions:
        for index, coefficient in direction.items():
            output[index] += coefficient
    return {index: coefficient for index, coefficient in output.items() if coefficient}


def verify_cubic_vanishing(flat_directions) -> None:
    """Verify by polarization that the cubic vanishes on the flat space."""

    zero_cubic = lambda direction: q_series(direction, 3)[3] == 0
    assert all(zero_cubic(direction) for direction in flat_directions)

    # The values on e_i +/- e_j determine all x_i^2 x_j and x_i x_j^2
    # coefficients of a homogeneous cubic.
    for i, j in combinations(range(len(flat_directions)), 2):
        first = flat_directions[i]
        second = flat_directions[j]
        assert zero_cubic(add_directions(first, second))
        assert zero_cubic(
            add_directions(first, {key: -value for key, value in second.items()})
        )

    # With all one- and two-index coefficients zero, evaluation at
    # e_i+e_j+e_k is six times the remaining square-free coefficient.
    for i, j, k in combinations(range(len(flat_directions)), 3):
        assert zero_cubic(
            add_directions(
                flat_directions[i], flat_directions[j], flat_directions[k]
            )
        )


def main() -> None:
    assert pairing(BASE, BASE) == 0
    matrix = hessian()
    components = connected_components(matrix)
    profile: defaultdict[tuple[int, Fraction], int] = defaultdict(int)
    for component in components:
        block = [[matrix[i][j] for j in component] for i in component]
        pivot = rank_one_certificate(block)
        profile[len(component), pivot] += 1

    expected = {
        (4, Fraction(1, 4)): 4,
        (4, Fraction(1, 8)): 2,
        (2, Fraction(1, 1)): 4 * (D - 2),
        (2, Fraction(1, 2)): 4 * (D - 1) ** 2 + 5,
        (2, Fraction(1, 4)): 8 * D - 12,
        (1, Fraction(1, 1)): 8 * D * (D - 1) * (D - 2),
        (1, Fraction(1, 2)): 16 * D * (D - 2),
        (1, Fraction(1, 4)): 8 * (D - 2),
        (1, Fraction(2, 1)): 2,
    }
    expected = {key: value for key, value in expected.items() if value}
    assert dict(profile) == expected
    expected_dimension = 8 * D**3 - 12
    expected_nullity = 4 * D**2 + 4 * D + 7
    expected_rank = expected_dimension - expected_nullity
    assert len(matrix) == expected_dimension
    assert len(components) == expected_rank
    assert (
        sum(len(component) - 1 for component in components)
        == expected_nullity
    )

    flat_directions = kernel_basis(matrix, components)
    nullity = sum(len(component) - 1 for component in components)
    assert len(flat_directions) == nullity
    individual_series = [q_series(direction) for direction in flat_directions]
    assert all(series[:4] == (0, 0, 0, 0) for series in individual_series)
    quartic_profile: defaultdict[Fraction, int] = defaultdict(int)
    for series in individual_series:
        quartic_profile[series[4]] += 1
    assert dict(quartic_profile) == {
        Fraction(0): expected_nullity - 6,
        Fraction(1): 6,
    }
    if D == 3:
        verify_cubic_vanishing(flat_directions)

    print("verified exact n=3 constrained Hessian at the canonical zero")
    print(
        "local dimension",
        D,
        "; tangent dimension",
        len(matrix),
        "; rank",
        len(components),
        "; nullity",
        nullity,
    )
    print("all", len(components), "connected blocks are positive rank one")
    for key in sorted(profile):
        print(key, profile[key])
    print("kernel-basis quartic profile", dict(quartic_profile))
    if D == 3:
        print(
            "all cubic Taylor coefficients vanish on the "
            "55-dimensional kernel"
        )


if __name__ == "__main__":
    main()
