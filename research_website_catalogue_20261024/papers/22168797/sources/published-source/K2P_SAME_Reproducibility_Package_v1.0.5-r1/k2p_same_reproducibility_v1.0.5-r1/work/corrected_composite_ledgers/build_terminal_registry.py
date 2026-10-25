#!/usr/bin/env python3
"""Freeze the exact 934 raw-four direct terminal certificates.

The production records are large and contain runtime metadata.  This registry
retains the exact proof payload, the original byte/semantic bindings, and the
36 later direct-polynomial overlays in a compact deterministic input artifact.
"""

from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

from composite_support import (
    ARTIFACTS,
    PACKAGE,
    PROJECT,
    canonical_bytes,
    load_json,
    sha_file,
    sha_object,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=Path, default=PROJECT / "runs/four_port_release_v4")
    parser.add_argument(
        "--output",
        type=Path,
        default=ARTIFACTS / "raw4_terminal_certificate_registry.json.gz",
    )
    args = parser.parse_args()

    direct_path = PACKAGE / "proofs/four_port_direct_residual_closure_certificate.json"
    direct = load_json(direct_path)
    overlays = {
        (int(row["source_index"]), int(row["canonical_class_id"])): row
        for row in direct["coverage"]
    }
    rows = []
    input_hashes = {"direct_overlay": sha_file(direct_path)}
    for source_index in range(6):
        manifest_path = (
            PACKAGE
            / f"results/four_port_release_v4/source_{source_index}/residual_manifest.json"
        )
        manifest = load_json(manifest_path)
        input_hashes[f"manifest_source_{source_index}"] = sha_file(manifest_path)
        for summary_row in manifest["records"]:
            status = summary_row["status"]
            if status == "restoration_parent":
                continue
            class_id = int(summary_row["canonical_class_id"])
            record_path = args.runs / f"source_{source_index}/records/class_{class_id:06d}.json"
            record = load_json(record_path)
            if record["semantic_record_sha256"] != summary_row["semantic_record_sha256"]:
                raise SystemExit(f"TERMINAL_SEMANTIC_BINDING_FAIL:{source_index}:{class_id}")
            if sha_file(record_path) != summary_row["record_sha256"]:
                raise SystemExit(f"TERMINAL_BYTE_BINDING_FAIL:{source_index}:{class_id}")
            key = (source_index, class_id)
            overlay = overlays.get(key)
            if status == "unresolved" and overlay is None:
                raise SystemExit(f"TERMINAL_MISSING_DIRECT_OVERLAY:{source_index}:{class_id}")
            if overlay is not None:
                certificate = {
                    "kind": "exact_direct_polynomial_separator",
                    "family": overlay["family"],
                    "degree": overlay["degree"],
                    "polynomial_sha256": overlay["polynomial_sha256"],
                    "source_pullback_sha256": overlay["source_pullback_sha256"],
                    "source_pullback_term_count": overlay["source_pullback_term_count"],
                    "target_pullback_term_count": overlay["target_pullback_term_count"],
                    "target_pullback_zero": overlay["target_pullback_zero"],
                    "strict_D_plus_witness_sha256": sha_object(overlay["strict_D_plus_witness"]),
                    "overlay_row_sha256": sha_object(overlay),
                }
            else:
                proof = record["certificate"]
                if not isinstance(proof, dict) or not proof.get("type"):
                    raise SystemExit(f"TERMINAL_CERTIFICATE_MISSING:{source_index}:{class_id}")
                certificate = {
                    "kind": proof["type"],
                    "certificate_payload_sha256": record["certificate_payload_sha256"],
                    "certificate_sha256": sha_object(proof),
                    "certificate": proof,
                }
            class_identifier = f"source_{source_index}:class_{class_id:06d}"
            row = {
                "class_id": class_id,
                "class_identifier": class_identifier,
                "descriptor_sha256": record["descriptor_sha256"],
                "manifest_record_sha256": summary_row["record_sha256"],
                "semantic_record_sha256": record["semantic_record_sha256"],
                "source_index": source_index,
                "terminal_certificate": certificate,
            }
            row["certificate_binding_sha256"] = sha_object(row)
            rows.append(row)
    rows.sort(key=lambda row: row["class_identifier"])
    if len(rows) != 934 or len({row["class_identifier"] for row in rows}) != 934:
        raise SystemExit(f"TERMINAL_REGISTRY_CENSUS_FAIL:{len(rows)}")
    payload = {
        "schema": "k2p-raw4-terminal-certificate-registry-v1",
        "status": "PASS",
        "terminal_class_count": len(rows),
        "class_id_hash_root": sha_object(sorted(row["class_identifier"] for row in rows)),
        "rows": rows,
        "input_artifact_sha256": input_hashes,
    }
    payload["payload_sha256"] = sha_object(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    with temporary.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as encoded:
            encoded.write(canonical_bytes(payload))
            encoded.write(b"\n")
    temporary.replace(args.output)
    print(json.dumps({"status": "PASS", "rows": len(rows), "sha256": sha_file(args.output)}, sort_keys=True))


if __name__ == "__main__":
    main()
