#!/usr/bin/env python3
"""Independent verifier for split-homotopy binary64 portfolios.

This checker deliberately does not import the discovery program.  It
reconstructs the four exact rational sources and independently recomputes
all stored endpoint maxima, hashes, spectra, and active graphs.  It is a
floating-point integrity checker, not an exact-real feasibility proof.
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

import numpy as np


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def unit_rows(array: np.ndarray) -> np.ndarray:
    x = np.asarray(array, dtype=np.float64)
    require(x.ndim == 2 and x.shape[1] == 5, "wrong coordinate shape")
    norms = np.sqrt(np.sum(x * x, axis=1))
    require(float(np.min(norms)) > 1e-14, "zero coordinate row")
    return np.ascontiguousarray(x / norms[:, None])


def pairs(x: np.ndarray):
    first, second = np.triu_indices(len(x), 1)
    values = np.sum(x[first] * x[second], axis=1)
    return first, second, values


def coordinate_hash(x: np.ndarray) -> str:
    data = np.ascontiguousarray(unit_rows(x), dtype="<f8")
    return hashlib.sha256(data.tobytes()).hexdigest()


def known_codes() -> dict[str, tuple[tuple[Fraction, ...], ...]]:
    d5 = []
    for first, second in itertools.combinations(range(5), 2):
        for sign_first in (-1, 1):
            for sign_second in (-1, 1):
                row = [Fraction(0)] * 5
                row[first] = sign_first
                row[second] = sign_second
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
    result = {
        "D5": tuple(d5),
        "L5": tuple(l5),
        "Q5": tuple(q5),
        "R5": tuple(r5),
    }
    require(
        all(len(code) == 40 and len(set(code)) == 40 for code in result.values()),
        "known source cardinality failure",
    )
    return result


def fraction_text(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def exact_histogram(code) -> dict[str, int]:
    counter = Counter(
        sum(code[i][k] * code[j][k] for k in range(5))
        for i, j in itertools.combinations(range(40), 2)
    )
    return {
        fraction_text(value): int(count)
        for value, count in sorted(counter.items())
    }


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


def check_graph(x: np.ndarray, record: dict) -> None:
    first, second, values = pairs(x)
    top = float(np.max(values))
    chosen = values >= top - float(record["tolerance"])
    edges = np.column_stack([first[chosen], second[chosen]]).astype(int).tolist()
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
    require(
        components(len(x), edges) == record["component_sizes"],
        "component sizes mismatch",
    )


def check_diagnostics(record: dict) -> dict:
    raw = np.asarray(record["coordinates_float64"], dtype=np.float64)
    x = unit_rows(raw)
    require(x.shape == (int(record["n"]), 5), "diagnostic cardinality mismatch")
    require(
        coordinate_hash(raw)
        == record["coordinate_little_endian_float64_sha256"],
        "coordinate hash mismatch",
    )
    first, second, values = pairs(x)
    top = float(np.max(values))
    require(
        top == float(record["maximum_inner_product_binary64"]),
        "maximum mismatch",
    )
    require(top.hex() == record["maximum_inner_product_float_hex"], "hex mismatch")
    maximizing = np.flatnonzero(values == top)
    require(
        [[int(first[k]), int(second[k])] for k in maximizing]
        == record["literal_binary64_maximizing_pairs"],
        "maximizing-pair mismatch",
    )
    require(
        int(np.sum(values > 0.5)) == int(record["pairs_above_one_half"]),
        "threshold pair count mismatch",
    )
    require(
        bool(top <= 0.5) == bool(record["meets_threshold_binary64"]),
        "threshold flag mismatch",
    )
    spectrum = np.linalg.eigvalsh(x.T @ x)
    require(
        np.allclose(
            spectrum,
            np.asarray(record["positive_gram_eigenvalues"]),
            rtol=0.0,
            atol=8e-13,
        ),
        "frame spectrum mismatch",
    )
    gram_spectrum = np.linalg.eigvalsh(x @ x.T)
    tail = float(np.max(np.abs(gram_spectrum[:-5])))
    require(
        abs(tail - float(record["gram_tail_max_abs"])) <= 8e-13,
        "Gram tail mismatch",
    )
    for key in ("active_1e-4", "active_1e-6", "active_1e-8"):
        check_graph(x, record[key])
    return {
        "n": len(x),
        "maximum": top,
        "maximum_hex": top.hex(),
        "hash": coordinate_hash(raw),
        "positive_gram_eigenvalues": spectrum.tolist(),
        "active_edges_1e-8": int(record["active_1e-8"]["edge_count"]),
    }


def verify(path: Path) -> dict:
    payload = json.loads(path.read_text())
    if "polished_best_by_source_n" in payload:
        return verify_polished(path, payload)
    require(payload["smooth_max_surrogate_used"] is False, "wrong method flag")
    exact = known_codes()
    for name, record in payload["sources"].items():
        expected_rows = [
            [fraction_text(value) for value in row] for row in exact[name]
        ]
        require(
            expected_rows == record["coordinates_numerator_over_sqrt2"],
            f"{name} exact coordinates mismatch",
        )
        require(
            exact_histogram(exact[name])
            == record[
                "exact_pair_inner_product_histogram_before_dividing_by_two"
            ],
            f"{name} exact histogram mismatch",
        )
        for row in exact[name]:
            require(sum(value * value for value in row) == 2, "source norm failure")
        for i, j in itertools.combinations(range(40), 2):
            require(
                sum(exact[name][i][k] * exact[name][j][k] for k in range(5))
                <= 1,
                "source cap failure",
            )
        check_diagnostics(record["floating_diagnostics"])

    checked_runs = []
    by_n: dict[int, list[tuple[float, dict]]] = {}
    by_source_n: dict[tuple[str, int], list[tuple[float, dict]]] = {}
    threshold = False
    for run in payload["runs"]:
        n = int(run["n"])
        require(n - 40 == int(run["split_count"]), "split count mismatch")
        require(
            len(run["selected_source_parent_indices"]) == n - 40,
            "parent count mismatch",
        )
        require(
            len(set(run["selected_source_parent_indices"])) == n - 40,
            "duplicate split parent",
        )
        require(
            len(run["current_split_pair_indices"]) == n - 40,
            "pair count mismatch",
        )
        require(
            run["separation_schedule_radians"]
            == payload["parameters"]["theta_schedule_radians"],
            "theta schedule mismatch",
        )
        require(
            run["release_radius_schedule"]
            == payload["parameters"]["release_radius_schedule"],
            "release schedule mismatch",
        )
        require(
            len(run["stages"])
            == len(payload["parameters"]["theta_schedule_radians"]),
            "stage count mismatch",
        )
        constrained = check_diagnostics(run["constrained_endpoint"])
        released = check_diagnostics(run["released_endpoint"])
        best = check_diagnostics(run["best"])
        require(
            best["maximum"] <= min(
                constrained["maximum"], released["maximum"]
            )
            + 2e-15,
            "stored best is not best endpoint",
        )
        by_n.setdefault(n, []).append((best["maximum"], run))
        by_source_n.setdefault((run["source"], n), []).append(
            (best["maximum"], run)
        )
        threshold |= best["maximum"] <= 0.5
        checked_runs.append(
            {
                "source": run["source"],
                "n": n,
                "seed": int(run["seed"]),
                "variant": int(run["variant"]),
                "constrained_maximum": constrained["maximum"],
                "released_maximum": released["maximum"],
                "best": best,
            }
        )

    for n, entries in by_n.items():
        _, chosen = min(entries, key=lambda item: item[0])
        record = payload["best_by_n"][str(n)]
        require(record["source"] == chosen["source"], "best-by-N source mismatch")
        require(int(record["seed"]) == int(chosen["seed"]), "best-by-N seed mismatch")
        require(
            float(record["maximum_inner_product_binary64"])
            == float(chosen["best"]["maximum_inner_product_binary64"]),
            "best-by-N value mismatch",
        )
    for key, entries in by_source_n.items():
        _, chosen = min(entries, key=lambda item: item[0])
        record = payload["best_by_source_n"][f"{key[0]}:{key[1]}"]
        require(
            int(record["seed"]) == int(chosen["seed"]),
            "best-by-source seed mismatch",
        )
        require(
            float(record["maximum_inner_product_binary64"])
            == float(chosen["best"]["maximum_inner_product_binary64"]),
            "best-by-source value mismatch",
        )
    require(
        bool(payload["binary64_threshold_hit"]) == threshold,
        "global threshold flag mismatch",
    )
    return {
        "portfolio": str(path),
        "sources_checked": sorted(payload["sources"]),
        "runs_checked": len(checked_runs),
        "binary64_threshold_hit": threshold,
        "runs": checked_runs,
        "warning": (
            "Binary64 integrity only; not exact-real or directed-interval "
            "verification."
        ),
    }


def verify_polished(path: Path, payload: dict) -> dict:
    source_path = Path(payload["source_best_file"])
    require(source_path.exists(), "polished source-best file is missing")
    require(
        hashlib.sha256(source_path.read_bytes()).hexdigest()
        == payload["source_best_sha256"],
        "polished source-best hash mismatch",
    )
    source = json.loads(source_path.read_text())
    require(
        set(source["best_by_source_n"])
        == set(payload["polished_best_by_source_n"]),
        "polished key set mismatch",
    )
    checked = []
    by_n: dict[int, list[tuple[float, dict]]] = {}
    threshold = False
    for key, record in payload["polished_best_by_source_n"].items():
        source_record = source["best_by_source_n"][key]
        require(
            record["initial"] == source_record["diagnostics"],
            "polish initial diagnostic mismatch",
        )
        initial = check_diagnostics(record["initial"])
        polished = check_diagnostics(record["polished"])
        selected = check_diagnostics(record["selected"])
        expected = (
            polished
            if polished["maximum"] < initial["maximum"]
            else initial
        )
        require(
            selected["hash"] == expected["hash"],
            "polished selection mismatch",
        )
        require(
            bool(record["polish_improved"])
            == (polished["maximum"] < initial["maximum"]),
            "polished improvement flag mismatch",
        )
        require(int(record["n"]) == selected["n"], "polished N mismatch")
        require(record["source"] == key.split(":")[0], "polished source mismatch")
        by_n.setdefault(selected["n"], []).append((selected["maximum"], record))
        threshold |= selected["maximum"] <= 0.5
        checked.append(
            {
                "key": key,
                "source": record["source"],
                "n": selected["n"],
                "seed": int(record["seed"]),
                "initial_maximum": initial["maximum"],
                "polished_maximum": polished["maximum"],
                "selected": selected,
                "solver_success": bool(record["solver"]["success"]),
            }
        )
    for n, entries in by_n.items():
        _, chosen = min(entries, key=lambda item: item[0])
        summary = payload["best_by_n"][str(n)]
        require(summary["source"] == chosen["source"], "polished best source mismatch")
        require(int(summary["seed"]) == int(chosen["seed"]), "polished best seed mismatch")
        require(
            float(summary["maximum_inner_product_binary64"])
            == float(chosen["selected"]["maximum_inner_product_binary64"]),
            "polished best value mismatch",
        )
    require(
        bool(payload["binary64_threshold_hit"]) == threshold,
        "polished threshold flag mismatch",
    )
    return {
        "portfolio": str(path),
        "source_best_file": str(source_path),
        "runs_checked": len(checked),
        "binary64_threshold_hit": threshold,
        "runs": checked,
        "warning": (
            "Binary64 integrity only; not exact-real or directed-interval "
            "verification."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio", type=Path)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = verify(arguments.portfolio)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if arguments.output is not None:
        arguments.output.write_text(rendered)
    if result["binary64_threshold_hit"]:
        raise SystemExit(
            "A <=1/2 binary64 endpoint requires exact or interval verification."
        )


if __name__ == "__main__":
    main()
