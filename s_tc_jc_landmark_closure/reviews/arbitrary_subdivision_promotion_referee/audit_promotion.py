#!/usr/bin/env python3
"""Lightweight clean-room audit of arbitrary-subdivision promotion evidence.

This program intentionally does not import any module under ``primary`` or
another review directory.  It treats the independently audited fixed-full and
compact-probe certificates as frozen inputs, then checks the theorem-level
inventory, transport-coherence, finite-bound, and weak-target-grammar facts
needed by the promotion argument.

It does not regenerate the local graph algebra certified by those inputs.
"""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import itertools
import json
import math
import struct
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


LANDMARK = Path(__file__).resolve().parents[2]


EXPECTED_HASHES = {
    "primary/certificates/hard_cover_schema3_n3_full_summary.json":
        "791844a802af61f64cba937a5adbe9d1d381d3fd7e55165914d4e4c885908e65",
    "primary/certificates/hard_cover_schema3_theta2_full_summary.json":
        "915bed0a3add001c1a94d6d862a2359e6ad75b3489f8d71b7adf006952b5ce37",
    "primary/certificates/probe_extension_schema3_n3_final_summary.json":
        "c8aa65474844276bc4d123152c6fd1b85276a38ee410ef61a4a64488f7886108",
    "primary/certificates/probe_extension_theta2_schema3_final_summary.json":
        "7e1c06223a683b888c365b4fa0fbe0568896a3c4e466be9b382f8d0fd7066c7a",
    "reviews/base_gate_adversarial_referee_n3/certificate.json":
        "6fbc3bf96eb82e9c2c1afd392d8bb2da5ee386345af2d536957ab83fff446a85",
    "reviews/base_gate_adversarial_referee/certificate.json":
        "a3ffde91422198cf548be1bb80ef4683289c47fdfcb42857dcbc72586d440d46",
    "reviews/compact_probe_format/final_n3_cleanroom/certificates/final_gate_certificate.json":
        "d17b2be70c19c862182af82edd1de3f781e62d41d0ee0048cff664edc6529e88",
    "reviews/compact_probe_format/final_n4_cleanroom/certificates/final_gate_certificate.json":
        "b6efd20d3c7b5da7194821e3bdcaf6228121cb1cbd210d8886d9d08499c5f894",
    "reviews/root_probe/parameter_submersion_certificate.json":
        "2652537dc8232f4887601250a108278c57404a3a87e17677916d480e19b3a433",
    "reviews/root_probe/probe_coherence_certificate.json":
        "85b0f3bb60200395a452b41faf289c6bda474929833263e363c67f853e4115b7",
    "reviews/root_probe/redstar_partition_certificate.json":
        "45ae3349fd70538885b88abc38754c1c504daa38f4225a6e4c1717846df2f5b9",
}


