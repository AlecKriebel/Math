#!/usr/bin/env python3
"""Bounded two-vertex extension probe around the C-123 L(K3,3) control.

The old graph and old A/R marking are fixed.  Two new inactive vertices are
adjoined with arbitrary old neighborhoods and an optional mutual edge.  The
probe asks for the strengthened static gluing obstruction with R=N_H(x).
Negative output is OBSERVED only.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "inactive_bipartite_gluing"
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


OLD = base.decode_graph6("HEhbtjK")
OLD_R = sum(1 << vertex for vertex in (0, 3, 4, 6))
OLD_A = sum(1 << vertex for vertex in (1, 2, 5, 7, 8))


def extend(mask9: int, mask10: int, adjacent: bool) -> tuple[int, ...]:
    rows = list(OLD) + [0, 0]
    for old in range(9):
        if mask9 & (1 << old):
            rows[old] |= 1 << 9
            rows[9] |= 1 << old
        if mask10 & (1 << old):
            rows[old] |= 1 << 10
            rows[10] |= 1 << old
    if adjacent:
        rows[9] |= 1 << 10
        rows[10] |= 1 << 9
    return tuple(rows)


def covariant(adjacency: tuple[int, ...], inactive: int) -> bool:
    return all(
        not (block & inactive and block & ~inactive)
        for block in base.covariance_classes(adjacency)
    )


def total_dominates(adjacency: tuple[int, ...], subset: int) -> bool:
    return all(adjacency[vertex] & subset for vertex in range(len(adjacency)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument("--output", type=Path, default=HERE / "lk33_result.json")
    args = parser.parse_args()
    started = time.monotonic()
    counts = {
        "extensions": 0,
        "bipartite_R": 0,
        "R_total_dominating": 0,
        "common_neighbor": 0,
        "three_colorable": 0,
        "covariant": 0,
        "successors": 0,
    }
    witness = None
    timed_out = False
    for statuses in ("RR", "RA", "AR"):
        inactive = OLD_R
        active = OLD_A
        if statuses[0] == "R":
            inactive |= 1 << 9
        else:
            active |= 1 << 9
        if statuses[1] == "R":
            inactive |= 1 << 10
        else:
            active |= 1 << 10
        for mask9 in range(1 << 9):
            if time.monotonic() - started > args.seconds:
                timed_out = True
                break
            for mask10 in range(1 << 9):
                for adjacent in (False, True):
                    counts["extensions"] += 1
                    adjacency = extend(mask9, mask10, adjacent)
                    if not base.is_bipartite_induced(adjacency, inactive):
                        continue
                    counts["bipartite_R"] += 1
                    if not total_dominates(adjacency, inactive):
                        continue
                    counts["R_total_dominating"] += 1
                    if not base.every_pair_has_common_neighbor(adjacency):
                        continue
                    counts["common_neighbor"] += 1
                    if not base.is_three_colorable(adjacency):
                        continue
                    counts["three_colorable"] += 1
                    if not covariant(adjacency, inactive):
                        continue
                    counts["covariant"] += 1
                    facets = base.triangles(adjacency)
                    _whole_h, guard = layers.target_extension(
                        adjacency, inactive
                    )
                    if not layers.static_successors_dominate(
                        guard, facets, active, 11
                    ):
                        continue
                    counts["successors"] += 1
                    witness = {
                        "H_prime_graph6_labeled": layers.graph6(adjacency),
                        "H_prime_edges": [
                            [u, v]
                            for u in range(11)
                            for v in range(u + 1, 11)
                            if adjacency[u] & (1 << v)
                        ],
                        "new_statuses": statuses,
                        "active_A": list(base.vertices(active)),
                        "inactive_R_equals_N_H_x": list(base.vertices(inactive)),
                        "full_active_root": [1, 5, 8],
                        "new_neighborhood_masks": [mask9, mask10],
                        "new_vertices_adjacent": adjacent,
                        "colorings": base.proper_three_coloring_partitions(
                            adjacency
                        ),
                        "covariance_classes": [
                            list(base.vertices(block))
                            for block in base.covariance_classes(adjacency)
                        ],
                        "H_with_target_graph6_labeled": layers.graph6(_whole_h),
                        "G_with_target_graph6_labeled": layers.graph6(guard),
                    }
                    break
                if witness is not None:
                    break
            if witness is not None:
                break
        if timed_out or witness is not None:
            break

    payload = {
        "schema": "gamma3-bipartite-gluing-lk33-extension-probe-v1",
        "claim_status": "OBSERVED",
        "scope": (
            "all two-vertex extensions of HEhbtjK with the old graph induced, "
            "old marking fixed, and new status patterns RR, RA, and AR"
        ),
        "time_cap_seconds": args.seconds,
        "timed_out": timed_out,
        "wall_seconds": time.monotonic() - started,
        "counts": counts,
        "witness": witness,
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
