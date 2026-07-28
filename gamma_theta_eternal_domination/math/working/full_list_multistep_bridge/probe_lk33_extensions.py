#!/usr/bin/env python3
"""Bounded discovery probe for the new second-attack condition.

The universe is exactly the 2^19 labeled two-vertex extensions of the fixed
nine-vertex L(K3,3) control.  This is a reproducible family sweep, but its
negative result is reported only as OBSERVED because it is not an
independently audited certificate package and says nothing about graphs
outside this extension family.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "gamma3_bipartite_gluing"
_SPEC = importlib.util.spec_from_file_location(
    "gamma3_lk33_extension", PARENT / "extend_lk33.py"
)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("cannot load the fixed L(K3,3) extension constructor")
extension = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(extension)
base = extension.base
layers = extension.layers


def successor_survives_attacks(
    guard_graph: tuple[int, ...],
    state: int,
    attacks: int,
) -> bool:
    for attack in base.vertices(attacks & ~state):
        if not any(
            layers.dominates(
                guard_graph,
                (state ^ (1 << guard)) | (1 << attack),
            )
            for guard in base.vertices(state & guard_graph[attack])
        ):
            return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    started = time.monotonic()
    counts = {
        "extensions": 0,
        "common_neighbor": 0,
        "three_colorable": 0,
        "covariant_markings": 0,
        "bipartite_R": 0,
        "R_total_dominating": 0,
        "full_root": 0,
        "color_obstruction": 0,
        "all_marked_target_successors_dominate": 0,
        "some_full_root_passes_B_second_attacks": 0,
        "some_full_root_passes_all_second_attacks": 0,
    }
    first_B_witness = None
    first_all_witness = None

    for mask9 in range(1 << 9):
        for mask10 in range(1 << 9):
            for new_vertices_adjacent in (False, True):
                counts["extensions"] += 1
                h_prime = extension.extend(
                    mask9, mask10, new_vertices_adjacent
                )
                if not base.every_pair_has_common_neighbor(h_prime):
                    continue
                counts["common_neighbor"] += 1
                if not base.is_three_colorable(h_prime):
                    continue
                counts["three_colorable"] += 1

                facets = base.triangles(h_prime)
                classes = base.covariance_classes(h_prime)
                universe = (1 << 11) - 1
                for selection in range(1 << len(classes)):
                    counts["covariant_markings"] += 1
                    inactive = 0
                    for index, block in enumerate(classes):
                        if selection & (1 << index):
                            inactive |= block
                    active = universe ^ inactive
                    if not base.is_bipartite_induced(h_prime, inactive):
                        continue
                    counts["bipartite_R"] += 1
                    if not extension.total_dominates(h_prime, inactive):
                        continue
                    counts["R_total_dominating"] += 1

                    roots = [
                        facet for facet in facets if not (facet & inactive)
                    ]
                    if not roots:
                        continue
                    counts["full_root"] += 1

                    h, guard = layers.target_extension(h_prime, inactive)
                    if base.is_three_colorable(h):
                        continue
                    counts["color_obstruction"] += 1
                    if not layers.static_successors_dominate(
                        guard, facets, active, 11
                    ):
                        continue
                    counts["all_marked_target_successors_dominate"] += 1

                    B_passing_roots = []
                    all_passing_roots = []
                    for root in roots:
                        B_passes = True
                        all_passes = True
                        for removed in base.vertices(root):
                            successor = (
                                (root ^ (1 << removed)) | (1 << 11)
                            )
                            B_passes &= successor_survives_attacks(
                                guard, successor, inactive
                            )
                            all_passes &= successor_survives_attacks(
                                guard, successor, (1 << 12) - 1
                            )
                        if B_passes:
                            B_passing_roots.append(root)
                        if all_passes:
                            all_passing_roots.append(root)

                    witness_base = {
                        "new_neighborhood_masks": [mask9, mask10],
                        "new_vertices_adjacent": new_vertices_adjacent,
                        "H_prime_graph6_labeled": layers.graph6(h_prime),
                        "inactive_R_equals_B": list(
                            base.vertices(inactive)
                        ),
                    }
                    if B_passing_roots:
                        counts[
                            "some_full_root_passes_B_second_attacks"
                        ] += 1
                        if first_B_witness is None:
                            first_B_witness = {
                                **witness_base,
                                "root": list(
                                    base.vertices(B_passing_roots[0])
                                ),
                            }
                    if all_passing_roots:
                        counts[
                            "some_full_root_passes_all_second_attacks"
                        ] += 1
                        if first_all_witness is None:
                            first_all_witness = {
                                **witness_base,
                                "root": list(
                                    base.vertices(all_passing_roots[0])
                                ),
                            }

    result = {
        "schema": "full-list-multistep-lk33-probe-v1",
        "claim_status": "OBSERVED",
        "scope": {
            "base_graph": "H'=L(K3,3), graph6 HEhbtjK",
            "extension": (
                "all labeled two-vertex extensions, including the optional "
                "edge between the new vertices"
            ),
            "extension_count": 1 << 19,
            "all_exact_ridge_covariance_class_union_markings": True,
            "independent_certificate_claimed": False,
            "universal_coverage_claimed": False,
        },
        "counts": counts,
        "first_B_second_attack_witness": first_B_witness,
        "first_all_second_attack_witness": first_all_witness,
        "wall_seconds": time.monotonic() - started,
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()

