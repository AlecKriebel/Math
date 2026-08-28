#!/usr/bin/env python3
"""Build the promotion-grade corrected restoration forest.

The released first-child enumeration and its ordering remain immutable.  The
646 historical rooted ``strict_tree_sunlet_sign`` leaves are treated only as
the affected-row selector and are reclassified from the original full K2P
maps.  No rooted triple type is used as a proof.
"""

from __future__ import annotations

import collections
import fractions
import hashlib
import importlib.util
import itertools
import json
import math
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import (  # noqa: E402
    StrictJSONError,
    decode_json_document,
    iter_canonical_gzip_jsonl,
)

RESTORATION_PATH = PROJECT / "work/restoration_forest/enumerate_five_port.py"
HISTORICAL_CERTIFICATE = PROJECT / "work/restoration_forest/five_port_certificate.json"
RAW_LEDGER = PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
OUTPUT = HERE / "corrected_restoration_forest.json"
CROSSWALK_OUTPUT = HERE / "corrected_restoration_historical_crosswalk.json"


class Failure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


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


def exact_labelled_mixed_payload(atlas, graph):
    """Serialize the labelled semi-directed graph with its actual node names.

    This is deliberately stronger than an isomorphism class: restoration is a
    concrete parent--child transport, so deleting the new arm must recover the
    exact recorded parent presentation, including its labelled vertices and
    retained arrowheads.
    """
    mixed = atlas.sd0_mixed(graph)
    nodes = [
        [repr(node), data.get("label"), data.get("role")]
        for node, data in sorted(mixed.nodes(data=True), key=lambda row: repr(row[0]))
    ]
    edges = []
    for left, right, data in mixed.edges(data=True):
        if repr(right) < repr(left):
            left, right = right, left
        edges.append([
            repr(left),
            repr(right),
            sorted(repr(node) for node in data.get("heads", frozenset())),
        ])
    edges.sort()
    return {"nodes": nodes, "edges": edges}


def first_parent_transport(atlas, kind, parent, child, identity):
    restricted = atlas.restrict_rooted(child, set(range(4)))
    parent_payload = exact_labelled_mixed_payload(atlas, parent)
    restricted_payload = exact_labelled_mixed_payload(atlas, restricted)
    require(parent_payload == restricted_payload, f"exact first parent transport:{kind}:{identity}")
    record = {
        "kind": kind,
        "deleted_label": 4,
        "kept_labels": [0, 1, 2, 3],
        "parent_mixed_graph_sha256": sha(parent_payload),
        "restricted_child_mixed_graph_sha256": sha(restricted_payload),
        **identity,
    }
    return sha(record), record


def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot import:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sparse_payload(polynomial):
    return [[list(exponent), str(coefficient)] for exponent, coefficient in sorted(polynomial.items())]


def sparse_hash(polynomial):
    return sha(sparse_payload(polynomial))


def evaluate_sparse(polynomial, point):
    total = fractions.Fraction(0)
    for exponent, coefficient in polynomial.items():
        term = fractions.Fraction(coefficient)
        for value, power in zip(point, exponent):
            if power:
                term *= value ** power
        total += term
    return total


def strict_physical_witness(atlas, descriptor, polynomial):
    for salt in range(32):
        edge_pairs, lambdas = atlas.default_exact_point(descriptor, salt)
        point = tuple(value for pair in edge_pairs for value in pair) + tuple(lambdas)
        value = evaluate_sparse(polynomial, point)
        if value:
            return {
                "salt": salt,
                "edge_pairs": [[str(s), str(g)] for s, g in edge_pairs],
                "lambdas": [str(value) for value in lambdas],
                "value": str(value),
            }
    raise Failure("nonzero polynomial lacks a physical exact witness")


def t_pullback(atlas, descriptor, outputs, triple, orientation):
    assignments = atlas.orbit_assignments(descriptor.k)
    index = {assignment: number for number, assignment in enumerate(assignments)}
    others = sorted(set(triple) - {orientation})
    order = (others[0], others[1], orientation)

    def coordinate(characters):
        assignment = [0] * descriptor.k
        for label, character in zip(order, characters):
            assignment[label] = character
        coordinate_index = index[atlas.ct_orbit_rep(tuple(assignment))]
        return coordinate_index, outputs[coordinate_index]

    v_index, v = coordinate((1, 3, 2))
    xs_index, xs = coordinate((1, 1, 0))
    xg_index, xg = coordinate((2, 2, 0))
    yg_index, yg = coordinate((2, 0, 2))
    zg_index, zg = coordinate((0, 2, 2))
    polynomial = atlas.sparse_lincomb(
        [atlas.sparse_mul_many([v, v, xg]), atlas.sparse_mul_many([xs, xs, yg, zg])],
        [1, -1],
    )

    # Observable multihomogeneity is exactly the two-sector bridge-torus
    # condition.  Weight slots (2a,2a+1) are the s/g sectors at leaf a.
    coordinate_weights = atlas.coordinate_weights(descriptor.k)
    left_weight = tuple(
        2 * coordinate_weights[v_index][slot] + coordinate_weights[xg_index][slot]
        for slot in range(2 * descriptor.k)
    )
    right_weight = tuple(
        2 * coordinate_weights[xs_index][slot]
        + coordinate_weights[yg_index][slot]
        + coordinate_weights[zg_index][slot]
        for slot in range(2 * descriptor.k)
    )
    expected = [0] * (2 * descriptor.k)
    for label in others:
        expected[2 * label] = 2
        expected[2 * label + 1] = 1
    expected[2 * orientation + 1] = 2
    require(left_weight == right_weight == tuple(expected), (
        "T_i boundary-incidence multidegree", descriptor.k, triple, orientation,
        left_weight, right_weight, expected,
    ))
    return polynomial, left_weight


