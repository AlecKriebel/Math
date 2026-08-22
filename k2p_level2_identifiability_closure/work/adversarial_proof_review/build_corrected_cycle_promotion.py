#!/usr/bin/env python3
"""Build the fail-closed, legacy-label-free cycle promotion projection.

The original ledgers are immutable provenance.  They are deliberately kept
outside the promotion directory.  This builder projects every original row
onto an authoritative terminal/obligation kind and binds every restored child
to the exact fixed-full construction data used by the graph generator.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
CYCLE = PROJECT / "work/cycle_three_port_closure"
ARTIFACTS = CYCLE / "artifacts"
PROMOTION = CYCLE / "promotion"
BASE_SOURCE = ARTIFACTS / "base_raw_ledger.jsonl.gz"
FULL_SOURCE = ARTIFACTS / "full_completion_ledger.jsonl.gz"
ROOT_SOURCE = ARTIFACTS / "restoration_roots.jsonl.gz"
TRUTH_SOURCE = HERE / "cycle_tree_sunlet_full_map_certificate.json"
BASE_OUTPUT = PROMOTION / "cycle_base_authoritative.jsonl.gz"
FULL_OUTPUT = PROMOTION / "cycle_full_authoritative.jsonl.gz"
SUMMARY_OUTPUT = PROMOTION / "cycle_promotion_certificate.json"


class ProjectionFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ProjectionFailure(message)


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


def read_gzip_rows(path):
    with gzip.open(path, "rt") as handle:
        for line in handle:
            yield json.loads(line)


class CanonicalGzipWriter:
    def __init__(self, path):
        self.path = path
        self.raw = None
        self.compressed = None
        self.text = None

    def __enter__(self):
        self.raw = self.path.open("wb")
        self.compressed = gzip.GzipFile(
            filename="", mode="wb", fileobj=self.raw, compresslevel=9, mtime=0
        )
        self.text = io.TextIOWrapper(self.compressed, encoding="utf-8", newline="\n")
        return self

    def write(self, row):
        self.text.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")

    def __exit__(self, exc_type, exc, traceback):
        self.text.close()
        self.raw.close()
        return False


def construction_binding(row):
    payload = {
        "schema": "k2p-cycle-fixed-full-child-transport-v1",
        "root_id": row["root_id"],
        "base_raw_id": row["base_raw_id"],
        "full_raw_id": row["raw_id"],
        "source_index": row["source_index"],
        "target_index": row["target_index"],
        "permutation_index": row["permutation_index"],
        "dummy_roles_in_label_order": row["dummy_roles_in_label_order"],
        "source_placement_path": row["source_placement_path"],
        "port_count": row["port_count"],
        "source_operation": "iterated_labelled_edge_subdivision_attachment",
        "target_operation": "simultaneous_labelled_dummy_role_promotion",
    }
    return sha(payload)


def main():
    PROMOTION.mkdir(parents=True, exist_ok=True)
    truth = json.loads(TRUTH_SOURCE.read_text())
    require(truth["status"] == "PASS", "whole-map truth is not PASS")
    require(truth["unresolved"] == truth["incoherent"] == 0, "whole-map truth incomplete")
    base_truth = truth["families"]["cycle_base"]["ordered_truth_row_hashes"]
    full_truth = truth["families"]["cycle_full_equal_topology"]["ordered_truth_row_hashes"]
    require(len(base_truth) == 7452 and len(full_truth) == 300, "truth row census")

    roots = {row["base_raw_id"]: row for row in read_gzip_rows(ROOT_SOURCE)}
    require(len(roots) == 5964, "restoration-root census")

    base_counts = {}
    base_hashes = []
    base_sign_index = 0
    with CanonicalGzipWriter(BASE_OUTPUT) as output:
        for source in read_gzip_rows(BASE_SOURCE):
            common = {
                "raw_id": source["raw_id"],
                "source_index": source["source_index"],
                "target_index": source["target_index"],
                "permutation_index": source["permutation_index"],
                "port_permutation": source["port_permutation"],
                "dummy_roles": source["dummy_roles"],
            }
            old_kind = source["category"]
            if old_kind == "tree_sunlet_pointwise_excluded":
                row = {
                    **common,
                    "terminal_kind": "full_map_Ti_strict_sign",
                    "whole_map_truth_row_sha256": base_truth[base_sign_index],
                    "whole_map_truth_payload_sha256": truth["payload_sha256"],
                }
                base_sign_index += 1
            elif old_kind == "restoration_root":
                root = roots[source["raw_id"]]
                require(
                    all(root[key] == source[key] for key in (
                        "source_index", "target_index", "permutation_index",
                        "port_permutation", "dummy_roles"
                    )),
                    f"restoration-root binding:{source['raw_id']}",
                )
                row = {
                    **common,
                    "terminal_kind": "fixed_full_restoration_obligation",
                    "root_id": root["root_id"],
                }
            elif old_kind == "isomorphic":
                row = {
                    **common,
                    "terminal_kind": "labelled_isomorphism",
                    "transport_certificate_id": source["certificate_id"],
                }
            elif old_kind == "triangle":
                row = {
                    **common,
                    "terminal_kind": "ordinary_triangle_relation",
                    "transport_certificate_id": source["certificate_id"],
                }
            else:
                raise ProjectionFailure(f"unknown base category:{old_kind}")
            base_counts[row["terminal_kind"]] = base_counts.get(row["terminal_kind"], 0) + 1
            row["authoritative_row_sha256"] = sha(row)
            base_hashes.append(row["authoritative_row_sha256"])
            output.write(row)
    require(base_sign_index == len(base_truth), "base truth binding coverage")

    full_counts = {}
    full_hashes = []
    full_sign_index = 0
    child_counts = {}
    child_transport_hashes = []
    with CanonicalGzipWriter(FULL_OUTPUT) as output:
        for source in read_gzip_rows(FULL_SOURCE):
            common = {
                "raw_id": source["raw_id"],
                "root_id": source["root_id"],
                "base_raw_id": source["base_raw_id"],
                "source_index": source["source_index"],
                "target_index": source["target_index"],
                "permutation_index": source["permutation_index"],
                "dummy_roles_in_label_order": source["dummy_roles_in_label_order"],
                "source_placement_path": source["source_placement_path"],
                "port_count": source["port_count"],
                "fixed_full_transport_sha256": construction_binding(source),
            }
            old_kind = source["category"]
            if old_kind == "quartet_pointwise_excluded":
                row = {
                    **common,
                    "terminal_kind": "displayed_quartet_strict_separator",
                    "proof_certificate_id": source["certificate_id"],
                }
            elif old_kind == "tree_sunlet_pointwise_excluded":
                row = {
                    **common,
                    "terminal_kind": "full_map_Ti_strict_sign",
                    "whole_map_truth_row_sha256": full_truth[full_sign_index],
                    "whole_map_truth_payload_sha256": truth["payload_sha256"],
                }
                full_sign_index += 1
            elif old_kind == "quadratic_separated":
                row = {
                    **common,
                    "terminal_kind": "exact_directional_quadratic",
                    "proof_certificate_id": source["certificate_id"],
                }
            elif old_kind == "isomorphic":
                row = {
                    **common,
                    "terminal_kind": "labelled_isomorphism",
                    "transport_certificate_id": source["certificate_id"],
                }
            else:
                raise ProjectionFailure(f"unknown full category:{old_kind}")
            full_counts[row["terminal_kind"]] = full_counts.get(row["terminal_kind"], 0) + 1
            child_counts[row["root_id"]] = child_counts.get(row["root_id"], 0) + 1
            child_transport_hashes.append(row["fixed_full_transport_sha256"])
            row["authoritative_row_sha256"] = sha(row)
            full_hashes.append(row["authoritative_row_sha256"])
            output.write(row)
    require(full_sign_index == len(full_truth), "full truth binding coverage")
    require(set(child_counts) == {row["root_id"] for row in roots.values()}, "missing root child")

    expected_base = {
        "full_map_Ti_strict_sign": 7452,
        "fixed_full_restoration_obligation": 5964,
        "labelled_isomorphism": 8,
        "ordinary_triangle_relation": 16,
    }
    expected_full = {
        "displayed_quartet_strict_separator": 535920,
        "full_map_Ti_strict_sign": 300,
        "exact_directional_quadratic": 132,
        "labelled_isomorphism": 12,
    }
    require(base_counts == expected_base, f"base promotion census:{base_counts}")
    require(full_counts == expected_full, f"full promotion census:{full_counts}")
    require(len(base_hashes) == 13440 and len(full_hashes) == 536364, "projection coverage")

    report = {
        "schema": "k2p-cycle-three-port-authoritative-promotion-v1",
        "status": "PASS",
        "claim_boundary": (
            "Only the terminal kinds in the authoritative ledgers are promoted. "
            "The immutable historical ledgers remain outside this promotion root."
        ),
        "legacy_rooted_reason_or_type_fields": 0,
        "inputs": {
            "atlas_sha256": sha_file(
                PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
            ),
            "cycle_common_sha256": sha_file(CYCLE / "cycle_common.py"),
            "cycle_generator_sha256": sha_file(CYCLE / "generate_cycle_closure.py"),
            "historical_base_ledger_sha256": sha_file(BASE_SOURCE),
            "historical_full_ledger_sha256": sha_file(FULL_SOURCE),
            "restoration_roots_sha256": sha_file(ROOT_SOURCE),
            "topology_witnesses_sha256": sha_file(ARTIFACTS / "topology_witnesses.json"),
            "transport_certificates_sha256": sha_file(ARTIFACTS / "transport_certificates.json"),
            "quadratic_certificates_sha256": sha_file(ARTIFACTS / "quadratic_certificates.json"),
            "physical_anchors_sha256": sha_file(ARTIFACTS / "physical_anchors.json"),
            "whole_map_truth_file_sha256": sha_file(TRUTH_SOURCE),
            "whole_map_truth_payload_sha256": truth["payload_sha256"],
        },
        "base": {
            "rows": len(base_hashes),
            "terminal_census": base_counts,
            "ordered_authoritative_row_hash_root": sha(base_hashes),
        },
        "fixed_full_restoration": {
            "roots": len(roots),
            "children": len(full_hashes),
            "roots_with_zero_children": sum(count == 0 for count in child_counts.values()),
            "ordered_child_transport_hash_root": sha(child_transport_hashes),
        },
        "full": {
            "rows": len(full_hashes),
            "terminal_census": full_counts,
            "ordered_authoritative_row_hash_root": sha(full_hashes),
            "unresolved": 0,
        },
        "outputs": {
            "cycle_base_authoritative.jsonl.gz": {
                "sha256": sha_file(BASE_OUTPUT),
                "rows": len(base_hashes),
            },
            "cycle_full_authoritative.jsonl.gz": {
                "sha256": sha_file(FULL_OUTPUT),
                "rows": len(full_hashes),
            },
        },
        "unresolved": 0,
        "incoherent": 0,
    }
    report["payload_sha256"] = sha(report)
    SUMMARY_OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": report["status"],
        "base": report["base"]["terminal_census"],
        "full": report["full"]["terminal_census"],
        "payload_sha256": report["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ProjectionFailure, KeyError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"CYCLE_PROMOTION_BUILD_FAIL:{exc}") from exc