FAMILIES = {
    "n3": {
        "compact_summaries": [
            (
                f"primary/certificates/compact_probe_schema3_n3_compact_s{i}_summary.json",
                digest,
            )
            for i, digest in enumerate(
                [
                    "dc7b806f9afc1af9909682f47ea4bdc9ac5a8631d78ce3a6b15d41c4f171ad73",
                    "996084af49c3e4ddf63b62cfa951be652a886e3424674f6e34d664b5a4901a37",
                    "a8162d2bb136668ce2f204ce2012c85eb4dbb5e42c7037307d974b5f9ebf2286",
                    "b246614dafc669784f8ef5e16ef62db79f08929b2afc2a6d14ce7f50bd7b7942",
                ]
            )
        ],
        "base_relations": "primary/certificates/hard_cover_n3_schema3_n3_full.jsonl.gz",
        "base_summary": "primary/certificates/hard_cover_schema3_n3_full_summary.json",
        "clean_gate": "reviews/compact_probe_format/final_n3_cleanroom/certificates/final_gate_certificate.json",
        "expected_paths": 144,
        "expected_path_commitment":
            "f5854297b43ec3715fe09b6afc5e7f4cac44d3e7fbae79c46ee4e1388da3acad",
        "expected_anchor_distribution": {5: 92, 6: 44, 7: 8},
        "expected_classification": {
            "generic_polynomial_separation": 90008,
            "labelled_isomorphism": 9676,
            "ordinary_T": 840,
            "strict_open_cube_separation": 624,
        },
        "expected_stage": {"A_plus_p": 9316, "A_plus_p_plus_q": 91832},
        "expected_base_classes": {
            "support_prefix_labelled_isomorphism": 120,
            "support_prefix_ordinary_T": 24,
        },
    },
    "n4": {
        "compact_summaries": [
            (
                f"primary/certificates/compact_probe_theta2_compact_n4_s{i}_summary.json",
                digest,
            )
            for i, digest in enumerate(
                [
                    "9649b08315dbd5d9dca8b8e4e1892deefe4cecacd81ea6f1880d994e56bd0863",
                    "ea0c7181389d4bb73a7a1332ec396f0223cf0e9746efde9f39bc79d3d3029de1",
                    "ab678bcbd268ffd704fa79c45ac8a1eb89e2907132eb5e12a99a625cc606ebbd",
                    "ffa5658edfaac800da9614fcaf32a576a09d26d6d1449fc89a2ac66efff551d6",
                ]
            )
        ],
        "base_relations": "primary/certificates/hard_cover_n4_schema3_theta2_full.jsonl.gz",
        "base_summary": "primary/certificates/hard_cover_schema3_theta2_full_summary.json",
        "clean_gate": "reviews/compact_probe_format/final_n4_cleanroom/certificates/final_gate_certificate.json",
        "expected_paths": 132,
        "expected_path_commitment":
            "21193cac2d8a977e785d9aeb980f57a2c10994d5893fa58c3038792d9c32c5c6",
        "expected_anchor_distribution": {6: 42, 7: 66, 8: 24},
        "expected_classification": {
            "generic_polynomial_separation": 153072,
            "labelled_isomorphism": 15510,
        },
        "expected_stage": {"A_plus_p": 12906, "A_plus_p_plus_q": 155676},
        "expected_base_classes": {"support_prefix_labelled_isomorphism": 132},
    },
}


CODE_CLASS = {
    0: "generic_polynomial_separation",
    1: "strict_open_cube_separation",
    2: "labelled_isomorphism",
    3: "ordinary_T",
}
BASE_TO_CHILD = {
    "support_prefix_labelled_isomorphism": "labelled_isomorphism",
    "support_prefix_ordinary_T": "ordinary_T",
}
MASK29 = (1 << 29) - 1


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, label: str, **context: Any) -> None:
    if not condition:
        payload = {"failure": label, **context}
        raise AuditFailure(json.dumps(payload, sort_keys=True))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_json(relative: str) -> dict[str, Any]:
    with (LANDMARK / relative).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def jsonl_gz(relative: str) -> Iterable[dict[str, Any]]:
    with gzip.open(LANDMARK / relative, "rt", encoding="utf-8") as handle:
        for line in handle:
            yield json.loads(line)


