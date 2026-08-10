#!/usr/bin/env python3
"""Fail-closed adversarial audit of the five n=3 hard-cover streams.

The verifier reconstructs the 5,344 fixed root relations and every emitted
state from primitive graphs.  It never imports ``primary`` and never selects
an invariant from a topology identifier.  Polynomial witnesses are pulled
back afresh from displayed-tree descendant masks.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import argparse
import gzip
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Iterable

from cleanroom_core import (
    Completion,
    RootedGraph,
    build_graph,
    canonical_json,
    canonical_mixed,
    class_audit,
    completion_retains_core,
    completions,
    core_rows,
    descriptor_bits_exact,
    exact_poly_hash,
    independent_sign_certificate,
    internal_vertex_audit,
    invariant_orbit,
    natural,
    ordered_quartet_deck,
    primitive_poly,
    pullback,
    quartet_descriptor,
    relabel,
    rooted_tree_child,
    sd0,
    sha256_bytes,
    source_and_sinks,
    stable_hash,
    t_quotient,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
CORE_PATH = PROJECT / "primary/certificates/core_universe.json"
SUPPORT_PATH = PROJECT / "primary/certificates/support_universe.json"
INVARIANT_PATH = PROJECT / "reviews/local_relations/proposed_invariants.json"
BIT_CACHE_PATH = PROJECT / "primary/certificates/descriptor_bits_cache.json.gz"
PRODUCER_PATH = PROJECT / "primary/hard_cover_compiler.py"
STREAM_NAMES = (
    "hard_cover_n3_sig0_all.jsonl.gz",
    "hard_cover_n3_sig1_all.jsonl.gz",
    "hard_cover_n3_sig2_all.jsonl.gz",
    "hard_cover_n3_sig3_5_all.jsonl.gz",
    "hard_cover_n3_sig6_7_all.jsonl.gz",
)
STREAMS = tuple(PROJECT / "primary/certificates" / name for name in STREAM_NAMES)


STATE_FIELDS = {
    "schema",
    "state_id",
    "selected_port_count",
    "source_mixed_code_sha256",
    "target_completion_mixed_code_sha256",
    "remaining_target_role_count",
    "probe_classification",
    "probe_witness",
    "raw_coverage",
    "children",
    "terminal_classification",
    "binding_sha256",
}
OPTIONAL_STATE_FIELDS = {"terminal_witness"}
RAW_FIELDS = {
    "selected_outgoing",
    "selected_signature_sha256",
    "source_primitive_id",
    "target_primitive_id",
    "source_position_to_label",
    "target_position_to_label",
    "target_dummy_roles",
    "target_incoming_selected",
    "root_case_id",
    "restoration_path",
    "source_extended_words",
    "restored_target_roles",
    "parent_state_id",
    "parent_path_binding_id",
    "path_binding_id",
}
ALLOWED_TERMINALS = {
    "generic_polynomial_separation",
    "strict_open_cube_separation",
    "refined_by_next_restoration",
    "support_prefix_labelled_isomorphism",
    "support_prefix_ordinary_T",
    # Three streams predate the producer's split into the preceding two
    # labels.  Their twelve records are audited algebraically and reported as
    # a provenance/schema drift rather than silently rewritten.
    "support_prefix_isomorphism_or_T",
}


@dataclass(frozen=True)
class Variant:
    primitive_id: str
    graph: RootedGraph
    labels: tuple[str, ...]
    provenance: tuple
    dummy_labels: tuple[str, ...]
    incoming_selected: bool
    retains_core: bool
    deck: tuple[tuple[tuple[int, int, int, int], tuple], ...]
    initial_words: tuple[tuple[str, ...], ...]
    core_id: str
    sink_labels: tuple[tuple[str, str], ...]
    extra_count: int | None

    def deck_map(self) -> dict:
        return dict(self.deck)


@dataclass
class Inventory:
    sources: dict[str, Variant]
    targets: dict[str, Variant]
    root_cases: dict[str, dict]
    signature_index_by_sha: dict[str, int]
    descriptor_bits: dict[tuple, int]
    invariant_orbit_sha256: str
    common_signature_count: int
    source_signature_count: int
    target_signature_count: int
    source_signature_values: tuple[int, ...]
    target_signature_values: tuple[int, ...]


def file_sha(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def graph_from_support(row: dict) -> RootedGraph:
    return RootedGraph(
        int(row["root"]),
        tuple((int(v), str(label)) for v, label in row["labels"]),
        tuple((int(u), int(v)) for u, v in row["arcs"]),
    )


def selected_labels(graph: RootedGraph) -> tuple[str, ...]:
    outgoing = tuple(sorted(
        (
            label
            for _, label in graph.labels
            if label != "INCOMING" and not label.startswith("D_")
        ),
        key=natural,
    ))
    return (*outgoing, "INCOMING")


def target_primitive(completion: Completion) -> str:
    return stable_hash({
        "kind": "target",
        "core": completion.core_id,
        "sink_mask": completion.selected_sink_mask,
        "repair": completion.repair_index,
        "words": completion.words,
        "selected": completion.selected_labels,
        "dummies": completion.dummy_labels,
        "incoming_selected": completion.incoming_selected,
        "arcs": completion.graph.arcs,
        "labels": completion.graph.labels,
    })


def build_inventory(
    *,
    selected_outgoing: int = 3,
    recompute_all_descriptor_bits: bool = True,
    source_core_ids: frozenset[str] | None = None,
    source_extra_counts: frozenset[int] | None = None,
    retain_only_target_signatures_seen_in_source: bool = False,
) -> Inventory:
    core_payload = json.loads(CORE_PATH.read_text())
    support_payload = json.loads(SUPPORT_PATH.read_text())
    invariant_payload = json.loads(INVARIANT_PATH.read_text())
    invariants = invariant_orbit(invariant_payload)
    orbit_hash = stable_hash(invariants)
    bit_cache: dict[tuple, int] = {}
    supplied_bits: dict[tuple, int] = {}
    with gzip.open(BIT_CACHE_PATH, "rt", encoding="utf-8") as handle:
        payload = json.load(handle)
    for row in payload["rows"]:
        reticulations, signatures = row["descriptor"]
        descriptor = int(reticulations), tuple(
            tuple(int(value) for value in signature) for signature in signatures
        )
        supplied_bits[descriptor] = int(row["bits"])

    def bits(descriptor: tuple) -> int:
        if descriptor not in bit_cache:
            if recompute_all_descriptor_bits:
                bit_cache[descriptor] = descriptor_bits_exact(descriptor, invariants)
            else:
                if descriptor not in supplied_bits:
                    raise AssertionError(("descriptor absent from supplied bit cache", descriptor))
                bit_cache[descriptor] = supplied_bits[descriptor]
        return bit_cache[descriptor]

    source_variants: list[Variant] = []
    for row in support_payload["records"]:
        if int(row["outgoing_count"]) != selected_outgoing:
            continue
        if source_core_ids is not None and row["core_id"] not in source_core_ids:
            continue
        if (
            source_extra_counts is not None
            and int(row["extra_count"]) not in source_extra_counts
        ):
            continue
        graph = graph_from_support(row)
        labels = selected_labels(graph)
        deck = ordered_quartet_deck(graph, labels)
        independent_code = canonical_mixed(sd0(graph))[0]
        if independent_code != row["mixed_code"]:
            raise AssertionError(("source mixed-code disagreement", row["core_id"]))
        primitive = stable_hash({
            "kind": "source",
            "core": row["core_id"],
            "repair": row["repair_index"],
            "words": row["words"],
            "sink_labels": row["sink_labels"],
            "mixed": independent_code,
        })
        source_variants.append(Variant(
            primitive, graph, labels,
            (row["core_id"], row["repair_index"], tuple(tuple(word) for word in row["words"])),
            (), True, True, tuple(sorted(deck.items())),
            tuple(tuple(word) for word in row["words"]), row["core_id"],
            tuple(sorted((str(k), str(v)) for k, v in row["sink_labels"].items())),
            int(row["extra_count"]),
        ))

    # A base is a descriptor-identical group.  The producer retains every
    # primitive variant in each group, so the audit does likewise.
    target_groups: dict[tuple, dict[str, Variant]] = defaultdict(dict)
    for incoming_selected in (True, False):
        port_count = selected_outgoing + 1
        for completion in completions(core_payload, port_count, incoming_selected):
            labels = (
                (*tuple(sorted(completion.selected_labels, key=natural)), "INCOMING")
                if incoming_selected
                else tuple(sorted(completion.selected_labels, key=natural))
            )
            if len(labels) != port_count:
                raise AssertionError((completion.core_id, labels))
            deck = ordered_quartet_deck(completion.graph, labels)
            primitive = target_primitive(completion)
            kind = "cycle" if completion.core_id == "cycle" else "theta"
            variant = Variant(
                primitive, completion.graph, labels,
                (
                    completion.core_id,
                    completion.selected_sink_mask,
                    completion.repair_index,
                    completion.words,
                    completion.dummy_labels,
                    completion.incoming_selected,
                ),
                completion.dummy_labels,
                completion.incoming_selected,
                completion_retains_core(completion, core_payload),
                tuple(sorted(deck.items())), completion.words, completion.core_id, (),
                None,
            )
            group_key = kind, variant.deck
            variant_key = stable_hash({
                "primitive": primitive,
                "mixed": canonical_mixed(sd0(completion.graph))[0],
                "selected": labels,
                "dummies": completion.dummy_labels,
            })
            target_groups[group_key].setdefault(variant_key, variant)

    source_records: dict[int, dict[str, tuple[Variant, tuple[int, ...], tuple]]] = defaultdict(dict)
    for variant in source_variants:
        assignment = tuple(range(selected_outgoing + 1))
        deck_map = variant.deck_map()
        descriptor_deck = tuple(
            deck_map[quartet]
            for quartet in combinations(range(selected_outgoing + 1), 4)
        )
        signature = 0
        for chunk, descriptor in enumerate(descriptor_deck):
            signature |= bits(descriptor) << (len(invariants) * chunk)
        variant_key = stable_hash({
            "primitive": variant.primitive_id,
            "assignment": assignment,
            "descriptor_deck": stable_hash(descriptor_deck),
        })
        source_records[signature].setdefault(
            variant_key, (variant, assignment, descriptor_deck)
        )

    target_records: dict[int, dict[str, tuple[Variant, tuple[int, ...], tuple]]] = defaultdict(dict)
    for group_key in sorted(target_groups, key=repr):
        variants = tuple(target_groups[group_key][key] for key in sorted(target_groups[group_key]))
        representative = min(variants, key=lambda row: (not row.retains_core, row.primitive_id))
        deck = representative.deck_map()
        for assignment in permutations(range(selected_outgoing + 1)):
            inverse = [0] * (selected_outgoing + 1)
            for position, actual in enumerate(assignment):
                inverse[actual] = position
            descriptor_deck = tuple(
                deck[tuple(inverse[value] for value in actual_quartet)]
                for actual_quartet in combinations(range(selected_outgoing + 1), 4)
            )
            signature = 0
            for chunk, descriptor in enumerate(descriptor_deck):
                signature |= bits(descriptor) << (len(invariants) * chunk)
            if (
                retain_only_target_signatures_seen_in_source
                and signature not in source_records
            ):
                continue
            descriptor_hash = stable_hash(descriptor_deck)
            for variant in variants:
                variant_key = stable_hash({
                    "primitive": variant.primitive_id,
                    "assignment": assignment,
                    "descriptor_deck": descriptor_hash,
                })
                target_records[signature].setdefault(
                    variant_key, (variant, tuple(assignment), descriptor_deck)
                )

    common = sorted(set(source_records) & set(target_records))
    signature_index_by_sha = {
        hashlib.sha256(str(signature).encode()).hexdigest(): index
        for index, signature in enumerate(common)
    }
    root_cases: dict[str, dict] = {}
    source_by_id = {variant.primitive_id: variant for variant in source_variants}
    target_by_id = {
        variant.primitive_id: variant
        for variants in target_groups.values()
        for variant in variants.values()
    }
    for signature in common:
        signature_sha = hashlib.sha256(str(signature).encode()).hexdigest()
        for source_variant, source_assignment, _ in source_records[signature].values():
            for target_variant, target_assignment, _ in target_records[signature].values():
                if target_variant.retains_core:
                    continue
                root_key = {
                    "selected_outgoing": selected_outgoing,
                    "selected_signature_sha256": signature_sha,
                    "source_primitive_id": source_variant.primitive_id,
                    "target_primitive_id": target_variant.primitive_id,
                    "source_provenance": source_variant.provenance,
                    "target_provenance": target_variant.provenance,
                    "source_selected_labels": source_variant.labels,
                    "target_selected_labels": target_variant.labels,
                    "source_position_to_label": source_assignment,
                    "target_position_to_label": target_assignment,
                    "target_dummy_roles": tuple(sorted(target_variant.dummy_labels, key=natural)),
                    "target_incoming_selected": target_variant.incoming_selected,
                }
                root_id = stable_hash(root_key)
                if root_id in root_cases:
                    raise AssertionError(("duplicate independent root id", root_id))
                root_cases[root_id] = root_key

    # Cache agreement is checked after independently deriving every descriptor
    # needed by the root inventory.  It is not used as the source of truth.
    cache_disagreements = [
        descriptor for descriptor, value in bit_cache.items()
        if supplied_bits.get(descriptor) != value
    ]
    if cache_disagreements:
        raise AssertionError(("descriptor-bit cache disagreement", len(cache_disagreements)))
    return Inventory(
        source_by_id,
        target_by_id,
        root_cases,
        signature_index_by_sha,
        bit_cache,
        orbit_hash,
        len(common),
        len(source_records),
        len(target_records),
        tuple(sorted(source_records)),
        tuple(sorted(target_records)),
    )


def read_streams(streams: Iterable[Path] = STREAMS) -> tuple[dict[str, dict], dict[str, tuple[str, dict]], dict]:
    states: dict[str, dict] = {}
    paths: dict[str, tuple[str, dict]] = {}
    file_rows = []
    failures: list[dict] = []
    for path in streams:
        if not path.exists():
            failures.append({"type": "missing_stream", "path": str(path)})
            continue
        uncompressed = hashlib.sha256()
        state_count = 0
        coverage_count = 0
        root_ids = set()
        terminal_counts = Counter()
        prior_state_id = None
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                uncompressed.update(line.encode())
                try:
                    record = json.loads(line)
                except Exception as error:
                    failures.append({
                        "type": "invalid_json", "path": str(path),
                        "line": line_number, "error": repr(error),
                    })
                    continue
                state_count += 1
                state_id = record.get("state_id")
                if not isinstance(state_id, str):
                    failures.append({"type": "missing_state_id", "path": str(path), "line": line_number})
                    continue
                if prior_state_id is not None and state_id <= prior_state_id:
                    failures.append({"type": "stream_not_strictly_sorted", "state_id": state_id})
                prior_state_id = state_id
                if state_id in states:
                    failures.append({"type": "duplicate_state_id", "state_id": state_id})
                states[state_id] = record
                terminal_counts[record.get("terminal_classification")] += 1
                if set(record) - (STATE_FIELDS | OPTIONAL_STATE_FIELDS):
                    failures.append({
                        "type": "unknown_state_fields", "state_id": state_id,
                        "fields": sorted(set(record) - (STATE_FIELDS | OPTIONAL_STATE_FIELDS)),
                    })
                if STATE_FIELDS - set(record):
                    failures.append({
                        "type": "missing_state_fields", "state_id": state_id,
                        "fields": sorted(STATE_FIELDS - set(record)),
                    })
                bound = dict(record)
                recorded_binding = bound.pop("binding_sha256", None)
                if stable_hash(bound) != recorded_binding:
                    failures.append({"type": "state_binding_mismatch", "state_id": state_id})
                for coverage in record.get("raw_coverage", []):
                    coverage_count += 1
                    if set(coverage) != RAW_FIELDS:
                        failures.append({
                            "type": "raw_schema_mismatch", "state_id": state_id,
                            "missing": sorted(RAW_FIELDS - set(coverage)),
                            "extra": sorted(set(coverage) - RAW_FIELDS),
                        })
                    path_id = coverage.get("path_binding_id")
                    bound_path = dict(coverage)
                    bound_path.pop("path_binding_id", None)
                    if stable_hash(bound_path) != path_id:
                        failures.append({"type": "path_binding_mismatch", "state_id": state_id})
                    if path_id in paths:
                        failures.append({"type": "duplicate_path_id", "path_id": path_id})
                    paths[path_id] = (state_id, coverage)
                    root_ids.add(coverage.get("root_case_id"))
        file_rows.append({
            "path": str(path.relative_to(PROJECT)),
            "gzip_sha256": file_sha(path),
            "uncompressed_sha256": uncompressed.hexdigest(),
            "bytes": path.stat().st_size,
            "state_count": state_count,
            "coverage_count": coverage_count,
            "root_case_count": len(root_ids),
            "terminal_counts": dict(sorted(terminal_counts.items(), key=lambda row: str(row[0]))),
        })
    return states, paths, {"files": file_rows, "failures": failures}


def root_key_from_coverage(coverage: dict) -> dict:
    return {
        key: coverage[key]
        for key in (
            "selected_outgoing",
            "selected_signature_sha256",
            "source_primitive_id",
            "target_primitive_id",
            "source_provenance",
            "target_provenance",
            "source_selected_labels",
            "target_selected_labels",
            "source_position_to_label",
            "target_position_to_label",
            "target_dummy_roles",
            "target_incoming_selected",
        )
    }


def source_graph_for(variant: Variant, coverage: dict, core_payload: dict) -> RootedGraph:
    core = {row["id"]: row for row in core_rows(core_payload)}[variant.core_id]
    _, sinks = source_and_sinks(core["arcs"])
    sink_labels = {sink: f"Q_SINK_{index}" for index, sink in enumerate(sinks)}
    graph = build_graph(core["arcs"], coverage["source_extended_words"], sink_labels)
    mapping = {
        label: f"L_{actual}"
        for label, actual in zip(variant.labels, coverage["source_position_to_label"])
    }
    return relabel(graph, mapping)


def target_graph_for(variant: Variant, coverage: dict) -> RootedGraph:
    mapping = {
        label: f"L_{actual}"
        for label, actual in zip(variant.labels, coverage["target_position_to_label"])
    }
    base_port_count = int(coverage["selected_outgoing"]) + 1
    for index, role in enumerate(coverage["restoration_path"]):
        mapping[role] = f"L_{base_port_count + index}"
    return relabel(variant.graph, mapping)


def subsequence_after_removing_restored(words: Iterable[Iterable[str]]) -> tuple[tuple[str, ...], ...]:
    return tuple(
        tuple(label for label in word if not label.startswith("L_"))
        for word in words
    )


def insert_one_label(words: Iterable[Iterable[str]], label: str) -> tuple[tuple[tuple[str, ...], ...], ...]:
    base = tuple(tuple(word) for word in words)
    answers = set()
    for segment, word in enumerate(base):
        for position in range(len(word) + 1):
            moved = list(base)
            moved[segment] = (*word[:position], label, *word[position:])
            answers.add(tuple(tuple(values) for values in moved))
    return tuple(sorted(answers, key=repr))


def semantic_audit(
    states: dict[str, dict],
    paths: dict[str, tuple[str, dict]],
    inventory: Inventory,
    *,
    verify_all_algebra: bool = True,
) -> dict:
    core_payload = json.loads(CORE_PATH.read_text())
    invariant_payload = json.loads(INVARIANT_PATH.read_text())
    invariants = invariant_orbit(invariant_payload)
    failures: list[dict] = []
    warnings: list[dict] = []
    state_key_to_id: dict[str, str] = {}
    root_ids_seen = set()
    first_paths_by_root: dict[str, list[str]] = defaultdict(list)
    child_paths_by_parent_path: dict[str, list[str]] = defaultdict(list)
    algebra_counts = Counter()
    class_sample_records: dict[str, dict] = {}
    polynomial_cache: dict[tuple, dict] = {}
    sign_cache: dict[str, dict] = {}
    derived_maps: dict[str, dict] = {}

    def rooted_graph_id(graph: RootedGraph) -> str:
        return stable_hash({
            "root": int(graph.root),
            "labels": tuple(
                (int(vertex), str(label)) for vertex, label in graph.labels
            ),
            "arcs": tuple((int(u), int(v)) for u, v in graph.arcs),
        })

    # First pass: exact root/path binding and parent data.
    for path_id, (state_id, coverage) in paths.items():
        root_id = coverage["root_case_id"]
        root_ids_seen.add(root_id)
        root_key = root_key_from_coverage(coverage)
        if stable_hash(root_key) != root_id:
            failures.append({"type": "root_case_hash_mismatch", "state_id": state_id, "path_id": path_id})
        independent_key = inventory.root_cases.get(root_id)
        if independent_key is None:
            failures.append({"type": "root_case_absent_from_independent_inventory", "root_case_id": root_id})
        elif canonical_json(independent_key) != canonical_json(root_key):
            failures.append({"type": "root_case_payload_mismatch", "root_case_id": root_id})
        source_assignment = coverage["source_position_to_label"]
        target_assignment = coverage["target_position_to_label"]
        base_port_count = int(coverage["selected_outgoing"]) + 1
        if source_assignment != list(range(base_port_count)):
            failures.append({"type": "source_not_anchored", "path_id": path_id})
        if sorted(target_assignment) != list(range(base_port_count)):
            failures.append({"type": "target_not_physical_bijection", "path_id": path_id})
        dummy_order = sorted(coverage["target_dummy_roles"], key=natural)
        path_roles = coverage["restoration_path"]
        if path_roles != dummy_order[: len(path_roles)]:
            failures.append({"type": "restoration_order_mismatch", "path_id": path_id})
        if sorted(path_roles) != coverage["restored_target_roles"]:
            failures.append({"type": "restored_role_set_mismatch", "path_id": path_id})
        record = states[state_id]
        if record["selected_port_count"] != base_port_count + len(path_roles):
            failures.append({"type": "selected_port_count_mismatch", "path_id": path_id})
        if record["remaining_target_role_count"] != len(dummy_order) - len(path_roles):
            failures.append({"type": "remaining_role_count_mismatch", "path_id": path_id})
        if coverage["parent_path_binding_id"] is None:
            if coverage["parent_state_id"] is not None or len(path_roles) != 1:
                failures.append({"type": "invalid_root_parent", "path_id": path_id})
            first_paths_by_root[root_id].append(path_id)
        else:
            parent_id = coverage["parent_path_binding_id"]
            parent_entry = paths.get(parent_id)
            if parent_entry is None:
                failures.append({"type": "missing_parent_path", "path_id": path_id})
            else:
                parent_state_id, parent = parent_entry
                if parent_state_id != coverage["parent_state_id"]:
                    failures.append({"type": "parent_state_mismatch", "path_id": path_id})
                if parent["root_case_id"] != root_id:
                    failures.append({"type": "parent_root_mismatch", "path_id": path_id})
                if parent["restoration_path"] != path_roles[:-1]:
                    failures.append({"type": "parent_prefix_mismatch", "path_id": path_id})
                if parent["source_primitive_id"] != coverage["source_primitive_id"] or parent["target_primitive_id"] != coverage["target_primitive_id"]:
                    failures.append({"type": "parent_fixed_relation_mismatch", "path_id": path_id})
                prior_words = tuple(tuple(word) for word in parent["source_extended_words"])
                current_words = tuple(tuple(word) for word in coverage["source_extended_words"])
                new_label = f"L_{base_port_count + len(path_roles) - 1}"
                stripped = tuple(tuple(label for label in word if label != new_label) for word in current_words)
                if stripped != prior_words:
                    failures.append({"type": "source_word_parent_mismatch", "path_id": path_id})
            child_paths_by_parent_path[parent_id].append(path_id)

        source_variant = inventory.sources.get(coverage["source_primitive_id"])
        target_variant = inventory.targets.get(coverage["target_primitive_id"])
        if source_variant is None:
            failures.append({"type": "unknown_source_primitive", "path_id": path_id})
            continue
        if target_variant is None:
            failures.append({"type": "unknown_target_primitive", "path_id": path_id})
            continue
        if tuple(target_variant.dummy_labels) != tuple(coverage["target_dummy_roles"]):
            # The producer stores the natural order in the root key.
            if tuple(sorted(target_variant.dummy_labels, key=natural)) != tuple(coverage["target_dummy_roles"]):
                failures.append({"type": "target_dummy_role_mismatch", "path_id": path_id})
        if target_variant.incoming_selected != coverage["target_incoming_selected"]:
            failures.append({"type": "target_incoming_mode_mismatch", "path_id": path_id})
        if subsequence_after_removing_restored(coverage["source_extended_words"]) != source_variant.initial_words:
            failures.append({"type": "source_word_extension_not_order_preserving", "path_id": path_id})

    independent_root_ids = set(inventory.root_cases)
    if root_ids_seen != independent_root_ids:
        failures.append({
            "type": "root_inventory_mismatch",
            "missing_count": len(independent_root_ids - root_ids_seen),
            "extra_count": len(root_ids_seen - independent_root_ids),
            "missing_examples": sorted(independent_root_ids - root_ids_seen)[:10],
            "extra_examples": sorted(root_ids_seen - independent_root_ids)[:10],
        })
    for root_id in independent_root_ids:
        if not first_paths_by_root.get(root_id):
            failures.append({"type": "root_case_has_no_first_path", "root_case_id": root_id})

    # The critical path-exhaustiveness check is per raw relation path, not per
    # deduplicated canonical state.
    missing_continuations = []
    for state_id, record in states.items():
        if record["terminal_classification"] != "refined_by_next_restoration":
            continue
        for coverage in record["raw_coverage"]:
            path_id = coverage["path_binding_id"]
            explicitly_bound = tuple(coverage.get("child_state_ids", ()))
            if not child_paths_by_parent_path.get(path_id) and not explicitly_bound:
                missing_continuations.append({
                    "state_id": state_id,
                    "path_binding_id": path_id,
                    "root_case_id": coverage["root_case_id"],
                    "restoration_path": coverage["restoration_path"],
                    "state_child_count": len(record["children"]),
                    "state_raw_coverage_count": len(record["raw_coverage"]),
                })
    if missing_continuations:
        failures.append({
            "type": "nonterminal_raw_paths_without_bound_children",
            "count": len(missing_continuations),
            "affected_root_cases": len({row["root_case_id"] for row in missing_continuations}),
            "examples": missing_continuations[:20],
        })

    for state_id, record in states.items():
        if record["terminal_classification"] not in ALLOWED_TERMINALS:
            failures.append({"type": "unknown_terminal_classification", "state_id": state_id})
        for child_id in record["children"]:
            child = states.get(child_id)
            if child is None:
                failures.append({"type": "missing_child_state", "state_id": state_id, "child_id": child_id})
            elif not any(row["parent_state_id"] == state_id for row in child["raw_coverage"]):
                failures.append({"type": "unbound_child_state", "state_id": state_id, "child_id": child_id})

    # Reconstruct every graph pair and its exact canonical state key.  This
    # simultaneously checks every physical port matching in every raw path.
    graph_cache: dict[tuple, tuple[RootedGraph, RootedGraph, str, str, dict, dict]] = {}
    state_graphs: dict[str, tuple[RootedGraph, RootedGraph, str, str]] = {}
    strata: dict[tuple, str] = {}
    allowed_state_ids = {
        state_id
        for state_id, record in states.items()
        if record["terminal_classification"].startswith("support_prefix")
    }
    for state_id in sorted(states):
        record = states[state_id]
        expected_pair = None
        for coverage in record["raw_coverage"]:
            source_variant = inventory.sources.get(coverage["source_primitive_id"])
            target_variant = inventory.targets.get(coverage["target_primitive_id"])
            if source_variant is None or target_variant is None:
                continue
            cache_key = (
                coverage["source_primitive_id"],
                tuple(coverage["source_position_to_label"]),
                tuple(tuple(word) for word in coverage["source_extended_words"]),
                coverage["target_primitive_id"],
                tuple(coverage["target_position_to_label"]),
                tuple(coverage["restoration_path"]),
            )
            if cache_key not in graph_cache:
                source_graph = source_graph_for(source_variant, coverage, core_payload)
                target_graph = target_graph_for(target_variant, coverage)
                source_mixed = sd0(source_graph)
                target_mixed = sd0(target_graph)
                source_code, source_map = canonical_mixed(source_mixed)
                target_code, target_map = canonical_mixed(target_mixed)
                graph_cache[cache_key] = (
                    source_graph, target_graph, source_code, target_code,
                    {str(k): int(v) for k, v in source_map.items()},
                    {str(k): int(v) for k, v in target_map.items()},
                )
            source_graph, target_graph, source_code, target_code, source_map, target_map = graph_cache[cache_key]
            source_graph_id = rooted_graph_id(source_graph)
            target_graph_id = rooted_graph_id(target_graph)
            remaining = tuple(
                sorted(coverage["target_dummy_roles"], key=natural)[len(coverage["restoration_path"]):]
            )
            key_payload = {
                "fixed_full_root_case_id": coverage["root_case_id"],
                "selected_port_count": record["selected_port_count"],
                "source_rooted_graph_id": source_graph_id,
                "target_rooted_graph_id": target_graph_id,
                "source_mixed_code": source_code,
                "target_completion_mixed_code": target_code,
                "remaining_target_roles": remaining,
                "port_matching": tuple(range(record["selected_port_count"])),
            }
            derived_state_id = stable_hash(key_payload)
            if derived_state_id != state_id:
                failures.append({"type": "state_id_graph_binding_mismatch", "state_id": state_id, "path_id": coverage["path_binding_id"], "derived": derived_state_id})
            if hashlib.sha256(source_code.encode()).hexdigest() != record["source_mixed_code_sha256"]:
                failures.append({"type": "source_code_hash_mismatch", "state_id": state_id})
            if hashlib.sha256(target_code.encode()).hexdigest() != record["target_completion_mixed_code_sha256"]:
                failures.append({"type": "target_code_hash_mismatch", "state_id": state_id})
            if record.get("fixed_full_root_case_id") != coverage["root_case_id"]:
                failures.append({"type": "state_fixed_root_case_mismatch", "state_id": state_id, "path_id": coverage["path_binding_id"]})
            if record.get("source_graph_id") != source_graph_id or coverage.get("source_graph_id") != source_graph_id:
                failures.append({"type": "state_or_coverage_source_rooted_graph_mismatch", "state_id": state_id, "path_id": coverage["path_binding_id"]})
            if record.get("target_graph_id") != target_graph_id or coverage.get("target_graph_id") != target_graph_id:
                failures.append({"type": "state_or_coverage_target_rooted_graph_mismatch", "state_id": state_id, "path_id": coverage["path_binding_id"]})
            canonical_key = canonical_json(key_payload)
            prior = state_key_to_id.setdefault(canonical_key, state_id)
            if prior != state_id:
                failures.append({"type": "canonical_state_not_unique", "state_id": state_id, "other": prior})
            pair = source_code, target_code
            if expected_pair is None:
                expected_pair = pair
                state_graphs[state_id] = (source_graph, target_graph, source_code, target_code)
                derived_maps[state_id] = {"source": source_map, "target": target_map}
            elif pair != expected_pair:
                failures.append({"type": "deduplicated_state_graph_disagreement", "state_id": state_id})
            stratum = (
                record["probe_classification"], record["selected_port_count"],
                source_variant.core_id, target_variant.core_id,
                target_variant.incoming_selected,
            )
            strata.setdefault(stratum, state_id)

    # Adversarially recompute the complete next-child set for every merged raw
    # presentation.  A canonical parent state is safe to merge only if every
    # one of its raw rooted provenances induces exactly the same canonical
    # child-state set.  State-level children are not allowed to stand in for
    # missing path-specific bindings.
    per_path_child_set_failures = []
    merged_child_set_disagreements = []
    state_level_child_set_failures = []
    for state_id in sorted(states):
        record = states[state_id]
        if record["terminal_classification"] != "refined_by_next_restoration":
            continue
        expected_by_path: dict[str, tuple[str, ...]] = {}
        for coverage in record["raw_coverage"]:
            source_variant = inventory.sources[coverage["source_primitive_id"]]
            target_variant = inventory.targets[coverage["target_primitive_id"]]
            path_roles = tuple(coverage["restoration_path"])
            dummy_order = tuple(sorted(coverage["target_dummy_roles"], key=natural))
            if len(path_roles) >= len(dummy_order):
                failures.append({"type": "refined_state_has_no_remaining_role", "state_id": state_id})
                continue
            next_role = dummy_order[len(path_roles)]
            base_port_count = int(coverage["selected_outgoing"]) + 1
            next_label = f"L_{base_port_count + len(path_roles)}"
            expected_children = set()
            for extended_words in insert_one_label(coverage["source_extended_words"], next_label):
                synthetic = dict(coverage)
                synthetic["source_extended_words"] = extended_words
                synthetic["restoration_path"] = (*path_roles, next_role)
                source_graph = source_graph_for(source_variant, synthetic, core_payload)
                target_graph = target_graph_for(target_variant, synthetic)
                source_code = canonical_mixed(sd0(source_graph))[0]
                target_code = canonical_mixed(sd0(target_graph))[0]
                source_graph_id = rooted_graph_id(source_graph)
                target_graph_id = rooted_graph_id(target_graph)
                remaining = dummy_order[len(path_roles) + 1:]
                expected_children.add(stable_hash({
                    "fixed_full_root_case_id": coverage["root_case_id"],
                    "selected_port_count": record["selected_port_count"] + 1,
                    "source_rooted_graph_id": source_graph_id,
                    "target_rooted_graph_id": target_graph_id,
                    "source_mixed_code": source_code,
                    "target_completion_mixed_code": target_code,
                    "remaining_target_roles": remaining,
                    "port_matching": tuple(range(record["selected_port_count"] + 1)),
                }))
            path_id = coverage["path_binding_id"]
            expected = tuple(sorted(expected_children))
            expected_by_path[path_id] = expected
            explicit_children = coverage.get("child_state_ids")
            if explicit_children is None:
                actual_bound = tuple(sorted({
                    paths[child_path_id][0]
                    for child_path_id in child_paths_by_parent_path.get(path_id, ())
                }))
            else:
                actual_bound = tuple(sorted(explicit_children))
            if actual_bound != expected:
                per_path_child_set_failures.append({
                    "state_id": state_id,
                    "path_binding_id": path_id,
                    "root_case_id": coverage["root_case_id"],
                    "expected_count": len(expected),
                    "actual_bound_count": len(actual_bound),
                    "missing": sorted(set(expected) - set(actual_bound))[:20],
                    "extra": sorted(set(actual_bound) - set(expected))[:20],
                })
            if tuple(sorted(record["children"])) != expected:
                state_level_child_set_failures.append({
                    "state_id": state_id,
                    "path_binding_id": path_id,
                    "expected_count": len(expected),
                    "state_child_count": len(record["children"]),
                    "missing": sorted(set(expected) - set(record["children"]))[:20],
                    "extra": sorted(set(record["children"]) - set(expected))[:20],
                })
        distinct_sets: dict[tuple[str, ...], list[str]] = defaultdict(list)
        for path_id, child_set in expected_by_path.items():
            distinct_sets[child_set].append(path_id)
        if len(distinct_sets) > 1:
            merged_child_set_disagreements.append({
                "state_id": state_id,
                "raw_coverage_count": len(record["raw_coverage"]),
                "distinct_expected_child_sets": len(distinct_sets),
                "groups": [
                    {"child_count": len(child_set), "path_examples": path_ids[:5], "children": list(child_set[:10])}
                    for child_set, path_ids in list(distinct_sets.items())[:8]
                ],
            })
    if per_path_child_set_failures:
        failures.append({
            "type": "per_presentation_child_set_mismatch",
            "count": len(per_path_child_set_failures),
            "examples": per_path_child_set_failures[:20],
        })
    if merged_child_set_disagreements:
        failures.append({
            "type": "canonical_merge_has_provenance_dependent_child_sets",
            "count": len(merged_child_set_disagreements),
            "examples": merged_child_set_disagreements[:20],
        })
    if state_level_child_set_failures:
        failures.append({
            "type": "state_level_child_set_mismatch",
            "count": len(state_level_child_set_failures),
            "examples": state_level_child_set_failures[:20],
        })

    # Deterministic class sample: every topology-permitting terminal and the
    # lexicographically first state of every structural/algebraic stratum.
    sampled_state_ids = allowed_state_ids | set(strata.values())
    for state_id in sorted(sampled_state_ids):
        record = states[state_id]
        for coverage in record["raw_coverage"] if state_id in allowed_state_ids else record["raw_coverage"][:1]:
            source_variant = inventory.sources[coverage["source_primitive_id"]]
            target_variant = inventory.targets[coverage["target_primitive_id"]]
            source_graph = source_graph_for(source_variant, coverage, core_payload)
            target_graph = target_graph_for(target_variant, coverage)
            source_result = class_audit(source_graph)
            target_result = class_audit(target_graph)
            for side, result in (("source", source_result), ("target", target_result)):
                required = (
                    result.get("rooted_valid")
                    and result.get("root_is_lsa")
                    and result.get("rooted_tree_child")
                    and result.get("internal_vertex_audit", {}).get("passes")
                    and result.get("internal_vertex_audit", {}).get("leaf_vertices_excluded")
                    and result.get("sd0_valid")
                    and result.get("standard_strong_local")
                    and result.get("level_at_most_two")
                    and int(result.get("triangle_count", 99)) <= 1
                )
                if not required:
                    failures.append({
                        "type": "class_membership_failure", "state_id": state_id,
                        "path_id": coverage["path_binding_id"], "side": side,
                        "result": result,
                    })
            class_sample_records[coverage["path_binding_id"]] = {
                "state_id": state_id,
                "terminal": record["terminal_classification"],
                "source": source_result,
                "target": target_result,
            }

    # Every graph-derived polynomial witness is recomputed.  Equal/unsigned
    # signatures are checked by rebuilding all quartet bit decks.  The skip
    # branch exists only for development timing; release verification never
    # enables it.
    for state_id in (sorted(states) if verify_all_algebra else ()):
        record = states[state_id]
        if state_id not in state_graphs:
            continue
        source_graph, target_graph, source_code, target_code = state_graphs[state_id]
        port_count = record["selected_port_count"]
        labels = tuple(f"L_{index}" for index in range(port_count))
        quartets = tuple(combinations(range(port_count), 4))
        classification = record["probe_classification"]
        witness = record["probe_witness"]
        if classification in {"generic_polynomial_separation", "strict_open_cube_separation"}:
            chunk = int(witness["quartet_chunk"])
            invariant_index = int(witness["invariant_index"])
            if not (0 <= chunk < len(quartets)) or not (0 <= invariant_index < len(invariants)):
                failures.append({"type": "witness_index_out_of_range", "state_id": state_id})
                continue
            quartet = quartets[chunk]
            source_descriptor = quartet_descriptor(source_graph, labels, quartet)
            target_descriptor = quartet_descriptor(target_graph, labels, quartet)
            source_poly = pullback(source_descriptor, invariants[invariant_index])
            target_poly = pullback(target_descriptor, invariants[invariant_index])
            algebra_counts[classification] += 1
            if classification == "generic_polynomial_separation":
                if not source_poly or target_poly:
                    failures.append({"type": "generic_separator_orientation_failure", "state_id": state_id})
                elif exact_poly_hash(source_poly) != witness.get("source_pullback_exact_sha256"):
                    failures.append({"type": "source_polynomial_hash_mismatch", "state_id": state_id})
            else:
                if source_poly or not target_poly:
                    failures.append({"type": "strict_separator_orientation_failure", "state_id": state_id})
                elif exact_poly_hash(target_poly) != witness.get("target_pullback_exact_sha256"):
                    failures.append({"type": "target_polynomial_hash_mismatch", "state_id": state_id})
                else:
                    polynomial_hash = exact_poly_hash(target_poly)
                    if polynomial_hash not in sign_cache:
                        sign_cache[polynomial_hash] = independent_sign_certificate(target_poly)
                    sign = sign_cache[polynomial_hash]
                    recorded_sign = witness.get("target_strict_sign")
                    certificate = witness.get("target_sign_certificate", {})
                    independent_sign = sign.get("strict_sign", sign.get("sign"))
                    if not sign.get("certified") or independent_sign != recorded_sign:
                        failures.append({"type": "strict_sign_replay_failure", "state_id": state_id, "independent": sign, "recorded": recorded_sign})
                    primitive_hash = hashlib.sha256(repr(primitive_poly(target_poly)).encode()).hexdigest()
                    if certificate.get("polynomial_sha256") != primitive_hash:
                        failures.append({"type": "strict_sign_polynomial_binding_failure", "state_id": state_id})
                    if not sign.get("factorization_exact", True):
                        failures.append({"type": "strict_sign_factorization_failure", "state_id": state_id})
                    if int(certificate.get("term_count", -1)) != len(target_poly):
                        failures.append({"type": "strict_sign_term_count_mismatch", "state_id": state_id})
                    if certificate.get("strict_sign") != independent_sign:
                        failures.append({"type": "strict_sign_certificate_sign_mismatch", "state_id": state_id})
                    independent_factors = sign.get("factors", [])
                    recorded_factors = certificate.get("factors", [])
                    if canonical_json(independent_factors) != canonical_json(recorded_factors):
                        failures.append({
                            "type": "strict_sign_factor_bernstein_mismatch",
                            "state_id": state_id,
                            "polynomial_sha256": polynomial_hash,
                            "independent_factor_count": len(independent_factors),
                            "recorded_factor_count": len(recorded_factors),
                        })
        elif classification in {"equal_invariant_signature", "unresolved_unsigned_signature"}:
            source_signature = 0
            target_signature = 0
            width = len(invariants)
            for chunk, quartet in enumerate(quartets):
                source_descriptor = quartet_descriptor(source_graph, labels, quartet)
                target_descriptor = quartet_descriptor(target_graph, labels, quartet)
                source_bits = inventory.descriptor_bits.get(source_descriptor)
                if source_bits is None:
                    source_bits = descriptor_bits_exact(source_descriptor, invariants)
                    inventory.descriptor_bits[source_descriptor] = source_bits
                target_bits = inventory.descriptor_bits.get(target_descriptor)
                if target_bits is None:
                    target_bits = descriptor_bits_exact(target_descriptor, invariants)
                    inventory.descriptor_bits[target_descriptor] = target_bits
                source_signature |= source_bits << (width * chunk)
                target_signature |= target_bits << (width * chunk)
            if classification == "equal_invariant_signature" and source_signature != target_signature:
                failures.append({"type": "equal_signature_replay_failure", "state_id": state_id})
            if classification == "unresolved_unsigned_signature":
                if source_signature == target_signature:
                    failures.append({"type": "unsigned_signature_replay_equal", "state_id": state_id})
                source_sha = hashlib.sha256(str(source_signature).encode()).hexdigest()
                target_sha = hashlib.sha256(str(target_signature).encode()).hexdigest()
                if witness.get("source_signature_sha256") != source_sha or witness.get("target_signature_sha256") != target_sha:
                    failures.append({"type": "unsigned_signature_hash_mismatch", "state_id": state_id})

    # Every topology-permitting terminal is independently reduced and
    # classified as literal isomorphism or ordinary T.
    terminal_reclassification = Counter()
    allowed_terminal_rows = []
    for state_id in sorted(allowed_state_ids):
        source_graph, target_graph, source_code, target_code = state_graphs[state_id]
        source_t_code, _ = canonical_mixed(t_quotient(sd0(source_graph)))
        target_t_code, _ = canonical_mixed(t_quotient(sd0(target_graph)))
        if source_t_code != target_t_code:
            failures.append({"type": "allowed_terminal_is_non_T", "state_id": state_id})
            classification = "non_T"
        elif source_code == target_code:
            classification = "labelled_isomorphism"
        else:
            classification = "ordinary_T"
        terminal_reclassification[classification] += 1
        terminal_witness = states[state_id].get("terminal_witness", {})
        expected_t_hash = hashlib.sha256(source_t_code.encode()).hexdigest()
        if terminal_witness.get("t_quotient_code_sha256") != expected_t_hash:
            failures.append({"type": "terminal_T_hash_mismatch", "state_id": state_id})
        if "mixed_codes_equal" in terminal_witness and bool(terminal_witness["mixed_codes_equal"]) != (source_code == target_code):
            failures.append({"type": "terminal_mixed_equality_mismatch", "state_id": state_id})
        allowed_terminal_rows.append({
            "state_id": state_id,
            "recorded": states[state_id]["terminal_classification"],
            "independent": classification,
            "raw_coverage_count": len(states[state_id]["raw_coverage"]),
            "selected_port_count": states[state_id]["selected_port_count"],
        })

    if any(
        record["terminal_classification"].startswith("unresolved")
        for record in states.values()
    ):
        failures.append({"type": "unresolved_terminal_present"})

    terminal_counts = Counter(record["terminal_classification"] for record in states.values())
    probe_counts = Counter(record["probe_classification"] for record in states.values())
    return {
        "failures": failures,
        "warnings": warnings,
        "root_case_count_seen": len(root_ids_seen),
        "root_case_count_independent": len(independent_root_ids),
        "canonical_state_count": len(states),
        "canonical_state_key_count": len(state_key_to_id),
        "raw_path_count": len(paths),
        "nonterminal_raw_paths_without_bound_children": len(missing_continuations),
        "affected_root_cases": len({row["root_case_id"] for row in missing_continuations}),
        "missing_continuation_examples": missing_continuations[:20],
        "per_presentation_child_set_mismatch_count": len(per_path_child_set_failures),
        "merged_state_provenance_dependent_child_set_count": len(merged_child_set_disagreements),
        "state_level_child_set_mismatch_count": len(state_level_child_set_failures),
        "per_presentation_child_set_examples": per_path_child_set_failures[:20],
        "merged_child_set_disagreement_examples": merged_child_set_disagreements[:20],
        "terminal_counts": dict(sorted(terminal_counts.items())),
        "probe_counts": dict(sorted(probe_counts.items())),
        "allowed_terminal_reclassification": dict(sorted(terminal_reclassification.items())),
        "allowed_terminal_rows": allowed_terminal_rows,
        "class_sample_path_count": len(class_sample_records),
        "class_sample_state_count": len(sampled_state_ids),
        "class_sample": class_sample_records,
        "algebra_replay_counts": dict(sorted(algebra_counts.items())),
        "unique_strict_polynomial_count": len(sign_cache),
        "derived_raw_to_canonical_maps": derived_maps,
    }


def git_tracked(path: Path) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(path.relative_to(PROJECT.parent))],
        cwd=PROJECT.parent,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "audit_certificate.json")
    parser.add_argument("--stream", action="append", type=Path, help="explicit primary stream; repeatable")
    parser.add_argument("--use-supplied-bit-cache", action="store_true", help="debug only; final audit must omit")
    parser.add_argument("--skip-algebra", action="store_true", help="debug only; final audit must omit")
    args = parser.parse_args()
    started = time.monotonic()
    streams = tuple(args.stream) if args.stream else STREAMS
    states, paths, stream_audit = read_streams(streams)
    inventory = build_inventory(recompute_all_descriptor_bits=not args.use_supplied_bit_cache)
    semantics = semantic_audit(states, paths, inventory, verify_all_algebra=not args.skip_algebra)
    leaf_regression_graph = RootedGraph(
        0,
        ((1, "leaf_A"), (2, "leaf_B")),
        ((0, 1), (0, 2)),
    )
    leaf_regression = {
        "rooted_tree_child": rooted_tree_child(leaf_regression_graph),
        "internal_vertex_audit": internal_vertex_audit(leaf_regression_graph),
        "assertion": "leaves are excluded from the internal-vertex quantifier",
    }
    if not leaf_regression["rooted_tree_child"] or not leaf_regression["internal_vertex_audit"]["passes"] or leaf_regression["internal_vertex_audit"]["checked_vertex_count"] != 1:
        semantics["failures"].append({"type": "leaf_quantifier_regression_failure", "detail": leaf_regression})
    all_failures = [*stream_audit["failures"], *semantics["failures"]]
    input_hashes = {
        str(path.relative_to(PROJECT)): file_sha(path)
        for path in (*streams, CORE_PATH, SUPPORT_PATH, INVARIANT_PATH, BIT_CACHE_PATH, PRODUCER_PATH)
    }
    tracked = {
        str(path.relative_to(PROJECT)): git_tracked(path)
        for path in (*streams, PRODUCER_PATH)
    }
    payload = {
        "schema": "final-hard-cover-adversary-v1",
        "status": "FALSE" if all_failures else "VERIFIED",
        "scope": "five primary/certificates/hard_cover_n3_*_all streams",
        "independence": "imports no primary module and regenerates graph-to-polynomial bindings",
        "inputs": input_hashes,
        "git_tracked": tracked,
        "stream_audit": stream_audit,
        "independent_inventory": {
            "source_signatures": inventory.source_signature_count,
            "target_signatures": inventory.target_signature_count,
            "common_signatures": inventory.common_signature_count,
            "root_cases": len(inventory.root_cases),
            "root_case_commitment_sha256": stable_hash(sorted(inventory.root_cases.items())),
            "descriptor_count_recomputed": len(inventory.descriptor_bits),
            "invariant_orbit_sha256": inventory.invariant_orbit_sha256,
        },
        "semantic_audit": semantics,
        "tree_child_leaf_quantifier_regression": leaf_regression,
        "failure_count": len(all_failures),
        "failures": all_failures,
        "elapsed_seconds": time.monotonic() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "failure_count": payload["failure_count"],
        "root_cases": len(inventory.root_cases),
        "states": len(states),
        "paths": len(paths),
        "missing_continuations": semantics["nonterminal_raw_paths_without_bound_children"],
        "output": str(args.output),
        "sha256": file_sha(args.output),
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))
    # A falsification is the expected successful outcome of this adversarial
    # program, so writing a FALSE certificate does not make the process fail.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
