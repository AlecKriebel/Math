#!/usr/bin/env python3
"""Independent, fail-closed replay of the corrected restoration forest."""

from __future__ import annotations

import argparse
import ast
import collections
import fractions
import gzip
import hashlib
import importlib.util
import itertools
import json
import math
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RESTORATION_PATH = PROJECT / "work/restoration_forest/enumerate_five_port.py"
HISTORICAL_PATH = PROJECT / "work/restoration_forest/five_port_certificate.json"
RAW_LEDGER = PROJECT / "work/raw_ledger_audit/artifacts/raw_directional_ledger.jsonl.gz"
DEFAULT_CERTIFICATE = HERE / "corrected_restoration_forest.json"
DEFAULT_CROSSWALK = HERE / "corrected_restoration_historical_crosswalk.json"
DEFAULT_REPORT = HERE / "corrected_restoration_replay_certificate.json"


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
    """Independent exact serialization for concrete restriction transports."""
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


def replay_first_parent_transport(atlas, kind, parent, child, identity):
    restricted = atlas.restrict_rooted(child, set(range(4)))
    parent_payload = exact_labelled_mixed_payload(atlas, parent)
    restricted_payload = exact_labelled_mixed_payload(atlas, restricted)
    require(parent_payload == restricted_payload, f"first exact parent restriction:{kind}:{identity}")
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
    require(spec is not None and spec.loader is not None, f"import:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sparse_payload(polynomial):
    return [[list(exponent), str(coefficient)] for exponent, coefficient in sorted(polynomial.items())]


def sparse_hash(polynomial):
    return sha(sparse_payload(polynomial))


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

    vi, v = coordinate((1, 3, 2))
    xsi, xs = coordinate((1, 1, 0))
    xgi, xg = coordinate((2, 2, 0))
    ygi, yg = coordinate((2, 0, 2))
    zgi, zg = coordinate((0, 2, 2))
    polynomial = atlas.sparse_lincomb(
        [atlas.sparse_mul_many([v, v, xg]), atlas.sparse_mul_many([xs, xs, yg, zg])],
        [1, -1],
    )
    weights = atlas.coordinate_weights(descriptor.k)
    left = tuple(2 * weights[vi][slot] + weights[xgi][slot] for slot in range(2 * descriptor.k))
    right = tuple(
        2 * weights[xsi][slot] + weights[ygi][slot] + weights[zgi][slot]
        for slot in range(2 * descriptor.k)
    )
    expected = [0] * (2 * descriptor.k)
    for label in others:
        expected[2 * label] = 2
        expected[2 * label + 1] = 1
    expected[2 * orientation + 1] = 2
    require(left == right == tuple(expected), "T_i observable multihomogeneity")
    return polynomial, left


def direct_bernstein(polynomial):
    require(polynomial, "empty signed polynomial")
    parameter_count = len(next(iter(polynomial)))
    monomial = tuple(min(exponent[i] for exponent in polynomial) for i in range(parameter_count))
    active = tuple(
        i for i in range(parameter_count)
        if len({exponent[i] - monomial[i] for exponent in polynomial}) > 1
    )
    residual = {
        tuple(exponent[i] - monomial[i] for i in active): fractions.Fraction(coefficient)
        for exponent, coefficient in polynomial.items()
    }
    degree = tuple(max(exponent[i] for exponent in residual) for i in range(len(active)))
    count = math.prod(value + 1 for value in degree)
    require(count <= 100_000, f"Bernstein replay bound:{count}")
    values = []
    for beta in itertools.product(*(range(value + 1) for value in degree)):
        total = fractions.Fraction(0)
        for alpha, coefficient in residual.items():
            if not all(left <= right for left, right in zip(alpha, beta)):
                continue
            factor = fractions.Fraction(1)
            for n, left, right in zip(degree, alpha, beta):
                factor *= fractions.Fraction(math.comb(right, left), math.comb(n, left))
            total += coefficient * factor
        values.append(total)
    signs = collections.Counter(-1 if value < 0 else 1 if value > 0 else 0 for value in values)
    require(signs[1] == 0 and signs[-1] > 0, f"Bernstein sign:{signs}")
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


def evaluate_sparse(polynomial, point):
    total = fractions.Fraction(0)
    for exponent, coefficient in polynomial.items():
        term = fractions.Fraction(coefficient)
        for value, power in zip(point, exponent):
            if power:
                term *= value ** power
        total += term
    return total


def parse_fraction(value):
    return fractions.Fraction(value)


def verify_physical_witness(descriptor, polynomial, witness):
    edge_pairs = [tuple(map(parse_fraction, pair)) for pair in witness["edge_pairs"]]
    lambdas = [parse_fraction(value) for value in witness["lambdas"]]
    require(len(edge_pairs) == descriptor.edge_class_count, "witness edge count")
    require(len(lambdas) == descriptor.retic_count, "witness lambda count")
    for s_value, g_value in edge_pairs:
        require(0 < s_value < 1, "witness s outside D_plus")
        require(0 < g_value < 1, "witness g outside D_plus")
        require(g_value > 2 * s_value - 1, "witness K2P stochastic inequality")
    for value in lambdas:
        require(0 < value < 1, "witness inheritance outside open interval")
    point = tuple(value for pair in edge_pairs for value in pair) + tuple(lambdas)
    evaluated = evaluate_sparse(polynomial, point)
    require(evaluated == parse_fraction(witness["value"]), "witness evaluation")
    require(evaluated != 0, "zero physical witness")


def polynomial_pullback(atlas, public_polynomial, outputs):
    columns = [
        atlas.sparse_mul_many([outputs[index] for index in monomial])
        for monomial, _ in public_polynomial
    ]
    return atlas.sparse_lincomb(columns, [coefficient for _, coefficient in public_polynomial])


def verify_algebra_certificate(atlas, proof, source_descriptor, target_descriptor):
    source_outputs = atlas.output_sparse_polynomials(source_descriptor)
    target_outputs = atlas.output_sparse_polynomials(target_descriptor)
    weights = atlas.coordinate_weights(source_descriptor.k)
    require(source_descriptor.k == target_descriptor.k, "algebra k mismatch")
    if proof["proof"] == "exact_multihomogeneous_quadratic":
        pairs = [tuple(pair) for pair in proof["coordinate_pairs"]]
        coefficients = [parse_fraction(value) for value in proof["coefficients"]]
        target_pullback = atlas.sparse_lincomb(
            [atlas.sparse_mul(target_outputs[left], target_outputs[right]) for left, right in pairs],
            coefficients,
        )
        source_pullback = atlas.sparse_lincomb(
            [atlas.sparse_mul(source_outputs[left], source_outputs[right]) for left, right in pairs],
            coefficients,
        )
        degrees = {
            tuple(weights[left][slot] + weights[right][slot] for slot in range(2 * source_descriptor.k))
            for left, right in pairs
        }
    elif proof["proof"] == "inherited_exact_F_2_112_quartic":
        public = [
            (tuple(monomial), parse_fraction(coefficient))
            for monomial, coefficient in proof["lifted_coordinate_monomials"]
        ]
        target_pullback = polynomial_pullback(atlas, public, target_outputs)
        source_pullback = polynomial_pullback(atlas, public, source_outputs)
        degrees = {
            tuple(
                sum(weights[index][slot] for index in monomial)
                for slot in range(2 * source_descriptor.k)
            )
            for monomial, _ in public
        }
    else:
        raise Failure(f"unknown algebra proof:{proof['proof']}")
    require(not target_pullback, "algebra target pullback nonzero")
    require(source_pullback, "algebra source pullback zero")
    require(len(source_pullback) == proof["source_pullback_term_count"], "algebra source term count")
    require(sparse_hash(source_pullback) == proof["source_pullback_sha256"], "algebra source hash")
    require(len(degrees) == 1 and list(next(iter(degrees))) == proof["weight"], "algebra bridge multihomogeneity")
    witness = proof["source_pullback_witness"]
    exponent = tuple(witness["parameter_exponent"])
    require(str(source_pullback.get(exponent)) == witness["coefficient"], "algebra coefficient witness")
    verify_physical_witness(source_descriptor, source_pullback, proof["strict_D_plus_witness"])


def split_payload(value):
    result = []
    for item in sorted(value, key=repr):
        if item == ("star",):
            result.append(["star"])
        else:
            result.append([list(item[0]), list(item[1])])
    return result


def first_quartet(atlas, source, target, labels):
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


def all_asymmetric_t(atlas, source_descriptor, source_outputs, target_descriptor, target_outputs, labels):
    result = []
    for triple in itertools.combinations(labels, 3):
        for orientation in triple:
            source, source_weight = t_pullback(atlas, source_descriptor, source_outputs, triple, orientation)
            target, target_weight = t_pullback(atlas, target_descriptor, target_outputs, triple, orientation)
            require(source_weight == target_weight, "T transport weight")
            if bool(source) != bool(target):
                result.append((triple, orientation, source, target, source_weight))
    return result


def verify_t_row(atlas, row_certificate, source_descriptor, source_outputs, target_descriptor, target_outputs, sign_records, polynomial_registry):
    triple = tuple(row_certificate["triple"])
    orientation = row_certificate["orientation"]
    source, source_weight = t_pullback(atlas, source_descriptor, source_outputs, triple, orientation)
    target, target_weight = t_pullback(atlas, target_descriptor, target_outputs, triple, orientation)
    require(source_weight == target_weight == tuple(row_certificate["observable_boundary_multidegree"]), "T row multidegree")
    require(sparse_hash(source) == row_certificate["source_pullback_sha256"], "T source hash")
    require(sparse_hash(target) == row_certificate["target_pullback_sha256"], "T target hash")
    signed_side = row_certificate["signed_side"]
    zero_side = row_certificate["zero_side"]
    require({signed_side, zero_side} == {"source", "target"}, "T side partition")
    signed = source if signed_side == "source" else target
    zero = source if zero_side == "source" else target
    require(not zero and signed, "T zero/sign identity")
    signed_hash = sparse_hash(signed)
    require(signed_hash == row_certificate["signed_pullback_sha256"], "T signed hash")
    require(signed_hash in sign_records, "missing T sign certificate")
    record = sign_records[signed_hash]
    require(record["pullback_sha256"] == signed_hash, "T record pullback hash")
    require(record["pullback_term_count"] == len(signed), "T record term count")
    require(record["strict_sign"] == row_certificate["strict_sign"], "T strict sign binding")
    require(record["observable_boundary_multidegree"] == list(source_weight), "T record multidegree")
    normalized = signed if record["strict_sign"] == "negative" else {
        exponent: -coefficient for exponent, coefficient in signed.items()
    }
    require(sparse_hash(normalized) == record["normalized_negative_pullback_sha256"], "T normalized hash")
    require(record["normalized_negative_pullback_sha256"] == row_certificate["normalized_negative_pullback_sha256"], "T row normalized hash")
    if signed_hash not in polynomial_registry:
        # Validate the exact Bernstein tensor at first use, so a reassigned or
        # altered sign certificate fails at the presentation that invokes it.
        require(
            direct_bernstein(normalized) == record["bernstein"],
            f"Bernstein record at first use:{signed_hash}",
        )
        polynomial_registry[signed_hash] = normalized
    else:
        require(polynomial_registry[signed_hash] == normalized, "T polynomial registry collision")


def main():
    if not __debug__:
        raise Failure("CORRECTED_RESTORATION_REPLAY_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--crosswalk", type=Path, default=DEFAULT_CROSSWALK)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    started = time.monotonic()
    certificate = json.loads(args.certificate.read_text())
    payload = certificate.get("payload_sha256")
    unhashed = dict(certificate)
    unhashed.pop("payload_sha256", None)
    require(payload == sha(unhashed), "corrected payload")
    require(certificate.get("schema") == "k2p-corrected-restoration-forest-v3", "schema")
    require(certificate.get("status") == "PASS", "status")
    require(certificate["inputs"]["restoration_generator_sha256"] == sha_file(RESTORATION_PATH), "generator input")
    require(
        certificate["inputs"]["provenance_crosswalk_sha256"] == sha_file(args.crosswalk),
        "provenance crosswalk input",
    )
    crosswalk = json.loads(args.crosswalk.read_text())
    crosswalk_payload = crosswalk.get("payload_sha256")
    unhashed_crosswalk = dict(crosswalk)
    unhashed_crosswalk.pop("payload_sha256", None)
    require(crosswalk_payload == sha(unhashed_crosswalk), "provenance crosswalk payload")
    require(
        crosswalk_payload == certificate["inputs"]["provenance_crosswalk_payload_sha256"],
        "provenance crosswalk payload binding",
    )
    require(
        crosswalk.get("schema") == "k2p-corrected-restoration-historical-crosswalk-v1",
        "provenance crosswalk schema",
    )
    require(crosswalk.get("status") == "PASS", "provenance crosswalk status")
    clean_serialized = canonical_bytes(certificate).decode()
    for retired in (
        "historical_proof_REVOKED_if_sign",
        "historical_row_sha256",
        "strict_tree_sunlet_sign",
    ):
        require(retired not in clean_serialized, f"retired classifier in clean projection:{retired}")
    first_coverage = certificate.get("first_coverage", [])
    second_coverage = certificate.get("second_coverage", [])
    crosswalk_first = crosswalk.get("first_coverage", [])
    crosswalk_second = crosswalk.get("second_coverage", [])
    require(len(first_coverage) == 36_568, "first coverage length")
    require(len(second_coverage) == 256, "second coverage length")
    require(len(crosswalk_first) == len(first_coverage), "crosswalk first coverage length")
    require(len(crosswalk_second) == len(second_coverage), "crosswalk second coverage length")
    recomputed_first_hashes = []
    for row in first_coverage:
        public = dict(row)
        row_hash = public.pop("row_sha256")
        require(sha(public) == row_hash, "first row hash")
        recomputed_first_hashes.append(row_hash)
    require(recomputed_first_hashes == certificate["first_row_hashes"], "first row hash list")
    require(sha(recomputed_first_hashes) == certificate["first_hash_root"], "first hash root")
    require(recomputed_first_hashes == crosswalk["clean_first_row_hashes"], "crosswalk clean first hashes")
    require(sha(recomputed_first_hashes) == crosswalk["clean_first_hash_root"], "crosswalk clean first root")
    recomputed_second_hashes = []
    for row in second_coverage:
        public = dict(row)
        row_hash = public.pop("row_sha256")
        require(sha(public) == row_hash, "second row hash")
        recomputed_second_hashes.append(row_hash)
    require(recomputed_second_hashes == certificate["second_row_hashes"], "second row hash list")
    require(sha(recomputed_second_hashes) == certificate["second_hash_root"], "second hash root")
    require(recomputed_second_hashes == crosswalk["clean_second_row_hashes"], "crosswalk clean second hashes")
    require(sha(recomputed_second_hashes) == crosswalk["clean_second_hash_root"], "crosswalk clean second root")

    # Fail closed on the abstract forest before any expensive algebra replay.
    require(
        certificate["census"]["forest_edges"]
        == len(first_coverage) + len(second_coverage)
        == 36_824,
        "forest edge census",
    )
    continuation_indices = {
        index for index, row in enumerate(first_coverage) if row["status"] == "continuation"
    }
    require(len(continuation_indices) == 32, "abstract continuation census")
    require(
        all(
            row["status"] == "separated"
            or (
                row["status"] == "continuation"
                and row["proof"] == "restore_remaining_physical_role"
                and len(row["remaining_roles"]) == 1
            )
            for row in first_coverage
        ),
        "abstract first-level status partition",
    )
    abstract_parent_use = collections.Counter()
    for row in second_coverage:
        parent_index = row["parent_first_coverage_index"]
        require(parent_index in continuation_indices, "abstract second parent")
        require(
            row["parent_first_row_sha256"] == first_coverage[parent_index]["row_sha256"],
            "abstract second parent hash",
        )
        require(row["status"] == "separated" and not row["remaining_roles"], "abstract second leaf")
        abstract_parent_use[parent_index] += 1
    require(
        set(abstract_parent_use) == continuation_indices
        and all(count == 8 for count in abstract_parent_use.values()),
        "abstract complete acyclic parent forest",
    )
    for ordinal, (record, clean_row) in enumerate(zip(crosswalk_first, first_coverage)):
        require(record["clean_row_sha256"] == clean_row["row_sha256"], f"crosswalk first row:{ordinal}")
        unhashed = dict(record)
        unhashed.pop("clean_row_sha256")
        old_row_hash = unhashed.pop("corrected_row_sha256")
        require(sha(unhashed) == old_row_hash, f"crosswalk enriched first row hash:{ordinal}")
    for ordinal, (record, clean_row) in enumerate(zip(crosswalk_second, second_coverage)):
        require(record["clean_row_sha256"] == clean_row["row_sha256"], f"crosswalk second row:{ordinal}")
        unhashed = dict(record)
        unhashed.pop("clean_row_sha256")
        old_row_hash = unhashed.pop("row_sha256")
        require(sha(unhashed) == old_row_hash, f"crosswalk enriched second row hash:{ordinal}")

    source_transport_records = certificate.get("first_source_transport_certificates", {})
    target_transport_records = certificate.get("first_target_transport_certificates", {})
    require(
        len(source_transport_records)
        == certificate["census"]["first_source_parent_transport_classes"]
        == 42,
        "source parent transport registry census",
    )
    require(
        len(target_transport_records)
        == certificate["census"]["first_target_parent_transport_classes"]
        == 4_986,
        "target parent transport registry census",
    )
    for transport_id, record in source_transport_records.items():
        require(sha(record) == transport_id, "source parent transport hash")
        require(
            record["parent_mixed_graph_sha256"]
            == record["restricted_child_mixed_graph_sha256"],
            "source parent transport payload equality",
        )
    for transport_id, record in target_transport_records.items():
        require(sha(record) == transport_id, "target parent transport hash")
        require(
            record["parent_mixed_graph_sha256"]
            == record["restricted_child_mixed_graph_sha256"],
            "target parent transport payload equality",
        )
    require(
        {row["source_parent_transport_id"] for row in first_coverage}
        == set(source_transport_records),
        "source parent transport reference coverage",
    )
    require(
        {row["target_parent_transport_id"] for row in first_coverage}
        == set(target_transport_records),
        "target parent transport reference coverage",
    )
    require(
        certificate["census"]["first_parent_transport_edges"] == len(first_coverage),
        "first parent transport edge census",
    )
    require(
        certificate["census"]["second_parent_transport_edges"] == len(second_coverage),
        "second parent transport edge census",
    )

    restoration = import_path("corrected_restoration_replay_generator", RESTORATION_PATH)
    atlas = restoration.load_atlas()
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    roots, manifest_hashes, parent_count = restoration.reconstruct_roots(atlas, sources, targets)
    require(parent_count == certificate["census"]["canonical_restoration_parents"] == 997, "parent count")
    require(manifest_hashes == certificate["inputs"]["manifest_sha256"], "manifest transports")
    require(
        certificate["inputs"]["raw_directional_ledger_sha256"]
        == crosswalk["inputs"]["raw_directional_ledger_sha256"]
        == sha_file(RAW_LEDGER),
        "raw directional ledger input",
    )
    obligation_keys = {
        (root["source_index"], root["canonical_class_id"])
        for root in roots
    }
    omitted_terminal_rows = []
    with gzip.open(RAW_LEDGER, "rt") as handle:
        for line in handle:
            raw = json.loads(line)
            if (
                raw.get("category") == "retained_terminal"
                and raw.get("status") in {"isomorphic", "triangle"}
                and targets[raw["target_index"]].dummy_labels
            ):
                require(
                    (raw["source_index"], raw["class_id"]) not in obligation_keys,
                    f"omitted terminal in obligation scope:{raw['raw_id']}",
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
    replayed_scope = {
        "member_presentations": len(omitted_terminal_rows),
        "canonical_classes": len({
            (row["source_index"], row["canonical_class_id"])
            for row in omitted_terminal_rows
        }),
        "ordered_record_sha256": sha(omitted_terminal_rows),
        "critical_triangle_raw_ids": [67_161, 67_167, 67_401, 67_407],
        "forest_intersection": 0,
        "downstream_contract": "restore physical equality anchors in the coherent probe package",
    }
    require(
        replayed_scope == certificate["scope_contract"] == crosswalk["scope_contract"],
        "omitted-terminal scope reconciliation",
    )
    historical = json.loads(HISTORICAL_PATH.read_text())
    historical_unhashed = dict(historical)
    historical_payload = historical_unhashed.pop("certificate_payload_sha256")
    require(
        sha(historical_unhashed)
        == historical_payload
        == crosswalk["inputs"]["historical_certificate_payload_sha256"],
        "historical payload",
    )
    require(
        crosswalk["inputs"]["historical_certificate_sha256"] == sha_file(HISTORICAL_PATH),
        "historical file binding",
    )
    historical_hashes = historical["ordered_raw_child_hashes"]

    quartet_records = certificate["quartet_certificates"]
    algebra_records = certificate["algebra_certificates"]
    sign_records = certificate["sign_certificates"]
    for key, record in quartet_records.items():
        require(sha(record) == key, "quartet registry hash")
    for key, record in algebra_records.items():
        require(sha(record) == key, "algebra registry hash")
    require(len(sign_records) == certificate["census"]["sign_polynomial_classes"] == 113, "sign registry count")

    source_graphs = {}
    source_descriptors = {}
    source_outputs = {}
    source_prepared = {}
    source_transport_ids = {}
    source_registry = restoration.MixedGraphRegistry(atlas)
    target_registry = restoration.MixedGraphRegistry(atlas)
    source_classes = {}
    target_classes = {}
    historical_algebra_cache = {}
    corrected_algebra_replay = set()
    polynomial_registry = {}
    relation_presentations = collections.Counter()
    exact_relations = collections.Counter()
    first_exact_relations = collections.Counter()
    corrected_first_counts = collections.Counter()
    first_status_counts = collections.Counter()
    continuation_states = []
    f112 = restoration.load_f112_quartic()
    ordinal = 0

    def source_data(root, insertion_index):
        key = (root["source_index"], insertion_index)
        if key not in source_graphs:
            source_graphs[key] = restoration.insert_source_leaf(
                atlas,
                sources[root["source_index"]].graph,
                root["source_insertion_edge_candidates"][insertion_index],
                4,
            )
            source_descriptors[key] = atlas.model_descriptor_fast2(source_graphs[key])
            source_outputs[key] = atlas.output_sparse_polynomials(source_descriptors[key])
            source_prepared[key] = atlas.prepare_mixed_source(source_graphs[key])
            source_classes[key] = source_registry.add(source_graphs[key])
            transport_id, transport = replay_first_parent_transport(
                atlas,
                "source_support_subdivision_attachment",
                sources[root["source_index"]].graph,
                source_graphs[key],
                {
                    "source_index": root["source_index"],
                    "source_insertion_index": insertion_index,
                },
            )
            require(
                source_transport_records.get(transport_id) == transport,
                f"source parent transport registry replay:{key}",
            )
            source_transport_ids[key] = transport_id
        return key, source_graphs[key], source_descriptors[key], source_outputs[key]

    for root in roots:
        roles = tuple(root["dummy_roles"])
        for role in roles:
            target_key = (root["target_index"], tuple(root["port_match"]), role)
            target_full, target_selected = restoration.promoted_target(
                atlas, targets, root["target_index"], tuple(root["port_match"]), role, 4
            )
            parent_target = atlas.selected_graph_from_completion(
                atlas.relabel_record(
                    targets[root["target_index"]], tuple(root["port_match"])
                )
            )
            target_transport_id, target_transport = replay_first_parent_transport(
                atlas,
                "target_dummy_promotion",
                parent_target,
                target_full,
                {
                    "target_index": root["target_index"],
                    "port_match": list(root["port_match"]),
                    "restored_role": role,
                },
            )
            require(
                target_transport_records.get(target_transport_id) == target_transport,
                f"target parent transport registry replay:{target_key}",
            )
            if target_key not in target_classes:
                target_classes[target_key] = target_registry.add(target_selected)
            target_descriptor = atlas.model_descriptor_fast2(target_full)
            target_outputs = atlas.output_sparse_polynomials(target_descriptor)
            for insertion_index, insertion in enumerate(root["source_insertion_edge_candidates"]):
                bound = first_coverage[ordinal]
                provenance_bound = crosswalk_first[ordinal]
                expected_identity = {
                    "root_id": root["root_id"],
                    "restored_role": role,
                    "restored_label": 4,
                    "remaining_roles": [item for item in roles if item != role],
                    "source_insertion_index": insertion_index,
                }
                require(bound["ordinal"] == ordinal, "first ordinal")
                for field, value in expected_identity.items():
                    require(bound[field] == value, f"first identity:{ordinal}:{field}")
                    require(
                        provenance_bound[field] == value,
                        f"crosswalk first identity:{ordinal}:{field}",
                    )
                source_key, source_graph, source_descriptor, source_output = source_data(root, insertion_index)
                require(
                    bound["source_parent_transport_id"] == source_transport_ids[source_key],
                    f"source parent transport row binding:{ordinal}",
                )
                require(
                    bound["target_parent_transport_id"] == target_transport_id,
                    f"target parent transport row binding:{ordinal}",
                )
                direct_relation = atlas.mixed_relation_exact_prepared(
                    source_prepared[source_key], target_selected
                )
                first_exact_relations[direct_relation] += 1
                require(
                    direct_relation == "none",
                    f"exact relation precedes all restoration exclusions:{ordinal}:{direct_relation}",
                )

                # Rebuild the complete historical row, including exact mixed
                # class IDs, rather than accepting ordinal alignment alone.
                old_result = restoration.proof_first_topology(atlas, source_graph, target_selected)
                remaining = len(roles) - 1
                if old_result["status"] == "equal_topology_deck":
                    algebra_key = (source_descriptor, target_descriptor)
                    if algebra_key not in historical_algebra_cache:
                        proof = restoration.quadratic_certificate(atlas, source_descriptor, target_descriptor)
                        if proof is None:
                            proof = restoration.inherited_quartic_certificate(
                                atlas, source_descriptor, target_descriptor, f112
                            )
                        historical_algebra_cache[algebra_key] = proof
                    if historical_algebra_cache[algebra_key] is not None:
                        old_result = historical_algebra_cache[algebra_key]
                    elif remaining == 0:
                        relation = atlas.mixed_relation_exact(source_graph, target_selected)
                        if relation == "isomorphic":
                            old_result = {"status": "isomorphic", "proof": "exact_labelled_mixed_graph"}
                        elif relation == "triangle":
                            old_result = {"status": "triangle", "proof": "ordinary_triangle_quotient"}
                historical_row = {
                    "root_id": root["root_id"],
                    "restored_role": role,
                    "restored_label": 4,
                    "remaining_roles": expected_identity["remaining_roles"],
                    "source_insertion_index": insertion_index,
                    "source_insertion": insertion,
                    "target_attachment": root["attachments"][role],
                    "source_mixed_class": source_classes[source_key],
                    "target_mixed_class": target_classes[target_key],
                    **old_result,
                }
                historical_hash = sha(historical_row)
                require(
                    historical_hash
                    == historical_hashes[ordinal]
                    == provenance_bound["historical_row_sha256"],
                    f"historical row hash:{ordinal}",
                )
                relation_presentations[(source_classes[source_key], target_classes[target_key])] += 1

                corrected_proof = bound["proof"]
                corrected_first_counts[corrected_proof] += 1
                first_status_counts[bound["status"]] += 1
                require(
                    provenance_bound["corrected_proof"] == corrected_proof
                    and provenance_bound["corrected_status"] == bound["status"],
                    f"crosswalk corrected classification:{ordinal}",
                )
                for certificate_field in ("certificate", "certificate_sha256"):
                    require(
                        provenance_bound.get(certificate_field) == bound.get(certificate_field),
                        f"crosswalk corrected certificate:{ordinal}:{certificate_field}",
                    )
                if corrected_proof == "displayed_quartet_mismatch":
                    record = quartet_records[bound["certificate_sha256"]]
                    require(first_quartet(atlas, source_graph, target_selected, range(5)) == record, f"quartet replay:{ordinal}")
                else:
                    exact_relations[direct_relation] += 1
                    if corrected_proof == "full_map_Ti_zero_strict_sign":
                        verify_t_row(
                            atlas,
                            bound["certificate"],
                            source_descriptor,
                            source_output,
                            target_descriptor,
                            target_outputs,
                            sign_records,
                            polynomial_registry,
                        )
                    elif corrected_proof == "restore_remaining_physical_role":
                        asymmetric = all_asymmetric_t(
                            atlas, source_descriptor, source_output, target_descriptor, target_outputs, range(5)
                        )
                        require(not asymmetric, f"continuation has asymmetric T:{ordinal}")
                        require(bound["certificate"] == {
                            "all_asymmetric_Ti_search": "none",
                            "next_restored_role": bound["remaining_roles"][0],
                            "next_restored_label": 5,
                            "expected_source_insertion_children": 8,
                        }, f"continuation certificate:{ordinal}")
                        continuation_states.append((ordinal, root, role, insertion_index))
                    elif corrected_proof in {
                        "exact_multihomogeneous_quadratic",
                        "inherited_exact_F_2_112_quartic",
                    }:
                        proof = algebra_records[bound["certificate_sha256"]]
                        replay_key = (bound["certificate_sha256"], source_descriptor, target_descriptor)
                        if replay_key not in corrected_algebra_replay:
                            verify_algebra_certificate(atlas, proof, source_descriptor, target_descriptor)
                            corrected_algebra_replay.add(replay_key)
                    else:
                        raise Failure(f"unknown corrected proof:{corrected_proof}")
                ordinal += 1
                if ordinal % 5_000 == 0:
                    print(f"restoration replay first:{ordinal}/36568", file=sys.stderr, flush=True)

    require(ordinal == 36_568, "first enumeration coverage")
    require(
        first_exact_relations == {"none": 36_568}
        and certificate["census"]["first_children_exact_relation_none"] == 36_568,
        "exact-relation-first census",
    )
    require(len(source_registry.representatives) == historical["census"]["exact_source_mixed_graph_classes"] == 35, "source graph classes")
    require(len(target_registry.representatives) == historical["census"]["exact_target_mixed_graph_classes"] == 314, "target graph classes")
    require(len(relation_presentations) == historical["census"]["exact_directed_relation_classes"] == 2240, "directed relation classes")
    require(dict(sorted(corrected_first_counts.items())) == certificate["census"]["first_proof_counts"], "corrected first census")
    require(dict(sorted(first_status_counts.items())) == certificate["census"]["first_status_counts"], "first status census")
    require(len(continuation_states) == certificate["census"]["continuation_parents"] == 32, "continuation count")

    corrected_second_counts = collections.Counter()
    second_ordinal = 0
    parent_use = collections.Counter()
    for first_index, root, first_role, first_insertion_index in continuation_states:
        parent = first_coverage[first_index]
        first_source = source_graphs[(root["source_index"], first_insertion_index)]
        remaining_role = parent["remaining_roles"][0]
        first_target_full, first_target_selected = restoration.promoted_target(
            atlas, targets, root["target_index"], tuple(root["port_match"]), first_role, 4
        )
        second_target_full = first_target_full.copy()
        nodes = [
            node for node, data in second_target_full.nodes(data=True)
            if data.get("dummy_name") == remaining_role
        ]
        require(len(nodes) == 1, "second target promotion node")
        data = second_target_full.nodes[nodes[0]]
        data["label"] = 5
        data["dummy"] = False
        data["dummy_name"] = None
        second_target_selected = atlas.restrict_rooted(second_target_full, set(range(6)))
        candidates = restoration.source_insertion_candidates(first_source)
        require(len(candidates) == 8, "second insertion candidate count")
        second_target_descriptor = atlas.model_descriptor_fast2(second_target_full)
        second_target_outputs = atlas.output_sparse_polynomials(second_target_descriptor)
        for second_index, candidate in enumerate(candidates):
            bound = second_coverage[second_ordinal]
            provenance_bound = crosswalk_second[second_ordinal]
            expected = {
                "parent_first_row_sha256": parent["row_sha256"],
                "parent_first_coverage_index": first_index,
                "root_id": root["root_id"],
                "first_restored_role": first_role,
                "first_restored_label": 4,
                "first_source_insertion_index": first_insertion_index,
                "second_restored_role": remaining_role,
                "second_restored_label": 5,
                "second_source_insertion_index": second_index,
                "remaining_roles": [],
            }
            for field, value in expected.items():
                require(bound[field] == value, f"second identity:{second_ordinal}:{field}")
                if field != "parent_first_row_sha256":
                    require(
                        provenance_bound[field] == value,
                        f"crosswalk second identity:{second_ordinal}:{field}",
                    )
            require(
                provenance_bound["parent_first_coverage_index"] == first_index
                and provenance_bound["parent_first_row_sha256"]
                == crosswalk_first[first_index]["corrected_row_sha256"],
                f"crosswalk second parent:{second_ordinal}",
            )
            for certificate_field in (
                "status",
                "proof",
                "certificate",
                "certificate_sha256",
                "source_parent_mixed_graph_sha256",
                "target_parent_mixed_graph_sha256",
            ):
                require(
                    provenance_bound.get(certificate_field) == bound.get(certificate_field),
                    f"crosswalk second classification:{second_ordinal}:{certificate_field}",
                )
            second_source = restoration.insert_source_leaf(atlas, first_source, candidate, 5)
            restricted_source = atlas.restrict_rooted(second_source, set(range(5)))
            restricted_target = atlas.restrict_rooted(second_target_full, set(range(5)))
            first_source_payload = exact_labelled_mixed_payload(atlas, first_source)
            first_target_payload = exact_labelled_mixed_payload(atlas, first_target_selected)
            require(
                exact_labelled_mixed_payload(atlas, restricted_source) == first_source_payload,
                f"source exact parent restriction:{second_ordinal}",
            )
            require(
                exact_labelled_mixed_payload(atlas, restricted_target) == first_target_payload,
                f"target exact parent restriction:{second_ordinal}",
            )
            require(
                bound["source_parent_mixed_graph_sha256"] == sha(first_source_payload),
                f"source second parent hash:{second_ordinal}",
            )
            require(
                bound["target_parent_mixed_graph_sha256"] == sha(first_target_payload),
                f"target second parent hash:{second_ordinal}",
            )
            if bound["proof"] == "displayed_quartet_mismatch":
                record = quartet_records[bound["certificate_sha256"]]
                require(first_quartet(atlas, second_source, second_target_selected, range(6)) == record, f"second quartet:{second_ordinal}")
            elif bound["proof"] == "full_map_Ti_zero_strict_sign":
                require(first_quartet(atlas, second_source, second_target_selected, range(6)) is None, f"second T has quartet:{second_ordinal}")
                relation = atlas.mixed_relation_exact_prepared(
                    atlas.prepare_mixed_source(second_source), second_target_selected
                )
                require(relation == "none", f"second T graph relation:{second_ordinal}:{relation}")
                exact_relations[relation] += 1
                second_source_descriptor = atlas.model_descriptor_fast2(second_source)
                second_source_outputs = atlas.output_sparse_polynomials(second_source_descriptor)
                verify_t_row(
                    atlas,
                    bound["certificate"],
                    second_source_descriptor,
                    second_source_outputs,
                    second_target_descriptor,
                    second_target_outputs,
                    sign_records,
                    polynomial_registry,
                )
            else:
                raise Failure(f"unknown second proof:{bound['proof']}")
            corrected_second_counts[bound["proof"]] += 1
            parent_use[parent["row_sha256"]] += 1
            second_ordinal += 1

    require(second_ordinal == 256, "second enumeration coverage")
    require(all(value == 8 for value in parent_use.values()) and len(parent_use) == 32, "unique complete parent expansion")
    require(dict(sorted(corrected_second_counts.items())) == certificate["census"]["second_proof_counts"], "second proof census")
    require(exact_relations["none"] == certificate["census"]["exact_graph_relation_none_residuals"] == 818, "exact residual relation census")

    # Every signed polynomial was independently normalized and replayed by the
    # direct Bernstein coefficient formula at its first invoking row.
    require(set(polynomial_registry) == set(sign_records), "sign polynomial coverage")
    for signed_hash, normalized in sorted(polynomial_registry.items()):
        record = sign_records[signed_hash]
        require(sparse_hash(normalized) == record["normalized_negative_pullback_sha256"], "normalized sign registry")

    referenced_algebra = {
        row["certificate_sha256"]
        for row in first_coverage
        if row["proof"] in {
            "exact_multihomogeneous_quadratic",
            "inherited_exact_F_2_112_quartic",
        }
    }
    require(referenced_algebra == set(algebra_records), "algebra certificate coverage")
    require(certificate["census"]["unresolved"] == 0, "unresolved status")
    require(certificate["census"]["missing_children"] == 0, "missing child status")
    require(certificate["census"]["cycles"] == 0 and certificate["census"]["max_depth"] == 2, "forest acyclicity")
    require(certificate["census"]["final_leaves"] == 36_792, "final leaf census")

    report = {
        "schema": "k2p-corrected-restoration-independent-replay-v3",
        "status": "PASS",
        "source_certificate_sha256": sha_file(args.certificate),
        "source_certificate_payload_sha256": payload,
        "source_crosswalk_sha256": sha_file(args.crosswalk),
        "source_crosswalk_payload_sha256": crosswalk_payload,
        "canonical_parents": parent_count,
        "member_roots": len(roots),
        "provenance_first_rows_rehashed": ordinal,
        "provenance_source_graph_classes": len(source_registry.representatives),
        "provenance_target_graph_classes": len(target_registry.representatives),
        "provenance_directed_relation_classes": len(relation_presentations),
        "continuation_parents": len(continuation_states),
        "second_children_replayed": second_ordinal,
        "first_source_parent_transports_replayed": len(source_transport_records),
        "first_target_parent_transports_replayed": len(target_transport_records),
        "first_parent_transport_edges_replayed": ordinal,
        "first_exact_relation_none_replayed": first_exact_relations["none"],
        "second_parent_transport_edges_replayed": second_ordinal,
        "omitted_terminal_member_scope_replayed": len(omitted_terminal_rows),
        "final_leaves": certificate["census"]["final_leaves"],
        "sign_classes_replayed": len(polynomial_registry),
        "algebra_classes_replayed": len(referenced_algebra),
        "exact_physical_witness_checks": len(corrected_algebra_replay),
        "unresolved": 0,
        "missing_children": 0,
        "cycles": 0,
        "runtime_seconds": time.monotonic() - started,
    }
    report["payload_sha256"] = sha(report)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (Failure, AssertionError, KeyError, IndexError, OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"CORRECTED_RESTORATION_REPLAY_FAIL:{error}") from error
