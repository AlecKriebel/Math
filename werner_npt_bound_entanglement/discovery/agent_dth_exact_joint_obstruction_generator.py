#!/usr/bin/env python3
"""Generate one exact rational obstruction satisfying both DTH PPT faces.

This extends the earlier 334-equation Gamma1 correction.  A discovery NPZ
selects a full-row-rank set of homogeneous face equations from the Gamma1
and final-slot (Gamma5) partial transposes, together with the same number of
holomorphic source coordinates.  The selected square minor and the rounded
candidate defect are then constructed from exact integer crossings and the
correction is solved over QQ by PARI/GP.

This is certificate-generation code.  Independent CRT membership and exact
positive-definiteness verifiers remain mandatory for the output.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import importlib.util
import math
import multiprocessing as mp
from pathlib import Path
import subprocess
import time

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VERIFY = ROOT / "verification"


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


OLD = import_file(
    "dth_joint_old_generator", HERE / "agent_dth_exact_obstruction_generator.py"
)
G5 = import_file(
    "dth_joint_gamma5_crt", VERIFY / "agent_dth_gamma5_face_crt.py"
)


HOL_SCALE = OLD.HOL_SCALE
KMOD = OLD.KMOD
FMOD = OLD.FMOD
BRIDGE1 = OLD.BRIDGE
LAST = G5.LAST


def prepare_constraints(selection, gamma1_certificate, gamma5_charts,
                        gamma5_pivots):
    cuts = np.asarray(selection["cut"], dtype=int)
    shapes_array = np.asarray(selection["row_shapes"], dtype=int)
    rows = np.asarray(selection["row_indices"], dtype=int)
    columns = np.asarray(selection["column_indices"], dtype=int)
    assert cuts.shape == rows.shape == columns.shape
    assert shapes_array.shape == (len(cuts), 3)
    cache = {}
    constraints = []
    maximum_bits = 0
    for cut, raw_shapes, q, column in zip(
        cuts, shapes_array, rows, columns
    ):
        cut = int(cut)
        shapes = tuple(map(int, raw_shapes))
        q = int(q)
        key = (cut, shapes, q)
        if key not in cache:
            if cut == 0:
                face, _ = FMOD.face_chart(shapes)
                tag = "".join(map(str, shapes))
                pivots = tuple(map(
                    int, gamma1_certificate["face_rows_" + tag]
                ))
            elif cut == 1:
                face = gamma5_charts[shapes]
                tag = "".join(map(str, shapes))
                selection_key = "g5_face_rows_" + tag
                if selection_key in selection.files:
                    # Replay the same interpolation functional chosen by the
                    # numerical rank-revealing selector.  Exact
                    # nonsingularity is checked inside primitive_integer_left.
                    pivots = tuple(map(int, selection[selection_key]))
                else:
                    pivots = gamma5_pivots[shapes]
            else:
                raise ValueError(f"unknown cut {cut}")
            if q in set(pivots):
                raise ValueError(
                    f"selected row {q} is a pivot in cut/block {cut}/{shapes}"
                )
            cache[key] = OLD.primitive_integer_left(face, pivots, q)
        left = cache[key]
        maximum_bits = max(
            maximum_bits,
            max(abs(value).bit_length() for _, value in left),
        )
        constraints.append((cut, shapes, left, int(column)))
    print("joint primitive face rows:", len(cache),
          "equations:", len(constraints),
          "maximum coefficient bits:", maximum_bits, flush=True)
    return constraints


G_CROSSINGS = None
G_TARGET_MULTS = None
G_HOL_RANGES = None
G_HOL_BLOCK_RANGES = None
G_TARGET_BLOCK_RANGES = None
G_CONSTRAINT_GROUPS = None
G_CANDIDATE_INTEGERS = None
G_CONSTRAINT_COUNT = None


def cross_integer_matrix(matrix, hol_shapes, target_shapes, cut):
    hol_dimensions = tuple(BRIDGE1.HOL_MULTS[shape] for shape in hol_shapes)
    tensor = OLD.matrix_to_tensor(matrix, hol_dimensions)
    crossing = G_CROSSINGS[cut]
    target_ranges = G_TARGET_BLOCK_RANGES[cut]
    maps = [
        crossing[np.ix_(target_ranges[target].reshape(-1),
                        G_HOL_BLOCK_RANGES[source].reshape(-1))]
        for target, source in zip(target_shapes, hol_shapes)
    ]
    if any(not np.any(local) for local in maps):
        size = math.prod(G_TARGET_MULTS[cut][shape]
                         for shape in target_shapes)
        return np.zeros((size, size), dtype=object)
    output = np.tensordot(maps[0], tensor, axes=(1, 0))
    output = np.tensordot(maps[1], output, axes=(1, 1)).transpose(1, 0, 2)
    output = np.tensordot(maps[2], output, axes=(1, 2)).transpose(1, 2, 0)
    target_dimensions = tuple(
        G_TARGET_MULTS[cut][shape] for shape in target_shapes
    )
    return OLD.tensor_to_matrix(output, target_dimensions)


def evaluate_constraints(crossed_by_cut_shape, cuts=(0, 1)):
    values = [0] * G_CONSTRAINT_COUNT
    for cut in cuts:
        groups = G_CONSTRAINT_GROUPS[cut]
        for shapes, rows in groups.items():
            matrix = crossed_by_cut_shape[(cut, shapes)]
            for global_row, left, column in rows:
                values[global_row] = sum(
                    coefficient * int(matrix[row, column])
                    for row, coefficient in left
                )
    return values


def source_worker(task):
    column, shapes, first, second, cuts = task
    basis = G_HOL_RANGES[shapes]
    matrix = np.outer(basis[:, first], basis[:, second])
    if first != second:
        matrix += np.outer(basis[:, second], basis[:, first])
    crossed = {
        (cut, target_shapes): cross_integer_matrix(
            matrix, shapes, target_shapes, cut
        )
        for cut in cuts
        for groups in (G_CONSTRAINT_GROUPS[cut],)
        for target_shapes in groups
    }
    return column, evaluate_constraints(crossed, cuts)


def candidate_worker(shapes):
    basis = G_HOL_RANGES[shapes]
    coordinate = G_CANDIDATE_INTEGERS[shapes]
    matrix = basis @ coordinate @ basis.T
    crossed = {
        (cut, target_shapes): cross_integer_matrix(
            matrix, shapes, target_shapes, cut
        )
        for cut, groups in G_CONSTRAINT_GROUPS.items()
        for target_shapes in groups
    }
    return evaluate_constraints(crossed)


def initialize_globals(crossings, ranges, constraints, candidate_integers):
    global G_CROSSINGS, G_TARGET_MULTS, G_HOL_RANGES
    global G_HOL_BLOCK_RANGES, G_TARGET_BLOCK_RANGES
    global G_CONSTRAINT_GROUPS, G_CANDIDATE_INTEGERS, G_CONSTRAINT_COUNT
    G_CROSSINGS = crossings
    G_TARGET_MULTS = {
        0: tuple(BRIDGE1.MIXED_MULTS),
        1: tuple(LAST.LAST_MULTS),
    }
    G_HOL_RANGES = ranges
    G_HOL_BLOCK_RANGES = OLD.block_ranges(BRIDGE1.HOL_MULTS)
    G_TARGET_BLOCK_RANGES = {
        0: OLD.block_ranges(BRIDGE1.MIXED_MULTS),
        1: OLD.block_ranges(LAST.LAST_MULTS),
    }
    groups = {0: {}, 1: {}}
    for index, (cut, shapes, left, column) in enumerate(constraints):
        groups[cut].setdefault(shapes, []).append(
            (index, left, column)
        )
    G_CONSTRAINT_GROUPS = groups
    G_CANDIDATE_INTEGERS = candidate_integers
    G_CONSTRAINT_COUNT = len(constraints)


def assert_source_labels(selection, ranges):
    labels = np.asarray(selection["source_labels"], dtype=int)
    global_columns = np.asarray(selection["source_columns"], dtype=int)
    assert labels.shape == (len(global_columns), 3)
    triples = list(product(range(5), repeat=3))
    for global_index, (block, first, second) in zip(global_columns, labels):
        block = int(block)
        shapes = triples[block]
        rank = ranges[shapes].shape[1]
        pairs = [(i, i) for i in range(rank)]
        pairs += [(i, j) for i in range(rank) for j in range(i + 1, rank)]
        before = sum(
            ranges[old].shape[1] * (ranges[old].shape[1] + 1) // 2
            for old in triples[:block]
        )
        assert int(global_index) == before + pairs.index(
            (int(first), int(second))
        )


def pari_schur_solve(matrix, rhs, split, directory):
    """Solve the joint system by eliminating the certified Gamma1 block."""
    size = len(rhs)
    assert 0 < split < size
    matrix_path = directory / "minor.gpdat"
    rhs_path = directory / "rhs.gpdat"
    output_path = directory / "solution.txt"
    output_path.unlink(missing_ok=True)
    with matrix_path.open("w") as handle:
        handle.write("[")
        for row, values in enumerate(matrix):
            if row:
                handle.write(";")
            handle.write(",".join(map(str, values)))
        handle.write("]\n")
    with rhs_path.open("w") as handle:
        handle.write("[" + ",".join(map(str, rhs)) + "]~\n")
    program = directory / "solve_schur.gp"
    program.write_text(
        f'M=read("{matrix_path}");\n'
        f'r=read("{rhs_path}");\n'
        f's={split}; n={size};\n'
        'A=M[1..s,1..s]; C=M[1..s,s+1..n];\n'
        'B=M[s+1..n,1..s]; D=M[s+1..n,s+1..n];\n'
        'r1=r[1..s]; r5=r[s+1..n];\n'
        'x0=matsolve(A,-r1); T=matsolve(A,C);\n'
        'S=D-B*T; rr=r5+B*x0;\n'
        'y=matsolve(S,-rr); x=x0-T*y; sol=concat(x~,y~)~;\n'
        f'for(i=1,#sol,write("{output_path}",numerator(sol[i])," ",'
        'denominator(sol[i])));\nquit\n'
    )
    subprocess.run(
        ["/opt/homebrew/bin/gp", "-q", "-s", "2000000000", str(program)],
        check=True,
    )
    lines = output_path.read_text().splitlines()
    assert len(lines) == size
    return [Fraction(*(map(int, line.split()))) for line in lines]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection", required=True)
    parser.add_argument(
        "--gamma1-minor", default="/tmp/dth_direct_defect_minor334.npz"
    )
    parser.add_argument(
        "--gamma1-work", default="/tmp/dth_exact_obstruction_work",
        help="directory containing the already certified 334-square minor",
    )
    parser.add_argument("--gamma5-charts", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--bits", type=int, default=100)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--work", default="/tmp/dth_exact_joint_work")
    parser.add_argument("--output", required=True)
    parser.add_argument("--reuse-minor", action="store_true")
    parser.add_argument(
        "--schur-split", type=int, default=334,
        help="leading Gamma1 block size used for exact block elimination",
    )
    args = parser.parse_args()

    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    selection = np.load(args.selection)
    gamma1_certificate = np.load(args.gamma1_minor)
    start = time.time()
    gamma5_charts, gamma5_pivots, chart_digest = (
        G5.read_sparse_face_charts(args.gamma5_charts)
    )
    print("Gamma5 chart sha256:", chart_digest, flush=True)
    constraints = prepare_constraints(
        selection, gamma1_certificate, gamma5_charts, gamma5_pivots
    )
    rank = len(constraints)
    source_columns = np.asarray(selection["source_columns"], dtype=int)
    source_labels = np.asarray(selection["source_labels"], dtype=int)
    assert len(source_columns) == len(source_labels) == rank
    crossings = {
        0: OLD.exact_crossing_numerator(),
        1: G5.exact_crossing_numerator()[0],
    }
    ranges = OLD.integer_hol_ranges()
    denominator, candidate_matrices, source_coordinates = OLD.rounded_candidate(
        args.candidate, args.bits
    )
    initialize_globals(crossings, ranges, constraints, candidate_matrices)
    assert_source_labels(selection, ranges)
    print("exact joint setup seconds", time.time() - start, flush=True)

    context = mp.get_context("fork")
    minor_path = work / "minor.gpdat"
    if args.reuse_minor:
        text = minor_path.read_text().strip()
        assert text[0] == "[" and text[-1] == "]"
        minor = [list(map(int, row.split(",")))
                 for row in text[1:-1].split(";")]
        assert len(minor) == rank
        assert all(len(row) == rank for row in minor)
        print("reused exact joint minor", flush=True)
    else:
        triples = list(product(range(5), repeat=3))
        split = args.schur_split
        old_columns = np.asarray(gamma1_certificate["source_columns"],
                                 dtype=int)
        old_labels = np.asarray(gamma1_certificate["source_labels"],
                                dtype=int)
        assert split == len(old_columns) == len(old_labels)
        assert np.array_equal(source_columns[:split], old_columns)
        assert np.array_equal(source_labels[:split], old_labels)
        tasks = [
            (column, triples[int(block)], int(first), int(second),
             (1,) if column < split else (0, 1))
            for column, (block, first, second) in enumerate(source_labels)
        ]
        minor = [[0] * rank for _ in range(rank)]
        old_text = (Path(args.gamma1_work) / "minor.gpdat").read_text().strip()
        assert old_text[0] == "[" and old_text[-1] == "]"
        old_minor = [list(map(int, row.split(",")))
                     for row in old_text[1:-1].split(";")]
        assert len(old_minor) == split
        assert all(len(row) == split for row in old_minor)
        for row in range(split):
            minor[row][:split] = old_minor[row]
        started = time.time()
        with context.Pool(args.workers) as pool:
            for done, (column, values) in enumerate(
                pool.imap_unordered(source_worker, tasks), 1
            ):
                for row, value in enumerate(values):
                    if column >= split or row >= split:
                        minor[row][column] = value
                if done % 20 == 0:
                    print("exact joint minor columns", done, "/", rank,
                          f"sec {time.time()-started:.1f}", flush=True)

    rhs = [0] * rank
    active_blocks = [
        shapes for shapes in product(range(5), repeat=3)
        if ranges[shapes].shape[1]
    ]
    started = time.time()
    with context.Pool(args.workers) as pool:
        for done, values in enumerate(
            pool.imap_unordered(candidate_worker, active_blocks), 1
        ):
            rhs = [left + right for left, right in zip(rhs, values)]
            if done % 10 == 0:
                print("exact joint RHS blocks", done, "/", len(active_blocks),
                      f"sec {time.time()-started:.1f}", flush=True)

    print("joint minor rank mod primes",
          OLD.rank_mod(minor, 1_000_003),
          OLD.rank_mod(minor, 1_000_033), flush=True)
    cuts = np.asarray(selection["cut"], dtype=int)
    assert np.all(cuts[:args.schur_split] == 0)
    assert np.all(cuts[args.schur_split:] == 1)
    assert len(set(map(int, source_columns))) == len(source_columns)
    print("PARI joint Schur solve begins; split", args.schur_split,
          "incremental Gamma5 rank", rank - args.schur_split, flush=True)
    correction = pari_schur_solve(
        minor, rhs, args.schur_split, work
    )
    for row in range(rank):
        assert sum(Fraction(minor[row][column]) * correction[column]
                   for column in range(rank)) == -rhs[row]
    maximum_correction = max(
        abs(float(value / denominator)) for value in correction
    )
    print("maximum joint A-coordinate correction", maximum_correction,
          flush=True)
    output = Path(args.output)
    OLD.write_certificate(
        output, denominator, candidate_matrices, source_columns, correction
    )
    print("wrote", output, "bytes", output.stat().st_size, flush=True)


if __name__ == "__main__":
    main()
