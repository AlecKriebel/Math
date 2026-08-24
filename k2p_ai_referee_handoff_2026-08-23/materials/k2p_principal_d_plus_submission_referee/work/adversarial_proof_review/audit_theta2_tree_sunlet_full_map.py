#!/usr/bin/env python3
"""Direct full-Fourier-map audit of the 2,528 theta2 sign rows.

This verifier does not use the legacy rooted tree/sunlet reduction as a
theorem.  The old witness is used only to select the labelled three-port
coordinate restriction.  The actual certificate is an exact identity on the
original five-port maps: one side's transported T_i pullback is zero and the
other side's pullback is strictly negative by exact tensor Bernstein
coefficients on the open unit cube.
"""

from __future__ import annotations

import collections
import gzip
import importlib.util
import itertools
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
CORE_PATH = HERE / "audit_raw4_tree_sunlet_full_map.py"
LEDGER = PROJECT / "work/theta2_five_port_closure/artifacts/raw_directional_ledger.jsonl.gz"
PROOFS = PROJECT / "work/theta2_five_port_closure/artifacts/direct_proof_certificates.json.gz"
OUTPUT = HERE / "theta2_tree_sunlet_full_map_certificate.json"


def load_core():
    spec = importlib.util.spec_from_file_location("theta2_full_map_core", CORE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import full-map core")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main():
    core = load_core()
    atlas = core.load_atlas()
    sources = atlas.source_supports(("theta2",))
    targets = atlas.target_completions(5, True) + atlas.target_completions(5, False)
    with gzip.open(PROOFS, "rt") as handle:
        proofs = json.load(handle)
    witnesses = proofs["topology_witnesses"]
    rows = []
    with gzip.open(LEDGER, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            if row.get("category") == "tree_sunlet_pointwise_excluded":
                rows.append(row)
    core.require(len(rows) == 2528, f"theta2 row census:{len(rows)}")

    prepared_sources = [atlas.prepare_mixed_source(source.graph) for source in sources]
    exact_relations = collections.Counter()
    metadata = []
    needs = collections.defaultdict(set)
    for row in rows:
        witness = witnesses[row["topology_witness_id"]]
        core.require(
            witness["reason"] == "tree_sunlet_strict_sign"
            and witness["source_type"] == "tree"
            and witness["target_type"] == "sunlet",
            f"theta2 legacy witness drift:{row['raw_id']}",
        )
        triple = tuple(witness["triple"])
        permutation = tuple(row["port_permutation"])
        relabelled = atlas.relabel_record(targets[row["target_index"]], permutation)
        selected = atlas.selected_graph_from_completion(relabelled)
        relation = atlas.mixed_relation_exact_prepared(
            prepared_sources[row["source_index"]], selected
        )
        exact_relations[relation] += 1
        core.require(
            relation == "none",
            f"theta2 exact terminal conflict:{row['raw_id']}:{relation}",
        )
        inverse = {new: old for old, new in enumerate(permutation)}
        mapped_triple = tuple(sorted(inverse[label] for label in triple))
        needs[row["target_index"]].add(mapped_triple)
        metadata.append((row, triple, mapped_triple, permutation, inverse))

    source_polynomials = {}
    for source_index, source in enumerate(sources):
        descriptor = atlas.model_descriptor_fast2(source.graph)
        outputs = atlas.output_sparse_polynomials(descriptor)
        for triple in {item[1] for item in metadata if item[0]["source_index"] == source_index}:
            for orientation in triple:
                polynomial = core.t_pullback(atlas, descriptor, outputs, triple, orientation)
                core.require(
                    not polynomial,
                    f"theta2 source tree T pullback nonzero:{source_index}:{triple}:{orientation}",
                )
                source_polynomials[(source_index, triple, orientation)] = polynomial

    target_polynomials = {}
    sign_certificates = {}
    chosen_by_target_triple = {}
    for target_index, triples in sorted(needs.items()):
        descriptor = atlas.model_descriptor_fast2(targets[target_index].graph)
        outputs = atlas.output_sparse_polynomials(descriptor)
        for triple in sorted(triples):
            candidates = []
            for orientation in triple:
                polynomial = core.t_pullback(atlas, descriptor, outputs, triple, orientation)
                target_polynomials[(target_index, triple, orientation)] = polynomial
                candidates.append((len(polynomial), orientation, polynomial))
            for _, orientation, polynomial in sorted(candidates, key=lambda x: (x[0], x[1])):
                try:
                    sign = core.bernstein_sign_certificate(polynomial)
                except core.TruthFailure:
                    continue
                digest = core.sparse_hash(polynomial)
                previous = sign_certificates.setdefault(
                    digest,
                    {
                        "pullback_sha256": digest,
                        "pullback_term_count": len(polynomial),
                        "sign": sign,
                        "target_presentations": [],
                    },
                )
                core.require(previous["sign"] == sign, "theta2 sign hash collision")
                previous["target_presentations"].append(
                    [target_index, list(triple), orientation]
                )
                chosen_by_target_triple[(target_index, triple)] = orientation
                break
            core.require(
                (target_index, triple) in chosen_by_target_triple,
                f"theta2 no signed orientation:{target_index}:{triple}",
            )

    row_hashes = []
    relation_classes = collections.Counter()
    for row, triple, mapped_triple, permutation, inverse in metadata:
        mapped_orientation = chosen_by_target_triple[(row["target_index"], mapped_triple)]
        relabelled_orientation = permutation[mapped_orientation]
        source_polynomial = source_polynomials[
            (row["source_index"], triple, relabelled_orientation)
        ]
        target_polynomial = target_polynomials[
            (row["target_index"], mapped_triple, mapped_orientation)
        ]
        core.require(not source_polynomial, f"theta2 source zero drift:{row['raw_id']}")
        target_digest = core.sparse_hash(target_polynomial)
        truth_row = {
            "raw_id": row["raw_id"],
            "source_index": row["source_index"],
            "target_index": row["target_index"],
            "permutation_index": row["permutation_index"],
            "legacy_witness_triple": list(triple),
            "chosen_T_orientation_label": relabelled_orientation,
            "source_pullback_sha256": core.sparse_hash(source_polynomial),
            "target_pullback_sha256": target_digest,
            "exact_full_graph_relation": "none",
            "result": "source_zero_strict_target_negative",
        }
        row_hashes.append(core.sha(truth_row))
        relation_classes[(core.sparse_hash(source_polynomial), target_digest)] += 1

    for certificate in sign_certificates.values():
        certificate["target_presentations"] = sorted(
            certificate["target_presentations"], key=lambda row: (row[0], row[1], row[2])
        )
    core.require(exact_relations == {"none": 2528}, f"theta2 exact census:{exact_relations}")
    core.require(len(row_hashes) == 2528, "theta2 truth coverage")
    report = {
        "schema": "k2p-theta2-tree-sunlet-full-map-truth-v1",
        "status": "PASS",
        "claim_boundary": (
            "Legacy rooted tree/sunlet names are used only to bind the three labels; "
            "the proof is the direct full five-port Fourier-map zero/sign identity."
        ),
        "inputs": {
            "atlas_sha256": core.sha_file(core.ATLAS_PATH),
            "raw_ledger_sha256": core.sha_file(LEDGER),
            "legacy_proof_table_sha256": core.sha_file(PROOFS),
        },
        "claimed_rows": len(rows),
        "exact_full_graph_relation_census": dict(exact_relations),
        "false_iso_or_triangle_conflicts": 0,
        "full_map_source_zero_rows": len(row_hashes),
        "full_map_strict_target_sign_rows": len(row_hashes),
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
    except (RuntimeError, KeyError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"THETA2_TREE_SUNLET_TRUTH_FAIL:{exc}") from exc
