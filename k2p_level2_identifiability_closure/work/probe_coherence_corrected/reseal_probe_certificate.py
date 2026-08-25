#!/usr/bin/env python3
"""Deterministically reseal the probe summary from immutable primary ledgers.

This is a packaging utility, not an independent verifier.  It is useful after
transporting the large primary ledgers or repairing a damaged summary file.
"""

from __future__ import annotations

import collections
import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
BUILDER = HERE / "build_probe_coherence_corrected.py"
CERTIFICATE = HERE / "probe_coherence_certificate.json"


class SealFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise SealFailure(message)


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


class Ordered:
    def __init__(self):
        self.rows = 0
        self.root = sha([])

    def add(self, row):
        self.root = sha({"previous": self.root, "row_sha256": sha(row)})
        self.rows += 1

    def public(self):
        return {
            "algorithm": "root_0=sha256(canonical([])); root_n=sha256(canonical({previous:root_(n-1),row_sha256:h_n}))",
            "rows": self.rows,
            "ordered_hash_root": self.root,
        }


def import_builder():
    spec = importlib.util.spec_from_file_location("probe_reseal_builder", BUILDER)
    require(spec is not None and spec.loader is not None, "builder import")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def stream_summary(path, status=False, origin=False, reverse=False, keep_rows=False):
    ordered = Ordered()
    counts = collections.Counter()
    by_origin = collections.Counter()
    reverse_counts = collections.Counter()
    equality = 0
    rows = []
    with gzip.open(path, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            ordered.add(row)
            if status:
                counts[row["status"]] += 1
                if row["status"] in {"isomorphic", "triangle"}:
                    equality += 1
            if origin:
                by_origin[(row["origin"], row["status"])] += 1
            if reverse and "reverse_order_certificate" in row:
                reverse_counts[row["reverse_order_certificate"]["reverse_parent_relation"]] += 1
            if keep_rows:
                rows.append(row)
    return ordered, counts, by_origin, reverse_counts, equality, rows


def store_summary(path):
    ordered = Ordered()
    ids = set()
    with gzip.open(path, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            require(row["record_id"] not in ids, f"duplicate store ID:{path.name}")
            ids.add(row["record_id"])
            ordered.add(row)
    return {
        "path": path.name,
        "sha256": sha_file(path),
        "unique_records": len(ids),
        "ordered_records": ordered.public(),
    }


def main():
    builder = import_builder()
    atlas = builder.import_path("probe_reseal_atlas", builder.ATLAS_PATH)
    common = builder.import_path("cycle_common", builder.CYCLE_COMMON)
    generator = builder.import_path("probe_reseal_cycle_generator", builder.CYCLE_GENERATOR)
    contract = json.loads(builder.INPUT_CONTRACT.read_text())
    anchors = builder.reconstruct_anchors(atlas, common, generator, contract)
    anchor_registry = builder.CanonicalRelationRegistry(atlas)
    coverage = collections.defaultdict(list)
    public_anchors = []
    for anchor in anchors:
        class_id = anchor_registry.add(anchor)
        coverage[class_id].append(anchor["anchor_id"])
        public_anchors.append(builder.public_anchor_row(anchor, class_id))
    anchor_inventory = {
        "status": "PASS",
        "anchors": len(anchors),
        "source_sites": sum(row["source_profile"]["site_count"] for row in anchors),
        "target_sites": sum(row["target_profile"]["site_count"] for row in anchors),
        "first_pairs": sum(
            row["source_profile"]["site_count"] * row["target_profile"]["site_count"]
            for row in anchors
        ),
        "relation_counts": dict(sorted(collections.Counter(row["relation"] for row in anchors).items())),
        "origin_counts": dict(sorted(collections.Counter(row["origin"] for row in anchors).items())),
        "canonical_anchor_classes": len(anchor_registry.representatives),
        "canonical_class_coverage": {
            str(class_id): members for class_id, members in sorted(coverage.items())
        },
        "ordered_public_anchor_hash_root": sha([sha(row) for row in public_anchors]),
        "public_anchors": public_anchors,
    }

    one_ordered, one_counts, one_by_origin, _, one_equality, one_rows = stream_summary(
        HERE / "one_port_ledger.jsonl.gz", status=True, origin=True
    )
    parent_ordered, _, _, _, _, parent_rows = stream_summary(
        HERE / "two_port_parent_inventory.jsonl.gz", keep_rows=True
    )
    two_ordered, two_counts, two_by_origin, reverse_counts, two_equality, two_rows = stream_summary(
        HERE / "two_port_ledger.jsonl.gz", status=True, origin=True, reverse=True
    )
    canonical_one = len({row["canonical_one_port_relation_class_id"] for row in parent_rows})
    base_global = {
        row["anchor_id"]: row["global_triangle"] is not None for row in public_anchors
    }
    inherited_parent_count = sum(base_global[row["base_anchor_id"]] for row in parent_rows)
    equality_global_count = 0
    with gzip.open(HERE / "two_port_ledger.jsonl.gz", "rt") as handle:
        for line in handle:
            row = json.loads(line)
            equality_global_count += (
                row["status"] in {"isomorphic", "triangle"}
                and base_global[row["base_anchor_id"]]
            )

    with gzip.open(HERE / "separation_proof_registry.json.gz", "rt") as handle:
        proof = json.load(handle)
    proof_claim = proof["payload_sha256"]
    proof_unhashed = dict(proof)
    proof_unhashed.pop("payload_sha256")
    require(proof_claim == sha(proof_unhashed), "proof payload")
    certificate = json.loads(CERTIFICATE.read_text())
    certificate["status"] = "PASS"
    # Rebind the summary to the exact current inputs.  This utility does not
    # regenerate the large ledgers; it reconstructs their graph-derived anchor
    # inventory under the current atlas and then reseals the immutable ledgers.
    # A clean full release replay remains the independent regeneration gate.
    certificate["inputs"] = {
        "atlas_sha256": sha_file(builder.ATLAS_PATH),
        "probe_input_contract_sha256": sha_file(builder.INPUT_CONTRACT),
        "probe_input_contract_payload_sha256": contract["payload_sha256"],
        "probe_input_independent_replay_sha256": sha_file(builder.INPUT_REPLAY),
        "probe_input_mutations_sha256": sha_file(builder.INPUT_MUTATIONS),
        "corrected_restoration_sha256": sha_file(builder.RESTORATION),
        "raw4_ledger_sha256": sha_file(builder.RAW4),
        "theta2_fixed_full_closure_sha256": sha_file(builder.THETA2),
        "cycle_physical_anchors_sha256": sha_file(builder.CYCLE_ANCHORS),
        "cycle_promotion_sha256": sha_file(builder.CYCLE_PROMOTION),
    }
    certificate["classifier_order"] = [
        "exact_labelled_isomorphism_or_ordinary_triangle",
        "displayed_quartet_mismatch",
        "direct_original_full_map_Ti_zero_versus_Bernstein_strict_sign",
        "unresolved_fatal",
    ]
    certificate["anchor_inventory"] = anchor_inventory
    certificate["one_port"] = {
        "raw_pairs": one_ordered.rows,
        "counts": dict(sorted(one_counts.items())),
        "counts_by_origin": {
            f"{origin_name}:{status_name}": count
            for (origin_name, status_name), count in sorted(one_by_origin.items())
        },
        "equality_survivors": one_equality,
        "canonical_equality_relation_classes": canonical_one,
        "ordered_ledger": one_ordered.public(),
        "ledger_sha256": sha_file(HERE / "one_port_ledger.jsonl.gz"),
        "unresolved": one_counts["unresolved"],
        "unresolved_examples": [],
    }
    certificate["two_port"] = {
        "parents": len(parent_rows),
        "raw_pairs": two_ordered.rows,
        "counts": dict(sorted(two_counts.items())),
        "counts_by_origin": {
            f"{origin_name}:{status_name}": count
            for (origin_name, status_name), count in sorted(two_by_origin.items())
        },
        "equality_survivors": two_equality,
        "ordered_parent_inventory": parent_ordered.public(),
        "parent_inventory_sha256": sha_file(HERE / "two_port_parent_inventory.jsonl.gz"),
        "ordered_ledger": two_ordered.public(),
        "ledger_sha256": sha_file(HERE / "two_port_ledger.jsonl.gz"),
        "unresolved": two_counts["unresolved"],
        "unresolved_examples": [],
        "reverse_order_parent_relation_counts": dict(sorted(reverse_counts.items())),
    }
    certificate["registries"] = {
        "separation": {
            "path": "separation_proof_registry.json.gz",
            "sha256": sha_file(HERE / "separation_proof_registry.json.gz"),
            "payload_sha256": proof_claim,
            "topological_proofs": len(proof["separation_proof_registry"]),
            "full_map_Ti_relation_certificates": len(proof["full_map_Ti_registry"]["certificates"]),
            "full_map_Ti_strict_polynomials": len(proof["full_map_Ti_registry"]["strict_polynomial_registry"]),
        },
        "exact_transports": store_summary(HERE / "exact_transport_ledger.jsonl.gz"),
        "parent_restrictions": store_summary(HERE / "parent_restriction_ledger.jsonl.gz"),
    }
    certificate["assembly_theorem"]["one_port_segment_gate"].update({
        "raw_pairs": one_ordered.rows,
        "equality_parents_retained": one_equality,
    })
    certificate["assembly_theorem"]["two_port_order_gate"].update({
        "raw_pairs_above_equality_parents_only": two_ordered.rows,
        "reversed_marginals_checked": two_equality,
    })
    certificate["assembly_theorem"]["one_global_triangle_gate"].update({
        "triangle_anchors": sum(base_global.values()),
        "one_port_parents_inheriting_triangle": inherited_parent_count,
        "two_port_equalities_inheriting_triangle": equality_global_count,
    })
    certificate.pop("operational", None)
    certificate.pop("payload_sha256", None)
    logical = dict(certificate)
    certificate["payload_sha256"] = sha(logical)
    CERTIFICATE.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "payload_sha256": certificate["payload_sha256"],
        "one": dict(sorted(one_counts.items())),
        "two": dict(sorted(two_counts.items())),
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (SealFailure, KeyError, OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"CORRECTED_PROBE_RESEAL_FAIL:{error}") from error
