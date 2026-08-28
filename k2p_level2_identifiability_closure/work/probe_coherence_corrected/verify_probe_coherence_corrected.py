#!/usr/bin/env python3
"""Independent fail-closed structural/algebra replay of the corrected probe release.

This verifier does not import the producer.  It streams every raw ledger,
rebuilds its Cartesian coverage and ordered hashes, validates every exact-map
and marginal reference, and independently recomputes every stored tensor
Bernstein certificate.  A second graph regeneration audit is maintained by
the adversarial theorem reviewer and cross-bound in the final release.
"""

from __future__ import annotations

import argparse
import collections
import fractions
import hashlib
import itertools
import json
import math
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEFAULT_OUTPUT = HERE / "probe_coherence_independent_verification.json"
STRICT_JSON_DIR = PROJECT / "work" / "final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import (  # noqa: E402
    StrictJSONError,
    decode_json_document,
    iter_canonical_gzip_jsonl,
    load_canonical_gzip_json,
)


class ReplayFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ReplayFailure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class OrderedReplay:
    def __init__(self):
        self.rows = 0
        self.root = sha([])

    def add(self, row):
        row_hash = sha(row)
        self.root = sha({"previous": self.root, "row_sha256": row_hash})
        self.rows += 1

    def require_equal(self, expected, name):
        require(expected["rows"] == self.rows, f"{name} row count")
        require(expected["ordered_hash_root"] == self.root, f"{name} ordered hash root")


def iter_jsonl(path):
    try:
        for number, row in enumerate(
            iter_canonical_gzip_jsonl(path, label=path.name)
        ):
            yield number, row
    except StrictJSONError as error:
        raise ReplayFailure(str(error)) from error


def load_streaming_registry(path, expected, record_kind, validator, compact):
    require(sha_file(path) == expected["sha256"], f"{record_kind} file hash")
    records = {}
    ordered = OrderedReplay()
    for number, row in iter_jsonl(path):
        require(row["record_kind"] == record_kind, f"{record_kind} kind:{number}")
        record_id = row["record_id"]
        require(record_id not in records, f"duplicate {record_kind}:{record_id}")
        validator(record_id, row["record"])
        records[record_id] = compact(row["record"])
        ordered.add(row)
    require(len(records) == expected["unique_records"], f"{record_kind} unique count")
    ordered.require_equal(expected["ordered_records"], record_kind)
    return records


def validate_transport(record_id, record):
    ordinary = record.get("ordinary_triangle_arrowhead_witness")
    public = dict(record)
    public.pop("ordinary_triangle_arrowhead_witness", None)
    claimed = public.pop("transport_sha256")
    require(record_id == claimed == sha(public), f"transport self hash:{record_id}")
    relation = public["relation"]
    require(relation in {"isomorphic", "triangle"}, f"transport relation:{record_id}")
    vertex_map = public["vertex_map"]
    require(len({row[0] for row in vertex_map}) == len(vertex_map), f"transport source vertex function:{record_id}")
    require(len({row[1] for row in vertex_map}) == len(vertex_map), f"transport target vertex bijection:{record_id}")
    edge_map = public["mixed_edge_map"]
    require(len({tuple(row[0]) for row in edge_map}) == len(edge_map), f"transport source edge function:{record_id}")
    require(len({tuple(row[1]) for row in edge_map}) == len(edge_map), f"transport target edge bijection:{record_id}")
    if relation == "isomorphic":
        require(public["source_triangle_edges"] is None, f"isomorphism source triangle:{record_id}")
        require(public["target_triangle_edges"] is None, f"isomorphism target triangle:{record_id}")
        require(ordinary is None, f"isomorphism ordinary witness:{record_id}")
    else:
        require(len(public["source_triangle_edges"]) == 3, f"source triangle edges:{record_id}")
        require(len(public["target_triangle_edges"]) == 3, f"target triangle edges:{record_id}")
        require(ordinary is not None, f"triangle arrowhead witness:{record_id}")
        require(ordinary["required_pattern"] == "exactly two triangle arrows into one common reticulation", f"triangle pattern:{record_id}")
        for side in ("source", "target"):
            common = ordinary[f"{side}_common_reticulation"]
            headed = ordinary[f"{side}_headed_edges"]
            require(len(headed) == 2, f"triangle headed edge count:{record_id}:{side}")
            require(all(common in edge for edge in headed), f"triangle common head:{record_id}:{side}")
            require(all(edge in public[f"{side}_triangle_edges"] for edge in headed), f"triangle headed subset:{record_id}:{side}")


