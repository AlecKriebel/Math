#!/usr/bin/env python3
"""Make the deterministic, authored-only publication archive from this audit."""
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
        if name in files:
            raise RuntimeError(f"Duplicate payload: {name}")
        if path.is_symlink():
            raise RuntimeError(f"Unexpected source symlink: {path}")
        if ".private" in path.name:
            raise RuntimeError(f"Private file cannot be packaged: {path.name}")
        files[name] = path.read_bytes()

    for name in ("support_slit.tex", "README.md", "CORRECTIONS.md", "BUILD.json",
                 "PDF_QA.json", "requirements.txt", "integrity.py", "run_all.py",
                 "JOBS.json", "SEALS.json"):
        add(name, PUB / name)
    add("metadata.json", PUB / "zenodo-deposit.json")
    add("CURRENT_PRIORITY_ASSESSMENT.json", AUDIT / "CURRENT_PRIORITY_ASSESSMENT.json")
    for name in ("USER_SUPPLIED_PRIMARY_SOURCES.json", "USER_PRIMARY_ROOT_NOTES.md",
                 "PRIMARY_SOURCE_ROOT_SEAL_CHECK.json", "PRIMARY_SOURCE_ROOT_REPLAY.json",
                 "PRIORITY09_ROOT_REPLAY.json", "PRIORITY10_ROOT_ACCEPTANCE.json",
                 "PRE_SUPPLIED_SOURCE_FREEZE_RECEIPT.json",
                 "GOH1992_SOURCE_RECEIPT.json", "GOH1992_ROOT_NOTES.md",
                 "GOH11_ROOT_ACCEPTANCE.json", "GOH12_ROOT_ACCEPTANCE.json",
                 "MANUSCRIPT_GOH_REVISION.json",
                 "USER_PRIORITY_LIMIT_AUTHORIZATION_20261014.json"):
        add(name, AUDIT / name)
    original = AUDIT / "original"
    for p in sorted(original.rglob("*")):
        if p.is_file() and p.suffix in (".md", ".json", ".py"):
            add("original/" + p.relative_to(original).as_posix(), p)
    for family in ("analytic01", "quantitative01", "source01", "priority02",
                   "priority03", "priority04_hib1996", "priority05_friedland1977",
                   "priority06_zemyan2003", "priority07_zemyan_bounds",
                   "priority08_radial_extrema", "priority09_commentary_citations",
                   "priority10_adversary", "priority11_goh1992_source",
                   "priority12_goh1992_adversary"):
        folder = AUDIT / "reviews" / family
        for p in sorted(folder.iterdir()):
            if p.is_file() and (p.suffix in (".md", ".json", ".jsonl", ".py")
                                or p.name == ".gitignore"):
                if ".private" not in p.name:
                    add(f"reviews/{family}/{p.name}", p)
    for p in sorted((AUDIT / "root_reproduction").iterdir()):
        if p.is_file() and p.suffix in (".md", ".json", ".py", ".tex"):
            if ".private" not in p.name:
                add("root_reproduction/" + p.name, p)
    registry = json.loads(files["SEALS.json"])
    nested_count = verify_nested(files, registry)
    manifest = {
        "problem_id": 2306072, "pr": 563,
        "head": "f3b23f6b2137a3a8eb25b7a20acbf7c98735b997",
        "nested_seals": registry,
        "files": {name: {"bytes": len(data),
                         "sha256": hashlib.sha256(data).hexdigest()}
                  for name, data in sorted(files.items())},
        "limits": "Authored proofs and evidence only. No third-party full text "
                  "or account data. Integrity is not authenticity or priority.",
    }
    files["MANIFEST.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    with tempfile.NamedTemporaryFile(dir=PUB, suffix=".zip", delete=False) as tmp:
        temporary = Path(tmp.name)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for name, data in sorted(files.items()):
                item = zipfile.ZipInfo("support_slit_verification/" + name,
                                       date_time=(2026, 10, 13, 12, 0, 0))
                item.compress_type = zipfile.ZIP_DEFLATED
                item.external_attr = 0o100644 << 16
                z.writestr(item, data)
        temporary.replace(PUB / "verification_package.zip")
    finally:
        temporary.unlink(missing_ok=True)
    (PUB / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    result = {
        "zip_sha256": hashlib.sha256(
            (PUB / "verification_package.zip").read_bytes()).hexdigest(),
        "zip_bytes": (PUB / "verification_package.zip").stat().st_size,
        "archive_members": len(files),
        "outer_payloads": len(manifest["files"]),
        "nested_entries": nested_count,
        "pdf_sha256": hashlib.sha256(
            (PUB / "support_slit.pdf").read_bytes()).hexdigest(),
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (PUB / "PACKAGE_BUILD.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
