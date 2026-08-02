"""Independent rational replay of the JC root path-reversal move Omega.

This verifier imports neither SymPy nor python-flint.  It evaluates displayed
trees directly over ``fractions.Fraction``, checks all 64 zero-sum Fourier
coordinates at the certified common point, and recomputes the four rank-nine
Jacobian minors by exact multilinear finite differences.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product

from enumerate_four_leaf_root_theta import enumerate_networks


SOURCE_LABELS = (1, 2, 3, 4)
TARGET_LABELS = (2, 1, 4, 3)
RANK_ROWS = (0, 1, 2, 3, 4, 5, 6, 7, 9)
N16_COLUMNS = (0, 1, 2, 3, 4, 7, 8, 9, 10)
N26_COLUMNS = (0, 1, 2, 3, 5, 7, 8, 9, 10)

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


def f(numerator, denominator=1):
    return Fraction(numerator, denominator)


POINTS = {
    "N16_source": (
        f(1, 2), f(1, 4), f(1, 2), f(1, 2), f(1, 2), f(1, 2), f(1, 2),
        f(1, 20), f(1, 2), f(1, 2), f(1, 10), f(1, 2), f(1, 2), f(1, 2),
    ),
    "N16_target": (
        f(7, 12), f(1, 7), f(1, 2), f(41, 48), f(28, 41), f(1, 2),
        f(1, 2), f(12, 205), f(1, 2), f(1, 2), f(3, 40), f(1, 2),
        f(1, 2), f(1, 2),
    ),
    "N26_source": (
        f(1, 4), f(1, 2), f(1, 2), f(3, 4), f(2, 3), f(1, 4), f(1, 2),
        f(1, 20), f(1, 2), f(1, 2), f(1, 10), f(1, 2), f(1, 2), f(1, 2),
    ),
    "N26_target": (
        f(1, 7), f(1, 2), f(41, 48), f(19, 24), f(14, 19), f(14, 41),
        f(1, 2), f(12, 205), f(1, 2), f(1, 2), f(3, 40), f(1, 2),
        f(1, 2), f(1, 2),
    ),
}

CANDIDATES = {
    "N16_source": (16, SOURCE_LABELS, N16_COLUMNS),
    "N16_target": (16, TARGET_LABELS, N16_COLUMNS),
    "N26_source": (26, SOURCE_LABELS, N26_COLUMNS),
    "N26_target": (26, TARGET_LABELS, N26_COLUMNS),
}

EXPECTED_MINORS = {
    "N16_source": f(-171, 2305843009213693952000000),
    "N16_target": f(-513, 9223372036854775808000000),
    "N26_source": f(57, 576460752303423488000000),
    "N26_target": f(189, 2305843009213693952000000),
}


def reticulation_vertices(vertices):
    return tuple(sorted(vertex for vertex, color in vertices.items() if color in {"R", "X"}))


def displayed_trees(vertices, edges, leaf_labels):
    reticulations = reticulation_vertices(vertices)
    incoming = {
        reticulation: tuple(
            index for index, (_tail, head) in enumerate(edges) if head == reticulation
        )
        for reticulation in reticulations
    }
    assert all(len(indices) == 2 for indices in incoming.values())
    trees = []
    for choices in product((0, 1), repeat=len(reticulations)):
        excluded = {
            incoming[reticulation][1 - choice]
            for reticulation, choice in zip(reticulations, choices)
        }
        selected = tuple(index for index in range(len(edges)) if index not in excluded)
        children = {}
        for index in selected:
            parent, child = edges[index]
            children.setdefault(parent, []).append(child)
        cache = {}

        def descendants(vertex):
            if vertex not in cache:
                if vertex in leaf_labels:
                    cache[vertex] = frozenset((leaf_labels[vertex],))
                else:
                    cache[vertex] = frozenset().union(
                        *(descendants(child) for child in children.get(vertex, ()))
                    )
            return cache[vertex]

        edge_descendants = {
            index: descendants(edges[index][1]) for index in selected
        }
        trees.append((choices, selected, edge_descendants))
    return reticulations, tuple(trees)


def evaluate_jc_coordinates(
    vertices, edges, leaf_labels, assignments, edge_values, inheritance
):
    reticulations, trees = displayed_trees(vertices, edges, leaf_labels)
    assert set(inheritance) == set(reticulations)
    coordinates = []
    for assignment in assignments:
        character_at_leaf = {
            label: assignment[label - 1] for label in leaf_labels.values()
        }
        total = f(0)
        for choices, selected, descendants in trees:
            term = f(1)
            for reticulation, choice in zip(reticulations, choices):
                probability = inheritance[reticulation]
                term *= probability if choice == 0 else 1 - probability
            for edge_index in selected:
                character = 0
                for leaf in descendants[edge_index]:
                    character ^= character_at_leaf[leaf]
                if character:
                    term *= edge_values[edge_index]
            total += term
        coordinates.append(total)
    return tuple(coordinates)


def evaluate(network, labels, assignments, values):
    edges = tuple(tuple(edge) for edge in network["edges"])
    reticulations = reticulation_vertices(network["vertices"])
    return evaluate_jc_coordinates(
        network["vertices"],
        edges,
        dict(zip(network["leaves"], labels)),
        assignments,
        values[: len(edges)],
        dict(zip(reticulations, values[len(edges) :])),
    )


def determinant(matrix):
    matrix = [list(row) for row in matrix]
    size = len(matrix)
    answer = f(1)
    for column in range(size):
        pivot = next(row for row in range(column, size) if matrix[row][column])
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            answer = -answer
        pivot_value = matrix[column][column]
        answer *= pivot_value
        for index in range(column, size):
            matrix[column][index] /= pivot_value
        for row in range(column + 1, size):
            multiplier = matrix[row][column]
            if multiplier:
                for index in range(column, size):
                    matrix[row][index] -= multiplier * matrix[column][index]
    return answer


def rank_minor(network, labels, values, columns):
    assignments = tuple(JC_REPRESENTATIVES[row + 1] for row in RANK_ROWS)
    derivative_columns = []
    for parameter_index in columns:
        at_zero = list(values)
        at_one = list(values)
        at_zero[parameter_index] = f(0)
        at_one[parameter_index] = f(1)
        zero_coordinates = evaluate(network, labels, assignments, at_zero)
        one_coordinates = evaluate(network, labels, assignments, at_one)
        derivative_columns.append(
            tuple(one - zero for one, zero in zip(one_coordinates, zero_coordinates))
        )
    return determinant(tuple(zip(*derivative_columns)))


def main():
    _raw, networks = enumerate_networks()
    common = None
    minors = {}
    for name, (network_index, labels, columns) in CANDIDATES.items():
        values = POINTS[name]
        assert all(0 < value < 1 for value in values)
        coordinates = evaluate(
            networks[network_index], labels, ZERO_SUM_ASSIGNMENTS, values
        )
        if common is None:
            common = coordinates
        else:
            assert coordinates == common
        minors[name] = rank_minor(networks[network_index], labels, values, columns)

    assert minors == EXPECTED_MINORS
    print("pure_stdlib_common_zero_sum_coordinates", len(common))
    print(
        "pure_stdlib_rank_nine_minors",
        {name: str(value) for name, value in minors.items()},
    )


if __name__ == "__main__":
    main()
