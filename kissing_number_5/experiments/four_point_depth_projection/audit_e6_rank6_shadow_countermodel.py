#!/usr/bin/env python3
"""Independent exact audit of the stronger E6 rank-six countermodel.

This checker does not import the source verifier.  In particular, the
38,760 frame inequalities are checked by exact rational LDL decomposition,
independently of the source verifier's Bareiss/Sylvester implementation.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "e6_rank6_shadow_countermodel.json"

CORE_INDICES = [
    0, 4, 5, 12, 13, 17, 20, 21, 25, 28,
    29, 32, 36, 40, 42, 43, 46, 49, 51, 55,
]
EXTRA_INDEX = 33
RANK_WITNESS_INDICES = [0, 4, 5, 12, 20, 40]
ARBITRARY_AXIS_CLIQUE = [4, 13, 43, 49, 33]
EXPECTED_FRAME_MINIMA = [
    12, 684, 28944, 1533168, 17029440, 71243712,
]


def roots() -> list[tuple[str, tuple[int, ...], int]]:
    result = []
    for first, second in combinations(range(5), 2):
        for first_sign, second_sign in product((-1, 1), repeat=2):
            vector = [0] * 5
            vector[first] = first_sign
            vector[second] = second_sign
            result.append(("D", tuple(vector), 0))
    for signs in product((-1, 1), repeat=5):
        parity = 1
        for sign in signs:
            parity *= sign
        result.append(("S", tuple(signs), parity))
    assert len(result) == 72
    return result


ROOTS = roots()


def antipode(
    root: tuple[str, tuple[int, ...], int],
) -> tuple[str, tuple[int, ...], int]:
    kind, vector, parity = root
    return kind, tuple(-entry for entry in vector), -parity


def dot_two(
    left: tuple[str, tuple[int, ...], int],
    right: tuple[str, tuple[int, ...], int],
) -> int:
    left_kind, left_vector, left_parity = left
    right_kind, right_vector, right_parity = right
    if left_kind == right_kind == "D":
        return sum(a * b for a, b in zip(left_vector, right_vector))
    if left_kind == "S" and right_kind == "D":
        return dot_two(right, left)
    if left_kind == "D":
        numerator = sum(
            a * b for a, b in zip(left_vector, right_vector)
        )
        assert numerator % 2 == 0
        return numerator // 2
    numerator = (
        sum(a * b for a, b in zip(left_vector, right_vector))
        + 3 * left_parity * right_parity
    )
    assert numerator % 4 == 0
    return numerator // 4


def selected_roots() -> list[tuple[str, tuple[int, ...], int]]:
    selected = []
    for index in CORE_INDICES:
        selected.extend((ROOTS[index], antipode(ROOTS[index])))
    selected.append(ROOTS[EXTRA_INDEX])
    assert len(selected) == len(set(selected)) == 41
    return selected


def determinant(matrix: list[list[int]]) -> int:
    """Fraction-free determinant, used only for the rank witness."""

    work = [row[:] for row in matrix]
    size = len(work)
    previous = 1
    sign = 1
    for column in range(size - 1):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        pivot_value = work[column][column]
        for row in range(column + 1, size):
            for other in range(column + 1, size):
                numerator = (
                    work[row][other] * pivot_value
                    - work[row][column] * work[column][other]
                )
                assert numerator % previous == 0
                work[row][other] = numerator // previous
        previous = pivot_value
    return sign * work[-1][-1]


def frame_congruence(subset: tuple[int, ...]) -> list[list[int]]:
    """Return the integral congruence of ``8(F_T-I/4)``."""

    top = [[0] * 5 for _ in range(5)]
    cross = [0] * 5
    bottom = 0
    for line_index in subset:
        kind, vector, parity = ROOTS[CORE_INDICES[line_index]]
        scale = 4 if kind == "D" else 1
        for row in range(5):
            for column in range(5):
                top[row][column] += (
                    scale * vector[row] * vector[column]
                )
        if kind == "S":
            for row in range(5):
                cross[row] += vector[row] * parity
            bottom += 3
    for coordinate in range(5):
        top[coordinate][coordinate] -= 2
    bottom -= 2

    result = [[0] * 6 for _ in range(6)]
    for row in range(5):
        for column in range(5):
            result[row][column] = 3 * top[row][column]
        result[row][5] = 3 * cross[row]
        result[5][row] = 3 * cross[row]
    result[5][5] = bottom
    return result


def ldl_leading_determinants(
    matrix: list[list[int]],
) -> list[Fraction]:
    """Exact unpivoted LDL; positivity is independently equivalent to PD."""

    size = len(matrix)
    lower = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    diagonal: list[Fraction] = []
    leading = []
    determinant_so_far = Fraction(1)
    for row in range(size):
        pivot = Fraction(matrix[row][row]) - sum(
            lower[row][column] ** 2 * diagonal[column]
            for column in range(row)
        )
        assert pivot > 0
        diagonal.append(pivot)
        lower[row][row] = 1
        determinant_so_far *= pivot
        leading.append(determinant_so_far)
        for later in range(row + 1, size):
            lower[later][row] = (
                Fraction(matrix[later][row])
                - sum(
                    lower[later][column]
                    * lower[row][column]
                    * diagonal[column]
                    for column in range(row)
                )
            ) / pivot
    return leading


def audit() -> dict[str, object]:
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert certificate["core_line_root_indices"] == CORE_INDICES
    assert certificate["extra_root_index"] == EXTRA_INDEX
    assert certificate["arbitrary_axis_five_clique_indices"] == (
        ARBITRARY_AXIS_CLIQUE
    )

    selected = selected_roots()
    pair_histogram = Counter(
        dot_two(left, right) for left, right in combinations(selected, 2)
    )
    assert pair_histogram == {-2: 20, -1: 219, 0: 362, 1: 219}

    contact_neighbors = [
        {
            other
            for other in range(41)
            if other != index
            and dot_two(selected[index], selected[other]) == 1
        }
        for index in range(41)
    ]
    common_histograms: dict[int, Counter[int]] = defaultdict(Counter)
    for left, right in combinations(range(41), 2):
        base = dot_two(selected[left], selected[right])
        common_histograms[base][
            len(contact_neighbors[left] & contact_neighbors[right])
        ] += 1
    common_maxima = {
        base: max(histogram)
        for base, histogram in common_histograms.items()
    }
    assert common_maxima == {-2: 0, -1: 1, 0: 5, 1: 7}

    witness = [ROOTS[index] for index in RANK_WITNESS_INDICES]
    witness_two_gram = [
        [dot_two(left, right) for right in witness] for left in witness
    ]
    assert determinant(witness_two_gram) == 3

    frame_minima: list[Fraction | None] = [None] * 6
    frame_cases = 0
    for subset in combinations(range(20), 14):
        leading = ldl_leading_determinants(frame_congruence(subset))
        for order, value in enumerate(leading):
            assert value.denominator == 1
            if frame_minima[order] is None or value < frame_minima[order]:
                frame_minima[order] = value
        frame_cases += 1
    assert frame_cases == 38760
    assert frame_minima == [Fraction(value) for value in EXPECTED_FRAME_MINIMA]
    assert Fraction(14, 300**2) < Fraction(1, 4)

    # The complete local contact-clique table supplies an additional audit
    # of the claimed positive-base and local-link shadows.
    clique_link_maxima = []
    clique_counts = []
    for size in range(1, 6):
        maximum = 0
        count = 0
        for clique in combinations(range(41), size):
            if size > 1 and not all(
                right in contact_neighbors[left]
                for left, right in combinations(clique, 2)
            ):
                continue
            common = set(range(41)) - set(clique)
            for vertex in clique:
                common &= contact_neighbors[vertex]
            maximum = max(maximum, len(common))
            count += 1
        clique_link_maxima.append(maximum)
        clique_counts.append(count)
    assert clique_link_maxima == [13, 7, 4, 1, 0]
    assert clique_counts == [41, 219, 318, 129, 5]

    negative_degrees = [
        sum(
            dot_two(selected[left], selected[right]) < 0
            for right in range(41)
            if right != left
        )
        for left in range(41)
    ]
    assert min(negative_degrees) == 10

    clique = [ROOTS[index] for index in ARBITRARY_AXIS_CLIQUE]
    assert all(root in selected for root in clique)
    assert all(
        dot_two(left, right) == 1
        for left, right in combinations(clique, 2)
    )
    arbitrary_axis_q = Fraction(-1, 6)
    arbitrary_height = Fraction(1, 2)
    arbitrary_parameter = (
        2 * arbitrary_height**2 / (1 + arbitrary_axis_q)
    )
    assert arbitrary_parameter == Fraction(3, 5)

    frame_potential = Fraction(41) + 2 * sum(
        multiplicity * Fraction(value, 2) ** 2
        for value, multiplicity in pair_histogram.items()
    )
    degree_two_sum = (5 * frame_potential - 41**2) / 4
    assert frame_potential == 300
    assert degree_two_sum == Fraction(-181, 4)

    return {
        "status": "PASS",
        "pair_histogram": dict(sorted(pair_histogram.items())),
        "common_contact_maxima": dict(sorted(common_maxima.items())),
        "rank_witness_det_two_gram": 3,
        "frame_cases_checked_by_fraction_ldl": frame_cases,
        "frame_leading_determinant_minima": [
            int(value) for value in frame_minima if value is not None
        ],
        "contact_clique_counts": clique_counts,
        "contact_clique_link_maxima": clique_link_maxima,
        "minimum_negative_degree": min(negative_degrees),
        "arbitrary_axis_failure": "5 > 4 at p=3/5",
        "degree_two_failure": str(degree_two_sum),
    }


if __name__ == "__main__":
    for key, value in audit().items():
        print(f"{key}: {value}")
