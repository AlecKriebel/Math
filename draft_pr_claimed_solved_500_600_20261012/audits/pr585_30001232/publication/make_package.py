#!/usr/bin/env python3
"""Deterministic authored-only package; explicit selections, pinned originals."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import zipfile
sys.dont_write_bytecode = True
from integrity import safe_path, verify_nested

PUB = Path(__file__).resolve().parent
AUDIT = PUB.parent
ROOT_FILES = ['ORIGINAL_SNAPSHOT.json', 'CURRENT_PRIORITY_ASSESSMENT.json', 'CURRENT_CORRECTIONS.md', 'ROOT_EARLY_PROOF.md', 'ROOT_MATH_ACCEPTANCE.md', 'ROOT_SOURCE_RECEIPT.json', 'ROOT_SOURCE_INTAKE.json', 'ROOT_FUENTES_INTAKE.json', 'ROOT_BAUER_SZEMBERG2010_INTAKE.json', 'ROOT_ADDITIONAL_PRIORITY_INTAKE.json', 'PRIORITY01_ROOT_ACCEPTANCE.json', 'PRIORITY02_ROOT_ACCEPTANCE.json', 'verify_original_snapshot.py', 'test_snapshot_gate.py']
REPLAY_FILES = ['GEOMETRY01_ROOT_REPLAY.json', 'PENCIL01_ROOT_REPLAY.json', 'ORIGINAL_FULL_REPLAY.json', 'verify_release.py.stdout.json', 'verify_release.py.stderr.txt', 'test_integrity.py.stdout.json', 'test_integrity.py.stderr.txt', 'ORIGINAL_STRICT_BASELINE.json', 'ORIGINAL_STRICT_REGRESSION.json']


def main():
    files = {}

    def add(name, path):
        safe_path(name)
        if name in files or path.is_symlink():
            raise RuntimeError(f"Invalid or duplicate source: {name}")
        try:
            relative = path.relative_to(AUDIT)
            resolved = path.resolve().relative_to(AUDIT)
        except ValueError as exc:
            raise RuntimeError(f"Source escapes the audit: {name}") from exc
        components = (*relative.parts, *resolved.parts, *safe_path(name).parts)
        if any(part in (".cache", "sources", "scratch", "qa", ".secrets")
               or ".private" in part for part in components):
            raise RuntimeError(f"Excluded source: {name}")
        files[name] = path.read_bytes()

    for name in ("seshadri_counterexample.tex", "README.md", "CORRECTIONS.md", "BUILD.json",
                 "PDF_QA.json", "requirements.txt", "integrity.py", "run_all.py",
                 "make_package.py", "JOBS.json", "SEALS.json"):
        add(name, PUB / name)
    add("metadata.json", PUB / "zenodo-deposit.json")
    for name in ROOT_FILES:
        add(name, AUDIT / name)
    snapshot = json.loads((AUDIT / "ORIGINAL_SNAPSHOT.json").read_text())
    # This independent literal binding precedes any use of the snapshot list.
    sys.path.insert(0, str(AUDIT))
    from verify_original_snapshot import verify
    verify(AUDIT)
    for record in snapshot["files"]:
        name = safe_path(record["path"]).as_posix()
        add("original/" + name, AUDIT / "original" / name)
    for family in ("geometry01", "pencil01", "priority01", "priority02"):
        folder = AUDIT / "reviews" / family
        add(f"reviews/{family}/SHA256SUMS", folder / "SHA256SUMS")
        for line in (folder / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split("  ", 1)
            safe_path(name)
            add(f"reviews/{family}/{name}", folder / name)
    for name in REPLAY_FILES:
        add("root_reproduction/" + name, AUDIT / "root_reproduction" / name)
    registry = json.loads(files["SEALS.json"])
    nested, original = verify_nested(files, registry)
    manifest = {
        "pr": 585, "problem_id": 30001232,
        "head": "0a94b2a7e8d682af7d51a3fba7fe8df4a36f6f27",
        "nested_seals": registry,
        "files": {name: {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                  for name, data in sorted(files.items())},
        "limits": "Authored evidence only; raw source/cache/account data excluded. Integrity is not authenticity, historical firstness, geometry, formal verification or human certification.",
    }
    files["MANIFEST.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(dir=PUB, suffix=".zip", delete=False) as temporary:
        tmp = Path(temporary.name)
    try:
        with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in sorted(files.items()):
                item = zipfile.ZipInfo("seshadri_counterexample_verification/" + name,
                                       date_time=(2026, 10, 15, 0, 0, 0))
                item.compress_type = zipfile.ZIP_DEFLATED
                item.external_attr = 0o100644 << 16
                archive.writestr(item, data)
        tmp.replace(PUB / "verification_package.zip")
    finally:
        tmp.unlink(missing_ok=True)
    (PUB / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    result = {"zip_sha256": hashlib.sha256((PUB / "verification_package.zip").read_bytes()).hexdigest(),
              "zip_bytes": (PUB / "verification_package.zip").stat().st_size,
              "archive_members": len(files), "outer_payloads": len(manifest["files"]),
              "nested_entries": nested, "nested_seals": len(registry), "original_inputs": original,
              "pdf_sha256": hashlib.sha256((PUB / "seshadri_counterexample.pdf").read_bytes()).hexdigest(),
              "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (PUB / "PACKAGE_BUILD.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
