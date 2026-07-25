#!/usr/bin/env python3
"""Numerical root-triangle/K7 exchangeability-square search.

The feature space consists of every degree-at-most-three polynomial in the
ten edges of a rooted K5, invariant under permutations of the three root
vertices and interchange of the two extension vertices.  The program
reoptimizes the K7 atom weights subject to the exact target triangle
marginal and uses eigenvector cuts to maximize the minimum eigenvalue of the
48 by 48 finite-exchangeability moment block.

This is discovery code.  Its floating output is not a proof.
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
from scipy.sparse import csc_matrix, hstack, vstack


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
CATALOG = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "k7"
    / "results"
    / "direct_k7_from_51.csv"
)
SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
CATALOG_SHA256 = (
    "16cee0b4f7b6b7655990a74f7ffef104c4aef43d5074696cbbb1bcf413d1a623"
)

PAIRS7 = tuple(itertools.combinations(range(7), 2))
PAIR_INDEX7 = {pair: index for index, pair in enumerate(PAIRS7)}
LOCAL_EDGES = (
    (0, 1),
    (0, 2),
    (1, 2),
    (0, 3),
    (0, 4),
    (1, 3),
    (1, 4),
    (2, 3),
    (2, 4),
    (3, 4),
)
LOCAL_EDGE_INDEX = {pair: index for index, pair in enumerate(LOCAL_EDGES)}
KERNEL = {2: 703, 3: 12654, 4: 442890}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def weak_compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, length - 1):
            yield (first,) + rest


def group_actions():
    actions = []
    for root_permutation in itertools.permutations(range(3)):
        for extension_permutation in ((3, 4), (4, 3)):
            permutation = tuple(root_permutation) + extension_permutation
            actions.append(
                tuple(
                    LOCAL_EDGE_INDEX[
                        tuple(
                            sorted(
                                (
                                    permutation[first],
                                    permutation[second],
                                )
                            )
                        )
                    ]
                    for first, second in LOCAL_EDGES
                )
            )
    return tuple(actions)


def invariant_monomial_orbits(maximum_degree=3):
    actions = group_actions()
    exponents = tuple(
        exponent
        for degree in range(maximum_degree + 1)
        for exponent in weak_compositions(degree, 10)
    )
    seen = set()
    orbits = []
    for exponent in exponents:
        if exponent in seen:
            continue
        orbit = set()
        for action in actions:
            image = [0] * 10
            for old_index, new_index in enumerate(action):
                image[new_index] = exponent[old_index]
            orbit.add(tuple(image))
        seen.update(orbit)
        orbits.append(tuple(sorted(orbit)))
    return tuple(orbits)


def monomial_value(values, exponent):
    result = 1
    for value, power in zip(values, exponent):
        if power:
            result *= value**power
    return result


def feature_vector(values, orbits):
    return tuple(
        sum(monomial_value(values, exponent) for exponent in orbit)
        for orbit in orbits
    )


def scaled_edge(edges, first, second):
    return edges[PAIR_INDEX7[tuple(sorted((first, second)))]] - 4


def atomic_moment(edges, orbits):
    dimension = len(orbits)
    result = np.zeros((dimension, dimension), dtype=np.int64)
    for root in itertools.combinations(range(7), 3):
        residual = tuple(vertex for vertex in range(7) if vertex not in root)
        extensions = tuple(itertools.combinations(residual, 2))
        values = []
        for extension in extensions:
            vertices = root + extension
            local_values = tuple(
                scaled_edge(edges, vertices[first], vertices[second])
                for first, second in LOCAL_EDGES
            )
            values.append(feature_vector(local_values, orbits))
        feature_matrix = np.asarray(values, dtype=np.int64)
        kernel = np.asarray(
            [
                [
                    KERNEL[len(set(first) | set(second))]
                    for second in extensions
                ]
                for first in extensions
            ],
            dtype=np.int64,
        )
        result += feature_matrix.T @ kernel @ feature_matrix
    if not np.array_equal(result, result.T):
        raise RuntimeError("atomic moment is not symmetric")
    return result


def parse_catalog(catalog_path):
    if sha256(SOURCE) != SOURCE_SHA256:
        raise RuntimeError("source hash mismatch")
    actual_catalog_hash = sha256(catalog_path)
    if catalog_path.resolve() == CATALOG.resolve() and (
        actual_catalog_hash != CATALOG_SHA256
    ):
        raise RuntimeError(
            f"catalog hash changed: expected {CATALOG_SHA256}, "
            f"got {actual_catalog_hash}"
        )
    lines = catalog_path.read_text().splitlines()
    edges = []
    triangle_counts = []
    for line in lines[1:]:
        fields = tuple(map(int, line.split(",")))
        if len(fields) != 56:
            raise RuntimeError("wrong catalog row width")
        edges.append(fields[:21])
        triangle_counts.append(np.bincount(fields[21:], minlength=51))
    return (
        lines[0],
        actual_catalog_hash,
        tuple(edges),
        np.asarray(triangle_counts, dtype=float).T,
    )


def compute_moments(edges, orbits, cache):
    if cache is not None and cache.exists():
        payload = np.load(cache)
        moments = payload["moments"]
        if moments.shape != (len(edges), len(orbits), len(orbits)):
            raise RuntimeError("moment cache has wrong shape")
        return moments
    moments = np.empty(
        (len(edges), len(orbits), len(orbits)),
        dtype=np.int64,
    )
    started = time.time()
    for index, atom_edges in enumerate(edges):
        moments[index] = atomic_moment(atom_edges, orbits)
        if (index + 1) % 100 == 0:
            print(
                f"moments={index + 1}/{len(edges)} "
                f"seconds={time.time() - started:.1f}",
                flush=True,
            )
    if cache is not None:
        cache.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(cache, moments=moments)
    return moments


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--cache", type=Path)
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--degree", type=int, choices=(1, 2, 3), default=3)
    parser.add_argument("--max-iterations", type=int, default=250)
    parser.add_argument("--cuts-per-iteration", type=int, default=8)
    parser.add_argument("--tolerance", type=float, default=2e-9)
    args = parser.parse_args()

    orbits = invariant_monomial_orbits(args.degree)
    expected_dimensions = {1: 4, 2: 15, 3: 48}
    if len(orbits) != expected_dimensions[args.degree]:
        raise RuntimeError("unexpected invariant feature dimension")
    catalog_header, catalog_hash, edges, triangle_counts = parse_catalog(
        args.catalog
    )
    moments_integer = compute_moments(edges, orbits, args.cache)
    moment_scale = float(np.max(np.abs(moments_integer)))
    moments = moments_integer.astype(float) / moment_scale

    source = json.loads(SOURCE.read_text())
    nu = np.asarray([float(Q(value)) for value in source["nu"]])
    target = np.concatenate(([1.0], 7.0 * nu / 312.0))
    equality = csc_matrix(
        np.vstack((np.ones(len(edges)), triangle_counts))
    )
    equality_with_margin = hstack(
        (equality, csc_matrix((equality.shape[0], 1))),
        format="csc",
    )

    dimension = len(orbits)
    cut_vectors = [np.eye(dimension)[index] for index in range(dimension)]
    cut_keys = {
        tuple(np.round(vector, 12))
        for vector in cut_vectors
    }
    history = []
    solution = None
    eigenvalues = None
    for iteration in range(args.max_iterations):
        cut_rows = np.asarray(
            [
                -np.einsum("i,aij,j->a", vector, moments, vector)
                for vector in cut_vectors
            ]
        )
        inequalities = hstack(
            (
                csc_matrix(cut_rows),
                csc_matrix(np.ones((len(cut_vectors), 1))),
            ),
            format="csc",
        )
        objective = np.zeros(len(edges) + 1)
        objective[-1] = -1.0
        result = linprog(
            objective,
            A_ub=inequalities,
            b_ub=np.zeros(len(cut_vectors)),
            A_eq=equality_with_margin,
            b_eq=target,
            bounds=[(0.0, None)] * len(edges) + [(None, None)],
            method="highs",
            options={
                "dual_feasibility_tolerance": 1e-9,
                "primal_feasibility_tolerance": 1e-9,
            },
        )
        if not result.success:
            history.append(
                {
                    "iteration": iteration,
                    "cuts": len(cut_vectors),
                    "success": False,
                    "message": result.message,
                }
            )
            break
        solution = result.x[:-1]
        margin = result.x[-1]
        aggregate = np.einsum("a,aij->ij", solution, moments)
        aggregate = (aggregate + aggregate.T) / 2
        eigenvalues, eigenvectors = np.linalg.eigh(aggregate)
        history.append(
            {
                "iteration": iteration,
                "cuts": len(cut_vectors),
                "claimed_margin": float(margin),
                "actual_minimum_eigenvalue": float(eigenvalues[0]),
                "active_atoms": int(np.count_nonzero(solution > 1e-10)),
                "equality_residual": float(
                    np.max(np.abs(equality @ solution - target))
                ),
            }
        )
        print(json.dumps(history[-1]), flush=True)
        if eigenvalues[0] >= margin - args.tolerance:
            break
        order = np.argsort(eigenvalues)
        added = 0
        for eigen_index in order:
            if eigenvalues[eigen_index] >= margin - args.tolerance:
                break
            vector = eigenvectors[:, eigen_index]
            sign_index = int(np.argmax(np.abs(vector)))
            if vector[sign_index] < 0:
                vector = -vector
            key = tuple(np.round(vector, 12))
            if key in cut_keys:
                continue
            cut_keys.add(key)
            cut_vectors.append(vector)
            added += 1
            if added == args.cuts_per_iteration:
                break
        if added == 0:
            break

    active = (
        np.flatnonzero(solution > 1e-10).tolist()
        if solution is not None
        else []
    )
    report = {
        "status": "NUMERICAL EVIDENCE ONLY",
        "scope_warning": (
            "The 1782-column K7 catalog is incomplete. Feasibility gives a "
            "candidate for exact reconstruction; infeasibility would apply "
            "only to this catalog."
        ),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "solver": "scipy.optimize.linprog(method='highs')",
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": SOURCE_SHA256,
        "catalog": (
            str(args.catalog.resolve().relative_to(ROOT))
            if args.catalog.resolve().is_relative_to(ROOT)
            else str(args.catalog.resolve())
        ),
        "catalog_sha256": catalog_hash,
        "catalog_header": catalog_header,
        "catalog_atoms": len(edges),
        "feature_degree": args.degree,
        "feature_dimension": dimension,
        "feature_orbits": [
            [list(exponent) for exponent in orbit] for orbit in orbits
        ],
        "integer_kernel_by_union_size": {
            str(key): value for key, value in KERNEL.items()
        },
        "moment_scale": moment_scale,
        "iterations": history,
        "success": solution is not None,
        "final_claimed_margin": (
            history[-1].get("claimed_margin") if solution is not None else None
        ),
        "final_eigenvalues": (
            [float(value) for value in eigenvalues]
            if eigenvalues is not None
            else None
        ),
        "active_columns": active,
        "active_weights": (
            [float(solution[index]) for index in active]
            if solution is not None
            else []
        ),
        "active_edges": [list(edges[index]) for index in active],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(
        json.dumps(
            {
                key: value
                for key, value in report.items()
                if key
                not in {
                    "feature_orbits",
                    "iterations",
                    "active_weights",
                    "active_edges",
                }
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
