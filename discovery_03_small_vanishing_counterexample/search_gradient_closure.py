#!/usr/bin/env python3
"""Search for a proper nondegenerate collision closure of the 44D gradient map."""

from __future__ import annotations

from itertools import combinations_with_replacement, permutations

import sympy as sp

from compressed_construction import compressed_cubic_map, compressed_collision_points


MODULUS = 1_000_033  # prime, 1 mod 4
I_MOD = 350_504      # I_MOD^2 == -1 mod MODULUS


def mod_complex(value):
    value = sp.expand(value)
    real, imag = value.as_real_imag()
    real = sp.Rational(real)
    imag = sp.Rational(imag)
    real_mod = int(real.p % MODULUS) * pow(int(real.q), -1, MODULUS)
    imag_mod = int(imag.p % MODULUS) * pow(int(imag.q), -1, MODULUS)
    return (real_mod + I_MOD * imag_mod) % MODULUS


class ModularBasis:
    def __init__(self, dimension):
        self.dimension = dimension
        self.rows = []
        self.pivots = []

    def add(self, vector):
        row = [value % MODULUS for value in vector]
        for pivot, basis_row in zip(self.pivots, self.rows):
            if row[pivot]:
                factor = row[pivot]
                row = [
                    (entry - factor * base) % MODULUS
                    for entry, base in zip(row, basis_row)
                ]
        pivot = next((index for index, value in enumerate(row) if value), None)
        if pivot is None:
            return False
        inverse = pow(row[pivot], -1, MODULUS)
        row = [(value * inverse) % MODULUS for value in row]
        for row_index, basis_row in enumerate(self.rows):
            if basis_row[pivot]:
                factor = basis_row[pivot]
                self.rows[row_index] = [
                    (entry - factor * new_entry) % MODULUS
                    for entry, new_entry in zip(basis_row, row)
                ]
        insert_at = sum(old_pivot < pivot for old_pivot in self.pivots)
        self.pivots.insert(insert_at, pivot)
        self.rows.insert(insert_at, row)
        return True


def matrix_inverse_mod(matrix):
    n = len(matrix)
    augmented = [
        [entry % MODULUS for entry in row]
        + [1 if i == j else 0 for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        inverse = pow(augmented[column][column], -1, MODULUS)
        augmented[column] = [(entry * inverse) % MODULUS for entry in augmented[column]]
        for row in range(n):
            if row != column and augmented[row][column]:
                factor = augmented[row][column]
                augmented[row] = [
                    (entry - factor * base) % MODULUS
                    for entry, base in zip(augmented[row], augmented[column])
                ]
    return [row[n:] for row in augmented]


def mat_vec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) % MODULUS for row in matrix]


def gradient_map():
    h_variables, h, _, _ = compressed_cubic_map()
    dimension = len(h_variables)
    a_variables = list(sp.symbols("A1:" + str(dimension + 1)))
    b_variables = list(sp.symbols("B1:" + str(dimension + 1)))
    substitutions = {
        h_variables[index]: a_variables[index] + sp.I * b_variables[index]
        for index in range(dimension)
    }
    potential = sp.expand(
        sp.I * sum(h[index].subs(substitutions) * b_variables[index] for index in range(dimension))
    )
    variables = a_variables + b_variables
    gradient = [sp.expand(sp.diff(potential, variable)) for variable in variables]
    return h_variables, h, variables, potential, gradient


def ordered_tensor(mapping, variables):
    tensor = []
    for component in mapping:
        terms = []
        for monomial, coefficient in sp.Poly(component, *variables).terms():
            if coefficient == 0:
                continue
            indices = []
            for variable_index, exponent in enumerate(monomial):
                indices.extend([variable_index] * exponent)
            ordered = sorted(set(permutations(indices)))
            tensor_coefficient = coefficient / len(ordered)
            modular_coefficient = mod_complex(tensor_coefficient)
            terms.extend((triple, modular_coefficient) for triple in ordered)
        tensor.append(terms)
    return tensor


def tensor_value(tensor, first, second, third):
    result = []
    for terms in tensor:
        value = 0
        for (i, j, k), coefficient in terms:
            value += coefficient * first[i] * second[j] * third[k]
        result.append(value % MODULUS)
    return result


def gradient_collision(h_variables, h):
    points = compressed_collision_points()
    dimension = len(h_variables)
    jacobian = sp.Matrix(h).jacobian(h_variables)
    modular_data = []
    for point in points[:2]:
        substitutions = dict(zip(h_variables, point))
        h_value = [mod_complex(component.subs(substitutions)) for component in h]
        jacobian_value = [
            [mod_complex(jacobian[i, j].subs(substitutions)) for j in range(dimension)]
            for i in range(dimension)
        ]
        point_mod = [mod_complex(value) for value in point]
        modular_data.append((point_mod, h_value, jacobian_value))

    point0, h0, jacobian0 = modular_data[0]
    point1, h1, _ = modular_data[1]
    k0 = [
        [(1 if i == j else 0) + jacobian0[j][i] for j in range(dimension)]
        for i in range(dimension)
    ]
    k0 = [[entry % MODULUS for entry in row] for row in k0]
    rhs = [I_MOD * (a - b) % MODULUS for a, b in zip(h0, h1)]
    y0 = mat_vec(matrix_inverse_mod(k0), rhs)
    y1 = [0] * dimension
    z0 = [
        (coordinate - I_MOD * dual) % MODULUS
        for coordinate, dual in zip(point0, y0)
    ] + y0
    z1 = point1 + y1
    return z0, z1


def rank_mod(matrix):
    basis = ModularBasis(len(matrix[0]) if matrix else 0)
    for row in matrix:
        basis.add(row)
    return len(basis.rows)


def main():
    h_variables, h, variables, potential, gradient = gradient_map()
    print("potential terms", len(sp.Poly(potential, *variables).terms()), flush=True)
    print("gradient terms", sum(len(sp.Poly(component, *variables).terms()) for component in gradient), flush=True)
    tensor = ordered_tensor(gradient, variables)
    collision = gradient_collision(h_variables, h)
    basis = ModularBasis(len(variables))
    basis.add(collision[0])
    basis.add(collision[1])

    round_index = 0
    while True:
        current = list(basis.rows)
        for i, j, k in combinations_with_replacement(range(len(current)), 3):
            basis.add(tensor_value(tensor, current[i], current[j], current[k]))
        print("round", round_index, "dimension", len(basis.rows), flush=True)
        round_index += 1
        if len(basis.rows) == len(current):
            break

    gram = [
        [sum(a * b for a, b in zip(first, second)) % MODULUS for second in basis.rows]
        for first in basis.rows
    ]
    print("closure dimension", len(basis.rows))
    print("Gram rank", rank_mod(gram))


if __name__ == "__main__":
    main()
