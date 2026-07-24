#!/usr/bin/env python3
"""Independent binary64 checker for round-6 bundle-search artifacts."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np


def edge_digest(edges: list[list[int]]) -> str:
    canonical = json.dumps(edges, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


def components(n: int, edges: list[list[int]]) -> list[int]:
    adjacency = [[] for _ in range(n)]
    for first, second in edges:
        adjacency[first].append(second)
        adjacency[second].append(first)
    seen = set()
    answer = []
    for start in range(n):
        if start in seen:
            continue
        seen.add(start)
        stack = [start]
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        answer.append(size)
    return sorted(answer, reverse=True)


def check_run(run: dict) -> float:
    stored = run["best"]
    x = np.asarray(stored["coordinates_float64"], dtype=float)
    if x.shape != (run["n"], 5):
        raise AssertionError("wrong coordinate shape")
    norms2 = np.sum(x * x, axis=1)
    norm_error = float(np.max(np.abs(norms2 - 1.0)))
    if abs(norm_error - stored["row_norm_max_error"]) > 2e-16:
        raise AssertionError("stored norm error mismatch")
    if norm_error > 8e-15:
        raise AssertionError("coordinates are not binary64-unit rows")
    gram = x @ x.T
    ii, jj = np.triu_indices(len(x), 1)
    values = gram[ii, jj]
    top = float(np.max(values))
    bottom = float(np.min(values))
    if abs(top - stored["maximum"]) > 5e-15:
        raise AssertionError("maximum mismatch")
    if abs(bottom - stored["minimum"]) > 5e-15:
        raise AssertionError("minimum mismatch")
    if abs(top - 0.5 - stored["gap_above_one_half"]) > 5e-15:
        raise AssertionError("gap mismatch")
    if int(np.sum(values < -0.5)) != stored[
        "deep_negative_pairs_below_minus_half"
    ]:
        raise AssertionError("deep-negative count mismatch")
    eigenvalues = np.linalg.eigvalsh(gram)
    if float(np.max(np.abs(eigenvalues - stored["gram_eigenvalues"]))) > 3e-13:
        raise AssertionError("Gram spectrum mismatch")
    for label, expected in stored["pair_quantiles"].items():
        observed = float(np.quantile(values, float(label)))
        if abs(observed - expected) > 5e-15:
            raise AssertionError("pair quantile mismatch")
    for tolerance in (1e-4, 1e-6, 1e-8):
        active = stored[f"active_{tolerance:.0e}"]
        chosen = values >= top - tolerance
        edges = np.column_stack([ii[chosen], jj[chosen]]).tolist()
        if edges != active["edges"]:
            raise AssertionError("active edge list mismatch")
        if edge_digest(edges) != active["edge_sha256"]:
            raise AssertionError("active edge digest mismatch")
        degree = np.bincount(np.asarray(edges, dtype=int).ravel(), minlength=len(x))
        unique, counts = np.unique(degree, return_counts=True)
        histogram = {
            str(int(key)): int(value) for key, value in zip(unique, counts)
        }
        if histogram != active["degree_histogram"]:
            raise AssertionError("degree histogram mismatch")
        if components(len(x), edges) != active["component_sizes"]:
            raise AssertionError("component sizes mismatch")
    return top


def check_depth(path: Path, portfolio_hash: str, portfolio: dict):
    with path.open() as stream:
        payload = json.load(stream)
    if payload["source_artifact_sha256"] != portfolio_hash:
        raise AssertionError("depth probe is not bound to this portfolio")
    probe = payload["probe"]
    if not probe["status"].startswith("NUMERICAL EVIDENCE ONLY"):
        raise AssertionError("depth probe lacks warning")
    split = probe["shallowest_split"]
    if (
        split["strict_negative"]
        + split["boundary"]
        + split["strict_positive"]
        != 41
    ):
        raise AssertionError("depth split does not total 41")
    if split["min_strict_side"] != min(
        split["strict_negative"], split["strict_positive"]
    ):
        raise AssertionError("strict-side minimum mismatch")
    if split["min_closed_side"] != min(
        split["strict_negative"] + split["boundary"],
        split["strict_positive"] + split["boundary"],
    ):
        raise AssertionError("closed-side minimum mismatch")
    if probe["hyperplanes_examined"] + probe[
        "rank_deficient_supports_skipped"
    ] != math_comb(41, 4):
        raise AssertionError("not all four-point supports accounted for")
    matching = [
        run
        for run in portfolio["runs"]
        if run["n"] == 41
        and run["seed"] == payload["source_seed"]
        and run["origin"] == payload["source_origin"]
    ]
    if len(matching) != 1:
        raise AssertionError("depth source trajectory is not unique")
    x = np.asarray(matching[0]["best"]["coordinates_float64"], dtype=float)
    normal = np.asarray(split["normal"], dtype=float)
    dots = x @ normal
    tolerance = float(probe["tolerance"])
    negative = int(np.sum(dots < -tolerance))
    positive = int(np.sum(dots > tolerance))
    boundary = len(x) - negative - positive
    if [negative, boundary, positive] != [
        split["strict_negative"],
        split["boundary"],
        split["strict_positive"],
    ]:
        raise AssertionError("stored shallow normal has the wrong split")

    # Re-enumerate the entire numerical probe independently.  We compare its
    # sign-symmetric histogram, which avoids relying on SVD normal orientation.
    histogram: dict[str, int] = {}
    examined = 0
    skipped = 0
    best_rank = None
    for support in itertools.combinations(range(41), 4):
        _, singular, right = np.linalg.svd(
            x[list(support)], full_matrices=True
        )
        if singular[-1] < 1e-10:
            skipped += 1
            continue
        dots = x @ right[-1]
        positive = int(np.sum(dots > tolerance))
        negative = int(np.sum(dots < -tolerance))
        boundary = 41 - positive - negative
        smaller = min(positive, negative)
        larger = max(positive, negative)
        label = f"{smaller}/{boundary}/{larger}"
        histogram[label] = histogram.get(label, 0) + 1
        ranking = (
            smaller,
            min(positive + boundary, negative + boundary),
            boundary,
        )
        if best_rank is None or ranking < best_rank:
            best_rank = ranking
        examined += 1
    if histogram != probe["split_histogram"]:
        raise AssertionError("independent depth split histogram mismatch")
    if examined != probe["hyperplanes_examined"] or skipped != probe[
        "rank_deficient_supports_skipped"
    ]:
        raise AssertionError("independent depth support accounting mismatch")
    stored_rank = (
        split["min_strict_side"],
        split["min_closed_side"],
        split["boundary"],
    )
    if stored_rank != best_rank:
        raise AssertionError("stored shallowest depth ranking mismatch")


def math_comb(n: int, k: int) -> int:
    result = 1
    for value in range(1, k + 1):
        result = result * (n - value + 1) // value
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio", type=Path)
    parser.add_argument("--depth", type=Path)
    arguments = parser.parse_args(argv)
    with arguments.portfolio.open() as stream:
        payload = json.load(stream)
    if not payload["status"].startswith("NUMERICAL EVIDENCE ONLY"):
        raise AssertionError("portfolio lacks numerical-only warning")
    best = {}
    for run in payload["runs"]:
        value = check_run(run)
        best[run["n"]] = min(best.get(run["n"], float("inf")), value)
    if sorted(best) != [41, 42, 43, 44]:
        raise AssertionError("portfolio does not cover N=41,42,43,44")
    for n in sorted(best):
        print(f"N={n} best verified maximum={best[n]:.16f}")
    portfolio_hash = sha256(arguments.portfolio)
    if arguments.depth is not None:
        check_depth(arguments.depth, portfolio_hash, payload)
        print("full depth histogram independently recomputed")
    print("PASS (binary64 artifact integrity only; not a proof)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
