#!/usr/bin/env python3
"""Fail-closed replay of the five-port K2P restoration certificate."""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PACKAGE = REPO / "package/referee/k2p_offline_sweep_portable"
ATLAS_PATH = PACKAGE / "atlas/k2p_atlas_core.py"
QUARTIC_PATH = PACKAGE / "proofs/theta_quartic_obstruction_certificates.json"
GENERATOR = HERE / "enumerate_five_port.py"


class VerificationFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationFailure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha_bytes(value):
    return hashlib.sha256(value).hexdigest()


def sha_file(path):
    return sha_bytes(path.read_bytes())


def sparse_payload(polynomial):
    return [
        [list(exponent), str(coefficient)]
        for exponent, coefficient in sorted(polynomial.items(), key=lambda row: repr(row[0]))
    ]


def sparse_hash(polynomial):
    return sha_bytes(canonical_bytes(sparse_payload(polynomial)))


def load_atlas():
    spec = importlib.util.spec_from_file_location("restoration_verify_atlas", ATLAS_PATH)
    require(spec is not None and spec.loader is not None, "cannot load atlas")
    module = importlib.util.module_from_spec(spec)
    sys.modules["restoration_verify_atlas"] = module
    spec.loader.exec_module(module)
    return module


def insert_source_leaf(atlas, graph, candidate, label):
    result = graph.copy()
    tail, head = ast.literal_eval(candidate["tail"]), ast.literal_eval(candidate["head"])
    require(result.has_edge(tail, head), "transported insertion edge is absent")
    data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    subdivision = ("restoration_subdivision", label, repr(tail), repr(head))
    leaf = ("leaf", "restoration", label)
    result.add_node(subdivision, role="tree", label=None, dummy=False)
    result.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    result.add_edge(tail, subdivision, **data)
    result.add_edge(subdivision, head, **data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    atlas.validate_graph(result)
    return result


def promote_target(atlas, targets, attachment, role, label):
    target_index = attachment["target_index"]
    permutation = tuple(attachment["port_match"])
    result = atlas.relabel_record(targets[target_index], permutation).graph.copy()
    nodes = [node for node, data in result.nodes(data=True) if data.get("dummy_name") == role]
    require(len(nodes) == 1, "restored target role is not unique")
    data = result.nodes[nodes[0]]
    data["label"], data["dummy"], data["dummy_name"] = label, False, None
    return result


def pullback(atlas, polynomial, outputs):
    columns = [
        atlas.sparse_mul_many([outputs[index] for index in monomial])
        for monomial, _ in polynomial
    ]
    return atlas.sparse_lincomb(columns, [coefficient for _, coefficient in polynomial])


def evaluate_sparse(polynomial, point):
    total = Fraction(0)
    for exponent, coefficient in polynomial.items():
        term = Fraction(coefficient)
        for value, power in zip(point, exponent):
            if power:
                term *= value ** power
        total += term
    return total


def coordinate_map(atlas, permutation):
    assignments = atlas.orbit_assignments(4)
    index = {assignment: offset for offset, assignment in enumerate(assignments)}
    return tuple(
        index[
            atlas.ct_orbit_rep(
                tuple(assignment[permutation[position]] for position in range(4))
            )
        ]
        for assignment in assignments
    )


def transform(atlas, polynomial, permutation):
    mapping = coordinate_map(atlas, permutation)
    return tuple(
        (tuple(sorted(mapping[index] for index in monomial)), coefficient)
        for monomial, coefficient in polynomial
    )


def lift(atlas, polynomial, quartet):
    assignments4 = atlas.orbit_assignments(4)
    assignments5 = atlas.orbit_assignments(5)
    index5 = {assignment: offset for offset, assignment in enumerate(assignments5)}
    mapping = []
    for assignment in assignments4:
        lifted = [0] * 5
        for position, label in enumerate(quartet):
            lifted[label] = assignment[position]
        mapping.append(index5[atlas.ct_orbit_rep(tuple(lifted))])
    return tuple(
        (tuple(sorted(mapping[index] for index in monomial)), coefficient)
        for monomial, coefficient in polynomial
    )


def load_f112():
    payload = json.loads(QUARTIC_PATH.read_text())
    row = next(
        item for item in payload["certificates"]
        if (item["source_index"], item["canonical_class_id"]) == (2, 112)
    )
    return tuple((tuple(indices), coefficient) for coefficient, indices in row["terms"])


def verify_strict_witness(atlas, descriptor, pullback_polynomial, stored):
    edge_pairs, lambdas = atlas.default_exact_point(descriptor, stored["salt"])
    require(
        [[str(s), str(g)] for s, g in edge_pairs] == stored["edge_pairs"],
        "strict edge witness drift",
    )
    require([str(value) for value in lambdas] == stored["lambdas"], "lambda witness drift")
    point = tuple(value for pair in edge_pairs for value in pair) + tuple(lambdas)
    value = evaluate_sparse(pullback_polynomial, point)
    require(value != 0 and str(value) == stored["value"], "strict source witness failed")


def verify_algebra_rows(certificate):
    atlas = load_atlas()
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    f112 = load_f112()
    proof_counts = Counter()
    seen = set()
    for row in certificate["algebra_rows"]:
        require(row["status"] == "separated", "algebra row is not separated")
        require(row["row_sha256"] == sha_bytes(canonical_bytes({
            key: value for key, value in row.items() if key != "row_sha256"
        })), "algebra row hash mismatch")
        require(row["root_id"] not in seen, "duplicate algebra root")
        seen.add(row["root_id"])
        source_index = int(row["root_id"].split(":", 1)[0][1:])
        source_graph = insert_source_leaf(
            atlas, sources[source_index].graph, row["source_insertion"], row["restored_label"]
        )
        attachment = row["target_attachment"]
        target_record = targets[attachment["target_index"]]
        expected_remaining = sorted(
            role for role in target_record.dummy_labels if role != row["restored_role"]
        )
        require(expected_remaining == row["remaining_roles"], "remaining-role transport mismatch")
        target_graph = promote_target(
            atlas, targets, attachment, row["restored_role"], row["restored_label"]
        )
        source_descriptor = atlas.model_descriptor_fast2(source_graph)
        target_descriptor = atlas.model_descriptor_fast2(target_graph)
        source_outputs = atlas.output_sparse_polynomials(source_descriptor)
        target_outputs = atlas.output_sparse_polynomials(target_descriptor)

        if row["proof"] == "exact_multihomogeneous_quadratic":
            polynomial = tuple(
                (tuple(pair), coefficient)
                for pair, coefficient in zip(row["coordinate_pairs"], row["coefficients"])
            )
        elif row["proof"] == "inherited_exact_F_2_112_quartic":
            polynomial = tuple(
                (tuple(monomial), coefficient)
                for monomial, coefficient in row["lifted_coordinate_monomials"]
            )
            rebuilt = lift(
                atlas,
                transform(atlas, f112, tuple(row["four_port_coordinate_permutation"])),
                tuple(row["selected_quartet"]),
            )
            require(polynomial == rebuilt, "quartic transport is not F_(2,112)")
        else:
            raise VerificationFailure("unknown algebra proof family")

        target_pullback = pullback(atlas, polynomial, target_outputs)
        source_pullback = pullback(atlas, polynomial, source_outputs)
        require(not target_pullback, "target pullback is nonzero")
        require(source_pullback, "source pullback is zero")
        require(len(source_pullback) == row["source_pullback_term_count"], "source term count")
        require(sparse_hash(source_pullback) == row["source_pullback_sha256"], "source hash")
        witness = row["source_pullback_witness"]
        exponent = tuple(witness["parameter_exponent"])
        require(str(source_pullback.get(exponent, 0)) == witness["coefficient"], "source monomial")
        weights = atlas.coordinate_weights(5)
        degree_rows = {
            tuple(sum(weights[index][slot] for index in monomial) for slot in range(10))
            for monomial, _ in polynomial
        }
        require(degree_rows == {tuple(row["weight"])}, "bridge multidegree mismatch")
        verify_strict_witness(
            atlas, source_descriptor, source_pullback, row["strict_D_plus_witness"]
        )
        proof_counts[row["proof"]] += 1
    require(
        proof_counts == Counter({
            "exact_multihomogeneous_quadratic": 148,
            "inherited_exact_F_2_112_quartic": 16,
        }),
        f"algebra proof census mismatch: {proof_counts}",
    )
    return proof_counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate", type=Path, default=HERE / "five_port_certificate.json"
    )
    parser.add_argument("--skip-regeneration", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    require(__debug__, "verification is disabled under Python -O")
    certificate = json.loads(args.certificate.read_text())
    require(certificate["schema"] == "k2p-restoration-five-port-certificate-v2", "schema")
    stored_payload = certificate["certificate_payload_sha256"]
    body = {key: value for key, value in certificate.items() if key != "certificate_payload_sha256"}
    require(sha_bytes(canonical_bytes(body)) == stored_payload, "certificate payload hash")
    require(sha_file(ATLAS_PATH) == certificate["inputs"]["atlas_sha256"], "atlas hash")
    require(sha_file(QUARTIC_PATH) == certificate["inputs"]["quartic_sha256"], "quartic hash")

    census = certificate["census"]
    expected = {
        "canonical_restoration_parents": 997,
        "member_roots": 2540,
        "member_dummy_multiplicity": {"1": 568, "2": 1260, "3": 712},
        "role_requests": 5224,
        "source_first_insertion_candidates_per_root": 7,
        "raw_five_port_children": 36568,
        "unique_source_children_by_frozen_index": 42,
        "unique_target_promotions_by_frozen_index": 4986,
        "exact_source_mixed_graph_classes": 35,
        "exact_target_mixed_graph_classes": 314,
        "exact_directed_relation_classes": 2240,
        "exact_algebra_descriptor_pairs_tested": 72,
        "status_counts": {"separated": 36568},
        "proof_counts": {
            "displayed_quartet_mismatch": 35758,
            "exact_multihomogeneous_quadratic": 148,
            "inherited_exact_F_2_112_quartic": 16,
            "strict_tree_sunlet_sign": 646,
        },
        "status_by_remaining_role_count": {
            "0:separated": 3976,
            "1:separated": 17640,
            "2:separated": 14952,
        },
    }
    require(census == expected, f"census mismatch: {census}")
    hashes = certificate["ordered_raw_child_hashes"]
    require(len(hashes) == 36568, "raw child hash count")
    require(
        sha_bytes(canonical_bytes(hashes)) == certificate["ordered_raw_child_hash_root"],
        "raw child hash root",
    )
    require(not certificate["unresolved_rows"], "unresolved rows remain")
    require(len(certificate["relation_class_presentation_counts"]) == 2240, "relation classes")
    require(
        sum(certificate["relation_class_presentation_counts"].values()) == 36568,
        "relation presentation coverage",
    )
    require(
        set(map(tuple, certificate["relation_class_statuses"].values())) == {("separated",)},
        "non-separated relation class",
    )
    algebra_counts = verify_algebra_rows(certificate)

    if not args.skip_regeneration:
        with tempfile.TemporaryDirectory(prefix="k2p-restoration-replay-") as directory:
            regenerated = Path(directory) / "five_port_certificate.json"
            completed = subprocess.run(
                [sys.executable, str(GENERATOR), "--output", str(regenerated)],
                cwd=REPO,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            require(completed.returncode == 0, f"regeneration failed: {completed.stderr}")
            require(regenerated.read_bytes() == args.certificate.read_bytes(), "regeneration drift")

    report = {
        "schema": "k2p-restoration-replay-report-v1",
        "status": "PASS",
        "certificate_sha256": sha_file(args.certificate),
        "payload_sha256": stored_payload,
        "raw_children": 36568,
        "canonical_relation_classes": 2240,
        "algebra_proof_counts": dict(sorted(algebra_counts.items())),
        "unresolved": 0,
    }
    if args.output is not None:
        args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationFailure as error:
        print(f"RESTORATION_VERIFY_FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
