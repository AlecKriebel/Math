#!/usr/bin/env python3
"""Generate the complete fixed-full three-port cycle closure package."""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import time
from fractions import Fraction
from pathlib import Path

from cycle_common import (
    DEFAULT_ARTIFACT_ROOT,
    DEFAULT_PACKAGE_ROOT,
    atomic_json,
    canonical_json_bytes,
    canonicalizer_sha256,
    descriptor_sha256,
    deterministic_gzip,
    exact_transport_records,
    fail,
    insert_source_leaf,
    load_atlas,
    relabel_and_promote_all,
    sha_file,
    sha_object,
    source_insertion_candidates,
    topology_decision,
    witness_id,
)
EXPECTED_BASE = collections.Counter(
    {
        "tree_sunlet_pointwise_excluded": 7452,
        "restoration_root": 5964,
        "triangle": 16,
        "isomorphic": 8,
    }
)
EXPECTED_ROOT_MULTIPLICITY = collections.Counter({1: 324, 2: 1896, 3: 2784, 4: 960})
EXPECTED_FULL = collections.Counter(
    {
        "quartet_pointwise_excluded": 535920,
        "tree_sunlet_pointwise_excluded": 300,
        "quadratic_separated": 132,
        "isomorphic": 12,
    }
)


def json_line(value) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def strict_source_witness(atlas, descriptor, polynomial):
    for salt in range(32):
        edge_pairs, lambdas = atlas.default_exact_point(descriptor, salt)
        point = tuple(value for pair in edge_pairs for value in pair) + tuple(lambdas)
        value = Fraction(0)
        for exponent, coefficient in polynomial.items():
            term = Fraction(coefficient)
            for coordinate, power in zip(point, exponent):
                if power:
                    term *= coordinate**power
            value += term
        if value:
            return {
                "salt": salt,
                "edge_pairs": [[str(s), str(g)] for s, g in edge_pairs],
                "lambdas": [str(inheritance) for inheritance in lambdas],
                "value": str(value),
            }
    fail("CYCLE_STRICT_WITNESS_FAIL")


def sparse_hash(polynomial) -> str:
    rows = [
        [list(exponent), str(coefficient)]
        for exponent, coefficient in sorted(polynomial.items())
    ]
    return sha_object(rows)


def build_source_configurations(atlas, sources):
    configurations = {}
    for source_index, source in enumerate(sources):
        states = [
            {
                "placement_path": [],
                "insertions": [],
                "graph": source.graph,
                "signature": atlas.topology_signature(source.graph),
            }
        ]
        for depth in range(1, 5):
            label = 2 + depth
            children = []
            for parent in states:
                candidates = source_insertion_candidates(parent["graph"])
                if len(candidates) != 2 + depth:
                    fail(
                        "CYCLE_SOURCE_CANDIDATE_CENSUS_FAIL",
                        (source_index, depth, len(candidates)),
                    )
                for insertion_index, candidate in enumerate(candidates):
                    graph = insert_source_leaf(atlas, parent["graph"], candidate, label)
                    children.append(
                        {
                            "placement_path": parent["placement_path"] + [insertion_index],
                            "insertions": parent["insertions"] + [candidate],
                            "graph": graph,
                            "signature": atlas.topology_signature(graph),
                        }
                    )
            states = children
            configurations[(source_index, depth)] = states
    expected = {1: 3, 2: 12, 3: 60, 4: 360}
    for source_index in range(len(sources)):
        for depth, count in expected.items():
            if len(configurations[(source_index, depth)]) != count:
                fail(
                    "CYCLE_SOURCE_CONFIGURATION_CENSUS_FAIL",
                    (source_index, depth, len(configurations[(source_index, depth)])),
                )
    return configurations


