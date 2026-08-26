#!/usr/bin/env python3
"""Independent finite-domain and ledger-contract audit.

This script intentionally imports no submission module.  It independently
enumerates the primitive completion grammar, decodes raw IDs, and checks the
stored finite streams and parent/reference contracts.  It does not claim to
rederive every analytic category predicate.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path


CORE = {
    "cycle": {"arcs": 2, "sinks": 1, "repairs": ((),)},
    "theta0": {"arcs": 5, "sinks": 1, "repairs": ((2, 3), (3, 4))},
    "theta1": {"arcs": 5, "sinks": 1, "repairs": ((2, 3), (2, 4))},
    "theta2": {"arcs": 6, "sinks": 2, "repairs": ((2, 3), (2, 5), (3, 4), (4, 5))},
    "theta3": {"arcs": 6, "sinks": 2, "repairs": ((2,), (4,))},
}


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha_obj(value):
    return hashlib.sha256(canon(value)).hexdigest()


def sha_file(path: Path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition, code, detail=None):
    if not condition:
        raise AssertionError(code if detail is None else f"{code}:{detail}")


def compositions(total: int, width: int):
    if width == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, width - 1):
            yield (first,) + rest


def completion_keys(k: int, incoming_selected: bool):
    """Literal completion grammar, independent of the submitted atlas."""
    rows = []
    outgoing = k - 1 if incoming_selected else k
    for core, spec in CORE.items():
        for mask in range(1 << spec["sinks"]):
            ordinary = outgoing - mask.bit_count()
            if ordinary < 0:
                continue
            for counts in compositions(ordinary, spec["arcs"]):
                repair_choices = spec["repairs"] if core != "cycle" else ((),)
                for repair_index, repair in enumerate(repair_choices):
                    repaired = tuple(
                        count if count else ("D" if edge in repair else 0)
                        for edge, count in enumerate(counts)
                    )
                    rows.append((core, mask, counts, repair_index if core != "cycle" else None, repaired))
    require(len(rows) == len(set(rows)), "PRIMITIVE_DUPLICATE")
    return rows


def stream_composite(path: Path, sources: int, targets: int, expected: dict[str, int]):
    port_count = 4 if sources == 6 else 5
    permutations = tuple(itertools.permutations(range(port_count)))
    per_source = targets * len(permutations)
    counts = Counter()
    evidence_kinds = Counter()
    plain = hashlib.sha256()
    last = -1
    with gzip.open(path, "rb") as handle:
        for ordinal, line in enumerate(handle):
            require(line.endswith(b"\n"), "COMPOSITE_NEWLINE", ordinal)
            plain.update(line)
            row = json.loads(line)
            require(canon(row) == line[:-1], "COMPOSITE_CANONICAL_JSON", ordinal)
            require(row.get("raw_id") == ordinal, "COMPOSITE_DENSE_RAW_ID", ordinal)
            source, rem = divmod(ordinal, per_source)
            target, perm_index = divmod(rem, len(permutations))
            require(row.get("source_index") == source, "COMPOSITE_SOURCE_INDEX", ordinal)
            require(row.get("target_index") == target, "COMPOSITE_TARGET_INDEX", ordinal)
            require(row.get("permutation_index") == perm_index, "COMPOSITE_PERM_INDEX", ordinal)
            require(row.get("port_permutation") == list(permutations[perm_index]), "COMPOSITE_PORT_WORD", ordinal)
            require(isinstance(row.get("evidence_binding"), dict), "COMPOSITE_EVIDENCE", ordinal)
            counts[row.get("corrected_category")] += 1
            evidence_kinds[row["evidence_binding"].get("kind")] += 1
            last = ordinal
    require(last + 1 == sources * per_source, "COMPOSITE_TOTAL", last + 1)
    require(dict(counts) == expected, "COMPOSITE_PARTITION", counts)
    return {
        "rows": last + 1,
        "category_counts": dict(sorted(counts.items())),
        "evidence_kind_counts": dict(sorted(evidence_kinds.items(), key=lambda item: str(item[0]))),
        "file_sha256": sha_file(path),
        "plain_sha256": plain.hexdigest(),
    }


def stream_ordered(path: Path, id_field: str, category_field: str):
    counts = Counter()
    last = -1
    with gzip.open(path, "rt") as handle:
        for ordinal, line in enumerate(handle):
            row = json.loads(line)
            require(row.get(id_field) == ordinal, "ORDERED_ID", (path.name, ordinal, row.get(id_field)))
            counts[row.get(category_field)] += 1
            last = ordinal
    return last + 1, dict(sorted(counts.items(), key=lambda item: str(item[0])))


def theta2_forest(project: Path):
    path = project / "work/theta2_five_port_closure/artifacts/fixed_full_restoration_closure.json.gz"
    with gzip.open(path, "rt") as handle:
        data = json.load(handle)
    roots = data["restoration_roots"]
    six = data["six_port_rows"]
    seven = data["seven_port_rows"]
    require(len(roots) == 56, "THETA2_ROOTS")
    require(len({row["base_raw_id"] for row in roots}) == 56, "THETA2_ROOT_UNIQUE")
    root_ids = {row["anchor_id"] for row in roots}
    require(len(root_ids) == 56, "THETA2_ROOT_ID_UNIQUE")
    six_ids = {row["path_id"] for row in six}
    require(len(six) == len(six_ids) == 576, "THETA2_SIX_UNIQUE")
    require(all(row["anchor_id"] in root_ids for row in six), "THETA2_SIX_PARENT")
    continuations = {row["path_id"] for row in six if row["category"] == "isomorphic" and row.get("remaining_roles")}
    require(len(continuations) == 32, "THETA2_CONTINUATIONS")
    require(len(seven) == 288 and len({row["path_id"] for row in seven}) == 288, "THETA2_SEVEN_UNIQUE")
    require(all(row["parent_path_id"] in continuations for row in seven), "THETA2_SEVEN_PARENT")
    six_counts = Counter(row["category"] for row in six)
    seven_counts = Counter(row["category"] for row in seven)
    require(six_counts == {"quartet_pointwise_excluded": 504, "isomorphic": 72}, "THETA2_SIX_COUNTS", six_counts)
    require(seven_counts == {"quartet_pointwise_excluded": 256, "isomorphic": 32}, "THETA2_SEVEN_COUNTS", seven_counts)
    return {
        "roots": 56,
        "six_children": len(six),
        "continuations": len(continuations),
        "seven_children": len(seven),
        "descendants": len(six) + len(seven),
        "leaves": len(six) - len(continuations) + len(seven),
        "six_categories": dict(six_counts),
        "seven_categories": dict(seven_counts),
        "file_sha256": sha_file(path),
    }


def cycle_layers(project: Path):
    base = project / "work/cycle_three_port_closure/promotion/cycle_base_authoritative.jsonl.gz"
    full = project / "work/cycle_three_port_closure/promotion/cycle_full_authoritative.jsonl.gz"
    base_rows, base_counts = stream_ordered(base, "raw_id", "terminal_kind")
    full_rows, full_counts = stream_ordered(full, "raw_id", "terminal_kind")
    require(base_rows == 13_440, "CYCLE_BASE_TOTAL")
    require(base_counts == {
        "fixed_full_restoration_obligation": 5_964,
        "full_map_Ti_strict_sign": 7_452,
        "labelled_isomorphism": 8,
        "ordinary_triangle_relation": 16,
    }, "CYCLE_BASE_PARTITION", base_counts)
    require(full_rows == 536_364, "CYCLE_FULL_TOTAL")
    require(full_counts == {
        "displayed_quartet_strict_separator": 535_920,
        "exact_directional_quadratic": 132,
        "full_map_Ti_strict_sign": 300,
        "labelled_isomorphism": 12,
    }, "CYCLE_FULL_PARTITION", full_counts)
    return {
        "base": {"rows": base_rows, "counts": base_counts, "sha256": sha_file(base)},
        "full": {"rows": full_rows, "counts": full_counts, "sha256": sha_file(full)},
    }


def terminal_registry(project: Path):
    path = project / "work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz"
    with gzip.open(path, "rt") as handle:
        data = json.load(handle)
    rows = data["rows"]
    require(len(rows) == 934, "TERMINAL_CLASS_TOTAL")
    ids = {(row["source_index"], row["class_id"]) for row in rows}
    require(len(ids) == 934, "TERMINAL_CLASS_UNIQUE")
    kinds = Counter(row["terminal_certificate"]["kind"] for row in rows)
    expected = {
        "exact_multihomogeneous_quadratic": 839,
        "exact_direct_polynomial_separator": 36,
        "direct_hard_case_F2_F3_F4": 4,
        "exact_mixed_graph_isomorphism": 20,
        "ordinary_triangle_quotient": 35,
    }
    require(kinds == expected, "TERMINAL_KIND_COUNTS", kinds)
    degrees = Counter(
        row["terminal_certificate"].get("degree")
        for row in rows
        if row["terminal_certificate"]["kind"] == "exact_direct_polynomial_separator"
    )
    require(degrees == {3: 2, 4: 12, 5: 22}, "TERMINAL_DEGREES", degrees)
    return {"classes": 934, "kinds": dict(kinds), "higher_degrees": dict(degrees), "sha256": sha_file(path)}


def restoration(project: Path):
    path = project / "work/restoration_sign_reclassification/corrected_restoration_forest.json"
    data = json.loads(path.read_text())
    first, second = data["first_coverage"], data["second_coverage"]
    require(len(first) == 36_568 and len(second) == 256, "RESTORATION_CHILD_COUNTS")
    for ordinal, row in enumerate(first):
        require(row["ordinal"] == ordinal, "RESTORATION_FIRST_ORDINAL", ordinal)
        require(row["row_sha256"] == sha_obj({k: v for k, v in row.items() if k != "row_sha256"}), "RESTORATION_FIRST_HASH", ordinal)
    first_hashes = {row["row_sha256"] for row in first}
    require(len(first_hashes) == len(first), "RESTORATION_FIRST_DUPLICATE")
    for row in second:
        require(row["parent_first_coverage_index"] < len(first), "RESTORATION_SECOND_INDEX")
        parent = first[row["parent_first_coverage_index"]]
        require(row["parent_first_row_sha256"] == parent["row_sha256"], "RESTORATION_SECOND_PARENT_HASH")
        require(row["root_id"] == parent["root_id"], "RESTORATION_SECOND_ROOT")
        require(row["row_sha256"] == sha_obj({k: v for k, v in row.items() if k != "row_sha256"}), "RESTORATION_SECOND_HASH")
    roots = {row["root_id"] for row in first}
    require(len(roots) == 2_540, "RESTORATION_ROOTS", len(roots))
    parent_ids = {":".join(root.split(":")[:2]) for root in roots}
    require(len(parent_ids) == 997, "RESTORATION_CANONICAL_PARENTS", len(parent_ids))
    first_status = Counter(row["status"] for row in first)
    require(first_status == {"separated": 36_536, "continuation": 32}, "RESTORATION_FIRST_STATUS", first_status)
    continuation_hashes = {row["row_sha256"] for row in first if row["status"] == "continuation"}
    require({row["parent_first_row_sha256"] for row in second} == continuation_hashes, "RESTORATION_CONTINUATION_COVERAGE")
    source_transports = data["first_source_transport_certificates"]
    target_transports = data["first_target_transport_certificates"]
    source_refs = {row["source_parent_transport_id"] for row in first}
    target_refs = {row["target_parent_transport_id"] for row in first}
    require(source_refs == set(source_transports) and len(source_refs) == 42, "RESTORATION_SOURCE_TRANSPORTS")
    require(target_refs == set(target_transports) and len(target_refs) == 4_986, "RESTORATION_TARGET_TRANSPORTS")
    return {
        "canonical_parents": len(parent_ids),
        "member_roots": len(roots),
        "first_children": len(first),
        "second_children": len(second),
        "edges": len(first) + len(second),
        "leaves": first_status["separated"] + len(second),
        "depth": 2,
        "source_transport_classes": len(source_refs),
        "target_transport_classes": len(target_refs),
        "first_proofs": dict(Counter(row["proof"] for row in first)),
        "second_proofs": dict(Counter(row["proof"] for row in second)),
        "sha256": sha_file(path),
    }


def probe(project: Path):
    certificate_path = project / "work/probe_coherence_corrected/probe_coherence_certificate.json"
    certificate = json.loads(certificate_path.read_text())
    anchor_rows = certificate["anchor_inventory"]["public_anchors"]
    require(len(anchor_rows) == 176, "PROBE_ANCHORS")
    anchors = {row["anchor_id"]: row for row in anchor_rows}
    require(len(anchors) == 176, "PROBE_ANCHOR_UNIQUE")
    source_sites = sum(row["source_site_count"] for row in anchor_rows)
    target_sites = sum(row["target_site_count"] for row in anchor_rows)
    require((source_sites, target_sites) == (2_206, 2_206), "PROBE_SITE_COUNTS")
    expected_one = sum(row["source_site_count"] * row["target_site_count"] for row in anchor_rows)
    require(expected_one == 29_964, "PROBE_ONE_CARTESIAN")

    one_path = project / "work/probe_coherence_corrected/one_port_ledger.jsonl.gz"
    one_keys = set()
    one_counts = Counter()
    one_equal = 0
    transport_refs = {row["transport_id"] for row in anchor_rows}
    restriction_refs = set()
    with gzip.open(one_path, "rt") as handle:
        for row_number, line in enumerate(handle):
            row = json.loads(line)
            anchor = anchors[row["parent_anchor_id"]]
            key = (row["parent_anchor_id"], row["source_site_index"], row["target_site_index"])
            require(key not in one_keys, "PROBE_ONE_DUPLICATE", key)
            one_keys.add(key)
            require(0 <= row["source_site_index"] < anchor["source_site_count"], "PROBE_ONE_SOURCE_SITE", key)
            require(0 <= row["target_site_index"] < anchor["target_site_count"], "PROBE_ONE_TARGET_SITE", key)
            one_counts[row["status"]] += 1
            if row["status"] in {"isomorphic", "triangle"}:
                one_equal += 1
                transport_refs.add(row["transport_id"])
            restriction_refs.update((row["source_parent_restriction_id"], row["target_parent_restriction_id"]))
    require(len(one_keys) == expected_one, "PROBE_ONE_ROWS")
    require(one_equal == 2_107, "PROBE_ONE_EQUALITIES")

    parent_path = project / "work/probe_coherence_corrected/two_port_parent_inventory.jsonl.gz"
    parents = {}
    expected_two = 0
    with gzip.open(parent_path, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            pid = row["one_port_parent_id"]
            require(pid not in parents, "PROBE_PARENT_DUPLICATE", pid)
            product_count = row["source_candidate_profile"]["site_count"] * row["target_candidate_profile"]["site_count"]
            require(row["raw_second_probe_pairs"] == product_count, "PROBE_PARENT_CARTESIAN", pid)
            expected_two += product_count
            parents[pid] = row
    require(len(parents) == 2_107 and expected_two == 544_571, "PROBE_PARENT_COUNTS")

    two_path = project / "work/probe_coherence_corrected/two_port_ledger.jsonl.gz"
    two_keys = set()
    two_counts = Counter()
    two_equal = 0
    with gzip.open(two_path, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            parent = parents[row["one_port_parent_id"]]
            key = (row["one_port_parent_id"], row["second_source_site_index"], row["second_target_site_index"])
            require(key not in two_keys, "PROBE_TWO_DUPLICATE", key)
            two_keys.add(key)
            require(0 <= row["second_source_site_index"] < parent["source_candidate_profile"]["site_count"], "PROBE_TWO_SOURCE_SITE", key)
            require(0 <= row["second_target_site_index"] < parent["target_candidate_profile"]["site_count"], "PROBE_TWO_TARGET_SITE", key)
            two_counts[row["status"]] += 1
            reverse = row.get("reverse_order_certificate")
            if row["status"] in {"isomorphic", "triangle"}:
                require(isinstance(reverse, dict) and reverse.get("same_base_anchor_id") == row["base_anchor_id"], "PROBE_REVERSE_CERTIFICATE", key)
                two_equal += 1
                transport_refs.add(row["transport_id"])
                transport_refs.add(reverse["reverse_parent_transport_id"])
            restriction_refs.update((row["source_parent_restriction_id"], row["target_parent_restriction_id"]))
    require(len(two_keys) == expected_two, "PROBE_TWO_ROWS")
    require(two_equal == 32_729, "PROBE_TWO_EQUALITIES")

    transport_path = project / "work/probe_coherence_corrected/exact_transport_ledger.jsonl.gz"
    ledger_transports = set()
    with gzip.open(transport_path, "rt") as handle:
        for line in handle:
            wrapper = json.loads(line)
            rid = wrapper["record_id"]
            require(rid not in ledger_transports, "PROBE_TRANSPORT_DUPLICATE", rid)
            ledger_transports.add(rid)
    require(len(ledger_transports) == 67_741, "PROBE_TRANSPORT_COUNT")
    require(transport_refs == ledger_transports, "PROBE_TRANSPORT_REFERENCE_CLOSURE", (len(transport_refs), len(ledger_transports)))

    restriction_path = project / "work/probe_coherence_corrected/parent_restriction_ledger.jsonl.gz"
    ledger_restrictions = set()
    with gzip.open(restriction_path, "rt") as handle:
        for line in handle:
            wrapper = json.loads(line)
            rid = wrapper["record_id"]
            require(rid not in ledger_restrictions, "PROBE_RESTRICTION_DUPLICATE", rid)
            ledger_restrictions.add(rid)
    require(len(ledger_restrictions) == 4_379, "PROBE_RESTRICTION_COUNT")
    require(restriction_refs == ledger_restrictions, "PROBE_RESTRICTION_REFERENCE_CLOSURE", (len(restriction_refs), len(ledger_restrictions)))
    return {
        "anchors": len(anchors),
        "source_sites": source_sites,
        "target_sites": target_sites,
        "one_rows": len(one_keys),
        "one_counts": dict(one_counts),
        "one_equalities": one_equal,
        "two_parents": len(parents),
        "two_rows": len(two_keys),
        "two_counts": dict(two_counts),
        "two_equalities": two_equal,
        "exact_transports": len(ledger_transports),
        "parent_restrictions": len(ledger_restrictions),
        "input_sha256": {
            "certificate": sha_file(certificate_path),
            "one": sha_file(one_path),
            "two_parents": sha_file(parent_path),
            "two": sha_file(two_path),
            "transports": sha_file(transport_path),
            "restrictions": sha_file(restriction_path),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    project = args.project.resolve()

    primitive = {}
    for k in (3, 4, 5):
        selected = completion_keys(k, True)
        marginalized = completion_keys(k, False)
        primitive[str(k)] = {"selected": len(selected), "marginalized": len(marginalized), "total": len(selected) + len(marginalized)}
    require(primitive == {
        "3": {"selected": 289, "marginalized": 831, "total": 1120},
        "4": {"selected": 831, "marginalized": 1983, "total": 2814},
        "5": {"selected": 1983, "marginalized": 4155, "total": 6138},
    }, "PRIMITIVE_COUNTS", primitive)

    raw4_path = project / "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz"
    theta2_path = project / "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_ledger.jsonl.gz"
    result = {
        "schema": "fresh-independent-finite-contract-audit-v1",
        "status": "PASS",
        "independence_boundary": "primitive completion domains/raw IDs and stored parent/reference contracts independently regenerated; analytic category predicates counted from submitted ledgers, not independently reclassified",
        "primitive": {"source_supports": {"raw4": 6, "theta2": 4, "cycle": 2}, "targets": primitive},
        "raw4": stream_composite(raw4_path, 6, 2814, {
            "direct_terminal_presentation": 1_472,
            "displayed_quartet_exclusion": 360_408,
            "exact_rank_exclusion": 23_822,
            "full_map_Ti_strict_sign": 16_974,
            "restoration_member_presentation": 2_540,
        }),
        "theta2": stream_composite(theta2_path, 4, 6138, {
            "direct_quadratic_separator": 240,
            "displayed_quartet_exclusion": 2_942_592,
            "exact_rank_exclusion": 800,
            "full_map_Ti_strict_sign": 2_528,
            "labelled_isomorphism": 80,
        }),
        "raw4_terminals": terminal_registry(project),
        "theta2_forest": theta2_forest(project),
        "cycle": cycle_layers(project),
        "restoration": restoration(project),
        "probe": probe(project),
    }
    result["payload_sha256"] = sha_obj(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "payload_sha256": result["payload_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
