#!/usr/bin/env python3
"""Rigorous CRT replay of every mixed-face equation for a DTH certificate.

The certificate stores exact rational holomorphic K-coordinate matrices.
This verifier clears one global coordinate denominator and obtains an
integer raw holomorphic restriction tensor.  It applies the integer
numerator of the exact local crossing modulo a deterministic sequence of
good primes, then checks *all* primitive integer left-kernel equations of
the exact 2266-dimensional product face.

The modular checks are converted to an exact characteristic-zero theorem by
an explicit coefficient bound.  If ``P`` is the product of the checked
primes and ``B`` bounds the absolute value of every integer residual, then

    residual == 0 (mod P),  P > 2 B

forces every residual to be zero over ZZ.  Thus floating-point arithmetic,
rank tolerances, and probabilistic prime arguments are absent.

This proves exact partial-transpose consistency with the product face.  PSD,
trace, and objective signs are intentionally audited by independent small
block verifiers.
"""

from __future__ import annotations

from fractions import Fraction
from functools import reduce
from itertools import product
from math import gcd
from pathlib import Path
import argparse
import importlib.util
import json
import math

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


KCHART = import_file("dth_exact_k_full_crt", HERE / "agent_dth_exact_k_coordinates.py")
FCHART = import_file("dth_exact_face_full_crt", HERE / "agent_dth_exact_face_coordinates.py")
CERTIFICATE_IO = import_file(
    "dth_certificate_io_full_crt", HERE / "agent_dth_certificate_io.py"
)
BRIDGE = KCHART.BRIDGE

HOL_SCALE = 360
CROSS_SCALE = 14_400
EXPECTED_FACE_RANK = 2266
EXPECTED_EQUATIONS = 826_573


