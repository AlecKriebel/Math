#!/usr/bin/env python3
"""Freeze the inspected PDF and a portable, exact verification archive."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / "verification"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    shutil.copyfile(ROOT / "manuscript/main.tex", PACKAGE / "manuscript/main.tex")
    run = subprocess.run([sys.executable, str(PACKAGE / "verify.py")],
                         capture_output=True, text=True, check=True)
    shutil.copyfile(PACKAGE / "results.json", PACKAGE / "expected_results.json")
    members = sorted(p for p in PACKAGE.rglob("*") if p.is_file()
                     and "__pycache__" not in p.parts
                     and p.name not in {"MANIFEST.json", "results.json"})
    manifest = {"schema": "canonical-W-D4-verification-archive-v1", "version": "1.0",
                "scope": "Attributed corrective note about the historical canonical-W converse; no first-priority or current-openness claim.",
                "files": [{"path": p.relative_to(PACKAGE).as_posix(),
                           "bytes": p.stat().st_size, "sha256": digest(p)} for p in members],
                "manifest_self_reference": "This manifest hashes every other archive member; its own hash is bound by BUILD_RECEIPT.json outside the archive."}
    (PACKAGE / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    members.append(PACKAGE / "MANIFEST.json")
    archive = ROOT / "Canonical_W_D4_Verification_v1.0.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as out:
        for path in sorted(members):
            info = zipfile.ZipInfo(path.relative_to(PACKAGE).as_posix(), date_time=(2026, 10, 17, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            out.writestr(info, path.read_bytes())
    pdf = ROOT / "Canonical_W_D4_Note_v1.0.pdf"
    shutil.copyfile(ROOT / "output/pdf/main.pdf", pdf)
    receipt = {"version": "1.0", "pdf": {"path": pdf.name, "bytes": pdf.stat().st_size, "sha256": digest(pdf)},
               "verification_zip": {"path": archive.name, "bytes": archive.stat().st_size, "sha256": digest(archive)},
               "manifest_sha256": digest(PACKAGE / "MANIFEST.json"),
               "manuscript_source_sha256": digest(ROOT / "manuscript/main.tex"),
               "verification_run": json.loads(run.stdout), "archive_members": len(members)}
    (ROOT / "BUILD_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
