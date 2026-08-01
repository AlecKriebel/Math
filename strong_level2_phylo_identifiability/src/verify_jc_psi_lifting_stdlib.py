"""Independent pure-stdlib replay of the lifted JC Psi certificate.

This script imports neither SymPy nor python-flint.  It checks the complete
256-coordinate rational-function identity with a small sparse-polynomial
implementation, replays the exact rational common point, and verifies the two
nonzero rank-ten determinants by exact multilinear finite differences.
"""

from __future__ import annotations

from fractions import Fraction
from functools import reduce
from itertools import permutations, product

from enumerate_four_leaf_root_theta import enumerate_networks
from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices


SOURCE_FREE_COLUMNS = (0, 1, 2, 3, 4, 6, 7, 8, 9, 10)
TARGET_FREE_COLUMNS = (0, 1, 2, 3, 4, 5, 7, 8, 9, 10)
RANK_ROWS = (0, 1, 2, 3, 4, 5, 6, 7, 14, 15)
VARIABLE_COUNT = 13
TOPOLOGIES = {
    "A": (18, (1, 2, 3, 4)),
    "A_reflected": (18, (3, 2, 1, 4)),
    "B": (19, (2, 1, 3, 4)),
    "B_reflected": (19, (2, 3, 1, 4)),
}


def poly_clean(polynomial):
    return {monomial: coefficient for monomial, coefficient in polynomial.items() if coefficient}


def poly_add(left, right):
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, Fraction(0)) + coefficient
    return poly_clean(answer)


def poly_neg(polynomial):
    return {monomial: -coefficient for monomial, coefficient in polynomial.items()}


def poly_scale(polynomial, scalar):
    scalar = Fraction(scalar)
    return poly_clean({monomial: scalar * coefficient for monomial, coefficient in polynomial.items()})


def poly_multiply(left, right):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(
                left_exponent + right_exponent
                for left_exponent, right_exponent in zip(left_monomial, right_monomial)
            )
            answer[monomial] = answer.get(monomial, Fraction(0)) + left_coefficient * right_coefficient
    return poly_clean(answer)


def poly_power(polynomial, exponent):
    answer = poly_constant(1)
    factor = polynomial
    while exponent:
        if exponent & 1:
            answer = poly_multiply(answer, factor)
        factor = poly_multiply(factor, factor)
        exponent //= 2
    return answer


def poly_constant(value):
    value = Fraction(value)
    return {} if not value else {(0,) * VARIABLE_COUNT: value}


def poly_variable(index):
    monomial = [0] * VARIABLE_COUNT
    monomial[index] = 1
    return {tuple(monomial): Fraction(1)}


VARIABLES = tuple(poly_variable(index) for index in range(VARIABLE_COUNT))
DENOMINATOR = poly_add(poly_multiply(VARIABLES[0], VARIABLES[1]), VARIABLES[2])
A1 = VARIABLES[1]


class RationalFunction:
    """Sparse numerator divided by D**d_power * a1**a1_power."""

    __slots__ = ("numerator", "d_power", "a1_power")

    def __init__(self, numerator, d_power=0, a1_power=0):
        self.numerator = poly_clean(numerator)
        self.d_power = d_power
        self.a1_power = a1_power

    @classmethod
    def coerce(cls, value):
        if isinstance(value, cls):
            return value
        return cls(poly_constant(value))

    def lifted_numerator(self, d_power, a1_power):
        answer = self.numerator
        if d_power > self.d_power:
            answer = poly_multiply(answer, poly_power(DENOMINATOR, d_power - self.d_power))
        if a1_power > self.a1_power:
            answer = poly_multiply(answer, poly_power(A1, a1_power - self.a1_power))
        return answer

    def __add__(self, other):
        other = self.coerce(other)
        d_power = max(self.d_power, other.d_power)
        a1_power = max(self.a1_power, other.a1_power)
        return RationalFunction(
            poly_add(
                self.lifted_numerator(d_power, a1_power),
                other.lifted_numerator(d_power, a1_power),
            ),
            d_power,
            a1_power,
        )

    __radd__ = __add__

    def __neg__(self):
        return RationalFunction(poly_neg(self.numerator), self.d_power, self.a1_power)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        return RationalFunction(
            poly_multiply(self.numerator, other.numerator),
            self.d_power + other.d_power,
            self.a1_power + other.a1_power,
        )

    __rmul__ = __mul__

    def __eq__(self, other):
        other = self.coerce(other)
        d_power = max(self.d_power, other.d_power)
        a1_power = max(self.a1_power, other.a1_power)
        return self.lifted_numerator(d_power, a1_power) == other.lifted_numerator(
            d_power, a1_power
        )


def rf_variable(index):
    return RationalFunction(VARIABLES[index])


def canonical_character_orbit(assignment):
    images = []
    for permutation in permutations((1, 2, 3)):
        mapping = {0: 0, 1: permutation[0], 2: permutation[1], 3: permutation[2]}
        images.append(tuple(mapping[value] for value in assignment))
    return min(images)


FIVE_LEAF_REPRESENTATIVES = tuple(
    sorted(
        {
            canonical_character_orbit(assignment)
            for assignment in product(range(4), repeat=5)
            if reduce(int.__xor__, assignment, 0) == 0
        }
    )
)

FIVE_LEAF_ZERO_SUM = tuple(
    (first, second, third, fourth, first ^ second ^ third ^ fourth)
    for first, second, third, fourth in product(range(4), repeat=4)
)


