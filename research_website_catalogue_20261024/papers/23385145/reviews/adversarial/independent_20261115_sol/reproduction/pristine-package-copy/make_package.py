#!/usr/bin/env python3
"""Deterministically package explicit authored evidence, preserving every seal."""
import hashlib
import json
from pathlib import Path
import tempfile
import zipfile
from integrity import safe_path, verify_nested

PUB = Path(__file__).resolve().parent
AUDIT = PUB.parent


def main():
    files = {}

    def add(name, path):
        safe_path(name)
        if name in files or path.is_symlink() or ".private" in path.name:
            raise RuntimeError(f"Invalid or duplicate source: {name}")
        # Checkout ancestors are irrelevant, but both source spellings matter:
        # resolving an internal alias must not erase an excluded directory.
        try:
            relative = path.relative_to(AUDIT)
            resolved = path.resolve().relative_to(AUDIT)
        except ValueError as exc:
            raise RuntimeError(f"Source escapes the audit: {name}") from exc
        components = (*relative.parts, *resolved.parts, *safe_path(name).parts)
        if any(part in (".cache", "sources", "scratch", "qa", ".secrets") for part in components):
            raise RuntimeError(f"Excluded source: {name}")
        files[name] = path.read_bytes()

    for name in ("weighted_centers.tex", "README.md", "CORRECTIONS.md", "BUILD.json",
                 "PDF_QA.json", "requirements.txt", "integrity.py", "run_all.py",
                 "make_package.py", "JOBS.json", "SEALS.json"):
        add(name, PUB / name)
    add("metadata.json", PUB / "zenodo-deposit.json")
    for name in ("ORIGINAL_SNAPSHOT.json", "CURRENT_PRIORITY_ASSESSMENT.json",
                 "ROOT_MATH_ACCEPTANCE.md", "ROOT_PRIORITY_CHECKPOINT.md",
                 "ROOT_SOURCE_RECEIPT.json", "ROOT_PUBLISHED_ESA_RECEIPT.json",
                 "ROOT_CUBEFREE_SOURCE_RECEIPT.json", "PRIORITY01_ROOT_ACCEPTANCE.json",
                 "PRIORITY02_ROOT_ACCEPTANCE.json"):
        add(name, AUDIT / name)
    snapshot = json.loads((AUDIT / "ORIGINAL_SNAPSHOT.json").read_text())
    for record in snapshot["files"]:
        name = safe_path(record["path"]).as_posix()
        add("original/" + name, AUDIT / "original" / name)
    for family in ("oracle01", "search01", "priority01", "priority02"):
        folder = AUDIT / "reviews" / family
        add(f"reviews/{family}/SHA256SUMS", folder / "SHA256SUMS")
        for line in (folder / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split("  ", 1)
            safe_path(name)
            add(f"reviews/{family}/{name}", folder / name)
    for path in sorted((AUDIT / "root_reproduction").iterdir()):
        if path.is_file() and path.suffix in (".json", ".md", ".py"):
            add("root_reproduction/" + path.name, path)
    registry = json.loads(files["SEALS.json"])
    nested, original = verify_nested(files, registry)
    manifest = {
        "pr": 570, "problem_id": 30006605,
        "head": "417ca52e83cf06b07c388d89c756cfd86473d5b0",
        "nested_seals": registry,
        "files": {name: {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                  for name, data in sorted(files.items())},
        "limits": "Authored evidence only, no raw third-party sources/account data. Integrity is not authenticity, historical firstness or formal/human certification.",
    }
    files["MANIFEST.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(dir=PUB, suffix=".zip", delete=False) as temporary:
        tmp = Path(temporary.name)
    try:
        with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in sorted(files.items()):
                item = zipfile.ZipInfo("weighted_centers_verification/" + name,
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
              "nested_entries": nested, "original_inputs": original,
              "pdf_sha256": hashlib.sha256((PUB / "weighted_centers.pdf").read_bytes()).hexdigest(),
              "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (PUB / "PACKAGE_BUILD.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
