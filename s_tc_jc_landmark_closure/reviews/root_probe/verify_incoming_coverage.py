#!/usr/bin/env python3
"""Clean-room audit of a fixed structural INCOMING role on both factors.

This verifier imports only the independent graph definitions in this review
directory.  It computes real pendant-boundary rootability from the narrow
rooting definition, then exhausts every boundary bijection between alternate
minimal supports of the same size.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import FrozenSet

from verify_root_probe import (
    EventCore,
    MixedGraph,
    canonical_json_bytes,
    derive_cycle_event_core,
    derive_theta_event_cores,
    enumerate_rootings,
    graph_from_core,
    local_tail_criterion,
    powerset,
    sha256_bytes,
)


def minimum_repairs(core: EventCore) -> tuple[FrozenSet[str], ...]:
    segment_ids = sorted(segment.id for segment in core.segments)
    satisfying = []
    for occupied in powerset(segment_ids):
        graph = graph_from_core(core, occupied)
        if graph is not None and graph.is_binary_shape() and local_tail_criterion(graph):
            satisfying.append(occupied)
    return tuple(sorted(
        (row for row in satisfying if not any(other < row for other in satisfying)),
        key=lambda row: (len(row), sorted(row)),
    ))


def pendant_edges(graph: MixedGraph) -> dict[str, tuple[str, str]]:
    answer = {}
    for node, data in graph.nodes.items():
        if not data.leaf:
            continue
        incident = [edge for edge in graph.edges if node in edge]
        if len(incident) != 1 or data.label is None:
            raise AssertionError((node, incident))
        answer[data.label] = incident[0]
    return answer


def support_record(core: EventCore, repair: FrozenSet[str]) -> dict:
    graph = graph_from_core(core, repair)
    if graph is None:
        raise AssertionError("minimum repair produced no graph")
    rootings = enumerate_rootings(graph)
    if not rootings or not all(rooting.tree_child for rooting in rootings):
        raise AssertionError("minimum support is not standard-strong")
    boundary_edges = pendant_edges(graph)
    rootable = sorted(
        label
        for label, edge in boundary_edges.items()
        if any(rooting.site == edge for rooting in rootings)
    )
    graph_record = graph.record()
    return {
        "support_id": f"{core.family}:{core.placement}:{','.join(sorted(repair))}",
        "family": core.family,
        "placement": core.placement,
        "repair": sorted(repair),
        "boundary_labels": sorted(boundary_edges),
        "rootable_boundary_labels": rootable,
        "nonrootable_boundary_labels": sorted(set(boundary_edges) - set(rootable)),
        "admissible_rooting_count": len(rootings),
        "tree_child_rooting_count": sum(rooting.tree_child for rooting in rootings),
        "pendant_rooting_sites": {
            label: list(edge) for label, edge in sorted(boundary_edges.items())
        },
        "admissible_pendant_rootings": [
            rooting.record() for rooting in rootings
            if rooting.site in set(boundary_edges.values())
        ],
        "mixed_graph": graph_record,
        "mixed_graph_sha256": sha256_bytes(canonical_json_bytes(graph_record)),
    }


def common_rootable(source: dict, target: dict, permutation: tuple[str, ...]) -> list[str]:
    source_labels = source["boundary_labels"]
    matching = dict(zip(source_labels, permutation))
    source_rootable = set(source["rootable_boundary_labels"])
    target_rootable = set(target["rootable_boundary_labels"])
    return sorted(label for label in source_rootable if matching[label] in target_rootable)


def exact_counterexample(supports: list[dict]) -> dict:
    source = next(
        row for row in supports
        if row["family"] == "TT"
        and row["placement"] == "nested"
        and row["repair"] == ["p0e2"]
    )
    roles = source["boundary_labels"]
    role_to_physical_source = {
        "incoming": "A",
        "repair:p0e2": "B",
        "sink:X1": "C",
        "sink:X2": "D",
    }
    role_to_physical_target = {
        "incoming": "C",
        "repair:p0e2": "D",
        "sink:X1": "A",
        "sink:X2": "B",
    }
    source_rootable_physical = sorted(
        role_to_physical_source[label] for label in source["rootable_boundary_labels"]
    )
    target_rootable_physical = sorted(
        role_to_physical_target[label] for label in source["rootable_boundary_labels"]
    )
    target_role_for_physical = {
        physical: role for role, physical in role_to_physical_target.items()
    }
    relative_target_roles = tuple(
        target_role_for_physical[role_to_physical_source[source_role]]
        for source_role in roles
    )
    intersection = sorted(set(source_rootable_physical) & set(target_rootable_physical))
    if intersection:
        raise AssertionError(intersection)
    if relative_target_roles[roles.index("incoming")] == "incoming":
        raise AssertionError("counterexample unexpectedly fixes incoming")
    return {
        "schema": "fixed-incoming-counterexample-v1",
        "claim_refuted": (
            "Individual real-boundary root reduction supplies a common admissible "
            "incoming boundary for every fixed physical port matching."
        ),
        "core": "TT:nested",
        "minimum_repair": source["repair"],
        "mixed_graph": source["mixed_graph"],
        "mixed_graph_sha256": source["mixed_graph_sha256"],
        "source_role_to_physical_label": role_to_physical_source,
        "target_role_to_physical_label": role_to_physical_target,
        "source_rootable_physical_labels": source_rootable_physical,
        "target_rootable_physical_labels": target_rootable_physical,
        "common_rootable_physical_labels": intersection,
        "source_role_order": roles,
        "target_roles_matched_to_source_role_order": list(relative_target_roles),
        "relative_target_permutation_indices": [roles.index(role) for role in relative_target_roles],
        "relative_permutation_fixes_structural_incoming": (
            relative_target_roles[roles.index("incoming")] == "incoming"
        ),
        "outgoing_only_target_orbit_size": 6,
        "full_target_orbit_size": 24,
        "explanation": (
            "Both labelled factors use the same standard-strong mixed graph. "
            "In the source, physical A and B occupy the two rootable roles; "
            "in the target, physical C and D occupy them.  Identity matching "
            "of physical labels has no boundary rootable on both sides.  The "
            "required relative target permutation moves the structural incoming "
            "position and is absent from the subgroup permuting only outgoing ports."
        ),
    }


def audit() -> tuple[dict, dict]:
    cores = [derive_cycle_event_core(), *derive_theta_event_cores()]
    supports = [
        support_record(core, repair)
        for core in cores
        for repair in minimum_repairs(core)
    ]
    counts = Counter()
    counts_by_boundary_size = Counter()
    no_common_by_support_pair = Counter()
    failures = []
    for source in supports:
        for target in supports:
            if len(source["boundary_labels"]) != len(target["boundary_labels"]):
                continue
            for permutation in itertools.permutations(target["boundary_labels"]):
                boundary_size = len(source["boundary_labels"])
                counts["ordered_support_boundary_bijections"] += 1
                counts_by_boundary_size[f"{boundary_size}:all"] += 1
                common = common_rootable(source, target, permutation)
                if common:
                    counts["bijections_with_common_rootable_boundary"] += 1
                    counts_by_boundary_size[f"{boundary_size}:with_common"] += 1
                else:
                    counts["bijections_without_common_rootable_boundary"] += 1
                    counts_by_boundary_size[f"{boundary_size}:without_common"] += 1
                    no_common_by_support_pair[
                        f"{source['support_id']} -> {target['support_id']}"
                    ] += 1
                    failures.append({
                        "source_support_id": source["support_id"],
                        "target_support_id": target["support_id"],
                        "source_boundary_order": source["boundary_labels"],
                        "target_labels_matched_to_source_order": list(permutation),
                    })
    counterexample = exact_counterexample(supports)
    full_relative = set(itertools.permutations(range(4)))
    fixed_incoming = {row for row in full_relative if row[0] == 0}
    witness = tuple(counterexample["relative_target_permutation_indices"])
    payload = {
        "schema": "incoming-role-coverage-clean-room-v1",
        "support_count": len(supports),
        "supports": supports,
        "boundary_bijection_counts": dict(sorted(counts.items())),
        "boundary_bijection_counts_by_boundary_size": dict(sorted(counts_by_boundary_size.items())),
        "no_common_bijections_by_ordered_support_pair": dict(sorted(no_common_by_support_pair.items())),
        "no_common_rootable_examples": failures[:20],
        "counterexample": counterexample,
        "group_action_check": {
            "degree": 4,
            "full_relative_permutation_count": len(full_relative),
            "fixed_incoming_subgroup_count": len(fixed_incoming),
            "counterexample_relative_permutation": list(witness),
            "counterexample_in_full_group": witness in full_relative,
            "counterexample_in_fixed_incoming_subgroup": witness in fixed_incoming,
        },
        "verdicts": {
            "individual_rootability_implies_common_rootability": "FALSE",
            "fixed_incoming_outgoing_only_quotient_exhaustive": "FALSE",
            "anchored_source_full_target_boundary_permutations_exhaustive": "VERIFIED",
        },
    }
    return payload, counterexample


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("incoming_coverage_certificate.json"))
    parser.add_argument(
        "--counterexample-output",
        type=Path,
        default=Path("counterexamples/fixed_incoming_relative_role.json"),
    )
    args = parser.parse_args()
    payload, counterexample = audit()
    args.output.write_bytes(canonical_json_bytes(payload))
    args.counterexample_output.parent.mkdir(parents=True, exist_ok=True)
    args.counterexample_output.write_bytes(canonical_json_bytes(counterexample))
    print(json.dumps({
        "output": str(args.output),
        "output_sha256": sha256_bytes(canonical_json_bytes(payload)),
        "counterexample_output": str(args.counterexample_output),
        "counterexample_sha256": sha256_bytes(canonical_json_bytes(counterexample)),
        "counts": payload["boundary_bijection_counts"],
        "verdicts": payload["verdicts"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
