#!/usr/bin/env python3
"""Independent binary64 integrity checker for the construction portfolio.

The checker deliberately does not import the discovery program.  It rebuilds
the four exact source codes, checks the claimed search coverage, normalizes
every saved coordinate row anew, and recomputes maxima, hashes, spectra,
quantiles, and active graphs.  Passing this checker establishes faithful
reporting of floating-point near misses only; it does not certify a spherical
code unless the recomputed maximum is at most 1/2 with separate exact or
directed-interval coordinates.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np


EXPECTED_STATUS = "NUMERICAL EVIDENCE ONLY — NOT A CONSTRUCTION CERTIFICATE"
MECHANISMS = {
    "latitude_layer_release",
    "known_source_layer_insertion",
    "unrelated_random_basin",
    "remove_k_add_k_plus_one",
    "heterogeneous_latitude_crossover",
    "evolutionary_latitude_block",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def unit_rows(array: np.ndarray) -> np.ndarray:
    x = np.asarray(array, dtype=np.float64)
    require(x.ndim == 2 and x.shape[1] == 5, "wrong coordinate shape")
    norms = np.sqrt(np.sum(x * x, axis=1))
    require(float(np.min(norms)) > 1e-14, "zero coordinate row")
    return np.ascontiguousarray(x / norms[:, None])


def pairs(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    first, second = np.triu_indices(len(x), 1)
    values = np.sum(x[first] * x[second], axis=1)
    return first, second, values


def coordinate_hash(x: np.ndarray) -> str:
    data = np.ascontiguousarray(unit_rows(x), dtype="<f8")
    return hashlib.sha256(data.tobytes()).hexdigest()


def exact_known_codes() -> dict[str, tuple[tuple[Fraction, ...], ...]]:
    d5 = []
    for first, second in itertools.combinations(range(5), 2):
        for sign_first in (-1, 1):
            for sign_second in (-1, 1):
                row = [Fraction(0)] * 5
                row[first] = Fraction(sign_first)
                row[second] = Fraction(sign_second)
                d5.append(tuple(row))
    l5 = [row for row in d5 if row[4] != 1]
    l5 += [
        tuple(Fraction(sign, 2) for sign in signs) + (Fraction(1),)
        for signs in itertools.product((-1, 1), repeat=4)
        if sum(sign < 0 for sign in signs) % 2 == 1
    ]
    q5 = [row for row in d5 if sum(row) != 2]
    q5 += [
        tuple(value + Fraction(4, 5) for value in row)
        for row in d5
        if sum(row) == -2
    ]
    r5 = [row for row in l5 if sum(row) != 2]
    r5 += [
        tuple(value + Fraction(4, 5) for value in row)
        for row in l5
        if sum(row) == -2
    ]
    result = {"D5": tuple(d5), "L5": tuple(l5), "Q5": tuple(q5), "R5": tuple(r5)}
    require(
        all(len(code) == 40 and len(set(code)) == 40 for code in result.values()),
        "known-code cardinality failure",
    )
    return result


def exact_source_audit() -> dict:
    answer = {}
    for name, code in exact_known_codes().items():
        norms = [sum(value * value for value in row) for row in code]
        normalized = []
        for i, j in itertools.combinations(range(40), 2):
            dot = sum(code[i][k] * code[j][k] for k in range(5))
            # All generated rows have the same exact squared norm 2.
            require(norms[i] == 2 and norms[j] == 2, f"{name}: norm failure")
            normalized.append(dot / 2)
        require(max(normalized) == Fraction(1, 2), f"{name}: wrong maximum")
        histogram = Counter(normalized)
        answer[name] = {
            "cardinality": len(code),
            "maximum_inner_product": "1/2",
            "inner_product_histogram": {
                (
                    str(value.numerator)
                    if value.denominator == 1
                    else f"{value.numerator}/{value.denominator}"
                ): int(count)
                for value, count in sorted(histogram.items())
            },
        }
    return answer


def components(n: int, edges: list[list[int]]) -> list[int]:
    adjacency = [set() for _ in range(n)]
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    seen: set[int] = set()
    sizes = []
    for start in range(n):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def check_active_graph(
    x: np.ndarray, maximum: float, record: dict
) -> dict:
    first, second, values = pairs(x)
    tolerance = float(record["tolerance_below_maximum"])
    active = values >= maximum - tolerance
    edges = np.column_stack([first[active], second[active]]).astype(int).tolist()
    require(edges == record["edges"], "active edge list mismatch")
    require(len(edges) == int(record["edge_count"]), "active edge count mismatch")
    digest = hashlib.sha256(
        json.dumps(edges, separators=(",", ":")).encode()
    ).hexdigest()
    require(digest == record["edge_sha256"], "active edge hash mismatch")
    degree = np.zeros(len(x), dtype=int)
    for i, j in edges:
        degree[i] += 1
        degree[j] += 1
    unique, counts = np.unique(degree, return_counts=True)
    histogram = {
        str(int(value)): int(count)
        for value, count in zip(unique, counts)
    }
    require(histogram == record["degree_histogram"], "degree histogram mismatch")
    component_sizes = components(len(x), edges)
    require(component_sizes == record["component_sizes"], "component mismatch")
    return {
        "edge_count": len(edges),
        "degree_histogram": histogram,
        "component_sizes": component_sizes,
    }


def check_record(record: dict) -> dict:
    require(record["status"] == EXPECTED_STATUS, "record status mismatch")
    require(record["mechanism"] in MECHANISMS, "unknown mechanism")
    raw = np.asarray(record["coordinates_float64"], dtype=np.float64)
    x = unit_rows(raw)
    n = int(record["n"])
    require(n in (41, 42, 43, 44), "wrong cardinality")
    require(x.shape == (n, 5), "coordinate cardinality mismatch")
    require(
        coordinate_hash(raw)
        == record["coordinate_little_endian_float64_sha256"],
        "coordinate hash mismatch",
    )
    first, second, values = pairs(x)
    maximum = float(np.max(values))
    require(
        maximum == float(record["maximum_inner_product_binary64"]),
        "maximum mismatch",
    )
    require(maximum.hex() == record["maximum_inner_product_float_hex"], "hex mismatch")
    require(
        float(record["gap_above_one_half"]) == maximum - 0.5,
        "gap mismatch",
    )
    maximizing = np.flatnonzero(values == maximum)
    require(
        [[int(first[index]), int(second[index])] for index in maximizing]
        == record["literal_binary64_maximizing_pairs"],
        "maximizing-pair mismatch",
    )
    require(
        float(np.min(values)) == float(record["minimum_inner_product"]),
        "minimum mismatch",
    )
    quantiles = np.quantile(
        values, [0.0, 0.01, 0.10, 0.25, 0.50, 0.75, 0.90, 0.99, 1.0]
    )
    require(
        np.array_equal(
            quantiles,
            np.asarray(record["pair_inner_product_quantiles"], dtype=np.float64),
        ),
        "pair quantiles mismatch",
    )
    gram_eigenvalues = np.linalg.eigvalsh(x @ x.T)[::-1]
    frame_eigenvalues = np.linalg.eigvalsh(x.T @ x)[::-1]
    require(
        np.allclose(
            gram_eigenvalues,
            np.asarray(record["gram_eigenvalues_descending"]),
            rtol=2e-12,
            atol=2e-13,
        ),
        "Gram spectrum mismatch",
    )
    require(
        np.allclose(
            frame_eigenvalues,
            np.asarray(record["frame_eigenvalues_descending"]),
            rtol=2e-12,
            atol=2e-13,
        ),
        "frame spectrum mismatch",
    )
    rank = int(np.sum(gram_eigenvalues > 1e-9))
    require(rank == int(record["numerical_gram_rank_at_1e-9"]), "rank mismatch")
    centroid_norm = float(np.linalg.norm(np.sum(x, axis=0)))
    require(
        math.isclose(
            centroid_norm, float(record["centroid_norm"]), rel_tol=2e-13, abs_tol=2e-13
        ),
        "centroid mismatch",
    )
    graph = check_active_graph(x, maximum, record["active_graph"])
    return {
        "label": record["label"],
        "mechanism": record["mechanism"],
        "n": n,
        "maximum": maximum,
        "maximum_hex": maximum.hex(),
        "gap_above_one_half": maximum - 0.5,
        "rank": rank,
        "frame_eigenvalues": frame_eigenvalues.tolist(),
        "centroid_norm": centroid_norm,
        "active_graph": graph,
    }


def verify(path: Path) -> dict:
    raw_bytes = path.read_bytes()
    data = json.loads(raw_bytes)
    require(data["status"] == EXPECTED_STATUS, "portfolio status mismatch")
    require(data["dimension"] == 5, "wrong dimension")
    require(data["cardinalities"] == [41, 42, 43, 44], "wrong cardinalities")
    counts = data["search_counts"]
    require(int(counts["latitude_layer_starts"]) > 0, "no layer starts")
    require(int(counts["known_source_layer_starts"]) > 0, "no source layer starts")
    require(int(counts["unrelated_random_starts"]) > 0, "no random starts")
    require(int(counts["heterogeneous_crossovers"]) > 0, "no heterogeneous crossover")
    require(int(counts["equal_cardinality_crossovers"]) > 0, "no equal crossover")
    # Every seed contributes four exact sources, five initial values
    # k=2,...,6, and four moves.  Consolidated portfolios sum whole seed runs.
    require(
        int(counts["surgery_moves"]) >= 4 * 5 * 4
        and int(counts["surgery_moves"]) % (4 * 5 * 4) == 0,
        "incomplete surgery coverage",
    )
    source_portfolios = data.get("consolidated_source_portfolios", [])
    for source in source_portfolios:
        source_path = path.parent / source["filename"]
        require(source_path.exists(), f"missing source portfolio {source_path}")
        require(
            hashlib.sha256(source_path.read_bytes()).hexdigest() == source["sha256"],
            f"source portfolio hash mismatch: {source_path}",
        )
    checked = [check_record(record) for record in data["records"]]
    labels = {record["label"] for record in checked}
    require(
        len(labels) == len(checked) and labels,
        "record labels are not unique",
    )
    require(
        set(record["mechanism"] for record in checked) == MECHANISMS,
        "mechanism portfolio incomplete",
    )
    for n in (41, 42, 43, 44):
        relevant = [record for record in checked if record["n"] == n]
        require(relevant, f"N={n}: no record")
        best = min(relevant, key=lambda item: item["maximum"])
        stored_label = data["best_record_labels_by_cardinality"][n - 41]
        require(best["label"] == stored_label, f"N={n}: wrong best label")
    # Every initial k and every exact source must occur among surgery records.
    surgery = [
        record for record in data["records"]
        if record["mechanism"] == "remove_k_add_k_plus_one"
    ]
    # Only the best record per N is stored, so coverage lives in global counts;
    # check that every retained record nevertheless has legal provenance.
    for record in surgery:
        provenance = record["provenance"]
        require(provenance["exact_source"] in exact_known_codes(), "bad source")
        require(int(provenance["initial_k"]) in range(2, 7), "bad initial k")
        require(
            all(int(move["k"]) in range(2, 7) for move in provenance["moves"]),
            "bad surgery k",
        )
    return {
        "status": "VERIFIED NUMERICAL REPORTING — NOT AN EXACT CODE",
        "portfolio_path": str(path),
        "portfolio_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "source_code_exact_audit": exact_source_audit(),
        "record_count": len(checked),
        "records": checked,
        "best_by_cardinality": {
            str(n): min(
                record["maximum"] for record in checked if record["n"] == n
            )
            for n in (41, 42, 43, 44)
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "portfolio",
        type=Path,
        nargs="?",
        default=Path(__file__).with_name("portfolio.json"),
    )
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args()
    report = verify(args.portfolio)
    if args.write_report is not None:
        args.write_report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