def generate_base(atlas, sources, targets, permutations, state):
    source_signatures = [atlas.topology_signature(source.graph) for source in sources]
    target_signatures = [
        atlas.topology_signature(atlas.selected_graph_from_completion(target))
        for target in targets
    ]
    raw_id = 0
    for source_index, source in enumerate(sources):
        for target_index, target in enumerate(targets):
            for permutation_index, permutation in enumerate(permutations):
                permuted = atlas.permute_signature(
                    target_signatures[target_index], permutation
                )
                content = topology_decision(
                    source_signatures[source_index],
                    (source_signatures[source_index][0], permuted[0], permuted[1]),
                )
                certificate_id = None
                if content is not None:
                    if content["reason"] != "tree_sunlet_strict_sign":
                        fail("CYCLE_BASE_UNEXPECTED_QUARTET", content)
                    category = "tree_sunlet_pointwise_excluded"
                    certificate_id = witness_id(content)
                    state["topology_witnesses"].setdefault(certificate_id, content)
                elif target.dummy_labels:
                    category = "restoration_root"
                else:
                    target_graph = atlas.relabel_record(target, permutation).graph
                    relation = atlas.mixed_relation_exact(source.graph, target_graph)
                    if relation not in {"isomorphic", "triangle"}:
                        fail(
                            "CYCLE_BASE_UNRESOLVED",
                            (source_index, target_index, permutation_index, relation),
                        )
                    category = relation
                    transports = exact_transport_records(
                        atlas, source.graph, target_graph, relation
                    )
                    if len(transports) != 1:
                        fail("CYCLE_BASE_TRANSPORT_MULTIPLICITY", len(transports))
                    transport = transports[0]
                    certificate_id = f"TR:{sha_object(transport)}"
                    state["transport_certificates"].setdefault(
                        certificate_id, transport
                    )
                    state["physical_anchors"].append(
                        {
                            "anchor_id": f"A3:{raw_id}",
                            "origin": "base_no_dummy",
                            "port_count": 3,
                            "base_raw_id": raw_id,
                            "source_index": source_index,
                            "target_index": target_index,
                            "permutation_index": permutation_index,
                            "port_permutation": list(permutation),
                            "relation": relation,
                            "transport_certificate_id": certificate_id,
                        }
                    )
                row = {
                    "raw_id": raw_id,
                    "source_index": source_index,
                    "target_index": target_index,
                    "permutation_index": permutation_index,
                    "port_permutation": list(permutation),
                    "dummy_roles": list(target.dummy_labels),
                    "category": category,
                    "certificate_id": certificate_id,
                }
                state["base_counts"][category] += 1
                if category == "restoration_root":
                    root_content = {
                        "base_raw_id": raw_id,
                        "source_index": source_index,
                        "target_index": target_index,
                        "permutation_index": permutation_index,
                        "port_permutation": list(permutation),
                        "dummy_roles": list(target.dummy_labels),
                    }
                    root_content["root_id"] = f"R:{sha_object(root_content)}"
                    state["roots"].append(root_content)
                    state["root_multiplicity"][len(target.dummy_labels)] += 1
                yield json_line(row)
                raw_id += 1


def generate_roots(state):
    for row in state["roots"]:
        yield json_line(row)


