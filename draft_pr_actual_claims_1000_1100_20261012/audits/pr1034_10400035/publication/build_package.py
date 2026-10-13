#!/usr/bin/env python3
"""Package pinned authored records; no proof replay or external action.

Determinism: fixed input bytes, ordered names, fixed ZIP timestamps/modes,
stored entries, canonical JSON. The PDF is an input, not a build product.
All paths and outputs stay within this one audit directory.
"""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

PUB = Path(__file__).resolve().parent
ROOT = PUB.parent
GENERATED = {
    "publication/PACKAGE_MANIFEST.json",
    "publication/CANDIDATE_INTEGRITY.json",
    "publication/source_audit_kit.zip",
    "publication/PACKAGE_INPUT_PINS.json",
}
ALLOWED_SUFFIXES = {".md", ".json", ".py", ".tex"}
FORBIDDEN_PARTS = {"raw", "rawprivate", "private", "cache", "caches", "__pycache__", "tmp", "duplicateinputarchives"}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")


def record(name, data):
    return {"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def safe_read(name):
    pp = PurePosixPath(name)
    require(not pp.is_absolute() and ".." not in pp.parts and str(pp) == name,
            "unsafe path: " + name)
    require(not (set(x.lower() for x in pp.parts) & FORBIDDEN_PARTS),
            "forbidden directory: " + name)
    require("private_raw" not in name.lower() and "raw_private" not in name.lower(),
            "private raw inventory is not public payload: " + name)
    require(name not in GENERATED, "generated file must not be recursively packaged: " + name)
    require(pp.suffix.lower() in ALLOWED_SUFFIXES or name == "publication/research_note.pdf",
            "forbidden body/extract/image/cache/archive type: " + name)
    path = ROOT / name
    require(path.is_file() and not path.is_symlink(), "missing file or symlink: " + name)
    require(path.resolve().is_relative_to(ROOT), "escaped root: " + name)
    data = path.read_bytes()
    if pp.suffix.lower() != ".pdf":
        data.decode("utf-8")
    else:
        require(data.startswith(b"%PDF-"), "manuscript output is not PDF")
    return data


def main():
    allow = json.loads((PUB / "PACKAGE_ALLOWLIST.json").read_text())
    names = allow["files"]
    require(names == sorted(set(names)), "allowlist must be sorted and unique")
    files = {name: safe_read(name) for name in names}
    pins = json.loads((PUB / "PACKAGE_INPUT_PINS.json").read_text())
    rows = [record(name, files[name]) for name in names]
    require(pins["files"] == rows, "pinned candidate bytes changed: refresh requires another review")

    original = json.loads(files["SUBMITTED_PINS.json"])
    require(original["head_oid"] == "86d076dae3e3fa8b7cda7fd9c6a822c3d7392c14", "wrong original head")
    require(len(original["files"]) == 19, "wrong original file count")
    expected_originals = {r["snapshot_path"] for r in original["files"]}
    actual_originals = {"submitted/" + x.name for x in (ROOT / "submitted").iterdir()}
    require(actual_originals == expected_originals, "original theoretical file set changed")
    require(expected_originals.issubset(files), "omitted original authored file")
    for r in original["files"]:
        actual = record(r["snapshot_path"], files[r["snapshot_path"]])
        require(actual["sha256"] == r["sha256"] and actual["bytes"] == r["bytes"],
                "original changed: " + r["snapshot_path"])

    metadata = json.loads(files["publication/metadata.json"])
    wrapper = json.loads(files["publication/zenodo_metadata_wrapper.json"])
    require(wrapper == {"metadata": metadata}, "Zenodo wrapper differs from exact metadata")
    require(metadata["title"] == "Finite-type invariants on free-exterior string links: low-degree restrictions and an order-seven example", "wrong current title")
    require(metadata["version"] == "1.0" and metadata["publication_date"] == "2026-10-13", "wrong edition identity")
    require(metadata["creators"][0]["orcid"] == "0009-0001-9320-500X", "wrong author ORCID")
    require(metadata["license"] == "cc-by-4.0", "wrong license")
    state = json.loads(files["publication/evidence/CURRENT_REVIEW_STATE.json"])
    require(state["publication_ready"] is False and state["required_review"] == "NEWwhole01",
            "this preparation builder binds the pending NEWwhole01 candidate only")
    require(state["state"] == "PENDING_NEW_WHOLE_PACKAGE_REVIEW", "wrong stage")

    manifest = {
        "schema": "authored-candidate-noncircular-manifest-v1",
        "original_head": original["head_oid"],
        "stage": "prepared_application_note_pending_NEWwhole01",
        "publication_ready": False,
        "files": rows,
        "hash_scope": "All allowlisted authored payload files. This manifest is included in the archive but excludes itself from the file hashes. Input pins and the external integrity receipt are outside the archive.",
        "source_body_policy": "No raw/private third-party bodies, verbatim extracts, OCR, images, caches, bytecode, or duplicate input archives.",
    }
    manifest_data = json_bytes(manifest)
    manifest_name = "publication/PACKAGE_MANIFEST.json"
    (PUB / "PACKAGE_MANIFEST.json").write_bytes(manifest_data)
    archive_files = {**files, manifest_name: manifest_data}
    archive = PUB / "source_audit_kit.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as zf:
        for name in sorted(archive_files):
            zi = zipfile.ZipInfo(name, date_time=(2026, 10, 13, 0, 0, 0))
            zi.create_system = 3
            zi.external_attr = 0o100644 << 16
            zi.compress_type = zipfile.ZIP_STORED
            zf.writestr(zi, archive_files[name])
    with zipfile.ZipFile(archive) as zf:
        require(zf.testzip() is None, "archive CRC failure")
        require(zf.namelist() == sorted(archive_files), "archive names differ")
        for name, data in archive_files.items():
            require(zf.read(name) == data, "archived bytes differ: " + name)
    integrity = {
        "schema": "authored-candidate-external-integrity-v1",
        "publication_ready": False,
        "required_review": "NEWwhole01",
        "original_files_byte_verified": 19,
        "payload_files": len(rows),
        "archive_entries_including_internal_manifest": len(archive_files),
        "manifest": record(manifest_name, manifest_data),
        "input_pins": record("publication/PACKAGE_INPUT_PINS.json", (PUB / "PACKAGE_INPUT_PINS.json").read_bytes()),
        "archive": record("publication/source_audit_kit.zip", archive.read_bytes()),
        "metadata_wrapper_exact": True,
        "zip_crc_and_every_entry_readback": True,
        "determinism": "sorted names; fixed timestamp; fixed regular-file mode; ZIP_STORED; frozen input bytes; canonical generated JSON; no runtime timestamp",
        "proof_execution": "none; frozen new arithmetic records are supplementary stage evidence",
        "external_actions": "none",
    }
    (PUB / "CANDIDATE_INTEGRITY.json").write_bytes(json_bytes(integrity))
    print(json.dumps(integrity, indent=2))


if __name__ == "__main__":
    main()
