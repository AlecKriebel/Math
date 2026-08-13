#!/usr/bin/env python3
"""One targeted exact audit of low fixed-colour sectors on a hostile K4 ray.

This is not an architecture scan.  It constructs the positively cleared L
and D matrices over a truncated QQ power-series ring, differentiates their
tree determinants, and converts the Taylor coefficients to the canonical
degree-420 Bernstein controls.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations
from math import comb


N = 4
FULL = (1 << N) - 1
ORDER = 12
ZERO = (F(0),) * (ORDER + 1)
ONE = (F(1),) + (F(0),) * ORDER


def p_add(*values):
    return tuple(sum((value[k] for value in values), F(0)) for k in range(ORDER + 1))


def p_neg(value):
    return tuple(-entry for entry in value)


def p_scale(value, scalar):
    return tuple(scalar * entry for entry in value)


def p_mul(left, right):
    return tuple(
        sum((left[i] * right[k - i] for i in range(k + 1)), F(0))
        for k in range(ORDER + 1)
    )


def subsets(items):
    items = tuple(items)
    for mask in range(1 << len(items)):
        yield tuple(items[index] for index in range(len(items)) if (mask >> index) & 1)


def linear(constant, slope):
    return (F(constant), F(slope)) + (F(0),) * (ORDER - 1)


def witness_data():
    # This is the already-frozen nonregular orientation witness; no graph
    # search is performed here.
    witness = {(0, 1): 0, (0, 2): 1000, (0, 3): 2,
               (1, 2): 1, (1, 3): 1000, (2, 3): 10}
    weights = {}
    for left in range(N):
        for right in range(left + 1, N):
            weights[left, right] = weights[right, left] = linear(
                1, witness[left, right] - 1
            )
    for vertex in range(N):
        weights[vertex, vertex] = ZERO
    degrees = [p_add(*(weights[vertex, other] for other in range(N)))
               for vertex in range(N)]
    factors = {}
    for target in range(N):
        neighbours = tuple(vertex for vertex in range(N) if vertex != target)
        for support in subsets(neighbours):
            if support:
                factors[target, frozenset(support)] = p_add(
                    p_scale(degrees[target], 2),
                    p_neg(p_add(*(weights[target, vertex] for vertex in support))),
                )
    return weights, degrees, factors


def product(values):
    answer = ONE
    for value in values:
        answer = p_mul(answer, value)
    return answer


def add_rate(matrix, row, column, value):
    if row != column:
        matrix[row][column] = p_add(matrix[row][column], value)


def finish_generator(matrix):
    for row in range(len(matrix)):
        matrix[row][row] = p_neg(p_add(*(
            matrix[row][column]
            for column in range(len(matrix))
            if column != row
        )))
    return matrix


def left_hatted(weights, degrees):
    size = FULL
    matrix = [[ZERO for _ in range(size)] for _ in range(size)]
    for state in range(1, FULL + 1):
        for target in range(N):
            if not ((state >> target) & 1):
                continue
            for source in range(N):
                arrow = product(
                    (weights[source, target],)
                    + tuple(degrees[vertex] for vertex in range(N) if vertex != source)
                )
                neutral = (state & ~(1 << target)) | (1 << source)
                selective = state | (1 << source)
                add_rate(matrix, state - 1, neutral - 1, arrow)
                add_rate(matrix, state - 1, selective - 1, arrow)
    return finish_generator(matrix)


def cleared_burst(weights, factors, target, support):
    all_factors = tuple(factors)
    answer = ZERO
    for order in permutations(support):
        prefixes = []
        prefix = set()
        numerator = []
        for vertex in order:
            prefix.add(vertex)
            prefixes.append((target, frozenset(prefix)))
            numerator.append(weights[target, vertex])
        remaining = (factors[key] for key in all_factors if key not in prefixes)
        answer = p_add(answer, product(tuple(numerator) + tuple(remaining)))
    return answer


def death_hatted(weights, factors):
    size = FULL - 1
    matrix = [[ZERO for _ in range(size)] for _ in range(size)]
    laws = {}
    for target in range(N):
        neighbours = tuple(vertex for vertex in range(N) if vertex != target)
        for support in subsets(neighbours):
            if support:
                laws[target, support] = cleared_burst(weights, factors, target, support)
    for state in range(1, FULL):
        for target in range(N):
            if not ((state >> target) & 1):
                continue
            without = state & ~(1 << target)
            for (law_target, support), value in laws.items():
                if law_target != target:
                    continue
                union = sum(1 << vertex for vertex in support)
                output = without | union
                if output < FULL:
                    add_rate(matrix, state - 1, output - 1, value)
    return finish_generator(matrix)


def matrix_coefficient(series_matrix, order):
    return [[entry[order] for entry in row] for row in series_matrix]


def matmul(left, right):
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def matadd(left, right):
    return [[a + b for a, b in zip(row_a, row_b)]
            for row_a, row_b in zip(left, right)]


def matscale(matrix, scalar):
    return [[scalar * entry for entry in row] for row in matrix]


def identity(size):
    return [[F(row == column) for column in range(size)] for row in range(size)]


def inverse(matrix):
    size = len(matrix)
    work = [row[:] + unit[:] for row, unit in zip(matrix, identity(size))]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        value = work[column][column]
        work[column] = [entry / value for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [entry - scale * pivot_entry
                         for entry, pivot_entry in zip(work[row], work[column])]
    return [row[size:] for row in work]


def determinant(matrix):
    work = [row[:] for row in matrix]
    answer = F(1)
    for column in range(len(work)):
        pivot = next(row for row in range(column, len(work)) if work[row][column])
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            scale = work[row][column] / value
            for other in range(column + 1, len(work)):
                work[row][other] -= scale * work[column][other]
    return answer


def trace(matrix):
    return sum((matrix[index][index] for index in range(len(matrix))), F(0))


def determinant_series(generator, ranks):
    size = len(generator)
    coefficients = [matrix_coefficient(generator, order) for order in range(ORDER + 1)]
    coefficients = [matscale(matrix, -1) for matrix in coefficients]
    for row in range(size):
        for column in range(size):
            coefficients[0][row][column] += F(ranks[row])
    inverse_coefficients = [inverse(coefficients[0])]
    for order in range(1, ORDER + 1):
        convolution = [[F(0) for _ in range(size)] for _ in range(size)]
        for k in range(1, order + 1):
            convolution = matadd(
                convolution,
                matmul(coefficients[k], inverse_coefficients[order - k]),
            )
        inverse_coefficients.append(matscale(
            matmul(inverse_coefficients[0], convolution), -1
        ))
    logarithmic_derivative = []
    for order in range(ORDER):
        value = F(0)
        for inverse_order in range(order + 1):
            derivative_order = order - inverse_order
            value += trace(matmul(
                inverse_coefficients[inverse_order],
                matscale(coefficients[derivative_order + 1], derivative_order + 1),
            ))
        logarithmic_derivative.append(value)
    result = [determinant(coefficients[0])]
    for order in range(ORDER):
        coefficient = sum(
            result[k] * logarithmic_derivative[order - k]
            for k in range(order + 1)
        ) / (order + 1)
        result.append(coefficient)
    return result


def convolution(left, right):
    return [sum((left[k] * right[order - k] for k in range(order + 1)), F(0))
            for order in range(ORDER + 1)]


def main():
    weights, degrees, factors = witness_data()
    left = left_hatted(weights, degrees)
    death = death_hatted(weights, factors)
    ranks_l = [state.bit_count() for state in range(1, FULL + 1)]
    ranks_d = [state.bit_count() for state in range(1, FULL)]
    det_z_l = determinant_series(left, [1] * FULL)
    det_y_l = determinant_series(left, ranks_l)
    det_z_d = determinant_series(death, [1] * (FULL - 1))
    det_y_d = determinant_series(death, ranks_d)
    left_product = convolution(det_z_l, det_z_d)
    right_product = convolution(det_y_l, det_y_d)
    taylor = [384 * left_product[k] - 105 * right_product[k]
              for k in range(ORDER + 1)]
    # Determinants are M_L Z and M_D Z, a common positive factor.  Here
    # N_b N_d=32*12=384 and D_b D_d=15*7=105.
    degree = 420
    bernstein = []
    z_bernstein = []
    y_bernstein = []
    for colour in range(ORDER + 1):
        transform = lambda series: sum(
            F(comb(colour, order), comb(degree, order)) * series[order]
            for order in range(colour + 1)
        )
        bernstein.append(transform(taylor))
        z_bernstein.append(sum(
            F(comb(colour, order), comb(degree, order)) * left_product[order]
            for order in range(colour + 1)
        ))
        y_bernstein.append(sum(
            F(comb(colour, order), comb(degree, order)) * right_product[order]
            for order in range(colour + 1)
        ))
    assert taylor[0] == taylor[1] == 0
    root_products = []
    for colour, value in enumerate(bernstein):
        ratio = "-" if colour < 2 else float(value / bernstein[2])
        root_product = y_bernstein[colour] / z_bernstein[colour]
        root_products.append(root_product)
        print(colour, "sign", (value > 0) - (value < 0),
              "ratio_to_C2", ratio, "Eroot", float(root_product))
    assert all(value > 0 for value in bernstein[2:])
    assert all(root_products[index + 1] < root_products[index]
               for index in range(1, ORDER))
    print("C2", bernstein[2])
    print("C3", bernstein[3])


if __name__ == "__main__":
    main()
