#!/usr/bin/env python3
"""Adversarial finite check of dummy completions versus red_* restrictions."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Dict, FrozenSet, Mapping, Sequence, Tuple

from verify_parameter_submersion import (
    build_completion,
    core_rows,
    source_and_sinks,
    switching_signatures,
)
from verify_root_probe import canonical_json_bytes, sha256_bytes


def ordered_distributions(labels: Sequence[str], segment_count: int):
    for assignment in itertools.product(range(segment_count), repeat=len(labels)):
        buckets = [[] for _ in range(segment_count)]
        for label, segment in zip(labels, assignment):
            buckets[segment].append(label)
        choices = [tuple(itertools.permutations(row)) if row else ((),) for row in buckets]
        for words in itertools.product(*choices):
            yield tuple(tuple(row) for row in words)


def relabel_signature_rows(
    signature: dict,
    old_labels: Sequence[str],
    new_labels: Sequence[str],
    label_map: Mapping[str, str],
) -> Tuple[Tuple[int, ...], ...]:
    old_index = {label: i for i, label in enumerate(old_labels)}
    new_index = {label: i for i, label in enumerate(new_labels)}
    rows = []
    for row in signature["signature_rows"]:
        moved_row = []
        for mask in row:
            moved = 0
            for old_label, target_label in label_map.items():
                if mask & (1 << old_index[old_label]):
                    moved |= 1 << new_index[target_label]
            moved_row.append(moved)
        rows.append(tuple(moved_row))
    return tuple(sorted(set(rows)))


def selected_reticulation_count(graph: dict) -> int:
    arcs = graph["arcs"]
    parents: Dict[str, list[str]] = defaultdict(list)
    indeg = Counter(v for _, v in arcs)
    for u, v in arcs:
        parents[v].append(u)
    selected_leaves = {
        leaf for leaf, label in graph["labels"].items()
        if label in set(graph["selected_labels"])
    }
    ancestors = set(selected_leaves)
    queue = deque(selected_leaves)
    while queue:
        node = queue.popleft()
        for parent in parents[node]:
            if parent not in ancestors:
                ancestors.add(parent)
                queue.append(parent)
    return sum(indeg[node] == 2 for node in ancestors)


def restriction_descriptor_check(
    core: dict,
    full_words: Sequence[Sequence[str]],
    selected: FrozenSet[str],
    repair_index: int,
    repair: Sequence[int],
    *,
    incoming_selected: bool,
) -> dict:
    source, sinks = source_and_sinks(core["arcs"])
    all_sink_mask = (1 << len(sinks)) - 1
    full_counts = tuple(len(row) for row in full_words)
    full = build_completion(
        core,
        sum(full_counts) + len(sinks),
        all_sink_mask,
        full_counts,
        None,
        (),
    )
    generated_to_actual = {}
    generated_cursor = 0
    for row in full_words:
        for actual_label in row:
            generated_to_actual[f"O_{generated_cursor}"] = actual_label
            generated_cursor += 1
    full["labels"] = {
        leaf: generated_to_actual.get(label, label)
        for leaf, label in full["labels"].items()
    }
    # build_completion names ordinary labels in segment order.  Replace its
    # selected list by the actual restriction while retaining omitted leaves
    # as zero-character leaves.
    full["selected_labels"] = tuple(sorted(
        ({"INCOMING", *selected} if incoming_selected else set(selected))
    ))

    selected_sink_mask = 0
    for i, _sink in enumerate(sinks):
        if f"SINK_{i}" in selected:
            selected_sink_mask |= 1 << i
    selected_words = []
    selected_ordinary_in_order = []
    for row in full_words:
        kept = []
        for label in row:
            if label in selected:
                kept.append(label)
                selected_ordinary_in_order.append(label)
        selected_words.append(tuple(kept))
    selected_counts = tuple(len(row) for row in selected_words)
    completion = build_completion(
        core,
        len(selected),
        selected_sink_mask,
        selected_counts,
        repair_index,
        repair,
    )
    if not incoming_selected:
        completion["selected_labels"] = tuple(
            label for label in completion["selected_labels"] if label != "INCOMING"
        )
    label_map = ({"INCOMING": "INCOMING"} if incoming_selected else {})
    for new_index, old_label in enumerate(selected_ordinary_in_order):
        label_map[old_label] = f"O_{new_index}"
    for i, _sink in enumerate(sinks):
        label = f"SINK_{i}"
        if label in selected:
            label_map[label] = label
    full_sig = switching_signatures(full)
    completion_sig = switching_signatures(completion)
    moved = relabel_signature_rows(
        full_sig,
        full["selected_labels"],
        completion["selected_labels"],
        label_map,
    )
    expected = tuple(tuple(row) for row in completion_sig["signature_rows"])
    occupied = {i for i, row in enumerate(selected_words) if row}
    all_sinks_selected = selected_sink_mask == all_sink_mask
    retains_core = (
        incoming_selected
        and all_sinks_selected
        and any(set(r) <= occupied for r in core["repairs"])
    )
    dummy_labels = list(completion["dummy_labels"])
    if not incoming_selected:
        dummy_labels.append("INCOMING")
    return {
        "descriptor_match": moved == expected,
        "incoming_selected": incoming_selected,
        "selected_sink_mask": selected_sink_mask,
        "selected_counts": selected_counts,
        "selected_occupied_segments": sorted(occupied),
        "retains_strong_core": retains_core,
        "selected_reticulation_count_after_ancestral_reduction": selected_reticulation_count(full),
        "full_reticulation_count": len(sinks) + sum(
            1 for vertex in {x for arc in core["arcs"] for x in arc}
            if Counter(v for _, v in core["arcs"])[vertex] == 2
            and Counter(u for u, _ in core["arcs"])[vertex] == 1
        ),
        "full_signature_sha256": sha256_bytes(canonical_json_bytes(full_sig)),
        "completion_signature_sha256": sha256_bytes(canonical_json_bytes(completion_sig)),
        "dummy_labels": tuple(sorted(dummy_labels)),
    }


def audit_partition(core_data: dict, ordinary_labels: int = 3) -> dict:
    commitment = hashlib.sha256()
    failures = []
    counts = Counter()
    examples = {}
    for core in core_rows(core_data):
        _source, sinks = source_and_sinks(core["arcs"])
        ordinary = tuple(f"O_{i}" for i in range(ordinary_labels))
        outgoing = ordinary + tuple(f"SINK_{i}" for i in range(len(sinks)))
        for full_words in ordered_distributions(ordinary, len(core["arcs"])):
            occupied_full = {i for i, row in enumerate(full_words) if row}
            witnesses = [
                (i, repair) for i, repair in enumerate(core["repairs"])
                if set(repair) <= occupied_full
            ]
            if not witnesses:
                continue
            for mask in range(1 << len(outgoing)):
                selected = frozenset(outgoing[i] for i in range(len(outgoing)) if mask & (1 << i))
                # Empty outgoing restrictions are not local probes.
                if not selected:
                    continue
                repair_index, repair = witnesses[0]
                for incoming_selected in (True, False):
                    result = restriction_descriptor_check(
                        core, full_words, selected, repair_index, repair,
                        incoming_selected=incoming_selected,
                    )
                    counts["restrictions"] += 1
                    counts[
                        "incoming_selected" if incoming_selected else "incoming_marginalized"
                    ] += 1
                    counts[
                        "core_retaining" if result["retains_strong_core"] else "nonretaining"
                    ] += 1
                    if result["selected_reticulation_count_after_ancestral_reduction"] < result["full_reticulation_count"]:
                        counts["strictly_smaller_reticulation_core"] += 1
                        examples.setdefault("smaller_core", {
                            "core_id": core["id"],
                            "full_words": full_words,
                            "selected": sorted(selected),
                            "result": result,
                        })
                    if not result["descriptor_match"]:
                        failures.append({
                            "core_id": core["id"],
                            "full_words": full_words,
                            "selected": sorted(selected),
                            "repair_index": repair_index,
                            "repair": repair,
                            "result": result,
                        })
                    row = {
                        "core_id": core["id"],
                        "full_words": full_words,
                        "selected": sorted(selected),
                        "repair_index": repair_index,
                        "result": result,
                    }
                    commitment.update(canonical_json_bytes(row))
    return {
        "ordinary_labels_per_full_expansion": ordinary_labels,
        "counts": dict(sorted(counts.items())),
        "descriptor_partition_failure_count": len(failures),
        "failures": failures[:5],
        "examples": examples,
        "restriction_commitment_sha256": commitment.hexdigest(),
        "scope_note": (
            "Finite exhaustion uses three ordinary port labels on every core, "
            "all ordered distributions, all strong full repairs, and every "
            "nonempty selected subset. The general proof is combinatorial: "
            "selected structural-incoming bit plus selected sink mask plus "
            "ordered selected subwords plus any full minimum-repair witness "
            "is the completion key; an omitted incoming boundary is a "
            "zero-character dummy, while omitted serial "
            "vertices merely enlarge existing signature product classes."
        ),
    }


def audit_routing(repo: Path) -> dict:
    atlas = (repo / "primary/atlas_compiler.py").read_text()
    union = (repo / "primary/cycle_theta_union_compiler.py").read_text()
    required = [
        "primary/certificates/bounded_atlas_summary.json",
        "primary/certificates/bounded_relations_n3.jsonl.gz",
        "primary/certificates/bounded_sign_library_n3.json",
        "primary/certificates/bounded_relations_n4.jsonl.gz",
        "primary/certificates/bounded_sign_library_n4.json",
        "primary/certificates/bounded_relations_n5.jsonl.gz",
        "primary/certificates/bounded_sign_library_n5.json",
        "primary/certificates/bounded_relations_n6.jsonl.gz",
        "primary/certificates/bounded_sign_library_n6.json",
        "primary/certificates/cycle_theta_union_summary.json",
        "primary/certificates/cycle_theta_union_relations.jsonl.gz",
        "primary/certificates/cycle_theta_union_signs.json",
    ]
    existence = {path: (repo / path).exists() for path in required}
    checks = {
        "equal_nonretaining_routes_pending": (
            'record["classification"] = "pending_support_completion"' in atlas
        ),
        "strict_nonretaining_not_discarded_before_algebra": (
            'record["classification"] = "strict_open_cube_separation"' in atlas
        ),
        "cycle_theta_compiler_selects_nonretaining": (
            "selected_retains_strong_core(completion)" in union
            and "weak_records" in union
        ),
        "cycle_theta_completion_enumerates_dummy_assignments": (
            "for assignment in permutations(range(old, old + len(dummies)))" in union
        ),
    }
    incoming_role_checks = {
        "bounded_target_uses_full_boundary_permutations": (
            "permutations(range(n + 1))" in atlas
        ),
        "bounded_target_includes_marginalized_incoming_completions": (
            "marginal_incoming_completions(n + 1)" in atlas
        ),
        "cycle_theta_union_uses_full_five_boundary_permutations": (
            "for assignment in permutations(range(5))" in union
        ),
        "cycle_theta_union_includes_marginalized_incoming_completions": (
            "marginal_incoming_completions(5)" in union
        ),
    }
    hard_cover_contract = all(existence.values()) and all(incoming_role_checks.values())
    return {
        "source_routing_checks": checks,
        "all_source_routing_checks_pass": all(checks.values()),
        "incoming_role_hard_cover_checks": incoming_role_checks,
        "all_incoming_role_hard_cover_checks_pass": all(incoming_role_checks.values()),
        "required_relation_artifacts_exist": existence,
        "all_required_relation_artifacts_exist": all(existence.values()),
        "hard_cover_contract_satisfied": hard_cover_contract,
        "hard_cover_status": (
            "artifact-and-incoming-role-complete"
            if hard_cover_contract
            else "UNRESOLVED: relation outputs and/or incoming-role coverage incomplete"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("redstar_partition_certificate.json"))
    args = parser.parse_args()
    repo = args.repo.resolve()
    core_path = repo / "primary/certificates/core_universe.json"
    before = hashlib.sha256(core_path.read_bytes()).hexdigest()
    core_data = json.loads(core_path.read_text())
    payload = {
        "schema": "redstar-completion-partition-clean-room-v1",
        "core_certificate_sha256": before,
        "partition": audit_partition(core_data),
        "routing": audit_routing(repo),
    }
    payload["core_input_stable"] = before == hashlib.sha256(core_path.read_bytes()).hexdigest()
    raw = canonical_json_bytes(payload)
    args.output.write_bytes(raw)
    print(json.dumps({
        "output": str(args.output),
        "sha256": sha256_bytes(raw),
        "counts": payload["partition"]["counts"],
        "partition_failures": payload["partition"]["descriptor_partition_failure_count"],
        "routing": payload["routing"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
