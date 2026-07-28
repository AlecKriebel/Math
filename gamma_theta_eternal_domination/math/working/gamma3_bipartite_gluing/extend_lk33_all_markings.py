#!/usr/bin/env python3
"""Targeted all-markings scan of two-vertex extensions of L(K3,3).

This is a bounded discovery probe, not a coverage theorem for all graphs.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "inactive_bipartite_gluing"
_EXT_SPEC = importlib.util.spec_from_file_location(
    "gamma3_lk33_extension", HERE / "extend_lk33.py"
)
if _EXT_SPEC is None or _EXT_SPEC.loader is None:
    raise RuntimeError("cannot load extend_lk33.py")
ext = importlib.util.module_from_spec(_EXT_SPEC)
_EXT_SPEC.loader.exec_module(ext)
base = ext.base
layers = ext.layers


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=600.0)
    parser.add_argument(
        "--output", type=Path, default=HERE / "lk33_all_markings_result.json"
    )
    args = parser.parse_args()
    started = time.monotonic()
    counts = {
        "extensions": 0,
        "common_neighbor": 0,
        "three_colorable": 0,
        "markings": 0,
        "bipartite_R": 0,
        "R_total_dominating": 0,
        "full_root": 0,
        "color_obstruction": 0,
        "successors": 0,
    }
    witness = None
    timed_out = False
    for mask9 in range(1 << 9):
        if time.monotonic() - started > args.seconds:
            timed_out = True
            break
        for mask10 in range(1 << 9):
            for adjacent in (False, True):
                counts["extensions"] += 1
                adjacency = ext.extend(mask9, mask10, adjacent)
                if not base.every_pair_has_common_neighbor(adjacency):
                    continue
                counts["common_neighbor"] += 1
                if not base.is_three_colorable(adjacency):
                    continue
                counts["three_colorable"] += 1
                facets = base.triangles(adjacency)
                classes = base.covariance_classes(adjacency)
                universe = (1 << 11) - 1
                for selection in range(1 << len(classes)):
                    counts["markings"] += 1
                    inactive = 0
                    for index, block in enumerate(classes):
                        if selection & (1 << index):
                            inactive |= block
                    active = universe ^ inactive
                    if not base.is_bipartite_induced(adjacency, inactive):
                        continue
                    counts["bipartite_R"] += 1
                    if not ext.total_dominates(adjacency, inactive):
                        continue
                    counts["R_total_dominating"] += 1
                    full = [facet for facet in facets if not (facet & inactive)]
                    if not full:
                        continue
                    counts["full_root"] += 1
                    whole_h, guard = layers.target_extension(adjacency, inactive)
                    if base.is_three_colorable(whole_h):
                        continue
                    counts["color_obstruction"] += 1
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
                        "active_A": list(base.vertices(active)),
                        "inactive_R_equals_N_H_x": list(base.vertices(inactive)),
                        "full_active_root": list(base.vertices(full[0])),
                        "new_neighborhood_masks": [mask9, mask10],
                        "new_vertices_adjacent": adjacent,
                        "colorings": base.proper_three_coloring_partitions(
                            adjacency
                        ),
                        "covariance_classes": [
                            list(base.vertices(block)) for block in classes
                        ],
                        "H_with_target_graph6_labeled": layers.graph6(whole_h),
                        "G_with_target_graph6_labeled": layers.graph6(guard),
                    }
                    break
                if witness is not None:
                    break
            if witness is not None:
                break
        if witness is not None:
            break

    payload = {
        "schema": "gamma3-bipartite-gluing-lk33-all-markings-probe-v1",
        "claim_status": "OBSERVED",
        "scope": (
            "lexicographic two-vertex-extension prefix of HEhbtjK through "
            "the first witness, with the old graph induced and every exact "
            "ridge-covariance class-union marking tested on each row"
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
