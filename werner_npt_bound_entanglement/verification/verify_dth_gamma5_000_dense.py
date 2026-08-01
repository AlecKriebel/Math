#!/usr/bin/env python3
"""Independent exact dense check of the Gamma5 ``(00,00,00)`` chart.

This verifier deliberately uses the small 27-dimensional rational
multiplicity block instead of expanding three 18-term local carrier vectors
into raw five-replica words.  It checks pair/Pluecker support rank two,
vanishing D5 rank, and equality of the primitive restriction chart recorded
in ``agent_dth_gamma5_000_chart.py``.
"""

from functools import reduce
from math import gcd
import sys

import sympy as sp

sys.path.insert(0, "verification")
import agent_dth_exact_gamma5_face_coordinates as dense
import agent_dth_gamma5_000_chart as certificate


def primitive_columns(matrix):
    output = sp.zeros(matrix.rows, matrix.cols)
    for column in range(matrix.cols):
        denominators = [int(sp.denom(matrix[row, column]))
                        for row in range(matrix.rows)]
        common = reduce(sp.ilcm, denominators, 1)
        values = [int(matrix[row, column] * common)
                  for row in range(matrix.rows)]
        divisor = reduce(gcd, (abs(value) for value in values if value), 0)
        values = [value // divisor for value in values]
        first = next(value for value in values if value)
        if first < 0:
            values = [-value for value in values]
        for row, value in enumerate(values):
            output[row, column] = value
    return output


def main():
    shapes = (5, 5, 5)
    support = dense.pair_pluecker_coordinates(shapes)
    physical, gram, restriction = dense.gamma5_face_coordinates(shapes)
    chart, pivots = dense.gamma5_face_chart(shapes)
    expected = sp.Matrix(certificate.PRIMITIVE_CHART)

    assert support.shape == (certificate.RAW_RANK,
                             certificate.SUPPORT_RANK)
    assert support.rank() == certificate.SUPPORT_RANK
    assert physical.shape == (certificate.RAW_RANK,
                              certificate.FACE_RANK)
    assert physical.rank() == certificate.FACE_RANK
    assert dense.delta_gram(shapes) * support == sp.zeros(
        certificate.RAW_RANK, certificate.SUPPORT_RANK
    )
    d0 = dense.kron3(tuple(dense.local_delta(shape, 0)
                           for shape in shapes))
    d2 = dense.kron3(tuple(dense.local_delta(shape, 2)
                           for shape in shapes))
    assert (d0 - d2) * support == sp.zeros(d0.rows,
                                            certificate.SUPPORT_RANK)
    assert (d0 + d2) * support == sp.zeros(d0.rows,
                                            certificate.SUPPORT_RANK)
    assert sp.Matrix.hstack(physical, support).rank() == (
        certificate.SUPPORT_RANK
    )
    assert restriction == gram * physical
    assert primitive_columns(chart) == expected
    assert tuple(pivots) == certificate.PIVOT_ROWS

    print("exact dense Gamma5 (00,00,00) chart passed")
    print("raw/support/delta/face:",
          certificate.RAW_RANK, certificate.SUPPORT_RANK,
          certificate.DELTA_RANK, certificate.FACE_RANK)
    print("primitive chart absolute pivot determinant: 12")


if __name__ == "__main__":
    main()
