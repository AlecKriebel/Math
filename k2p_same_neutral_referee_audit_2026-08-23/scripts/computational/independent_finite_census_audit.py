#!/usr/bin/env python3
"""Independent finite-census and structural-contract audit for K2P-SAME.

This deliberately does not import the submitted classifier, canonicalizer, or
ledger verifiers.  It rebuilds the primitive completion index sets from a
literal core specification, reconstructs raw IDs, and scans the sealed
ledgers as streams.  Its remit is completeness/contract checking, not proving
the algebraic truth of a terminal label.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path


CORES = {
    "cycle": {
        "arcs": (("S", "X"), ("S", "X")),
        "retics": ("X",), "sinks": ("X",), "repairs": ((0,), (1,)),
    },
    "theta0": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X"), ("V", "X"), ("U", "V")),
        "retics": ("V", "X"), "sinks": ("X",), "repairs": ((2, 3), (3, 4)),
    },
    "theta1": {
        "arcs": (("S", "U"), ("S", "X"), ("V", "X"), ("U", "V"), ("U", "V")),
        "retics": ("V", "X"), "sinks": ("X",), "repairs": ((2, 3), (2, 4)),
    },
    "theta2": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1")),
        "retics": ("X0", "X1"), "sinks": ("X0", "X1"),
        "repairs": ((2, 3), (2, 5), (3, 4), (4, 5)),
    },
    "theta3": {
        "arcs": (("S", "U"), ("S", "X0"), ("V", "X0"), ("U", "X1"), ("V", "X1"), ("U", "V")),
        "retics": ("X0", "X1"), "sinks": ("X0", "X1"), "repairs": ((2,), (4,)),
    },
}


def require(ok: bool, code: str, detail=None) -> None:
    if not ok:
        raise RuntimeError(code if detail is None else f"{code}: {detail}")


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha_obj(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def weak_compositions(total: int, bins: int):
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, bins - 1):
            yield (first,) + rest


def primitive_targets(k: int, incoming_selected: bool):
    """Standalone reconstruction of the ordered target-record index set."""
    rows = []
    for core_id, spec in CORES.items():
        ordinary_plus_sinks = k - 1 if incoming_selected else k
        sink_count = len(spec["sinks"])
        for mask in range(1 << sink_count):
            ordinary = ordinary_plus_sinks - mask.bit_count()
            if ordinary < 0:
                continue
            for counts in weak_compositions(ordinary, len(spec["arcs"])):
                next_label = 1 if incoming_selected else 0
                selected_words = []
                for count in counts:
                    selected_words.append(tuple(range(next_label, next_label + count)))
                    next_label += count
                repairs = ((None, ()),) if core_id == "cycle" else tuple(enumerate(spec["repairs"]))
                for repair_index, repair in repairs:
                    words = [list(word) for word in selected_words]
                    sink_next_label = next_label
                    dummy_roles = []
                    for arc_index in repair:
                        if not words[arc_index]:
                            role = f"D_REPAIR_{repair_index}_{arc_index}"
                            words[arc_index].append(role)
                            dummy_roles.append(role)
                    sink_labels = []
                    for sink_index in range(sink_count):
                        if mask & (1 << sink_index):
                            sink_labels.append(sink_next_label)
                            sink_next_label += 1
                        else:
                            role = f"D_SINK_{sink_index}"
                            sink_labels.append(role)
                            dummy_roles.append(role)
                    incoming = 0 if incoming_selected else "INCOMING"
                    if not incoming_selected:
                        dummy_roles.append("INCOMING")
                    labels = [incoming] + [x for word in words for x in word] + sink_labels
                    integer_labels = sorted(x for x in labels if isinstance(x, int))
                    require(integer_labels == list(range(k)), "PRIMITIVE_LABEL_SET", (k, incoming_selected, core_id, counts, mask))
                    # Independent binary/TC sanity check at the core-template level.
                    indegree = Counter()
                    outdegree = Counter()
                    for tail, head in spec["arcs"]:
                        outdegree[tail] += 1
                        indegree[head] += 1
                    require(all(indegree[r] == 2 for r in spec["retics"]), "CORE_RETIC_INDEGREE", core_id)
                    require(all(len(words[i]) or i not in repair for i in range(len(words))), "REPAIR_EMPTY", core_id)
                    rows.append({
                        "core_id": core_id,
                        "incoming_selected": incoming_selected,
                        "repair_index": repair_index,
                        "selected_sink_mask": mask,
                        "words": tuple(tuple(word) for word in words),
                        "sink_labels": tuple(sink_labels),
                        "incoming": incoming,
                        "dummy_roles": tuple(sorted(dummy_roles)),
                    })
    require(len({repr(row) for row in rows}) == len(rows), "PRIMITIVE_TARGET_DUPLICATE", (k, incoming_selected))
    return rows


def primitive_sources(core_ids):
    rows = []
    for core_id in core_ids:
        spec = CORES[core_id]
        for repair_index, repair in enumerate(spec["repairs"]):
            words = [[] for _ in spec["arcs"]]
            next_label = 1
            for arc_index in repair:
                words[arc_index].append(next_label)
                next_label += 1
            sink_labels = tuple(range(next_label, next_label + len(spec["sinks"])))
            rows.append((core_id, repair_index, tuple(tuple(x) for x in words), sink_labels))
    require(len(set(rows)) == len(rows), "PRIMITIVE_SOURCE_DUPLICATE")
    return rows


def scan_composite(path: Path, k: int, source_count: int, target_count: int):
    categories = Counter()
    raw_count = source_count * target_count * math.factorial(k)
    permutations = tuple(itertools.permutations(range(k)))
    stream_hash = hashlib.sha256()
    byte_count = 0
    first = None
    last = None
    terminal_classes = set()
    restoration_parents = set()
    quartet_invariant_kinds = Counter()
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            stream_hash.update(line)
            byte_count += len(line)
            row = json.loads(line)
            require(row["raw_id"] == ordinal, "COMPOSITE_RAW_ID_ORDER", (path.name, ordinal, row["raw_id"]))
            expected = ((row["source_index"] * target_count + row["target_index"]) * math.factorial(k)
                        + row["permutation_index"])
            require(expected == ordinal, "COMPOSITE_RAW_ID_FORMULA", (path.name, ordinal, expected))
            require(tuple(row["port_permutation"]) == permutations[row["permutation_index"]],
                    "COMPOSITE_PERMUTATION", (path.name, ordinal))
            category = row["corrected_category"]
            categories[category] += 1
            evidence = row["evidence_binding"]
            if category == "displayed_quartet_exclusion":
                quartet_invariant_kinds[evidence.get("invariant_kind")] += 1
                # This is intentionally only a structural observation: the row
                # contains no Fourier coordinate tuple or polynomial body.
                require("coordinate_indices" not in evidence and "polynomial" not in evidence,
                        "UNEXPECTED_QUARTET_ALGEBRA_BINDING", ordinal)
            elif category == "direct_terminal_presentation":
                terminal_classes.add(evidence["terminal_class_id"])
            elif category == "restoration_member_presentation":
                restoration_parents.add(evidence["restoration_parent_id"])
            first = row if first is None else first
            last = row
    require((last["raw_id"] + 1 if last else 0) == raw_count, "COMPOSITE_ROW_COUNT", path.name)
    return {
        "rows": raw_count,
        "category_counts": dict(categories),
        "uncompressed_bytes": byte_count,
        "uncompressed_sha256": stream_hash.hexdigest(),
        "file_sha256": sha_file(path),
        "terminal_classes": len(terminal_classes),
        "restoration_parents": len(restoration_parents),
        "quartet_invariant_kinds": dict(quartet_invariant_kinds),
        "first_raw_id": first["raw_id"], "last_raw_id": last["raw_id"],
    }


def scan_terminal_registry(path: Path):
    with gzip.open(path, "rt") as stream:
        data = json.load(stream)
    kinds = Counter()
    degrees = Counter()
    prior = (-1, -1)
    for row in data["rows"]:
        key = (row["source_index"], row["class_id"])
        require(key > prior, "TERMINAL_CLASS_ID_ORDER", key)
        prior = key
        terminal = row["terminal_certificate"]
        kinds[terminal["kind"]] += 1
        if terminal["kind"] == "exact_direct_polynomial_separator":
            degrees[terminal["degree"]] += 1
    return {
        "classes": len(data["rows"]), "kind_counts": dict(kinds),
        "higher_degree_counts": {str(k): v for k, v in sorted(degrees.items())},
        "file_sha256": sha_file(path), "payload_sha256": data["payload_sha256"],
    }


def scan_theta2_restoration(path: Path):
    with gzip.open(path, "rt") as stream:
        data = json.load(stream)
    roots = data["restoration_roots"]
    root_roles = {row["anchor_id"]: tuple(row["dummy_roles"]) for row in roots}
    require(Counter(len(v) for v in root_roles.values()) == {1: 40, 2: 16}, "THETA2_ROOT_ROLE_HIST")
    six = defaultdict(set)
    continuation = set()
    six_categories = Counter()
    for row in data["six_port_rows"]:
        six[row["anchor_id"]].add((row["restored_role"], row["source_insertion_index"]))
        six_categories[row["category"]] += 1
        if row["category"] == "isomorphic" and row["remaining_roles"]:
            continuation.add(row["path_id"])
    for anchor, roles in root_roles.items():
        require(six[anchor] == {(role, index) for role in roles for index in range(8)},
                "THETA2_FIRST_CARTESIAN", anchor)
    seven = defaultdict(set)
    seven_categories = Counter()
    for row in data["seven_port_rows"]:
        seven[row["parent_path_id"]].add(row["source_insertion_index"])
        seven_categories[row["category"]] += 1
    require(set(seven) == continuation, "THETA2_CONTINUATION_PARENT_SET")
    require(all(indices == set(range(9)) for indices in seven.values()), "THETA2_SECOND_CARTESIAN")
    leaves = sum(v for k, v in six_categories.items() if k != "isomorphic")
    leaves += sum(v for k, v in seven_categories.items())
    leaves += six_categories["isomorphic"] - len(continuation)
    return {
        "roots": len(roots), "one_dummy_roots": 40, "two_dummy_roots": 16,
        "six_children": len(data["six_port_rows"]), "six_categories": dict(six_categories),
        "continuations": len(continuation), "seven_children": len(data["seven_port_rows"]),
        "seven_categories": dict(seven_categories), "descendants": len(data["six_port_rows"]) + len(data["seven_port_rows"]),
        "leaves": leaves, "file_sha256": sha_file(path),
    }


def scan_cycle(base_path: Path, full_path: Path, target_count: int):
    permutations = tuple(itertools.permutations(range(3)))
    base_categories = Counter()
    roots = {}
    base_hashes = hashlib.sha256()
    with gzip.open(base_path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line)
            require(row["raw_id"] == ordinal, "CYCLE_BASE_RAW_ORDER", ordinal)
            expected = ((row["source_index"] * target_count + row["target_index"]) * 6 + row["permutation_index"])
            require(expected == ordinal, "CYCLE_BASE_RAW_FORMULA", ordinal)
            require(tuple(row["port_permutation"]) == permutations[row["permutation_index"]], "CYCLE_BASE_PERM", ordinal)
            payload = dict(row); claimed = payload.pop("authoritative_row_sha256")
            require(sha_obj(payload) == claimed, "CYCLE_BASE_ROW_HASH", ordinal)
            base_hashes.update(bytes.fromhex(claimed))
            base_categories[row["terminal_kind"]] += 1
            if row["terminal_kind"] == "fixed_full_restoration_obligation":
                roots[ordinal] = tuple(row["dummy_roles"])
    require(ordinal + 1 == 13440, "CYCLE_BASE_COUNT")
    role_hist = Counter(len(v) for v in roots.values())
    full_categories = Counter()
    current = None
    paths = set()
    expected_for_current = 0
    def finish(root_id, seen, expected_count):
        if root_id is not None:
            require(len(seen) == expected_count, "CYCLE_COMPLETION_MULTIPLICITY", (root_id, len(seen), expected_count))
    with gzip.open(full_path, "rt") as stream:
        for ordinal, line in enumerate(stream):
            row = json.loads(line)
            require(row["raw_id"] == ordinal, "CYCLE_FULL_RAW_ORDER", ordinal)
            base_id = row["base_raw_id"]
            require(base_id in roots, "CYCLE_FULL_UNKNOWN_ROOT", base_id)
            if current != base_id:
                finish(current, paths, expected_for_current)
                current, paths = base_id, set()
                depth = len(roots[base_id])
                expected_for_current = math.prod(range(3, 3 + depth))
            path_tuple = tuple(row["source_placement_path"])
            depth = len(roots[base_id])
            require(len(path_tuple) == depth, "CYCLE_PATH_DEPTH", ordinal)
            require(all(0 <= value < 3 + step for step, value in enumerate(path_tuple)), "CYCLE_PATH_INDEX", ordinal)
            require(path_tuple not in paths, "CYCLE_PATH_DUPLICATE", (base_id, path_tuple))
            paths.add(path_tuple)
            full_categories[row["terminal_kind"]] += 1
        finish(current, paths, expected_for_current)
    require(ordinal + 1 == 536364, "CYCLE_FULL_COUNT")
    return {
        "base_rows": 13440, "base_categories": dict(base_categories),
        "restoration_roots": len(roots), "root_dummy_histogram": {str(k): v for k, v in sorted(role_hist.items())},
        "full_rows": 536364, "full_categories": dict(full_categories),
        "base_file_sha256": sha_file(base_path), "full_file_sha256": sha_file(full_path),
        "base_ordered_row_hash_root": base_hashes.hexdigest(),
    }


def scan_restoration(path: Path):
    data = json.loads(path.read_text())
    first_groups = defaultdict(set)
    first_roles = defaultdict(set)
    first_proofs = Counter()
    continuation_indices = set()
    source_transport_ids = set(data["first_source_transport_certificates"])
    target_transport_ids = set(data["first_target_transport_certificates"])
    for ordinal, row in enumerate(data["first_coverage"]):
        payload = dict(row); claimed = payload.pop("row_sha256")
        require(sha_obj(payload) == claimed, "RESTORATION_FIRST_ROW_HASH", ordinal)
        require(claimed == data["first_row_hashes"][ordinal], "RESTORATION_FIRST_HASH_LIST", ordinal)
        require(row["source_parent_transport_id"] in source_transport_ids, "RESTORATION_SOURCE_TRANSPORT_REF", ordinal)
        require(row["target_parent_transport_id"] in target_transport_ids, "RESTORATION_TARGET_TRANSPORT_REF", ordinal)
        root = row["root_id"]
        first_groups[root].add((row["restored_role"], row["source_insertion_index"]))
        first_roles[root].add(row["restored_role"])
        first_proofs[row["proof"]] += 1
        if row["status"] == "continuation":
            continuation_indices.add(ordinal)
    for root, roles in first_roles.items():
        require(first_groups[root] == {(role, index) for role in roles for index in range(7)},
                "RESTORATION_FIRST_CARTESIAN", root)
    second_groups = defaultdict(set)
    second_proofs = Counter()
    for ordinal, row in enumerate(data["second_coverage"]):
        payload = dict(row); claimed = payload.pop("row_sha256")
        require(sha_obj(payload) == claimed, "RESTORATION_SECOND_ROW_HASH", ordinal)
        require(claimed == data["second_row_hashes"][ordinal], "RESTORATION_SECOND_HASH_LIST", ordinal)
        parent = row["parent_first_coverage_index"]
        require(parent in continuation_indices, "RESTORATION_SECOND_NONCONTINUATION_PARENT", ordinal)
        require(row["parent_first_row_sha256"] == data["first_coverage"][parent]["row_sha256"],
                "RESTORATION_SECOND_PARENT_HASH", ordinal)
        second_groups[parent].add(row["second_source_insertion_index"])
        second_proofs[row["proof"]] += 1
    require(set(second_groups) == continuation_indices, "RESTORATION_CONTINUATION_COVERAGE")
    require(all(indices == set(range(8)) for indices in second_groups.values()), "RESTORATION_SECOND_CARTESIAN")
    role_hist = Counter(len(roles) for roles in first_roles.values())
    canonical_parent_ids = {":".join(root.split(":")[:2]) for root in first_roles}
    return {
        "canonical_parents": len(canonical_parent_ids), "member_roots": len(first_roles),
        "root_role_histogram": {str(k): v for k, v in sorted(role_hist.items())},
        "first_children": len(data["first_coverage"]), "first_proofs": dict(first_proofs),
        "continuations": len(continuation_indices), "second_children": len(data["second_coverage"]),
        "second_proofs": dict(second_proofs), "forest_edges": len(data["first_coverage"]) + len(data["second_coverage"]),
        "leaves": len(data["first_coverage"]) - len(continuation_indices) + len(data["second_coverage"]),
        "source_transport_classes": len(source_transport_ids), "target_transport_classes": len(target_transport_ids),
        "file_sha256": sha_file(path), "payload_sha256": data["payload_sha256"],
    }


def validate_candidate_profile(profile, expected_k=None):
    k = profile["port_count"]
    r = profile["reticulation_count"]
    require(expected_k is None or k == expected_k, "PROBE_PROFILE_PORT_COUNT")
    require(profile["site_count"] == 2 * k + 3 * r - 3, "PROBE_SITE_FORMULA", (k, r))
    sites = profile["sites"]
    require(len(sites) == profile["site_count"], "PROBE_SITE_LIST_COUNT")
    require(len({site["site_id"] for site in sites}) == len(sites), "PROBE_SITE_ID_DUPLICATE")
    require(sum(profile["site_type_census"].values()) == len(sites), "PROBE_SITE_TYPE_COUNT")
    return len(sites)


def scan_probe(project: Path):
    contract_path = project / "work/adversarial_proof_review/probe_input_contract.json"
    contract = json.loads(contract_path.read_text())
    origin_counts = Counter()
    relation_counts = Counter()
    source_sites = target_sites = raw_one = 0
    anchor_dims = {}
    for row in contract["anchors"]:
        payload = dict(row); claimed = payload.pop("anchor_row_sha256")
        require(sha_obj(payload) == claimed, "PROBE_ANCHOR_ROW_HASH", row["anchor_id"])
        k = len(row["labels"])
        ns = validate_candidate_profile(row["source_candidate_profile"], k)
        nt = validate_candidate_profile(row["target_candidate_profile"], k)
        anchor_dims[row["anchor_id"]] = (ns, nt)
        source_sites += ns; target_sites += nt; raw_one += ns * nt
        origin_counts[row["origin"]] += 1; relation_counts[row["relation"]] += 1
    one_path = project / "work/probe_coherence_corrected/one_port_ledger.jsonl.gz"
    one_categories = Counter(); one_expected_next = defaultdict(int)
    equality_parents = set(); transport_refs = set(); restriction_refs = set()
    with gzip.open(one_path, "rt") as stream:
        for line in stream:
            row = json.loads(line); anchor = row["parent_anchor_id"]
            ns, nt = anchor_dims[anchor]
            local = row["source_site_index"] * nt + row["target_site_index"]
            require(local == one_expected_next[anchor], "PROBE_ONE_CARTESIAN", (anchor, local, one_expected_next[anchor]))
            one_expected_next[anchor] += 1
            one_categories[row["status"]] += 1
            restriction_refs.update((row["source_parent_restriction_id"], row["target_parent_restriction_id"]))
            if row["status"] in ("isomorphic", "triangle"):
                transport_refs.update((row["parent_transport_id"], row["transport_id"]))
                equality_parents.add(f"P1:{anchor}:{row['source_site_index']}:{row['target_site_index']}")
    require(all(one_expected_next[a] == ns * nt for a, (ns, nt) in anchor_dims.items()), "PROBE_ONE_COMPLETE")
    inv_path = project / "work/probe_coherence_corrected/two_port_parent_inventory.jsonl.gz"
    inventory = {}
    inventory_relation = Counter()
    with gzip.open(inv_path, "rt") as stream:
        for line in stream:
            row = json.loads(line); parent = row["one_port_parent_id"]
            require(parent not in inventory, "PROBE_PARENT_DUPLICATE", parent)
            ns = validate_candidate_profile(row["source_candidate_profile"])
            nt = validate_candidate_profile(row["target_candidate_profile"])
            require(row["raw_second_probe_pairs"] == ns * nt, "PROBE_PARENT_PAIR_COUNT", parent)
            inventory[parent] = (ns, nt)
            inventory_relation[row["relation"]] += 1
    require(set(inventory) == equality_parents, "PROBE_PARENT_INVENTORY_SET")
    two_path = project / "work/probe_coherence_corrected/two_port_ledger.jsonl.gz"
    two_categories = Counter(); two_expected_next = defaultdict(int)
    reversed_checked = 0
    with gzip.open(two_path, "rt") as stream:
        for line in stream:
            row = json.loads(line); parent = row["one_port_parent_id"]
            ns, nt = inventory[parent]
            local = row["second_source_site_index"] * nt + row["second_target_site_index"]
            require(local == two_expected_next[parent], "PROBE_TWO_CARTESIAN", (parent, local, two_expected_next[parent]))
            two_expected_next[parent] += 1
            two_categories[row["status"]] += 1
            restriction_refs.update((row["source_parent_restriction_id"], row["target_parent_restriction_id"]))
            if row["status"] in ("isomorphic", "triangle"):
                transport_refs.update((row["parent_transport_id"], row["transport_id"]))
                require(row.get("reverse_order_certificate") is not None, "PROBE_REVERSE_CERT_MISSING")
                reversed_checked += 1
    require(all(two_expected_next[p] == ns * nt for p, (ns, nt) in inventory.items()), "PROBE_TWO_COMPLETE")
    exact_path = project / "work/probe_coherence_corrected/exact_transport_ledger.jsonl.gz"
    exact_ids = set(); triangle_transports = 0
    with gzip.open(exact_path, "rt") as stream:
        for line in stream:
            row = json.loads(line); record = row["record"]
            require(row["record_id"] not in exact_ids, "PROBE_EXACT_TRANSPORT_DUPLICATE")
            exact_ids.add(row["record_id"])
            require(row["record_id"] == record["transport_sha256"], "PROBE_TRANSPORT_ID_INTERNAL")
            vertex_map = record["vertex_map"]
            require(len({x[0] for x in vertex_map}) == len(vertex_map) == len({x[1] for x in vertex_map}), "PROBE_VERTEX_MAP_BIJECTION")
            edge_map = record["mixed_edge_map"]
            require(len({repr(x[0]) for x in edge_map}) == len(edge_map) == len({repr(x[1]) for x in edge_map}), "PROBE_EDGE_MAP_BIJECTION")
            if record["relation"] == "triangle":
                triangle_transports += 1
                witness = record["ordinary_triangle_arrowhead_witness"]
                for side in ("source", "target"):
                    edges = record[f"{side}_triangle_edges"]
                    headed = witness[f"{side}_headed_edges"]
                    common = witness[f"{side}_common_reticulation"]
                    require(len(edges) == 3 and len(headed) == 2, "PROBE_TRIANGLE_EDGE_COUNT")
                    require(all(common in edge for edge in headed), "PROBE_TRIANGLE_COMMON_RETIC")
                    require(all(edge in edges for edge in headed), "PROBE_TRIANGLE_HEADED_SUBSET")
    require(transport_refs <= exact_ids, "PROBE_MISSING_EXACT_TRANSPORT_REFS", len(transport_refs - exact_ids))
    restriction_path = project / "work/probe_coherence_corrected/parent_restriction_ledger.jsonl.gz"
    restriction_ids = set()
    with gzip.open(restriction_path, "rt") as stream:
        for line in stream:
            row = json.loads(line)
            require(row["record_id"] not in restriction_ids, "PROBE_RESTRICTION_DUPLICATE")
            restriction_ids.add(row["record_id"])
            record = row["record"]
            require(record["exact_labelled_relation"] == "isomorphic", "PROBE_RESTRICTION_RELATION")
            require(record["parent_mixed_graph_sha256"] == record["restricted_mixed_graph_sha256"],
                    "PROBE_RESTRICTION_GRAPH_MISMATCH")
            require(len(record["restriction_transport_sha256"]) == 64, "PROBE_RESTRICTION_TRANSPORT_DIGEST")
    require(restriction_refs <= restriction_ids, "PROBE_MISSING_RESTRICTION_REFS", len(restriction_refs - restriction_ids))
    return {
        "anchors": len(contract["anchors"]), "origins": dict(origin_counts), "relations": dict(relation_counts),
        "source_sites": source_sites, "target_sites": target_sites, "one_raw_pairs": raw_one,
        "one_counts": dict(one_categories), "one_equalities": len(equality_parents),
        "two_parents": len(inventory), "two_raw_pairs": sum(ns * nt for ns, nt in inventory.values()),
        "two_counts": dict(two_categories), "two_equalities": reversed_checked,
        "exact_transports": len(exact_ids), "triangle_transports": triangle_transports,
        "parent_restrictions": len(restriction_ids),
        "contract_file_sha256": sha_file(contract_path), "one_file_sha256": sha_file(one_path),
        "two_file_sha256": sha_file(two_path), "inventory_file_sha256": sha_file(inv_path),
        "exact_file_sha256": sha_file(exact_path), "restriction_file_sha256": sha_file(restriction_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    project = args.project.resolve()
    target_sets = {}
    for k in (3, 4, 5):
        selected = primitive_targets(k, True)
        marginalized = primitive_targets(k, False)
        target_sets[k] = (selected, marginalized)
    primitive = {
        "target_counts": {str(k): {"incoming_selected": len(v[0]), "incoming_marginalized": len(v[1]), "total": len(v[0]) + len(v[1])}
                          for k, v in target_sets.items()},
        "source_counts": {
            "cycle": len(primitive_sources(("cycle",))),
            "four_port": len(primitive_sources(("theta0", "theta1", "theta3"))),
            "theta2": len(primitive_sources(("theta2",))),
        },
    }
    composite_root = project / "work/corrected_composite_ledgers/artifacts"
    raw4 = scan_composite(composite_root / "raw4_corrected_composite_ledger.jsonl.gz", 4, 6,
                          len(target_sets[4][0]) + len(target_sets[4][1]))
    theta2 = scan_composite(composite_root / "theta2_corrected_composite_ledger.jsonl.gz", 5, 4,
                            len(target_sets[5][0]) + len(target_sets[5][1]))
    terminal = scan_terminal_registry(composite_root / "raw4_terminal_certificate_registry.json.gz")
    theta2_restoration = scan_theta2_restoration(project / "work/theta2_five_port_closure/artifacts/fixed_full_restoration_closure.json.gz")
    cycle = scan_cycle(project / "work/cycle_three_port_closure/promotion/cycle_base_authoritative.jsonl.gz",
                       project / "work/cycle_three_port_closure/promotion/cycle_full_authoritative.jsonl.gz",
                       len(target_sets[3][0]) + len(target_sets[3][1]))
    restoration = scan_restoration(project / "work/restoration_sign_reclassification/corrected_restoration_forest.json")
    probe = scan_probe(project)
    result = {
        "schema": "independent-k2p-finite-census-audit-v1",
        "independence": "No submitted classifier, canonicalizer, generator, or verifier imported; literal primitive specifications plus streamed artifact contracts.",
        "primitive": primitive, "raw4": raw4, "terminal_registry": terminal,
        "theta2": theta2, "theta2_restoration": theta2_restoration,
        "cycle": cycle, "restoration": restoration, "probe": probe,
        "status": "PASS",
    }
    payload = dict(result)
    result["payload_sha256"] = sha_obj(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "runtime_seconds": time.monotonic() - started,
                      "payload_sha256": result["payload_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
