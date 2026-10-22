#!/usr/bin/env python3
"""One-time repaired delivery build; all older artifacts retain before copies."""
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

AUDIT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
DELIVERY = AUDIT / "preprint_v1_0"
KIT = DELIVERY / "verification_kit"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(p, d):
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def main():
    for name in ["EXTERNAL_BINDING.json", "verification_kit.zip"]:
        old = DELIVERY / name
        before = WORK / "before/preprint_v1_0" / name
        if old.read_bytes() != before.read_bytes():
            raise RuntimeError("Refuse a repeated or ambiguous delivery mutation")
        old.unlink()
    argv = [sys.executable, "-I", "-B", str(KIT / "build_archive.py"), "--output", str(DELIVERY / "verification_kit.zip")]
    result = subprocess.run(argv, capture_output=True, text=True, timeout=120)
    dump(WORK / "ARCHIVE_BUILD_REPAIR01.json", {"argv": argv, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
    if result.returncode:
        raise RuntimeError("Current archive build failed: " + result.stderr)
    def row(name):
        p = DELIVERY / name
        return {"filename": name, "bytes": p.stat().st_size, "sha256": sha(p)}
    binding = {"schema_version": 2, "as_of_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "scope": "External noncircular repaired-candidate binding. Live wrapper, binding, PDF and ZIP are excluded from the current archive; captured older bytes inside are explicitly historical. No signature or human peer review is claimed.",
               "manifest_sha256": sha(KIT / "MANIFEST.json"),
               "metadata_sha256": sha(KIT / "metadata.json"),
               "research_metadata_sha256": sha(KIT / "research_metadata.json"),
               "deposit_manifest_sha256": sha(DELIVERY / "deposit_metadata.json"),
               "pdf": row("preprint.pdf"), "archive": row("verification_kit.zip"),
               "external_files": [row(n) for n in ["CURRENT_STATUS_REPAIR01.json", "README.md", "deposit_metadata.json", "metadata.json", "preprint.tex", "research_metadata.json"]]}
    dump(DELIVERY / "EXTERNAL_BINDING.json", binding)
    print(json.dumps({"archive": binding["archive"], "pdf_unchanged": binding["pdf"], "binding_sha256": sha(DELIVERY / "EXTERNAL_BINDING.json")}))


if __name__ == "__main__":
    main()
