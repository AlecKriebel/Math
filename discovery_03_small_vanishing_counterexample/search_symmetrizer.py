#!/usr/bin/env python3
"""Search for a nonsingular symmetric form that symmetrizes the 22D map."""

from __future__ import annotations

import random

import sympy as sp

from compressed_construction import compressed_cubic_map


MODULUS = 1_000_003


def mod_rational(value):
    value = sp.Rational(value)
    return int(value.p % MODULUS) * pow(int(value.q), -1, MODULUS) % MODULUS


class ModularRowBasis:
    def __init__(self, width):
        self.width = width
        self.rows = {}
        self.original_rows = []

    def add(self, rational_row):
        row = [mod_rational(value) for value in rational_row]
        for pivot in sorted(self.rows):
            if row[pivot]:
                factor = row[pivot]
                basis_row = self.rows[pivot]
                row = [
                    (entry - factor * base) % MODULUS
                    for entry, base in zip(row, basis_row)
                ]
        pivot = next((index for index, value in enumerate(row) if value), None)
        if pivot is None:
            return False
        inverse = pow(row[pivot], -1, MODULUS)
        row = [(value * inverse) % MODULUS for value in row]
        for old_pivot, basis_row in list(self.rows.items()):
            if basis_row[pivot]:
                factor = basis_row[pivot]
                self.rows[old_pivot] = [
                    (entry - factor * new_entry) % MODULUS
                    for entry, new_entry in zip(basis_row, row)
                ]
        self.rows[pivot] = row
        self.original_rows.append(rational_row)
        return True


def coefficient_matrices(variables, mapping):
    jacobian = sp.Matrix(mapping).jacobian(variables)
    monomials = sorted(
        set().union(*[set(sp.Poly(entry, *variables).monoms()) for entry in jacobian])
    )
    matrices = []
    for monomial in monomials:
        matrix = sp.Matrix(
            [
                [sp.Poly(jacobian[i, j], *variables).coeff_monomial(monomial) for j in range(len(variables))]
                for i in range(len(variables))
            ]
        )
        if matrix != sp.zeros(len(variables)):
            matrices.append(matrix)
    return matrices


def symmetrizer_system(matrices):
    dimension = matrices[0].rows
    positions = [(i, j) for i in range(dimension) for j in range(i, dimension)]
    position_index = {position: index for index, position in enumerate(positions)}
    basis = ModularRowBasis(len(positions))

    for matrix in matrices:
        for i in range(dimension):
            for j in range(i + 1, dimension):
                row = [sp.Integer(0)] * len(positions)
                for k in range(dimension):
                    first = matrix[k, i]
                    if first:
                        row[position_index[tuple(sorted((k, j)))]] += first
                    second = matrix[k, j]
                    if second:
                        row[position_index[tuple(sorted((i, k)))]] -= second
                if any(row):
                    basis.add(row)
    exact_matrix = sp.Matrix(basis.original_rows)
    return positions, basis, exact_matrix


def vector_to_symmetric(vector, positions, dimension):
    matrix = sp.zeros(dimension)
    for value, (i, j) in zip(vector, positions):
        matrix[i, j] = value
        matrix[j, i] = value
    return matrix


def main():
    variables, mapping, _, _ = compressed_cubic_map()
    matrices = coefficient_matrices(variables, mapping)
    positions, modular_basis, exact_system = symmetrizer_system(matrices)
    nullity_modular = len(positions) - len(modular_basis.rows)
    print(
        "dimension", len(variables), "coefficient matrices", len(matrices),
        "symmetric unknowns", len(positions), "modular rank", len(modular_basis.rows),
        "modular nullity", nullity_modular,
    )
    if nullity_modular == 0:
        print("No nonzero symmetrizer exists modulo the test prime.")
        return

    nullspace = exact_system.nullspace()
    print("exact nullity", len(nullspace))
    symmetric_basis = [
        vector_to_symmetric(vector, positions, len(variables))
        for vector in nullspace
    ]
    rng = random.Random(20260721)
    trials = [[1 if index == chosen else 0 for index in range(len(nullspace))] for chosen in range(len(nullspace))]
    trials += [[rng.randint(-4, 4) for _ in nullspace] for _ in range(200)]
    for coefficients in trials:
        candidate = sp.zeros(len(variables))
        for coefficient, basis_matrix in zip(coefficients, symmetric_basis):
            candidate += coefficient * basis_matrix
        determinant = candidate.det()
        if determinant:
            print("NONSINGULAR SYMMETRIZER FOUND")
            print("coefficients", coefficients)
            print("determinant", determinant)
            return
    print("No nonsingular combination found in deterministic trials.")


if __name__ == "__main__":
    main()
