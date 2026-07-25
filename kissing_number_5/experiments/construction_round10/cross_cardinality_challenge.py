#!/usr/bin/env python3
"""Challenge local subset traps by deleting from larger structured outputs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np

from .rank5_metric_subset_search import (
    STATUS,
    diagnostics,
    epigraph_slsqp,
    mapped_points,
    optimize_metric,
    root_shell,
    unrestricted_refine,
)


def best_deletion(coordinates: np.ndarray, target: int) -> tuple[np.ndarray, dict]:
    n = len(coordinates)
    deletion_count = n - target
    if deletion_count < 1 or deletion_count > 3:
        raise ValueError("this exact deletion audit supports one to three points")
    gram = coordinates @ coordinates.T
    best_key: tuple[float, float] | None = None
    best_keep: np.ndarray | None = None
    combinations_checked = 0
    for removed in itertools.combinations(range(n), deletion_count):
        keep = np.asarray(
            [index for index in range(n) if index not in removed], dtype=int
        )
        block = gram[np.ix_(keep, keep)]
        values = block[np.triu_indices(target, 1)]
        maximum = float(np.max(values))
        # This second coordinate deterministically resolves large plateaus.
        top_sum = float(np.sum(np.sort(values)[-min(40, len(values)) :]))
        key = (maximum, top_sum)
        if best_key is None or key < best_key:
            best_key = key
            best_keep = keep
        combinations_checked += 1
    if best_keep is None or best_key is None:
        raise AssertionError("deletion enumeration failed")
    return best_keep, {
        "source_size": n,
        "target_size": target,
        "deletion_count": deletion_count,
        "combinations_checked": combinations_checked,
        "pre_reoptimization_maximum": best_key[0],
        "top40_pair_sum_tiebreak": best_key[1],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("portfolio", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    source_payload = json.loads(arguments.portfolio.read_text())
    if not source_payload.get("completed"):
        raise SystemExit("source portfolio is not complete")
    output: dict = {
        "evidence_status": STATUS,
        "source_portfolio_sha256": hashlib.sha256(
            arguments.portfolio.read_bytes()
        ).hexdigest(),
        "interpretation": (
            "exact enumeration of binary64 deletions, followed by numerical "
            "metric and unrestricted refinement; not a certificate"
        ),
        "runs": [],
        "best_by_n": {},
    }
    for target in (41, 42, 43):
        sources = [
            run
            for run in source_payload["structured_runs"]
            if target < run["n"] <= target + 3
        ]
        # Only the best two parents at each larger cardinality are needed to
        # expose the non-monotone local-search artifact.
        retained = []
        for source_size in range(target + 1, 45):
            group = [run for run in sources if run["n"] == source_size]
            group.sort(
                key=lambda run: run["structured_diagnostics"][
                    "maximum_inner_product"
                ]
            )
            retained.extend(group[:2])
        candidates = []
        for source in retained:
            coordinates = np.asarray(
                source["structured_coordinates_float64"], dtype=float
            )
            keep, deletion = best_deletion(coordinates, target)
            candidates.append((deletion["pre_reoptimization_maximum"], source, keep, deletion))
        candidates.sort(key=lambda item: item[0])
        # Reoptimize and release only the two best cross-cardinality children.
        for rank, (_, source, keep, deletion) in enumerate(candidates[:2]):
            roots, labels = root_shell(source["family"])
            parent_indices = np.asarray(source["selected_root_indices"], dtype=int)
            child_indices = parent_indices[keep]
            matrix = np.asarray(source["map_float64"], dtype=float)
            matrix, metric_history = optimize_metric(
                roots,
                child_indices,
                matrix,
                betas=(120.0, 480.0, 1920.0, 7680.0),
                iterations=700,
            )
            structured = mapped_points(roots[child_indices], matrix)
            released, smooth_history = unrestricted_refine(structured)
            sqp_coordinates, sqp = epigraph_slsqp(released)
            if (
                diagnostics(sqp_coordinates)["maximum_inner_product"]
                <= diagnostics(released)["maximum_inner_product"] + 2e-10
            ):
                final = sqp_coordinates
                endpoint = "epigraph_slsqp"
            else:
                final = released
                endpoint = "smooth_continuation"
            run = {
                "target_n": target,
                "rank": rank,
                "source_n": source["n"],
                "source_family": source["family"],
                "source_seed": source["seed"],
                "deletion_audit": deletion,
                "child_root_indices": child_indices.tolist(),
                "child_root_labels": [
                    labels[int(index)] for index in child_indices
                ],
                "reoptimized_map_float64": matrix.tolist(),
                "metric_history": metric_history,
                "structured_diagnostics": diagnostics(structured),
                "structured_coordinates_float64": structured.tolist(),
                "smooth_history": smooth_history,
                "epigraph_slsqp": sqp,
                "chosen_endpoint": endpoint,
                "final_diagnostics": diagnostics(final),
                "coordinates_float64": final.tolist(),
            }
            output["runs"].append(run)
            prior = output["best_by_n"].get(str(target))
            value = run["final_diagnostics"]["maximum_inner_product"]
            if prior is None or value < prior["maximum_inner_product"]:
                output["best_by_n"][str(target)] = {
                    "maximum_inner_product": value,
                    "run_index": len(output["runs"]) - 1,
                    "coordinate_little_endian_float64_sha256": run[
                        "final_diagnostics"
                    ]["coordinate_little_endian_float64_sha256"],
                }
    output["completed"] = True
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n"
    )


if __name__ == "__main__":
    main()
