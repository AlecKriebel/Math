#!/usr/bin/env python3
"""Independent fail-closed replay of either corrected composite ledger.

This verifier does not import the producer.  It regenerates the primitive
source/target/permutation coordinates, recomputes every displayed-quartet
witness, rebinds every non-quartet certificate from its locked proof artifact,
and independently reserializes the complete gzip byte stream in a temporary
file.  Optional whole-map replayers algebraically rebuild every signed map.
"""

from __future__ import annotations

import argparse
import collections
import dataclasses
import gzip
import hashlib
import importlib.util
import itertools
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ARTIFACTS = HERE / "artifacts"
PACKAGE = PROJECT / "package/referee/k2p_offline_sweep_portable"
STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import (  # noqa: E402
    decode_json_document,
    iter_canonical_gzip_jsonl,
    load_canonical_gzip_json,
)
TOTALS = {"raw4": 405_216, "theta2": 2_946_240}
EXPECTED = {
    "raw4": {
        "displayed_quartet_exclusion": 360_408,
        "full_map_Ti_strict_sign": 16_974,
        "exact_rank_exclusion": 23_822,
        "direct_terminal_presentation": 1_472,
        "restoration_member_presentation": 2_540,
    },
    "theta2": {
        "displayed_quartet_exclusion": 2_942_592,
        "full_map_Ti_strict_sign": 2_528,
        "exact_rank_exclusion": 800,
        "direct_quadratic_separator": 240,
        "labelled_isomorphism": 80,
    },
}
FORBIDDEN = (b"tree_sunlet", b"strict_tree_sunlet_sign", b"tree_sunlet_pointwise_excluded", b"tree_sunlet_REVOKED")


class ReplayFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise ReplayFailure(code if detail is None else f"{code}:{detail}")


