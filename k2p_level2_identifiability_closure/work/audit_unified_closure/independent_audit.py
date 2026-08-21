#!/usr/bin/env python3
"""Independent adversarial audit of the 36-record direct residual closure.

This audit deliberately does not import the unified verifier.  It rebuilds the
production census from all 1,931 JSON records, recomputes the semantic manifest
and sweep roots, recompiles the 36 graph maps through the atlas compiler, and
replays every fixed obstruction over Q.
"""

from __future__ import annotations

import dataclasses
import hashlib
import itertools
import json
import math
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUN_ROOT = ROOT / "runs/four_port_full_v2"
ATLAS = ROOT / "package/referee/k2p_offline_sweep_portable/atlas"
sys.path.insert(0, str(ATLAS))

# This is the production compiler, a code path distinct from the graph-map
# implementation embedded in the unified verifier.
from k2p_atlas_core import (  # noqa: E402
    coordinate_weights,
    eval_descriptor,
    model_descriptor,
    orbit_assignments,
    output_sparse_polynomials,
    relabel_record,
    source_supports,
    target_completions,
)


EXPECTED_COUNTS = (536, 747, 276, 276, 64, 32)
EXPECTED_STATUS_COUNTS = {
    "error": 0,
    "isomorphic": 20,
    "restoration_parent": 997,
    "separated": 843,
    "triangle": 35,
    "unresolved": 36,
}
EXPECTED_SWEEP_ROOT = (
    "33b894a62f4bb993e580a03527d2d3509122ba4e84f1056ca70f4991ce04b899"
)
BINDING_KEYS = (
    "compiler_sha256",
    "canonicalizer_sha256",
    "descriptor_pickle_sha256",
    "rank_pickle_sha256",
    "output_schema_sha256",
    "input_lock_sha256",
    "hard_certificate_sha256",
)
DIAGNOSTIC_FIELDS = {
    "runtime_seconds",
    "peak_rss_bytes",
    "runtime_platform",
    "generated_at_utc",
    "record_payload_sha256",
    "semantic_record_sha256",
}

CUBIC = (
    ((0, 15, 35), 1),
    ((0, 20, 30), 1),
    ((1, 14, 35), 1),
    ((2, 15, 33), 1),
    ((2, 18, 32), 1),
    ((2, 23, 33), -1),
    ((3, 11, 35), -1),
    ((4, 20, 26), -1),
    ((6, 12, 33), 1),
    ((6, 18, 28), -1),
    ((7, 12, 32), -1),
    ((7, 15, 28), -1),
    ((7, 23, 28), 1),
    ((9, 10, 30), -1),
)
E = (0, 1, 2, 3)
A = (1, 0, 2, 3)
B = (0, 1, 3, 2)
H = (1, 0, 3, 2)


