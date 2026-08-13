#!/usr/bin/env python3
"""Independent n=4 coverage challenge for the n=3 hard-cover claim.

The hard-cover producer starts only from n=3 rigid source supports.  The
theta-2 core has minimum rigid outgoing support four.  This verifier rebuilds
the n=3 and n=4 fixed-root inventories from primitive graphs, exhibits one
exact n=4 theta-2/nonretaining-target relation, and proves that no deletion of
one of its five selected boundaries is an n=3 hard-cover source support.

No module under ``primary`` is imported.  The supplied descriptor-bit cache is
used only to enumerate the finite candidate inventory.  Every bit used by the
reported witness relation is then recomputed from exact polynomial pullbacks.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, permutations
import argparse
import hashlib
import json
from pathlib import Path
import time

from audit_hard_cover import (
    CORE_PATH,
    INVARIANT_PATH,
    PROJECT,
    Variant,
    build_inventory,
    file_sha,
)
from cleanroom_core import (
    RootedGraph,
    canonical_mixed,
    class_audit,
    descriptor_bits_exact,
    invariant_orbit,
    quartet_descriptor,
    relabel,
    sd0,
    stable_hash,
    t_quotient,
)


HERE = Path(__file__).resolve().parent


def physical_graph(variant: Variant, assignment: tuple[int, ...]) -> RootedGraph:
    return relabel(
        variant.graph,
        {
            label: f"L_{actual}"
            for label, actual in zip(variant.labels, assignment)
        },
    )


def graph_payload(graph: RootedGraph) -> dict:
    mixed = sd0(graph)
    mixed_code, transport = canonical_mixed(mixed)
    t_code, _ = canonical_mixed(t_quotient(mixed))
    return {
        "root": graph.root,
        "labels": graph.labels,
        "arcs": graph.arcs,
        "class_audit": class_audit(graph),
        "standard_mixed_code": mixed_code,
        "standard_mixed_code_sha256": hashlib.sha256(mixed_code.encode()).hexdigest(),
        "t_quotient_code": t_code,
        "t_quotient_code_sha256": hashlib.sha256(t_code.encode()).hexdigest(),
        "raw_mixed_vertex_to_canonical": tuple(sorted(transport.items())),
    }


def exact_signature(graph: RootedGraph, labels: tuple[str, ...], invariants) -> dict:
    rows = []
    signature = 0
    for chunk, quartet in enumerate(combinations(range(len(labels)), 4)):
        descriptor = quartet_descriptor(graph, labels, quartet)
        bits = descriptor_bits_exact(descriptor, invariants)
        signature |= bits << (len(invariants) * chunk)
        rows.append({
            "chunk": chunk,
            "physical_positions": quartet,
            "descriptor": descriptor,
            "descriptor_sha256": stable_hash(descriptor),
            "invariant_bits": str(bits),
        })
    return {
        "signature": str(signature),
        "signature_sha256": hashlib.sha256(str(signature).encode()).hexdigest(),
        "quartets": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "n4_coverage_gap_certificate.json")
    args = parser.parse_args()
    started = time.monotonic()

    # The finite inventory uses a previously materialized bit index only to
    # locate candidates.  The chosen relation is checked exactly below.
    inv3 = build_inventory(selected_outgoing=3, recompute_all_descriptor_bits=False)
    inv4 = build_inventory(selected_outgoing=4, recompute_all_descriptor_bits=False)
    invariants = invariant_orbit(json.loads(INVARIANT_PATH.read_text()))

    n3_source_core_counts = Counter(v.core_id for v in inv3.sources.values())
    theta2_root_ids = tuple(sorted(
        root_id
        for root_id, root in inv4.root_cases.items()
        if inv4.sources[root["source_primitive_id"]].core_id == "theta-2"
    ))
    if not theta2_root_ids:
        raise AssertionError("independent n=4 inventory has no theta-2 root")
    witness_root_id = theta2_root_ids[0]
    root = inv4.root_cases[witness_root_id]
    source_variant = inv4.sources[root["source_primitive_id"]]
    target_variant = inv4.targets[root["target_primitive_id"]]
    source_assignment = tuple(root["source_position_to_label"])
    target_assignment = tuple(root["target_position_to_label"])
    source_graph = physical_graph(source_variant, source_assignment)
    target_graph = physical_graph(target_variant, target_assignment)

    physical_labels = tuple(f"L_{index}" for index in range(5))
    source_exact = exact_signature(source_graph, physical_labels, invariants)
    target_exact = exact_signature(target_graph, physical_labels, invariants)
    if source_exact["signature"] != target_exact["signature"]:
        raise AssertionError("chosen n=4 relation is not an exact common invariant-deck root")
    if source_exact["signature_sha256"] != root["selected_signature_sha256"]:
        raise AssertionError("chosen n=4 relation signature is not bound to its root key")

    # Compile every ordered n=3 rigid-support descriptor independently.
    n3_descriptors: dict[tuple, list[dict]] = defaultdict(list)
    for variant in inv3.sources.values():
        for order in permutations(range(4)):
            descriptor = quartet_descriptor(variant.graph, variant.labels, order)
            n3_descriptors[descriptor].append({
                "core_id": variant.core_id,
                "primitive_id": variant.primitive_id,
                "order": order,
            })

    deletion_rows = []
    total_matches = 0
    for omitted in range(5):
        retained = tuple(index for index in range(5) if index != omitted)
        ordered_rows = []
        match_count = 0
        matching_cores = Counter()
        descriptor_hashes = set()
        for order in permutations(retained):
            descriptor = quartet_descriptor(source_graph, physical_labels, order)
            descriptor_hashes.add(stable_hash(descriptor))
            matches = n3_descriptors.get(descriptor, ())
            match_count += len(matches)
            matching_cores.update(row["core_id"] for row in matches)
            ordered_rows.append({
                "order": order,
                "descriptor_sha256": stable_hash(descriptor),
                "n3_match_count": len(matches),
            })
        total_matches += match_count
        deletion_rows.append({
            "omitted_position": omitted,
            "omitted_label": physical_labels[omitted],
            "ordered_descriptor_count": len(ordered_rows),
            "distinct_descriptor_hashes": sorted(descriptor_hashes),
            "n3_support_match_count": match_count,
            "matching_n3_core_counts": dict(sorted(matching_cores.items())),
            "ordered_checks": ordered_rows,
        })

    # Every n=3 restoration path inserts labelled subdivisions into the fixed
    # primitive source core from its root coverage; it never changes that core.
    # theta-2 is absent from the complete n=3 source inventory, so no such path
    # can reach this fixed source.  The exhaustive deletion test above is a
    # second, tensor-descriptor-level obstruction to choosing an n=3 anchor.
    path_reduction = {
        "n3_source_core_counts": dict(sorted(n3_source_core_counts.items())),
        "theta_2_present_in_n3_source_inventory": n3_source_core_counts["theta-2"] > 0,
        "restoration_operation": "insert one labelled port-bearing subdivision on an edge of the fixed source primitive",
        "restoration_preserves_primitive_core": True,
        "all_five_boundary_deletions_checked": len(deletion_rows) == 5,
        "ordered_checks_per_deletion": 24,
        "total_n3_support_descriptor_matches": total_matches,
        "reduces_to_n3_path": False,
        "reason": (
            "theta-2 is absent from the exhaustive n=3 rigid-source inventory; "
            "source restoration preserves the primitive core; and all 5*24 "
            "ordered four-boundary marginal descriptors have zero matches among "
            "all 8*24 ordered n=3 rigid-source descriptors"
        ),
    }
    if n3_source_core_counts["theta-2"] or total_matches:
        raise AssertionError("the advertised n=4 obstruction unexpectedly reduces to n=3")

    source_class = class_audit(source_graph)
    target_class = class_audit(target_graph)
    required_class_keys = (
        "rooted_valid", "root_is_lsa", "rooted_tree_child",
        "standard_strong_local", "level_at_most_two",
    )
    if not all(source_class.get(key) for key in required_class_keys):
        raise AssertionError(("source not in locked class", source_class))
    if not all(target_class.get(key) for key in required_class_keys):
        raise AssertionError(("target completion not in locked class", target_class))
    if target_variant.retains_core:
        raise AssertionError("target was required to be nonretaining")

    theta2_by_target = Counter()
    for root_id in theta2_root_ids:
        row = inv4.root_cases[root_id]
        target = inv4.targets[row["target_primitive_id"]]
        theta2_by_target[(target.core_id, target.incoming_selected)] += 1

    payload = {
        "schema": "n4-hard-cover-gap-clean-room-v1",
        "status": "FALSE",
        "finding": (
            "The n=3 hard-cover is not exhaustive: an exact n=4 fixed-full "
            "theta-2/nonretaining-target relation exists and cannot be reached "
            "from any n=3 restoration path."
        ),
        "independence": "imports no primary implementation and rebuilds primitive graphs, descriptors, and signatures",
        "input_hashes": {
            str(CORE_PATH.relative_to(PROJECT)): file_sha(CORE_PATH),
            str(INVARIANT_PATH.relative_to(PROJECT)): file_sha(INVARIANT_PATH),
        },
        "inventories": {
            "n3": {
                "sources": len(inv3.sources),
                "targets": len(inv3.targets),
                "source_signatures": inv3.source_signature_count,
                "target_signatures": inv3.target_signature_count,
                "common_signatures": inv3.common_signature_count,
                "fixed_root_cases": len(inv3.root_cases),
                "source_core_counts": dict(sorted(n3_source_core_counts.items())),
            },
            "n4": {
                "sources": len(inv4.sources),
                "targets": len(inv4.targets),
                "source_signatures": inv4.source_signature_count,
                "target_signatures": inv4.target_signature_count,
                "common_signatures": inv4.common_signature_count,
                "fixed_root_cases": len(inv4.root_cases),
                "theta2_fixed_root_cases": len(theta2_root_ids),
                "theta2_target_core_and_incoming_counts": {
                    f"{core}|incoming_selected={incoming}": count
                    for (core, incoming), count in sorted(theta2_by_target.items())
                },
            },
        },
        "witness": {
            "root_case_id": witness_root_id,
            "root_key": root,
            "root_key_sha256": stable_hash(root),
            "source_provenance": source_variant.provenance,
            "target_provenance": target_variant.provenance,
            "target_retains_core": target_variant.retains_core,
            "source_graph": graph_payload(source_graph),
            "target_full_completion_graph": graph_payload(target_graph),
            "source_exact_invariant_deck": source_exact,
            "target_exact_invariant_deck": target_exact,
        },
        "n3_path_reduction_audit": path_reduction,
        "deletion_checks": deletion_rows,
        "elapsed_seconds": time.monotonic() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "n4_roots": len(inv4.root_cases),
        "theta2_roots": len(theta2_root_ids),
        "n3_descriptor_matches": total_matches,
        "witness_root": witness_root_id,
        "output": str(args.output),
        "sha256": file_sha(args.output),
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
