#!/usr/bin/env python3
"""Refresh only this unsealed repair edition after documentation correction."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parent
AUDIT = WORK.parents[1]
DELIVERY = AUDIT / "preprint_v1_0"
KIT = DELIVERY / "verification_kit"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    binding = json.loads((DELIVERY / "EXTERNAL_BINDING.json").read_text())
    if sha(DELIVERY / "verification_kit.zip") != binding["archive"]["sha256"]:
        raise RuntimeError("Refuse unrelated archive mutation")
    (WORK / "INTERMEDIATE_BINDING_BEFORE_DOC_CORRECTION.json").write_text(json.dumps(binding, indent=2) + "\n")
    (DELIVERY / "EXTERNAL_BINDING.json").unlink()
    (DELIVERY / "verification_kit.zip").unlink()
    r = subprocess.run([sys.executable, "-I", "-B", str(KIT / "build_archive.py"), "--output", str(DELIVERY / "verification_kit.zip")], capture_output=True, text=True, timeout=120)
    (WORK / "FINAL_ARCHIVE_BUILD_REPAIR01.json").write_text(json.dumps({"returncode": r.returncode, "stdout": r.stdout, "stderr": r.stderr}, indent=2) + "\n")
    if r.returncode:
        raise RuntimeError(r.stderr)
    binding["manifest_sha256"] = sha(KIT / "MANIFEST.json")
    archive = DELIVERY / "verification_kit.zip"
    binding["archive"].update(bytes=archive.stat().st_size, sha256=sha(archive))
    for row in binding["external_files"]:
        p = DELIVERY / row["filename"]
        row.update(bytes=p.stat().st_size, sha256=sha(p))
    (DELIVERY / "EXTERNAL_BINDING.json").write_text(json.dumps(binding, indent=2, ensure_ascii=False) + "\n")
    for n in ["REPRODUCTION_RECEIPTS.jsonl", "REPRODUCTION_SUMMARY.json", "ARCHIVE_PAYLOAD_CHECKS.json", "REPOSITORY_LOCAL_CHECK.json"]:
        (WORK / n).rename(WORK / ("INITIAL_" + n))
    print(json.dumps(binding["archive"]))


if __name__ == "__main__":
    main()
