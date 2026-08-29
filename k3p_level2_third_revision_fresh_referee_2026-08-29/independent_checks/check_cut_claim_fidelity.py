#!/usr/bin/env python3
"""Demonstrate whether nonfinal implication claims are semantically bound."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


AUDIT = Path(__file__).resolve().parents[1]
PROOF = AUDIT / "package_copy/proof_package"
HERE = PROOF / "cut_recovery/strong_crossbridge/global_transfer"
ORIGINAL = HERE / "K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json"
VERIFIER = HERE / "verify_global_transfer.py"
OUTPUT = AUDIT / "independent_checks/results/c1_claim_fidelity"


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to reuse {OUTPUT}")
    OUTPUT.mkdir(parents=True)
    evidence = json.loads(ORIGINAL.read_text(encoding="utf-8"))
    changed = []
    for row in evidence["analytic_implication"][:-1]:
        changed.append({"id": row["id"], "original_claim": row["claim"]})
        row["claim"] = "NONEMPTY_BUT_SEMANTICALLY_FALSE_PLACEHOLDER"
    body = dict(evidence)
    body.pop("payload_sha256", None)
    evidence["payload_sha256"] = hashlib.sha256(canonical(body)).hexdigest()
    mutant = OUTPUT / "MUTATED_CUT_EVIDENCE.json"
    mutant.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")

    runs = []
    for optimized in (False, True):
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.extend([
            str(VERIFIER), "--cut-evidence", str(mutant), "--mutations",
            "--no-write-report",
        ])
        result = subprocess.run(
            command, cwd=PROOF, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, check=False, timeout=600,
            env=dict(os.environ),
        )
        runs.append({
            "optimized": optimized,
            "command": command,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
        })

    accepted = all(row["returncode"] == 0 for row in runs)
    report = {
        "schema": "k3p-third-revision-cut-claim-fidelity-test-v1",
        "status": "VULNERABILITY_CONFIRMED" if accepted else "MUTANT_REJECTED",
        "interpretation": (
            "Both ordinary and optimized direct semantic verifiers accepted "
            "eight payload-resealed false-placeholder implication claims, "
            "while the global certificate still binds the default evidence."
            if accepted else
            "At least one direct verifier rejected the claim-body mutant."
        ),
        "changed_claims": changed,
        "final_claim_left_exact": evidence["analytic_implication"][-1]["claim"],
        "original_evidence_sha256": sha256(ORIGINAL),
        "mutant_evidence_sha256": sha256(mutant),
        "mutant_payload_sha256": evidence["payload_sha256"],
        "global_certificate_default_binding_not_rewritten": True,
        "runs": runs,
    }
    report_path = OUTPUT / "REPORT.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": report["status"], "accepted_runs": sum(
            row["returncode"] == 0 for row in runs
        ), "report_sha256": sha256(report_path),
    }, sort_keys=True))
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
