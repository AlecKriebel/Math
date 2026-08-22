#!/usr/bin/env python3
"""Direct full-map audit of the 646 restoration-forest sign children."""

from __future__ import annotations

import collections
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
CORE_PATH = HERE / "audit_raw4_tree_sunlet_full_map.py"
RESTORATION_SOURCE = PROJECT / "work/restoration_forest/enumerate_five_port.py"
RESTORATION_CERTIFICATE = PROJECT / "work/restoration_forest/five_port_certificate.json"
OUTPUT = HERE / "restoration_tree_sunlet_full_map_certificate.json"
METADATA_CACHE = HERE / "restoration_tree_sunlet_metadata_cache.json"


def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def descriptor_outputs(atlas, graph, cache, key):
    if key not in cache:
        descriptor = atlas.model_descriptor_fast2(graph)
        cache[key] = (descriptor, atlas.output_sparse_polynomials(descriptor))
    return cache[key]


def sign_definite_certificate(core, polynomial):
    """Certify either strict sign; multiplying an invariant by -1 is harmless."""
    try:
        certificate = core.bernstein_sign_certificate(polynomial)
        return "negative", certificate, polynomial
    except core.TruthFailure as exc:
        # If both signs occur among the exact Bernstein coefficients, negating
        # cannot help and would merely repeat the expensive tensor transform.
        detail = str(exc)
        if " 1:" in detail and "-1:" in detail:
            raise
        negated = {exponent: -coefficient for exponent, coefficient in polynomial.items()}
        certificate = core.bernstein_sign_certificate(negated)
        return "positive", certificate, negated


