#!/usr/bin/env python3
"""Exact verifier for the Perron/robust-depth hybrid barriers.

Only the Python standard library is used.  Every comparison is performed
in Q or in a real quadratic extension of Q.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "certificate.json"


def frac(value: str | int | Fraction) -> Fraction:
    if isinstance(value, Fraction):
        return value
    return Fraction(value)


class Quadratic:
    """Element a+b*sqrt(d), for one fixed positive rational d."""

    __slots__ = ("a", "b", "d")

    def __init__(
        self,
        a: int | Fraction = 0,
        b: int | Fraction = 0,
        d: int | Fraction = 1,
    ) -> None:
        self.a = frac(a)
        self.b = frac(b)
        self.d = frac(d)
        if self.d <= 0:
            raise ValueError("the radicand must be positive")

    def _coerce(self, other: object) -> "Quadratic":
        if isinstance(other, Quadratic):
            if other.d != self.d:
                raise ValueError("incompatible quadratic fields")
            return other
        if isinstance(other, (int, Fraction)):
            return Quadratic(other, 0, self.d)
        return NotImplemented  # type: ignore[return-value]

    def __add__(self, other: object) -> "Quadratic":
        rhs = self._coerce(other)
        if rhs is NotImplemented:
            return NotImplemented  # type: ignore[return-value]
        return Quadratic(self.a + rhs.a, self.b + rhs.b, self.d)

    def __radd__(self, other: object) -> "Quadratic":
        return self + other

    def __neg__(self) -> "Quadratic":
        return Quadratic(-self.a, -self.b, self.d)

    def __sub__(self, other: object) -> "Quadratic":
        rhs = self._coerce(other)
        if rhs is NotImplemented:
            return NotImplemented  # type: ignore[return-value]
        return self + (-rhs)

    def __rsub__(self, other: object) -> "Quadratic":
        return (-self) + other

    def __mul__(self, other: object) -> "Quadratic":
        rhs = self._coerce(other)
        if rhs is NotImplemented:
            return NotImplemented  # type: ignore[return-value]
        return Quadratic(
            self.a * rhs.a + self.b * rhs.b * self.d,
            self.a * rhs.b + self.b * rhs.a,
            self.d,
        )

    def __rmul__(self, other: object) -> "Quadratic":
        return self * other

    def inverse(self) -> "Quadratic":
        denominator = self.a * self.a - self.b * self.b * self.d
        if denominator == 0:
            raise ZeroDivisionError
        return Quadratic(
            self.a / denominator, -self.b / denominator, self.d
        )

    def __truediv__(self, other: object) -> "Quadratic":
        rhs = self._coerce(other)
        if rhs is NotImplemented:
            return NotImplemented  # type: ignore[return-value]
        return self * rhs.inverse()

    def __rtruediv__(self, other: object) -> "Quadratic":
        return self._coerce(other) * self.inverse()

    def __pow__(self, exponent: int) -> "Quadratic":
        if exponent < 0:
            return (self.inverse()) ** (-exponent)
        answer = Quadratic(1, 0, self.d)
        base = self
        power = exponent
        while power:
            if power & 1:
                answer = answer * base
            base = base * base
            power >>= 1
        return answer

    def __eq__(self, other: object) -> bool:
        rhs = self._coerce(other)
        if rhs is NotImplemented:
            return False
        return self.a == rhs.a and self.b == rhs.b

    def __hash__(self) -> int:
        return hash((self.a, self.b, self.d))

    def sign(self) -> int:
        """Return the exact sign, using one rational square comparison."""
        if self.b == 0:
            return (self.a > 0) - (self.a < 0)
        if self.b < 0:
            return -(-self).sign()
        if self.a >= 0:
            return 1
        comparison = self.b * self.b * self.d - self.a * self.a
        return (comparison > 0) - (comparison < 0)

    def __repr__(self) -> str:
        return f"Quadratic({self.a!r}, {self.b!r}, {self.d!r})"

    def exact_string(self) -> str:
        if self.b == 0:
            return str(self.a)
        return f"{self.a}+({self.b})*sqrt({self.d})"


def qsum(values: Iterable[Quadratic], d: Fraction) -> Quadratic:
    total = Quadratic(0, 0, d)
    for value in values:
        total += value
    return total


def dot(left: Sequence, right: Sequence):
    if len(left) != len(right):
        raise ValueError("dimension mismatch")
    if not left:
        return Fraction(0)
    total = left[0] * right[0]
    for first, second in zip(left[1:], right[1:]):
        total += first * second
    return total


def matvec(matrix: Sequence[Sequence], vector: Sequence):
    return [dot(row, vector) for row in matrix]


def rank(matrix: Sequence[Sequence]) -> int:
    if not matrix:
        return 0
    work = [list(row) for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column] != 0),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            multiplier = work[row][column]
            if multiplier != 0:
                work[row] = [
                    entry - multiplier * base
                    for entry, base in zip(work[row], work[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def identity(size: int, one=Fraction(1), zero=Fraction(0)):
    return [
        [one if row == column else zero for column in range(size)]
        for row in range(size)
    ]


def outer(vector: Sequence):
    return [[first * second for second in vector] for first in vector]


def matrix_add(left: Sequence[Sequence], right: Sequence[Sequence]):
    return [
        [a + b for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def matrix_scale(scalar, matrix: Sequence[Sequence]):
    return [[scalar * entry for entry in row] for row in matrix]


def d5_lines_scaled() -> list[list[int]]:
    """Twenty line representatives, with actual vector z/sqrt(2)."""
    lines: list[list[int]] = []
    for first in range(5):
        for second in range(first + 1, 5):
            plus = [0] * 5
            plus[first] = 1
            plus[second] = 1
            minus = [0] * 5
            minus[first] = 1
            minus[second] = -1
            lines.extend((plus, minus))
    return lines


def d5_roots_scaled() -> list[list[int]]:
    roots: list[list[int]] = []
    for line in d5_lines_scaled():
        roots.append(line)
        roots.append([-entry for entry in line])
    return roots


def gram_from_scaled_rational(vectors: Sequence[Sequence[int]]):
    return [
        [Fraction(dot(first, second), 2) for second in vectors]
        for first in vectors
    ]


def verify_scalar_family(data: dict, delta: Fraction, floor: Fraction) -> dict:
    sample = data["scalar_family_sample"]
    r = frac(sample["parameter_r"])
    k = frac(sample["k"])
    Delta = k * r * r
    t = 41 - Delta
    rho = 42 - Delta
    m = Fraction(7, 5) * r
    c_squared = Fraction(41, 70) - Fraction(41, 25) * r * r
    c = Quadratic(0, 1, c_squared)

    assert Delta == frac(sample["D"])
    assert t == frac(sample["t"])
    assert rho == frac(sample["rho"])
    assert m == frac(sample["m"])
    assert c_squared == frac(sample["c_squared"])

    a_minus = Quadratic(m, -1, c_squared)
    a_middle = Quadratic(m, 0, c_squared)
    a_plus = Quadratic(m, 1, c_squared)
    axial = [a_minus] * 7 + [a_middle] * 27 + [a_plus] * 7
    one = Quadratic(1, 0, c_squared)
    weights = [(one - 2 * r * value) / t for value in axial]

    assert len(axial) == 41
    assert qsum(weights, c_squared) == 1
    assert all(weight.sign() > 0 for weight in weights)
    low_tail = sum((value + delta).sign() < 0 for value in axial)
    high_tail = sum((value - delta).sign() > 0 for value in axial)
    assert low_tail >= 7
    assert high_tail >= 7
    assert all((value + 1).sign() > 0 for value in axial)
    assert all((1 - value).sign() > 0 for value in axial)

    first = qsum(axial, c_squared)
    second = qsum((value * value for value in axial), c_squared)
    assert first == Delta / (2 * r)
    assert second == Delta / (4 * r * r) - t / 2
    assert second.b == 0

    weighted_first = qsum(
        (weight * value for weight, value in zip(weights, axial)), c_squared
    )
    weighted_second = qsum(
        (weight * weight for weight in weights), c_squared
    )
    assert weighted_first == r
    assert 1 == t * weighted_second + 2 * r * r

    upper_threshold = Quadratic((1 + 2 * delta * r) / t, 0, c_squared)
    lower_threshold = Quadratic((1 - 2 * delta * r) / t, 0, c_squared)
    high_weight_tail = sum(
        (weight - upper_threshold).sign() > 0 for weight in weights
    )
    low_weight_tail = sum(
        (weight - lower_threshold).sign() < 0 for weight in weights
    )
    assert high_weight_tail >= 7
    assert low_weight_tail >= 7

    mean = first / 41
    variance = qsum(
        ((value - mean) ** 2 for value in axial), c_squared
    )
    assert variance.b == 0
    assert variance.a > Fraction(7, 45000)
    assert (
        Delta - 82 * r * r
        == Fraction(164) * r * r * variance.a / t
    )
    assert (
        Delta
        > Fraction(835059) * r * r
        / (Fraction(10000) * (1 + 2 * r * r))
    )

    axis = Fraction(41, 5) + Delta / 2
    transverse = Fraction(41, 5) - Delta / 8
    assert axis == frac(sample["frame_axis_eigenvalue"])
    assert transverse == frac(sample["frame_transverse_eigenvalue"])
    assert axis + 4 * transverse == 41
    assert min(axis, transverse) > floor

    centered_second = (axis - Fraction(41, 5)) ** 2 + 4 * (
        transverse - Fraction(41, 5)
    ) ** 2
    centered_third = (axis - Fraction(41, 5)) ** 3 + 4 * (
        transverse - Fraction(41, 5)
    ) ** 3
    assert centered_second == frac(sample["claimed_centered_second_moment"])
    assert centered_third == frac(sample["claimed_centered_third_moment"])
    assert 20 * centered_third**2 == 9 * centered_second**3
    assert centered_second == frac(
        sample["claimed_frame_potential_excess_over_Welch"]
    )

    covariance_axis = second.a - first.a * first.a / 41
    assert covariance_axis == 14 * c_squared
    assert min(covariance_axis, transverse) > Fraction(7, 45000)

    # Coefficient-level checks for the entire one-parameter family.
    # Here z=r^2.  A polynomial is stored as (constant, coefficient of z).
    Delta_poly = (Fraction(0), k)
    energy_poly = (Fraction(41, 5), k / 2)
    transverse_poly = (Fraction(41, 5), -k / 8)
    assert (
        energy_poly[0] + 4 * transverse_poly[0],
        energy_poly[1] + 4 * transverse_poly[1],
    ) == (Fraction(41), Fraction(0))
    assert k == 2 * Fraction(287, 5)
    assert Fraction(41) + 2 * energy_poly[0] == Fraction(287, 5)
    assert -Delta_poly[1] + 2 * energy_poly[1] == 0

    return {
        "sample_size": len(axial),
        "rho": str(rho),
        "strict_low_tail": low_tail,
        "strict_high_tail": high_tail,
        "frame_potential": str(Fraction(1681, 5) + centered_second),
        "rank_five_cubic_equality": True,
    }


def verify_d5_depth(delta: Fraction) -> dict:
    lines = d5_lines_scaled()
    assert len(lines) == 20
    actual_outer_sum = [[Fraction(0) for _ in range(5)] for _ in range(5)]
    for line in lines:
        projector = [
            [Fraction(first * second, 2) for second in line] for first in line
        ]
        actual_outer_sum = matrix_add(actual_outer_sum, projector)
    assert actual_outer_sum == matrix_scale(Fraction(4), identity(5))

    maximum_pair_square = Fraction(0)
    for first_index, first in enumerate(lines):
        for second in lines[first_index + 1 :]:
            inner = Fraction(dot(first, second), 2)
            maximum_pair_square = max(maximum_pair_square, inner * inner)
    assert maximum_pair_square == Fraction(1, 4)

    trace_square_upper = Fraction(7) + 2 * Fraction(21) * maximum_pair_square
    spectral_lower_at_cutoff = Fraction(39, 10) ** 2 + (
        Fraction(7) - Fraction(39, 10)
    ) ** 2 / 4
    assert trace_square_upper == Fraction(35, 2)
    assert spectral_lower_at_cutoff == Fraction(1409, 80)
    assert spectral_lower_at_cutoff > trace_square_upper
    assert 13 * delta * delta < Fraction(1, 10)

    return {
        "line_count": 20,
        "guaranteed_each_side": 8,
        "spectral_cutoff": "39/10",
        "remaining_frame_floor": "1/10",
    }


def verify_d5_duplicate(data: dict, floor: Fraction) -> dict:
    roots = d5_roots_scaled()
    duplicate_index = int(data["d5_duplicate"]["duplicate_zero_based_root_index"])
    vectors = roots + [roots[duplicate_index]]
    gram = gram_from_scaled_rational(vectors)
    assert len(vectors) == 41
    assert all(gram[index][index] == 1 for index in range(41))
    assert rank(gram) == 5
    augmented = [row + [Fraction(1)] for row in gram]
    assert rank(augmented) == 6

    violating = [
        (first, second)
        for first in range(41)
        for second in range(first + 1, 41)
        if gram[first][second] > Fraction(1, 2)
    ]
    assert violating == [(duplicate_index, 40)]
    assert len(violating) == int(
        data["d5_duplicate"]["number_of_unordered_kissing_inequality_violations"]
    )

    frame = [[Fraction(0) for _ in range(5)] for _ in range(5)]
    centroid_scaled = [0] * 5
    for vector in vectors:
        centroid_scaled = [
            current + entry for current, entry in zip(centroid_scaled, vector)
        ]
        frame = matrix_add(
            frame,
            [[Fraction(first * second, 2) for second in vector] for first in vector],
        )
    y_scaled = vectors[-1]
    assert centroid_scaled == y_scaled
    expected_frame = matrix_add(
        matrix_scale(Fraction(8), identity(5)),
        [[Fraction(first * second, 2) for second in y_scaled] for first in y_scaled],
    )
    assert frame == expected_frame
    assert min(map(frac, data["d5_duplicate"]["frame_spectrum"])) > floor

    d = Fraction(3473)
    Delta = Quadratic(Fraction(59, 2), Fraction(-1, 2), d)
    t = 41 - Delta
    rho = 42 - Delta
    assert (Delta * Delta - 59 * Delta + 2) == 0
    assert Delta.sign() > 0
    assert (1 - Delta).sign() > 0
    assert (rho - 41).sign() > 0
    assert (42 - rho).sign() > 0

    y_inner_products = gram[-1]
    weights = [
        (Quadratic(1, 0, d) - Delta * inner) / t
        for inner in y_inner_products
    ]
    assert qsum(weights, d) == 1
    assert all(weight.sign() > 0 for weight in weights)

    A = [
        [2 * gram[row][column] - 1 for column in range(41)]
        for row in range(41)
    ]
    W = [
        [
            (1 if row == column else 0) - A[row][column]
            for column in range(41)
        ]
        for row in range(41)
    ]
    A_quadratic = [
        [Quadratic(entry, 0, d) for entry in row] for row in A
    ]
    W_quadratic = [
        [Quadratic(entry, 0, d) for entry in row] for row in W
    ]
    assert matvec(A_quadratic, weights) == [-t * value for value in weights]
    assert matvec(W_quadratic, weights) == [rho * value for value in weights]
    assert rank(A) == 6

    v_scaled = [
        qsum(
            (
                weight * vectors[index][coordinate]
                for index, weight in enumerate(weights)
            ),
            d,
        )
        for coordinate in range(5)
    ]
    expected_v_scaled = [Delta * entry / 2 for entry in y_scaled]
    assert v_scaled == expected_v_scaled
    v_norm_squared = dot(v_scaled, v_scaled) / 2
    assert v_norm_squared == (Delta / 2) ** 2
    assert 1 == t * qsum((value * value for value in weights), d) + 2 * v_norm_squared

    return {
        "rho": rho.exact_string(),
        "violating_pairs": len(violating),
        "gram_rank": rank(gram),
        "A_rank": rank(A),
        "positive_top_eigenvector": True,
    }


def verify_centered_endpoint(data: dict, floor: Fraction) -> dict:
    d = Fraction(3)
    lines = d5_lines_scaled()
    r_scaled = lines[0]
    z_scaled = lines[1]
    assert dot(r_scaled, z_scaled) == 0

    retained_integer = d5_roots_scaled()[2:]
    retained = [
        [Quadratic(entry, 0, d) for entry in vector]
        for vector in retained_integer
    ]
    r = [Quadratic(entry, 0, d) for entry in r_scaled]
    z = [Quadratic(entry, 0, d) for entry in z_scaled]
    y_plus = [
        -first / 2 + Quadratic(0, Fraction(1, 2), d) * second
        for first, second in zip(r, z)
    ]
    y_minus = [
        -first / 2 - Quadratic(0, Fraction(1, 2), d) * second
        for first, second in zip(r, z)
    ]
    vectors = retained + [r, y_plus, y_minus]
    assert len(vectors) == 41

    zero = Quadratic(0, 0, d)
    one = Quadratic(1, 0, d)
    for vector in vectors:
        assert dot(vector, vector) / 2 == one
    centroid = [qsum((vector[j] for vector in vectors), d) for j in range(5)]
    assert centroid == [zero] * 5
    assert rank(vectors) == 5

    gram = [[dot(first, second) / 2 for second in vectors] for first in vectors]
    assert rank(gram) == 5
    assert all(gram[index][index] == one for index in range(41))
    assert all(qsum(row, d) == zero for row in gram)

    frame = [[zero for _ in range(5)] for _ in range(5)]
    for vector in vectors:
        frame = matrix_add(frame, matrix_scale(Quadratic(Fraction(1, 2), 0, d), outer(vector)))

    rational_r_projector = [
        [Fraction(first * second, 2) for second in r_scaled] for first in r_scaled
    ]
    rational_z_projector = [
        [Fraction(first * second, 2) for second in z_scaled] for first in z_scaled
    ]
    expected_rational = matrix_add(
        matrix_add(
            matrix_scale(Fraction(8), identity(5)),
            matrix_scale(Fraction(-1, 2), rational_r_projector),
        ),
        matrix_scale(Fraction(3, 2), rational_z_projector),
    )
    expected = [
        [Quadratic(entry, 0, d) for entry in row] for row in expected_rational
    ]
    assert frame == expected
    assert matvec(frame, r) == [Fraction(15, 2) * entry for entry in r]
    assert matvec(frame, z) == [Fraction(19, 2) * entry for entry in z]
    for coordinate in range(2, 5):
        basis = [zero] * 5
        basis[coordinate] = one
        assert matvec(frame, basis) == [8 * entry for entry in basis]
    assert min(map(frac, data["d5_centered_triangle_replacement"]["frame_spectrum"])) > floor

    ones = [one] * 41
    A = [
        [2 * gram[row][column] - one for column in range(41)]
        for row in range(41)
    ]
    W = [
        [
            (one if row == column else zero) - A[row][column]
            for column in range(41)
        ]
        for row in range(41)
    ]
    assert matvec(A, ones) == [-41 * one] * 41
    assert matvec(W, ones) == [42 * one] * 41
    assert rank(A) == 6

    # After deleting +/-r, +z is the first retained normalized root.
    retained_z = retained[0]
    violating_inner = dot(y_plus, retained_z) / 2
    assert violating_inner == Quadratic(0, Fraction(1, 2), d)
    assert (violating_inner - Fraction(1, 2)).sign() > 0

    violating_count = sum(
        (gram[first][second] - Fraction(1, 2)).sign() > 0
        for first in range(41)
        for second in range(first + 1, 41)
    )
    assert violating_count > 0

    return {
        "rho": "42",
        "gram_rank": rank(gram),
        "A_rank": rank(A),
        "violating_pairs": violating_count,
        "explicit_violation": violating_inner.exact_string(),
        "global_depth_inherited_each_side": 7,
    }


def verify_all() -> dict:
    data = json.loads(CERTIFICATE.read_text())
    assert data["schema"] == "kissing5.perron_robust_depth_hybrid.v1"
    delta = frac(data["delta"])
    floor = frac(data["frame_floor"])
    assert delta == Fraction(1, 300)
    assert floor == Fraction(15059, 40000)

    report = {
        "scalar_family": verify_scalar_family(data, delta, floor),
        "d5_depth": verify_d5_depth(delta),
        "d5_duplicate": verify_d5_duplicate(data, floor),
        "centered_endpoint": verify_centered_endpoint(data, floor),
    }
    return report


def main() -> None:
    report = verify_all()
    print(json.dumps(report, indent=2, sort_keys=True))
    print("exact Perron/robust-depth hybrid verification: PASS")


if __name__ == "__main__":
    main()
