#!/usr/bin/env python3
"""Exact CRT replay for the final-slot DTH face.

The input is an exact rational density in the 125 holomorphic
Pluecker/Omega charts.  Partial transpose of the final ``z`` replica changes
the local module from ``V^tensor5`` to ``V^tensor4 tensor conjugate(V)``.
This verifier constructs the exact local crossing and proves that every one
of the resulting 216 blocks lies in the canonical face of reduced
multiplicity-rank sum 751

    K5 = (pair/Pluecker support) intersect ker(D5).

Every primitive integer left-kernel equation is checked modulo a product of
deterministic primes larger than twice an explicit integer residual bound.
The same CRT pass recovers all exact coordinate matrices on K5.  Positivity
of those matrices is deliberately left to an independent block verifier.
"""

from __future__ import annotations

from fractions import Fraction
from functools import reduce
from itertools import product
from math import gcd
from pathlib import Path
import argparse
import gzip
import hashlib
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


BASE = import_file("dth_gamma5_crt_base", HERE / "agent_dth_full_face_crt.py")
LAST = import_file("dth_gamma5_crt_bridge", HERE / "agent_dth_last_crossing_exact.py")
FACE5 = import_file(
    "dth_gamma5_crt_face", HERE / "agent_dth_exact_gamma5_face_coordinates.py"
)

EXPECTED_REDUCED_RANK = 751
EXPECTED_ACTIVE_BLOCKS = 188


