#!/usr/bin/env python3
"""Assemble the explicit owned publication set; omit research caches and secrets."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

PROJECT = Path(__file__).resolve().parents[1]
KIT = PROJECT / "publication" / "upload-kit"
EPOCH = "1791347194"


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    KIT.mkdir(exist_ok=True)
    selected = {
        "main.tex": "manuscript/main.tex",
        "upstream-citations.bib": "manuscript/upstream-citations.bib",
        "README.md": "publication/README.md",
        "VALIDATION.md": "publication/VALIDATION.md",
        "DEPENDENCY_LEDGER.md": "DEPENDENCY_LEDGER.md",
        "UPSTREAM_MANIFEST.json": "sources/UPSTREAM_MANIFEST.json",
        "FORMAL_SCOPE.md": "checks/FORMAL_SCOPE.md",
        "reproduce.py": "checks/reproduce.py",
        "supplement/conditional-transfer.md": "manuscript/CONDITIONAL_TRANSFER.md",
        "audit/PRIORITY_AUDIT.md": "agent_notes/priority_audit.md",
        "audit/analytic_falsification.md": "reviews/analytic_falsification.md",
        "audit/corner_rederive.md": "checks/analytic_falsification/corner_rederive.md",
        "audit/ordinary_hms_verifier.md": "reviews/ordinary_hms_verifier.md",
    }
    for name in ["bulles_transfer", "mixed_k3_audit", "ks_tensor_audit",
                 "ks_geometry_audit", "realization_audit", "cm_theta_audit",
                 "root_cm_and_deformation_audit"]:
        selected[f"audit/{name}.md"] = f"agent_notes/{name}.md"
    for name in ["cm_arithmetic_falsification", "cm_finite_locus_falsification"]:
        selected[f"audit/{name}.md"] = f"agent_notes/{name}.md"
    for name in ["verify_local_spin_pairing.py", "verify_graph_signs.py",
                 "local_spin_pairing_certificate.json", "graph_sign_certificate.json"]:
        selected[f"checks/{name}"] = f"checks/mixed_k3_audit/{name}"
    selected["checks/check_finite_sign_identities.py"] = "checks/realization_audit/check_finite_sign_identities.py"
    for name in ["check_identities.py", "identity_results.json"]:
        selected[f"checks/{name}"] = f"checks/analytic_falsification/{name}"
    for name in ["verify_hecke_counts.py", "hecke_counts.json"]:
        selected[f"checks/{name}"] = f"checks/cm_arithmetic/{name}"
    with tempfile.TemporaryDirectory(prefix="assemble-", dir=PROJECT / "checks" / "builds") as raw:
        root = Path(raw)
        hashes = {}
        for name, relative in selected.items():
            source = PROJECT / relative
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            hashes[name] = digest(target)
        (root / "ARCHIVE_MAP.json").write_text(json.dumps(selected, sort_keys=True, indent=2) + "\n")
        hashes["ARCHIVE_MAP.json"] = digest(root / "ARCHIVE_MAP.json")
        (root / "SHA256SUMS.json").write_text(json.dumps(hashes, sort_keys=True, indent=2) + "\n")
        env = os.environ.copy()
        env["SOURCE_DATE_EPOCH"] = EPOCH
        env["FORCE_SOURCE_DATE"] = "1"
        # The runner builds from another clean directory and verifies all selected files.
        built = subprocess.run([os.sys.executable, "reproduce.py"], cwd=root,
                               env=env, check=True, capture_output=True, text=True)
        report = json.loads(built.stdout)
        shutil.copy2(root / "reproduced" / "paper.pdf", KIT / "paper.pdf")
        (PROJECT / "publication" / "clean-build.json").write_text(json.dumps(report, indent=2) + "\n")
        with zipfile.ZipFile(KIT / "source-and-verification.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name in sorted([*selected, "ARCHIVE_MAP.json", "SHA256SUMS.json"]):
                info = zipfile.ZipInfo(name, date_time=(2026, 10, 6, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, (root / name).read_bytes())
    files = [{"name": name, "bytes": (KIT / name).stat().st_size,
              "sha256": digest(KIT / name)}
             for name in ["paper.pdf", "source-and-verification.zip"]]
    (PROJECT / "publication" / "artifact-manifest.json").write_text(
        json.dumps({"files": files, "source_files": hashes}, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"files": files, "clean_build": report}, indent=2))


if __name__ == "__main__":
    main()
