#!/usr/bin/env python3
"""Verify the exact spin-flip interpretation of the second 37D component.

Only the Python standard library is used.  The constrained Hessian and
its kernel are independently reconstructed from Q3 by the standard-library
derivation module in this directory.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
DERIVATION = HERE / "derive_n3_boundary_effective_quartic.py"
DECOMPOSITION = (
    HERE / "certificates" / "n3_boundary_effective_zero_decomposition.json"
)


def load_derivation():
    spec = importlib.util.spec_from_file_location("n3_derivation", DERIVATION)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


derive = load_derivation()

Gaussian = tuple[Fraction, Fraction]
ZERO: Gaussian = (Fraction(0), Fraction(0))
ONE: Gaussian = (Fraction(1), Fraction(0))
I: Gaussian = (Fraction(0), Fraction(1))


def gadd(first: Gaussian, second: Gaussian) -> Gaussian:
    return (first[0] + second[0], first[1] + second[1])


def gneg(value: Gaussian) -> Gaussian:
    return (-value[0], -value[1])


def gconjugate(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def gscale(value: Gaussian, scalar: Fraction) -> Gaussian:
    return (scalar * value[0], scalar * value[1])


def add_entry(output, key, value: Gaussian) -> None:
    output[key] = gadd(output.get(key, ZERO), value)
    if output[key] == ZERO:
        del output[key]


def matrix_multiply(first, second):
    output = []
    for row in range(len(first)):
        output_row = []
        for column in range(len(second[0])):
            value = ZERO
            for middle in range(len(second)):
                value = gadd(
                    value,
                    derive.gmul(
                        first[row][middle], second[middle][column]
                    ),
                )
            output_row.append(value)
        output.append(output_row)
    return output


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def kronecker(first, second):
    return [
        [
            derive.gmul(
                first[row // len(second)][column // len(second[0])],
                second[row % len(second)][column % len(second[0])],
            )
            for column in range(len(first[0]) * len(second[0]))
        ]
        for row in range(len(first) * len(second))
    ]


def check_spinflip_identity() -> None:
    epsilon = [[ZERO, gneg(ONE)], [ONE, ZERO]]
    assert transpose(epsilon) == [
        [gneg(value) for value in row] for row in epsilon
    ]
    traceless_basis = [
        [[ONE, ZERO], [ZERO, gneg(ONE)]],
        [[ZERO, ONE], [ZERO, ZERO]],
        [[ZERO, ZERO], [ONE, ZERO]],
    ]
    symmetric_factors = []
    for matrix in traceless_basis:
        product = matrix_multiply(epsilon, matrix)
        assert transpose(product) == product
        symmetric_factors.append(product)
    for first in symmetric_factors:
        for second in symmetric_factors:
            for third in symmetric_factors:
                product = kronecker(kronecker(first, second), third)
                assert transpose(product) == product


def j_action(row):
    """Return J|row> for J=epsilon^tensor3."""
    return (
        Fraction(-1) ** sum(row),
        tuple(1 - bit for bit in row),
    )


def spinflip(frame):
    """Return -J conjugate(frame) epsilon."""
    output = {}
    for (row, column), value in frame.items():
        sign, complement = j_action(row)
        if column == 0:
            add_entry(
                output,
                (complement, 1),
                gscale(gconjugate(value), sign),
            )
        else:
            add_entry(
                output,
                (complement, 0),
                gscale(gconjugate(value), -sign),
            )
    return output


LABEL_TO_COORDINATE = {
    label: index for index, label in enumerate(derive.LABELS)
}


def gauge_to_chart(left, right):
    """Set the right logical tangent to zero and encode chart coordinates."""
    right_logical = [
        [right.get((derive.V0[row], column), ZERO) for column in range(2)]
        for row in range(2)
    ]
    for row in range(2):
        for column in range(2):
            add_entry(
                left,
                (derive.U0[row], column),
                gneg(right_logical[row][column]),
            )
            add_entry(
                right,
                (derive.V0[row], column),
                gneg(right_logical[row][column]),
            )

    assert all(
        right.get((row, column), ZERO) == ZERO
        for row in derive.V0
        for column in range(2)
    )
    output = defaultdict(Fraction)
    for side, frame, base in (
        ("U", left, set(derive.U0)),
        ("V", right, set(derive.V0)),
    ):
        for (row, column), value in frame.items():
            if row in base:
                continue
            if value[0]:
                output[
                    LABEL_TO_COORDINATE[(side, row, column, "real")]
                ] += value[0]
            if value[1]:
                output[
                    LABEL_TO_COORDINATE[(side, row, column, "imag")]
                ] += value[1]

    logical = [
        [left.get((derive.U0[row], column), ZERO) for column in range(2)]
        for row in range(2)
    ]
    assert all(
        logical[row][column]
        == gneg(gconjugate(logical[column][row]))
        for row in range(2)
        for column in range(2)
    )
    assert logical[0][0][0] == logical[1][1][0] == 0
    output[LABEL_TO_COORDINATE[("logical", 0)]] += logical[0][0][1]
    output[LABEL_TO_COORDINATE[("logical", 1)]] += logical[1][1][1]
    output[LABEL_TO_COORDINATE[("logical", 2)]] += logical[0][1][0]
    output[LABEL_TO_COORDINATE[("logical", 3)]] += logical[0][1][1]
    return {index: value for index, value in output.items() if value}


def spinflip_chart_directions():
    base_left = {
        (derive.U0[0], 0): ONE,
        (derive.U0[1], 1): ONE,
    }
    assert spinflip(base_left) == {
        (derive.V0[0], 0): ONE,
        (derive.V0[1], 1): ONE,
    }

    directions = []
    qubit_rows = [
        (first, second, third)
        for first in range(2)
        for second in range(2)
        for third in range(2)
    ]

    # Twenty-four horizontal Stiefel directions.
    for row in qubit_rows:
        if row in derive.U0:
            continue
        for column in range(2):
            for phase in (ONE, I):
                left = {(row, column): phase}
                directions.append(
                    gauge_to_chart(dict(left), spinflip(left))
                )

    # Four u(2) Stiefel directions.
    logical_generators = (
        ((I, ZERO), (ZERO, ZERO)),
        ((ZERO, ZERO), (ZERO, I)),
        ((ZERO, ONE), (gneg(ONE), ZERO)),
        ((ZERO, I), (I, ZERO)),
    )
    for generator in logical_generators:
        left = {}
        for row in range(2):
            for column in range(2):
                if generator[row][column] != ZERO:
                    left[derive.U0[row], column] = generator[row][column]
        directions.append(gauge_to_chart(dict(left), spinflip(left)))

    # Twelve local-plane graph directions.
    for site in range(3):
        for bit in range(2):
            for phase in (ONE, I):
                left = {}
                right = {}
                for base, output in ((derive.U0, left), (derive.V0, right)):
                    for logical, row in enumerate(base):
                        if row[site] != bit:
                            continue
                        moved = list(row)
                        moved[site] = 2
                        output[tuple(moved), logical] = phase
                directions.append(gauge_to_chart(left, right))

    assert len(directions) == 40
    return directions


def dense_rref(rows, dimension):
    work = []
    for row in rows:
        if isinstance(row, dict):
            dense = [
                Fraction(row.get(index, 0)) for index in range(dimension)
            ]
        else:
            dense = [Fraction(value) for value in row]
            assert len(dense) == dimension
        if any(dense):
            work.append(dense)
    pivot_row = 0
    for column in range(dimension):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(
                    work[row], work[pivot_row]
                )
            ]
        pivot_row += 1
    return tuple(tuple(row) for row in work[:pivot_row])


def nullspace_rows(rows, dimension):
    reduced = dense_rref(rows, dimension)
    pivots = [
        next(index for index, value in enumerate(row) if value)
        for row in reduced
    ]
    output = []
    for free in range(dimension):
        if free in pivots:
            continue
        vector = [Fraction(0) for _ in range(dimension)]
        vector[free] = 1
        for row, pivot in zip(reduced, pivots):
            vector[pivot] = -row[free]
        output.append(
            {index: value for index, value in enumerate(vector) if value}
        )
    return output


def decode_component(data, dimension):
    return [
        {
            index: Fraction(numerator, denominator)
            for index, (numerator, denominator) in row
        }
        for row in data
    ]


EXPECTED_ANNIHILATOR = [
    {5: Fraction(1), 6: Fraction(1)},
    {8: Fraction(1), 9: Fraction(-1)},
    {17: Fraction(1), 18: Fraction(1)},
    {20: Fraction(1), 21: Fraction(-1)},
    {27: Fraction(1), 28: Fraction(-1)},
    {30: Fraction(1), 31: Fraction(1)},
    *({index: Fraction(1)} for index in (
        36, 37, 40, 41, 42, 43, 44, 45, 48, 49, 52, 53
    )),
]


def main() -> None:
    check_spinflip_identity()
    chart_directions = spinflip_chart_directions()
    assert len(dense_rref(chart_directions, len(derive.COORDINATES))) == 37

    hessian = derive.derive_hessian()
    kernel, _ = derive.derive_kernel_and_pivots(hessian)
    components = derive.connected_components(hessian)
    nonpivots = []
    for component in components:
        pivot = max(component, key=lambda index: hessian[index][index])
        nonpivots.extend(index for index in component if index != pivot)
    assert len(nonpivots) == len(kernel) == 55

    kernel_directions = []
    for original in chart_directions:
        coordinates = {
            variable: original.get(nonpivot, 0)
            for variable, nonpivot in enumerate(nonpivots)
            if original.get(nonpivot, 0)
        }
        reconstructed = defaultdict(Fraction)
        for variable, value in coordinates.items():
            for coordinate, coefficient in kernel[variable].items():
                reconstructed[coordinate] += value * coefficient
        assert {
            coordinate: value
            for coordinate, value in reconstructed.items()
            if value
        } == original
        kernel_directions.append(coordinates)

    assert len(dense_rref(kernel_directions, 55)) == 37
    annihilator = dense_rref(nullspace_rows(kernel_directions, 55), 55)
    assert len(annihilator) == 18
    assert annihilator == dense_rref(EXPECTED_ANNIHILATOR, 55)

    certificate = json.loads(DECOMPOSITION.read_text())
    assert certificate["format"] == "n3-boundary-effective-zero-decomposition-v1"
    assert certificate["dimension"] == 55
    matches = []
    for number, component in enumerate(certificate["components"]):
        decoded = decode_component(component, 55)
        if dense_rref(decoded, 55) == annihilator:
            matches.append(number)
    assert matches == [1]

    print(
        "verified exact local-qubit spin-flip tangent:",
        "40 parameters, rank 37 in the 204D chart,",
        "rank 37 in the 55D Hessian kernel,",
        "18-dimensional annihilator, unique zero-component match 1",
    )


if __name__ == "__main__":
    main()
