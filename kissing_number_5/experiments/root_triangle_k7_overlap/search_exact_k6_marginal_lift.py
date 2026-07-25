#!/usr/bin/env python3
"""Search for a quarter-grid K7 lift of the repaired 73-atom K6 marginal.

This is a discovery program.  It enumerates every rank-five quarter-grid K7
atom having a face isomorphic to one of the 73 target K6 atoms, then retains
exactly those atoms whose seven faces all belong to the target support.  A
floating linear program tests whether their deletion marginal equals the
specified rational K6 distribution.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import sys
import time

import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import csc_matrix


ROOT = Path(__file__).resolve().parents[2]
TARGET = (
    ROOT
    / "experiments"
    / "global_flag_reoptimization"
    / "centered_degree2_repair_certificate.json"
)
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
TARGET_SHA256 = (
    "7b8dd73bfdaced21fe6a6f6acd74231a976b7359bce600cf45c0d1c44db895d6"
)
SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)

VALUES = (-4, -3, -2, -1, 0, 1, 2)
VALUE_INDEX = {value: index for index, value in enumerate(VALUES)}
PAIRS6 = tuple(itertools.combinations(range(6), 2))
PAIRS7 = tuple(itertools.combinations(range(7), 2))
PAIR_INDEX6 = {pair: index for index, pair in enumerate(PAIRS6)}
PAIR_INDEX7 = {pair: index for index, pair in enumerate(PAIRS7)}
PERMUTATIONS = {
    size: tuple(itertools.permutations(range(size))) for size in range(1, 6)
}
K6_RELABELINGS = tuple(
    tuple(
        PAIR_INDEX6[tuple(sorted((permutation[first], permutation[second])))]
        for first, second in PAIRS6
    )
    for permutation in itertools.permutations(range(6))
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def determinant(matrix):
    size = len(matrix)
    total = 0
    for permutation in PERMUTATIONS[size]:
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        product = 1
        for i in range(size):
            product *= matrix[i][permutation[i]]
        total += (-1 if inversions % 2 else 1) * product
    return total


def adjugate(matrix):
    size = len(matrix)
    answer = [[0] * size for _ in range(size)]
    for row in range(size):
        for column in range(size):
            minor = [
                [
                    matrix[i][j]
                    for j in range(size)
                    if j != row
                ]
                for i in range(size)
                if i != column
            ]
            answer[row][column] = (
                (-1 if (row + column) % 2 else 1) * determinant(minor)
            )
    return answer


def scaled_gram6(edges):
    matrix = [[4 if i == j else 0 for j in range(6)] for i in range(6)]
    for (i, j), color in zip(PAIRS6, edges):
        matrix[i][j] = VALUES[color]
        matrix[j][i] = VALUES[color]
    return matrix


def canonical_k6(edges):
    return min(
        tuple(edges[index] for index in relabeling)
        for relabeling in K6_RELABELINGS
    )


def extract_face(edges7, omitted):
    vertices = tuple(vertex for vertex in range(7) if vertex != omitted)
    return tuple(
        edges7[PAIR_INDEX7[(vertices[first], vertices[second])]]
        for first, second in PAIRS6
    )


def triangle_signature(edges6, triple_index):
    result = []
    for i, j, k in itertools.combinations(range(6), 3):
        colors = tuple(
            sorted(
                (
                    edges6[PAIR_INDEX6[(i, j)]],
                    edges6[PAIR_INDEX6[(i, k)]],
                    edges6[PAIR_INDEX6[(j, k)]],
                )
            )
        )
        result.append(triple_index[colors])
    return tuple(sorted(result))


def extension_candidates(base_edges):
    gram = scaled_gram6(base_edges)
    choice = None
    for omitted in range(6):
        indices = [index for index in range(6) if index != omitted]
        base = [[gram[i][j] for j in indices] for i in indices]
        base_determinant = determinant(base)
        if base_determinant > 0:
            choice = omitted, indices, base, base_determinant
            break
    if choice is None:
        raise RuntimeError("target K6 atom has no positive 5x5 block")
    omitted, indices, base, base_determinant = choice
    adj = adjugate(base)
    omitted_correlations = [gram[index][omitted] for index in indices]

    for color_vector in itertools.product(range(7), repeat=5):
        values = [VALUES[color] for color in color_vector]
        squared_norm_numerator = sum(
            values[i] * adj[i][j] * values[j]
            for i in range(5)
            for j in range(5)
        )
        if squared_norm_numerator != 4 * base_determinant:
            continue
        omitted_numerator = sum(
            omitted_correlations[i] * adj[i][j] * values[j]
            for i in range(5)
            for j in range(5)
        )
        if omitted_numerator % base_determinant:
            continue
        omitted_value = omitted_numerator // base_determinant
        if omitted_value not in VALUE_INDEX:
            continue

        new_colors = [None] * 6
        for index, color in zip(indices, color_vector):
            new_colors[index] = color
        new_colors[omitted] = VALUE_INDEX[omitted_value]
        edges = [0] * 21
        for pair, color in zip(PAIRS6, base_edges):
            edges[PAIR_INDEX7[pair]] = color
        for index, color in enumerate(new_colors):
            edges[PAIR_INDEX7[(index, 6)]] = color
        yield tuple(edges)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if sha256(TARGET) != TARGET_SHA256:
        raise RuntimeError("target certificate hash mismatch")
    if sha256(SOURCE) != SOURCE_SHA256:
        raise RuntimeError("triangle source hash mismatch")
    target = json.loads(TARGET.read_text())
    source = json.loads(SOURCE.read_text())
    triple_index = {
        tuple(triple): index
        for index, triple in enumerate(source["triple_orbits"])
    }
    target_edges = tuple(
        tuple(
            atom[
                "edge_color_indices_01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
            ]
        )
        for atom in target["atoms"]
    )
    target_weights = tuple(Q(atom["weight"]) for atom in target["atoms"])
    target_canonical = tuple(canonical_k6(edges) for edges in target_edges)
    if len(set(target_canonical)) != len(target_canonical):
        raise RuntimeError("target contains duplicate K6 isomorphism types")
    canonical_index = {
        canonical: index for index, canonical in enumerate(target_canonical)
    }
    target_signatures = tuple(
        triangle_signature(edges, triple_index) for edges in target_edges
    )
    signature_candidates = {}
    for index, signature in enumerate(target_signatures):
        signature_candidates.setdefault(signature, []).append(index)

    started = time.time()
    raw_extensions = 0
    signature_survivors = 0
    accepted_by_edges = {}
    for base_index, base_edges in enumerate(target_edges):
        base_extensions = 0
        base_accepted = 0
        for edges7 in extension_candidates(base_edges):
            raw_extensions += 1
            base_extensions += 1
            face_edges = []
            possible = True
            for omitted in range(7):
                face = extract_face(edges7, omitted)
                signature = triangle_signature(face, triple_index)
                if signature not in signature_candidates:
                    possible = False
                    break
                face_edges.append(face)
            if not possible:
                continue
            signature_survivors += 1
            face_types = []
            for face in face_edges:
                canonical = canonical_k6(face)
                target_index = canonical_index.get(canonical)
                if target_index is None:
                    possible = False
                    break
                face_types.append(target_index)
            if not possible:
                continue
            counts = tuple(face_types.count(index) for index in range(73))
            previous = accepted_by_edges.get(edges7)
            if previous is not None and previous != counts:
                raise RuntimeError("inconsistent deletion count")
            accepted_by_edges[edges7] = counts
            base_accepted += 1
        print(
            f"base={base_index:02d} extensions={base_extensions} "
            f"accepted={base_accepted} total={len(accepted_by_edges)}",
            flush=True,
        )

    candidates = tuple(accepted_by_edges.items())
    if candidates:
        row_indices = []
        column_indices = []
        values = []
        for column, (_edges, counts) in enumerate(candidates):
            row_indices.append(0)
            column_indices.append(column)
            values.append(1.0)
            for index, count in enumerate(counts):
                if count:
                    row_indices.append(1 + index)
                    column_indices.append(column)
                    values.append(float(count))
        matrix = csc_matrix(
            (values, (row_indices, column_indices)),
            shape=(74, len(candidates)),
        )
        target_vector = np.array(
            [1.0] + [float(7 * weight) for weight in target_weights]
        )
        result = linprog(
            np.zeros(len(candidates)),
            A_eq=matrix,
            b_eq=target_vector,
            bounds=(0.0, None),
            method="highs",
        )
        residual = (
            float(np.max(np.abs(matrix @ result.x - target_vector)))
            if result.success
            else None
        )
        active = (
            np.flatnonzero(result.x > 1e-10).tolist()
            if result.success
            else []
        )
    else:
        result = None
        residual = None
        active = []

    report = {
        "status": "NUMERICAL EVIDENCE ONLY",
        "scope": (
            "Complete quarter-grid rank-five K7 extension search for the "
            "specific 73-orbit K6 support; not a continuous obstruction."
        ),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "solver": "scipy.optimize.linprog(method='highs')",
        "target_certificate": str(TARGET.relative_to(ROOT)),
        "target_sha256": TARGET_SHA256,
        "source_certificate": str(SOURCE.relative_to(ROOT)),
        "source_sha256": SOURCE_SHA256,
        "target_atoms": len(target_edges),
        "raw_labeled_extensions": raw_extensions,
        "signature_survivors": signature_survivors,
        "accepted_distinct_labeled_edges": len(candidates),
        "elapsed_seconds": time.time() - started,
        "lp_success": bool(result.success) if result is not None else False,
        "lp_message": result.message if result is not None else "no columns",
        "maximum_equality_residual": residual,
        "active_columns": active,
        "active_weights": (
            [float(result.x[index]) for index in active]
            if result is not None and result.success
            else []
        ),
        "candidates": [
            {
                "edges": list(edges),
                "deletion_counts": [
                    [index, count]
                    for index, count in enumerate(counts)
                    if count
                ],
            }
            for edges, counts in candidates
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in report if key != "candidates"}, indent=2))


if __name__ == "__main__":
    main()
