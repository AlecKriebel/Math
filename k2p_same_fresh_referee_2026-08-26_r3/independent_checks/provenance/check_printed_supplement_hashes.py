#!/usr/bin/env python3
"""Compare printed supplement artifact hashes with the packaged bytes.

This reviewer check imports no submission code.  It parses the two compact
hash presentations in supplement.tex and hashes the referenced files itself.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


AUTHORITY_RE = re.compile(
    r"authority:\s*\\path\{([^}]+)\};\s*"
    r"SHA-256:\s*\\hashvalue\{([0-9a-f]{64})\}",
    re.MULTILINE,
)

FROZEN_ANCHORS = {
    "unified release lock": "work/final_theorem_release/RELEASE_LOCK.json",
    "raw-four composite ledger": "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz",
    "raw-four independent replay": "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_independent_replay.json",
    "raw-four terminal registry": "work/raw4_sign_reclassification/raw4_corrected_terminal_ledger.json",
    "raw-four mutation report": "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_mutations.json",
    "five-port \\(\\theta_2\\) composite ledger": "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_ledger.jsonl.gz",
    "five-port independent replay": "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_independent_replay.json",
    "five-port mutation report": "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_mutations.json",
    "full-map certificate reseal audit": "work/final_theorem_release/full_map_reseal_audit.json",
    "composite reseal differential audit": "work/final_theorem_release/composite_reseal_diff_audit.json",
    "corrected 997-parent forest": "work/restoration_sign_reclassification/corrected_restoration_forest.json",
    "restoration independent replay": "work/restoration_sign_reclassification/corrected_restoration_replay_certificate.json",
    "probe input contract": "work/adversarial_proof_review/probe_input_contract.json",
    "full probe primary": "work/probe_coherence_corrected/probe_coherence_certificate.json",
    "full probe independent graph audit": "work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit_certificate.json",
    "full probe adversarial mutation report": "work/global_proof_adversary/probe_full_audit/independent_probe_mutation_report.json",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    source = project / "proof_compression_submission/supplement/supplement.tex"
    text = source.read_text()

    rows = []
    for match in AUTHORITY_RE.finditer(text):
        rel, printed = match.groups()
        path = project / rel
        actual = sha256(path) if path.is_file() else None
        rows.append({
            "presentation": "authority-table",
            "label": rel,
            "path": rel,
            "line": text.count("\n", 0, match.start()) + 1,
            "printed_sha256": printed,
            "actual_sha256": actual,
            "status": "PASS" if actual == printed else "FAIL",
        })

    for label, rel in FROZEN_ANCHORS.items():
        pattern = re.compile(
            re.escape(label) + r"\s*&\s*\\hashvalue\{([0-9a-f]{64})\}",
            re.MULTILINE,
        )
        match = pattern.search(text)
        if match is None:
            rows.append({
                "presentation": "frozen-anchor-table",
                "label": label,
                "path": rel,
                "line": None,
                "printed_sha256": None,
                "actual_sha256": sha256(project / rel) if (project / rel).is_file() else None,
                "status": "MISSING",
            })
            continue
        printed = match.group(1)
        actual = sha256(project / rel) if (project / rel).is_file() else None
        rows.append({
            "presentation": "frozen-anchor-table",
            "label": label,
            "path": rel,
            "line": text.count("\n", 0, match.start()) + 1,
            "printed_sha256": printed,
            "actual_sha256": actual,
            "status": "PASS" if actual == printed else "FAIL",
        })

    failures = [row for row in rows if row["status"] != "PASS"]
    result = {
        "schema": "independent-printed-supplement-hash-audit-v1",
        "source": str(source.relative_to(project)),
        "source_sha256": sha256(source),
        "rows_checked": len(rows),
        "failure_count": len(failures),
        "failures": failures,
        "status": "PASS" if not failures else "FAIL",
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "failure_count": len(failures), "payload_sha256": result["payload_sha256"]}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