def lcm(left, right):
    return abs(left // gcd(left, right) * right)


def block_ranges(multiplicities):
    result = []
    offset = 0
    for multiplicity in multiplicities:
        result.append(np.arange(
            offset, offset + multiplicity * multiplicity
        ).reshape(multiplicity, multiplicity))
        offset += multiplicity * multiplicity
    assert offset == 103
    return result


def block_indices(ranges, shapes):
    grids = [ranges[s] for s in shapes]
    return (
        grids[0][:, None, None, :, None, None],
        grids[1][None, :, None, None, :, None],
        grids[2][None, None, :, None, None, :],
    )


def put_block(tensor, ranges, shapes, dimensions, matrix):
    tensor[block_indices(ranges, shapes)] = matrix.reshape(
        (*dimensions, *dimensions)
    )


def get_block(tensor, ranges, shapes, dimensions):
    size = math.prod(dimensions)
    return tensor[block_indices(ranges, shapes)].reshape(size, size)


def parse_certificate(path):
    path = Path(path)
    if path.suffix == ".gz":
        coordinates, _ = CERTIFICATE_IO.read_certificate(path)
        common_denominator = 1
        for matrix in coordinates.values():
            for row in matrix:
                for value in row:
                    common_denominator = lcm(
                        common_denominator, value.denominator
                    )
        return coordinates, common_denominator
    data = json.loads(Path(path).read_text())
    assert data["version"] == 1
    coordinates = {}
    common_denominator = 1
    for shapes in product(range(5), repeat=3):
        tag = "".join(map(str, shapes))
        block = data["blocks"][tag]
        dimension = int(block["dimension"])
        entries = [Fraction(int(pair[0]), int(pair[1]))
                   for pair in block["upper"]]
        assert len(entries) == dimension * (dimension + 1) // 2
        matrix = [[Fraction(0) for _ in range(dimension)]
                  for _ in range(dimension)]
        position = 0
        for i in range(dimension):
            matrix[i][i] = entries[position]
            position += 1
        for i in range(dimension):
            for j in range(i + 1, dimension):
                matrix[i][j] = matrix[j][i] = entries[position]
                position += 1
        coordinates[shapes] = matrix
        for value in entries:
            common_denominator = lcm(common_denominator, value.denominator)
    assert len(coordinates) == 125
    return coordinates, common_denominator


def coordinate_denominator(coordinates):
    denominator = 1
    for matrix in coordinates.values():
        for row in matrix:
            for value in row:
                denominator = lcm(denominator, Fraction(value).denominator)
    return denominator


def exact_crossing_numerator():
    hol, mixed, _, _ = BRIDGE.exact_restriction_bridge()
    h = sp.polys.matrices.DomainMatrix.from_list_sympy(103, 103, hol)
    m = sp.polys.matrices.DomainMatrix.from_list_sympy(103, 103, mixed)
    inverse_numerator, denominator = h.inv_den()
    numerator = (m * inverse_numerator).to_Matrix()
    common = reduce(gcd, [abs(int(value)) for value in numerator if value]
                    + [int(denominator)])
    denominator = int(denominator) // common
    assert denominator == CROSS_SCALE
    integer = np.asarray([
        [int(numerator[row, column]) // common for column in range(103)]
        for row in range(103)
    ], dtype=object)
    assert max(abs(int(value)) for value in integer.flat) == 115_200
    return integer


def integer_hol_charts(coordinates, common_denominator):
    charts = {}
    integer_coordinates = {}
    hol_bound = 0
    total_dimension = 0
    for count, shapes in enumerate(product(range(5), repeat=3), 1):
        _, _, exact_range = KCHART.hol_k_coordinates(shapes)
        chart = np.asarray([
            [int(HOL_SCALE * exact_range[row, column])
             for column in range(exact_range.cols)]
            for row in range(exact_range.rows)
        ], dtype=object)
        assert all(HOL_SCALE * exact_range[row, column]
                   == int(HOL_SCALE * exact_range[row, column])
                   for row in range(exact_range.rows)
                   for column in range(exact_range.cols))
        coordinate = coordinates[shapes]
        assert len(coordinate) == chart.shape[1]
        if chart.shape[1]:
            integer_coordinate = np.asarray([
                [value.numerator * (common_denominator // value.denominator)
                 for value in row]
                for row in coordinate
            ], dtype=object)
        else:
            integer_coordinate = np.zeros((0, 0), dtype=object)
        charts[shapes] = chart
        integer_coordinates[shapes] = integer_coordinate
        total_dimension += chart.shape[1] * (chart.shape[1] + 1) // 2
        if chart.shape[1]:
            maximum_coordinate = max(
                abs(int(value)) for value in integer_coordinate.flat
            )
            maximum_row_sum = max(
                sum(abs(int(value)) for value in row) for row in chart
            )
            hol_bound = max(
                hol_bound,
                maximum_coordinate * maximum_row_sum * maximum_row_sum,
            )
        if count % 25 == 0:
            print("integer hol charts", count, "/125", flush=True)
    assert total_dimension == 4139
    return charts, integer_coordinates, hol_bound


def primitive_left_kernel(face, pivot_rows):
    """Return a primitive integer basis L with L*face=0."""
    rows, rank = face.shape
    if not rank:
        return np.eye(rows, dtype=object)
    principal = face[list(pivot_rows), :]
    inverse = principal.inv()
    outside = [row for row in range(rows) if row not in set(pivot_rows)]
    result = np.zeros((len(outside), rows), dtype=object)
    for output_row, q in enumerate(outside):
        alpha = face[q, :] * inverse
        values = {q: sp.Integer(1)}
        for pivot, value in zip(pivot_rows, alpha):
            values[int(pivot)] = values.get(int(pivot), sp.Integer(0)) - value
        denominator = 1
        for value in values.values():
            denominator = sp.ilcm(denominator, int(sp.denom(value)))
        integer = {
            row: int(value * denominator)
            for row, value in values.items() if value
        }
        common = reduce(gcd, [abs(value) for value in integer.values()])
        integer = {row: value // common for row, value in integer.items()}
        first = next(value for _, value in sorted(integer.items()) if value)
        if first < 0:
            integer = {row: -value for row, value in integer.items()}
        for row, value in integer.items():
            result[output_row, row] = value
    # Literal exact annihilation, independently of the later CRT test.
    assert sp.Matrix(result.tolist()) * face == sp.zeros(len(outside), rank)
    return result


def integer_face_kernels(with_charts=False):
    kernels = {}
    charts = {}
    pivot_rows = {}
    total_rank = 0
    total_equations = 0
    maximum_l1 = 0
    for count, shapes in enumerate(product(range(6), repeat=3), 1):
        face, pivots = FCHART.face_chart(shapes)
        assert all(value == int(value) for value in face)
        kernel = primitive_left_kernel(face, pivots)
        kernels[shapes] = kernel
        if with_charts:
            charts[shapes] = np.asarray(face.tolist(), dtype=object)
            pivot_rows[shapes] = tuple(map(int, pivots))
        total_rank += face.cols
        total_equations += kernel.shape[0] * face.rows
        if kernel.shape[0]:
            maximum_l1 = max(
                maximum_l1,
                max(sum(abs(int(value)) for value in row) for row in kernel),
            )
        if count % 24 == 0:
            print("integer face kernels", count, "/216", flush=True)
    assert total_rank == EXPECTED_FACE_RANK
    assert total_equations == EXPECTED_EQUATIONS
    if with_charts:
        return kernels, maximum_l1, charts, pivot_rows
    return kernels, maximum_l1


def mod_matrix(matrix, prime):
    source = np.asarray(matrix, dtype=object)
    if not source.size:
        return np.zeros(source.shape, dtype=np.int64)
    values = [int(value) % prime for value in source.flat]
    return np.asarray(values, dtype=np.int64).reshape(source.shape)


def mode_apply_mod(local, tensor, axis, prime):
    out = np.tensordot(local, tensor, axes=(1, axis)) % prime
    if axis:
        order = list(range(1, out.ndim))
        order.insert(axis, 0)
        out = out.transpose(order)
    return out


def crossing_apply_mod(local, tensor, prime):
    out = mode_apply_mod(local, tensor, 0, prime)
    out = mode_apply_mod(local, out, 1, prime)
    out = mode_apply_mod(local, out, 2, prime)
    return out


def replay_prime(prime, crossing, hol_charts, coordinates, face_kernels,
                 hol_ranges, mixed_ranges, face_pivot_rows=None):
    crossing_mod = mod_matrix(crossing, prime)
    hol_tensor = np.zeros((103, 103, 103), dtype=np.int64)
    for shapes in product(range(5), repeat=3):
        chart = mod_matrix(hol_charts[shapes], prime)
        coordinate = mod_matrix(coordinates[shapes], prime)
        if chart.shape[1]:
            block = chart @ coordinate % prime
            block = block @ chart.T % prime
        else:
            block = np.zeros((chart.shape[0], chart.shape[0]), dtype=np.int64)
        dimensions = tuple(BRIDGE.HOL_MULTS[s] for s in shapes)
        put_block(hol_tensor, hol_ranges, shapes, dimensions, block)
    mixed_tensor = crossing_apply_mod(crossing_mod, hol_tensor, prime)

    maximum_residual = 0
    pivot_blocks = {} if face_pivot_rows is not None else None
    for shapes in product(range(6), repeat=3):
        dimensions = tuple(BRIDGE.MIXED_MULTS[s] for s in shapes)
        block = get_block(mixed_tensor, mixed_ranges, shapes, dimensions)
        kernel = mod_matrix(face_kernels[shapes], prime)
        if kernel.shape[0]:
            residual = kernel @ block % prime
            if np.any(residual):
                maximum_residual = max(
                    maximum_residual,
                    max(int(value) for value in residual.flat),
                )
        if face_pivot_rows is not None:
            pivots = face_pivot_rows[shapes]
            pivot_blocks[shapes] = block[np.ix_(pivots, pivots)].copy()
    assert maximum_residual == 0
    return pivot_blocks


def deterministic_primes():
    value = 1_000_003
    while True:
        value = int(sp.nextprime(value))
        # Keeping p near 10^6 makes every length-216 int64 dot product safe.
        yield value


def crt_update(current, new_residue, modulus, prime):
    """Merge one matrix of residues into ``current`` modulo ``modulus``."""
    if not current.size:
        return current
    current_mod = np.asarray(
        [int(value) % prime for value in current.flat], dtype=np.int64
    ).reshape(current.shape)
    inverse = pow(modulus % prime, -1, prime)
    delta = (new_residue - current_mod) % prime
    delta = delta * inverse % prime
    return current + modulus * delta.astype(object)


def signed_representatives(matrix, modulus, bound):
    half = modulus // 2
    output = np.empty(matrix.shape, dtype=object)
    maximum = 0
    for index, value in enumerate(matrix.flat):
        value = int(value)
        if value > half:
            value -= modulus
        maximum = max(maximum, abs(value))
        output.flat[index] = value
    assert maximum <= bound
    return output


def verify_coordinates(coordinates, verbose=True):
    """Verify full exact face support and return all exact mixed B blocks.

    ``coordinates`` maps the 125 holomorphic shape triples to exact
    symmetric K-coordinate matrices.  The return value maps all 216 mixed
    shape triples to exact symmetric coordinate matrices represented as
    nested :class:`fractions.Fraction` rows.

    The face-support conclusion is exact: every primitive integer residual
    vanishes modulo a product larger than twice its proved magnitude bound.
    The same CRT run reconstructs the 64,900 pivot-principal entries needed
    to recover the mixed coordinate blocks.  Positivity of those small
    blocks is deliberately checked by the independent cone verifier.
    """
    expected = set(product(range(5), repeat=3))
    if set(coordinates) != expected:
        raise ValueError("holomorphic coordinate block set is incomplete")
    common_denominator = coordinate_denominator(coordinates)
    if verbose:
        print("global coordinate denominator bits:",
              common_denominator.bit_length(), flush=True)
    crossing = exact_crossing_numerator()
    hol_charts, integer_coordinates, hol_bound = integer_hol_charts(
        coordinates, common_denominator
    )
    (face_kernels, maximum_l1, face_charts,
     face_pivots) = integer_face_kernels(with_charts=True)
    crossing_row_l1 = max(
        sum(abs(int(value)) for value in row) for row in crossing
    )
    mixed_bound = hol_bound * crossing_row_l1 ** 3
    residual_bound = maximum_l1 * mixed_bound
    if verbose:
        print("hol numerator bound bits:", hol_bound.bit_length(), flush=True)
        print("maximum primitive face L1 bits:", maximum_l1.bit_length(),
              flush=True)
        print("mixed entry bound bits:", mixed_bound.bit_length(), flush=True)
        print("integer residual bound bits:", residual_bound.bit_length(),
              flush=True)

    residues = {
        shapes: np.zeros((len(face_pivots[shapes]), len(face_pivots[shapes])),
                         dtype=object)
        for shapes in product(range(6), repeat=3)
    }
    modulus = 1
    hol_ranges = block_ranges(BRIDGE.HOL_MULTS)
    mixed_ranges = block_ranges(BRIDGE.MIXED_MULTS)
    checked = []
    for prime in deterministic_primes():
        pivot_blocks = replay_prime(
            prime, crossing, hol_charts, integer_coordinates, face_kernels,
            hol_ranges, mixed_ranges, face_pivots,
        )
        for shapes in product(range(6), repeat=3):
            residues[shapes] = crt_update(
                residues[shapes], pivot_blocks[shapes], modulus, prime
            )
        modulus *= prime
        checked.append(prime)
        if verbose:
            print("CRT prime", len(checked), prime,
                  "modulus bits", modulus.bit_length(), flush=True)
        if modulus > 2 * residual_bound:
            break
    assert modulus > 2 * residual_bound

    mixed_denominator = (
        common_denominator * HOL_SCALE ** 2 * CROSS_SCALE ** 3
    )
    exact_blocks = {}
    for count, shapes in enumerate(product(range(6), repeat=3), 1):
        signed = signed_representatives(
            residues[shapes], modulus, mixed_bound
        )
        face = sp.Matrix(face_charts[shapes].tolist())
        pivots = face_pivots[shapes]
        rank = len(pivots)
        if rank:
            principal = face[list(pivots), :]
            mixed_principal = sp.Matrix(signed.tolist()) / mixed_denominator
            coordinate = principal.inv() * mixed_principal * principal.inv().T
            coordinate = coordinate.applyfunc(sp.factor)
            assert coordinate == coordinate.T
            exact_blocks[shapes] = [
                [Fraction(int(sp.numer(coordinate[i, j])),
                          int(sp.denom(coordinate[i, j])))
                 for j in range(rank)]
                for i in range(rank)
            ]
        else:
            exact_blocks[shapes] = []
        if verbose and count % 24 == 0:
            print("recovered exact mixed blocks", count, "/216", flush=True)

    if verbose:
        print("exact full-face CRT certificate passed")
        print("checked primes:", len(checked))
        print("face rank:", EXPECTED_FACE_RANK,
              "literal membership equations:", EXPECTED_EQUATIONS)
    return exact_blocks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate", default="/tmp/dth_exact_obstruction_v2.json.gz"
    )
    parser.add_argument("--maximum-primes", type=int, default=1000)
    args = parser.parse_args()

    coordinates, _ = parse_certificate(args.certificate)
    verify_coordinates(coordinates)


if __name__ == "__main__":
    main()
