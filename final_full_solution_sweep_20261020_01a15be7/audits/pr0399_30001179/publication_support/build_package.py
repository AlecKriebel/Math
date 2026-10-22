#!/usr/bin/env python3
"""Internal reversible packaging helper; never calls a provider or Git."""
import argparse
import datetime
import hashlib
import json
import pathlib
import shutil
import sys
import zipfile

sys.dont_write_bytecode = True
from integrity import load_json, require, safe_relative, verify_bundle


def digest(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def copy(source, target):
    require(source.is_file() and not source.is_symlink(), "copy source not a regular file")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def build(audit, destination):
    require(not destination.exists(), "refusing to overwrite an existing package")
    support = audit / "publication_support"
    snapshot = load_json(audit / "SOURCE_SNAPSHOT.json")
    originals = snapshot["files"]
    require(len(originals) == 11, "exactly eleven originals required")
    for record in originals:
        name = safe_relative(record["snapshot"])
        require(digest(audit / name) == {"bytes": record["bytes"], "sha256": record["sha256"]},
                "original differs from snapshot: " + name)
    seals = {"measure_ordinal": "6472625ee7f2305a0faaa2ec0e6abc4d4c26eddbe59ca181659016f58eca70dc",
             "continuity_core": "e0308083e2dab3d809d99bf086ae0d1d30b31334ecf73e93db44e113de450d32",
             "priority_source": "117a4af370051051871c77540b2ed6d87c66c10e305add289931c067d0935b86"}
    family_files = []
    for family, seal in seals.items():
        directory = audit / "reviews" / family
        manifest = directory / "AUTHORED_FILE_MANIFEST.json"
        require(digest(manifest)["sha256"] == seal, "family seal changed: " + family)
        entries = load_json(manifest)["files"]
        names = {"AUTHORED_FILE_MANIFEST.json", "AUTHORED_FILE_MANIFEST.sha256"}
        for entry in entries:
            name = safe_relative(entry["path"])
            require(type(entry["bytes"]) is int and entry["bytes"] >= 0,
                    "family byte count must be exact integer")
            require(digest(directory / name) == {"bytes": entry["bytes"], "sha256": entry["sha256"]},
                    "family payload changed: " + family + "/" + name)
            names.add(name)
        actual = {p.relative_to(directory).as_posix() for p in directory.rglob("*") if p.is_file()}
        # This one root-created ignored interpreter cache is not an authored
        # scientific artifact and is never copied into the public bundle.
        ignored_cache = {"__pycache__/fetch_sources.cpython-314.pyc"} if family == "priority_source" else set()
        require(actual - ignored_cache == names and not any(p.is_symlink() for p in directory.rglob("*")),
                "family inventory differs from seal: " + family)
        family_files.extend("reviews/%s/%s" % (family, name) for name in sorted(names))

    destination.mkdir(parents=True)
    for record in originals:
        copy(audit / record["snapshot"], destination / record["snapshot"])
    for name in family_files:
        copy(audit / name, destination / name)
    provenance = ["SOURCE_SNAPSHOT.json", "ROOT_ANALYTIC_ASSESSMENT.md",
                  "ROOT_SOURCE_READING_LEDGER.json", "ROOT_ORIGINAL_REPRODUCTION.json",
                  "ROOT_PRIORITY_SEARCH_CHECKPOINT.json", "ROOT_MEASURE_ORDINAL_ACCEPTANCE.json",
                  "ROOT_CONTINUITY_CORE_ACCEPTANCE.json", "ROOT_PRIORITY_ACCEPTANCE.json",
                  "ROOT_SCIENTIFIC_REVIEW_ACCEPTANCE.json"]
    for name in provenance:
        copy(audit / name, destination / "provenance" / name)
    for name in ("integrity.py", "reproduce.py", "test_integrity_controls.py"):
        copy(support / name, destination / "tools" / name)
    for source, target in ((support / "BUNDLE_README.md", "README.md"),
                           (support / "REPRODUCE.md", "REPRODUCE.md"),
                           (support / "CODE_LICENSE.txt", "CODE_LICENSE.txt"),
                           (audit / "preprint/LICENSE.txt", "LICENSE.txt"),
                           (audit / "preprint/CITATION.cff", "CITATION.cff"),
                           (audit / "preprint/main.tex", "manuscript/main.tex"),
                           (support / "SOURCE_REFERENCE_LEDGER.json", "source/SOURCE_REFERENCE_LEDGER.json"),
                           (support / "PDF_QA_RECEIPT.json", "receipts/PDF_QA_RECEIPT.json"),
                           (support / "INTEGRITY_CONTROL_RECEIPT.json", "receipts/INTEGRITY_CONTROL_RECEIPT.json")):
        copy(source, destination / target)
    entries = [dict(path=p.relative_to(destination).as_posix(), **digest(p))
               for p in sorted(destination.rglob("*")) if p.is_file()]
    (destination / "FILES.json").write_text(json.dumps({"schema": 1, "files": entries}, indent=2) + "\n")
    result = verify_bundle(destination)
    result["preserved_originals"] = len(originals)
    result["preserved_family_payloads"] = sum(len(load_json(audit / "reviews" / f / "AUTHORED_FILE_MANIFEST.json")["files"]) for f in seals)
    return result


def zip_package(destination, archive):
    require(not archive.exists(), "refusing to overwrite existing archive")
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for path in sorted(destination.rglob("*")):
            if path.is_file():
                name = destination.name + "/" + path.relative_to(destination).as_posix()
                info = zipfile.ZipInfo(name, date_time=(2026, 10, 21, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                output.writestr(info, path.read_bytes())
    return digest(archive)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit", type=pathlib.Path)
    parser.add_argument("destination", type=pathlib.Path)
    parser.add_argument("archive", type=pathlib.Path)
    args = parser.parse_args()
    result = build(args.audit, args.destination)
    result["archive"] = zip_package(args.destination, args.archive)
    result["publication_ready"] = False
    result["timestamp_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(json.dumps(result, indent=2, sort_keys=True))