def main():
    core = import_path("restoration_full_map_core", CORE_PATH)
    restoration = import_path("restoration_full_map_generator", RESTORATION_SOURCE)
    atlas = core.load_atlas()
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    roots, manifest_hashes, canonical_parent_count = restoration.reconstruct_roots(
        atlas, sources, targets
    )
    core.require(canonical_parent_count == 997, "restoration parent census")

    source_graphs = {}
    target_graphs = {}
    prepared_sources = {}
    metadata = []
    exact_relations = collections.Counter()
    full_child_count = 0
    proof_counts = collections.Counter()
    for root in roots:
        source_index = root["source_index"]
        target_index = root["target_index"]
        permutation = tuple(root["port_match"])
        roles = tuple(root["dummy_roles"])
        for role in roles:
            target_key = (target_index, permutation, role)
            if target_key not in target_graphs:
                target_graphs[target_key] = restoration.promoted_target(
                    atlas, targets, target_index, permutation, role, 4
                )
            target_full, target_selected = target_graphs[target_key]
            for insertion_index, candidate in enumerate(
                root["source_insertion_edge_candidates"]
            ):
                full_child_count += 1
                source_key = (source_index, insertion_index)
                if source_key not in source_graphs:
                    source_graphs[source_key] = restoration.insert_source_leaf(
                        atlas, sources[source_index].graph, candidate, 4
                    )
                    prepared_sources[source_key] = atlas.prepare_mixed_source(
                        source_graphs[source_key]
                    )
                source_graph = source_graphs[source_key]
                result = restoration.proof_first_topology(
                    atlas, source_graph, target_selected
                )
                proof_counts[result.get("proof") or result["status"]] += 1
                if result.get("proof") != "strict_tree_sunlet_sign":
                    continue
                relation = atlas.mixed_relation_exact_prepared(
                    prepared_sources[source_key], target_selected
                )
                exact_relations[relation] += 1
                row_id = {
                    "root_id": root["root_id"],
                    "restored_role": role,
                    "restored_label": 4,
                    "source_insertion_index": insertion_index,
                }
                core.require(
                    relation == "none",
                    f"restoration exact terminal conflict:{row_id}:{relation}",
                )
                triple = tuple(result["labels"])
                core.require(
                    {result["source_type"], result["target_type"]}
                    == {"tree", "sunlet"},
                    f"restoration legacy witness drift:{row_id}",
                )
                metadata.append(
                    {
                        "row_id": row_id,
                        "source_key": source_key,
                        "target_key": target_key,
                        "triple": triple,
                        "source_type": result["source_type"],
                        "target_type": result["target_type"],
                    }
                )

    core.require(full_child_count == 36568, f"restoration raw child census:{full_child_count}")
    core.require(len(metadata) == 646, f"restoration sign census:{len(metadata)}")
    core.require(exact_relations == {"none": 646}, f"restoration exact census:{exact_relations}")
    METADATA_CACHE.write_text(
        json.dumps(
            {
                "schema": "k2p-restoration-tree-sunlet-metadata-cache-v1",
                "rows": [
                    {
                        **row,
                        "source_key": list(row["source_key"]),
                        "target_key": [
                            row["target_key"][0],
                            list(row["target_key"][1]),
                            row["target_key"][2],
                        ],
                        "triple": list(row["triple"]),
                    }
                    for row in metadata
                ],
            },
            sort_keys=True,
            indent=2,
        )
        + "\n"
    )
    # The complete official certificate is a binding input; this replay only
    # replaces the 646 sign leaves and does not re-prove its other 35,922 rows.
    official = json.loads(RESTORATION_CERTIFICATE.read_text())
    core.require(
        official["census"]["proof_counts"]["strict_tree_sunlet_sign"] == 646,
        "restoration official sign census drift",
    )

    descriptor_cache = {}
    pullbacks = {}
    sign_certificates = {}
    presentations = collections.defaultdict(set)
    # Compile exactly the graph/triple pairs needed, independently from the
    # frozen certificate's structural names.
    for row in metadata:
        triple = row["triple"]
        for side, key, graph in (
            (
                "source",
                row["source_key"],
                source_graphs[row["source_key"]],
            ),
            (
                "target",
                row["target_key"],
                target_graphs[row["target_key"]][0],
            ),
        ):
            graph_key = (side, key)
            descriptor, outputs = descriptor_outputs(
                atlas, graph, descriptor_cache, graph_key
            )
            pair_key = (side, key, triple)
            if (side, key, triple, triple[0]) not in pullbacks:
                for orientation in triple:
                    polynomial = core.t_pullback(
                        atlas, descriptor, outputs, triple, orientation
                    )
                    pullbacks[(side, key, triple, orientation)] = polynomial

    row_hashes = []
    relation_classes = collections.Counter()
    signed_sides = collections.Counter()
    strict_signs = collections.Counter()
    sign_cache = {}
    for row in metadata:
        triple = row["triple"]
        prospective = []
        for orientation in triple:
            source_polynomial = pullbacks[
                ("source", row["source_key"], triple, orientation)
            ]
            target_polynomial = pullbacks[
                ("target", row["target_key"], triple, orientation)
            ]
            if not source_polynomial and target_polynomial:
                signed_side, signed_polynomial = "target", target_polynomial
            elif not target_polynomial and source_polynomial:
                signed_side, signed_polynomial = "source", source_polynomial
            else:
                continue
            prospective.append(
                (len(signed_polynomial), orientation, signed_side, signed_polynomial)
            )
        candidates = []
        for _, orientation, signed_side, signed_polynomial in sorted(
            prospective, key=lambda item: (item[0], item[1], item[2])
        ):
            polynomial_digest = core.sparse_hash(signed_polynomial)
            if polynomial_digest not in sign_cache:
                try:
                    sign_cache[polynomial_digest] = sign_definite_certificate(
                        core, signed_polynomial
                    )
                except core.TruthFailure:
                    sign_cache[polynomial_digest] = None
            cached_sign = sign_cache[polynomial_digest]
            if cached_sign is None:
                continue
            strict_sign, sign, normalized = cached_sign
            try:
                core.require(sign is not None, "missing strict sign certificate")
            except core.TruthFailure:
                continue
            candidates.append(
                (
                    len(signed_polynomial),
                    orientation,
                    signed_side,
                    strict_sign,
                    sign,
                    normalized,
                )
            )
            # Shortest exact orientation wins; no need to test larger tensors.
            break
        core.require(
            candidates,
            f"restoration no direct full-map zero/sign orientation:{row['row_id']}",
        )
        (
            _,
            orientation,
            signed_side,
            strict_sign,
            sign,
            normalized,
        ) = sorted(candidates, key=lambda item: (item[0], item[1], item[2]))[0]
        zero_side = "target" if signed_side == "source" else "source"
        source_polynomial = pullbacks[
            ("source", row["source_key"], triple, orientation)
        ]
        target_polynomial = pullbacks[
            ("target", row["target_key"], triple, orientation)
        ]
        zero_polynomial = source_polynomial if zero_side == "source" else target_polynomial
        signed_polynomial = source_polynomial if signed_side == "source" else target_polynomial
        core.require(not zero_polynomial, f"restoration zero-side drift:{row['row_id']}")
        signed_digest = core.sparse_hash(signed_polynomial)
        normalized_digest = core.sparse_hash(normalized)
        previous = sign_certificates.setdefault(
            signed_digest,
            {
                "pullback_sha256": signed_digest,
                "pullback_term_count": len(signed_polynomial),
                "strict_sign": strict_sign,
                "normalized_negative_pullback_sha256": normalized_digest,
                "sign": sign,
                "presentations": [],
            },
        )
        core.require(
            previous["strict_sign"] == strict_sign
            and previous["normalized_negative_pullback_sha256"] == normalized_digest
            and previous["sign"] == sign,
            "restoration sign hash collision",
        )
        signed_sides[signed_side] += 1
        strict_signs[strict_sign] += 1
        presentations[signed_digest].add(
            (
                signed_side,
                repr(row["source_key"] if signed_side == "source" else row["target_key"]),
                triple,
                orientation,
            )
        )
        truth_row = {
            **row["row_id"],
            "legacy_witness_triple": list(triple),
            "chosen_T_orientation_label": orientation,
            "source_pullback_sha256": core.sparse_hash(source_polynomial),
            "target_pullback_sha256": core.sparse_hash(target_polynomial),
            "exact_full_graph_relation": "none",
            "result": (
                f"strict_source_{strict_sign}_target_zero"
                if signed_side == "source"
                else f"source_zero_strict_target_{strict_sign}"
            ),
        }
        row_hashes.append(core.sha(truth_row))
        relation_classes[
            (core.sparse_hash(source_polynomial), core.sparse_hash(target_polynomial))
        ] += 1

    for digest, certificate in sign_certificates.items():
        certificate["presentations"] = [
            [side, key, list(triple), orientation]
            for side, key, triple, orientation in sorted(presentations[digest])
        ]
    core.require(len(row_hashes) == 646, "restoration truth row coverage")
    report = {
        "schema": "k2p-restoration-tree-sunlet-full-map-truth-v1",
        "status": "PASS",
        "claim_boundary": (
            "Each former rooted tree/sunlet child is rebound to a direct T_i zero/sign "
            "identity on the original physical five-port source and target maps."
        ),
        "inputs": {
            "atlas_sha256": core.sha_file(core.ATLAS_PATH),
            "restoration_generator_sha256": core.sha_file(RESTORATION_SOURCE),
            "restoration_certificate_sha256": core.sha_file(RESTORATION_CERTIFICATE),
            "manifest_sha256": manifest_hashes,
        },
        "complete_restoration_child_census_replayed": full_child_count,
        "claimed_rows": len(metadata),
        "exact_full_graph_relation_census": dict(exact_relations),
        "false_iso_or_triangle_conflicts": 0,
        "full_map_zero_rows": len(row_hashes),
        "full_map_strict_sign_rows": len(row_hashes),
        "signed_side_census": dict(sorted(signed_sides.items())),
        "strict_sign_census": dict(sorted(strict_signs.items())),
        "unresolved": 0,
        "incoherent": 0,
        "canonical_polynomial_relation_classes": len(relation_classes),
        "canonical_relation_class_multiplicities": {
            f"{source}:{target}": count
            for (source, target), count in sorted(relation_classes.items())
        },
        "sign_certificates": dict(sorted(sign_certificates.items())),
        "ordered_truth_row_hashes": row_hashes,
        "ordered_truth_row_hash_root": core.sha(row_hashes),
    }
    report["payload_sha256"] = core.sha(report)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": report["status"],
                "rows": report["claimed_rows"],
                "classes": report["canonical_polynomial_relation_classes"],
                "sign_polynomials": len(sign_certificates),
                "payload_sha256": report["payload_sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, AssertionError, KeyError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"RESTORATION_TREE_SUNLET_TRUTH_FAIL:{exc}") from exc
