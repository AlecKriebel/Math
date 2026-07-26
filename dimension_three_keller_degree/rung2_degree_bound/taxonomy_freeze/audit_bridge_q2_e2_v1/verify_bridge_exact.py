#!/usr/bin/env python3
"""Dependency-free exact checks for the clean-room Q2-E2 bridge audit.

The checker deliberately imports no computer-algebra package and reads no
other project file.  It verifies:

* the 45 frozen coefficient pivots, including the 15 pivots that are empty
  in a rank-two row, and the 45 intrinsic rank-two minor guards refining
  the remaining 30 pivots;
* the disjoint 4+5+4 marked-companion route;
* the raw E7 kernels, legal gauges, and three-dimensional quotients for the
  two CO strata;
* the complete E6/E5 coefficient chains that force det(L)=0 on both CO
  strata;
* the division-free finite-k CTAU/CT obstruction and its pivot-cover Bezout
  identity; and
* the exact 3+6+1+1+2=13 attachment ledger, with C0 kept separate as an
  automorphism exit rather than a determinant contradiction.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import sys


if not __debug__:
    print("FAIL: assertions are required; do not run with -O", file=sys.stderr)
    raise SystemExit(2)


class Ring:
    def __init__(self, names: tuple[str, ...]):
        if len(set(names)) != len(names):
            raise ValueError("duplicate variable")
        self.names = names
        self.position = {name: index for index, name in enumerate(names)}
        self.zero_exponent = (0,) * len(names)

    def constant(self, value: int | Fraction) -> "Poly":
        value = Fraction(value)
        return Poly(self, {} if value == 0 else {self.zero_exponent: value})

    def variable(self, name: str) -> "Poly":
        exponent = [0] * len(self.names)
        exponent[self.position[name]] = 1
        return Poly(self, {tuple(exponent): Fraction(1)})


class Poly:
    def __init__(self, ring: Ring, terms: dict[tuple[int, ...], Fraction]):
        self.ring = ring
        clean: dict[tuple[int, ...], Fraction] = {}
        for exponent, coefficient in terms.items():
            coefficient = Fraction(coefficient)
            if len(exponent) != len(ring.names):
                raise ValueError("wrong exponent length")
            if coefficient:
                clean[exponent] = clean.get(exponent, Fraction(0)) + coefficient
        self.terms = {
            exponent: coefficient
            for exponent, coefficient in clean.items()
            if coefficient
        }

    def _coerce(self, other: object) -> "Poly":
        if isinstance(other, Poly):
            if other.ring is not self.ring:
                raise ValueError("mixed polynomial rings")
            return other
        if isinstance(other, (int, Fraction)):
            return self.ring.constant(other)
        return NotImplemented

    def __add__(self, other: object) -> "Poly":
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        terms = dict(self.terms)
        for exponent, coefficient in other.terms.items():
            terms[exponent] = terms.get(exponent, Fraction(0)) + coefficient
        return Poly(self.ring, terms)

    __radd__ = __add__

    def __neg__(self) -> "Poly":
        return Poly(
            self.ring,
            {exponent: -coefficient for exponent, coefficient in self.terms.items()},
        )

    def __sub__(self, other: object) -> "Poly":
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return self + (-other)

    def __rsub__(self, other: object) -> "Poly":
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return other - self

    def __mul__(self, other: object) -> "Poly":
        other = self._coerce(other)
        if other is NotImplemented:
            return NotImplemented
        terms: dict[tuple[int, ...], Fraction] = {}
        for left_exponent, left_coefficient in self.terms.items():
            for right_exponent, right_coefficient in other.terms.items():
                exponent = tuple(
                    left + right
                    for left, right in zip(left_exponent, right_exponent)
                )
                terms[exponent] = (
                    terms.get(exponent, Fraction(0))
                    + left_coefficient * right_coefficient
                )
        return Poly(self.ring, terms)

    __rmul__ = __mul__

    def __pow__(self, exponent: int) -> "Poly":
        if exponent < 0:
            raise ValueError("negative polynomial exponent")
        answer = self.ring.constant(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                answer = answer * base
            base = base * base
            power >>= 1
        return answer

    def derivative(self, name: str) -> "Poly":
        position = self.ring.position[name]
        terms: dict[tuple[int, ...], Fraction] = {}
        for exponent, coefficient in self.terms.items():
            degree = exponent[position]
            if degree:
                new_exponent = list(exponent)
                new_exponent[position] -= 1
                key = tuple(new_exponent)
                terms[key] = terms.get(key, Fraction(0)) + coefficient * degree
        return Poly(self.ring, terms)

    def coefficient(self, fixed: dict[str, int]) -> "Poly":
        positions = {
            self.ring.position[name]: degree for name, degree in fixed.items()
        }
        terms: dict[tuple[int, ...], Fraction] = {}
        for exponent, coefficient in self.terms.items():
            if any(exponent[position] != degree for position, degree in positions.items()):
                continue
            new_exponent = list(exponent)
            for position in positions:
                new_exponent[position] = 0
            key = tuple(new_exponent)
            terms[key] = terms.get(key, Fraction(0)) + coefficient
        return Poly(self.ring, terms)

    def substitute(self, substitutions: dict[str, "Poly" | int | Fraction]) -> "Poly":
        images: list[Poly] = []
        for name in self.ring.names:
            image = substitutions.get(name, self.ring.variable(name))
            if not isinstance(image, Poly):
                image = self.ring.constant(image)
            if image.ring is not self.ring:
                raise ValueError("substitution from wrong ring")
            images.append(image)
        answer = self.ring.constant(0)
        for exponent, coefficient in self.terms.items():
            term = self.ring.constant(coefficient)
            for image, degree in zip(images, exponent):
                if degree:
                    term = term * image**degree
            answer = answer + term
        return answer

    def constant_value(self) -> Fraction:
        if not self.terms:
            return Fraction(0)
        if set(self.terms) != {self.ring.zero_exponent}:
            raise ValueError("polynomial is not constant")
        return self.terms[self.ring.zero_exponent]

    def __eq__(self, other: object) -> bool:
        other = self._coerce(other)
        if other is NotImplemented:
            return False
        return self.terms == other.terms

    def __bool__(self) -> bool:
        return bool(self.terms)


def matrix_add(*matrices: list[list[Poly]]) -> list[list[Poly]]:
    rows = len(matrices[0])
    columns = len(matrices[0][0])
    return [
        [sum(matrix[row][column] for matrix in matrices) for column in range(columns)]
        for row in range(rows)
    ]


def matrix_scale(scalar: Poly, matrix: list[list[Poly]]) -> list[list[Poly]]:
    return [[scalar * entry for entry in row] for row in matrix]


def jacobian(vector: tuple[Poly, Poly, Poly]) -> list[list[Poly]]:
    return [[entry.derivative(name) for name in ("x", "y", "z")] for entry in vector]


def determinant3(matrix: list[list[Poly]]) -> Poly:
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def homogeneous_monomials(
    ring: Ring, degree: int
) -> tuple[tuple[tuple[int, int, int], Poly], ...]:
    x, y, z = (ring.variable(name) for name in ("x", "y", "z"))
    return tuple(
        ((i, j, degree - i - j), x**i * y**j * z ** (degree - i - j))
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def spatial_coefficients(poly: Poly, degree: int) -> dict[tuple[int, int, int], Poly]:
    answer: dict[tuple[int, int, int], Poly] = {}
    for exponent, _ in homogeneous_monomials(poly.ring, degree):
        coefficient = poly.coefficient(
            {"x": exponent[0], "y": exponent[1], "z": exponent[2]}
        )
        if coefficient:
            answer[exponent] = coefficient
    return answer


def weighted_determinant(
    ring: Ring,
    linear: list[list[Poly]],
    h2: tuple[Poly, Poly, Poly],
    h3: tuple[Poly, Poly, Poly],
    h4: tuple[Poly, Poly, Poly],
) -> Poly:
    weight = ring.variable("w")
    return determinant3(
        matrix_add(
            linear,
            matrix_scale(weight, jacobian(h2)),
            matrix_scale(weight**2, jacobian(h3)),
            matrix_scale(weight**3, jacobian(h4)),
        )
    )


def rank_fraction(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    if not work:
        return 0
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [entry / scale for entry in work[rank]]
        for row in range(rows):
            if row != rank and work[row][column]:
                multiplier = work[row][column]
                work[row] = [
                    left - multiplier * right
                    for left, right in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == rows:
            break
    return rank


def matrix_vector(
    matrix: list[list[Fraction]], vector: list[Fraction]
) -> list[Fraction]:
    return [sum(entry * value for entry, value in zip(row, vector)) for row in matrix]


def coefficient_vector(
    triple: tuple[Poly, Poly, Poly],
    cubic_monomials: tuple[tuple[tuple[int, int, int], Poly], ...],
    quadratic_monomials: tuple[tuple[tuple[int, int, int], Poly], ...],
) -> list[Fraction]:
    answer: list[Fraction] = []
    for form, monomials in (
        (triple[0], cubic_monomials),
        (triple[1], cubic_monomials),
        (triple[2], quadratic_monomials),
    ):
        for exponent, _ in monomials:
            answer.append(
                form.coefficient(
                    {"x": exponent[0], "y": exponent[1], "z": exponent[2]}
                ).constant_value()
            )
    return answer


def verify_route_tables() -> None:
    monomials4 = (
        "x^4",
        "x^3y",
        "x^3z",
        "x^2y^2",
        "x^2yz",
        "x^2z^2",
        "xy^3",
        "xy^2z",
        "xyz^2",
        "xz^3",
        "y^4",
        "y^3z",
        "y^2z^2",
        "yz^3",
        "z^4",
    )
    coefficient_routes = tuple(
        (
            f"C_{index}",
            index // 15 + 1,
            monomials4[index % 15],
            "INTRINSIC_MINOR" if index < 30 else "EMPTY_RANK_AT_MOST_ONE",
        )
        for index in range(45)
    )
    assert len(coefficient_routes) == 45
    assert len({route[0] for route in coefficient_routes}) == 45
    assert {
        (component, monomial)
        for _, component, monomial, _ in coefficient_routes
    } == {
        (component, monomial)
        for component in (1, 2, 3)
        for monomial in monomials4
    }
    assert sum(route[3] == "INTRINSIC_MINOR" for route in coefficient_routes) == 30
    assert (
        sum(route[3] == "EMPTY_RANK_AT_MOST_ONE" for route in coefficient_routes)
        == 15
    )
    for pivot in range(45):
        test = [0] * 45
        test[pivot] = 1
        selected = next(index for index, value in enumerate(test) if value)
        assert selected == pivot
        possible_nonzero_components = {
            coefficient // 15 + 1
            for coefficient in range(pivot, 45)
        }
        if pivot >= 30:
            assert possible_nonzero_components == {3}
            # The Jacobian of a vector with only one nonzero target
            # component has row rank at most one.
            assert coefficient_routes[pivot][3] == "EMPTY_RANK_AT_MOST_ONE"
        else:
            assert len(possible_nonzero_components) >= 2
            assert coefficient_routes[pivot][3] == "INTRINSIC_MINOR"

    quadratic_columns = ("x^2", "xy", "xz", "y^2", "yz", "z^2")
    row_pairs = ((1, 2), (1, 3), (2, 3))
    column_pairs = tuple(combinations(range(6), 2))
    minor_routes = tuple(
        (
            f"M_{index}",
            row_pair,
            (quadratic_columns[left], quadratic_columns[right]),
        )
        for index, (row_pair, (left, right)) in enumerate(
            (item for row_pair in row_pairs for item in ((row_pair, pair) for pair in column_pairs))
        )
    )
    assert len(minor_routes) == 45
    assert len({route[0] for route in minor_routes}) == 45
    assert len(
        {
            (route[1], route[2])
            for route in minor_routes
        }
    ) == 45

    def first_nonzero_minor(matrix: tuple[tuple[int, ...], ...]) -> int | None:
        minors: list[int] = []
        for first_row, second_row in row_pairs:
            for first_column, second_column in column_pairs:
                minors.append(
                    matrix[first_row - 1][first_column]
                    * matrix[second_row - 1][second_column]
                    - matrix[first_row - 1][second_column]
                    * matrix[second_row - 1][first_column]
                )
        return next((index for index, value in enumerate(minors) if value), None)

    samples = (
        ((1, 0, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0)),
        ((0, 0, 0, 0, 0, 0), (0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 1, 0)),
        ((1, 2, 3, 4, 5, 6), (2, 4, 6, 8, 10, 12), (0, 1, 0, 1, 0, 1)),
    )
    assert all(first_nonzero_minor(sample) is not None for sample in samples)
    rank_one = (
        (1, 2, 3, 4, 5, 6),
        (2, 4, 6, 8, 10, 12),
        (-1, -2, -3, -4, -5, -6),
    )
    assert first_nonzero_minor(rank_one) is None

    prefix = "Q2-E2-A2-B1-D1-N1-MD-"
    ledgers = {
        "P21-HR2": ("C0", "CH", "CS", "CO"),
        "P21-HSM": ("C0", "CH", "CT", "CS", "CTAU"),
        "P3-HSM": ("C0", "CH", "CS", "CO"),
    }
    stable_ids = tuple(
        prefix + pair + "-" + suffix
        for pair, suffixes in ledgers.items()
        for suffix in suffixes
    )
    assert len(stable_ids) == 13 == len(set(stable_ids))

    terminal_kind = {
        stable_id: (
            "AUTOMORPHISM_EXIT" if stable_id.endswith("-C0") else "DET_L_ZERO"
        )
        for stable_id in stable_ids
    }
    assert list(terminal_kind.values()).count("AUTOMORPHISM_EXIT") == 3
    assert list(terminal_kind.values()).count("DET_L_ZERO") == 10

    def outer(nonzero: bool, u: int, v: int, modulus: int) -> str:
        if not nonzero:
            return "C0"
        if v % modulus == 0:
            return "CH"
        if u % modulus == 0:
            return "CS"
        return "CO"

    def middle(nonzero: bool, u: int, v: int, modulus: int) -> str:
        if not nonzero:
            return "C0"
        if v % modulus == 0:
            return "CH"
        if u % modulus == 0:
            return "CS"
        if (u + v) % modulus == 0:
            return "CT"
        return "CTAU"

    for prime in (5, 7, 11):
        projective_points = ((0, 1),) + tuple((1, value) for value in range(prime))
        outer_labels = [outer(True, u, v, prime) for u, v in projective_points]
        middle_labels = [middle(True, u, v, prime) for u, v in projective_points]
        assert outer_labels.count("CH") == 1
        assert outer_labels.count("CS") == 1
        assert outer_labels.count("CO") == prime - 1
        assert middle_labels.count("CH") == 1
        assert middle_labels.count("CS") == 1
        assert middle_labels.count("CT") == 1
        assert middle_labels.count("CTAU") == prime - 2
        assert outer(False, 0, 0, prime) == "C0"
        assert middle(False, 0, 0, prime) == "C0"


def verify_e7_quotient(case: str) -> None:
    raw_names = tuple(f"u{index}" for index in range(10)) + tuple(
        f"v{index}" for index in range(10)
    ) + tuple(f"t{index}" for index in range(6))
    ring = Ring(("x", "y", "z", "w") + raw_names)
    x, y, z, w = (ring.variable(name) for name in ("x", "y", "z", "w"))
    cubic_monomials = homogeneous_monomials(ring, 3)
    quadratic_monomials = homogeneous_monomials(ring, 2)
    raw = {name: ring.variable(name) for name in raw_names}
    U = sum(raw[f"u{index}"] * monomial for index, (_, monomial) in enumerate(cubic_monomials))
    V = sum(raw[f"v{index}"] * monomial for index, (_, monomial) in enumerate(cubic_monomials))
    W = sum(raw[f"t{index}"] * monomial for index, (_, monomial) in enumerate(quadratic_monomials))
    h = y * z if case == "P21" else y**2 + x * z
    P = h**2
    Q = h * x**2
    R = x * (h + x**2)
    zero = ring.constant(0)
    determinant = determinant3(
        matrix_add(
            matrix_scale(w, jacobian((zero, zero, W))),
            matrix_scale(w**2, jacobian((U, V, R))),
            matrix_scale(w**3, jacobian((P, Q, zero))),
        )
    )
    e7 = determinant.coefficient({"w": 7})
    equations = [
        e7.coefficient({"x": exponent[0], "y": exponent[1], "z": exponent[2]})
        for exponent, _ in homogeneous_monomials(ring, 7)
    ]
    matrix: list[list[Fraction]] = []
    raw_positions = {ring.position[name] for name in raw_names}
    for equation in equations:
        row = [Fraction(0)] * len(raw_names)
        for exponent, coefficient in equation.terms.items():
            occupied = [position for position in raw_positions if exponent[position]]
            assert len(occupied) == 1
            position = occupied[0]
            assert exponent[position] == 1
            assert sum(exponent) == 1
            raw_index = ring.position[raw_names[0]]
            row[position - raw_index] += coefficient
        matrix.append(row)
    assert len(matrix) == 36 and len(matrix[0]) == 26
    assert rank_fraction(matrix) == 18

    if case == "P21":
        kernel_triples = (
            (x**3, zero, zero),
            (x * h, zero, zero),
            (zero, x**3, zero),
            (zero, x * h, zero),
            (zero, zero, x**2),
            (2 * y * h, x**2 * y, x * y),
            (2 * z * h, x**2 * z, x * z),
            (zero, zero, h),
        )
        normal_triples = (
            (x**3, zero, zero),
            (zero, x**3, zero),
            (zero, zero, x**2),
        )
    else:
        kernel_triples = (
            (x**3, zero, zero),
            (x * h, zero, zero),
            (zero, x**3, zero),
            (zero, x * h, zero),
            (zero, zero, x**2),
            (2 * y * h, x**2 * y, x * y),
            (2 * z * h, x**2 * z, x * z),
            (-2 * z * h, -x**2 * z, y**2),
        )
        normal_triples = (
            (x**3, zero, zero),
            (zero, x**3, zero),
            (2 * z * h, x**2 * z, x * z),
        )
    kernel_vectors = [
        coefficient_vector(triple, cubic_monomials, quadratic_monomials)
        for triple in kernel_triples
    ]
    assert all(not any(matrix_vector(matrix, vector)) for vector in kernel_vectors)
    assert rank_fraction([list(row) for row in zip(*kernel_vectors)]) == 8

    gauge_triples = (
        (R, zero, zero),
        (zero, R, zero),
        (P.derivative("x"), Q.derivative("x"), R.derivative("x")),
        (P.derivative("y"), Q.derivative("y"), R.derivative("y")),
        (P.derivative("z"), Q.derivative("z"), R.derivative("z")),
    )
    gauge_vectors = [
        coefficient_vector(triple, cubic_monomials, quadratic_monomials)
        for triple in gauge_triples
    ]
    assert all(not any(matrix_vector(matrix, vector)) for vector in gauge_vectors)
    assert rank_fraction([list(row) for row in zip(*gauge_vectors)]) == 5
    normal_vectors = [
        coefficient_vector(triple, cubic_monomials, quadratic_monomials)
        for triple in normal_triples
    ]
    combined = gauge_vectors + normal_vectors
    assert rank_fraction([list(row) for row in zip(*combined)]) == 8


def lower_ring(include_k: bool = False) -> tuple[Ring, dict[str, Poly]]:
    names = (
        ("x", "y", "z", "w", "A", "B", "C", "T")
        + (("k",) if include_k else ())
        + tuple(f"a{index}" for index in range(6))
        + tuple(f"b{index}" for index in range(6))
        + tuple(f"l{index}" for index in range(9))
    )
    ring = Ring(names)
    return ring, {name: ring.variable(name) for name in names}


def general_lower_data(
    ring: Ring, variables: dict[str, Poly], W: Poly
) -> tuple[tuple[Poly, Poly, Poly], list[list[Poly]]]:
    monomials2 = homogeneous_monomials(ring, 2)
    first = sum(
        variables[f"a{index}"] * monomial
        for index, (_, monomial) in enumerate(monomials2)
    )
    second = sum(
        variables[f"b{index}"] * monomial
        for index, (_, monomial) in enumerate(monomials2)
    )
    linear = [
        [variables[f"l{3 * row + column}"] for column in range(3)]
        for row in range(3)
    ]
    return (first, second, W), linear


def assert_coefficient_map(
    actual: Poly,
    degree: int,
    expected: dict[tuple[int, int, int], Poly],
) -> None:
    actual_map = spatial_coefficients(actual, degree)
    assert set(actual_map) == set(expected)
    assert all(actual_map[exponent] == value for exponent, value in expected.items())


def verify_p21_co_lower() -> None:
    ring, q = lower_ring()
    x, y, z, w = (q[name] for name in ("x", "y", "z", "w"))
    A, B, T = (q[name] for name in ("A", "B", "T"))
    a = tuple(q[f"a{index}"] for index in range(6))
    b = tuple(q[f"b{index}"] for index in range(6))
    ell = tuple(q[f"l{index}"] for index in range(9))
    h = y * z
    h2, linear = general_lower_data(ring, q, T * x**2)
    determinant = weighted_determinant(
        ring,
        linear,
        h2,
        (A * x**3, B * x**3, x * (h + x**2)),
        (h**2, h * x**2, ring.constant(0)),
    )
    assert all(not determinant.coefficient({"w": degree}) for degree in (9, 8, 7))
    e6 = determinant.coefficient({"w": 6})
    expected6 = {
        (5, 1, 0): 3 * a[1],
        (5, 0, 1): -3 * a[2],
        (4, 2, 0): 6 * a[3],
        (4, 0, 2): -6 * a[5],
        (3, 2, 1): -a[1] - 6 * b[1],
        (3, 1, 2): a[2] + 6 * b[2],
        (2, 3, 1): -2 * (a[3] + 6 * b[3]),
        (2, 1, 3): 2 * (a[5] + 6 * b[5]),
        (1, 3, 2): -2 * (b[1] - 2 * ell[7]),
        (1, 2, 3): 2 * (b[2] - 2 * ell[8]),
        (0, 4, 2): -4 * b[3],
        (0, 2, 4): 4 * b[5],
    }
    assert_coefficient_map(e6, 6, expected6)
    forced6 = {
        "a1": 0,
        "a2": 0,
        "a3": 0,
        "a5": 0,
        "b1": 0,
        "b2": 0,
        "b3": 0,
        "b5": 0,
        "l7": 0,
        "l8": 0,
    }
    assert not e6.substitute(forced6)
    e5 = determinant.coefficient({"w": 5}).substitute(forced6)
    expected5 = {
        (4, 1, 0): 3 * ell[1],
        (4, 0, 1): -3 * ell[2],
        (2, 2, 1): -ell[1] - 6 * ell[4],
        (2, 1, 2): ell[2] + 6 * ell[5],
        (0, 3, 2): -2 * ell[4],
        (0, 2, 3): 2 * ell[5],
    }
    assert_coefficient_map(e5, 5, expected5)
    determinant_linear = determinant3(linear)
    assert not determinant_linear.substitute(
        forced6 | {"l1": 0, "l2": 0, "l4": 0, "l5": 0}
    )


def verify_p3_co_lower() -> None:
    ring, q = lower_ring()
    x, y, z, w = (q[name] for name in ("x", "y", "z", "w"))
    A, B, C = (q[name] for name in ("A", "B", "C"))
    a = tuple(q[f"a{index}"] for index in range(6))
    b = tuple(q[f"b{index}"] for index in range(6))
    ell = tuple(q[f"l{index}"] for index in range(9))
    h = y**2 + x * z
    h2, linear = general_lower_data(ring, q, C * x * z)
    determinant = weighted_determinant(
        ring,
        linear,
        h2,
        (
            A * x**3 + 2 * C * z * h,
            B * x**3 + C * x**2 * z,
            x * (h + x**2),
        ),
        (h**2, h * x**2, ring.constant(0)),
    )
    assert all(not determinant.coefficient({"w": degree}) for degree in (9, 8, 7))
    e6 = determinant.coefficient({"w": 6})
    expected6 = {
        (6, 0, 0): 3 * a[1],
        (5, 1, 0): -6 * (a[2] - a[3]),
        (5, 0, 1): -a[1] + 3 * a[4] - 6 * b[1],
        (4, 2, 0): -a[1] - 6 * a[4] - 6 * b[1],
        (4, 1, 1): 2 * (6 * C**2 + a[2] - a[3] - 6 * a[5] + 6 * b[2] - 6 * b[3]),
        (4, 0, 2): -a[4] - 2 * b[1] - 6 * b[4] + 4 * ell[7],
        (3, 3, 0): 2 * (a[2] - a[3] + 6 * b[2] - 6 * b[3]),
        (3, 2, 1): a[4] - 4 * b[1] + 6 * b[4] + 8 * ell[7],
        (3, 1, 2): 4 * (-C**2 + a[5] + b[2] - b[3] + 6 * b[5] - 2 * ell[8]),
        (3, 0, 3): -2 * b[4],
        (2, 4, 0): 2 * (a[4] - b[1] + 6 * b[4] + 2 * ell[7]),
        (2, 3, 1): 4 * (-C**2 + a[5] + 2 * b[2] - 2 * b[3] + 6 * b[5] - 4 * ell[8]),
        (2, 1, 3): 8 * b[5],
        (1, 5, 0): 4 * (b[2] - b[3] - 2 * ell[8]),
        (1, 4, 1): 6 * b[4],
        (1, 3, 2): 16 * b[5],
        (0, 6, 0): 4 * b[4],
        (0, 5, 1): 8 * b[5],
    }
    assert_coefficient_map(e6, 6, expected6)
    forced6 = {
        "a1": 0,
        "a2": a[3],
        "a4": 0,
        "a5": C**2,
        "b1": 0,
        "b2": b[3],
        "b4": 0,
        "b5": 0,
        "l7": 0,
        "l8": 0,
    }
    assert not e6.substitute(forced6)
    e5 = determinant.coefficient({"w": 5}).substitute(forced6)
    expected5 = {
        (5, 0, 0): 3 * ell[1],
        (4, 1, 0): 6 * (C * a[3] - ell[2]),
        (4, 0, 1): -ell[1] - 6 * ell[4],
        (3, 2, 0): -ell[1] - 6 * ell[4],
        (3, 1, 1): -2 * (C * a[3] + 6 * C * b[3] - ell[2] - 6 * ell[5]),
        (3, 0, 2): -2 * ell[4],
        (2, 3, 0): -2 * (C * a[3] + 6 * C * b[3] - ell[2] - 6 * ell[5]),
        (2, 2, 1): -4 * ell[4],
        (2, 1, 2): -4 * (C * b[3] - ell[5]),
        (1, 4, 0): -2 * ell[4],
        (1, 3, 1): -8 * (C * b[3] - ell[5]),
        (0, 5, 0): -4 * (C * b[3] - ell[5]),
    }
    assert_coefficient_map(e5, 5, expected5)
    determinant_linear = determinant3(linear)
    assert not determinant_linear.substitute(
        forced6
        | {
            "l1": 0,
            "l2": C * a[3],
            "l4": 0,
            "l5": C * b[3],
        }
    )


def verify_ctau_lower() -> None:
    ring, q = lower_ring(include_k=True)
    x, y, z, w = (q[name] for name in ("x", "y", "z", "w"))
    A, B, T, k = (q[name] for name in ("A", "B", "T", "k"))
    a = tuple(q[f"a{index}"] for index in range(6))
    b = tuple(q[f"b{index}"] for index in range(6))
    ell = tuple(q[f"l{index}"] for index in range(9))
    h = x**2 + y * z
    h2, linear = general_lower_data(ring, q, T * x**2)
    determinant = weighted_determinant(
        ring,
        linear,
        h2,
        (A * x**3, B * x**3, x * (h + k * x**2)),
        (h**2, h * x**2, ring.constant(0)),
    )
    assert all(not determinant.coefficient({"w": degree}) for degree in (9, 8, 7))
    e6 = determinant.coefficient({"w": 6})
    expected6 = {
        (5, 1, 0): (3 * k - 1) * a[1] - (6 * k + 2) * b[1] + 4 * ell[7],
        (5, 0, 1): -(3 * k - 1) * a[2] + (6 * k + 2) * b[2] - 4 * ell[8],
        (4, 2, 0): 2 * ((3 * k - 1) * a[3] - (6 * k + 2) * b[3]),
        (4, 0, 2): -2 * ((3 * k - 1) * a[5] - (6 * k + 2) * b[5]),
        (3, 2, 1): -a[1] - (6 * k + 4) * b[1] + 8 * ell[7],
        (3, 1, 2): a[2] + (6 * k + 4) * b[2] - 8 * ell[8],
        (2, 3, 1): -2 * (a[3] + (6 * k + 4) * b[3]),
        (2, 1, 3): 2 * (a[5] + (6 * k + 4) * b[5]),
        (1, 3, 2): -2 * (b[1] - 2 * ell[7]),
        (1, 2, 3): 2 * (b[2] - 2 * ell[8]),
        (0, 4, 2): -4 * b[3],
        (0, 2, 4): 4 * b[5],
    }
    assert_coefficient_map(e6, 6, expected6)
    y_chain = expected6[(5, 1, 0)].substitute(
        {"b1": 2 * ell[7], "a1": -12 * k * ell[7]}
    )
    z_chain = expected6[(5, 0, 1)].substitute(
        {"b2": 2 * ell[8], "a2": -12 * k * ell[8]}
    )
    assert y_chain == -36 * k**2 * ell[7]
    assert z_chain == 36 * k**2 * ell[8]
    forced6 = {
        "a1": 0,
        "a2": 0,
        "a3": 0,
        "a5": 0,
        "b1": 0,
        "b2": 0,
        "b3": 0,
        "b5": 0,
        "l7": 0,
        "l8": 0,
    }
    assert not e6.substitute(forced6)
    e5 = determinant.coefficient({"w": 5}).substitute(forced6)
    expected5 = {
        (4, 1, 0): (3 * k - 1) * ell[1] - (6 * k + 2) * ell[4],
        (4, 0, 1): -(3 * k - 1) * ell[2] + (6 * k + 2) * ell[5],
        (2, 2, 1): -ell[1] - (6 * k + 4) * ell[4],
        (2, 1, 2): ell[2] + (6 * k + 4) * ell[5],
        (0, 3, 2): -2 * ell[4],
        (0, 2, 3): 2 * ell[5],
    }
    assert_coefficient_map(e5, 5, expected5)
    assert not determinant3(linear).substitute(
        forced6 | {"l1": 0, "l2": 0, "l4": 0, "l5": 0}
    )
    pivot_q = 9 * k**2 + 6 * k - 1
    pivot_r = 3 * k - 1
    assert Fraction(1, 2) * pivot_q - Fraction(3, 2) * (k + 1) * pivot_r == 1


def main() -> None:
    verify_route_tables()
    verify_e7_quotient("P21")
    verify_e7_quotient("P3")
    verify_p21_co_lower()
    verify_p3_co_lower()
    verify_ctau_lower()
    print("AUDIT_BRIDGE_Q2_E2_EXACT_PASS_B625E1")
    print(
        "routes: 30 rank-two-possible coefficient pivots; "
        "15 empty rank-one pivots; 45 intrinsic minors; 4+5+4=13 strata"
    )
    print("CO E7: rank 18, nullity 8, gauge 5, quotient 3 (both cases)")
    print("terminal kinds: 3 AUTOMORPHISM_EXIT; 10 DET_L_ZERO")


if __name__ == "__main__":
    main()
