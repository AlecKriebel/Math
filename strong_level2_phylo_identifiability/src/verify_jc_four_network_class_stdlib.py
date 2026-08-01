"""Independent pure-stdlib replay of the four-network JC common point.

This verifier imports neither SymPy nor python-flint.  It implements arithmetic
in Q(beta), evaluates all displayed trees directly, and obtains Jacobian
columns by exact multilinear finite differences.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product

from enumerate_four_leaf_root_theta import enumerate_networks
from generic_fourier_network import evaluate_jc_coordinates, reticulation_vertices


A = 43337075
B = -36083110
C = 7336259
BETA_SQUARED_CONSTANT = Fraction(-C, A)
BETA_SQUARED_LINEAR = Fraction(-B, A)


@dataclass(frozen=True)
class Quadratic:
    constant: Fraction = Fraction(0)
    linear: Fraction = Fraction(0)

    @staticmethod
    def coerce(value):
        if isinstance(value, Quadratic):
            return value
        return Quadratic(Fraction(value), Fraction(0))

    def __add__(self, other):
        other = self.coerce(other)
        return Quadratic(self.constant + other.constant, self.linear + other.linear)

    __radd__ = __add__

    def __neg__(self):
        return Quadratic(-self.constant, -self.linear)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        beta_squared = self.linear * other.linear
        return Quadratic(
            self.constant * other.constant + beta_squared * BETA_SQUARED_CONSTANT,
            self.constant * other.linear
            + self.linear * other.constant
            + beta_squared * BETA_SQUARED_LINEAR,
        )

    __rmul__ = __mul__

    def inverse(self):
        if not self:
            raise ZeroDivisionError
        # The conjugate root is BETA_SQUARED_LINEAR-beta.
        conjugate = Quadratic(
            self.constant + self.linear * BETA_SQUARED_LINEAR,
            -self.linear,
        )
        norm = self * conjugate
        assert norm.linear == 0 and norm.constant != 0
        return Quadratic(conjugate.constant / norm.constant, conjugate.linear / norm.constant)

    def __truediv__(self, other):
        return self * self.coerce(other).inverse()

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def __bool__(self):
        return self.constant != 0 or self.linear != 0

    def compact(self):
        return (str(self.constant), str(self.linear))


ZERO = Quadratic()
ONE = Quadratic(Fraction(1))
BETA = Quadratic(Fraction(0), Fraction(1))


JC_REPRESENTATIVES = (
    (0, 0, 0, 0),
    (0, 0, 1, 1),
    (0, 1, 0, 1),
    (0, 1, 1, 0),
    (0, 1, 2, 3),
    (1, 0, 0, 1),
    (1, 0, 1, 0),
    (1, 0, 2, 3),
    (1, 1, 0, 0),
    (1, 1, 1, 1),
    (1, 1, 2, 2),
    (1, 2, 0, 3),
    (1, 2, 1, 2),
    (1, 2, 2, 1),
    (1, 2, 3, 0),
)

ZERO_SUM_ASSIGNMENTS = tuple(
    (first, second, third, first ^ second ^ third)
    for first, second, third in product(range(4), repeat=3)
)

CANDIDATES = {
    0: (1, 2, 3, 4),
    4: (1, 2, 4, 3),
    13: (2, 1, 3, 4),
    22: (2, 1, 3, 4),
}

MINOR_COLUMNS = {
    0: (0, 1, 3, 4, 6, 7, 8, 9),
    4: (0, 1, 3, 4, 5, 6, 8, 9),
    13: (0, 1, 2, 3, 6, 7, 9, 10),
    22: (0, 1, 2, 4, 6, 7, 9, 10),
}


def q(value=0):
    return Quadratic.coerce(value)


def source_values():
    return tuple(
        map(
            q,
            (
                Fraction(3, 5),
                Fraction(1, 2),
                Fraction(2, 3),
                Fraction(3, 4),
                Fraction(1, 2),
                Fraction(9, 20),
                Fraction(2, 5),
                Fraction(1, 3),
                Fraction(1, 5),
                Fraction(1, 2),
                Fraction(3, 8),
                Fraction(1, 2),
            ),
        )
    )


def target_values():
    return (
        24835 * BETA / (20678 - 24835 * BETA),
        q(Fraction(1, 2)),
        q(Fraction(2, 3)),
        q(Fraction(3, 4)),
        q(10339) / (53010 * BETA),
        q(Fraction(9934, 12215)),
        q(Fraction(171, 775)),
        q(Fraction(1, 2)),
        q(Fraction(3, 20)) / BETA,
        q(Fraction(1, 2)),
        q(Fraction(31, 190)),
        q(Fraction(1767, 4832)),
    )


def common_parameters():
    source = source_values()
    target = target_values()
    result = {
        22: source + (q(Fraction(1, 2)), q(Fraction(1, 2))),
        13: (
            source[2] * source[3],
            source[0],
            source[1],
            source[2],
            source[4] / source[2],
            *source[5:],
            q(Fraction(1, 2)),
            q(Fraction(1, 2)),
        ),
    }

    x = target[0]
    x_ac = target[2] * target[3]
    y = q(Fraction(1, 2)) * x_ac + q(Fraction(1, 2)) * x * target[1]
    redirected = (
        x,
        target[2],
        target[3],
        target[1],
        target[4],
        target[5] * y / x,
        target[6],
        target[7],
        target[9],
        target[10],
        target[8] * x / y,
        target[11],
        q(Fraction(1, 2)),
        q(Fraction(1, 2)),
    )
    result[0] = redirected
    result[4] = (
        redirected[0],
        q(Fraction(3, 4)),
        q(Fraction(4, 3)) * redirected[4],
        redirected[5],
        redirected[6],
        redirected[7],
        redirected[1] * redirected[2],
        redirected[3],
        redirected[8],
        redirected[9],
        redirected[11],
        redirected[10],
        redirected[13],
        redirected[12],
    )
    assert all(len(values) == 14 for values in result.values())
    return result


def evaluate(network, labels, assignments, values):
    edges = tuple(tuple(edge) for edge in network["edges"])
    reticulations = reticulation_vertices(network["vertices"])
    edge_values = values[: len(edges)]
    inheritance = dict(zip(reticulations, values[len(edges) :]))
    return evaluate_jc_coordinates(
        network["vertices"],
        edges,
        dict(zip(network["leaves"], labels)),
        assignments,
        edge_values,
        inheritance,
    )


def determinant(matrix):
    matrix = [list(row) for row in matrix]
    size = len(matrix)
    result = ONE
    for column in range(size):
        pivot = next(row for row in range(column, size) if matrix[row][column])
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            result = -result
        pivot_value = matrix[column][column]
        result *= pivot_value
        inverse = pivot_value.inverse()
        for index in range(column, size):
            matrix[column][index] *= inverse
        for row in range(column + 1, size):
            multiplier = matrix[row][column]
            if not multiplier:
                continue
            for index in range(column, size):
                matrix[row][index] -= multiplier * matrix[column][index]
    return result


def rank_minor(network, labels, values, columns):
    rows = []
    for parameter_index in columns:
        at_zero = list(values)
        at_one = list(values)
        at_zero[parameter_index] = ZERO
        at_one[parameter_index] = ONE
        zero_coordinates = evaluate(network, labels, JC_REPRESENTATIVES[1:9], at_zero)
        one_coordinates = evaluate(network, labels, JC_REPRESENTATIVES[1:9], at_one)
        rows.append(tuple(one - zero for one, zero in zip(one_coordinates, zero_coordinates)))
    return determinant(tuple(zip(*rows)))


def main():
    _raw, networks = enumerate_networks()
    parameters = common_parameters()
    base = evaluate(networks[22], CANDIDATES[22], ZERO_SUM_ASSIGNMENTS, parameters[22])

    for network_index in (0, 4, 13):
        candidate = evaluate(
            networks[network_index],
            CANDIDATES[network_index],
            ZERO_SUM_ASSIGNMENTS,
            parameters[network_index],
        )
        assert candidate == base

    determinants = {}
    for network_index in sorted(CANDIDATES):
        value = rank_minor(
            networks[network_index],
            CANDIDATES[network_index],
            parameters[network_index],
            MINOR_COLUMNS[network_index],
        )
        assert value
        determinants[network_index] = value.compact()

    expected_rational = Quadratic(Fraction(-14348907, 13107200000000000000000))
    assert determinants[13] == expected_rational.compact()
    assert determinants[22] == expected_rational.compact()
    print("pure_stdlib_common_coordinates", len(base))
    print("pure_stdlib_nonzero_rank_eight_determinants", determinants)


if __name__ == "__main__":
    main()
