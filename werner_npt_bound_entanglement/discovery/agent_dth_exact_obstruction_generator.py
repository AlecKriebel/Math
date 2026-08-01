#!/usr/bin/env python3
"""Generate an exact rational constrained-DTH pseudomoment obstruction.

The numerical candidate is rounded in the 4139 exact holomorphic support
coordinates.  A literal exact 334 by 334 face-defect minor is then used to
correct 334 pivot coordinates over QQ.  All crossing arithmetic used to
form the minor and right-hand side is integral after the common scalings

    E_hol -> 360 E_hol,       C_cross -> 14400 C_cross.

This is certificate-generation code.  The resulting artifact must be
replayed by a smaller independent verifier before it is a theorem.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from functools import reduce
from itertools import product
import importlib.util
import json
import math
import multiprocessing as mp
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import numpy as np
import scipy.linalg as la
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VERIFY = ROOT / "verification"


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


KMOD = import_file("dth_exact_k_generator",
                   VERIFY / "agent_dth_exact_k_coordinates.py")
FMOD = import_file("dth_exact_face_generator",
                   VERIFY / "agent_dth_exact_face_coordinates.py")
BRIDGE = KMOD.BRIDGE
FACE = FMOD.FACE

HOL_SCALE = 360
CROSS_SCALE = 14_400


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


def exact_crossing_numerator():
    hol, mixed, _, _ = BRIDGE.exact_restriction_bridge()
    h = sp.polys.matrices.DomainMatrix.from_list_sympy(103, 103, hol)
    m = sp.polys.matrices.DomainMatrix.from_list_sympy(103, 103, mixed)
    inverse_numerator, denominator = h.inv_den()
    numerator = (m * inverse_numerator).to_Matrix()
    common = reduce(math.gcd, [abs(int(x)) for x in numerator if x]
                    + [int(denominator)])
    denominator = int(denominator) // common
    assert denominator == CROSS_SCALE
    out = np.asarray([
        [int(numerator[i, j]) // common for j in range(103)]
        for i in range(103)
    ], dtype=object)
    assert max(abs(int(x)) for x in out.flat) == 115_200
    return out


def integer_hol_ranges():
    result = {}
    for count, shapes in enumerate(product(range(5), repeat=3), 1):
        exact = KMOD.hol_k_coordinates(shapes)[2]
        result[shapes] = np.asarray([
            [int(HOL_SCALE * exact[i, j]) for j in range(exact.cols)]
            for i in range(exact.rows)
        ], dtype=object)
        if count % 25 == 0:
            print("integer hol ranges", count, "/125", flush=True)
    return result


def primitive_integer_left(face, pivots, q):
    principal = face[list(pivots), :]
    alpha = (principal.T).inv() * face[q, :].T
    entries = {int(q): sp.Integer(1)}
    for row, value in zip(pivots, alpha):
        entries[int(row)] = entries.get(int(row), sp.Integer(0)) - value
    denominator = 1
    for value in entries.values():
        denominator = sp.ilcm(denominator, int(sp.denom(value)))
    integer = {row: int(value * denominator)
               for row, value in entries.items() if value}
    common = reduce(math.gcd, [abs(value) for value in integer.values()])
    integer = {row: value // common for row, value in integer.items()}
    first = next(value for _, value in sorted(integer.items()) if value)
    if first < 0:
        integer = {row: -value for row, value in integer.items()}
    # Exact annihilation audit.
    for column in range(face.cols):
        assert sum(value * int(face[row, column])
                   for row, value in integer.items()) == 0
    return tuple(sorted(integer.items()))


def prepare_constraints(certificate):
    cache = {}
    constraints = []
    maximum_bits = 0
    for shapes_array, q, s in zip(
        certificate["row_shapes"], certificate["row_indices"],
        certificate["column_indices"]
    ):
        shapes = tuple(map(int, shapes_array))
        q, s = int(q), int(s)
        key = (shapes, q)
        if key not in cache:
            face, _ = FMOD.face_chart(shapes)
            tag = "".join(map(str, shapes))
            pivots = tuple(map(int, certificate["face_rows_" + tag]))
            cache[key] = primitive_integer_left(face, pivots, q)
        left = cache[key]
        maximum_bits = max(maximum_bits,
                           max(abs(v).bit_length() for _, v in left))
        constraints.append((shapes, left, s))
    print("primitive face rows:", len(cache),
          "maximum coefficient bits:", maximum_bits, flush=True)
    return constraints


G_CROSS = None
G_HOL_RANGES = None
G_HOL_BLOCK_RANGES = None
G_MIXED_BLOCK_RANGES = None
G_CONSTRAINT_GROUPS = None
G_CANDIDATE_INTEGERS = None


def matrix_to_tensor(matrix, dimensions):
    return matrix.reshape((*dimensions, *dimensions)).transpose(
        0, 3, 1, 4, 2, 5
    ).reshape(tuple(d * d for d in dimensions))


def tensor_to_matrix(tensor, dimensions):
    return tensor.reshape(
        dimensions[0], dimensions[0], dimensions[1], dimensions[1],
        dimensions[2], dimensions[2]
    ).transpose(0, 2, 4, 1, 3, 5).reshape(
        int(np.prod(dimensions)), int(np.prod(dimensions))
    )


def cross_integer_matrix(matrix, hol_shapes, mixed_shapes):
    hol_dimensions = tuple(BRIDGE.HOL_MULTS[s] for s in hol_shapes)
    tensor = matrix_to_tensor(matrix, hol_dimensions)
    maps = [
        G_CROSS[np.ix_(G_MIXED_BLOCK_RANGES[mu].reshape(-1),
                       G_HOL_BLOCK_RANGES[lam].reshape(-1))]
        for mu, lam in zip(mixed_shapes, hol_shapes)
    ]
    if any(not np.any(local) for local in maps):
        size = math.prod(BRIDGE.MIXED_MULTS[s] for s in mixed_shapes)
        return np.zeros((size, size), dtype=object)
    out = np.tensordot(maps[0], tensor, axes=(1, 0))
    out = np.tensordot(maps[1], out, axes=(1, 1)).transpose(1, 0, 2)
    out = np.tensordot(maps[2], out, axes=(1, 2)).transpose(1, 2, 0)
    dimensions = tuple(BRIDGE.MIXED_MULTS[s] for s in mixed_shapes)
    return tensor_to_matrix(out, dimensions)


def evaluate_constraints(matrix_by_shapes):
    values = [0] * sum(len(rows) for rows in G_CONSTRAINT_GROUPS.values())
    for shapes, rows in G_CONSTRAINT_GROUPS.items():
        matrix = matrix_by_shapes[shapes]
        for global_row, left, column in rows:
            values[global_row] = sum(
                coefficient * int(matrix[row, column])
                for row, coefficient in left
            )
    return values


def source_worker(task):
    column, shapes, first, second = task
    basis = G_HOL_RANGES[shapes]
    matrix = np.outer(basis[:, first], basis[:, second])
    if first != second:
        matrix += np.outer(basis[:, second], basis[:, first])
    crossed = {
        mixed_shapes: cross_integer_matrix(matrix, shapes, mixed_shapes)
        for mixed_shapes in G_CONSTRAINT_GROUPS
    }
    return column, evaluate_constraints(crossed)


def candidate_worker(shapes):
    basis = G_HOL_RANGES[shapes]
    coordinate = G_CANDIDATE_INTEGERS[shapes]
    matrix = basis @ coordinate @ basis.T
    crossed = {
        mixed_shapes: cross_integer_matrix(matrix, shapes, mixed_shapes)
        for mixed_shapes in G_CONSTRAINT_GROUPS
    }
    return evaluate_constraints(crossed)


def initialize_globals(crossing, ranges, constraints, candidate_integers):
    global G_CROSS, G_HOL_RANGES, G_HOL_BLOCK_RANGES
    global G_MIXED_BLOCK_RANGES, G_CONSTRAINT_GROUPS, G_CANDIDATE_INTEGERS
    G_CROSS = crossing
    G_HOL_RANGES = ranges
    G_HOL_BLOCK_RANGES = block_ranges(BRIDGE.HOL_MULTS)
    G_MIXED_BLOCK_RANGES = block_ranges(BRIDGE.MIXED_MULTS)
    groups = {}
    for index, (shapes, left, column) in enumerate(constraints):
        groups.setdefault(shapes, []).append((index, left, column))
    G_CONSTRAINT_GROUPS = groups
    G_CANDIDATE_INTEGERS = candidate_integers


def rounded_candidate(path, bits):
    data = np.load(path)
    denominator = 1 << bits
    matrices = {}
    coordinates = []
    for shapes in product(range(5), repeat=3):
        tag = "".join(map(str, shapes))
        numerical = data["A_" + tag]
        integer = np.asarray([
            [int(round(float(value) * denominator)) for value in row]
            for row in numerical
        ], dtype=object)
        assert np.array_equal(integer, integer.T)
        matrices[shapes] = integer
        k = integer.shape[0]
        coordinates.extend(int(integer[i, i]) for i in range(k))
        coordinates.extend(int(integer[i, j])
                           for i in range(k) for j in range(i + 1, k))
    assert len(coordinates) == 4139
    return denominator, matrices, coordinates


def rank_mod(matrix, prime):
    reduced = np.asarray([[int(x) % prime for x in row] for row in matrix],
                         dtype=np.int64)
    return FACE.rank_mod(reduced, prime)


def pari_solve(matrix, rhs, directory):
    matrix_path = directory / "minor.gpdat"
    rhs_path = directory / "rhs.gpdat"
    output_path = directory / "solution.txt"
    # GP's write() appends.  Certificate generation must be restart-safe.
    output_path.unlink(missing_ok=True)
    with matrix_path.open("w") as handle:
        handle.write("[")
        for i, row in enumerate(matrix):
            if i:
                handle.write(";")
            handle.write(",".join(map(str, row)))
        handle.write("]\n")
    with rhs_path.open("w") as handle:
        handle.write("[" + ",".join(map(str, rhs)) + "]~\n")
    program = directory / "solve.gp"
    program.write_text(
        f'M=read("{matrix_path}");\n'
        f'r=read("{rhs_path}");\n'
        'y=matsolve(M,-r);\n'
        f'for(i=1,#y,write("{output_path}",numerator(y[i])," ",'
        'denominator(y[i])));\nquit\n'
    )
    subprocess.run(
        ["/opt/homebrew/bin/gp", "-q", "-s", "1000000000", str(program)],
        check=True,
    )
    lines = output_path.read_text().splitlines()
    assert len(lines) == len(rhs)
    return [Fraction(*(map(int, line.split()))) for line in lines]


def write_certificate(path, denominator, matrices, pivot_global, correction):
    pivot_correction = {int(index): value
                        for index, value in zip(pivot_global, correction)}
    output = {"version": 1, "rounding_bits": denominator.bit_length() - 1,
              "blocks": {}}
    offset = 0
    for shapes in product(range(5), repeat=3):
        integer = matrices[shapes]
        k = integer.shape[0]
        pairs = [(i, i) for i in range(k)]
        pairs += [(i, j) for i in range(k) for j in range(i + 1, k)]
        entries = []
        for local, (i, j) in enumerate(pairs):
            value = Fraction(int(integer[i, j]), denominator)
            if offset + local in pivot_correction:
                value += pivot_correction[offset + local] / denominator
            entries.append([value.numerator, value.denominator])
        output["blocks"]["".join(map(str, shapes))] = {
            "dimension": k, "upper": entries,
        }
        offset += len(pairs)
    assert offset == 4139
    path.write_text(json.dumps(output, separators=(",", ":")))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--minor", default="/tmp/dth_direct_defect_minor334.npz")
    parser.add_argument("--candidate", default="/tmp/dth_theta018_exact_hol_charts.npz")
    parser.add_argument("--bits", type=int, default=100)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--work", default="/tmp/dth_exact_obstruction_work")
    parser.add_argument("--output", default="/tmp/dth_exact_obstruction.json")
    parser.add_argument("--reuse-linear-system", action="store_true")
    args = parser.parse_args()

    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    certificate = np.load(args.minor)
    start = time.time()
    crossing = exact_crossing_numerator()
    ranges = integer_hol_ranges()
    constraints = prepare_constraints(certificate)
    denominator, candidate_matrices, source_coordinates = rounded_candidate(
        args.candidate, args.bits
    )
    initialize_globals(crossing, ranges, constraints, candidate_matrices)
    print("exact setup seconds", time.time() - start, flush=True)

    labels = certificate["source_labels"]
    triples = list(product(range(5), repeat=3))
    context = mp.get_context("fork")
    if args.reuse_linear_system:
        text = (work / "minor.gpdat").read_text().strip()
        assert text[0] == "[" and text[-1] == "]"
        minor = [list(map(int, row.split(",")))
                 for row in text[1:-1].split(";")]
        text = (work / "rhs.gpdat").read_text().strip()
        assert text.startswith("[") and text.endswith("]~")
        rhs = list(map(int, text[1:-2].split(",")))
        assert len(minor) == len(rhs) == 334
        assert all(len(row) == 334 for row in minor)
        print("reused exact integer minor and RHS", flush=True)
    else:
        source_tasks = [
            (column, triples[int(block)], int(first), int(second))
            for column, (block, first, second) in enumerate(labels)
        ]
        minor = [[0] * 334 for _ in range(334)]
        start = time.time()
        with context.Pool(args.workers) as pool:
            for done, (column, values) in enumerate(
                pool.imap_unordered(source_worker, source_tasks), 1
            ):
                for row, value in enumerate(values):
                    minor[row][column] = value
                if done % 20 == 0:
                    print("exact minor columns", done, "/334",
                          f"sec {time.time()-start:.1f}", flush=True)
        rhs = [0] * 334
        active_blocks = [shapes for shapes in product(range(5), repeat=3)
                         if ranges[shapes].shape[1]]
        start = time.time()
        with context.Pool(args.workers) as pool:
            for done, values in enumerate(
                pool.imap_unordered(candidate_worker, active_blocks), 1
            ):
                rhs = [x + y for x, y in zip(rhs, values)]
                if done % 10 == 0:
                    print("exact RHS blocks", done, "/", len(active_blocks),
                          f"sec {time.time()-start:.1f}", flush=True)
    print("minor rank mod primes",
          rank_mod(minor, 1_000_003), rank_mod(minor, 1_000_033), flush=True)

    pivot_global = certificate["source_columns"].astype(int)
    # Direct consistency check: the pivot source labels are exactly the
    # corresponding global source-coordinate labels selected upstream.
    for global_index, (block, first, second) in zip(
        pivot_global, certificate["source_labels"]
    ):
        shapes = triples[int(block)]
        k = ranges[shapes].shape[1]
        pairs = [(i, i) for i in range(k)]
        pairs += [(i, j) for i in range(k) for j in range(i + 1, k)]
        # Recover the global offset deterministically.
        before = sum(
            ranges[old].shape[1] * (ranges[old].shape[1] + 1) // 2
            for old in triples[:int(block)]
        )
        assert int(global_index) == before + pairs.index((int(first), int(second)))

    print("PARI solve begins", flush=True)
    correction = pari_solve(minor, rhs, work)
    # Exact equation replay.
    for row in range(334):
        assert sum(Fraction(minor[row][column]) * correction[column]
                   for column in range(334)) == -rhs[row]
    corrected = list(map(Fraction, source_coordinates))
    for index, value in zip(pivot_global, correction):
        corrected[int(index)] += value
    maximum_correction = max(abs(float(value / denominator))
                             for value in correction)
    print("maximum A-coordinate correction", maximum_correction, flush=True)

    output = Path(args.output)
    write_certificate(output, denominator, candidate_matrices,
                      pivot_global, correction)
    print("wrote", output, "bytes", output.stat().st_size, flush=True)


if __name__ == "__main__":
    main()
