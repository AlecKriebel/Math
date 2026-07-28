#!/usr/bin/env python3
"""Targeted discovery scan of the existing edge-toggle candidate database.

This is not an exhaustive universe generator and its negative outcome is not
a finite theorem.  It only asks whether one of the already generated graphs
with (gamma, alpha, theta) = (3, 3, 4) has a target deletion satisfying the
static C-108 gluing hypotheses with the physical inactive set N_H(x).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sqlite3
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[2]
SOURCE = CAMPAIGN / "math" / "working" / "inactive_bipartite_gluing"

_BASE_SPEC = importlib.util.spec_from_file_location(
    "inactive_bipartite_search_static", SOURCE / "search_static.py"
)
if _BASE_SPEC is None or _BASE_SPEC.loader is None:
    raise RuntimeError("cannot load search_static.py")
base = importlib.util.module_from_spec(_BASE_SPEC)
_BASE_SPEC.loader.exec_module(base)

_LAYER_SPEC = importlib.util.spec_from_file_location(
    "inactive_bipartite_search_layers", SOURCE / "search_layers.py"
)
if _LAYER_SPEC is None or _LAYER_SPEC.loader is None:
    raise RuntimeError("cannot load search_layers.py")
layers = importlib.util.module_from_spec(_LAYER_SPEC)
_LAYER_SPEC.loader.exec_module(layers)


def delete_vertex(adjacency: tuple[int, ...], target: int) -> tuple[int, ...]:
    keep = [vertex for vertex in range(len(adjacency)) if vertex != target]
    relabel = {old: new for new, old in enumerate(keep)}
    rows = [0 for _ in keep]
    for old_u in keep:
        new_u = relabel[old_u]
        for old_v in keep:
            if adjacency[old_u] & (1 << old_v):
                rows[new_u] |= 1 << relabel[old_v]
    return tuple(rows)


def relabeled_mask(mask: int, target: int, order: int) -> int:
    answer = 0
    for old in range(order):
        if old == target or not (mask & (1 << old)):
            continue
        new = old if old < target else old - 1
        answer |= 1 << new
    return answer


def marking_is_covariant(adjacency: tuple[int, ...], inactive: int) -> bool:
    for block in base.covariance_classes(adjacency):
        if block & inactive and block & ~inactive:
            return False
    return True


def analyze(
    record: str,
    *,
    allow_dynamically_inactive_neighbors: bool,
) -> dict[str, object] | None:
    guard = base.decode_graph6(record)
    whole_h = layers.complement(guard)
    if not base.every_pair_has_common_neighbor(whole_h):
        return None
    if base.is_three_colorable(whole_h):
        return None
    order = len(guard)
    for target in range(order):
        h_prime = delete_vertex(whole_h, target)
        if not base.every_pair_has_common_neighbor(h_prime):
            continue
        if not base.is_three_colorable(h_prime):
            continue
        facets = base.triangles(h_prime)
        if not facets:
            continue
        old_complement_neighbors = whole_h[target]
        complement_neighbors = relabeled_mask(
            old_complement_neighbors, target, order
        )
        all_deletion = (1 << (order - 1)) - 1
        classes = base.covariance_classes(h_prime)
        forced_inactive = 0
        optional: list[int] = []
        for block in classes:
            if block & complement_neighbors:
                forced_inactive |= block
            else:
                optional.append(block)
        selections = (
            range(1 << len(optional))
            if allow_dynamically_inactive_neighbors
            else range(1)
        )
        for selection in selections:
            inactive = forced_inactive
            if allow_dynamically_inactive_neighbors:
                for index, block in enumerate(optional):
                    if selection & (1 << index):
                        inactive |= block
            active = all_deletion ^ inactive
            if not base.is_bipartite_induced(h_prime, inactive):
                continue
            if not marking_is_covariant(h_prime, inactive):
                raise AssertionError("class-union marking lost covariance")
            full = [facet for facet in facets if not (facet & inactive)]
            if not full:
                continue
            # Rebuild with the physical complement neighborhood B=N_H(x),
            # which may be a strict subset of the family-inactive set R.
            rebuilt_h, rebuilt_g = layers.target_extension(
                h_prime, complement_neighbors
            )
            if not base.every_pair_has_common_neighbor(rebuilt_h):
                raise AssertionError(
                    "database gamma=3 row failed common-neighbor check"
                )
            if not layers.static_successors_dominate(
                rebuilt_g, facets, active, len(h_prime)
            ):
                continue
            if base.is_three_colorable(rebuilt_h):
                raise AssertionError("database theta=4 row became three-colorable")
            partitions = base.proper_three_coloring_partitions(h_prime)
            return {
                "status": "OBSERVED_EXACT_STATIC_COUNTERMODEL",
                "source_guard_graph6_canonical": record,
                "order_of_target_extension": order,
                "target_in_source_labeling": target,
                "H_prime_graph6_labeled": layers.graph6(h_prime),
                "H_with_target_graph6_labeled": layers.graph6(rebuilt_h),
                "G_with_target_graph6_labeled": layers.graph6(rebuilt_g),
                "active_A": list(base.vertices(active)),
                "inactive_R": list(base.vertices(inactive)),
                "physical_N_H_x": list(base.vertices(complement_neighbors)),
                "full_active_root": list(base.vertices(full[0])),
                "covariance_classes": [
                    list(base.vertices(block)) for block in classes
                ],
                "three_coloring_partitions": partitions,
            }
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--database",
        type=Path,
        default=CAMPAIGN / "results" / "checkpoints" / "edge_toggles.sqlite3",
    )
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument("--limit", type=int, default=8587)
    parser.add_argument(
        "--allow-dynamically-inactive-neighbors",
        action="store_true",
        help="allow R to strictly contain the physical complement neighborhood",
    )
    parser.add_argument(
        "--graph6",
        action="append",
        default=[],
        help="scan this explicit guard graph instead of the database",
    )
    parser.add_argument("--output", type=Path, default=HERE / "scan_result.json")
    args = parser.parse_args()

    started = time.monotonic()
    checked = 0
    witness = None
    if args.graph6:
        records = ((record,) for record in args.graph6)
        for (record,) in records:
            checked += 1
            witness = analyze(
                record,
                allow_dynamically_inactive_neighbors=(
                    args.allow_dynamically_inactive_neighbors
                ),
            )
            if witness is not None:
                break
    else:
        with sqlite3.connect(args.database) as connection:
            columns = {
                row[1]
                for row in connection.execute(
                    "PRAGMA table_info(canonical_graphs)"
                )
            }
            if {"gamma_a", "alpha_a", "theta_a"} <= columns:
                query = """
                    SELECT graph6
                    FROM canonical_graphs
                    WHERE gamma_a = 3 AND alpha_a = 3 AND theta_a = 4
                    ORDER BY graph6
                    LIMIT ?
                """
            elif {"gamma", "alpha"} <= columns:
                query = """
                    SELECT graph6
                    FROM canonical_graphs
                    WHERE gamma = 3 AND alpha = 3
                    ORDER BY graph6
                    LIMIT ?
                """
            else:
                raise RuntimeError("unrecognized candidate database schema")
            cursor = connection.execute(query, (args.limit,))
            for (record,) in cursor:
                if time.monotonic() - started > args.seconds:
                    break
                checked += 1
                witness = analyze(
                    record,
                    allow_dynamically_inactive_neighbors=(
                        args.allow_dynamically_inactive_neighbors
                    ),
                )
                if witness is not None:
                    break
            cursor.close()

    payload = {
        "schema": "gamma3-bipartite-gluing-targeted-scan-v1",
        "claim_status": "OBSERVED",
        "source_scope": (
            "explicit graph6 inputs"
            if args.graph6
            else f"existing candidate database only: {args.database}"
        ),
        "rows_checked": checked,
        "wall_seconds": time.monotonic() - started,
        "time_cap_seconds": args.seconds,
        "allow_dynamically_inactive_neighbors": (
            args.allow_dynamically_inactive_neighbors
        ),
        "witness": witness,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