def negative_bernstein_certificate(polynomial):
    require(polynomial, "empty signed pullback")
    parameter_count = len(next(iter(polynomial)))
    monomial = tuple(
        min(exponent[index] for exponent in polynomial)
        for index in range(parameter_count)
    )
    active = tuple(
        index
        for index in range(parameter_count)
        if len({exponent[index] - monomial[index] for exponent in polynomial}) > 1
    )
    residual = {
        tuple(exponent[index] - monomial[index] for index in active): fractions.Fraction(coefficient)
        for exponent, coefficient in polynomial.items()
    }
    degree = tuple(max(exponent[index] for exponent in residual) for index in range(len(active)))
    shape = tuple(value + 1 for value in degree)
    count = math.prod(shape)
    require(count <= 100_000, f"Bernstein tensor bound:{count}")
    strides = tuple(math.prod(shape[index + 1 :]) for index in range(len(shape)))
    values = [fractions.Fraction(0)] * count
    for exponent, coefficient in residual.items():
        values[sum(value * stride for value, stride in zip(exponent, strides))] = coefficient
    for axis, axis_degree in enumerate(degree):
        stride = strides[axis]
        outer_count = math.prod(shape[:axis])
        block_size = (axis_degree + 1) * stride
        denominators = tuple(math.comb(axis_degree, alpha) for alpha in range(axis_degree + 1))
        converted = [fractions.Fraction(0)] * count
        for outer in range(outer_count):
            base = outer * block_size
            for inner in range(stride):
                power = tuple(
                    values[base + alpha * stride + inner]
                    for alpha in range(axis_degree + 1)
                )
                for beta in range(axis_degree + 1):
                    converted[base + beta * stride + inner] = sum(
                        power[alpha]
                        * fractions.Fraction(math.comb(beta, alpha), denominators[alpha])
                        for alpha in range(beta + 1)
                    )
        values = converted
    signs = collections.Counter(-1 if value < 0 else 1 if value > 0 else 0 for value in values)
    require(signs[1] == 0 and signs[-1] > 0, f"not Bernstein negative:{signs}")
    result = {
        "method": "exact_tensor_Bernstein_after_positive_monomial",
        "positive_monomial_exponent": list(monomial),
        "active_parameter_indices": list(active),
        "Bernstein_multidegree": list(degree),
        "Bernstein_coefficient_count": count,
        "negative_coefficients": signs[-1],
        "zero_coefficients": signs[0],
        "positive_coefficients": signs[1],
        "minimum_coefficient": str(min(values)),
        "maximum_coefficient": str(max(values)),
        "domain": "the full open positive parameter cube (0,1)^m, which contains the principal D_plus parameter domain as a subset",
        "conclusion": "strictly_negative",
    }
    result["certificate_sha256"] = sha(result)
    return result


def sign_definite(polynomial):
    try:
        return "negative", polynomial, negative_bernstein_certificate(polynomial)
    except Failure:
        negated = {exponent: -coefficient for exponent, coefficient in polynomial.items()}
        try:
            return "positive", negated, negative_bernstein_certificate(negated)
        except Failure:
            return None


def split_payload(value):
    result = []
    for item in sorted(value, key=repr):
        if item == ("star",):
            result.append(["star"])
        else:
            result.append([list(item[0]), list(item[1])])
    return result


def quartet_separator(atlas, source, target, labels):
    for quartet in itertools.combinations(labels, 4):
        source_splits = atlas.quartet_splits(source, quartet)
        target_splits = atlas.quartet_splits(target, quartet)
        if source_splits != target_splits:
            return {
                "quartet": list(quartet),
                "source_splits": split_payload(source_splits),
                "target_splits": split_payload(target_splits),
            }
    return None


def verify_algebra_multihomogeneity(atlas, proof, k):
    weights = atlas.coordinate_weights(k)
    if proof["proof"] == "exact_multihomogeneous_quadratic":
        degrees = {
            tuple(weights[left][slot] + weights[right][slot] for slot in range(2 * k))
            for left, right in proof["coordinate_pairs"]
        }
        require(len(degrees) == 1, "quadratic multihomogeneity")
        require(list(next(iter(degrees))) == proof["weight"], "quadratic weight binding")
    elif proof["proof"] == "inherited_exact_F_2_112_quartic":
        degrees = {
            tuple(
                sum(weights[index][slot] for index in monomial)
                for slot in range(2 * k)
            )
            for monomial, _ in proof["lifted_coordinate_monomials"]
        }
        require(len(degrees) == 1, "quartic boundary-incidence multihomogeneity")
        require(list(next(iter(degrees))) == proof["weight"], "quartic weight binding")
    else:
        raise Failure(f"unknown algebra proof:{proof['proof']}")