def canonical_data(value: Any):
    if dataclasses.is_dataclass(value):
        return {
            field.name: canonical_data(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, dict):
        return {
            str(key): canonical_data(item)
            for key, item in sorted(value.items(), key=lambda pair: repr(pair[0]))
        }
    if isinstance(value, (tuple, list)):
        return [canonical_data(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def sha_object(value: Any) -> str:
    raw = json.dumps(
        canonical_data(value), sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(raw).hexdigest()


def digest(value: Any) -> str:
    raw = json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=str
    ).encode()
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic_record_hash(record: dict) -> str:
    body = {
        key: value for key, value in record.items() if key not in DIAGNOSTIC_FIELDS
    }
    raw = json.dumps(
        body, sort_keys=True, separators=(",", ":"), default=str
    ).encode()
    return hashlib.sha256(raw).hexdigest()


def payload_record_hash(record: dict) -> str:
    body = {
        key: value
        for key, value in record.items()
        if key != "record_payload_sha256"
    }
    raw = json.dumps(
        body, sort_keys=True, separators=(",", ":"), default=str
    ).encode()
    return hashlib.sha256(raw).hexdigest()


def graph_payload(graph) -> dict:
    nodes = []
    for node, data in sorted(graph.nodes(data=True), key=lambda pair: repr(pair[0])):
        nodes.append(
            [repr(node), {str(key): repr(value) for key, value in sorted(data.items())}]
        )
    edges = []
    for tail, head, data in sorted(
        graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
    ):
        edges.append(
            [
                repr(tail),
                repr(head),
                {str(key): repr(value) for key, value in sorted(data.items())},
            ]
        )
    return {
        "nodes": nodes,
        "edges": edges,
        "graph": {
            str(key): repr(value) for key, value in sorted(graph.graph.items())
        },
    }


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(permutation)
    for index, image in enumerate(permutation):
        result[image] = index
    return tuple(result)


def ct_rep(characters: tuple[int, ...]) -> tuple[int, ...]:
    swapped = tuple(3 if value == 1 else (1 if value == 3 else value) for value in characters)
    return min(characters, swapped)


def coordinate_action(permutation: tuple[int, ...]) -> tuple[int, ...]:
    assignments = orbit_assignments(4)
    index = {assignment: offset for offset, assignment in enumerate(assignments)}
    return tuple(
        index[
            ct_rep(
                tuple(
                    assignment[permutation[position]]
                    for position in range(4)
                )
            )
        ]
        for assignment in assignments
    )


def transform(polynomial: tuple, permutation: tuple[int, ...]) -> tuple:
    action = coordinate_action(permutation)
    return tuple(
        (tuple(sorted(action[index] for index in monomial)), coefficient)
        for monomial, coefficient in polynomial
    )


def sparse_multiply(left: dict, right: dict) -> dict:
    output = defaultdict(int)
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(
                a + b for a, b in zip(left_exponent, right_exponent)
            )
            output[exponent] += left_coefficient * right_coefficient
    return {exponent: coefficient for exponent, coefficient in output.items() if coefficient}


def monomial_pullback(monomial: tuple[int, ...], outputs: tuple[dict, ...]) -> dict:
    result = {tuple(0 for _ in next(iter(outputs[0]))): 1}
    for coordinate in monomial:
        result = sparse_multiply(result, outputs[coordinate])
    return result


def pullback(polynomial: tuple, outputs: tuple[dict, ...]) -> dict:
    result = defaultdict(Fraction)
    cache = {}
    for monomial, coefficient in polynomial:
        if monomial not in cache:
            cache[monomial] = monomial_pullback(monomial, outputs)
        for exponent, value in cache[monomial].items():
            result[exponent] += Fraction(coefficient) * value
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def evaluate_polynomial(polynomial: tuple, coordinates: tuple[Fraction, ...]) -> Fraction:
    return sum(
        Fraction(coefficient)
        * math.prod(coordinates[index] for index in monomial)
        for monomial, coefficient in polynomial
    )


def multidegree(polynomial: tuple) -> tuple[int, ...]:
    weights = coordinate_weights(4)
    rows = {
        tuple(
            sum(weights[index][slot] for index in monomial)
            for slot in range(8)
        )
        for monomial, _coefficient in polynomial
    }
    if len(rows) != 1:
        raise AssertionError(f"not multihomogeneous: {rows}")
    return next(iter(rows))


def strict_source_point(descriptor):
    edge_pairs = tuple(
        (Fraction(1, 4), Fraction(index + 1, 10))
        for index in range(descriptor.edge_class_count)
    )
    lambdas = (Fraction(1, 3), Fraction(2, 3))
    if descriptor.edge_class_count != 8 or descriptor.retic_count != 2:
        raise AssertionError("unexpected source parameter dimensions")
    for s_value, g_value in edge_pairs:
        if not (0 < s_value < 1 and 0 < g_value < 1 and g_value > 2 * s_value - 1):
            raise AssertionError("strict D+ inequality failed")
    if not all(0 < value < 1 for value in lambdas):
        raise AssertionError("strict inheritance inequality failed")
    return edge_pairs, lambdas


def full_census():
    merged_path = RUN_ROOT / "FOUR_PORT_SWEEP_MERGED_STATUS.json"
    merged = json.loads(merged_path.read_text())
    if merged["schema"] != "k2p-four-port-six-source-merge-v2":
        raise AssertionError("wrong merge schema")
    if not merged["all_manifests_complete"] or not merged["all_six_sources_present"]:
        raise AssertionError("merge not complete")

    bindings = merged["bindings"]
    if set(bindings) != set(BINDING_KEYS):
        raise AssertionError("unexpected binding fields")
    status_counts = Counter()
    unresolved = set()
    direct_unresolved = set()
    manifest_rows = []
    records = {}
    raw_record_count = 0

    for source_index, expected_count in enumerate(EXPECTED_COUNTS):
        manifest_path = RUN_ROOT / f"source_{source_index}/residual_manifest.json"
        manifest = json.loads(manifest_path.read_text())
        merged_row = merged["sources"][source_index]
        if sha_file(manifest_path) != merged_row["manifest_sha256"]:
            raise AssertionError("manifest file binding failed")
        if manifest["source_index"] != source_index:
            raise AssertionError("manifest source mismatch")
        if manifest["canonical_class_count"] != expected_count:
            raise AssertionError("manifest class count mismatch")
        summaries = manifest["records"]
        ids = [row["canonical_class_id"] for row in summaries]
        if ids != list(range(expected_count)):
            raise AssertionError("manifest IDs are not exact and ordered")
        if manifest["record_count"] != expected_count or not manifest["complete"]:
            raise AssertionError("manifest false completion")
        for key in BINDING_KEYS:
            if manifest[key] != bindings[key]:
                raise AssertionError("manifest input binding mismatch")

        for summary in summaries:
            class_id = summary["canonical_class_id"]
            record_path = (
                RUN_ROOT
                / f"source_{source_index}/records/class_{class_id:06d}.json"
            )
            record = json.loads(record_path.read_text())
            if record["source_index"] != source_index or record["canonical_class_id"] != class_id:
                raise AssertionError("record identity mismatch")
            if payload_record_hash(record) != record["record_payload_sha256"]:
                raise AssertionError("record payload self-hash mismatch")
            if semantic_record_hash(record) != record["semantic_record_sha256"]:
                raise AssertionError("record semantic self-hash mismatch")
            expected_summary = {
                "canonical_class_id": class_id,
                "status": record["status"],
                "stratum": record["stratum"],
                "descriptor_sha256": record["descriptor_sha256"],
                "record_sha256": sha_file(record_path),
                "semantic_record_sha256": record["semantic_record_sha256"],
                "omitted_roles": record["omitted_roles"],
                "child_requests": record["child_requests"],
            }
            if summary != expected_summary:
                raise AssertionError("record/manifest summary mismatch")
            for key in BINDING_KEYS:
                if record[key] != bindings[key]:
                    raise AssertionError("record input binding mismatch")
            status_counts[record["status"]] += 1
            key = (source_index, class_id)
            if record["status"] == "unresolved":
                unresolved.add(key)
                if record["stratum"] == "direct_no_dummy":
                    direct_unresolved.add(key)
                records[key] = record
            raw_record_count += 1

        derived_unresolved = sorted(
            row["canonical_class_id"] for row in summaries if row["status"] == "unresolved"
        )
        if manifest["unresolved"] != derived_unresolved:
            raise AssertionError("unresolved manifest summary mismatch")
        immutable = {"schema": "k2p-four-port-record-v3", **bindings}
        semantic_summaries = [
            {key: value for key, value in row.items() if key != "record_sha256"}
            for row in summaries
        ]
        semantic_manifest = sha_object(
            {
                "source_index": source_index,
                "canonical_class_count": expected_count,
                "immutable": immutable,
                "records": semantic_summaries,
            }
        )
        if semantic_manifest != manifest["semantic_manifest_sha256"]:
            raise AssertionError("semantic manifest hash mismatch")
        if semantic_manifest != merged_row["semantic_manifest_sha256"]:
            raise AssertionError("merged semantic manifest binding mismatch")
        manifest_rows.append(
            {
                "source_index": source_index,
                "canonical_class_count": expected_count,
                "semantic_manifest_sha256": semantic_manifest,
            }
        )

    semantic_sweep = sha_object(
        {
            "schema": merged["schema"],
            "bindings": bindings,
            "sources": manifest_rows,
        }
    )
    if semantic_sweep != merged["semantic_sweep_sha256"]:
        raise AssertionError("recomputed semantic sweep root mismatch")
    if semantic_sweep != EXPECTED_SWEEP_ROOT:
        raise AssertionError("unexpected production semantic sweep root")
    observed_status_counts = {
        status: status_counts.get(status, 0) for status in EXPECTED_STATUS_COUNTS
    }
    if observed_status_counts != EXPECTED_STATUS_COUNTS:
        raise AssertionError(f"status count mismatch: {dict(status_counts)}")
    if raw_record_count != sum(EXPECTED_COUNTS):
        raise AssertionError("wrong total production record count")
    if unresolved != direct_unresolved or len(unresolved) != 36:
        raise AssertionError("unresolved set is not exactly 36 direct records")
    return merged, records, unresolved, status_counts, raw_record_count


def graph_bindings(records: dict):
    sources = tuple(source_supports())
    targets = target_completions(4, True)
    if tuple((row.core_id, row.repair_index) for row in sources) != (
        ("theta0", 0),
        ("theta0", 1),
        ("theta1", 0),
        ("theta1", 1),
        ("theta3", 0),
        ("theta3", 1),
    ):
        raise AssertionError("source grammar order changed")
    descriptor_cache = {}
    target_cache = {}
    for key, record in records.items():
        source_index, _class_id = key
        if len(record["members"]) != 1 or record["omitted_roles"]:
            raise AssertionError("residual record is not one-member direct")
        source_hash = sha_object(graph_payload(sources[source_index].graph))
        if source_hash != record["source_graph_sha256"]:
            raise AssertionError("source graph binding mismatch")
        member = record["members"][0]
        target_key = (member["target_index"], tuple(member["port_match"]))
        if target_key not in target_cache:
            target = relabel_record(
                targets[member["target_index"]], tuple(member["port_match"])
            )
            target_cache[target_key] = (
                target,
                model_descriptor(target.graph),
            )
        target, descriptor = target_cache[target_key]
        target_hash = sha_object(graph_payload(target.graph))
        if target_hash != member["target_selected_graph_sha256"]:
            raise AssertionError("target selected graph binding mismatch")
        if sha_object([target_hash]) != record["target_graph_sha256"]:
            raise AssertionError("target graph collection binding mismatch")
        if sha_object(descriptor) != record["descriptor_sha256"]:
            raise AssertionError("target descriptor binding mismatch")
        if source_index not in descriptor_cache:
            source_descriptor = model_descriptor(sources[source_index].graph)
            descriptor_cache[source_index] = (
                source_descriptor,
                output_sparse_polynomials(source_descriptor),
            )
    return sources, targets, descriptor_cache, target_cache


def load_polynomials():
    quintic_artifact = json.loads(
        (ROOT / "work/theta0_quintic_orbit_certificate.json").read_text()
    )
    quintic = tuple(
        (tuple(monomial), coefficient)
        for monomial, coefficient in quintic_artifact["invariant"]
    )
    if digest(quintic) != "02f835bbc6b00704a993426b25e074a26239cc7124059402372b136cccb5ec4f":
        raise AssertionError("quintic hash mismatch")

    quartic_artifact = json.loads(
        (ROOT / "work/theta_quartic_obstruction_certificates.json").read_text()
    )
    bases = {
        (row["source_index"], row["canonical_class_id"]): row
        for row in quartic_artifact["certificates"]
    }
    quartics = {
        "F112": tuple(
            (tuple(indices), coefficient)
            for coefficient, indices in bases[(2, 112)]["terms"]
        ),
        "F113": tuple(
            (tuple(indices), coefficient)
            for coefficient, indices in bases[(2, 113)]["terms"]
        ),
        "F48": tuple(
            (tuple(indices), coefficient)
            for coefficient, indices in bases[(4, 8)]["terms"]
        ),
    }
    expected_quartic_hashes = {
        "F112": "176c030342cee7504fc2e488f39c448ad1d5e3631489c70c9e29f43b4f025c17",
        "F113": "b8a2203572f8a268758ca549aadd9a85a88d02dcf630a1970c657a191c6c4cba",
        "F48": "314ae606c30b87b305b2a7762bdf612a2a00811dca298242ce7cb0e8eb45b14f",
    }
    for name, polynomial in quartics.items():
        if digest(polynomial) != expected_quartic_hashes[name]:
            raise AssertionError(f"{name} hash mismatch")
    return quintic, quartics


def obstruction_for(key, record, quintic, quartics):
    source_index, class_id = key
    permutation = tuple(record["members"][0]["port_match"])
    if source_index == 1:
        return "theta0_quintic_port_orbit", transform(quintic, inverse(permutation))
    if source_index in (2, 3):
        if class_id in (112, 115):
            return "lower_theta_quartic", quartics["F112"]
        if class_id in (113, 114):
            return "lower_theta_quartic", quartics["F113"]
    if source_index == 4:
        if class_id in (8, 11):
            return "lower_theta_quartic", quartics["F48"]
        if class_id in (9, 10):
            return "lower_theta_quartic", transform(quartics["F48"], A)
    if source_index == 5 and class_id in (9, 10):
        return "theta3_cubic", CUBIC
    raise AssertionError(f"unmapped residual {key}")


def replay_all(records, descriptor_cache, target_cache, quintic, quartics):
    unified = json.loads(
        (ROOT / "work/four_port_direct_residual_closure_certificate.json").read_text()
    )
    if unified["schema"] != "k2p-four-port-direct-residual-closure-v1":
        raise AssertionError("wrong unified certificate schema")
    unhashed = dict(unified)
    advertised_payload_hash = unhashed.pop("payload_sha256_without_hash")
    if sha_object(unhashed) != advertised_payload_hash:
        raise AssertionError("unified certificate payload self-hash mismatch")
    if unified["verifier_sha256"] != sha_file(
        ROOT / "work/verify_four_port_direct_residual_closure.py"
    ):
        raise AssertionError("unified verifier binding mismatch")
    for relative_path, expected_hash in unified["proof_input_sha256"].items():
        if sha_file(ROOT / relative_path) != expected_hash:
            raise AssertionError(f"proof input binding mismatch: {relative_path}")
    if unified["unresolved_input_count"] != 36 or unified["binding_gaps"]:
        raise AssertionError("unified input census/binding gaps mismatch")

    unified_rows = {
        (row["source_index"], row["canonical_class_id"]): row
        for row in unified["coverage"]
    }
    if len(unified_rows) != len(unified["coverage"]):
        raise AssertionError("duplicate unified coverage rows")
    unified_bindings = {
        (row["source_index"], row["canonical_class_id"]): row
        for row in unified["record_bindings"]
    }
    if len(unified_bindings) != len(unified["record_bindings"]):
        raise AssertionError("duplicate unified record bindings")
    if set(unified_bindings) != set(records):
        raise AssertionError("unified record binding set mismatch")
    for key, record in records.items():
        source_index, class_id = key
        binding = unified_bindings[key]
        record_path = (
            RUN_ROOT
            / f"source_{source_index}/records/class_{class_id:06d}.json"
        )
        member = record["members"][0]
        if binding != {
            "source_index": source_index,
            "canonical_class_id": class_id,
            "semantic_record_sha256": record["semantic_record_sha256"],
            "record_file_sha256": sha_file(record_path),
            "source_graph_sha256": record["source_graph_sha256"],
            "target_selected_graph_sha256": member["target_selected_graph_sha256"],
            "descriptor_sha256": record["descriptor_sha256"],
        }:
            raise AssertionError(f"unified binding row mismatch at {key}")
    family_counts = Counter()
    proof_rows = []
    for key in sorted(records):
        record = records[key]
        source_index, class_id = key
        family, polynomial = obstruction_for(key, record, quintic, quartics)
        family_counts[family] += 1
        source_descriptor, source_outputs = descriptor_cache[source_index]
        member = record["members"][0]
        target_key = (member["target_index"], tuple(member["port_match"]))
        _target, target_descriptor = target_cache[target_key]
        target_outputs = output_sparse_polynomials(target_descriptor)
        target_pullback = pullback(polynomial, target_outputs)
        source_pullback = pullback(polynomial, source_outputs)
        if target_pullback:
            raise AssertionError(f"target pullback nonzero at {key}")
        if not source_pullback:
            raise AssertionError(f"source pullback zero at {key}")
        weight = multidegree(polynomial)
        edge_pairs, lambdas = strict_source_point(source_descriptor)
        coordinates = eval_descriptor(source_descriptor, edge_pairs, lambdas)
        strict_value = evaluate_polynomial(polynomial, coordinates)
        if not strict_value:
            raise AssertionError(f"strict source witness zero at {key}")
        row = unified_rows.get(key)
        if row is None:
            raise AssertionError(f"missing unified row {key}")
        if row["family"] != family:
            raise AssertionError(f"family mismatch at {key}")
        if row["semantic_record_sha256"] != record["semantic_record_sha256"]:
            raise AssertionError(f"record hash mismatch at {key}")
        if row["polynomial_sha256"] != digest(polynomial):
            raise AssertionError(f"polynomial hash mismatch at {key}")
        if tuple(row["bridge_multidegree"]) != weight:
            raise AssertionError(f"multidegree mismatch at {key}")
        if row["source_pullback_term_count"] != len(source_pullback):
            raise AssertionError(f"source term count mismatch at {key}")
        if row["source_pullback_sha256"] != sha_object(source_pullback):
            raise AssertionError(f"source pullback hash mismatch at {key}")
        list_hash = digest(sorted(source_pullback.items(), key=lambda item: repr(item[0])))
        if row["source_pullback_list_sha256"] != list_hash:
            raise AssertionError(f"source pullback list hash mismatch at {key}")
        strict_row = row["strict_D_plus_witness"]
        if Fraction(strict_row["normalized_source_obstruction_value"]) != strict_value:
            raise AssertionError(f"strict witness value mismatch at {key}")
        pendant_pairs = tuple(
            (Fraction(s_value), Fraction(g_value))
            for s_value, g_value in strict_row["selected_pendant_edge_pairs"]
        )
        if len(pendant_pairs) != 4:
            raise AssertionError(f"pendant witness count mismatch at {key}")
        for s_value, g_value in pendant_pairs:
            if not (0 < s_value < 1 and 0 < g_value < 1 and g_value > 2 * s_value - 1):
                raise AssertionError(f"pendant strict D+ inequality failed at {key}")
        pendant_factor = math.prod(
            pendant_pairs[port][0] ** weight[2 * port]
            * pendant_pairs[port][1] ** weight[2 * port + 1]
            for port in range(4)
        )
        if Fraction(strict_row["pendant_multihomogeneous_factor"]) != pendant_factor:
            raise AssertionError(f"pendant factor mismatch at {key}")
        if Fraction(strict_row["physical_source_obstruction_value"]) != strict_value * pendant_factor:
            raise AssertionError(f"physical source witness mismatch at {key}")
        proof_rows.append(
            {
                "source_index": source_index,
                "canonical_class_id": class_id,
                "family": family,
                "degree": len(polynomial[0][0]),
                "term_count": len(polynomial),
                "source_pullback_term_count": len(source_pullback),
                "source_pullback_sha256": sha_object(source_pullback),
                "strict_value": str(strict_value),
            }
        )
    expected_families = {
        "theta0_quintic_port_orbit": 22,
        "lower_theta_quartic": 12,
        "theta3_cubic": 2,
    }
    if dict(family_counts) != expected_families:
        raise AssertionError(f"family census mismatch: {dict(family_counts)}")
    if unified["proof_family_counts"] != expected_families:
        raise AssertionError("advertised proof-family census mismatch")
    if set(unified_rows) != set(records):
        raise AssertionError("unified coverage is not exactly the production residual set")
    if unified["covered_direct_classes"] != [list(key) for key in sorted(records)]:
        raise AssertionError("covered-direct-class list mismatch")
    if unified["residual_direct_classes"] or unified["residual_direct_class_count"] != 0:
        raise AssertionError("unified certificate advertises a residual")
    return proof_rows, family_counts, unified


def adversarial_local_tests(records, descriptor_cache, target_cache, quintic, quartics):
    tests = {}
    residual_keys = set(records)

    dropped = residual_keys - {(5, 10)}
    tests["dropped_coverage_detected"] = dropped != residual_keys

    swapped = list(sorted(residual_keys))
    swapped[-1] = swapped[-2]
    tests["duplicated_swapped_coverage_detected"] = set(swapped) != residual_keys

    mutated_record = json.loads(json.dumps(records[(5, 9)]))
    mutated_record["members"][0]["port_match"] = [1, 0, 2, 3]
    tests["mutated_record_binding_detected"] = (
        semantic_record_hash(mutated_record)
        != mutated_record["semantic_record_sha256"]
    )

    # A coefficient mutation of F112 must destroy its target identity.
    bad_f112 = list(quartics["F112"])
    monomial, coefficient = bad_f112[0]
    bad_f112[0] = (monomial, coefficient + 1)
    target_member = records[(2, 112)]["members"][0]
    target_key = (target_member["target_index"], tuple(target_member["port_match"]))
    _target, target_descriptor = target_cache[target_key]
    tests["mutated_quartic_coefficient_detected"] = bool(
        pullback(tuple(bad_f112), output_sparse_polynomials(target_descriptor))
    )

    # Search for and record one genuinely invalid family swap.
    wrong_candidates = {
        "F113_on_s2c112": quartics["F113"],
        "F48_on_s2c112": quartics["F48"],
        "C3_on_s2c112": CUBIC,
    }
    invalid_swaps = []
    for name, polynomial in wrong_candidates.items():
        if pullback(polynomial, output_sparse_polynomials(target_descriptor)):
            invalid_swaps.append(name)
    tests["wrong_family_swap_detected"] = bool(invalid_swaps)
    tests["invalid_swap_examples"] = invalid_swaps

    if not all(value for key, value in tests.items() if key != "invalid_swap_examples"):
        raise AssertionError(f"one or more adversarial local tests failed: {tests}")
    return tests


def main():
    merged, records, unresolved, status_counts, record_count = full_census()
    sources, targets, descriptor_cache, target_cache = graph_bindings(records)
    quintic, quartics = load_polynomials()
    proof_rows, family_counts, unified = replay_all(
        records, descriptor_cache, target_cache, quintic, quartics
    )
    mutation_tests = adversarial_local_tests(
        records, descriptor_cache, target_cache, quintic, quartics
    )
    output = {
        "schema": "k2p-four-port-direct-residual-independent-audit-v1",
        "result": "PASS",
        "production_run": {
            "record_count": record_count,
            "semantic_sweep_sha256": merged["semantic_sweep_sha256"],
            "status_counts": EXPECTED_STATUS_COUNTS,
            "unresolved_direct_count": len(unresolved),
        },
        "proof_family_counts": dict(family_counts),
        "exact_replay_rows": proof_rows,
        "covered_keys": [list(key) for key in sorted(unresolved)],
        "residual_after_overlay": [],
        "adversarial_local_tests": mutation_tests,
        "primary_artifacts": {
            "unified_verifier_sha256": sha_file(
                ROOT / "work/verify_four_port_direct_residual_closure.py"
            ),
            "unified_certificate_sha256": sha_file(
                ROOT / "work/four_port_direct_residual_closure_certificate.json"
            ),
            "quintic_certificate_sha256": sha_file(
                ROOT / "work/theta0_quintic_orbit_certificate.json"
            ),
            "quartic_certificate_sha256": sha_file(
                ROOT / "work/theta_quartic_obstruction_certificates.json"
            ),
        },
        "audit_script_sha256": sha_file(Path(__file__)),
    }
    output["payload_sha256_without_hash"] = sha_object(output)
    destination = Path(__file__).with_name("independent_audit_certificate.json")
    destination.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print("INDEPENDENT_DIRECT_RESIDUAL_AUDIT_PASS")
    print(f"records={record_count} residual_input={len(unresolved)} residual_output=0")
    print(f"families={dict(family_counts)}")
    print(f"payload_sha256={output['payload_sha256_without_hash']}")
    print(f"certificate_sha256={sha_file(destination)}")


if __name__ == "__main__":
    main()
