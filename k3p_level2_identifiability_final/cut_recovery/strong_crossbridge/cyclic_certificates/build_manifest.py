#!/usr/bin/env python3
"""Build the theorem-facing manifest after exact replay succeeds."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
CERTIFICATE = HERE / "CYCLIC_SIX_MINOR_CERTIFICATES.json"
REPORT = HERE / "VERIFICATION_REPORT.json"
OPTIMIZED_REPORT = HERE / "OPTIMIZED_VERIFICATION_REPORT.json"
OUTPUT = HERE / "THEOREM_MANIFEST.json"
SHA_MANIFEST = HERE / "MANIFEST.sha256"
PACKAGE_FILES = (
    "CYCLIC_SIX_MINOR_CERTIFICATES.json",
    "VERIFICATION_REPORT.json",
    "OPTIMIZED_VERIFICATION_REPORT.json",
    "generate_cyclic_certificates.py",
    "verify_cyclic_certificates.py",
    "build_manifest.py",
    "README.md",
    "WORK_LOG.md",
)


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def sha_file(path: Path) -> str:
    answer = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            answer.update(block)
    return answer.hexdigest()


def main():
    certificate = json.loads(CERTIFICATE.read_text())
    report = json.loads(REPORT.read_text())
    optimized_report = json.loads(OPTIMIZED_REPORT.read_text())
    require(certificate["status"] == report["status"] == "PASS", "replay status")
    require(report["artifact_sha256"] == sha_file(CERTIFICATE), "artifact/report binding")
    require(report["verifier_sha256"] == sha_file(HERE / "verify_cyclic_certificates.py"), "verifier/report binding")
    require(report["identity_count"] == certificate["identity_count"] == 30, "identity count")
    require(report["mutation_count"] == 40, "mutation count")
    require(report["target117_identity_crosswalks"] == 3, "target117 audit crosswalk")
    require(report["python_optimized"] is False, "ordinary replay mode")
    require(optimized_report["status"] == "PASS", "optimized replay status")
    require(optimized_report["python_optimized"] is True, "optimized replay mode")
    require(optimized_report["artifact_sha256"] == sha_file(CERTIFICATE), "optimized artifact binding")
    require(optimized_report["verifier_sha256"] == sha_file(HERE / "verify_cyclic_certificates.py"), "optimized verifier binding")
    require(optimized_report["mutation_count"] == 40, "optimized mutation count")

    file_hashes = {name: sha_file(HERE / name) for name in PACKAGE_FILES}
    manifest = {
        "schema": "k3p-cyclic-six-minor-theorem-manifest-v1",
        "status": "PASS",
        "scope": {
            "universe": "graph-derived one-active wrong-split four-port K3P target directions",
            "target_indices": certificate["target_indices"],
            "target_count": certificate["record_count"],
            "identity_count": certificate["identity_count"],
            "domain": "strict principal K3P edge domain and inheritance parameters in (0,1)",
        },
        "certified_claim": (
            "For each listed target direction, the normalized 01|23 Fourier "
            "flattening has rank greater than four at every strict principal-domain "
            "parameter point."
        ),
        "proof_mechanism": (
            "Six selected minors obey three exact cyclic identities with strictly "
            "positive multipliers; simultaneous vanishing would make each of three "
            "positive negative-log spectra the absolute difference of the other two, "
            "contradicting the equation for the largest."
        ),
        "validation": {
            "exact_identity_replays": report["identity_count"],
            "strict_log_orderings_checked": report["strict_log_orderings_checked"],
            "target117_independent_audit_crosswalks": report["target117_identity_crosswalks"],
            "adversarial_mutations_rejected": report["mutation_count"],
            "optimized_python_replay": optimized_report["status"],
            "producer_imported_by_verifier": report["producer_imported"],
        },
        "limitations": (
            "This package certifies only the ten listed target directions; it does "
            "not by itself prove the finite-universe reduction or the global theorem."
        ),
        "files": file_hashes,
        "upstream_inputs": certificate["inputs"],
        "independent_target117_audit": certificate["target117_independent_audit"],
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    temporary.replace(OUTPUT)

    all_files = PACKAGE_FILES + ("THEOREM_MANIFEST.json",)
    lines = [f"{sha_file(HERE / name)}  {name}" for name in all_files]
    temporary_sha = SHA_MANIFEST.with_suffix(".sha256.tmp")
    temporary_sha.write_text("\n".join(lines) + "\n")
    temporary_sha.replace(SHA_MANIFEST)
    print(json.dumps({"status": "PASS", "files": len(all_files), "target_count": 10, "identity_count": 30}, sort_keys=True))


if __name__ == "__main__":
    main()