def graph_descriptor(atlas, graph):
    descriptor = atlas.model_descriptor_fast2(graph)
    return descriptor, atlas.output_sparse_polynomials(descriptor)


def find_strict_t_separator(
    atlas,
    source_descriptor,
    source_outputs,
    target_descriptor,
    target_outputs,
    labels,
    sign_cache,
    sign_certificates,
):
    asymmetric = []
    for triple in itertools.combinations(labels, 3):
        for orientation in triple:
            source_polynomial, source_weight = t_pullback(
                atlas, source_descriptor, source_outputs, triple, orientation
            )
            target_polynomial, target_weight = t_pullback(
                atlas, target_descriptor, target_outputs, triple, orientation
            )
            require(source_weight == target_weight, "source/target T weight transport")
            if not source_polynomial and target_polynomial:
                asymmetric.append((len(target_polynomial), triple, orientation, "target", target_polynomial, source_polynomial, target_polynomial, source_weight))
            elif not target_polynomial and source_polynomial:
                asymmetric.append((len(source_polynomial), triple, orientation, "source", source_polynomial, source_polynomial, target_polynomial, source_weight))
    for candidate in sorted(asymmetric, key=lambda row: (row[0], row[1], row[2], row[3])):
        term_count, triple, orientation, signed_side, signed_polynomial, source_polynomial, target_polynomial, weight = candidate
        signed_sha256 = sparse_hash(signed_polynomial)
        if signed_sha256 not in sign_cache:
            sign_cache[signed_sha256] = sign_definite(signed_polynomial)
        definite = sign_cache[signed_sha256]
        if definite is None:
            continue
        strict_sign, normalized_negative, bernstein = definite
        normalized_sha256 = sparse_hash(normalized_negative)
        certificate = {
            "pullback_sha256": signed_sha256,
            "pullback_term_count": term_count,
            "strict_sign": strict_sign,
            "normalized_negative_pullback_sha256": normalized_sha256,
            "observable_boundary_multidegree": list(weight),
            "bernstein": bernstein,
        }
        previous = sign_certificates.setdefault(signed_sha256, certificate)
        require(previous == certificate, "T sign certificate collision")
        return {
            "triple": list(triple),
            "orientation": orientation,
            "signed_side": signed_side,
            "zero_side": "source" if signed_side == "target" else "target",
            "strict_sign": strict_sign,
            "source_pullback_sha256": sparse_hash(source_polynomial),
            "target_pullback_sha256": sparse_hash(target_polynomial),
            "signed_pullback_sha256": signed_sha256,
            "normalized_negative_pullback_sha256": normalized_sha256,
            "observable_boundary_multidegree": list(weight),
        }
    return None