def validate_restriction(record_id, record):
    require(record_id == f"R:{sha(record)}", f"restriction self hash:{record_id}")
    require(record["exact_labelled_relation"] == "isomorphic", f"restriction relation:{record_id}")
    require(isinstance(record["removed_label"], int), f"restriction label:{record_id}")
    for key in (
        "restricted_mixed_graph_sha256", "parent_mixed_graph_sha256",
        "restriction_transport_sha256",
    ):
        require(len(record[key]) == 64, f"restriction hash:{record_id}:{key}")


def compact_transport(record):
    ordinary = record["ordinary_triangle_arrowhead_witness"]
    return {
        "relation": record["relation"],
        "source_triangle_edges": record["source_triangle_edges"],
        "target_triangle_edges": record["target_triangle_edges"],
        "source_common_reticulation": None if ordinary is None else ordinary["source_common_reticulation"],
        "target_common_reticulation": None if ordinary is None else ordinary["target_common_reticulation"],
    }


def compact_restriction(record):
    del record
    return True


def sparse_from_payload(payload):
    result = {}
    for exponent, coefficient in payload:
        key = tuple(exponent)
        require(key not in result, "duplicate sparse exponent")
        value = fractions.Fraction(coefficient)
        require(value, "stored zero sparse coefficient")
        result[key] = value
    return result


def bernstein_replay(polynomial):
    require(polynomial, "empty strict polynomial")
    parameter_count = len(next(iter(polynomial)))
    require(all(len(exponent) == parameter_count for exponent in polynomial), "sparse width")
    common = tuple(min(exponent[i] for exponent in polynomial) for i in range(parameter_count))
    active = tuple(i for i in range(parameter_count) if len({exponent[i] for exponent in polynomial}) > 1)
    reduced = collections.defaultdict(fractions.Fraction)
    for exponent, coefficient in polynomial.items():
        reduced[tuple(exponent[i] - common[i] for i in active)] += coefficient
    reduced = {exponent: coefficient for exponent, coefficient in reduced.items() if coefficient}
    degrees = tuple(max(exponent[i] for exponent in reduced) for i in range(len(active)))
    shape = tuple(degree + 1 for degree in degrees)
    count = math.prod(shape)
    require(count <= 2_000_000, "Bernstein replay cap")
    strides = tuple(math.prod(shape[i + 1 :]) for i in range(len(shape)))
    values = [fractions.Fraction(0)] * count
    for exponent, coefficient in reduced.items():
        values[sum(value * stride for value, stride in zip(exponent, strides))] += coefficient
    for axis, degree in enumerate(degrees):
        stride = strides[axis]
        outer = math.prod(shape[:axis])
        block = (degree + 1) * stride
        transformed = [fractions.Fraction(0)] * count
        for outer_index in range(outer):
            base = outer_index * block
            for inner_index in range(stride):
                source = [values[base + value * stride + inner_index] for value in range(degree + 1)]
                for beta in range(degree + 1):
                    total = fractions.Fraction(0)
                    for alpha in range(beta + 1):
                        if source[alpha]:
                            total += source[alpha] * fractions.Fraction(
                                math.comb(beta, alpha), math.comb(degree, alpha)
                            )
                    transformed[base + beta * stride + inner_index] = total
        values = transformed
    signs = collections.Counter(-1 if value < 0 else 1 if value > 0 else 0 for value in values)
    require(not (signs[-1] and signs[1]), "mixed Bernstein signs")
    require(signs[-1] or signs[1], "zero Bernstein polynomial")
    return {
        "method": "exact_tensor_Bernstein_after_strictly_positive_monomial",
        "parameter_count": parameter_count,
        "strictly_positive_monomial_exponent": list(common),
        "active_parameter_indices": list(active),
        "Bernstein_multidegree": list(degrees),
        "Bernstein_coefficient_count": count,
        "negative_coefficients": signs[-1],
        "zero_coefficients": signs[0],
        "positive_coefficients": signs[1],
        "minimum_coefficient": str(min(values)),
        "maximum_coefficient": str(max(values)),
        "ordered_Bernstein_coefficients_sha256": sha([str(value) for value in values]),
        "strict_sign": -1 if signs[-1] else 1,
        "domain": (
            "the full open unit cube in physical edge-sector and inheritance "
            "variables, which contains the physical principal D_plus subset"
        ),
    }


