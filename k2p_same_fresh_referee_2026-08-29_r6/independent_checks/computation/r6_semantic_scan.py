#!/usr/bin/env python3
"""Reviewer-owned semantic scan of the R6 K2P computational package.

The scan deliberately does not import a submitted classifier as its decision
procedure.  It reconstructs raw coordinates and primitive encodings, streams
the corrected ledgers, checks restoration/probe/parameter joins, audits the
verifier-facing composite mutation reports and code paths, and attacks the
typed printed-anchor gate with the actual strict-sign overlay.
"""

from __future__ import annotations

import argparse
import ast
import collections
import gzip
import hashlib
import importlib.util
import itertools
import json
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


class Failure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise Failure(code if detail is None else f"{code}:{detail}")


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def sha_object(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def unique_hook(label: str):
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, "DUPLICATE_JSON_NAME", f"{label}:{key}")
            result[key] = value
        return result

    return hook


def decode(data: bytes, label: str, *, canonical_line: bool = False) -> Any:
    try:
        value = json.loads(
            data.decode("utf-8"),
            object_pairs_hook=unique_hook(label),
            parse_constant=lambda token: (_ for _ in ()).throw(
                Failure(f"NONFINITE_JSON:{label}:{token}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Failure(f"JSON_DECODE:{label}:{error}") from error
    if canonical_line:
        require(data == canonical(value) + b"\n", "NONCANONICAL_JSON", label)
    return value


def load_json(path: Path) -> dict[str, Any]:
    value = decode(path.read_bytes(), path.as_posix())
    require(isinstance(value, dict), "JSON_NOT_OBJECT", path)
    return value


def load_gzip_document(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rb") as handle:
        plain = handle.read()
    value = decode(plain, path.as_posix(), canonical_line=True)
    require(isinstance(value, dict), "GZIP_JSON_NOT_OBJECT", path)
    return value


def verify_payload(document: dict[str, Any], label: str) -> None:
    body = dict(document)
    claimed = body.pop("payload_sha256", None)
    require(claimed == sha_object(body), "PAYLOAD_HASH", label)


CORES = {
    "cycle": {
        "arcs": (("S", "X"), ("S", "X")),
        "retics": ("X",),
        "sinks": ("X",),
        "repairs": ((0,), (1,)),
    },
    "theta0": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X"), ("V", "X"), ("U", "V")),
        "retics": ("V", "X"),
        "sinks": ("X",),
        "repairs": ((2, 3), (3, 4)),
    },
    "theta1": {
        "arcs": (("S", "U"), ("S", "X"), ("V", "X"), ("U", "V"), ("U", "V")),
        "retics": ("V", "X"),
        "sinks": ("X",),
        "repairs": ((2, 3), (2, 4)),
    },
    "theta2": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1")),
        "retics": ("X0", "X1"),
        "sinks": ("X0", "X1"),
        "repairs": ((2, 3), (2, 5), (3, 4), (4, 5)),
    },
    "theta3": {
        "arcs": (("S", "U"), ("S", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V")),
        "retics": ("X0", "X1"),
        "sinks": ("X0", "X1"),
        "repairs": ((2,), (4,)),
    },
}


def weak_compositions(total: int, bins: int) -> Iterable[tuple[int, ...]]:
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, bins - 1):
            yield (first,) + tail


@dataclass(frozen=True)
class Primitive:
    core: str
    incoming_selected: bool
    repair: int | None
    sink_mask: int
    words: tuple[tuple[object, ...], ...]
    sinks: tuple[tuple[str, object], ...]
    incoming: object


def targets(k: int) -> tuple[Primitive, ...]:
    rows: list[Primitive] = []
    for incoming_selected in (True, False):
        nout = k - 1 if incoming_selected else k
        for core, spec in CORES.items():
            for mask in range(1 << len(spec["sinks"])):
                ordinary = nout - mask.bit_count()
                if ordinary < 0:
                    continue
                for counts in weak_compositions(ordinary, len(spec["arcs"])):
                    labels = iter(range(1 if incoming_selected else 0, k))
                    selected = tuple(
                        tuple(next(labels) for _ in range(count)) for count in counts
                    )
                    repairs = ((None, ()),) if core == "cycle" else tuple(enumerate(spec["repairs"]))
                    for repair_index, repair in repairs:
                        words = [list(word) for word in selected]
                        for arc_index in repair:
                            if not words[arc_index]:
                                words[arc_index].append(
                                    f"D_REPAIR_{repair_index}_{arc_index}"
                                )
                        used = [item for word in selected for item in word]
                        next_label = max(used) + 1 if used else (1 if incoming_selected else 0)
                        sink_rows = []
                        for index, sink in enumerate(spec["sinks"]):
                            if mask >> index & 1:
                                value: object = next_label
                                next_label += 1
                            else:
                                value = f"D_SINK_{index}"
                            sink_rows.append((sink, value))
                        primitive = Primitive(
                            core,
                            incoming_selected,
                            repair_index,
                            mask,
                            tuple(tuple(word) for word in words),
                            tuple(sink_rows),
                            0 if incoming_selected else "INCOMING",
                        )
                        selected_labels = sorted(
                            item
                            for word in primitive.words
                            for item in word
                            if type(item) is int
                        ) + sorted(
                            value for _, value in primitive.sinks if type(value) is int
                        )
                        if type(primitive.incoming) is int:
                            selected_labels.append(primitive.incoming)
                        require(sorted(selected_labels) == list(range(k)), "TARGET_LABELS")
                        rows.append(primitive)
    return tuple(rows)


def sources(core_names: tuple[str, ...]) -> tuple[Primitive, ...]:
    rows = []
    for core in core_names:
        spec = CORES[core]
        for repair_index, repair in enumerate(spec["repairs"]):
            words: list[list[object]] = [[] for _ in spec["arcs"]]
            next_label = 1
            for arc_index in repair:
                words[arc_index].append(next_label)
                next_label += 1
            sink_rows = []
            for sink in spec["sinks"]:
                sink_rows.append((sink, next_label))
                next_label += 1
            rows.append(
                Primitive(
                    core,
                    True,
                    repair_index,
                    (1 << len(spec["sinks"])) - 1,
                    tuple(tuple(word) for word in words),
                    tuple(sink_rows),
                    0,
                )
            )
    return tuple(rows)


def graph_encoding(primitive: Primitive, permutation: tuple[int, ...]) -> dict[str, Any]:
    spec = CORES[primitive.core]
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[tuple[str, str, str]] = []

    def mapped(value: object) -> object:
        return permutation[value] if type(value) is int else value

    def node(name: str, role: str, label: object | None = None) -> None:
        nodes[name] = {"role": role, "label": label}

    for name in sorted({item for arc in spec["arcs"] for item in arc}):
        node(f"core:{name}", "retic" if name in spec["retics"] else "tree")
    node("root", "root")
    node("leaf:incoming", "leaf", mapped(primitive.incoming))
    edges.extend((("root", "core:S", "incoming_core"), ("root", "leaf:incoming", "incoming_arm")))
    for arc_index, ((tail, head), word) in enumerate(zip(spec["arcs"], primitive.words)):
        previous = f"core:{tail}"
        for word_index, label in enumerate(word):
            subdivision = f"sub:{arc_index}:{word_index}"
            leaf = f"leaf:seg:{arc_index}:{word_index}"
            node(subdivision, "tree")
            node(leaf, "leaf", mapped(label))
            edges.append((previous, subdivision, f"seg{arc_index}"))
            edges.append((subdivision, leaf, "arm"))
            previous = subdivision
        edges.append((previous, f"core:{head}", f"seg{arc_index}"))
    for index, (sink, value) in enumerate(primitive.sinks):
        leaf = f"leaf:sink:{index}"
        node(leaf, "leaf", mapped(value))
        edges.append((f"core:{sink}", leaf, "sink_arm"))
    indegree = collections.Counter(head for _, head, _ in edges)
    outdegree = collections.Counter(tail for tail, _, _ in edges)
    expected = {"root": (0, 2), "tree": (1, 2), "retic": (2, 1), "leaf": (1, 0)}
    for name, data in nodes.items():
        require((indegree[name], outdegree[name]) == expected[data["role"]], "GRAPH_DEGREE", name)
    pending = {name: indegree[name] for name in nodes}
    queue = collections.deque(name for name, degree in pending.items() if degree == 0)
    visited = 0
    children: dict[str, list[str]] = collections.defaultdict(list)
    for tail, head, _ in edges:
        children[tail].append(head)
    while queue:
        current = queue.popleft()
        visited += 1
        for child in children[current]:
            pending[child] -= 1
            if pending[child] == 0:
                queue.append(child)
    require(visited == len(nodes), "GRAPH_CYCLE")
    labels = [data["label"] for data in nodes.values() if type(data["label"]) is int]
    require(sorted(labels) == list(range(len(permutation))), "GRAPH_PORT_LABELS")
    return {
        "core": primitive.core,
        "incoming_selected": primitive.incoming_selected,
        "repair": primitive.repair,
        "sink_mask": primitive.sink_mask,
        "nodes": [[key, nodes[key]] for key in sorted(nodes)],
        "edges": [list(row) for row in sorted(edges)],
    }


COMPOSITE_EXPECTED = {
    "raw4": {
        "total": 405_216,
        "k": 4,
        "source_count": 6,
        "target_count": 2_814,
        "categories": {
            "displayed_quartet_exclusion": 360_408,
            "full_map_Ti_strict_sign": 16_974,
            "exact_rank_exclusion": 23_822,
            "direct_terminal_presentation": 1_472,
            "restoration_member_presentation": 2_540,
        },
    },
    "theta2": {
        "total": 2_946_240,
        "k": 5,
        "source_count": 4,
        "target_count": 6_138,
        "categories": {
            "displayed_quartet_exclusion": 2_942_592,
            "full_map_Ti_strict_sign": 2_528,
            "exact_rank_exclusion": 800,
            "direct_quadratic_separator": 240,
            "labelled_isomorphism": 80,
        },
    },
}


EVIDENCE_KINDS = {
    "displayed_quartet_exclusion": "exact_displayed_quartet_witness",
    "full_map_Ti_strict_sign": "exact_whole_map_Ti_zero_sign_certificate",
    "exact_rank_exclusion": "matched_exact_rank_lower_symbolic_upper",
    "direct_terminal_presentation": "exact_terminal_class_and_direct_certificate",
    "restoration_member_presentation": "exact_restoration_parent_and_physical_transport",
    "direct_quadratic_separator": "exact_multihomogeneous_quadratic_separator",
    "labelled_isomorphism": "exact_labelled_semi_directed_isomorphism",
}


def scan_composite(project: Path, family: str) -> tuple[dict[str, Any], dict[str, Any]]:
    expected = COMPOSITE_EXPECTED[family]
    artifacts = project / "work/corrected_composite_ledgers/artifacts"
    ledger = artifacts / f"{family}_corrected_composite_ledger.jsonl.gz"
    summary_path = artifacts / f"{family}_corrected_composite_summary.json"
    mutation_path = artifacts / f"{family}_corrected_composite_mutations.json"
    summary = load_json(summary_path)
    mutations = load_json(mutation_path)
    verify_payload(summary, f"{family}:summary")
    verify_payload(mutations, f"{family}:mutations")
    mutation_targets = {
        int(row["mutated_raw_ids"][0])
        for row in mutations["tests"]
        if row.get("test_type") == "complete_disposable_ledger_attack"
    }
    rows_by_target: dict[int, dict[str, Any]] = {}
    category_counts: collections.Counter[str] = collections.Counter()
    source_counts: collections.Counter[int] = collections.Counter()
    row_root = hashlib.sha256()
    raw_root = hashlib.sha256()
    plain_root = hashlib.sha256()
    plain_bytes = 0
    restoration_bindings: dict[str, dict[str, Any]] = {}
    permutations = tuple(itertools.permutations(range(expected["k"])))
    per_source = expected["target_count"] * len(permutations)
    with gzip.open(ledger, "rb") as handle:
        for ordinal, line in enumerate(handle):
            require(line.endswith(b"\n") and line != b"\n", "COMPOSITE_LINE", f"{family}:{ordinal}")
            row = json.loads(line)
            payload = canonical(row)
            require(line == payload + b"\n", "COMPOSITE_CANONICAL", f"{family}:{ordinal}")
            require(row.get("raw_id") == ordinal, "COMPOSITE_RAW_ID", f"{family}:{ordinal}")
            source_index, remainder = divmod(ordinal, per_source)
            target_index, permutation_index = divmod(remainder, len(permutations))
            require(
                row.get("source_index") == source_index
                and row.get("target_index") == target_index
                and row.get("permutation_index") == permutation_index
                and row.get("port_permutation") == list(permutations[permutation_index]),
                "COMPOSITE_COORDINATE",
                f"{family}:{ordinal}",
            )
            category = row.get("corrected_category")
            require(category in expected["categories"], "COMPOSITE_CATEGORY", f"{family}:{ordinal}")
            require(
                row.get("evidence_binding", {}).get("kind") == EVIDENCE_KINDS[category],
                "COMPOSITE_EVIDENCE_KIND",
                f"{family}:{ordinal}",
            )
            require(b"tree_sunlet" not in payload, "COMPOSITE_REVOKED_TOKEN", f"{family}:{ordinal}")
            if ordinal in mutation_targets:
                rows_by_target[ordinal] = row
            if family == "raw4" and category == "restoration_member_presentation":
                evidence = row["evidence_binding"]
                root_id = evidence["physical_member_root_id"]
                parent = evidence["restoration_parent_id"]
                expected_parent = (
                    f"source_{source_index}:class_"
                    f"{int(root_id.split(':')[1][1:]):06d}"
                )
                require(parent == expected_parent, "COMPOSITE_RESTORATION_PARENT", root_id)
                require(root_id not in restoration_bindings, "COMPOSITE_RESTORATION_DUPLICATE", root_id)
                restoration_bindings[root_id] = evidence
            category_counts[category] += 1
            source_counts[source_index] += 1
            row_root.update(hashlib.sha256(payload).digest())
            raw_root.update(hashlib.sha256(canonical(ordinal)).digest())
            plain_root.update(line)
            plain_bytes += len(line)
    row_count = sum(category_counts.values())
    require(row_count == expected["total"], "COMPOSITE_TOTAL", family)
    require(dict(category_counts) == expected["categories"], "COMPOSITE_PARTITION", family)
    require(
        source_counts == collections.Counter({index: per_source for index in range(expected["source_count"])}),
        "COMPOSITE_SOURCE_CENSUS",
        family,
    )
    require(set(rows_by_target) == mutation_targets, "COMPOSITE_MUTATION_TARGETS", family)
    require(summary["ledger_sha256"] == sha_file(ledger), "COMPOSITE_LEDGER_SHA", family)
    require(summary["ordered_row_hash_root"] == row_root.hexdigest(), "COMPOSITE_ROW_ROOT", family)
    require(summary["ordered_raw_id_hash_root"] == raw_root.hexdigest(), "COMPOSITE_RAW_ROOT", family)
    require(summary["uncompressed_stream_sha256"] == plain_root.hexdigest(), "COMPOSITE_PLAIN_ROOT", family)
    require(summary["uncompressed_bytes"] == plain_bytes, "COMPOSITE_PLAIN_BYTES", family)
    return (
        {
            "rows": row_count,
            "category_counts": dict(category_counts),
            "source_counts": dict(source_counts),
            "ledger_sha256": sha_file(ledger),
            "ordered_row_hash_root": row_root.hexdigest(),
            "uncompressed_bytes": plain_bytes,
            "mutation_target_count": len(mutation_targets),
        },
        {"mutation_report": mutations, "target_rows": rows_by_target, "restoration": restoration_bindings},
    )


def terminal_and_direct_audit(project: Path) -> dict[str, Any]:
    registry_path = project / "work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz"
    registry = load_gzip_document(registry_path)
    verify_payload(registry, "terminal_registry")
    require(registry["schema"] == "k2p-raw4-terminal-certificate-registry-v1", "REGISTRY_SCHEMA")
    require(registry["terminal_class_count"] == len(registry["rows"]) == 934, "REGISTRY_COUNT")
    ids = []
    kinds: collections.Counter[str] = collections.Counter()
    degrees: collections.Counter[int] = collections.Counter()
    for row in registry["rows"]:
        identifier = f"source_{row['source_index']}:class_{row['class_id']:06d}"
        require(row["class_identifier"] == identifier, "REGISTRY_IDENTIFIER", identifier)
        binding = dict(row)
        claimed = binding.pop("certificate_binding_sha256")
        require(claimed == sha_object(binding), "REGISTRY_BINDING", identifier)
        certificate = row["terminal_certificate"]
        kinds[certificate["kind"]] += 1
        if certificate["kind"] == "exact_direct_polynomial_separator":
            degrees[int(certificate["degree"])] += 1
        ids.append(identifier)
    require(len(ids) == len(set(ids)) == 934, "REGISTRY_UNIQUE")
    require(registry["class_id_hash_root"] == sha_object(sorted(ids)), "REGISTRY_ID_ROOT")
    expected_kinds = {
        "exact_multihomogeneous_quadratic": 839,
        "exact_direct_polynomial_separator": 36,
        "ordinary_triangle_quotient": 35,
        "exact_mixed_graph_isomorphism": 20,
        "direct_hard_case_F2_F3_F4": 4,
    }
    require(dict(kinds) == expected_kinds, "REGISTRY_KIND_COUNTS", kinds)
    require(degrees == {3: 2, 4: 12, 5: 22}, "REGISTRY_DEGREES", degrees)
    direct_path = project / "package/referee/k2p_offline_sweep_portable/proofs/four_port_direct_residual_closure_certificate.json"
    direct = load_json(direct_path)
    require(len(direct["coverage"]) == 36, "DIRECT_COUNT")
    witness_checks = 0
    for row in direct["coverage"]:
        require(row["target_pullback_zero"] is True and row["target_pullback_term_count"] == 0, "DIRECT_TARGET_ZERO")
        require(row["source_pullback_term_count"] > 0, "DIRECT_SOURCE_NONZERO")
        witness = row["strict_D_plus_witness"]
        require(witness["nonzero"] is True, "DIRECT_WITNESS_ZERO")
        for s_text, g_text in witness["internal_edge_class_pairs"] + witness["selected_pendant_edge_pairs"]:
            s, g = Fraction(s_text), Fraction(g_text)
            require(0 < s < 1 and 0 < g < 1 and g > 2 * s - 1, "DIRECT_DOMAIN")
            witness_checks += 1
        for inheritance in witness["inheritance_probabilities"]:
            require(0 < Fraction(inheritance) < 1, "DIRECT_INHERITANCE")
    return {
        "registry_sha256": sha_file(registry_path),
        "registry_payload_sha256": registry["payload_sha256"],
        "terminal_classes": 934,
        "kind_counts": dict(kinds),
        "direct_degree_counts": {str(key): degrees[key] for key in sorted(degrees)},
        "strict_rational_edge_pairs_checked": witness_checks,
        "direct_certificate_sha256": sha_file(direct_path),
    }


def restoration_audit(project: Path, raw4_bindings: dict[str, dict[str, Any]]) -> dict[str, Any]:
    path = project / "work/restoration_sign_reclassification/corrected_restoration_forest.json"
    forest = load_json(path)
    verify_payload(forest, "restoration_forest")
    first = forest["first_coverage"]
    second = forest["second_coverage"]
    require(len(first) == 36_568 and len(second) == 256, "RESTORATION_EDGE_COUNTS")
    grouped: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    first_hashes = set()
    for index, row in enumerate(first):
        body = dict(row)
        claimed = body.pop("row_sha256")
        require(claimed == sha_object(body), "RESTORATION_FIRST_HASH", index)
        require(claimed not in first_hashes, "RESTORATION_FIRST_DUPLICATE", index)
        first_hashes.add(claimed)
        grouped[row["root_id"]].append(row)
    require(set(grouped) == set(raw4_bindings), "RESTORATION_ROOT_JOIN")
    for root_id, rows in grouped.items():
        rows.sort(key=lambda row: row["ordinal"])
        evidence = raw4_bindings[root_id]
        require(
            [row["ordinal"] for row in rows]
            == sorted({row["ordinal"] for row in rows}),
            "RESTORATION_ORDINAL",
            root_id,
        )
        require(evidence["first_child_count"] == len(rows), "RESTORATION_CHILD_COUNT", root_id)
        require(
            evidence["first_child_row_hash_root"] == sha_object([row["row_sha256"] for row in rows]),
            "RESTORATION_CHILD_ROOT",
            root_id,
        )
        require(
            evidence["first_child_transport_hash_root"]
            == sha_object([[row["source_parent_transport_id"], row["target_parent_transport_id"]] for row in rows]),
            "RESTORATION_TRANSPORT_ROOT",
            root_id,
        )
    continuation_parents = set()
    second_hashes = set()
    for index, row in enumerate(second):
        body = dict(row)
        claimed = body.pop("row_sha256")
        require(claimed == sha_object(body), "RESTORATION_SECOND_HASH", index)
        require(claimed not in second_hashes, "RESTORATION_SECOND_DUPLICATE", index)
        second_hashes.add(claimed)
        parent_index = row["parent_first_coverage_index"]
        require(0 <= parent_index < len(first), "RESTORATION_SECOND_PARENT_INDEX", index)
        require(row["parent_first_row_sha256"] == first[parent_index]["row_sha256"], "RESTORATION_SECOND_PARENT_HASH", index)
        require(row["root_id"] == first[parent_index]["root_id"], "RESTORATION_SECOND_ROOT", index)
        continuation_parents.add(parent_index)
    census = forest["census"]
    require(
        census["canonical_restoration_parents"] == 997
        and census["member_roots"] == len(grouped) == 2_540
        and census["first_children"] == len(first)
        and census["second_children"] == len(second)
        and census["forest_edges"] == len(first) + len(second) == 36_824
        and census["final_leaves"] == 36_792
        and census["max_depth"] == 2
        and census["cycles"] == census["missing_children"] == census["unresolved"] == 0
        and census["continuation_parents"] == len(continuation_parents) == 32,
        "RESTORATION_CENSUS",
    )
    return {
        "forest_sha256": sha_file(path),
        "payload_sha256": forest["payload_sha256"],
        "canonical_parents": 997,
        "member_roots": len(grouped),
        "first_children": len(first),
        "second_children": len(second),
        "edges": len(first) + len(second),
        "continuation_parents": len(continuation_parents),
        "cycles": 0,
        "unresolved": 0,
    }


def stream_objects(path: Path) -> Iterable[dict[str, Any]]:
    with gzip.open(path, "rb") as handle:
        for number, line in enumerate(handle, 1):
            value = json.loads(line)
            require(line == canonical(value) + b"\n", "STREAM_CANONICAL", f"{path.name}:{number}")
            yield value


def probe_join_audit(project: Path) -> dict[str, Any]:
    root = project / "work/probe_coherence_corrected"
    exact_ids = set()
    for item in stream_objects(root / "exact_transport_ledger.jsonl.gz"):
        require(item["record_id"] == item["record"]["transport_sha256"], "EXACT_TRANSPORT_ID")
        exact_ids.add(item["record_id"])
    restriction_ids = set()
    for item in stream_objects(root / "parent_restriction_ledger.jsonl.gz"):
        restriction_ids.add(item["record_id"])
    inventory_ids = set()
    inventory_raw_pairs = 0
    for item in stream_objects(root / "two_port_parent_inventory.jsonl.gz"):
        require(item["one_port_parent_id"] not in inventory_ids, "PROBE_INVENTORY_DUPLICATE")
        inventory_ids.add(item["one_port_parent_id"])
        inventory_raw_pairs += int(item["raw_second_probe_pairs"])
        for side in ("source_candidate_profile", "target_candidate_profile"):
            profile = item[side]
            require(profile["all_mixed_edge_sites_included"] is True, "PROBE_SITE_COVERAGE")
            require(profile["site_count"] == len(profile["sites"]), "PROBE_SITE_COUNT")
            require(len({row["site_id"] for row in profile["sites"]}) == len(profile["sites"]), "PROBE_SITE_DUPLICATE")
    one_counts: collections.Counter[str] = collections.Counter()
    one_equal = set()
    one_rows = 0
    for item in stream_objects(root / "one_port_ledger.jsonl.gz"):
        one_rows += 1
        status = item["status"]
        one_counts[status] += 1
        if status in {"isomorphic", "triangle"}:
            require(item["parent_transport_id"] in exact_ids, "ONE_PARENT_TRANSPORT")
            require(item["transport_id"] in exact_ids, "ONE_TRANSPORT")
            require(item["source_parent_restriction_id"] in restriction_ids, "ONE_SOURCE_RESTRICTION")
            require(item["target_parent_restriction_id"] in restriction_ids, "ONE_TARGET_RESTRICTION")
            one_equal.add(
                f"P1:{item['parent_anchor_id']}:{item['source_site_index']}:{item['target_site_index']}"
            )
    two_counts: collections.Counter[str] = collections.Counter()
    two_rows = 0
    exact_two = 0
    for item in stream_objects(root / "two_port_ledger.jsonl.gz"):
        two_rows += 1
        status = item["status"]
        two_counts[status] += 1
        require(item["one_port_parent_id"] in inventory_ids, "TWO_PARENT_INVENTORY")
        if status in {"isomorphic", "triangle"}:
            require(item["parent_transport_id"] in exact_ids, "TWO_PARENT_TRANSPORT")
            require(item["transport_id"] in exact_ids, "TWO_TRANSPORT")
            require(item["source_parent_restriction_id"] in restriction_ids, "TWO_SOURCE_RESTRICTION")
            require(item["target_parent_restriction_id"] in restriction_ids, "TWO_TARGET_RESTRICTION")
            reverse = item["reverse_order_certificate"]
            require(reverse["same_base_anchor_id"] == item["base_anchor_id"], "TWO_REVERSE_ANCHOR")
            require(reverse["reverse_parent_transport_id"] in exact_ids, "TWO_REVERSE_TRANSPORT")
            exact_two += 1
    require(len(exact_ids) == 67_741, "PROBE_EXACT_TRANSPORT_COUNT")
    require(len(restriction_ids) == 4_379, "PROBE_RESTRICTION_COUNT")
    require(len(inventory_ids) == len(one_equal) == 2_107, "PROBE_ONE_EQUALITIES")
    require(one_rows == 29_964 and two_rows == inventory_raw_pairs == 544_571, "PROBE_PAIR_COUNTS")
    require(exact_two == 32_729, "PROBE_TWO_EQUALITIES")
    require(one_counts == {"displayed_quartet_mismatch": 27_758, "full_map_Ti_strict_sign": 99, "isomorphic": 1_915, "triangle": 192}, "PROBE_ONE_PARTITION", one_counts)
    require(two_counts == {"displayed_quartet_mismatch": 511_266, "full_map_Ti_strict_sign": 576, "isomorphic": 30_969, "triangle": 1_760}, "PROBE_TWO_PARTITION", two_counts)
    return {
        "exact_transport_ids": len(exact_ids),
        "parent_restriction_ids": len(restriction_ids),
        "one_port_rows": one_rows,
        "one_port_equalities": len(one_equal),
        "two_port_rows": two_rows,
        "two_port_equalities": exact_two,
        "one_port_partition": dict(one_counts),
        "two_port_partition": dict(two_counts),
    }


def parameter_transport_audit(project: Path) -> dict[str, Any]:
    root = project / "work/canonicalizer_completeness/inheritance_transport"
    files = {
        "relations": "probe_relation_parameter_transports.jsonl.gz",
        "probe_restrictions": "probe_restriction_parameter_transports.jsonl.gz",
        "restoration_restrictions": "restoration_restriction_parameter_transports.jsonl.gz",
    }
    counts: dict[str, int] = {}
    affine = complement = identity = triangle_sections = 0
    bad = 0
    for role, filename in files.items():
        count = 0
        for wrapper in stream_objects(root / filename):
            count += 1
            row = wrapper["row"]
            body = dict(row)
            require(wrapper["row_sha256"] == sha_object(body), "PARAMETER_ROW_HASH", f"{role}:{count}")
            if row.get("relation") == "triangle":
                require(row.get("triangle_local_parameters_are_not_affine_parent_flips") is True, "TRIANGLE_AFFINE_FLAG")
            for action in row["inheritance_actions"]:
                if action["mode"] == "ordinary_triangle_local_section":
                    triangle_sections += 1
                    require(action.get("section_certificate") == "rank_nine_ordinary_triangle_common_germ", "TRIANGLE_SECTION")
                    continue
                require(action["mode"] == "affine_parent_transport", "PARAMETER_ACTION_MODE")
                affine += 1
                reversed_order = action["parent_order_reversed"]
                mapping_key = (
                    "source_parent_index_to_target_parent_index"
                    if "source_parent_index_to_target_parent_index" in action
                    else "child_parent_index_to_parent_parent_index"
                )
                formula_key = (
                    "target_lambda_from_source"
                    if "target_lambda_from_source" in action
                    else "parent_lambda_from_child"
                )
                expected_mapping = [1, 0] if reversed_order else [0, 1]
                expected_formula = "one_minus_lambda" if reversed_order else "lambda"
                if action.get(mapping_key) != expected_mapping or action.get(formula_key) != expected_formula:
                    bad += 1
                if reversed_order:
                    complement += 1
                else:
                    identity += 1
            for edge in row["edge_actions"]:
                require(edge["mode"] in {"paired_K2P_product", "paired_serial_product", "ordinary_triangle_local_section"}, "PARAMETER_EDGE_MODE")
                if edge["mode"] != "ordinary_triangle_local_section":
                    require(
                        (edge.get("s_action"), edge.get("g_action")) == ("match_products", "match_products")
                        or (edge.get("parent_s_from_child"), edge.get("parent_g_from_child")) == ("product", "product"),
                        "PARAMETER_PAIRED_PRODUCT",
                    )
        counts[role] = count
    require(
        counts
        == {
            "relations": 67_741,
            "probe_restrictions": 71_022,
            "restoration_restrictions": 5_540,
        },
        "PARAMETER_COUNTS",
        counts,
    )
    require(bad == 0 and affine > 0 and complement > 0 and identity > 0 and triangle_sections > 0, "PARAMETER_TRANSPORT_SEMANTICS")
    return {
        "ledger_counts": counts,
        "affine_actions": affine,
        "identity_actions": identity,
        "complement_actions": complement,
        "triangle_local_sections": triangle_sections,
        "illicit_complements": bad,
    }


def mutation_forensics(project: Path, context: dict[str, dict[str, Any]]) -> dict[str, Any]:
    runner = project / "work/corrected_composite_ledgers/run_composite_mutations.py"
    verifier = project / "work/corrected_composite_ledgers/verify_corrected_composites_independent.py"
    runner_source = runner.read_text(encoding="utf-8")
    tree = ast.parse(runner_source)
    functions = {node.name: node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    semantic_calls = {node.func.id for node in ast.walk(functions["run_semantic_case"]) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    main_calls = {node.func.id for node in ast.walk(functions["main"]) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    require({"rewrite_complete_mutant", "invoke_verifier"} <= semantic_calls, "MUTATION_CODE_PATH")
    require("run_semantic_case" in main_calls, "MUTATION_MAIN_PATH")
    require('"--ledger"' in runner_source and '"--summary"' in runner_source and '"--skip-heavy-full-map"' in runner_source, "MUTATION_VERIFIER_ARGUMENTS")
    verifier_sha = sha_file(verifier)
    results = {}
    expected_names = {
        "raw4": {
            "omitted_raw_row", "duplicate_raw_id", "wrong_port_permutation", "reassigned_category",
            "reassigned_evidence_binding", "false_rank_exclusion", "rooted_restriction_reintroduction",
            "wrong_restoration_parent", "broken_transport", "reassigned_cubic_certificate",
            "reassigned_quartic_certificate", "reassigned_quintic_certificate", "python_optimized_mode",
            "source_tree_immutability",
        },
        "theta2": {
            "omitted_raw_row", "duplicate_raw_id", "wrong_port_permutation", "reassigned_category",
            "reassigned_evidence_binding", "false_rank_exclusion", "rooted_restriction_reintroduction",
            "missing_restoration_child", "reassigned_quadratic_certificate", "broken_transport",
            "python_optimized_mode", "source_tree_immutability",
        },
    }
    for family, item in context.items():
        report = item["mutation_report"]
        tests = report["tests"]
        require({row["name"] for row in tests} == expected_names[family], "MUTATION_NAME_COVERAGE", family)
        semantic_rows = [row for row in tests if row["test_type"] == "complete_disposable_ledger_attack"]
        require(len(semantic_rows) == (12 if family == "raw4" else 10), "MUTATION_SEMANTIC_COUNT", family)
        mutant_hashes = set()
        for row in semantic_rows:
            target = int(row["mutated_raw_ids"][0])
            require(target in item["target_rows"], "MUTATION_TARGET_ABSENT", f"{family}:{target}")
            diff = row["mutation_diff"]
            total = COMPOSITE_EXPECTED[family]["total"]
            expected_diff = {
                "change": (total, 1, 0, 0),
                "omit": (total - 1, 0, 1, 0),
                "duplicate": (total + 1, 0, 0, 1),
            }[row["mutation_mode"]]
            require(
                (diff["output_rows"], diff["changed_rows"], diff["deleted_rows"], diff["inserted_rows"]) == expected_diff
                and diff["input_rows"] == total,
                "MUTATION_DIFF",
                f"{family}:{row['name']}",
            )
            expected_diagnostic = f"CORRECTED_COMPOSITE_REPLAY_FAIL:{row['expected_semantic_diagnostic']}"
            require(
                row["complete_mutant_ledger_created"] is True
                and row["production_verifier_invoked"] is True
                and row["production_verifier_sha256"] == verifier_sha
                and row["verifier_exit_code"] == 1
                and row["observed_semantic_diagnostic"] == expected_diagnostic
                and row["semantic_diagnostic_matched"] is True
                and row["verifier_report_created"] is False
                and row["mutated_ledger_bytes"] > 0
                and len(row["mutated_ledger_sha256"]) == 64,
                "MUTATION_PRODUCTION_EVIDENCE",
                f"{family}:{row['name']}",
            )
            mutant_hashes.add(row["mutated_ledger_sha256"])
        require(len(mutant_hashes) == len(semantic_rows), "MUTATION_HASH_COLLISION", family)
        optimized = next(row for row in tests if row["name"] == "python_optimized_mode")
        immutability = next(row for row in tests if row["name"] == "source_tree_immutability")
        require(optimized["production_verifier_invoked"] is True and optimized["verifier_exit_code"] == 1 and optimized["semantic_diagnostic_matched"] is True, "MUTATION_OPTIMIZED", family)
        require(immutability["source_fingerprints_unchanged"] is True and immutability["production_verifier_invoked"] is False, "MUTATION_IMMUTABILITY", family)
        require(report["mutation_runner_sha256"] == sha_file(runner) and report["production_verifier_sha256"] == verifier_sha and report["source_tree_drift"] == report["survivors"] == 0, "MUTATION_REPORT_BINDING", family)
        results[family] = {
            "schema": report["schema"],
            "payload_sha256": report["payload_sha256"],
            "tests": len(tests),
            "complete_ledger_attacks": len(semantic_rows),
            "distinct_mutant_hashes": len(mutant_hashes),
            "intended_diagnostics": len(semantic_rows),
            "survivors": 0,
            "source_tree_drift": 0,
        }
    return {
        "runner_sha256": sha_file(runner),
        "verifier_sha256": verifier_sha,
        "ast_confirmed_call_path": "main -> run_semantic_case -> rewrite_complete_mutant + invoke_verifier",
        "families": results,
    }


def printed_anchor_audit(project: Path) -> dict[str, Any]:
    registry_relative = "work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz"
    overlay_relative = "work/raw4_sign_reclassification/raw4_corrected_terminal_ledger.json"
    registry_path = project / registry_relative
    overlay_path = project / overlay_relative
    registry = load_gzip_document(registry_path)
    overlay = load_json(overlay_path)
    supplement_path = project / "proof_compression_submission/supplement/supplement.tex"
    supplement = supplement_path.read_text(encoding="utf-8")
    registry_sha = sha_file(registry_path)
    overlay_sha = sha_file(overlay_path)
    label = "raw-four 934-class terminal certificate registry"
    require(supplement.count(label) == 1 and supplement.count(registry_sha) == 1, "PRINTED_REGISTRY_ROW")
    require(overlay_sha not in supplement, "PRINTED_OVERLAY_MISLABEL")
    audit_path = project / "proof_compression_submission/adversarial_review/audit_article_sources.py"
    specification = importlib.util.spec_from_file_location("r6_anchor_gate", audit_path)
    require(specification is not None and specification.loader is not None, "ANCHOR_IMPORT")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    require(module.PRINTED_FROZEN_ANCHORS[label] == registry_relative, "ANCHOR_ROLE_MAPPING")
    require(
        module.PRINTED_FROZEN_ANCHOR_TYPES[label]
        == {"schema": "k2p-raw4-terminal-certificate-registry-v1", "count_field": "terminal_class_count", "count": 934},
        "ANCHOR_TYPE_MAPPING",
    )
    baseline = module.audit_printed_authority_hashes(project, supplement)
    require(baseline["status"] == "PASS", "ANCHOR_BASELINE")
    mutant_anchors = dict(module.PRINTED_FROZEN_ANCHORS)
    mutant_anchors[label] = overlay_relative
    mutant = supplement.replace(registry_sha, overlay_sha, 1)
    observed = ""
    try:
        module.audit_printed_authority_hashes(
            project,
            mutant,
            frozen_anchors=mutant_anchors,
            frozen_anchor_types=module.PRINTED_FROZEN_ANCHOR_TYPES,
        )
    except module.AuditFailure as error:
        observed = str(error)
    require(observed.startswith(f"PRINTED_FROZEN_ANCHOR_SCHEMA_DRIFT:{label}:"), "ANCHOR_OVERLAY_ATTACK", observed)
    narratives = module.audit_current_narrative_roles(project)
    require(narratives["status"] == "PASS" and narratives["rows_checked"] == 3, "NARRATIVE_ROLES")
    return {
        "supplement_sha256": sha_file(supplement_path),
        "registry_sha256": registry_sha,
        "registry_schema": registry["schema"],
        "registry_count": registry["terminal_class_count"],
        "overlay_sha256": overlay_sha,
        "overlay_schema": overlay["schema"],
        "overlay_corrected_rows": overlay["corrected_rows"],
        "baseline_rows_checked": baseline["rows_checked"],
        "coherent_overlay_swap_diagnostic": observed,
        "current_narratives_typed_as_reader_snapshots": narratives["rows_checked"],
        "status": "PASS",
    }


def optimized_guards(project: Path, runtime_python: Path) -> dict[str, Any]:
    cases = (
        ("composite_verifier", "work/corrected_composite_ledgers/verify_corrected_composites_independent.py", ("--family", "raw4", "--report", "OUT")),
        ("composite_mutations", "work/corrected_composite_ledgers/run_composite_mutations.py", ("--family", "raw4", "--output", "OUT")),
        ("static_article_audit", "proof_compression_submission/adversarial_review/audit_article_sources.py", ()),
        ("printed_anchor_mutations", "proof_compression_submission/adversarial_review/test_printed_authority_hash_gate.py", ()),
        ("raw4_generator", "work/raw_ledger_audit/generate_raw_ledger.py", ("--output-root", "OUTDIR")),
        ("raw4_verifier", "work/raw_ledger_audit/verify_raw_ledger.py", ()),
        ("theta2_generator", "work/theta2_five_port_closure/generate_theta2_ledger.py", ("--output-root", "OUTDIR")),
        ("theta2_verifier", "work/theta2_five_port_closure/verify_theta2_ledger.py", ("--quick",)),
        ("canonicalizer", "work/canonicalizer_completeness/canonicalizer_audit.py", ("--semantic-only",)),
        ("parameter_transport", "work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py", ("--structural-only",)),
        ("rank_upper", "work/rank_upper_certificates/verify_rank_upper_certificates.py", ("--output", "OUT")),
        ("final_release", "work/final_theorem_release/verify_final_theorem_release.py", ("--quick", "--output", "OUT")),
    )
    rows = []
    for name, relative, raw_arguments in cases:
        with tempfile.TemporaryDirectory(prefix="r6-optimized-") as directory:
            scratch = Path(directory)
            output = scratch / "stale-pass.json"
            output.write_text('{"status":"PASS"}\n', encoding="utf-8")
            arguments = tuple(
                str(output) if item == "OUT" else str(scratch / "out") if item == "OUTDIR" else item
                for item in raw_arguments
            )
            completed = subprocess.run(
                [str(runtime_python), "-O", "-B", str(project / relative), *arguments],
                cwd=scratch,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=30,
                check=False,
            )
            observed = completed.stdout.strip()
            require(completed.returncode != 0 and "OPTIMIZED" in observed.upper(), "OPTIMIZED_GUARD", f"{name}:{completed.returncode}:{observed[:500]}")
            rows.append({"entry_point": name, "path": relative, "exit_code": completed.returncode, "diagnostic": observed})
    atlas = project / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
    parsed = ast.parse(atlas.read_text(encoding="utf-8"))
    assert_statements = [node.lineno for node in ast.walk(parsed) if isinstance(node, ast.Assert)]
    require(not assert_statements, "ATLAS_ASSERT_STATEMENTS", assert_statements)
    return {
        "runtime_python": str(runtime_python),
        "entry_points": rows,
        "entry_point_count": len(rows),
        "atlas_assert_statement_count": 0,
    }


def strict_json_attacks(project: Path) -> dict[str, Any]:
    path = project / "work/final_theorem_release/strict_json.py"
    specification = importlib.util.spec_from_file_location("r6_strict_json", path)
    require(specification is not None and specification.loader is not None, "STRICT_IMPORT")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    cases = (
        (b'{"a":1,"a":1}\n', "STRICT_JSON_DUPLICATE_NAME"),
        (b'{"a":0,"a":1}\n', "STRICT_JSON_DUPLICATE_NAME"),
        (b'{"z":1,"a":2}\n', "STRICT_JSON_NONCANONICAL"),
        (b'{"a":NaN}\n', "STRICT_JSON_NONFINITE"),
    )
    rows = []
    for index, (payload, marker) in enumerate(cases):
        observed = ""
        try:
            module.decode_json_document(
                payload,
                label=f"r6-case-{index}",
                require_object=True,
                require_canonical_bytes=True,
                require_terminal_newline=True,
            )
        except module.StrictJSONError as error:
            observed = str(error)
        require(marker in observed, "STRICT_JSON_ATTACK", f"{index}:{observed}")
        rows.append({"case": index, "expected": marker, "observed": observed})
    return {"strict_json_sha256": sha_file(path), "attacks": rows, "rejected": len(rows)}


def primitive_reconstruction(context: dict[str, dict[str, Any]]) -> dict[str, Any]:
    raw4_targets = targets(4)
    theta2_targets = targets(5)
    raw4_sources = sources(("theta0", "theta1", "theta3"))
    theta2_sources = sources(("theta2",))
    require((len(raw4_sources), len(raw4_targets), len(theta2_sources), len(theta2_targets)) == (6, 2814, 4, 6138), "PRIMITIVE_CENSUS")
    representatives = []
    for family, raw_ids, source_rows, target_rows, k in (
        ("raw4", (0, 97, 2185, 69_457, 154_800, 357_409, 405_215), raw4_sources, raw4_targets, 4),
        ("theta2", (0, 19_161, 166_200, 166_201, 2_946_239), theta2_sources, theta2_targets, 5),
    ):
        per_source = len(target_rows) * len(tuple(itertools.permutations(range(k))))
        permutations = tuple(itertools.permutations(range(k)))
        for raw_id in raw_ids:
            source_index, remainder = divmod(raw_id, per_source)
            target_index, permutation_index = divmod(remainder, len(permutations))
            permutation = permutations[permutation_index]
            source_encoding = graph_encoding(source_rows[source_index], tuple(range(k)))
            target_encoding = graph_encoding(target_rows[target_index], permutation)
            representatives.append(
                {
                    "family": family,
                    "raw_id": raw_id,
                    "source_index": source_index,
                    "target_index": target_index,
                    "permutation_index": permutation_index,
                    "port_permutation": list(permutation),
                    "source_core": source_rows[source_index].core,
                    "target_core": target_rows[target_index].core,
                    "target_repair": target_rows[target_index].repair,
                    "target_sink_mask": target_rows[target_index].sink_mask,
                    "source_graph_encoding_sha256": sha_object(source_encoding),
                    "target_graph_encoding_sha256": sha_object(target_encoding),
                }
            )
    return {
        "primitive_counts": {
            "raw4_sources": len(raw4_sources),
            "raw4_targets": len(raw4_targets),
            "theta2_sources": len(theta2_sources),
            "theta2_targets": len(theta2_targets),
            "all_archetypes_including_cycle_families_expected": 10_084,
        },
        "raw_direction_formulas": {
            "raw4": "raw_id=((source_index*2814)+target_index)*24+permutation_index",
            "theta2": "raw_id=((source_index*6138)+target_index)*120+permutation_index",
        },
        "representatives": representatives,
        "independence": "locally reimplemented weak compositions, repair insertion, sink masks, subdivision words, graph degrees, DAG check, port permutations, and raw-id inversion",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--runtime-python", type=Path, default=Path(sys.executable))
    args = parser.parse_args()
    project = args.project.resolve()
    require(project.is_dir(), "PROJECT")
    started = time.monotonic()
    raw4_result, raw4_context = scan_composite(project, "raw4")
    theta2_result, theta2_context = scan_composite(project, "theta2")
    context = {"raw4": raw4_context, "theta2": theta2_context}
    result = {
        "schema": "r6-independent-k2p-computational-semantic-audit-v1",
        "status": "PASS",
        "source_project": str(project),
        "primitive_reconstruction": primitive_reconstruction(context),
        "composites": {"raw4": raw4_result, "theta2": theta2_result},
        "terminal_and_direct_certificates": terminal_and_direct_audit(project),
        "restoration": restoration_audit(project, raw4_context["restoration"]),
        "probe_graph_joins": probe_join_audit(project),
        "parameter_transports": parameter_transport_audit(project),
        "composite_mutation_forensics": mutation_forensics(project, context),
        "printed_semantic_anchor": printed_anchor_audit(project),
        "strict_json_attacks": strict_json_attacks(project),
        "optimized_mode_guards": optimized_guards(project, args.runtime_python.absolute()),
        "runtime_seconds": round(time.monotonic() - started, 6),
        "unresolved": 0,
    }
    result["payload_sha256"] = sha_object(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "PASS",
                "raw4_rows": raw4_result["rows"],
                "theta2_rows": theta2_result["rows"],
                "probe_rows": result["probe_graph_joins"]["one_port_rows"] + result["probe_graph_joins"]["two_port_rows"],
                "parameter_transport_rows": sum(result["parameter_transports"]["ledger_counts"].values()),
                "payload_sha256": result["payload_sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except Failure as error:
        raise SystemExit(f"R6_SEMANTIC_SCAN_FAIL:{error}")