def canonical_data(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {field.name: canonical_data(getattr(value, field.name)) for field in dataclasses.fields(value)}
    if isinstance(value, dict):
        return {str(key): canonical_data(item) for key, item in sorted(value.items(), key=lambda pair: repr(pair[0]))}
    if isinstance(value, (tuple, list)):
        return [canonical_data(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted((canonical_data(item) for item in value), key=repr)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(canonical_data(value), sort_keys=True, separators=(",", ":")).encode()


def sha_object(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_payload(value: dict[str, Any]) -> None:
    claimed = value.get("payload_sha256")
    body = dict(value)
    body.pop("payload_sha256", None)
    require(claimed == sha_object(body), "PAYLOAD_HASH_FAIL")


def load_json(path: Path) -> dict[str, Any]:
    value = decode_json_document(path.read_bytes(), label=path.name, require_object=True)
    require(isinstance(value, dict), "JSON_OBJECT_FAIL", path)
    return value


def load_gzip_json(path: Path) -> dict[str, Any]:
    value = load_canonical_gzip_json(path, label=path.name)
    require(isinstance(value, dict), "GZIP_JSON_OBJECT_FAIL", path)
    return value


def load_atlas(family: str):
    path = PACKAGE / "atlas/k2p_atlas_core.py"
    spec = importlib.util.spec_from_file_location(f"independent_composite_{family}_atlas", path)
    require(spec is not None and spec.loader is not None, "ATLAS_IMPORT_FAIL")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def quartet_witness(source_signature, permuted_target_signature) -> dict[str, Any] | None:
    _labels, source_quartets, _source_triples = source_signature
    target_quartets, _target_triples = permuted_target_signature
    for (quad, source_values_raw), (target_quad, target_values_raw) in zip(source_quartets, target_quartets):
        require(quad == target_quad, "QUARTET_LABEL_DRIFT")
        if source_values_raw == target_values_raw:
            continue
        source_values, target_values = set(source_values_raw), set(target_values_raw)
        require(bool(source_values) and bool(target_values), "EMPTY_QUARTET_SET")
        if len(source_values) == 1:
            split = next(iter(source_values)); zero_on, positive_on, kind = "source", "target", "I_singleton"
        elif len(target_values) == 1:
            split = next(iter(target_values)); zero_on, positive_on, kind = "target", "source", "I_singleton"
        else:
            difference = target_values - source_values
            if difference:
                split = min(difference, key=repr); zero_on, positive_on = "source", "target"
            else:
                split = min(source_values - target_values, key=repr); zero_on, positive_on = "target", "source"
            kind = "J_membership"
        split_rows = lambda values: sorted([[list(item[0]), list(item[1])] for item in values])
        return {
            "distinguished_split": [list(split[0]), list(split[1])],
            "invariant_kind": kind,
            "quartet": list(quad),
            "reason": "displayed_quartet_mismatch",
            "source_displayed_splits": split_rows(source_values),
            "strictly_positive_on": positive_on,
            "target_displayed_splits": split_rows(target_values),
            "zero_on": zero_on,
        }
    return None


def compact_witness(content: dict[str, Any]) -> dict[str, Any]:
    digest = sha_object(content)
    return {
        "kind": "exact_displayed_quartet_witness",
        "witness_id": f"Q:{digest}",
        "witness_payload_sha256": digest,
        "quartet": content["quartet"],
        "distinguished_split": content["distinguished_split"],
        "invariant_kind": content["invariant_kind"],
        "zero_on": content["zero_on"],
        "strictly_positive_on": content["strictly_positive_on"],
        "source_displayed_splits_sha256": sha_object(content["source_displayed_splits"]),
        "target_displayed_splits_sha256": sha_object(content["target_displayed_splits"]),
    }


def raw4_context(atlas) -> dict[str, Any]:
    lower_path = PROJECT / "work/raw_ledger_audit/artifacts/rank_lower_certificates.json.gz"
    upper_path = PROJECT / "work/raw_ledger_audit/artifacts/rank_upper_binding.json.gz"
    classes_path = PROJECT / "work/raw_ledger_audit/artifacts/retained_class_partition.json.gz"
    overlay_path = PROJECT / "work/raw4_sign_reclassification/raw4_corrected_terminal_ledger.json"
    terminal_path = ARTIFACTS / "raw4_terminal_certificate_registry.json.gz"
    forest_path = PROJECT / "work/restoration_sign_reclassification/corrected_restoration_forest.json"
    lower = {row["descriptor_sha256"]: row for row in load_gzip_json(lower_path)["descriptors"]}
    upper = {row["raw_ledger_descriptor_sha256"]: row for row in load_gzip_json(upper_path)["descriptors"]}
    classes = {(row["source_index"], row["canonical_class_id"]): row for row in load_gzip_json(classes_path)["classes"]}
    terminal_payload = load_gzip_json(terminal_path)
    terminals = {(row["source_index"], row["class_id"]): row for row in terminal_payload["rows"]}
    overlay = load_json(overlay_path)
    class_keys = sorted(overlay["canonical_relation_class_multiplicities"])
    class_ids = {key: index for index, key in enumerate(class_keys)}
    whole_map = {}
    for item in overlay["coverage"]:
        source_hash, target_hash = item["source_pullback_sha256"], item["target_pullback_sha256"]
        sign = overlay["sign_certificates"][source_hash]["sign_certificate"]
        clean_item = {key: value for key, value in item.items() if key != "historical_reason"}
        whole_map[item["raw_id"]] = {
            "kind": "exact_whole_map_Ti_zero_sign_certificate",
            "Ti_relation_class_id": class_ids[f"{source_hash}:{target_hash}"],
            "coordinate_triple": item["source_triple"],
            "chosen_T_orientation_label": item["source_T_orientation_label"],
            "source_pullback_sha256": source_hash,
            "source_pullback_term_count": item["source_pullback_term_count"],
            "source_strict_sign": sign["conclusion"],
            "target_pullback_sha256": target_hash,
            "target_pullback_term_count": 0,
            "target_identically_zero": True,
            "coefficient_certificate_sha256": sign["certificate_sha256"],
            "Bernstein_multidegree": sign["Bernstein_multidegree"],
            "Bernstein_coefficient_count": sign["Bernstein_coefficient_count"],
            "negative_coefficients": sign["negative_coefficients"],
            "zero_coefficients": sign["zero_coefficients"],
            "positive_coefficients": sign["positive_coefficients"],
            "exact_full_graph_relation": item["exact_full_graph_relation"],
            "overlay_evidence_sha256": sha_object(clean_item),
        }
    forest = load_json(forest_path)
    grouped: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for item in forest["first_coverage"]:
        grouped[item["root_id"]].append(item)
    forest_members = {}
    for root_id, children in grouped.items():
        children.sort(key=lambda item: item["ordinal"])
        forest_members[root_id] = {
            "first_child_count": len(children),
            "first_child_row_hash_root": sha_object([row["row_sha256"] for row in children]),
            "first_child_transport_hash_root": sha_object([[row["source_parent_transport_id"], row["target_parent_transport_id"]] for row in children]),
        }
    sources = tuple(atlas.source_supports())
    targets = tuple(atlas.target_completions(4, True) + atlas.target_completions(4, False))
    permutations = tuple(itertools.permutations(range(4)))
    source_digests = tuple(sha_object(atlas.model_descriptor_fast2(source.graph)) for source in sources)
    return {
        "sources": sources, "targets": targets, "permutations": permutations,
        "source_signatures": tuple(atlas.topology_signature(source.graph) for source in sources),
        "target_signatures": tuple(atlas.topology_signature(atlas.selected_graph_from_completion(target)) for target in targets),
        "source_digests": source_digests,
        "source_ranks": tuple(lower[digest]["rank"] for digest in source_digests),
        "lower": lower, "upper": upper, "classes": classes, "terminals": terminals,
        "terminal_payload": terminal_payload, "whole_map": whole_map, "forest": forest,
        "forest_members": forest_members, "target_cache": {}, "class_maps": [dict() for _ in sources],
    }


def theta2_context(atlas) -> dict[str, Any]:
    historical = PROJECT / "work/theta2_five_port_closure/artifacts/raw_directional_ledger.jsonl.gz"
    remaining = {}
    for row in iter_canonical_gzip_jsonl(historical, label=historical.name):
        if row["category"] != "quartet_pointwise_excluded":
            remaining[row["raw_id"]] = row
    direct = load_gzip_json(PROJECT / "work/theta2_five_port_closure/artifacts/direct_proof_certificates.json.gz")
    ranks = {row["descriptor_sha256"]: row for row in load_gzip_json(PROJECT / "work/theta2_five_port_closure/artifacts/exact_rank_certificates.json.gz")["descriptors"]}
    truth = load_json(PROJECT / "work/adversarial_proof_review/theta2_tree_sunlet_full_map_certificate.json")
    selected = sorted((row for row in remaining.values() if row["category"] == "tree_sunlet_pointwise_excluded"), key=lambda row: row["raw_id"])
    truth_hash_by_raw = {row["raw_id"]: truth["ordered_truth_row_hashes"][index] for index, row in enumerate(selected)}
    relation_ids = {key: index for index, key in enumerate(sorted(truth["canonical_relation_class_multiplicities"]))}
    closure = load_gzip_json(PROJECT / "work/theta2_five_port_closure/artifacts/fixed_full_restoration_closure.json.gz")
    roots = {row["base_raw_id"]: row for row in closure["restoration_roots"]}
    first: dict[int, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in closure["six_port_rows"]: first[row["base_raw_id"]].append(row)
    root_bindings = {}
    for raw_id, root in roots.items():
        children = sorted(first[raw_id], key=lambda row: row["path_id"])
        root_bindings[raw_id] = {
            "anchor_id": root["anchor_id"],
            "descendant_root_sha256": sha_object(root),
            "first_child_count": len(children),
            "first_child_id_hash_root": sha_object([row["path_id"] for row in children]),
        }
    sources = tuple(atlas.source_supports(("theta2",)))
    targets = tuple(atlas.target_completions(5, True) + atlas.target_completions(5, False))
    permutations = tuple(itertools.permutations(range(5)))
    return {
        "sources": sources, "targets": targets, "permutations": permutations,
        "source_signatures": tuple(atlas.topology_signature(source.graph) for source in sources),
        "target_signatures": tuple(atlas.topology_signature(atlas.selected_graph_from_completion(target)) for target in targets),
        "source_digests": tuple(sha_object(atlas.model_descriptor_fast2(source.graph)) for source in sources),
        "remaining": remaining, "direct": direct, "ranks": ranks, "truth": truth,
        "truth_hash_by_raw": truth_hash_by_raw, "relation_ids": relation_ids,
        "root_bindings": root_bindings, "target_cache": {},
    }


def expected_nonquartet_raw4(row: dict[str, Any], context: dict[str, Any], atlas) -> None:
    raw_id, source_index, target_index, permutation_index = row["raw_id"], row["source_index"], row["target_index"], row["permutation_index"]
    if raw_id in context["whole_map"]:
        require(row["corrected_category"] == "full_map_Ti_strict_sign", "RAW4_WHOLE_MAP_CATEGORY", raw_id)
        require(row["exact_reason"] == "whole_map_source_strict_sign_target_zero", "RAW4_WHOLE_MAP_REASON", raw_id)
        require(row["evidence_binding"] == context["whole_map"][raw_id], "RAW4_WHOLE_MAP_EVIDENCE", raw_id)
        return
    key = (target_index, permutation_index)
    if key not in context["target_cache"]:
        record = atlas.relabel_record(context["targets"][target_index], context["permutations"][permutation_index])
        digest = sha_object(atlas.model_descriptor_fast2(record.graph))
        context["target_cache"][key] = (digest, context["lower"][digest]["rank"])
    digest, target_rank = context["target_cache"][key]
    require(row.get("target_descriptor_sha256") == digest, "RAW4_TARGET_DESCRIPTOR", raw_id)
    if target_rank < context["source_ranks"][source_index]:
        lower, upper = context["lower"][digest], context["upper"][digest]
        expected = {
            "kind": "matched_exact_rank_lower_symbolic_upper", "source_exact_rank": context["source_ranks"][source_index],
            "target_exact_rank": target_rank, "target_descriptor_sha256": digest,
            "source_lower_certificate_sha256": sha_object(context["lower"][context["source_digests"][source_index]]),
            "source_lower_minor_determinant": context["lower"][context["source_digests"][source_index]]["minor_determinant"],
            "target_lower_certificate_sha256": sha_object(lower), "target_upper_certificate_sha256": sha_object(upper),
            "target_lower_minor_determinant": lower["minor_determinant"], "target_upper_mechanism": upper["upper_mechanism"],
        }
        require(row["corrected_category"] == "exact_rank_exclusion" and row["evidence_binding"] == expected, "RAW4_RANK_EVIDENCE", raw_id)
        return
    class_map = context["class_maps"][source_index]
    if digest not in class_map: class_map[digest] = len(class_map)
    class_id = class_map[digest]
    class_row = context["classes"][(source_index, class_id)]
    require(class_row["descriptor_sha256"] == digest, "RAW4_CLASS_DESCRIPTOR", raw_id)
    class_identifier = f"source_{source_index}:class_{class_id:06d}"
    if class_row["ledger_category"] == "retained_terminal":
        certificate = context["terminals"][(source_index, class_id)]
        expected = {
            "kind": "exact_terminal_class_and_direct_certificate", "terminal_class_id": class_identifier,
            "terminal_certificate_binding_sha256": certificate["certificate_binding_sha256"],
            "terminal_certificate_kind": certificate["terminal_certificate"]["kind"],
            "terminal_registry_payload_sha256": context["terminal_payload"]["payload_sha256"],
        }
        require(row["corrected_category"] == "direct_terminal_presentation" and row["evidence_binding"] == expected, "RAW4_TERMINAL_EVIDENCE", raw_id)
    else:
        parent = class_row["restoration_obligation_id"]
        permutation = row["port_permutation"]
        root_id = f"s{source_index}:c{class_id}:t{target_index}:p{''.join(map(str, permutation))}"
        transport = {
            "canonical_parent_id": parent, "physical_member_root_id": root_id,
            "source_descriptor_sha256": context["source_digests"][source_index],
            "target_descriptor_sha256": digest, "port_permutation": permutation, "direction": "source_to_target",
        }
        expected = {
            "kind": "exact_restoration_parent_and_physical_transport", "restoration_parent_id": parent,
            "physical_member_root_id": root_id, "presentation_transport_sha256": sha_object(transport),
            "forest_payload_sha256": context["forest"]["payload_sha256"], **context["forest_members"][root_id],
        }
        require(row["corrected_category"] == "restoration_member_presentation" and row["evidence_binding"] == expected, "RAW4_RESTORATION_EVIDENCE", raw_id)


def expected_nonquartet_theta2(row: dict[str, Any], context: dict[str, Any], atlas) -> None:
    raw_id = row["raw_id"]
    old = context["remaining"].get(raw_id)
    require(old is not None, "THETA2_NONQUARTET_PROVENANCE_MISSING", raw_id)
    evidence = row["evidence_binding"]
    if old["category"] == "tree_sunlet_pointwise_excluded":
        require(row["corrected_category"] == "full_map_Ti_strict_sign", "THETA2_WHOLE_MAP_CATEGORY", raw_id)
        source_hash, target_hash = evidence["source_pullback_sha256"], evidence["target_pullback_sha256"]
        sign = context["truth"]["sign_certificates"].get(target_hash)
        require(sign is not None, "THETA2_SIGN_HASH", raw_id)
        sign_data = sign["sign"]
        require(evidence["Ti_relation_class_id"] == context["relation_ids"][f"{source_hash}:{target_hash}"], "THETA2_RELATION_CLASS", raw_id)
        require(evidence["source_identically_zero"] is True and evidence["source_pullback_term_count"] == 0, "THETA2_SOURCE_ZERO", raw_id)
        require(evidence["coefficient_certificate_sha256"] == sign_data["certificate_sha256"], "THETA2_SIGN_CERTIFICATE", raw_id)
        truth_row = {
            "raw_id": raw_id, "source_index": row["source_index"], "target_index": row["target_index"],
            "permutation_index": row["permutation_index"], "legacy_witness_triple": evidence["coordinate_triple"],
            "chosen_T_orientation_label": evidence["chosen_T_orientation_label"],
            "source_pullback_sha256": source_hash, "target_pullback_sha256": target_hash,
            "exact_full_graph_relation": "none", "result": "source_zero_strict_target_negative",
        }
        require(sha_object(truth_row) == context["truth_hash_by_raw"][raw_id], "THETA2_TRUTH_ROW_HASH", raw_id)
        return
    target_index, permutation_index = row["target_index"], row["permutation_index"]
    key = (target_index, permutation_index)
    if key not in context["target_cache"]:
        record = atlas.relabel_record(context["targets"][target_index], context["permutations"][permutation_index])
        context["target_cache"][key] = sha_object(atlas.model_descriptor_fast2(record.graph))
    require(row.get("target_descriptor_sha256") == context["target_cache"][key] == old["target_descriptor_sha256"], "THETA2_TARGET_DESCRIPTOR", raw_id)
    if old["category"] == "rank_excluded":
        cert = context["ranks"][old["target_descriptor_sha256"]]
        expected = {
            "kind": "matched_exact_rank_lower_symbolic_upper", "source_exact_rank": old["source_rank"],
            "target_exact_rank": cert["exact_generic_rank"], "target_descriptor_sha256": old["target_descriptor_sha256"],
            "source_lower_certificate_sha256": sha_object(context["ranks"][context["source_digests"][row["source_index"]]]["lower_certificate"]),
            "source_lower_minor_determinant": context["ranks"][context["source_digests"][row["source_index"]]]["lower_certificate"]["minor_determinant"],
            "target_lower_certificate_sha256": sha_object(cert["lower_certificate"]), "target_upper_certificate_sha256": sha_object(cert["upper_certificate"]),
            "target_lower_minor_determinant": cert["lower_certificate"]["minor_determinant"], "target_upper_mechanism": cert["upper_certificate"]["method"],
        }
        require(row["corrected_category"] == "exact_rank_exclusion" and evidence == expected, "THETA2_RANK_EVIDENCE", raw_id)
    elif old["category"] == "quadratic_separated":
        cert = context["direct"]["quadratic_certificates"][old["certificate_id"]]
        expected = {
            "kind": "exact_multihomogeneous_quadratic_separator", "certificate_id": old["certificate_id"],
            "certificate_sha256": sha_object(cert), "degree": cert["degree"], "source_pullback_sha256": cert["source_pullback_sha256"],
            "target_pullback": cert["target_pullback"], "class_id": old["class_id"],
        }
        require(row["corrected_category"] == "direct_quadratic_separator" and evidence == expected, "THETA2_QUADRATIC_EVIDENCE", raw_id)
    elif old["category"] == "isomorphic":
        cert = context["direct"]["isomorphism_certificates"][old["certificate_id"]]
        expected = {
            "kind": "exact_labelled_semi_directed_isomorphism", "certificate_id": old["certificate_id"],
            "certificate_sha256": sha_object(cert), "mixed_vertex_mapping_sha256": sha_object(cert["mixed_vertex_mapping_source_to_target"]),
            "class_id": old["class_id"],
        }
        if raw_id in context["root_bindings"]: expected["physical_restoration_descendants"] = context["root_bindings"][raw_id]
        require(row["corrected_category"] == "labelled_isomorphism" and evidence == expected, "THETA2_ISOMORPHISM_EVIDENCE", raw_id)
    else:
        raise ReplayFailure(f"THETA2_CATEGORY_UNEXPECTED:{raw_id}:{old['category']}")


def run_heavy_full_map(family: str) -> dict[str, Any]:
    if family == "raw4":
        script = PROJECT / "work/raw4_sign_reclassification/verify_raw4_corrected_terminal_ledger.py"
        certificate = PROJECT / "work/raw4_sign_reclassification/raw4_corrected_terminal_ledger.json"
        flag = "--certificate"
    else:
        script = PROJECT / "work/theta2_sign_reclassification/verify_theta2_full_map_independent.py"
        certificate = PROJECT / "work/adversarial_proof_review/theta2_tree_sunlet_full_map_certificate.json"
        flag = "--certificate"
    with tempfile.TemporaryDirectory(prefix=f"k2p-{family}-full-map-") as directory:
        report_path = Path(directory) / "report.json"
        result = subprocess.run(
            [sys.executable, str(script), flag, str(certificate), "--report", str(report_path)],
            cwd=PROJECT, text=True, capture_output=True, check=False,
        )
        require(result.returncode == 0, "HEAVY_FULL_MAP_REPLAY_FAIL", result.stderr[-2000:])
        report = load_json(report_path)
        require(report.get("status") == "PASS", "HEAVY_FULL_MAP_STATUS")
        return {"script_sha256": sha_file(script), "report_payload_sha256": report["payload_sha256"], "rows_replayed": report["raw_rows_replayed"]}


def replay(family: str, ledger: Path, summary_path: Path, report_path: Path, heavy: bool) -> None:
    require(__debug__, "OPTIMIZED_MODE_FORBIDDEN")
    summary = load_json(summary_path); verify_payload(summary)
    total = TOTALS[family]
    require(summary["total_rows"] == total and summary["category_counts"] == EXPECTED[family], "SUMMARY_CENSUS")
    atlas = load_atlas(family)
    context = raw4_context(atlas) if family == "raw4" else theta2_context(atlas)
    require(len(context["sources"]) == (6 if family == "raw4" else 4), "SOURCE_CENSUS")
    require(len(context["targets"]) == (2814 if family == "raw4" else 6138), "TARGET_CENSUS")
    per_source = len(context["targets"]) * len(context["permutations"])
    fingerprints = {"ledger": sha_file(ledger), "summary": sha_file(summary_path), "verifier": sha_file(Path(__file__))}
    categories = collections.Counter()
    row_root = hashlib.sha256(); raw_root = hashlib.sha256(); plain = hashlib.sha256()
    seen = 0
    with tempfile.TemporaryDirectory(prefix=f"k2p-{family}-composite-replay-") as directory:
        regenerated = Path(directory) / "ledger.jsonl.gz"
        with regenerated.open("wb") as raw_output:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw_output, mtime=0, compresslevel=6) as encoded:
                for expected_id, row in enumerate(
                    iter_canonical_gzip_jsonl(ledger, label=ledger.name)
                ):
                    payload = canonical_bytes(row)
                    line = payload + b"\n"
                    require(not any(token in payload for token in FORBIDDEN), "FORBIDDEN_ROOTED_TOKEN", expected_id)
                    require(row.get("raw_id") == expected_id, "RAW_ID_ORDER", expected_id)
                    source_index, remainder = divmod(expected_id, per_source)
                    target_index, permutation_index = divmod(remainder, len(context["permutations"]))
                    permutation = list(context["permutations"][permutation_index])
                    require(row.get("source_index") == source_index and row.get("target_index") == target_index, "RAW_COORDINATE", expected_id)
                    require(row.get("permutation_index") == permutation_index and row.get("port_permutation") == permutation, "PORT_PERMUTATION", expected_id)
                    require(row.get("source_descriptor_sha256") == context["source_digests"][source_index], "SOURCE_DESCRIPTOR", expected_id)
                    require(row.get("schema") == f"k2p-{family}-corrected-composite-row-v1", "ROW_SCHEMA", expected_id)
                    require(isinstance(row.get("evidence_binding"), dict) and len(row["evidence_binding"]) > 2, "EVIDENCE_MISSING", expected_id)
                    content = quartet_witness(
                        context["source_signatures"][source_index],
                        atlas.permute_signature(context["target_signatures"][target_index], tuple(permutation)),
                    )
                    if content is not None:
                        require(row["corrected_category"] == "displayed_quartet_exclusion", "QUARTET_CATEGORY", expected_id)
                        require(row["exact_reason"] == "source_target_displayed_quartet_sets_differ", "QUARTET_REASON", expected_id)
                        require(row["evidence_binding"] == compact_witness(content), "QUARTET_WITNESS", expected_id)
                    else:
                        if family == "raw4": expected_nonquartet_raw4(row, context, atlas)
                        else: expected_nonquartet_theta2(row, context, atlas)
                    categories[row["corrected_category"]] += 1
                    digest = hashlib.sha256(payload).digest(); row_root.update(digest)
                    raw_root.update(hashlib.sha256(canonical_bytes(expected_id)).digest()); plain.update(line)
                    encoded.write(line)
                    seen += 1
                    if seen % 500_000 == 0:
                        print(json.dumps({"family": family, "independent_rows": seen}, sort_keys=True), flush=True)
        regenerated_hash = sha_file(regenerated)
    require(seen == total and categories == EXPECTED[family], "REPLAY_CENSUS", (seen, categories))
    require(regenerated_hash == sha_file(ledger) == summary["ledger_sha256"], "REGENERATED_GZIP_BYTE_MISMATCH")
    require(row_root.hexdigest() == summary["ordered_row_hash_root"], "ROW_HASH_ROOT")
    require(raw_root.hexdigest() == summary["ordered_raw_id_hash_root"], "RAW_ID_HASH_ROOT")
    require(plain.hexdigest() == summary["uncompressed_stream_sha256"], "PLAIN_STREAM_HASH")
    heavy_record = run_heavy_full_map(family) if heavy else {"status": "SKIPPED_STRUCTURAL_PHASE"}
    after = {"ledger": sha_file(ledger), "summary": sha_file(summary_path), "verifier": sha_file(Path(__file__))}
    require(fingerprints == after, "SOURCE_TREE_DRIFT")
    report = {
        "schema": f"k2p-{family}-corrected-composite-independent-replay-v1",
        "status": "PASS",
        "summary_sha256": sha_file(summary_path),
        "source_ledger_sha256": sha_file(ledger),
        "regenerated_ledger_sha256": regenerated_hash,
        "total_rows": total,
        "distinct_raw_ids": total,
        "category_counts": dict(categories),
        "ordered_row_hash_root": row_root.hexdigest(),
        "primitive_graph_generation_replayed": True,
        "source_target_permutations_replayed": True,
        "classification_evidence_replayed": True,
        "canonical_serialization_replayed": True,
        "whole_map_algebraic_replay": heavy_record,
        "duplicate_raw_ids": 0,
        "missing_raw_ids": 0,
        "unresolved": 0,
        "forbidden_rooted_field_count": 0,
        "forbidden_rooted_reason_count": 0,
        "source_tree_drift": 0,
    }
    report["payload_sha256"] = sha_object(report)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"family": family, "status": "PASS", "rows": total, "regenerated_ledger_sha256": regenerated_hash, "payload_sha256": report["payload_sha256"]}, sort_keys=True))


def main() -> None:
    require(__debug__, "OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", choices=("raw4", "theta2"), required=True)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--skip-heavy-full-map", action="store_true")
    args = parser.parse_args()
    ledger = args.ledger or ARTIFACTS / f"{args.family}_corrected_composite_ledger.jsonl.gz"
    summary = args.summary or ARTIFACTS / f"{args.family}_corrected_composite_summary.json"
    report = args.report or ARTIFACTS / f"{args.family}_corrected_composite_independent_replay.json"
    replay(args.family, ledger, summary, report, not args.skip_heavy_full_map)


if __name__ == "__main__":
    try:
        main()
    except (ReplayFailure, KeyError, OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"CORRECTED_COMPOSITE_REPLAY_FAIL:{error}") from error