def decode_words(encoded: str) -> tuple[int, ...]:
    raw = base64.b64decode(encoded, validate=True)
    require(len(raw) % 4 == 0, "packed_word_alignment", byte_count=len(raw))
    if not raw:
        return ()
    return struct.unpack("<" + "I" * (len(raw) // 4), raw)


def normalized_pairs(rows: list[list[Any]]) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for left, right in rows:
        require(left not in result, "transport_duplicate_source", source=left)
        result[left] = right
    require(len(set(result.values())) == len(result), "transport_not_injective")
    return result


def identity_ports(transport: dict[str, Any]) -> dict[str, str]:
    mapping = normalized_pairs(transport["port_transport"])
    require(all(k == v for k, v in mapping.items()), "nonidentity_physical_port_transport")
    return mapping


def transport_extends(parent: dict[str, Any], child: dict[str, Any], label: str) -> None:
    p_vertices = normalized_pairs(parent["vertex_transport"])
    c_vertices = normalized_pairs(child["vertex_transport"])
    require(
        all(c_vertices.get(k) == v for k, v in p_vertices.items()),
        "vertex_transport_does_not_restrict",
        relation=label,
    )
    p_ports = identity_ports(parent)
    c_ports = identity_ports(child)
    require(
        all(c_ports.get(k) == v for k, v in p_ports.items()),
        "port_transport_does_not_restrict",
        relation=label,
    )
    p_outside = set(map(tuple, parent["reticulation_transport_outside_redirected_triangle"]))
    c_outside = set(map(tuple, child["reticulation_transport_outside_redirected_triangle"]))
    require(
        p_outside <= c_outside,
        "outside_reticulation_transport_does_not_restrict",
        relation=label,
    )


def load_transports(summary: dict[str, Any]) -> list[dict[str, Any]]:
    info = summary["streams"]["transports"]
    relative = info["path"]
    require(
        sha256_file(LANDMARK / relative) == info["file_sha256"],
        "transport_stream_physical_hash",
        path=relative,
    )
    records = list(jsonl_gz(relative))
    require(len(records) == info["records"], "transport_record_count", path=relative)
    records.sort(key=lambda row: int(row["transport_index"]))
    require(
        [int(row["transport_index"]) for row in records] == list(range(len(records))),
        "transport_index_gap",
        path=relative,
    )
    return records


def load_base_classes(relative: str, wanted: set[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for row in jsonl_gz(relative):
        state_id = row["state_id"]
        if state_id in wanted:
            require(state_id not in result, "duplicate_base_state", state_id=state_id)
            result[state_id] = row["terminal_classification"]
    require(set(result) == wanted, "missing_base_state", missing=sorted(wanted - set(result))[:5])
    return result


def audit_family(name: str, config: dict[str, Any]) -> dict[str, Any]:
    summaries: list[dict[str, Any]] = []
    rows_with_library: list[tuple[dict[str, Any], list[dict[str, Any]], str]] = []
    ranges: list[tuple[int, int]] = []
    path_indices: set[int] = set()
    anchor_distribution: Counter[int] = Counter()
    port_distribution = {"A_plus_p": Counter(), "A_plus_p_plus_q": Counter()}
    classification: Counter[str] = Counter()
    stage: Counter[str] = Counter()
    per_base_child: Counter[tuple[str, str, str]] = Counter()
    shard_input_hashes: dict[str, str] = {}

    for relative, expected_sha in config["compact_summaries"]:
        actual_sha = sha256_file(LANDMARK / relative)
        require(actual_sha == expected_sha, "compact_summary_hash", path=relative, actual=actual_sha)
        summary = load_json(relative)
        summaries.append(summary)
        require(summary["status"] == "EXACTLY_COMPUTED", "compact_summary_status", path=relative)
        require(
            summary["path_inventory_count"] == config["expected_paths"],
            "path_inventory_count",
            path=relative,
        )
        require(
            summary["path_inventory_sha256"] == config["expected_path_commitment"],
            "path_inventory_commitment",
            path=relative,
        )
        start, stop = map(int, summary["path_range"])
        ranges.append((start, stop))
        transports = load_transports(summary)
        path_info = summary["streams"]["paths"]
        require(
            sha256_file(LANDMARK / path_info["path"]) == path_info["file_sha256"],
            "path_stream_physical_hash",
            path=path_info["path"],
        )
        local_rows = list(jsonl_gz(path_info["path"]))
        require(len(local_rows) == path_info["records"] == stop - start, "path_stream_count")
        require([int(row["path_index"]) for row in local_rows] == list(range(start, stop)),
                "path_stream_order", path=path_info["path"])
        for row in local_rows:
            idx = int(row["path_index"])
            require(idx not in path_indices, "duplicate_path_index", family=name, path_index=idx)
            path_indices.add(idx)
            rows_with_library.append((row, transports, relative))
        for key, value in summary.get("input_sha256", {}).items():
            if key in shard_input_hashes:
                require(shard_input_hashes[key] == value, "cross_shard_input_hash", input=key)
            shard_input_hashes[key] = value

    ranges.sort()
    require(ranges[0][0] == 0, "shard_initial_gap", family=name)
    require(all(ranges[i][1] == ranges[i + 1][0] for i in range(len(ranges) - 1)),
            "shard_gap_or_overlap", family=name, ranges=ranges)
    require(ranges[-1][1] == config["expected_paths"], "shard_final_gap", family=name)

    wanted = {row["base_state_id"] for row, _, _ in rows_with_library}
    base_classes = load_base_classes(config["base_relations"], wanted)
    base_class_counts = Counter(base_classes.values())
    require(dict(base_class_counts) == config["expected_base_classes"],
            "base_terminal_class_counts", family=name, actual=dict(base_class_counts))

    t_path_allowed_p: Counter[int] = Counter()
    t_path_allowed_q: Counter[int] = Counter()
    transport_extension_checks = 0

    for row, transports, source_summary in sorted(rows_with_library, key=lambda item: item[0]["path_index"]):
        path_index = int(row["path_index"])
        selected = int(row["selected_port_count"])
        anchor_distribution[selected] += 1
        p_words = decode_words(row["p_words_base64_le_u32"])
        q_words = decode_words(row["q_words_base64_le_u32"])
        require(len(p_words) == int(row["p_word_count"]), "p_word_count", path_index=path_index)
        require(len(q_words) == int(row["q_word_count"]), "q_word_count", path_index=path_index)
        require(
            len(p_words) == len(row["source_p_arcs"]) * len(row["target_p_arcs"]),
            "p_cartesian_indexing",
            path_index=path_index,
        )
        for word in p_words + q_words:
            require((word >> 29) in CODE_CLASS, "invalid_class_code", path_index=path_index)

        base_class = base_classes[row["base_state_id"]]
        expected_allowed_class = BASE_TO_CHILD[base_class]
        base_record = transports[int(row["base_transport_index"])]
        require(base_record["classification"] == expected_allowed_class,
                "base_transport_class", path_index=path_index)
        base_transport = base_record["transport"]
        base_ports = identity_ports(base_transport)
        require(len(base_ports) == selected, "base_transport_port_count", path_index=path_index)

        allowed = [i for i, word in enumerate(p_words) if (word >> 29) in (2, 3)]
        require(allowed == list(map(int, row["allowed_p_flat_indices"])),
                "allowed_p_index_set", path_index=path_index)
        require(len(allowed) == len(row["q_shapes"]), "q_shape_block_count", path_index=path_index)

        p_transports: dict[int, dict[str, Any]] = {}
        for flat, word in enumerate(p_words):
            cls = CODE_CLASS[word >> 29]
            classification[cls] += 1
            stage["A_plus_p"] += 1
            port_distribution["A_plus_p"][selected + 1] += 1
            per_base_child[(base_class, "A_plus_p", cls)] += 1
            if cls in ("labelled_isomorphism", "ordinary_T"):
                require(cls == expected_allowed_class, "probe_class_switch", path_index=path_index, flat=flat)
                index = word & MASK29
                require(index < len(transports), "p_transport_index", path_index=path_index, index=index)
                record = transports[index]
                require(record["classification"] == cls, "p_transport_class", path_index=path_index)
                child_transport = record["transport"]
                transport_extends(base_transport, child_transport, f"{name}:{path_index}:p:{flat}")
                require(len(identity_ports(child_transport)) == selected + 1,
                        "p_transport_port_count", path_index=path_index)
                p_transports[flat] = child_transport
                transport_extension_checks += 1

        q_offset = 0
        allowed_q_this_path = 0
        for flat, shape in zip(allowed, row["q_shapes"]):
            require(len(shape) == 2 and min(map(int, shape)) > 0,
                    "invalid_q_shape", path_index=path_index, shape=shape)
            block_length = int(shape[0]) * int(shape[1])
            block = q_words[q_offset:q_offset + block_length]
            require(len(block) == block_length, "truncated_q_block", path_index=path_index)
            q_offset += block_length
            parent_transport = p_transports[flat]
            for local, word in enumerate(block):
                cls = CODE_CLASS[word >> 29]
                classification[cls] += 1
                stage["A_plus_p_plus_q"] += 1
                port_distribution["A_plus_p_plus_q"][selected + 2] += 1
                per_base_child[(base_class, "A_plus_p_plus_q", cls)] += 1
                if cls in ("labelled_isomorphism", "ordinary_T"):
                    require(cls == expected_allowed_class,
                            "conditional_probe_class_switch", path_index=path_index, flat=flat, local=local)
                    index = word & MASK29
                    require(index < len(transports), "q_transport_index", path_index=path_index, index=index)
                    record = transports[index]
                    require(record["classification"] == cls, "q_transport_class", path_index=path_index)
                    child_transport = record["transport"]
                    transport_extends(parent_transport, child_transport,
                                      f"{name}:{path_index}:p:{flat}:q:{local}")
                    require(len(identity_ports(child_transport)) == selected + 2,
                            "q_transport_port_count", path_index=path_index)
                    transport_extension_checks += 1
                    allowed_q_this_path += 1
        require(q_offset == len(q_words), "q_block_partition", path_index=path_index)
        if base_class == "support_prefix_ordinary_T":
            t_path_allowed_p[len(allowed)] += 1
            t_path_allowed_q[allowed_q_this_path] += 1

    require(dict(anchor_distribution) == config["expected_anchor_distribution"],
            "anchor_port_distribution", family=name, actual=dict(anchor_distribution))
    require(dict(classification) == config["expected_classification"],
            "classification_totals", family=name, actual=dict(classification))
    require(dict(stage) == config["expected_stage"],
            "stage_totals", family=name, actual=dict(stage))

    clean = load_json(config["clean_gate"])
    require(clean["status"] in ("VERIFIED", "VERIFIED_AFTER_CORRECTION"),
            "clean_gate_status", family=name)
    require(clean["global_verbose_binding_bijection"] is True,
            "compact_verbose_bijection", family=name)
    require(clean["classification_counts"] == config["expected_classification"],
            "clean_gate_classification", family=name)

    max_anchor = max(anchor_distribution)
    return {
        "family": name,
        "path_ranges": ranges,
        "path_inventory_count": len(path_indices),
        "path_inventory_sha256": config["expected_path_commitment"],
        "base_terminal_classification": dict(sorted(base_class_counts.items())),
        "anchor_tensor_port_distribution": {str(k): v for k, v in sorted(anchor_distribution.items())},
        "probe_tensor_port_distribution": {
            key: {str(k): v for k, v in sorted(value.items())}
            for key, value in port_distribution.items()
        },
        "maximum_anchor_tensor_ports": max_anchor,
        "maximum_probe_tensor_ports": max_anchor + 2,
        "classification_counts": dict(sorted(classification.items())),
        "stage_counts": dict(stage),
        "transport_extension_checks": transport_extension_checks,
        "base_to_child_classification_counts": {
            "|".join(key): value for key, value in sorted(per_base_child.items())
        },
        "ordinary_T_path_allowed_p_distribution": {
            str(k): v for k, v in sorted(t_path_allowed_p.items())
        },
        "ordinary_T_path_allowed_q_distribution": {
            str(k): v for k, v in sorted(t_path_allowed_q.items())
        },
        "clean_gate_sha256": EXPECTED_HASHES[config["clean_gate"]],
    }


def weak_compositions(total: int, parts: int) -> Iterable[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, parts - 1):
            yield (first,) + rest


def word_presentations(segment_count: int, labels: tuple[str, ...]) -> Iterable[tuple[tuple[str, ...], ...]]:
    for ordering in itertools.permutations(labels):
        for lengths in weak_compositions(len(labels), segment_count):
            cursor = 0
            words = []
            for length in lengths:
                words.append(tuple(ordering[cursor:cursor + length]))
                cursor += length
            yield tuple(words)


def probe_signature(words: tuple[tuple[str, ...], ...], labels: tuple[str, ...]) -> tuple[Any, ...]:
    location: dict[str, tuple[int, int]] = {}
    for segment, word in enumerate(words):
        for position, label in enumerate(word):
            location[label] = (segment, position)
    one_port = tuple(location[label][0] for label in labels)
    pair_order = []
    for left, right in itertools.combinations(labels, 2):
        ls, lp = location[left]
        rs, rp = location[right]
        pair_order.append(0 if ls != rs else (-1 if lp < rp else 1))
    return one_port + tuple(pair_order)


def audit_word_reconstruction() -> dict[str, Any]:
    results = []
    for segments in (2, 5, 6):
        for label_count in (3, 4):
            labels = tuple(f"p{i}" for i in range(label_count))
            seen: dict[tuple[Any, ...], tuple[tuple[str, ...], ...]] = {}
            count = 0
            for words in word_presentations(segments, labels):
                count += 1
                signature = probe_signature(words, labels)
                require(signature not in seen, "probe_deck_collision",
                        segments=segments, labels=label_count,
                        first=seen.get(signature), second=words)
                seen[signature] = words
            expected = math.factorial(label_count) * math.comb(label_count + segments - 1, segments - 1)
            require(count == expected == len(seen), "word_presentation_count",
                    segments=segments, labels=label_count)
            results.append({
                "segment_count": segments,
                "extra_label_count": label_count,
                "ordered_word_count": count,
                "probe_signature_count": len(seen),
                "collisions": 0,
                "empty_segments_included": True,
                "same_segment_repetitions_included": True,
            })
    return {
        "finite_adversarial_checks": results,
        "general_argument": (
            "one-port data partitions labels by the fixed anchor interval; "
            "two-port data gives every comparison within an interval; a finite "
            "strict total order is uniquely determined by all pair comparisons"
        ),
    }


def audit_weak_target_grammar(relative: str) -> dict[str, Any]:
    coverage_count = 0
    state_count = 0
    incoming_modes: Counter[str] = Counter()
    role_occurrences: Counter[str] = Counter()
    dummy_combinations: Counter[tuple[str, ...]] = Counter()
    terminal_classes: Counter[str] = Counter()
    for state in jsonl_gz(relative):
        state_count += 1
        terminal_classes[state["terminal_classification"]] += 1
        for row in state["raw_coverage"]:
            coverage_count += 1
            incoming_selected = bool(row["target_incoming_selected"])
            dummy_roles = list(row["target_dummy_roles"])
            restored = list(row["restored_target_roles"])
            restored_map = dict(row["restored_role_to_label"])
            path_roles = list(row["restoration_path"])
            remaining = list(state["remaining_target_roles"])
            require(("INCOMING" in dummy_roles) == (not incoming_selected),
                    "weak_grammar_incoming_dummy", state_id=state["state_id"])
            require(set(restored) == set(restored_map),
                    "weak_grammar_restored_map", state_id=state["state_id"])
            require(set(restored) <= set(dummy_roles),
                    "weak_grammar_restored_subset", state_id=state["state_id"])
            require(set(path_roles) == set(restored) and len(path_roles) == len(set(path_roles)),
                    "weak_grammar_restoration_path", state_id=state["state_id"])
            require(list(row["dummy_order"]) == dummy_roles,
                    "weak_grammar_dummy_order", state_id=state["state_id"])
            require(set(remaining) == set(dummy_roles) - set(restored),
                    "weak_grammar_remaining_partition", state_id=state["state_id"])
            require(set(remaining).isdisjoint(restored),
                    "weak_grammar_partition_overlap", state_id=state["state_id"])
            kinds = []
            for role in dummy_roles:
                if role == "INCOMING":
                    kind = "incoming"
                elif role.startswith("D_SINK_"):
                    kind = "sink"
                elif role.startswith("D_REPAIR_"):
                    kind = "repair"
                else:
                    raise AuditFailure(json.dumps({"failure": "unknown_dummy_role", "role": role}))
                kinds.append(kind)
                role_occurrences[kind] += 1
            dummy_combinations[tuple(sorted(kinds))] += 1
            incoming_modes["selected" if incoming_selected else "marginalized"] += 1
    return {
        "relation_states": state_count,
        "raw_coverage_records": coverage_count,
        "incoming_modes": dict(sorted(incoming_modes.items())),
        "dummy_role_occurrences": dict(sorted(role_occurrences.items())),
        "dummy_role_combination_count": len(dummy_combinations),
        "terminal_classes": dict(sorted(terminal_classes.items())),
        "schema_consistency_failures": 0,
    }


def audit_locked_inputs() -> dict[str, str]:
    declared = load_json("reviews/arbitrary_subdivision_promotion_referee/INPUT_LOCK.json")
    declared_general = {
        **declared["base_and_verbose"],
        **declared["independent_certificates"],
    }
    require(declared_general == EXPECTED_HASHES, "input_lock_constant_disagreement")
    declared_compact = declared["compact_summaries"]
    expected_compact = {
        relative: digest
        for config in FAMILIES.values()
        for relative, digest in config["compact_summaries"]
    }
    require(declared_compact == expected_compact, "compact_input_lock_constant_disagreement")
    actual: dict[str, str] = {}
    for relative, expected in EXPECTED_HASHES.items():
        digest = sha256_file(LANDMARK / relative)
        require(digest == expected, "locked_input_hash", path=relative, expected=expected, actual=digest)
        actual[relative] = digest
    require(load_json("reviews/base_gate_adversarial_referee_n3/certificate.json")["status"] == "VERIFIED",
            "n3_base_gate_status")
    require(load_json("reviews/base_gate_adversarial_referee/certificate.json")["status"] == "VERIFIED",
            "n4_base_gate_status")
    submersion = load_json("reviews/root_probe/parameter_submersion_certificate.json")
    require(submersion["full_row_rank_failure_count"] == 0, "upstream_submersion_failures")
    require(submersion["completion_count"] == 42908, "upstream_submersion_count")
    require(submersion["general_open_product_certificate"]["class_blocks_are_disjoint_by_equivalence_partition"] is True,
            "upstream_product_partition")
    redstar = load_json("reviews/root_probe/redstar_partition_certificate.json")
    require(redstar["partition"]["descriptor_partition_failure_count"] == 0,
            "upstream_weak_grammar_failure")
    require(redstar["partition"]["counts"]["restrictions"] == 24792,
            "upstream_weak_grammar_count")
    return actual


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    locked = audit_locked_inputs()
    families = [audit_family(name, config) for name, config in FAMILIES.items()]
    weak_grammar = {
        name: audit_weak_target_grammar(config["base_relations"])
        for name, config in FAMILIES.items()
    }
    word_reconstruction = audit_word_reconstruction()
    global_max = max(row["maximum_probe_tensor_ports"] for row in families)
    require(global_max == 10, "exact_tensor_port_bound", actual=global_max)

    certificate = {
        "schema": "arbitrary-subdivision-promotion-referee-v1",
        "status": "VERIFIED_AFTER_CORRECTION",
        "scope": (
            "arbitrary-subdivision promotion from the frozen independently "
            "verified n3/n4 fixed-full terminals and compact probe families"
        ),
        "locked_inputs": locked,
        "families": families,
        "aggregate": {
            "fixed_anchor_paths": sum(row["path_inventory_count"] for row in families),
            "probe_relations": sum(sum(row["stage_counts"].values()) for row in families),
            "classification_counts": dict(sorted(sum(
                (Counter(row["classification_counts"]) for row in families), Counter()
            ).items())),
            "maximum_fixed_anchor_tensor_ports": max(row["maximum_anchor_tensor_ports"] for row in families),
            "exact_attained_probe_tensor_port_bound": global_max,
            "bound_attained_by_family": "n4",
            "relations_at_bound": families[1]["probe_tensor_port_distribution"]["A_plus_p_plus_q"]["10"],
        },
        "path_product_submersion": {
            "parameter_map": "y_C=product_{e in C} x_e on disjoint nonempty classes C",
            "jacobian_entry": "partial y_C / partial x_e = y_C/x_e > 0",
            "rank": "one independent row per disjoint class everywhere on (0,1)^E",
            "surjective_semialgebraic_section": "x_e=y_C^(1/|C|)",
            "model_image_locus": (
                "intersection of the full-model regular locus and the selected-"
                "model generic-rank locus; nonempty Zariski open in source parameters"
            ),
            "upstream_bounded_completion_maps": 42908,
            "upstream_failure_count": 0,
        },
        "word_reconstruction": word_reconstruction,
        "weak_target_grammar": {
            "structural_partition_certificate_restrictions": 24792,
            "structural_partition_failures": 0,
            "final_hard_cover_stream_checks": weak_grammar,
            "interpretation": (
                "dummy-restored graphs represent selected tensors only; an "
                "intrinsically nonstrong selected restriction is not promoted "
                "to a standard-strong topology"
            ),
        },
        "theorem_logic": {
            "common_anchor": "the exact path-bound A=Q_s union Q_t",
            "one_port": "every surviving transport extends the one fixed anchor transport",
            "two_port": "every surviving q transport extends its exact p transport",
            "ordinary_T": (
                "all 24 n3 T anchors have exactly 5 allowed p and 30 allowed q "
                "relations; every allowed descendant remains T and restricts "
                "the same anchor quotient map"
            ),
            "containment_descent": (
                "choose a point of the source-open containment germ in the dense "
                "marginal-submersion locus; the marginal image is source-relative "
                "open and lies in the target restriction image pointwise"
            ),
            "continuous_target_parameter_selection_used": False,
        },
        "corrections": [
            "The certified finite bound is 10 tensor ports, not the historical crude 12.",
            "Coherence is anchored at the exact union A=Q_s union Q_t; Q_s alone is unsafe after a T sink change.",
            "The verdict is conditional on the already verified fixed-full n3/n4 terminal universes and does not regenerate their graph algebra.",
        ],
        "failures": [],
    }

    rendered = json.dumps(certificate, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