def four_port_rank_digest(descriptor) -> str:
    payload = json.dumps(
        [
            descriptor.k,
            descriptor.retic_count,
            descriptor.edge_class_count,
            descriptor.outputs,
            descriptor.edge_signatures,
        ],
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def rank_witness(atlas, descriptor, digest, cache, coverage_index):
    if digest not in cache:
        coverage_digest = four_port_rank_digest(descriptor)
        coverage = coverage_index.get(coverage_digest)
        lower_candidates = [
            atlas.rank_certificate(descriptor, salt=salt) for salt in range(8)
        ]
        lower = max(lower_candidates, key=lambda row: int(row["rank"]))
        cache[digest] = {
            "descriptor_sha256": digest,
            "four_port_rank_descriptor_sha256": coverage_digest,
            "witnessed_jacobian_rank": int(lower["rank"]),
            "lower_point_salts_checked": 8,
            "lower_certificate": lower,
            "external_exact_rank_coverage_row": coverage,
        }
    return cache[digest]


def quadratic_certificate(atlas, source_descriptor, target_descriptor, state):
    source_digest = descriptor_sha256(source_descriptor)
    target_digest = descriptor_sha256(target_descriptor)
    pair_content = {
        "source_descriptor_sha256": source_digest,
        "target_descriptor_sha256": target_digest,
    }
    certificate_id = f"QD:{sha_object(pair_content)}"
    if certificate_id in state["quadratic_certificates"]:
        return certificate_id
    separator = atlas.quadratic_separator_fast(
        source_descriptor, target_descriptor, max_block_size=16
    )
    if separator is None:
        fail("CYCLE_QUADRATIC_MISSING", pair_content)
    target_outputs = atlas.output_sparse_polynomials(target_descriptor)
    target_columns = [
        atlas.sparse_mul(target_outputs[left], target_outputs[right])
        for left, right in separator["coordinate_pairs"]
    ]
    if atlas.sparse_lincomb(target_columns, separator["coefficients"]):
        fail("CYCLE_QUADRATIC_TARGET_NONZERO", certificate_id)
    source_pullback = separator["source_pullback"]
    if not source_pullback:
        fail("CYCLE_QUADRATIC_SOURCE_ZERO", certificate_id)
    source_rank = rank_witness(
        atlas,
        source_descriptor,
        source_digest,
        state["rank_certificates"],
        state["rank_coverage_index"],
    )
    target_rank = rank_witness(
        atlas,
        target_descriptor,
        target_digest,
        state["rank_certificates"],
        state["rank_coverage_index"],
    )
    certificate = {
        "certificate_id": certificate_id,
        **pair_content,
        "degree": 2,
        "weight": list(separator["weight"]),
        "coordinate_pairs": [list(pair) for pair in separator["coordinate_pairs"]],
        "coefficients": list(separator["coefficients"]),
        "target_pullback_term_count": 0,
        "source_pullback_term_count": len(source_pullback),
        "source_pullback_sha256": sparse_hash(source_pullback),
        "strict_D_plus_witness": strict_source_witness(
            atlas, source_descriptor, source_pullback
        ),
        "source_witnessed_jacobian_rank": source_rank["witnessed_jacobian_rank"],
        "target_witnessed_jacobian_rank": target_rank["witnessed_jacobian_rank"],
    }
    state["quadratic_certificates"][certificate_id] = certificate
    return certificate_id


def generate_full(atlas, sources, targets, permutations, configurations, state):
    descriptor_cache = {}
    raw_id = 0
    for root in state["roots"]:
        source_index = root["source_index"]
        target_index = root["target_index"]
        permutation_index = root["permutation_index"]
        roles = tuple(root["dummy_roles"])
        depth = len(roles)
        target_graph = relabel_and_promote_all(
            atlas, targets[target_index], permutations[permutation_index], roles
        )
        target_signature = atlas.topology_signature(target_graph)
        for configuration in configurations[(source_index, depth)]:
            source_graph = configuration["graph"]
            content = topology_decision(configuration["signature"], target_signature)
            if content is not None:
                certificate_id = witness_id(content)
                previous = state["topology_witnesses"].setdefault(
                    certificate_id, content
                )
                if previous != content:
                    fail("CYCLE_TOPOLOGY_WITNESS_COLLISION", certificate_id)
                category = (
                    "quartet_pointwise_excluded"
                    if content["reason"] == "displayed_quartet_mismatch"
                    else "tree_sunlet_pointwise_excluded"
                )
            else:
                relation = atlas.mixed_relation_exact(source_graph, target_graph)
                if relation == "isomorphic":
                    category = "isomorphic"
                    transports = exact_transport_records(
                        atlas, source_graph, target_graph, relation
                    )
                    if len(transports) != 1:
                        fail("CYCLE_FULL_TRANSPORT_MULTIPLICITY", len(transports))
                    transport = transports[0]
                    certificate_id = f"TR:{sha_object(transport)}"
                    state["transport_certificates"].setdefault(
                        certificate_id, transport
                    )
                    state["physical_anchors"].append(
                        {
                            "anchor_id": f"AF:{raw_id}",
                            "origin": "fixed_full_restoration",
                            "port_count": 3 + depth,
                            "full_raw_id": raw_id,
                            "root_id": root["root_id"],
                            "base_raw_id": root["base_raw_id"],
                            "source_index": source_index,
                            "target_index": target_index,
                            "permutation_index": permutation_index,
                            "port_permutation": list(permutations[permutation_index]),
                            "dummy_roles_in_label_order": list(roles),
                            "source_placement_path": configuration["placement_path"],
                            "relation": relation,
                            "transport_certificate_id": certificate_id,
                        }
                    )
                elif relation in {None, "none"}:
                    category = "quadratic_separated"
                    source_key = (
                        source_index,
                        depth,
                        tuple(configuration["placement_path"]),
                    )
                    if source_key not in descriptor_cache:
                        descriptor_cache[source_key] = atlas.model_descriptor_fast2(
                            source_graph
                        )
                    target_key = (
                        "target",
                        target_index,
                        permutation_index,
                        roles,
                    )
                    if target_key not in descriptor_cache:
                        descriptor_cache[target_key] = atlas.model_descriptor_fast2(
                            target_graph
                        )
                    certificate_id = quadratic_certificate(
                        atlas,
                        descriptor_cache[source_key],
                        descriptor_cache[target_key],
                        state,
                    )
                    state["quadratic_multiplicity"][certificate_id] += 1
                else:
                    fail(
                        "CYCLE_FULL_UNEXPECTED_RELATION",
                        (root["root_id"], configuration["placement_path"], relation),
                    )
            row = {
                "raw_id": raw_id,
                "root_id": root["root_id"],
                "base_raw_id": root["base_raw_id"],
                "source_index": source_index,
                "target_index": target_index,
                "permutation_index": permutation_index,
                "dummy_roles_in_label_order": list(roles),
                "port_count": 3 + depth,
                "source_placement_path": configuration["placement_path"],
                "category": category,
                "certificate_id": certificate_id,
            }
            state["full_counts"][category] += 1
            yield json_line(row)
            raw_id += 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, default=DEFAULT_PACKAGE_ROOT)
    parser.add_argument("--artifact-root", type=Path, default=DEFAULT_ARTIFACT_ROOT)
    args = parser.parse_args()
    started = time.time()
    atlas = load_atlas(args.package_root)
    sources = tuple(atlas.source_supports(core_ids=("cycle",)))
    targets = tuple(
        atlas.target_completions(3, True) + atlas.target_completions(3, False)
    )
    permutations = tuple(itertools.permutations(range(3)))
    if (len(sources), len(targets), len(permutations)) != (2, 1120, 6):
        fail("CYCLE_PRIMITIVE_CENSUS_FAIL", (len(sources), len(targets), len(permutations)))
    artifact_root = args.artifact_root
    artifact_root.mkdir(parents=True, exist_ok=True)
    rank_coverage_path = (
        Path(__file__).resolve().parents[1]
        / "rank_upper_certificates/rank_upper_coverage.json"
    )
    rank_coverage = json.loads(rank_coverage_path.read_text())
    rank_coverage_index = {
        row["descriptor_sha256"]: row for row in rank_coverage["descriptors"]
    }
    state = {
        "base_counts": collections.Counter(),
        "full_counts": collections.Counter(),
        "root_multiplicity": collections.Counter(),
        "roots": [],
        "topology_witnesses": {},
        "transport_certificates": {},
        "physical_anchors": [],
        "quadratic_certificates": {},
        "quadratic_multiplicity": collections.Counter(),
        "rank_certificates": {},
        "rank_coverage_index": rank_coverage_index,
    }
    base_path = artifact_root / "base_raw_ledger.jsonl.gz"
    base_meta = deterministic_gzip(
        base_path, generate_base(atlas, sources, targets, permutations, state)
    )
    if state["base_counts"] != EXPECTED_BASE:
        fail("CYCLE_BASE_CENSUS_FAIL", dict(state["base_counts"]))
    if state["root_multiplicity"] != EXPECTED_ROOT_MULTIPLICITY:
        fail("CYCLE_ROOT_MULTIPLICITY_FAIL", dict(state["root_multiplicity"]))
    roots_path = artifact_root / "restoration_roots.jsonl.gz"
    roots_meta = deterministic_gzip(roots_path, generate_roots(state))
    configurations = build_source_configurations(atlas, sources)
    full_path = artifact_root / "full_completion_ledger.jsonl.gz"
    full_meta = deterministic_gzip(
        full_path,
        generate_full(atlas, sources, targets, permutations, configurations, state),
    )
    if state["full_counts"] != EXPECTED_FULL:
        fail("CYCLE_FULL_CENSUS_FAIL", dict(state["full_counts"]))
    if len(state["quadratic_certificates"]) != 54:
        fail("CYCLE_QUADRATIC_CLASS_CENSUS_FAIL", len(state["quadratic_certificates"]))
    multiplicity_census = collections.Counter(state["quadratic_multiplicity"].values())
    if multiplicity_census != collections.Counter({2: 42, 4: 12}):
        fail("CYCLE_QUADRATIC_MULTIPLICITY_FAIL", dict(multiplicity_census))
    restored_anchors = [
        row for row in state["physical_anchors"] if row["origin"] == "fixed_full_restoration"
    ]
    if len(restored_anchors) != 12:
        fail("CYCLE_RESTORED_ANCHOR_CENSUS_FAIL", len(restored_anchors))
    if len(state["physical_anchors"]) != 36:
        fail("CYCLE_ALL_ANCHOR_CENSUS_FAIL", len(state["physical_anchors"]))

    certificate_payloads = {
        "topology_witnesses.json": {
            "schema": "k2p-cycle-topology-witnesses-v1",
            "witnesses": {
                key: state["topology_witnesses"][key]
                for key in sorted(state["topology_witnesses"])
            },
        },
        "transport_certificates.json": {
            "schema": "k2p-cycle-transport-certificates-v1",
            "certificates": {
                key: state["transport_certificates"][key]
                for key in sorted(state["transport_certificates"])
            },
        },
        "quadratic_certificates.json": {
            "schema": "k2p-cycle-quadratic-certificates-v1",
            "certificates": {
                key: state["quadratic_certificates"][key]
                for key in sorted(state["quadratic_certificates"])
            },
            "raw_multiplicity": {
                key: state["quadratic_multiplicity"][key]
                for key in sorted(state["quadratic_multiplicity"])
            },
        },
        "rank_witnesses.json": {
            "schema": "k2p-cycle-jacobian-rank-witnesses-v1",
            "certificates": {
                key: state["rank_certificates"][key]
                for key in sorted(state["rank_certificates"])
            },
        },
        "physical_anchors.json": {
            "schema": "k2p-cycle-physical-anchors-v1",
            "anchors": state["physical_anchors"],
        },
    }
    artifact_metadata = {
        "base_raw_ledger.jsonl.gz": base_meta,
        "restoration_roots.jsonl.gz": roots_meta,
        "full_completion_ledger.jsonl.gz": full_meta,
    }
    for name, payload in certificate_payloads.items():
        path = artifact_root / name
        atomic_json(path, payload)
        artifact_metadata[name] = {
            "sha256": sha_file(path),
            "bytes": path.stat().st_size,
        }

    source_ranks = collections.Counter()
    target_ranks = collections.Counter()
    for certificate in state["quadratic_certificates"].values():
        source_ranks[certificate["source_witnessed_jacobian_rank"]] += 1
        target_ranks[certificate["target_witnessed_jacobian_rank"]] += 1
    summary = {
        "schema": "k2p-cycle-three-port-closure-summary-v1",
        "status": "PASS",
        "claim": (
            "Every raw directed three-port cycle relation is pointwise excluded, "
            "an ordinary no-dummy terminal, or a fixed-full restoration root; every "
            "physical completion of every root is pointwise topology-excluded, "
            "quadratically excluded in the source-to-target direction, or exactly "
            "labelled-isomorphic."
        ),
        "logic": (
            "Fix one full containment first and restore all actual omitted labels in "
            "that same network pair. Source marginal openness selects exactly one of "
            "the enumerated labelled placements. No abstract parent-to-child lift and "
            "no target marginal openness is used."
        ),
        "bindings": {
            "atlas_sha256": sha_file(args.package_root / "atlas/k2p_atlas_core.py"),
            "canonicalizer_sha256": canonicalizer_sha256(atlas),
            "generator_sha256": sha_file(Path(__file__)),
            "common_replayer_sha256": sha_file(Path(__file__).with_name("cycle_common.py")),
            "independent_verifier_sha256": sha_file(
                Path(__file__).with_name("verify_cycle_closure.py")
            ),
            "mutation_suite_sha256": sha_file(
                Path(__file__).with_name("test_mutations.py")
            ),
            "rank_upper_coverage_sha256": sha_file(rank_coverage_path),
            "rank_upper_manifest_sha256": sha_file(
                rank_coverage_path.with_name("manifest.json")
            ),
        },
        "base": {
            "source_supports": len(sources),
            "target_completions": len(targets),
            "permutations": len(permutations),
            "raw_relations": 13440,
            "categories": dict(sorted(state["base_counts"].items())),
            "no_dummy_physical_anchors": 24,
        },
        "restoration": {
            "roots": len(state["roots"]),
            "root_multiplicity_by_dummy_count": {
                str(key): value for key, value in sorted(state["root_multiplicity"].items())
            },
            "physical_completions": sum(state["full_counts"].values()),
            "categories": dict(sorted(state["full_counts"].items())),
            "unresolved": 0,
            "restored_physical_isomorphic_anchors": len(restored_anchors),
        },
        "quadratics": {
            "raw_relations": state["full_counts"]["quadratic_separated"],
            "descriptor_pair_classes": len(state["quadratic_certificates"]),
            "class_multiplicity_census": {
                str(key): value for key, value in sorted(multiplicity_census.items())
            },
            "source_witnessed_jacobian_rank_class_census": {
                str(key): value for key, value in sorted(source_ranks.items())
            },
            "target_witnessed_jacobian_rank_class_census": {
                str(key): value for key, value in sorted(target_ranks.items())
            },
        },
        "physical_anchors": {
            "total": len(state["physical_anchors"]),
            "base_no_dummy": 24,
            "fixed_full_restored": 12,
            "all_have_unique_exact_transport": True,
        },
        "artifacts": artifact_metadata,
    }
    summary["payload_sha256"] = sha_object(summary)
    atomic_json(artifact_root / "cycle_three_port_summary.json", summary)
    print(json.dumps(summary, sort_keys=True))
    print(f"K2P_CYCLE_GENERATION_ELAPSED_SECONDS={time.time() - started:.6f}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        if isinstance(exc, KeyboardInterrupt):
            raise
        raise SystemExit(str(exc)) from exc