def augmented_network(name):
    _raw, networks = enumerate_networks()
    network_index, labels = TOPOLOGIES[name]
    base = networks[network_index]
    vertices = dict(base["vertices"])
    vertices["S"] = "T"
    vertices["RHO"] = "S"
    vertices["LIN"] = "L"
    edges = tuple(tuple(edge) for edge in base["edges"]) + (
        ("RHO", "S"),
        ("RHO", "LIN"),
    )
    leaf_labels = dict(zip(base["leaves"], labels))
    leaf_labels["LIN"] = 5
    return vertices, edges, leaf_labels


def evaluate(name, assignments, values):
    vertices, edges, leaf_labels = augmented_network(name)
    reticulations = reticulation_vertices(vertices)
    return evaluate_jc_coordinates(
        vertices,
        edges,
        leaf_labels,
        assignments,
        values[: len(edges)],
        dict(zip(reticulations, values[len(edges) :])),
    )


def symbolic_parameters():
    variables = tuple(rf_variable(index) for index in range(VARIABLE_COUNT))
    a0, a1, a2, a3, a4, a6, a7, a8, a9, a10, a11, a12, a13 = variables
    half = RationalFunction.coerce(Fraction(1, 2))
    source = (
        a0,
        a1,
        a2,
        a3,
        a4,
        half,
        a6,
        a7,
        a8,
        a9,
        a10,
        a11,
        a12,
        a13,
        half,
        half,
    )
    b0 = RationalFunction(poly_scale(poly_multiply(poly_multiply(VARIABLES[0], VARIABLES[1]), VARIABLES[3]), 4), 1, 0)
    b2 = RationalFunction(poly_scale(poly_multiply(poly_multiply(VARIABLES[1], VARIABLES[2]), VARIABLES[3]), 4), 1, 0)
    b3 = RationalFunction(poly_scale(DENOMINATOR, Fraction(1, 4)), 0, 1)
    target = (
        b0,
        a1,
        b2,
        b3,
        a6,
        a7,
        half,
        a4,
        a9,
        a10,
        a8,
        a11,
        a12,
        a13,
        half,
        half,
    )
    return source, target


def rational_points():
    source = [Fraction(1, 2)] * 16
    for index, value in zip(
        SOURCE_FREE_COLUMNS,
        (
            Fraction(9, 10),
            Fraction(1, 2),
            Fraction(1, 2),
            Fraction(1, 2),
            Fraction(2, 5),
            Fraction(1, 10),
            Fraction(1, 3),
            Fraction(3, 5),
            Fraction(2, 3),
            Fraction(3, 4),
        ),
    ):
        source[index] = value
    target = [Fraction(1, 2)] * 16
    for index, value in {
        0: Fraction(18, 19),
        1: Fraction(1, 2),
        2: Fraction(10, 19),
        3: Fraction(19, 40),
        4: Fraction(1, 10),
        5: Fraction(1, 3),
        7: Fraction(2, 5),
        8: Fraction(2, 3),
        9: Fraction(3, 4),
        10: Fraction(3, 5),
    }.items():
        target[index] = value
    return tuple(source), tuple(target)


def determinant(matrix):
    matrix = [list(row) for row in matrix]
    answer = Fraction(1)
    for column in range(len(matrix)):
        pivot = next(row for row in range(column, len(matrix)) if matrix[row][column])
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            answer = -answer
        pivot_value = matrix[column][column]
        answer *= pivot_value
        for row in range(column + 1, len(matrix)):
            if not matrix[row][column]:
                continue
            multiplier = matrix[row][column] / pivot_value
            for index in range(column, len(matrix)):
                matrix[row][index] -= multiplier * matrix[column][index]
    return answer


def rank_minor(name, values, columns):
    assignments = tuple(FIVE_LEAF_REPRESENTATIVES[row + 1] for row in RANK_ROWS)
    derivative_columns = []
    for parameter_index in columns:
        at_zero = list(values)
        at_one = list(values)
        at_zero[parameter_index] = Fraction(0)
        at_one[parameter_index] = Fraction(1)
        zero_coordinates = evaluate(name, assignments, at_zero)
        one_coordinates = evaluate(name, assignments, at_one)
        derivative_columns.append(
            tuple(one - zero for one, zero in zip(one_coordinates, zero_coordinates))
        )
    return determinant(tuple(zip(*derivative_columns)))


def main():
    source_symbolic, target_symbolic = symbolic_parameters()
    symbolic_checks = {}
    for source_name, target_name in (
        ("A", "B_reflected"),
        ("A_reflected", "B"),
    ):
        source_coordinates = evaluate(source_name, FIVE_LEAF_ZERO_SUM, source_symbolic)
        target_coordinates = evaluate(target_name, FIVE_LEAF_ZERO_SUM, target_symbolic)
        assert source_coordinates == target_coordinates
        symbolic_checks[f"{source_name}--{target_name}"] = len(source_coordinates)

    source_point, target_point = rational_points()
    assert all(0 < value < 1 for value in source_point)
    assert all(0 < value < 1 for value in target_point)
    source_values = evaluate("A", FIVE_LEAF_ZERO_SUM, source_point)
    target_values = evaluate("B_reflected", FIVE_LEAF_ZERO_SUM, target_point)
    assert source_values == target_values

    source_minor = rank_minor("A", source_point, SOURCE_FREE_COLUMNS)
    target_minor = rank_minor("B_reflected", target_point, TARGET_FREE_COLUMNS)
    assert source_minor == -Fraction(263169, 13743895347200000000000)
    assert target_minor == Fraction(5000211, 274877906944000000000000)
    print("pure_stdlib_symbolic_coordinates", symbolic_checks)
    print("pure_stdlib_rational_common_coordinates", len(source_values))
    print("pure_stdlib_rank_ten_minors", source_minor, target_minor)
    print("PASS: independent standard-library exact replay")


if __name__ == "__main__":
    main()
