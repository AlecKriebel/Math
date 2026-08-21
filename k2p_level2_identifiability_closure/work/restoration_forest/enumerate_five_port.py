#!/usr/bin/env python3
"""Generate and proof-filter every v4 restoration parent's five-port child.

This program only reads the locked v4 release.  It writes one deterministic
JSON certificate under this workspace.  The certificate binds all raw child
transports through a Merkle-style ordered SHA-256 root while retaining each
non-separated/equal-deck row explicitly for subsequent four-port-deck and
forest expansion.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PACKAGE = REPO / "package/referee/k2p_offline_sweep_portable"
ATLAS_PATH = PACKAGE / "atlas/k2p_atlas_core.py"
RESULT_ROOT = PACKAGE / "results/four_port_release_v4"
QUARTIC_PATH = PACKAGE / "proofs/theta_quartic_obstruction_certificates.json"


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def sparse_payload(polynomial):
    return [
        [list(exponent), str(coefficient)]
        for exponent, coefficient in sorted(polynomial.items(), key=lambda row: repr(row[0]))
    ]


def sparse_hash(polynomial) -> str:
    return sha_bytes(canonical_bytes(sparse_payload(polynomial)))


def load_atlas():
    spec = importlib.util.spec_from_file_location("restoration_atlas", ATLAS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {ATLAS_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["restoration_atlas"] = module
    spec.loader.exec_module(module)
    return module


def source_insertion_candidates(graph):
    rows = []
    for tail, head, data in sorted(
        graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
    ):
        if graph.nodes[head].get("role") == "leaf":
            continue
        if graph.nodes[tail].get("role") == "root":
            continue
        rows.append(
            {"tail": repr(tail), "head": repr(head), "edge_role": data.get("edge_role")}
        )
    return rows


def insert_source_leaf(atlas, graph, candidate, label: int):
    result = graph.copy()
    tail = ast.literal_eval(candidate["tail"])
    head = ast.literal_eval(candidate["head"])
    if not result.has_edge(tail, head):
        raise AssertionError(("missing insertion edge", candidate))
    edge_data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    subdivision = ("restoration_subdivision", label, repr(tail), repr(head))
    leaf = ("leaf", "restoration", label)
    if subdivision in result or leaf in result:
        raise AssertionError(("node collision", subdivision, leaf))
    result.add_node(subdivision, role="tree", label=None, dummy=False)
    result.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    result.add_edge(tail, subdivision, **edge_data)
    result.add_edge(subdivision, head, **edge_data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    atlas.validate_graph(result)
    return result


def promoted_target(atlas, targets, target_index, permutation, role, label: int):
    result = atlas.relabel_record(targets[target_index], tuple(permutation)).graph.copy()
    nodes = [n for n, data in result.nodes(data=True) if data.get("dummy_name") == role]
    if len(nodes) != 1:
        raise AssertionError((target_index, permutation, role, nodes))
    data = result.nodes[nodes[0]]
    data["label"] = label
    data["dummy"] = False
    data["dummy_name"] = None
    selected = atlas.restrict_rooted(result, set(range(label + 1)))
    return result, selected


def serialize_split_set(value):
    def key(item):
        return repr(item)

    answer = []
    for item in sorted(value, key=key):
        if item == ("star",):
            answer.append(["star"])
        else:
            answer.append([list(item[0]), list(item[1])])
    return answer


def proof_first_topology(atlas, source_graph, target_graph):
    labels = tuple(
        sorted(
            data["label"]
            for _, data in source_graph.nodes(data=True)
            if isinstance(data.get("label"), int)
        )
    )
    target_labels = tuple(
        sorted(
            data["label"]
            for _, data in target_graph.nodes(data=True)
            if isinstance(data.get("label"), int)
        )
    )
    if labels != target_labels:
        raise AssertionError((labels, target_labels))
    for quartet in itertools.combinations(labels, 4):
        source_splits = atlas.quartet_splits(source_graph, quartet)
        target_splits = atlas.quartet_splits(target_graph, quartet)
        if source_splits != target_splits:
            return {
                "status": "separated",
                "proof": "displayed_quartet_mismatch",
                "labels": list(quartet),
                "source_splits": serialize_split_set(source_splits),
                "target_splits": serialize_split_set(target_splits),
            }
    for triple in itertools.combinations(labels, 3):
        source_type = atlas.triple_type(source_graph, triple)
        target_type = atlas.triple_type(target_graph, triple)
        if {source_type, target_type} == {"tree", "sunlet"}:
            return {
                "status": "separated",
                "proof": "strict_tree_sunlet_sign",
                "labels": list(triple),
                "source_type": source_type,
                "target_type": target_type,
            }
    return {"status": "equal_topology_deck", "proof": None}


def exact_graph_matcher(atlas, left, right):
    node_match = lambda x, y: x.get("kind") == y.get("kind") and x.get("label") == y.get("label")
    edge_match = lambda x, y: x.get("head") == y.get("head")
    return atlas.nx.algorithms.isomorphism.GraphMatcher(
        left, right, node_match=node_match, edge_match=edge_match
    ).is_isomorphic()


class MixedGraphRegistry:
    """WL-bucketed, exact incidence-graph canonical deduplication.

    The WL digest is only an acceleration bucket.  Class membership always
    requires the corrected exact incidence-graph isomorphism test.
    """

    def __init__(self, atlas):
        self.atlas = atlas
        self.buckets = defaultdict(list)
        self.representatives = []

    def add(self, graph):
        mixed = self.atlas.sd0_mixed(graph)
        incidence = self.atlas.mixed_incidence_graph(mixed)
        for _, data in incidence.nodes(data=True):
            data["wl_color"] = f"{data.get('kind')}|{data.get('label')!r}"
        for _, _, data in incidence.edges(data=True):
            data["wl_head"] = "1" if data.get("head") else "0"
        bucket = self.atlas.nx.weisfeiler_lehman_graph_hash(
            incidence, node_attr="wl_color", edge_attr="wl_head", iterations=8
        )
        for class_id in self.buckets[bucket]:
            if exact_graph_matcher(self.atlas, self.representatives[class_id], incidence):
                return class_id
        class_id = len(self.representatives)
        self.representatives.append(incidence)
        self.buckets[bucket].append(class_id)
        return class_id


def evaluate_sparse_at_point(polynomial, point):
    total = Fraction(0)
    for exponent, coefficient in polynomial.items():
        term = Fraction(coefficient)
        for value, power in zip(point, exponent):
            if power:
                term *= value ** power
        total += term
    return total


def strict_source_witness(atlas, descriptor, source_pullback):
    for salt in range(32):
        edge_pairs, lambdas = atlas.default_exact_point(descriptor, salt)
        point = tuple(value for pair in edge_pairs for value in pair) + tuple(lambdas)
        value = evaluate_sparse_at_point(source_pullback, point)
        if value:
            return {
                "salt": salt,
                "edge_pairs": [[str(s), str(g)] for s, g in edge_pairs],
                "lambdas": [str(value) for value in lambdas],
                "value": str(value),
            }
    raise AssertionError("fixed strict-point deck missed a nonzero pullback")


def quadratic_certificate(atlas, source_descriptor, target_descriptor):
    separator = atlas.quadratic_separator_fast(
        source_descriptor, target_descriptor, max_block_size=16
    )
    if separator is None:
        return None
    target_outputs = atlas.output_sparse_polynomials(target_descriptor)
    target_columns = [
        atlas.sparse_mul(target_outputs[i], target_outputs[j])
        for i, j in separator["coordinate_pairs"]
    ]
    if atlas.sparse_lincomb(target_columns, separator["coefficients"]):
        raise AssertionError("quadratic target pullback is nonzero")
    source_pullback = separator["source_pullback"]
    witness_exponent, witness_coefficient = next(
        iter(sorted(source_pullback.items(), key=lambda row: repr(row[0])))
    )
    return {
        "status": "separated",
        "proof": "exact_multihomogeneous_quadratic",
        "degree": 2,
        "weight": list(separator["weight"]),
        "coordinate_pairs": [list(pair) for pair in separator["coordinate_pairs"]],
        "coefficients": list(separator["coefficients"]),
        "target_pullback_term_count": 0,
        "source_pullback_term_count": len(source_pullback),
        "source_pullback_sha256": sparse_hash(source_pullback),
        "source_pullback_witness": {
            "parameter_exponent": list(witness_exponent),
            "coefficient": str(witness_coefficient),
        },
        "strict_D_plus_witness": strict_source_witness(
            atlas, source_descriptor, source_pullback
        ),
    }


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


def transform_polynomial(atlas, polynomial, permutation):
    mapping = coordinate_map(atlas, permutation)
    return tuple(
        (tuple(sorted(mapping[index] for index in monomial)), coefficient)
        for monomial, coefficient in polynomial
    )


def lift_four_port_polynomial(atlas, polynomial, quartet):
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


def polynomial_pullback(atlas, polynomial, outputs):
    columns = [
        atlas.sparse_mul_many([outputs[index] for index in monomial])
        for monomial, _ in polynomial
    ]
    return atlas.sparse_lincomb(columns, [coefficient for _, coefficient in polynomial])


def load_f112_quartic():
    payload = json.loads(QUARTIC_PATH.read_text())
    row = next(
        item
        for item in payload["certificates"]
        if (item["source_index"], item["canonical_class_id"]) == (2, 112)
    )
    return tuple((tuple(indices), coefficient) for coefficient, indices in row["terms"])


def inherited_quartic_certificate(atlas, source_descriptor, target_descriptor, base):
    source_outputs = atlas.output_sparse_polynomials(source_descriptor)
    target_outputs = atlas.output_sparse_polynomials(target_descriptor)
    for quartet in itertools.combinations(range(5), 4):
        for permutation in itertools.permutations(range(4)):
            transported = transform_polynomial(atlas, base, permutation)
            lifted = lift_four_port_polynomial(atlas, transported, quartet)
            target_pullback = polynomial_pullback(atlas, lifted, target_outputs)
            if target_pullback:
                continue
            source_pullback = polynomial_pullback(atlas, lifted, source_outputs)
            if not source_pullback:
                continue
            witness_exponent, witness_coefficient = next(
                iter(sorted(source_pullback.items(), key=lambda row: repr(row[0])))
            )
            weights = atlas.coordinate_weights(5)
            degree_rows = {
                tuple(
                    sum(weights[index][slot] for index in monomial)
                    for slot in range(10)
                )
                for monomial, _ in lifted
            }
            if len(degree_rows) != 1:
                raise AssertionError("lifted quartic is not bridge multihomogeneous")
            return {
                "status": "separated",
                "proof": "inherited_exact_F_2_112_quartic",
                "degree": 4,
                "selected_quartet": list(quartet),
                "four_port_coordinate_permutation": list(permutation),
                "lifted_coordinate_monomials": [
                    [list(monomial), coefficient] for monomial, coefficient in lifted
                ],
                "weight": list(next(iter(degree_rows))),
                "target_pullback_term_count": 0,
                "source_pullback_term_count": len(source_pullback),
                "source_pullback_sha256": sparse_hash(source_pullback),
                "source_pullback_witness": {
                    "parameter_exponent": list(witness_exponent),
                    "coefficient": str(witness_coefficient),
                },
                "strict_D_plus_witness": strict_source_witness(
                    atlas, source_descriptor, source_pullback
                ),
            }
    return None


def reconstruct_roots(atlas, sources, targets):
    roots = []
    manifest_hashes = {}
    canonical_parent_count = 0
    for path in sorted(RESULT_ROOT.glob("source_*/residual_manifest.json")):
        manifest_hashes[str(path.relative_to(PACKAGE))] = sha_file(path)
        manifest = json.loads(path.read_text())
        source_index = manifest["source_index"]
        expected_candidates = source_insertion_candidates(sources[source_index].graph)
        for record in manifest["records"]:
            if record["status"] != "restoration_parent":
                continue
            canonical_parent_count += 1
            attachments = defaultdict(dict)
            frozen_candidates = None
            for request in record["child_requests"]:
                candidates = request["source_insertion_edge_candidates"]
                if frozen_candidates is None:
                    frozen_candidates = candidates
                if candidates != frozen_candidates or candidates != expected_candidates:
                    raise AssertionError((source_index, record["canonical_class_id"], "candidate drift"))
                role = request["omitted_role"]
                for attachment in request["target_dummy_attachments"]:
                    key = (attachment["target_index"], tuple(attachment["port_match"]))
                    previous = attachments[key].get(role)
                    if previous is not None and previous != attachment:
                        raise AssertionError(("attachment conflict", key, role))
                    attachments[key][role] = attachment
            if frozen_candidates is None:
                raise AssertionError("restoration parent without requests")
            for (target_index, permutation), by_role in sorted(attachments.items()):
                roles = tuple(sorted(by_role))
                if roles != tuple(targets[target_index].dummy_labels):
                    raise AssertionError(
                        (source_index, record["canonical_class_id"], target_index, roles,
                         targets[target_index].dummy_labels)
                    )
                root_id = (
                    f"s{source_index}:c{record['canonical_class_id']}:t{target_index}:p"
                    + "".join(map(str, permutation))
                )
                roots.append(
                    {
                        "root_id": root_id,
                        "source_index": source_index,
                        "canonical_class_id": record["canonical_class_id"],
                        "target_index": target_index,
                        "port_match": list(permutation),
                        "dummy_roles": list(roles),
                        "attachments": by_role,
                        "source_insertion_edge_candidates": frozen_candidates,
                    }
                )
    if canonical_parent_count != 997:
        raise AssertionError(canonical_parent_count)
    return roots, manifest_hashes, canonical_parent_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=HERE / "five_port_certificate.json"
    )
    args = parser.parse_args()

    atlas = load_atlas()
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    roots, manifest_hashes, canonical_parent_count = reconstruct_roots(atlas, sources, targets)

    source_cache = {}
    target_cache = {}
    source_descriptor_cache = {}
    target_descriptor_cache = {}
    algebra_cache = {}
    source_registry = MixedGraphRegistry(atlas)
    target_registry = MixedGraphRegistry(atlas)
    source_mixed_classes = {}
    target_mixed_classes = {}
    relation_presentations = Counter()
    relation_statuses = defaultdict(set)
    counts = Counter()
    proof_counts = Counter()
    counts_by_remaining = Counter()
    algebra_rows = []
    unresolved_rows = []
    ordered_row_hashes = []
    f112 = load_f112_quartic()

    for root in roots:
        source_index = root["source_index"]
        target_index = root["target_index"]
        permutation = tuple(root["port_match"])
        roles = tuple(root["dummy_roles"])
        for role in roles:
            target_key = (target_index, permutation, role)
            if target_key not in target_cache:
                target_cache[target_key] = promoted_target(
                    atlas, targets, target_index, permutation, role, 4
                )
            target_full, target_selected = target_cache[target_key]
            if target_key not in target_mixed_classes:
                target_mixed_classes[target_key] = target_registry.add(target_selected)
            for insertion_index, candidate in enumerate(root["source_insertion_edge_candidates"]):
                source_key = (source_index, insertion_index)
                if source_key not in source_cache:
                    source_cache[source_key] = insert_source_leaf(
                        atlas, sources[source_index].graph, candidate, 4
                    )
                source_graph = source_cache[source_key]
                if source_key not in source_mixed_classes:
                    source_mixed_classes[source_key] = source_registry.add(source_graph)
                result = proof_first_topology(atlas, source_graph, target_selected)
                remaining = len(roles) - 1
                if result["status"] == "equal_topology_deck":
                    if source_key not in source_descriptor_cache:
                        source_descriptor_cache[source_key] = atlas.model_descriptor_fast2(source_graph)
                    if target_key not in target_descriptor_cache:
                        target_descriptor_cache[target_key] = atlas.model_descriptor_fast2(target_full)
                    source_descriptor = source_descriptor_cache[source_key]
                    target_descriptor = target_descriptor_cache[target_key]
                    algebra_key = (source_descriptor, target_descriptor)
                    if algebra_key not in algebra_cache:
                        proof = quadratic_certificate(atlas, source_descriptor, target_descriptor)
                        if proof is None:
                            proof = inherited_quartic_certificate(
                                atlas, source_descriptor, target_descriptor, f112
                            )
                        algebra_cache[algebra_key] = proof
                    if algebra_cache[algebra_key] is not None:
                        result = algebra_cache[algebra_key]
                    elif remaining == 0:
                        relation = atlas.mixed_relation_exact(source_graph, target_selected)
                        if relation == "isomorphic":
                            result = {"status": "isomorphic", "proof": "exact_labelled_mixed_graph"}
                        elif relation == "triangle":
                            result = {"status": "triangle", "proof": "ordinary_triangle_quotient"}
                source_class = source_mixed_classes[source_key]
                target_class = target_mixed_classes[target_key]
                row = {
                    "root_id": root["root_id"],
                    "restored_role": role,
                    "restored_label": 4,
                    "remaining_roles": [item for item in roles if item != role],
                    "source_insertion_index": insertion_index,
                    "source_insertion": candidate,
                    "target_attachment": root["attachments"][role],
                    "source_mixed_class": source_class,
                    "target_mixed_class": target_class,
                    **result,
                }
                row_hash = sha_bytes(canonical_bytes(row))
                ordered_row_hashes.append(row_hash)
                counts[row["status"]] += 1
                proof_counts[row["proof"] or row["status"]] += 1
                counts_by_remaining[(remaining, row["status"])] += 1
                relation_key = (source_class, target_class)
                relation_presentations[relation_key] += 1
                relation_statuses[relation_key].add(row["status"])
                if row["proof"] in {
                    "exact_multihomogeneous_quadratic",
                    "inherited_exact_F_2_112_quartic",
                }:
                    algebra_rows.append({**row, "row_sha256": row_hash})
                if row["status"] not in {"separated", "isomorphic", "triangle"}:
                    unresolved_rows.append({**row, "row_sha256": row_hash})

    multiplicity = Counter(len(root["dummy_roles"]) for root in roots)
    expected_raw = sum(len(root["dummy_roles"]) * 7 for root in roots)
    if len(ordered_row_hashes) != expected_raw or expected_raw != 36568:
        raise AssertionError((len(ordered_row_hashes), expected_raw))
    expected_proofs = {
        "displayed_quartet_mismatch": 35758,
        "strict_tree_sunlet_sign": 646,
        "exact_multihomogeneous_quadratic": 148,
        "inherited_exact_F_2_112_quartic": 16,
    }
    if counts != Counter({"separated": 36568}):
        raise AssertionError(("nonterminal five-port child", counts))
    if proof_counts != Counter(expected_proofs):
        raise AssertionError(("proof census drift", proof_counts))
    if unresolved_rows:
        raise AssertionError(("unresolved five-port children", len(unresolved_rows)))
    if any(statuses != {"separated"} for statuses in relation_statuses.values()):
        raise AssertionError("a canonical directed relation class has non-separated status")
    certificate = {
        "schema": "k2p-restoration-five-port-certificate-v2",
        "scope": (
            "Complete raw five-port child expansion with exact topology, quadratic, and "
            "inherited-quartic separation certificates; this finite certificate does not "
            "by itself prove the marginal-restoration implication or final K2P theorem."
        ),
        "inputs": {
            "atlas_path": str(ATLAS_PATH.relative_to(REPO)),
            "atlas_sha256": sha_file(ATLAS_PATH),
            "quartic_path": str(QUARTIC_PATH.relative_to(REPO)),
            "quartic_sha256": sha_file(QUARTIC_PATH),
            "manifest_sha256": manifest_hashes,
        },
        "census": {
            "canonical_restoration_parents": canonical_parent_count,
            "member_roots": len(roots),
            "member_dummy_multiplicity": {str(k): v for k, v in sorted(multiplicity.items())},
            "role_requests": sum(len(root["dummy_roles"]) for root in roots),
            "source_first_insertion_candidates_per_root": 7,
            "raw_five_port_children": len(ordered_row_hashes),
            "unique_source_children_by_frozen_index": len(source_cache),
            "unique_target_promotions_by_frozen_index": len(target_cache),
            "exact_source_mixed_graph_classes": len(source_registry.representatives),
            "exact_target_mixed_graph_classes": len(target_registry.representatives),
            "exact_directed_relation_classes": len(relation_presentations),
            "exact_algebra_descriptor_pairs_tested": len(algebra_cache),
            "status_counts": dict(sorted(counts.items())),
            "proof_counts": dict(sorted(proof_counts.items())),
            "status_by_remaining_role_count": {
                f"{remaining}:{status}": value
                for (remaining, status), value in sorted(counts_by_remaining.items())
            },
        },
        "ordered_raw_child_hash_root": sha_bytes(canonical_bytes(ordered_row_hashes)),
        "ordered_raw_child_hashes": ordered_row_hashes,
        "relation_class_presentation_counts": {
            f"{source}:{target}": count
            for (source, target), count in sorted(relation_presentations.items())
        },
        "relation_class_statuses": {
            f"{source}:{target}": sorted(relation_statuses[(source, target)])
            for source, target in sorted(relation_statuses)
        },
        "algebra_rows": algebra_rows,
        "unresolved_rows": unresolved_rows,
    }
    payload_hash = sha_bytes(canonical_bytes(certificate))
    certificate["certificate_payload_sha256"] = payload_hash
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), **certificate["census"], "payload": payload_hash}, sort_keys=True))


if __name__ == "__main__":
    main()