def main():
    if not __debug__:
        raise Failure("CORRECTED_RESTORATION_OPTIMIZED_MODE_FORBIDDEN")
    restoration = import_path("corrected_restoration_generator", RESTORATION_PATH)
    atlas = restoration.load_atlas()
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    roots, manifest_hashes, canonical_parent_count = restoration.reconstruct_roots(
        atlas, sources, targets
    )
    require(canonical_parent_count == 997, "canonical parent count")
    obligation_keys = {
        (root["source_index"], root["canonical_class_id"])
        for root in roots
    }
    omitted_terminal_rows = []
    for raw in iter_canonical_gzip_jsonl(RAW_LEDGER, label=RAW_LEDGER.name):
        if (
            raw.get("category") == "retained_terminal"
            and raw.get("status") in {"isomorphic", "triangle"}
            and targets[raw["target_index"]].dummy_labels
        ):
            require(
                (raw["source_index"], raw["class_id"]) not in obligation_keys,
                f"omitted terminal leaked into obligation forest:{raw['raw_id']}",
            )
            omitted_terminal_rows.append({
                "raw_id": raw["raw_id"],
                "source_index": raw["source_index"],
                "canonical_class_id": raw["class_id"],
                "target_index": raw["target_index"],
                "permutation_index": raw["permutation_index"],
                "relation": raw["status"],
            })
    omitted_terminal_rows.sort(key=lambda row: row["raw_id"])
    require(len(omitted_terminal_rows) == 54, "omitted terminal member scope")
    require(
        len({(row["source_index"], row["canonical_class_id"]) for row in omitted_terminal_rows})
        == 35,
        "omitted terminal class scope",
    )
    critical_triangle_ids = {67_161, 67_167, 67_401, 67_407}
    require(
        {
            row["raw_id"]
            for row in omitted_terminal_rows
            if row["relation"] == "triangle"
        }
        >= critical_triangle_ids,
        "critical omitted terminal triangle scope",
    )
    omitted_terminal_scope = {
        "member_presentations": len(omitted_terminal_rows),
        "canonical_classes": len({
            (row["source_index"], row["canonical_class_id"])
            for row in omitted_terminal_rows
        }),
        "ordered_record_sha256": sha(omitted_terminal_rows),
        "critical_triangle_raw_ids": sorted(critical_triangle_ids),
        "forest_intersection": 0,
        "downstream_contract": "restore physical equality anchors in the coherent probe package",
    }
    historical = decode_json_document(
        HISTORICAL_CERTIFICATE.read_bytes(),
        label=HISTORICAL_CERTIFICATE.name,
        require_object=True,
    )
    historical_unhashed = dict(historical)
    historical_payload = historical_unhashed.pop("certificate_payload_sha256")
    require(sha(historical_unhashed) == historical_payload, "historical payload")
    require(historical["census"]["raw_five_port_children"] == 36_568, "historical raw census")
    require(historical["census"]["proof_counts"]["strict_tree_sunlet_sign"] == 646, "historical affected census")
    historical_hashes = historical["ordered_raw_child_hashes"]

    source_graph_cache = {}
    source_descriptor_cache = {}
    source_outputs_cache = {}
    source_prepared_cache = {}
    source_transport_cache = {}
    first_source_transport_certificates = {}
    first_target_transport_certificates = {}
    algebra_cache = {}
    algebra_certificates = {}
    quartet_certificates = {}
    sign_cache = {}
    sign_certificates = {}
    f112 = restoration.load_f112_quartic()
    first_coverage = []
    continuation_states = []
    historical_proof_counts = collections.Counter()
    corrected_first_counts = collections.Counter()
    exact_relations = collections.Counter()
    first_exact_relations = collections.Counter()
    ordinal = 0

    def source_data(root, insertion_index):
        key = (root["source_index"], insertion_index)
        if key not in source_graph_cache:
            source_graph_cache[key] = restoration.insert_source_leaf(
                atlas,
                sources[root["source_index"]].graph,
                root["source_insertion_edge_candidates"][insertion_index],
                4,
            )
            descriptor, outputs = graph_descriptor(atlas, source_graph_cache[key])
            source_descriptor_cache[key] = descriptor
            source_outputs_cache[key] = outputs
            source_prepared_cache[key] = atlas.prepare_mixed_source(source_graph_cache[key])
            transport_id, transport = first_parent_transport(
                atlas,
                "source_support_subdivision_attachment",
                sources[root["source_index"]].graph,
                source_graph_cache[key],
                {
                    "source_index": root["source_index"],
                    "source_insertion_index": insertion_index,
                },
            )
            source_transport_cache[key] = transport_id
            previous = first_source_transport_certificates.setdefault(transport_id, transport)
            require(previous == transport, "source parent transport collision")
        return (
            key,
            source_graph_cache[key],
            source_descriptor_cache[key],
            source_outputs_cache[key],
        )

    for root in roots:
        roles = tuple(root["dummy_roles"])
        for restored_role in roles:
            target_full, target_selected = restoration.promoted_target(
                atlas,
                targets,
                root["target_index"],
                tuple(root["port_match"]),
                restored_role,
                4,
            )
            parent_target = atlas.selected_graph_from_completion(
                atlas.relabel_record(
                    targets[root["target_index"]], tuple(root["port_match"])
                )
            )
            target_transport_id, target_transport = first_parent_transport(
                atlas,
                "target_dummy_promotion",
                parent_target,
                target_full,
                {
                    "target_index": root["target_index"],
                    "port_match": list(root["port_match"]),
                    "restored_role": restored_role,
                },
            )
            previous = first_target_transport_certificates.setdefault(
                target_transport_id, target_transport
            )
            require(previous == target_transport, "target parent transport collision")
            target_descriptor = target_outputs = None
            for insertion_index, insertion in enumerate(root["source_insertion_edge_candidates"]):
                require(ordinal < len(historical_hashes), "historical ordinal overflow")
                source_key, source_graph, source_descriptor, source_outputs = source_data(
                    root, insertion_index
                )
                remaining_roles = [role for role in roles if role != restored_role]
                identity = {
                    "root_id": root["root_id"],
                    "restored_role": restored_role,
                    "restored_label": 4,
                    "remaining_roles": remaining_roles,
                    "source_insertion_index": insertion_index,
                }
                direct_relation = atlas.mixed_relation_exact_prepared(
                    source_prepared_cache[source_key], target_selected
                )
                first_exact_relations[direct_relation] += 1
                require(
                    direct_relation == "none",
                    f"exact relation must precede restoration exclusion:{identity}:{direct_relation}",
                )
                historical_result = restoration.proof_first_topology(
                    atlas, source_graph, target_selected
                )
                historical_proof = historical_result.get("proof") or historical_result["status"]
                historical_proof_counts[historical_proof] += 1
                row = {
                    "ordinal": ordinal,
                    **identity,
                    "historical_row_sha256": historical_hashes[ordinal],
                    "historical_proof_REVOKED_if_sign": historical_proof,
                    "source_parent_transport_id": source_transport_cache[source_key],
                    "target_parent_transport_id": target_transport_id,
                }

                quartet = quartet_separator(atlas, source_graph, target_selected, range(5))
                if historical_proof == "strict_tree_sunlet_sign":
                    require(quartet is None, f"affected row has quartet:{identity}")
                    exact_relations[direct_relation] += 1
                    if target_descriptor is None:
                        target_descriptor, target_outputs = graph_descriptor(atlas, target_full)
                    t_certificate = find_strict_t_separator(
                        atlas,
                        source_descriptor,
                        source_outputs,
                        target_descriptor,
                        target_outputs,
                        range(5),
                        sign_cache,
                        sign_certificates,
                    )
                    if t_certificate is not None:
                        row.update({
                            "corrected_status": "separated",
                            "corrected_proof": "full_map_Ti_zero_strict_sign",
                            "certificate": t_certificate,
                        })
                        corrected_first_counts["full_map_Ti_zero_strict_sign"] += 1
                    elif remaining_roles:
                        require(len(remaining_roles) == 1, f"continuation arity:{identity}")
                        row.update({
                            "corrected_status": "continuation",
                            "corrected_proof": "restore_remaining_physical_role",
                            "certificate": {
                                "all_asymmetric_Ti_search": "none",
                                "next_restored_role": remaining_roles[0],
                                "next_restored_label": 5,
                                "expected_source_insertion_children": 8,
                            },
                        })
                        corrected_first_counts["restore_remaining_physical_role"] += 1
                        continuation_states.append(
                            (len(first_coverage), root, restored_role, insertion_index)
                        )
                    else:
                        proof = restoration.inherited_quartic_certificate(
                            atlas, source_descriptor, target_descriptor, f112
                        )
                        require(proof is not None, f"physical affected row unresolved:{identity}")
                        verify_algebra_multihomogeneity(atlas, proof, 5)
                        proof_sha256 = sha(proof)
                        algebra_certificates.setdefault(proof_sha256, proof)
                        require(algebra_certificates[proof_sha256] == proof, "quartic certificate collision")
                        row.update({
                            "corrected_status": "separated",
                            "corrected_proof": "inherited_exact_F_2_112_quartic",
                            "certificate_sha256": proof_sha256,
                        })
                        corrected_first_counts["inherited_exact_F_2_112_quartic_new"] += 1
                elif quartet is not None:
                    require(historical_proof == "displayed_quartet_mismatch", (
                        "historical non-sign topology drift", identity, historical_proof
                    ))
                    row.update({
                        "corrected_status": "separated",
                        "corrected_proof": "displayed_quartet_mismatch",
                        "certificate_sha256": sha(quartet),
                    })
                    quartet_certificates.setdefault(sha(quartet), quartet)
                    require(quartet_certificates[sha(quartet)] == quartet, "quartet certificate collision")
                    corrected_first_counts["displayed_quartet_mismatch"] += 1
                else:
                    exact_relations[direct_relation] += 1
                    if target_descriptor is None:
                        target_descriptor, target_outputs = graph_descriptor(atlas, target_full)
                    algebra_key = (source_descriptor, target_descriptor)
                    if algebra_key not in algebra_cache:
                        proof = restoration.quadratic_certificate(
                            atlas, source_descriptor, target_descriptor
                        )
                        if proof is None:
                            proof = restoration.inherited_quartic_certificate(
                                atlas, source_descriptor, target_descriptor, f112
                            )
                        require(proof is not None, f"unaffected residual unresolved:{identity}")
                        verify_algebra_multihomogeneity(atlas, proof, 5)
                        algebra_cache[algebra_key] = proof
                    proof = algebra_cache[algebra_key]
                    require(historical_proof == "equal_topology_deck", (
                        "historical algebra selector drift", identity, historical_proof
                    ))
                    proof_sha256 = sha(proof)
                    algebra_certificates.setdefault(proof_sha256, proof)
                    require(algebra_certificates[proof_sha256] == proof, "algebra certificate collision")
                    row.update({
                        "corrected_status": "separated",
                        "corrected_proof": proof["proof"],
                        "certificate_sha256": proof_sha256,
                    })
                    corrected_first_counts[proof["proof"]] += 1

                row["corrected_row_sha256"] = sha(row)
                first_coverage.append(row)
                ordinal += 1
                if ordinal % 5_000 == 0:
                    print(f"corrected restoration first:{ordinal}/36568", file=sys.stderr, flush=True)

    require(ordinal == len(historical_hashes) == 36_568, "complete first-child coverage")
    require(first_exact_relations == {"none": 36_568}, "exact-relation-first census")
    require(historical_proof_counts == {
        "displayed_quartet_mismatch": 35_758,
        "strict_tree_sunlet_sign": 646,
        "equal_topology_deck": 164,
    }, f"historical proof census:{historical_proof_counts}")
    require(corrected_first_counts == {
        "displayed_quartet_mismatch": 35_758,
        "exact_multihomogeneous_quadratic": 148,
        "inherited_exact_F_2_112_quartic": 16,
        "full_map_Ti_zero_strict_sign": 606,
        "restore_remaining_physical_role": 32,
        "inherited_exact_F_2_112_quartic_new": 8,
    }, f"corrected first census:{corrected_first_counts}")
    require(len(continuation_states) == 32, "continuation parent census")
    require(len(first_source_transport_certificates) == 42, "first source transport classes")
    require(len(first_target_transport_certificates) == 4_986, "first target transport classes")

    second_coverage = []
    corrected_second_counts = collections.Counter()
    for first_coverage_index, root, first_role, first_insertion_index in continuation_states:
        parent = first_coverage[first_coverage_index]
        remaining_role = parent["remaining_roles"][0]
        first_source = source_graph_cache[(root["source_index"], first_insertion_index)]
        target_full, first_target_selected = restoration.promoted_target(
            atlas,
            targets,
            root["target_index"],
            tuple(root["port_match"]),
            first_role,
            4,
        )
        second_target_full = target_full.copy()
        nodes = [
            node for node, data in second_target_full.nodes(data=True)
            if data.get("dummy_name") == remaining_role
        ]
        require(len(nodes) == 1, f"second target role transport:{parent}")
        data = second_target_full.nodes[nodes[0]]
        data["label"] = 5
        data["dummy"] = False
        data["dummy_name"] = None
        second_target_selected = atlas.restrict_rooted(second_target_full, set(range(6)))
        second_candidates = restoration.source_insertion_candidates(first_source)
        require(len(second_candidates) == 8, f"second insertion census:{parent}")
        second_target_descriptor = second_target_outputs = None
        for second_index, second_insertion in enumerate(second_candidates):
            second_source = restoration.insert_source_leaf(
                atlas, first_source, second_insertion, 5
            )
            restricted_second_source = atlas.restrict_rooted(second_source, set(range(5)))
            restricted_second_target = atlas.restrict_rooted(second_target_full, set(range(5)))
            first_source_payload = exact_labelled_mixed_payload(atlas, first_source)
            first_target_payload = exact_labelled_mixed_payload(atlas, first_target_selected)
            require(
                exact_labelled_mixed_payload(atlas, restricted_second_source)
                == first_source_payload,
                f"exact second source parent transport:{parent['corrected_row_sha256']}:{second_index}",
            )
            require(
                exact_labelled_mixed_payload(atlas, restricted_second_target)
                == first_target_payload,
                f"exact second target parent transport:{parent['corrected_row_sha256']}:{second_index}",
            )
            row = {
                "parent_first_row_sha256": parent["corrected_row_sha256"],
                "parent_first_coverage_index": first_coverage_index,
                "root_id": root["root_id"],
                "first_restored_role": first_role,
                "first_restored_label": 4,
                "first_source_insertion_index": first_insertion_index,
                "second_restored_role": remaining_role,
                "second_restored_label": 5,
                "second_source_insertion_index": second_index,
                "remaining_roles": [],
                "source_parent_mixed_graph_sha256": sha(first_source_payload),
                "target_parent_mixed_graph_sha256": sha(first_target_payload),
            }
            quartet = quartet_separator(
                atlas, second_source, second_target_selected, range(6)
            )
            if quartet is not None:
                row.update({
                    "status": "separated",
                    "proof": "displayed_quartet_mismatch",
                    "certificate_sha256": sha(quartet),
                })
                quartet_certificates.setdefault(sha(quartet), quartet)
                require(quartet_certificates[sha(quartet)] == quartet, "second quartet certificate collision")
                corrected_second_counts["displayed_quartet_mismatch"] += 1
            else:
                relation = atlas.mixed_relation_exact_prepared(
                    atlas.prepare_mixed_source(second_source), second_target_selected
                )
                require(relation == "none", f"second residual graph relation:{row}:{relation}")
                exact_relations[relation] += 1
                source_descriptor, source_outputs = graph_descriptor(atlas, second_source)
                if second_target_descriptor is None:
                    second_target_descriptor, second_target_outputs = graph_descriptor(
                        atlas, second_target_full
                    )
                t_certificate = find_strict_t_separator(
                    atlas,
                    source_descriptor,
                    source_outputs,
                    second_target_descriptor,
                    second_target_outputs,
                    range(6),
                    sign_cache,
                    sign_certificates,
                )
                require(t_certificate is not None, f"second residual unresolved:{row}")
                row.update({
                    "status": "separated",
                    "proof": "full_map_Ti_zero_strict_sign",
                    "certificate": t_certificate,
                })
                corrected_second_counts["full_map_Ti_zero_strict_sign"] += 1
            row["row_sha256"] = sha(row)
            second_coverage.append(row)

    require(len(second_coverage) == 256, "second child coverage")
    require(corrected_second_counts == {
        "displayed_quartet_mismatch": 248,
        "full_map_Ti_zero_strict_sign": 8,
    }, f"second census:{corrected_second_counts}")
    require(all(row["remaining_roles"] == [] for row in second_coverage), "second physical leaves")

    first_status_counts = collections.Counter(row["corrected_status"] for row in first_coverage)
    require(first_status_counts == {"separated": 36_536, "continuation": 32}, "first status counts")
    final_leaf_count = first_status_counts["separated"] + len(second_coverage)
    require(final_leaf_count == 36_792, "final leaf count")

    # Project the promotion artifact onto corrected facts only.  The retired
    # classifier fields and immutable old row hashes live exclusively in the
    # separate provenance crosswalk below.
    clean_first_coverage = []
    for source_row in first_coverage:
        clean_row = {
            "ordinal": source_row["ordinal"],
            "root_id": source_row["root_id"],
            "restored_role": source_row["restored_role"],
            "restored_label": source_row["restored_label"],
            "remaining_roles": source_row["remaining_roles"],
            "source_insertion_index": source_row["source_insertion_index"],
            "source_parent_transport_id": source_row["source_parent_transport_id"],
            "target_parent_transport_id": source_row["target_parent_transport_id"],
            "status": source_row["corrected_status"],
            "proof": source_row["corrected_proof"],
        }
        if "certificate" in source_row:
            clean_row["certificate"] = source_row["certificate"]
        if "certificate_sha256" in source_row:
            clean_row["certificate_sha256"] = source_row["certificate_sha256"]
        clean_row["row_sha256"] = sha(clean_row)
        clean_first_coverage.append(clean_row)

    clean_second_coverage = []
    for source_row in second_coverage:
        clean_row = {
            key: value
            for key, value in source_row.items()
            if key not in {"row_sha256", "parent_first_row_sha256"}
        }
        parent_index = clean_row["parent_first_coverage_index"]
        clean_row["parent_first_row_sha256"] = clean_first_coverage[parent_index]["row_sha256"]
        clean_row["row_sha256"] = sha(clean_row)
        clean_second_coverage.append(clean_row)

    clean_first_hashes = [row["row_sha256"] for row in clean_first_coverage]
    clean_second_hashes = [row["row_sha256"] for row in clean_second_coverage]
    clean_first_proof_counts = collections.Counter(row["proof"] for row in clean_first_coverage)
    require(clean_first_proof_counts == {
        "displayed_quartet_mismatch": 35_758,
        "exact_multihomogeneous_quadratic": 148,
        "inherited_exact_F_2_112_quartic": 24,
        "full_map_Ti_zero_strict_sign": 606,
        "restore_remaining_physical_role": 32,
    }, f"clean first proof census:{clean_first_proof_counts}")

    crosswalk_first = []
    for source_row, clean_row in zip(first_coverage, clean_first_coverage):
        record = dict(source_row)
        record["clean_row_sha256"] = clean_row["row_sha256"]
        crosswalk_first.append(record)
    crosswalk_second = []
    for source_row, clean_row in zip(second_coverage, clean_second_coverage):
        record = dict(source_row)
        record["clean_row_sha256"] = clean_row["row_sha256"]
        crosswalk_second.append(record)

    crosswalk = {
        "schema": "k2p-corrected-restoration-historical-crosswalk-v1",
        "status": "PASS",
        "claim_boundary": (
            "Immutable provenance crosswalk from the released first-child ordering and "
            "retired rooted classifier fields to the clean corrected restoration forest."
        ),
        "inputs": {
            "restoration_generator_sha256": sha_file(RESTORATION_PATH),
            "historical_certificate_sha256": sha_file(HISTORICAL_CERTIFICATE),
            "historical_certificate_payload_sha256": historical_payload,
            "atlas_sha256": historical["inputs"]["atlas_sha256"],
            "quartic_sha256": historical["inputs"]["quartic_sha256"],
            "manifest_sha256": manifest_hashes,
            "raw_directional_ledger_sha256": sha_file(RAW_LEDGER),
        },
        "census": {
            "canonical_restoration_parents": canonical_parent_count,
            "member_roots": len(roots),
            "first_children": len(first_coverage),
            "historical_affected_sign_rows": historical_proof_counts["strict_tree_sunlet_sign"],
            "corrected_first_proof_counts": dict(sorted(corrected_first_counts.items())),
            "corrected_first_status_counts": dict(sorted(first_status_counts.items())),
            "continuation_parents": len(continuation_states),
            "source_second_insertion_candidates_per_parent": 8,
            "second_children": len(second_coverage),
            "corrected_second_proof_counts": dict(sorted(corrected_second_counts.items())),
            "final_leaves": final_leaf_count,
            "exact_graph_relation_none_residuals": exact_relations["none"],
            "first_children_exact_relation_none": first_exact_relations["none"],
            "sign_polynomial_classes": len(sign_certificates),
            "algebra_certificate_classes": len(algebra_certificates),
            "first_source_parent_transport_classes": len(first_source_transport_certificates),
            "first_target_parent_transport_classes": len(first_target_transport_certificates),
            "first_parent_transport_edges": len(first_coverage),
            "second_parent_transport_edges": len(second_coverage),
            "unresolved": 0,
            "missing_children": 0,
            "cycles": 0,
            "max_depth": 2,
        },
        "bridge_torus": {
            "T_i_multihomogeneity": "replayed for every presentation; selected non-oriented leaves have sector weight (s^2 g), the oriented leaf has g^2, and all other arm weights are zero",
            "quartic_multihomogeneity": "replayed from every lifted observable monomial",
            "conclusion": "all algebra separators descend through the independent s/g boundary-incidence bridge torus",
        },
        "transport_contract": {
            "first_child": "every row binds source_parent_transport_id and target_parent_transport_id; deleting label 4 and suppressing its subdivision recovers the exact labelled semi-directed parent payload on both sides",
            "second_child": "parent_first_row_sha256 plus second_restored_role and second_source_insertion_index uniquely reconstruct the remaining target promotion to label 5 and one of the eight source subdivision attachments",
            "restriction": "every first and second edge is replayed by deleting the newest labelled arm and requiring exact equality with the recorded parent mixed-graph payload, including node names, labels, roles, and retained arrowheads",
        },
        "scope_contract": omitted_terminal_scope,
        "first_source_transport_certificates": dict(sorted(first_source_transport_certificates.items())),
        "first_target_transport_certificates": dict(sorted(first_target_transport_certificates.items())),
        "quartet_certificates": dict(sorted(quartet_certificates.items())),
        "algebra_certificates": dict(sorted(algebra_certificates.items())),
        "sign_certificates": dict(sorted(sign_certificates.items())),
        "first_coverage": crosswalk_first,
        "first_row_hashes": [row["corrected_row_sha256"] for row in first_coverage],
        "first_hash_root": sha([row["corrected_row_sha256"] for row in first_coverage]),
        "clean_first_row_hashes": clean_first_hashes,
        "clean_first_hash_root": sha(clean_first_hashes),
        "second_coverage": crosswalk_second,
        "second_row_hashes": [row["row_sha256"] for row in second_coverage],
        "second_hash_root": sha([row["row_sha256"] for row in second_coverage]),
        "clean_second_row_hashes": clean_second_hashes,
        "clean_second_hash_root": sha(clean_second_hashes),
    }
    crosswalk["payload_sha256"] = sha(crosswalk)
    CROSSWALK_OUTPUT.write_text(json.dumps(crosswalk, indent=2, sort_keys=True) + "\n")

    report = {
        "schema": "k2p-corrected-restoration-forest-v3",
        "status": "PASS",
        "claim_boundary": (
            "Complete corrected first-/second-child restoration forest.  Every terminal "
            "proof is a displayed-quartet mismatch, an exact full-map T_i zero/strict-sign "
            "identity, an exact multihomogeneous quadratic, or a transported exact "
            "F_(2,112) quartic."
        ),
        "inputs": {
            "restoration_generator_sha256": sha_file(RESTORATION_PATH),
            "atlas_sha256": historical["inputs"]["atlas_sha256"],
            "quartic_sha256": historical["inputs"]["quartic_sha256"],
            "manifest_sha256": manifest_hashes,
            "raw_directional_ledger_sha256": sha_file(RAW_LEDGER),
            "provenance_crosswalk_sha256": sha_file(CROSSWALK_OUTPUT),
            "provenance_crosswalk_payload_sha256": crosswalk["payload_sha256"],
        },
        "census": {
            "canonical_restoration_parents": canonical_parent_count,
            "member_roots": len(roots),
            "forest_edges": len(clean_first_coverage) + len(clean_second_coverage),
            "first_children": len(clean_first_coverage),
            "first_proof_counts": dict(sorted(clean_first_proof_counts.items())),
            "first_status_counts": dict(sorted(first_status_counts.items())),
            "continuation_parents": len(continuation_states),
            "source_second_insertion_candidates_per_parent": 8,
            "second_children": len(clean_second_coverage),
            "second_proof_counts": dict(sorted(corrected_second_counts.items())),
            "final_leaves": final_leaf_count,
            "exact_graph_relation_none_residuals": exact_relations["none"],
            "first_children_exact_relation_none": first_exact_relations["none"],
            "sign_polynomial_classes": len(sign_certificates),
            "algebra_certificate_classes": len(algebra_certificates),
            "first_source_parent_transport_classes": len(first_source_transport_certificates),
            "first_target_parent_transport_classes": len(first_target_transport_certificates),
            "first_parent_transport_edges": len(clean_first_coverage),
            "second_parent_transport_edges": len(clean_second_coverage),
            "unresolved": 0,
            "missing_children": 0,
            "cycles": 0,
            "max_depth": 2,
        },
        "bridge_torus": crosswalk["bridge_torus"],
        "transport_contract": crosswalk["transport_contract"],
        "scope_contract": omitted_terminal_scope,
        "first_source_transport_certificates": dict(sorted(first_source_transport_certificates.items())),
        "first_target_transport_certificates": dict(sorted(first_target_transport_certificates.items())),
        "quartet_certificates": dict(sorted(quartet_certificates.items())),
        "algebra_certificates": dict(sorted(algebra_certificates.items())),
        "sign_certificates": dict(sorted(sign_certificates.items())),
        "first_coverage": clean_first_coverage,
        "first_row_hashes": clean_first_hashes,
        "first_hash_root": sha(clean_first_hashes),
        "second_coverage": clean_second_coverage,
        "second_row_hashes": clean_second_hashes,
        "second_hash_root": sha(clean_second_hashes),
    }
    forbidden = (
        "historical_proof_REVOKED_if_sign",
        "historical_row_sha256",
        "strict_tree_sunlet_sign",
    )
    serialized_report = canonical_bytes(report).decode()
    require(not any(token in serialized_report for token in forbidden), "retired classifier leaked into clean projection")
    report["payload_sha256"] = sha(report)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": report["status"],
        **report["census"],
        "payload_sha256": report["payload_sha256"],
        "crosswalk_payload_sha256": crosswalk["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (
        Failure,
        StrictJSONError,
        AssertionError,
        KeyError,
        IndexError,
        OSError,
        json.JSONDecodeError,
    ) as error:
        raise SystemExit(f"CORRECTED_RESTORATION_FAIL:{error}") from error