def validate_profile(profile, name):
    require(profile["all_mixed_edge_sites_included"] is True, f"profile completeness:{name}")
    require(profile["site_count"] == 2 * profile["port_count"] + 3 * profile["reticulation_count"] - 3, f"profile formula:{name}")
    require(len(profile["sites"]) == profile["site_count"], f"profile site rows:{name}")
    require(len({row["site_id"] for row in profile["sites"]}) == profile["site_count"], f"profile site IDs:{name}")
    require(profile["root_half_equivalence"]["semi_directed_relation_after_insertion"] == "isomorphic", f"profile root halves:{name}")
    require(
        profile["ordered_site_hash_root"] == sha([sha(row) for row in profile["sites"]]),
        f"profile ordered site root:{name}",
    )


def validate_inherited_triangle(row, base_anchor, transports, name):
    inherited = base_anchor["global_triangle"]
    expected_hash = None if inherited is None else sha(inherited)
    require(row["global_triangle_sha256"] == expected_hash, f"global triangle hash:{name}")
    transport = transports[row["transport_id"]]
    if row["status"] == "triangle":
        require(inherited is not None, f"new triangle above isomorphism:{name}")
        require(transport["source_triangle_edges"] == inherited["source_triangle_edges"], f"source inherited triangle:{name}")
        require(transport["target_triangle_edges"] == inherited["target_triangle_edges"], f"target inherited triangle:{name}")
        require(transport["source_common_reticulation"] == inherited["source_reticulation"], f"source inherited reticulation:{name}")
        require(transport["target_common_reticulation"] == inherited["target_reticulation"], f"target inherited reticulation:{name}")


def logical_payload(report):
    value = dict(report)
    value.pop("payload_sha256", None)
    value.pop("operational", None)
    return sha(value)