def read_sparse_face_charts(path):
    """Read the deterministic exact sparse-chart export.

    The companion exporter derives every column directly in the physical
    word module.  Keeping this loader separate from the dense SymPy fallback
    makes repeated CRT passes cheap while retaining an exact integer chart.
    """
    path = Path(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with gzip.open(path, "rt", encoding="ascii") as handle:
        payload = json.load(handle)
    assert payload["format"] == "dth-gamma5-face-integer-charts-v1"
    assert tuple(payload["last_names"]) == tuple(LAST.LAST_NAMES)
    assert tuple(payload["last_multiplicities"]) == tuple(LAST.LAST_MULTS)
    assert int(payload["reduced_support_rank"]) == 772
    assert int(payload["reduced_delta_rank"]) == 21
    assert int(payload["reduced_face_rank"]) == EXPECTED_REDUCED_RANK
    assert int(payload["active_blocks"]) == EXPECTED_ACTIVE_BLOCKS
    charts = {}
    pivots = {}
    total_rank = active = 0
    expected_tags = {
        ",".join(map(str, shapes)) for shapes in product(range(6), repeat=3)
    }
    assert set(payload["blocks"]) == expected_tags
    for shapes in product(range(6), repeat=3):
        block = payload["blocks"][",".join(map(str, shapes))]
        rows = math.prod(LAST.LAST_MULTS[shape] for shape in shapes)
        rank = int(block["face_rank"])
        assert int(block["raw_rank"]) == rows
        assert int(block["support_rank"]) - int(block["delta_rank"]) == rank
        matrix = block["matrix"]
        assert len(matrix) == rows
        assert all(len(row) == rank for row in matrix)
        assert all(isinstance(value, int) for row in matrix for value in row)
        selected = tuple(map(int, block["pivot_rows"]))
        assert len(selected) == rank and len(set(selected)) == rank
        assert all(0 <= row < rows for row in selected)
        chart = sp.Matrix(matrix)
        if rank:
            # This is also replayed when the primitive left kernel is built,
            # but the explicit check gives a local artifact-integrity error.
            assert chart[list(selected), :].det() != 0
        charts[shapes] = chart
        pivots[shapes] = selected
        total_rank += rank
        active += int(rank > 0)
    assert total_rank == EXPECTED_REDUCED_RANK
    assert active == EXPECTED_ACTIVE_BLOCKS
    return charts, pivots, digest


def write_exact_blocks(path, blocks, source_certificate):
    payload = {
        "version": 1,
        "source": str(source_certificate),
        "reduced_multiplicity_rank": EXPECTED_REDUCED_RANK,
        "blocks": {},
    }
    for shapes in product(range(6), repeat=3):
        matrix = blocks[shapes]
        dimension = len(matrix)
        upper = []
        for row in range(dimension):
            value = Fraction(matrix[row][row])
            upper.append([value.numerator, value.denominator])
        for row in range(dimension):
            for column in range(row + 1, dimension):
                value = Fraction(matrix[row][column])
                upper.append([value.numerator, value.denominator])
        payload["blocks"]["".join(map(str, shapes))] = {
            "dimension": dimension,
            "upper": upper,
        }
    Path(path).write_text(json.dumps(payload, separators=(",", ":")),
                          encoding="ascii")


def exact_crossing_numerator():
    holomorphic, final, _, _ = LAST.exact_last_restriction_bridge()
    hol_domain = sp.polys.matrices.DomainMatrix.from_list_sympy(
        103, 103, holomorphic
    )
    final_domain = sp.polys.matrices.DomainMatrix.from_list_sympy(
        103, 103, final
    )
    inverse_numerator, denominator = hol_domain.inv_den()
    numerator = (final_domain * inverse_numerator).to_Matrix()
    common = reduce(
        gcd,
        [abs(int(value)) for value in numerator if value] + [int(denominator)],
    )
    denominator = int(denominator) // common
    integer = np.asarray(
        [
            [int(numerator[row, column]) // common for column in range(103)]
            for row in range(103)
        ],
        dtype=object,
    )

    hol_transpose = BASE.transpose_permutation(
        BASE.block_ranges(LAST.bridge.HOL_MULTS)
    )
    final_transpose = BASE.transpose_permutation(
        BASE.block_ranges(LAST.LAST_MULTS)
    )
    assert np.array_equal(
        integer[:, hol_transpose], integer[final_transpose, :]
    )
    return integer, denominator


def integer_face_kernels(with_charts=False, chart_path=None):
    archived_charts = archived_pivots = None
    chart_digest = None
    if chart_path is not None:
        archived_charts, archived_pivots, chart_digest = (
            read_sparse_face_charts(chart_path)
        )
        print("loaded exact sparse Gamma5 charts", chart_path,
              "sha256", chart_digest, flush=True)
    kernels = {}
    charts = {}
    pivot_rows = {}
    total_rank = 0
    active = 0
    total_equations = 0
    maximum_l1 = 0
    for count, shapes in enumerate(product(range(6), repeat=3), 1):
        if archived_charts is None:
            face, pivots = FACE5.gamma5_face_chart(shapes)
        else:
            face = archived_charts[shapes]
            pivots = archived_pivots[shapes]
        assert all(value == int(value) for value in face)
        kernel = BASE.primitive_left_kernel(face, pivots)
        kernels[shapes] = kernel
        if with_charts:
            charts[shapes] = np.asarray(face.tolist(), dtype=object)
            pivot_rows[shapes] = tuple(map(int, pivots))
        total_rank += face.cols
        active += int(face.cols > 0)
        total_equations += kernel.shape[0] * face.rows
        if kernel.shape[0]:
            maximum_l1 = max(
                maximum_l1,
                max(sum(abs(int(value)) for value in row) for row in kernel),
            )
        if count % 24 == 0:
            print("integer Gamma5 face kernels", count, "/216", flush=True)
    assert total_rank == EXPECTED_REDUCED_RANK
    assert active == EXPECTED_ACTIVE_BLOCKS
    if with_charts:
        return (
            kernels,
            maximum_l1,
            charts,
            pivot_rows,
            total_equations,
        )
    return kernels, maximum_l1, total_equations


def replay_prime(
    prime,
    crossing,
    hol_charts,
    coordinates,
    face_kernels,
    hol_ranges,
    final_ranges,
    face_pivot_rows=None,
):
    crossing_mod = BASE.mod_matrix(crossing, prime)
    hol_tensor = np.zeros((103, 103, 103), dtype=np.int64)
    for shapes in product(range(5), repeat=3):
        chart = BASE.mod_matrix(hol_charts[shapes], prime)
        coordinate = BASE.mod_matrix(coordinates[shapes], prime)
        if chart.shape[1]:
            block = chart @ coordinate % prime
            block = block @ chart.T % prime
        else:
            block = np.zeros((chart.shape[0], chart.shape[0]), dtype=np.int64)
        dimensions = tuple(LAST.bridge.HOL_MULTS[shape] for shape in shapes)
        BASE.put_block(hol_tensor, hol_ranges, shapes, dimensions, block)
    final_tensor = BASE.crossing_apply_mod(crossing_mod, hol_tensor, prime)

    pivot_blocks = {} if face_pivot_rows is not None else None
    for shapes in product(range(6), repeat=3):
        dimensions = tuple(LAST.LAST_MULTS[shape] for shape in shapes)
        block = BASE.get_block(final_tensor, final_ranges, shapes, dimensions)
        kernel = BASE.mod_matrix(face_kernels[shapes], prime)
        if kernel.shape[0]:
            residual = kernel @ block % prime
            if np.any(residual):
                location = tuple(map(int, np.argwhere(residual)[0]))
                raise AssertionError(
                    f"nonzero Gamma5 face residual modulo {prime} in "
                    f"block {shapes} at {location}: "
                    f"{int(residual[location])}"
                )
        if face_pivot_rows is not None:
            pivots = face_pivot_rows[shapes]
            pivot_blocks[shapes] = block[np.ix_(pivots, pivots)].copy()
    return pivot_blocks


def verify_coordinates(coordinates, verbose=True, chart_path=None):
    expected = set(product(range(5), repeat=3))
    if set(coordinates) != expected:
        raise ValueError("holomorphic coordinate block set is incomplete")
    common_denominator = BASE.coordinate_denominator(coordinates)
    crossing, crossing_denominator = exact_crossing_numerator()
    hol_charts, integer_coordinates, hol_bound = BASE.integer_hol_charts(
        coordinates, common_denominator
    )
    (
        face_kernels,
        maximum_l1,
        face_charts,
        face_pivots,
        total_equations,
    ) = integer_face_kernels(with_charts=True, chart_path=chart_path)
    crossing_row_l1 = max(
        sum(abs(int(value)) for value in row) for row in crossing
    )
    final_bound = hol_bound * crossing_row_l1**3
    residual_bound = maximum_l1 * final_bound
    if verbose:
        print("Gamma5 coordinate denominator bits:",
              common_denominator.bit_length(), flush=True)
        print("Gamma5 crossing denominator:", crossing_denominator, flush=True)
        print("Gamma5 crossing row-L1 bits:", crossing_row_l1.bit_length(),
              flush=True)
        print("Gamma5 entry/residual bound bits:",
              final_bound.bit_length(), residual_bound.bit_length(),
              flush=True)
        print("Gamma5 literal face equations:", total_equations, flush=True)

    residues = {
        shapes: np.zeros(
            (len(face_pivots[shapes]), len(face_pivots[shapes])), dtype=object
        )
        for shapes in product(range(6), repeat=3)
    }
    modulus = 1
    hol_ranges = BASE.block_ranges(LAST.bridge.HOL_MULTS)
    final_ranges = BASE.block_ranges(LAST.LAST_MULTS)
    checked = []
    for prime in BASE.deterministic_primes():
        pivot_blocks = replay_prime(
            prime,
            crossing,
            hol_charts,
            integer_coordinates,
            face_kernels,
            hol_ranges,
            final_ranges,
            face_pivots,
        )
        for shapes in product(range(6), repeat=3):
            residues[shapes] = BASE.crt_update(
                residues[shapes], pivot_blocks[shapes], modulus, prime
            )
        modulus *= prime
        checked.append(prime)
        if verbose:
            print("Gamma5 CRT prime", len(checked), prime,
                  "modulus bits", modulus.bit_length(), flush=True)
        if modulus > 2 * residual_bound:
            break
    assert modulus > 2 * residual_bound

    final_denominator = (
        common_denominator * BASE.HOL_SCALE**2 * crossing_denominator**3
    )
    exact_blocks = {}
    for count, shapes in enumerate(product(range(6), repeat=3), 1):
        signed = BASE.signed_representatives(
            residues[shapes], modulus, final_bound
        )
        face = sp.Matrix(face_charts[shapes].tolist())
        pivots = face_pivots[shapes]
        rank = len(pivots)
        if rank:
            principal = face[list(pivots), :]
            final_principal = sp.Matrix(signed.tolist()) / final_denominator
            coordinate = (
                principal.inv() * final_principal * principal.inv().T
            ).applyfunc(sp.factor)
            assert coordinate == coordinate.T
            exact_blocks[shapes] = [
                [
                    Fraction(
                        int(sp.numer(coordinate[row, column])),
                        int(sp.denom(coordinate[row, column])),
                    )
                    for column in range(rank)
                ]
                for row in range(rank)
            ]
        else:
            exact_blocks[shapes] = []
        if verbose and count % 24 == 0:
            print("recovered exact Gamma5 blocks", count, "/216", flush=True)
    if verbose:
        print("exact Gamma5 face CRT certificate passed")
        print("checked primes:", len(checked))
        print("Gamma5 reduced multiplicity-rank sum/active:",
              EXPECTED_REDUCED_RANK,
              EXPECTED_ACTIVE_BLOCKS)
    return exact_blocks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", required=True)
    parser.add_argument("--face-charts")
    parser.add_argument("--output")
    args = parser.parse_args()
    coordinates, _ = BASE.parse_certificate(args.certificate)
    exact = verify_coordinates(coordinates, chart_path=args.face_charts)
    if args.output:
        write_exact_blocks(args.output, exact, args.certificate)
        print("wrote exact Gamma5 coordinates", args.output,
              "bytes", Path(args.output).stat().st_size)


if __name__ == "__main__":
    main()
