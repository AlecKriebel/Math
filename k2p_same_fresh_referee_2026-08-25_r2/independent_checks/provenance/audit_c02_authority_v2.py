#!/usr/bin/env python3
"""Independent scope/authority audit for the revised C02 certificate.

This script deliberately imports no submitted Python module.  It checks the
sealed JSON and TeX objects directly, recomputes their file digests, and makes
the old restoration numbers visible while verifying that they occur only in
objects classified as historical and non-promotable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.project.resolve()

    paths = {
        "crosswalk": root / "proof_compression_submission/crosswalk/THEOREM_ARTIFACT_CROSSWALK.json",
        "lock": root / "work/final_theorem_release/RELEASE_LOCK.json",
        "historical": root / "work/final_theorem_release/HISTORICAL_ARTIFACT_REGISTRY.json",
        "certificate": root / "work/adversarial_proof_review/topology_direction_certificate.json",
        "old_narrative": root / "work/adversarial_proof_review/TOPOLOGY_DIRECTIONAL_THEOREM.md",
        "forest": root / "work/restoration_sign_reclassification/corrected_restoration_forest.json",
        "supplement": root / "proof_compression_submission/supplement/supplement.tex",
    }
    data = {name: json.loads(path.read_text()) for name, path in paths.items()
            if path.suffix == ".json"}

    c02 = next(row for row in data["crosswalk"]["claims"]
               if row["claim_id"] == "C02-quartet-tree-of-blobs")
    cert_rows = [row for row in c02["authoritative_artifacts"]
                 if row["path"] == "work/adversarial_proof_review/topology_direction_certificate.json"]
    historical_rows = {row["path"]: row for row in data["historical"]["artifacts"]}
    old_path = "work/adversarial_proof_review/TOPOLOGY_DIRECTIONAL_THEOREM.md"
    old_registry = historical_rows[old_path]
    old_lock = data["lock"]["files"][old_path]
    cert_lock = data["lock"]["files"]["work/adversarial_proof_review/topology_direction_certificate.json"]
    forest = data["forest"]["census"]
    cert = data["certificate"]
    supp = paths["supplement"].read_text()
    old_text = paths["old_narrative"].read_text()

    expected_first = {
        "displayed_quartet_mismatch": 35758,
        "full_map_Ti_zero_strict_sign": 606,
        "exact_multihomogeneous_quadratic": 148,
        "inherited_exact_F_2_112_quartic": 24,
        "restore_remaining_physical_role": 32,
    }
    expected_second = {
        "displayed_quartet_mismatch": 248,
        "full_map_Ti_zero_strict_sign": 8,
    }
    checks = {
        "single_c02_certificate_row": len(cert_rows) == 1,
        "c02_certificate_digest_exact": len(cert_rows) == 1
        and cert_rows[0]["sha256"] == sha256(paths["certificate"]),
        "c02_role_disclaims_restoration_and_Ti": len(cert_rows) == 1
        and "no restoration or whole-map T_i authority" in cert_rows[0]["role"],
        "certificate_v2_schema": cert.get("schema") == "k2p-displayed-quartet-direction-audit-v2",
        "certificate_scope_raw_quartet_only": "raw four-port displayed-quartet" in cert.get("scope", "")
        and "no restoration or whole-map T_i classifier" in cert.get("scope", ""),
        "certificate_excludes_old_authorities": cert.get("excluded_claims") == [
            "rooted tree/sunlet classification",
            "restoration-child classification",
            "whole-map T_i classification",
        ],
        "certificate_omits_old_binding_fields": "published_ledgers" not in cert
        and "restoration_topology_binding" not in cert,
        "certificate_release_lock_exact": cert_lock["sha256"] == sha256(paths["certificate"])
        and cert_lock["layer"] == "quartet_tree_of_blobs",
        "old_narrative_still_contains_stale_counts": "646 restoration children" in old_text
        and "36,404 topology-terminal restoration children" in old_text,
        "old_narrative_historical_lock_layer": old_lock["layer"] == "historical_proof_provenance",
        "old_narrative_registry_revoked": old_registry["classification"]
        == "REVOKED_ROOTED_TOPOLOGY_ORACLE_NARRATIVE"
        and old_registry["promotion_authority"] is False,
        "old_narrative_digests_exact": old_lock["sha256"] == sha256(paths["old_narrative"])
        == old_registry["sha256"],
        "old_narrative_absent_from_c02_authority": all(
            row["path"] != old_path for row in c02["authoritative_artifacts"]
        ),
        "current_forest_first_partition": forest["first_proof_counts"] == expected_first,
        "current_forest_second_partition": forest["second_proof_counts"] == expected_second,
        "current_forest_totals": {
            key: forest[key]
            for key in ("first_children", "second_children", "forest_edges", "final_leaves")
        } == {
            "first_children": 36568,
            "second_children": 256,
            "forest_edges": 36824,
            "final_leaves": 36792,
        },
        "supplement_prints_current_partition": all(token in supp for token in (
            r"\text{quartet separator}&35,758",
            r"\text{whole-map \(\Ti\)}&606",
            r"\text{quadratic}&148",
            r"\text{transported quartic}&24",
            r"\text{continuation}&32",
            "36,824 edges, 36,792 exact separator leaves",
        )),
    }
    result = {
        "schema": "independent-k2p-c02-authority-audit-v2",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "current_counts": {
            "first": forest["first_proof_counts"],
            "second": forest["second_proof_counts"],
            "first_children": forest["first_children"],
            "second_children": forest["second_children"],
            "forest_edges": forest["forest_edges"],
            "final_leaves": forest["final_leaves"],
        },
        "authority": {
            "certificate_path": cert_rows[0]["path"] if cert_rows else None,
            "certificate_sha256": sha256(paths["certificate"]),
            "certificate_role": cert_rows[0]["role"] if cert_rows else None,
            "historical_path": old_path,
            "historical_sha256": sha256(paths["old_narrative"]),
            "historical_classification": old_registry["classification"],
            "historical_promotion_authority": old_registry["promotion_authority"],
        },
        "evidence_type": "provenance_and_authority_scoping; not a mathematical proof",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