def main():
    if not __debug__:
        raise ReplayFailure("CORRECTED_PROBE_REPLAY_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", type=Path, default=HERE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    root = args.package_dir.resolve()
    started = time.monotonic()
    certificate_path = root / "probe_coherence_certificate.json"
    report = decode_json_document(
        certificate_path.read_bytes(),
        label=certificate_path.name,
        require_object=True,
    )
    require(report["schema"] == "k2p-corrected-coherent-probe-closure-v1", "schema")
    require(report["status"] == "PASS", "release status")
    require(report["payload_sha256"] == logical_payload(report), "logical payload")
    require(report["forbidden_rooted_triple_oracle_used"] is False, "rooted oracle flag")
    require(report["classifier_order"] == [
        "exact_labelled_isomorphism_or_ordinary_triangle",
        "displayed_quartet_mismatch",
        "direct_original_full_map_Ti_zero_versus_Bernstein_strict_sign",
        "unresolved_fatal",
    ], "classifier order")

    input_paths = {
        "atlas_sha256": PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py",
        "probe_input_contract_sha256": PROJECT / "work/adversarial_proof_review/probe_input_contract.json",
        "probe_input_independent_replay_sha256": PROJECT / "work/adversarial_proof_review/probe_input_independent_verification.json",
        "probe_input_mutations_sha256": PROJECT / "work/adversarial_proof_review/probe_input_mutation_certificate.json",
        "corrected_restoration_sha256": PROJECT / "work/restoration_sign_reclassification/corrected_restoration_forest.json",
        "raw4_ledger_sha256": PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz",
        "theta2_fixed_full_closure_sha256": PROJECT / "work/theta2_five_port_closure/artifacts/fixed_full_restoration_closure.json.gz",
        "cycle_physical_anchors_sha256": PROJECT / "work/cycle_three_port_closure/artifacts/physical_anchors.json",
        "cycle_promotion_sha256": PROJECT / "work/cycle_three_port_closure/promotion/cycle_promotion_certificate.json",
    }
    for field, path in input_paths.items():
        require(sha_file(path) == report["inputs"][field], f"input binding:{field}")

    proof_path = root / report["registries"]["separation"]["path"]
    require(sha_file(proof_path) == report["registries"]["separation"]["sha256"], "proof registry file hash")
    proof = load_canonical_gzip_json(proof_path, label=proof_path.name)
    claimed = proof.pop("payload_sha256")
    require(claimed == sha(proof), "proof registry payload")
    proof["payload_sha256"] = claimed
    require(claimed == report["registries"]["separation"]["payload_sha256"], "proof registry cross-binding")
    topological = proof["separation_proof_registry"]
    for proof_id, item in topological.items():
        require(proof_id == f"Q:{sha(item)}", f"quartet proof self hash:{proof_id}")
        require(item["source_displayed_splits"] != item["target_displayed_splits"], f"quartet proof inequality:{proof_id}")

    ti = proof["full_map_Ti_registry"]
    strict_polynomials = ti["strict_polynomial_registry"]
    for polynomial_id, item in strict_polynomials.items():
        polynomial = sparse_from_payload(item["pullback"])
        require(polynomial_id == item["pullback_sha256"] == sha(item["pullback"]), f"strict polynomial hash:{polynomial_id}")
        replayed = bernstein_replay(polynomial)
        require(replayed == item["Bernstein_certificate"], f"Bernstein replay:{polynomial_id}")
        parameter_indices = {
            index
            for row in item["parameterization"]["edge_sector_pairs"]
            for index in row[2:]
        } | {
            row[1] for row in item["parameterization"]["inheritance_variables"]
        }
        require(parameter_indices == set(range(replayed["parameter_count"])), f"parameter registry:{polynomial_id}")
    for certificate_id, item in ti["certificates"].items():
        require(certificate_id == f"TI:{sha(item)}", f"T_i certificate self hash:{certificate_id}")
        require(item["zero_pullback_sha256"] == sha([]), f"T_i zero hash:{certificate_id}")
        require(item["strict_pullback_sha256"] in strict_polynomials, f"T_i strict reference:{certificate_id}")
        triple = set(map(str, item["triple"]))
        weights = item["boundary_incidence_multihomogeneity"]
        require(set(weights) == triple | {"all_unselected_boundary_incidence_weights"}, f"T_i weights labels:{certificate_id}")
        require(sorted(value for key, value in weights.items() if key != "all_unselected_boundary_incidence_weights") == ["g^2", "s^2*g", "s^2*g"], f"T_i weights:{certificate_id}")

    transports = load_streaming_registry(
        root / report["registries"]["exact_transports"]["path"],
        report["registries"]["exact_transports"],
        "exact_labelled_mixed_graph_transport", validate_transport, compact_transport,
    )
    restrictions = load_streaming_registry(
        root / report["registries"]["parent_restrictions"]["path"],
        report["registries"]["parent_restrictions"],
        "exact_parent_marginal_restriction", validate_restriction, compact_restriction,
    )

    anchors = {row["anchor_id"]: row for row in report["anchor_inventory"]["public_anchors"]}
    require(len(anchors) == report["anchor_inventory"]["anchors"] == 176, "anchor rows")
    require(sum(row["source_site_count"] * row["target_site_count"] for row in anchors.values()) == 29_964, "anchor Cartesian total")
    require(all(row["transport_id"] in transports for row in anchors.values()), "anchor transport references")

    one_path = root / "one_port_ledger.jsonl.gz"
    require(sha_file(one_path) == report["one_port"]["ledger_sha256"], "one ledger hash")
    one_ordered = OrderedReplay()
    one_counts = collections.Counter()
    one_source_sites = {}
    one_target_sites = {}
    one_equalities = {}
    one_equality_order = []
    expected_one = iter(
        (anchor["anchor_id"], source_index, target_index)
        for anchor in report["anchor_inventory"]["public_anchors"]
        for source_index in range(anchor["source_site_count"])
        for target_index in range(anchor["target_site_count"])
    )
    for number, row in iter_jsonl(one_path):
        one_ordered.add(row)
        require(row["stage"] == "A+p", f"one stage:{number}")
        anchor = anchors[row["parent_anchor_id"]]
        key = (row["parent_anchor_id"], row["source_site_index"], row["target_site_index"])
        require(key == next(expected_one, None), f"one Cartesian/order coverage:{number}:{key}")
        source_key = (row["parent_anchor_id"], row["source_site_index"])
        target_key = (row["parent_anchor_id"], row["target_site_index"])
        require(one_source_sites.setdefault(source_key, row["source_site_id"]) == row["source_site_id"], f"one source site drift:{source_key}")
        require(one_target_sites.setdefault(target_key, row["target_site_id"]) == row["target_site_id"], f"one target site drift:{target_key}")
        require(row["source_parent_restriction_id"] in restrictions, f"one source restriction:{number}")
        require(row["target_parent_restriction_id"] in restrictions, f"one target restriction:{number}")
        status = row["status"]
        one_counts[status] += 1
        if status in {"isomorphic", "triangle"}:
            require(row["transport_id"] in transports, f"one transport:{number}")
            require(row["parent_transport_id"] == anchor["transport_id"], f"one parent transport:{number}")
            validate_inherited_triangle(row, anchor, transports, f"one:{number}")
            parent_id = f"P1:{row['parent_anchor_id']}:{row['source_site_index']}:{row['target_site_index']}"
            require(parent_id not in one_equalities, f"duplicate one equality:{parent_id}")
            one_equalities[parent_id] = {
                "parent_anchor_id": row["parent_anchor_id"],
                "status": row["status"],
                "transport_id": row["transport_id"],
            }
            one_equality_order.append(parent_id)
        elif status == "displayed_quartet_mismatch":
            require(row["proof_id"] in topological, f"one quartet proof:{number}")
        elif status == "full_map_Ti_strict_sign":
            require(row["proof_id"] in ti["certificates"], f"one T_i proof:{number}")
        else:
            raise ReplayFailure(f"unexpected one status:{status}")
    one_ordered.require_equal(report["one_port"]["ordered_ledger"], "one ledger")
    require(dict(sorted(one_counts.items())) == report["one_port"]["counts"], "one counts")
    require(len(one_equalities) == report["one_port"]["equality_survivors"], "one equality count")
    require(next(expected_one, None) is None, "one Cartesian tail missing")

    parent_path = root / "two_port_parent_inventory.jsonl.gz"
    require(sha_file(parent_path) == report["two_port"]["parent_inventory_sha256"], "two-parent file hash")
    parent_ordered = OrderedReplay()
    parents = {}
    parent_order = []
    second_total = 0
    one_classes_by_base = collections.defaultdict(set)
    for number, row in iter_jsonl(parent_path):
        parent_ordered.add(row)
        parent_id = row["one_port_parent_id"]
        require(parent_id not in parents and parent_id in one_equalities, f"two parent identity:{number}")
        require(parent_id == one_equality_order[number], f"two parent ordered equality coverage:{number}")
        one_row = one_equalities[parent_id]
        require(row["base_anchor_id"] == one_row["parent_anchor_id"], f"two base parent:{number}")
        require(row["relation"] == one_row["status"], f"two parent relation:{number}")
        validate_profile(row["source_candidate_profile"], f"source:{parent_id}")
        validate_profile(row["target_candidate_profile"], f"target:{parent_id}")
        expected_pairs = row["source_candidate_profile"]["site_count"] * row["target_candidate_profile"]["site_count"]
        require(expected_pairs == row["raw_second_probe_pairs"], f"two parent pair count:{number}")
        second_total += expected_pairs
        parents[parent_id] = {
            "base_anchor_id": row["base_anchor_id"],
            "relation": row["relation"],
            "canonical_one_port_relation_class_id": row["canonical_one_port_relation_class_id"],
            "source_site_count": row["source_candidate_profile"]["site_count"],
            "target_site_count": row["target_candidate_profile"]["site_count"],
        }
        parent_order.append(parent_id)
        one_classes_by_base[row["base_anchor_id"]].add(row["canonical_one_port_relation_class_id"])
    parent_ordered.require_equal(report["two_port"]["ordered_parent_inventory"], "two-parent inventory")
    require(set(parents) == set(one_equalities), "all and only one equalities are two parents")
    require(second_total == report["two_port"]["raw_pairs"], "two raw total from parents")

    two_path = root / "two_port_ledger.jsonl.gz"
    require(sha_file(two_path) == report["two_port"]["ledger_sha256"], "two ledger hash")
    two_ordered = OrderedReplay()
    two_counts = collections.Counter()
    reverse_counts = collections.Counter()
    expected_two = iter(
        (parent_id, source_index, target_index)
        for parent_id in parent_order
        for source_index in range(parents[parent_id]["source_site_count"])
        for target_index in range(parents[parent_id]["target_site_count"])
    )
    for number, row in iter_jsonl(two_path):
        two_ordered.add(row)
        require(row["stage"] == "A+p+q", f"two stage:{number}")
        parent = parents[row["one_port_parent_id"]]
        require(row["base_anchor_id"] == parent["base_anchor_id"], f"two base:{number}")
        key = (
            row["one_port_parent_id"], row["second_source_site_index"],
            row["second_target_site_index"],
        )
        require(key == next(expected_two, None), f"two Cartesian/order coverage:{number}:{key}")
        require(row["source_parent_restriction_id"] in restrictions, f"two source restriction:{number}")
        require(row["target_parent_restriction_id"] in restrictions, f"two target restriction:{number}")
        status = row["status"]
        two_counts[status] += 1
        if status in {"isomorphic", "triangle"}:
            require(row["transport_id"] in transports, f"two transport:{number}")
            require(row["parent_transport_id"] == one_equalities[row["one_port_parent_id"]]["transport_id"], f"two parent transport:{number}")
            validate_inherited_triangle(
                row, anchors[row["base_anchor_id"]], transports, f"two:{number}"
            )
            reverse = row["reverse_order_certificate"]
            require(reverse["same_base_anchor_id"] == row["base_anchor_id"], f"reverse base:{number}")
            require(reverse["reverse_parent_transport_id"] in transports, f"reverse transport:{number}")
            require(reverse["reverse_parent_canonical_one_port_class_id"] in one_classes_by_base[row["base_anchor_id"]], f"reverse class:{number}")
            require(reverse["reverse_parent_relation"] in {"isomorphic", "triangle"}, f"reverse relation:{number}")
            reverse_counts[reverse["reverse_parent_relation"]] += 1
        elif status == "displayed_quartet_mismatch":
            require(row["proof_id"] in topological, f"two quartet proof:{number}")
            require("reverse_order_certificate" not in row, f"separator reverse payload:{number}")
        elif status == "full_map_Ti_strict_sign":
            require(row["proof_id"] in ti["certificates"], f"two T_i proof:{number}")
            require("reverse_order_certificate" not in row, f"separator reverse payload:{number}")
        else:
            raise ReplayFailure(f"unexpected two status:{status}")
    two_ordered.require_equal(report["two_port"]["ordered_ledger"], "two ledger")
    require(dict(sorted(two_counts.items())) == report["two_port"]["counts"], "two counts")
    require(dict(sorted(reverse_counts.items())) == report["two_port"]["reverse_order_parent_relation_counts"], "reverse counts")
    require(next(expected_two, None) is None, "two Cartesian tail missing")

    assembly = report["assembly_theorem"]
    require(assembly["unresolved"] == assembly["incoherent"] == 0, "assembly zero gates")
    require(assembly["two_port_order_gate"]["reversed_marginals_checked"] == sum(reverse_counts.values()), "assembly reverse census")
    require(assembly["one_global_triangle_gate"]["new_triangle_created_above_isomorphic_parent"] == 0, "assembly new triangle")
    verification = {
        "schema": "k2p-corrected-probe-independent-verification-v1",
        "status": "PASS",
        "source_certificate_sha256": sha_file(certificate_path),
        "source_payload_sha256": report["payload_sha256"],
        "anchors": len(anchors),
        "one_port_counts": dict(sorted(one_counts.items())),
        "two_port_parents": len(parents),
        "two_port_counts": dict(sorted(two_counts.items())),
        "reverse_order_counts": dict(sorted(reverse_counts.items())),
        "transport_records": len(transports),
        "restriction_records": len(restrictions),
        "quartet_certificates": len(topological),
        "T_i_relation_certificates": len(ti["certificates"]),
        "T_i_strict_polynomials_replayed": len(strict_polynomials),
        "unresolved": 0,
        "incoherent": 0,
        "operational": {"runtime_seconds": time.monotonic() - started},
    }
    logical = dict(verification)
    logical.pop("operational")
    verification["payload_sha256"] = sha(logical)
    args.output.write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "one": verification["one_port_counts"],
        "two": verification["two_port_counts"],
        "payload_sha256": verification["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ReplayFailure, KeyError, IndexError, OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"CORRECTED_PROBE_REPLAY_FAIL:{error}") from error
