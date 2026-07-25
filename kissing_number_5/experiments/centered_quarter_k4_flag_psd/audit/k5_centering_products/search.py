#!/usr/bin/env python3
"""Search the centered quarter-grid K2--K5 product relaxation.

This is discovery code.  It uses every full S5 orbit from
``enumerate_k5_orbits.cpp``; no triangle-count compression is used.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog
from scipy.sparse import (
    csc_matrix,
    csr_matrix,
    hstack,
    load_npz,
    save_npz,
    vstack,
)

from experiments.centered_quarter_k4_flag_psd.audit.rationalize_full_witness import (
    affine_system,
)
from experiments.centered_quarter_k4_flag_psd.audit.search_full_centering import (
    coefficients,
    edge,
)
from experiments.centered_quarter_k4_flag_psd.search import canonical


EDGES5 = tuple(itertools.combinations(range(5), 2))
EDGE5_INDEX = {pair: index for index, pair in enumerate(EDGES5)}
PERMUTATIONS5 = tuple(itertools.permutations(range(5)))


def edge5(pattern: np.ndarray, first: int, second: int) -> int:
    return int(pattern[EDGE5_INDEX[tuple(sorted((first, second)))]])


def canonical_descriptor(
    q: int, a: int, b: int, c: int, d: int, center: int
) -> tuple[int, int, int, int, int, int]:
    direct = (q, a, b, c, d, center)
    swapped_center = 1 if center == 0 else 0 if center == 1 else 2
    swapped = (q, b, a, d, c, swapped_center)
    return min(direct, swapped)


def parse_orbits(path: Path) -> tuple[np.ndarray, str]:
    lines = path.read_text().splitlines()
    assert lines
    header = lines[0]
    assert header == (
        "# feasible_labeled_k5=12087822 full_orbits=108023 "
        "orbit_size_sum=12087822"
    )
    patterns = np.loadtxt(
        path,
        delimiter=",",
        comments="#",
        usecols=range(1, 11),
        dtype=np.int8,
    )
    automorphisms = np.loadtxt(
        path,
        delimiter=",",
        comments="#",
        usecols=(11,),
        dtype=np.int16,
    )
    assert patterns.shape == (108023, 10)
    assert np.all((0 <= patterns) & (patterns < 7))
    assert all(120 % int(value) == 0 for value in automorphisms)
    assert sum(120 // int(value) for value in automorphisms) == 12087822
    return patterns, header


def product_descriptors(k4_orbits: tuple[tuple[int, ...], ...]):
    descriptors = set()
    for pattern in k4_orbits:
        for i, j, k, extension in itertools.permutations(range(4)):
            q = edge(pattern, i, j)
            a = edge(pattern, i, k)
            b = edge(pattern, j, k)
            c = edge(pattern, i, extension)
            d = edge(pattern, j, extension)
            for center in range(3):
                descriptors.add(
                    canonical_descriptor(q, a, b, c, d, center)
                )
    return tuple(sorted(descriptors))


def build_matrices(
    data: dict,
    patterns: np.ndarray,
    cache: Path,
) -> tuple[csr_matrix, csr_matrix, csr_matrix, tuple]:
    product_k4_path = cache / "product_k4.npz"
    product_k5_path = cache / "product_k5.npz"
    face_path = cache / "face_k5.npz"
    descriptor_path = cache / "descriptors.json"
    if all(
        path.exists()
        for path in (
            product_k4_path,
            product_k5_path,
            face_path,
            descriptor_path,
        )
    ):
        descriptors = tuple(
            tuple(item) for item in json.loads(descriptor_path.read_text())
        )
        return (
            load_npz(product_k4_path).tocsr(),
            load_npz(product_k5_path).tocsr(),
            load_npz(face_path).tocsr(),
            descriptors,
        )

    descriptors = product_descriptors(data["orbits"])
    descriptor_index = {
        descriptor: index for index, descriptor in enumerate(descriptors)
    }
    print(f"product rows after edge-swap symmetry: {len(descriptors)}")
    grid4 = tuple(round(4 * float(value)) for value in data["grid"])

    k4_rows: list[int] = []
    k4_columns: list[int] = []
    k4_values: list[int] = []
    for column, pattern in enumerate(data["orbits"]):
        contribution: dict[int, int] = {}
        for i, j, k, extension in itertools.permutations(range(4)):
            q = edge(pattern, i, j)
            a = edge(pattern, i, k)
            b = edge(pattern, j, k)
            c = edge(pattern, i, extension)
            d = edge(pattern, j, extension)
            centers = (i, j, k)
            incidents = ((q, a), (q, b), (a, b))
            for center, (vertex, incident) in enumerate(
                zip(centers, incidents)
            ):
                descriptor = canonical_descriptor(
                    q, a, b, c, d, center
                )
                row = descriptor_index[descriptor]
                target4 = -4 - grid4[incident[0]] - grid4[incident[1]]
                coefficient = 5 * (
                    grid4[edge(pattern, vertex, extension)] - target4
                )
                if coefficient:
                    contribution[row] = (
                        contribution.get(row, 0) + coefficient
                    )
        for row, value in contribution.items():
            if value:
                k4_rows.append(row)
                k4_columns.append(column)
                k4_values.append(value)
    product_k4 = csr_matrix(
        (k4_values, (k4_rows, k4_columns)),
        shape=(len(descriptors), len(data["orbits"])),
        dtype=np.float64,
    )

    k5_rows: list[int] = []
    k5_columns: list[int] = []
    k5_values: list[int] = []
    face_rows: list[int] = []
    face_columns: list[int] = []
    face_values: list[int] = []
    k4_index = {
        pattern: index for index, pattern in enumerate(data["orbits"])
    }
    started = time.monotonic()
    for column, pattern in enumerate(patterns):
        face_counts: dict[int, int] = {}
        for omitted in range(5):
            vertices = [vertex for vertex in range(5) if vertex != omitted]
            face = tuple(
                edge5(pattern, vertices[first], vertices[second])
                for first, second in itertools.combinations(range(4), 2)
            )
            orbit = k4_index[canonical(face)]
            face_counts[orbit] = face_counts.get(orbit, 0) + 1
        for row, value in face_counts.items():
            face_rows.append(row)
            face_columns.append(column)
            face_values.append(value)

        contribution: dict[int, int] = {}
        for i, j, k, extension, other in PERMUTATIONS5:
            q = edge5(pattern, i, j)
            a = edge5(pattern, i, k)
            b = edge5(pattern, j, k)
            c = edge5(pattern, i, extension)
            d = edge5(pattern, j, extension)
            for center, vertex in enumerate((i, j, k)):
                descriptor = canonical_descriptor(
                    q, a, b, c, d, center
                )
                row = descriptor_index[descriptor]
                coefficient = 37 * grid4[
                    edge5(pattern, vertex, other)
                ]
                if coefficient:
                    contribution[row] = (
                        contribution.get(row, 0) + coefficient
                    )
        for row, value in contribution.items():
            if value:
                k5_rows.append(row)
                k5_columns.append(column)
                k5_values.append(value)
        if (column + 1) % 10000 == 0:
            print(
                f"built {column + 1}/{len(patterns)} K5 columns "
                f"in {time.monotonic() - started:.1f}s",
                flush=True,
            )

    product_k5 = csr_matrix(
        (k5_values, (k5_rows, k5_columns)),
        shape=(len(descriptors), len(patterns)),
        dtype=np.float64,
    )
    face_k5 = csr_matrix(
        (face_values, (face_rows, face_columns)),
        shape=(len(data["orbits"]), len(patterns)),
        dtype=np.float64,
    )
    cache.mkdir(parents=True, exist_ok=True)
    save_npz(product_k4_path, product_k4)
    save_npz(product_k5_path, product_k5)
    save_npz(face_path, face_k5)
    descriptor_path.write_text(json.dumps(descriptors) + "\n")
    return product_k4, product_k5, face_k5, descriptors


def main() -> None:
    root = Path(__file__).resolve().parents[4]
    folder = Path(__file__).resolve().parent
    source = json.loads(
        (
            root
            / "certificates/centered_quarter_bv_pseudodistribution.json"
        ).read_text()
    )
    data = coefficients(source)
    orbit_path = folder / "results/k5_orbits.csv"
    patterns, orbit_header = parse_orbits(orbit_path)
    product_k4, product_k5, face_k5, descriptors = build_matrices(
        data, patterns, folder / "results/matrix_cache"
    )
    print(
        f"nnz product K4={product_k4.nnz} "
        f"K5={product_k5.nnz} faces={face_k5.nnz}",
        flush=True,
    )

    affine, affine_rhs = affine_system(data)
    # Remove exactly redundant affine rows using the same deterministic
    # rank-revealing selection as the K4 rationalizer.
    _, factor, permutation = qr(
        affine.T.astype(float), pivoting=True, mode="economic"
    )
    diagonal = np.abs(np.diag(factor))
    rank = int(np.sum(diagonal > diagonal[0] * 1e-10))
    affine = affine[permutation[:rank]]
    affine_rhs = affine_rhs[permutation[:rank]]

    lower_count = affine.shape[1]
    k5_count = len(patterns)
    zero_lower_k5 = csr_matrix((rank, k5_count))
    affine_block = hstack(
        (csr_matrix(affine, dtype=float), zero_lower_k5), format="csr"
    )

    # A uniform K4 face of a uniform K5 set has distribution k4, hence
    # expected face count = 5*k4.
    face_left = csr_matrix(
        (
            [-5.0] * len(data["orbits"]),
            (
                range(len(data["orbits"])),
                range(7 + len(data["triples"]), lower_count),
            ),
        ),
        shape=(len(data["orbits"]), lower_count),
    )
    face_block = hstack((face_left, face_k5), format="csr")

    product_left = hstack(
        (
            csr_matrix(
                (len(descriptors), 7 + len(data["triples"]))
            ),
            product_k4,
        ),
        format="csr",
    )
    product_block = hstack(
        (product_left, product_k5), format="csr"
    )
    matrix = vstack(
        (affine_block, face_block, product_block), format="csc"
    )
    target = np.r_[
        affine_rhs.astype(float),
        np.zeros(len(data["orbits"]) + len(descriptors)),
    ]
    print(
        f"LP shape={matrix.shape} nnz={matrix.nnz} "
        f"affine_rank={rank}",
        flush=True,
    )
    result = linprog(
        np.zeros(matrix.shape[1]),
        A_eq=matrix,
        b_eq=target,
        bounds=(0, None),
        method="highs",
        options={"time_limit": 1200},
    )
    report = {
        "schema": "kissing5.centered_quarter_k2_k5_product_search.v1",
        "status": str(result.message),
        "success": bool(result.success),
        "linprog_status": int(result.status),
        "full_k5_orbit_header": orbit_header,
        "full_k5_orbit_sha256": hashlib.sha256(
            orbit_path.read_bytes()
        ).hexdigest(),
        "k5_orbit_count": len(patterns),
        "product_row_count": len(descriptors),
        "affine_rank": rank,
        "matrix_shape": list(matrix.shape),
        "matrix_nnz": int(matrix.nnz),
    }
    if result.x is not None:
        lower = result.x[:lower_count]
        mu = result.x[lower_count:]
        residual = matrix @ result.x - target
        report.update(
            {
                "maximum_equality_residual": float(
                    np.max(np.abs(residual))
                ),
                "minimum_variable": float(np.min(result.x)),
                "positive_lower_variables_at_1e-10": int(
                    np.sum(lower > 1e-10)
                ),
                "positive_k5_orbits_at_1e-10": int(
                    np.sum(mu > 1e-10)
                ),
                "lower": lower.tolist(),
                "k5": mu.tolist(),
            }
        )
    output = folder / "results/search.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                key: value
                for key, value in report.items()
                if key not in ("lower", "k5")
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
