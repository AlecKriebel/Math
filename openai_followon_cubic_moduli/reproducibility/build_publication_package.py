#!/usr/bin/env python3
"""Build two exact Zenodo payloads from an explicit, hash-frozen selection.

Standard library only. No network, credentials, Git, LaTeX compilation, or
deposit operations. --plan is read-only. --build requires a final frozen
selection and final metadata; it never rewrites the manuscript or input PDF.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
REQUIRED = {
    "main.tex", "sources/PINNED_MANIFEST.json",
    "reproducibility/build_publication_package.py",
    "reproducibility/build_paper.py",
    "reproducibility/verify_constants.py",
    "reproducibility/verify_boundary_examples.py",
    "publication/LICENSES.md", "publication/SOURCE_PROVENANCE.json",
    "publication/README_FOR_DEPOSIT.md",
    "publication/THEOREMS_AND_DEPENDENCIES.md",
}
ALLOWED_ROOTS = {"agent_notes", "reviews", "receipts", "reproducibility", "publication"}
ALLOWED_ROOT_FILES = {"main.tex"}
RESERVED = {"README.md", "SOURCE_SHA256SUMS.txt", "publication/metadata.json", "publication/package_selection.json"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def safe_project_file(name: str, *, paper: bool = False) -> Path:
    if not isinstance(name, str) or not name or "\\" in name or any(ord(c) < 32 or ord(c) == 127 for c in name):
        raise ValueError(f"invalid project-relative filename: {name!r}")
    part = PurePosixPath(name)
    if part.is_absolute() or str(part) != name or any(p in {".", ".."} or p.startswith(".") for p in part.parts):
        raise ValueError(f"unsafe project-relative filename: {name!r}")
    if paper:
        if name != "paper.pdf":
            raise ValueError("the separately downloadable input must be project paper.pdf")
    elif name != "sources/PINNED_MANIFEST.json":
        if name not in ALLOWED_ROOT_FILES and part.parts[0] not in ALLOWED_ROOTS:
            raise ValueError(f"unapproved source location: {name}")
        if part.suffix not in {".tex", ".md", ".py", ".json"}:
            raise ValueError(f"unapproved source type: {name}")
        low = name.lower()
        if any(p in {"tmp", "__pycache__", "upload-kit"} for p in part.parts):
            raise ValueError(f"cache or generated output excluded: {name}")
        if any(s in low for s in ("checkpoint_push", "original_request", "secret", "credential", "token.env")):
            raise ValueError(f"personal, credential, or Git helper material excluded: {name}")
        if part.parts[0] == "receipts" and any(s in part.name for s in ("push_", "remote", "zenodo", "deposit", "publish", "stage")):
            raise ValueError(f"publication/Git operational receipt excluded from research archive: {name}")
        if "proposed" in part.name or name in RESERVED:
            raise ValueError(f"draft or generated package member excluded: {name}")
    path = ROOT.joinpath(*part.parts)
    walk = ROOT
    for component in part.parts:
        walk = walk / component
        if walk.is_symlink():
            raise ValueError(f"symlink input excluded: {name}")
    if not path.resolve().is_relative_to(ROOT):
        raise ValueError(f"input outside project: {name}")
    return path


def archive(members: dict[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_STORED) as zf:
        for name in sorted(members):
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_STORED
            zf.writestr(info, members[name])
    return buffer.getvalue()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".package-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--selection", type=Path, required=True, help="explicit proposed or frozen selection JSON")
    parser.add_argument("--metadata", type=Path, required=True, help="proposed or final Zenodo metadata JSON")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--plan", action="store_true", help="read-only inventory and input hashes (default)")
    mode.add_argument("--build", action="store_true", help="write payloads only from final hash-frozen inputs")
    args = parser.parse_args()
    for argument in (args.selection, args.metadata):
        if argument.is_symlink() or argument.resolve().parent != ROOT / "publication" or argument.suffix != ".json":
            raise ValueError("selection and metadata must be ordinary project publication/*.json files")
    selection = json.loads(args.selection.read_text(encoding="utf-8"))
    if not isinstance(selection, dict) or set(selection) != {"schema_version", "status", "paper", "source_files", "input_sha256"} or selection["schema_version"] != 1:
        raise ValueError("selection must use the documented version-1 schema")
    if selection["status"] not in {"proposed", "frozen"} or not isinstance(selection["paper"], str):
        raise ValueError("selection status must be proposed or frozen and paper must be a filename")
    expected = selection["input_sha256"]
    if not isinstance(expected, dict) or not all(isinstance(k, str) and isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v) for k, v in expected.items()):
        raise ValueError("input_sha256 must map names to lowercase SHA256 digests")
    names = selection["source_files"]
    if not isinstance(names, list) or not all(isinstance(x, str) for x in names) or len(names) != len(set(names)):
        raise ValueError("source_files must be an explicit list of distinct filenames")
    if not REQUIRED.issubset(names):
        raise ValueError(f"missing required source members: {sorted(REQUIRED - set(names))}")
    paths = {name: safe_project_file(name) for name in names}
    paths[selection["paper"]] = safe_project_file(selection["paper"], paper=True)
    missing = [name for name, path in paths.items() if not path.is_file()]
    snapshots = {name: path.read_bytes() for name, path in paths.items() if path.is_file()}
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    if not isinstance(metadata, dict) or not all(isinstance(metadata.get(key), str) and metadata[key].strip() for key in ("title", "description")):
        raise ValueError("metadata needs title, description, and creators")
    creators = metadata.get("creators")
    if not isinstance(creators, list) or not creators or not all(isinstance(c, dict) and isinstance(c.get("name"), str) and c["name"].strip() for c in creators):
        raise ValueError("metadata creators must be a nonempty list of named creator objects")
    if metadata.get("upload_type") != "publication" or metadata.get("publication_type") != "preprint":
        raise ValueError("this kit is a publication/preprint")
    if metadata.get("license") != "cc-by-4.0" or metadata.get("access_right") != "open":
        raise ValueError("this kit follows the documented open CC-BY-4.0 convention")
    metadata_data = json_bytes(metadata)
    hashes = {name: digest(data) for name, data in sorted(snapshots.items())}
    hashes["@metadata"] = digest(metadata_data)
    pdf_valid = selection["paper"] in snapshots and snapshots[selection["paper"]].startswith(b"%PDF-")
    plan = {
        "selection_status": selection["status"], "missing_inputs": missing, "pdf_signature_valid": pdf_valid,
        "input_sha256": hashes, "pdf_unchanged": True,
        "deposit_payload_names": ["paper.pdf", "source-and-verification.zip"],
        "source_member_names": sorted(names) + sorted(RESERVED),
        "build_ready": not missing and pdf_valid and selection["status"] == "frozen" and selection["input_sha256"] == hashes and "proposed" not in args.selection.name and "proposed" not in args.metadata.name,
    }
    if not args.build:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return
    if missing:
        raise ValueError(f"missing frozen inputs: {missing}")
    if selection["status"] != "frozen" or selection["input_sha256"] != hashes:
        raise ValueError("build requires status=frozen and exact input_sha256 from the final read-only plan")
    if "proposed" in args.selection.name or "proposed" in args.metadata.name:
        raise ValueError("freeze final selection and metadata under final filenames before building")
    pdf = snapshots.pop(selection["paper"])
    if not pdf.startswith(b"%PDF-"):
        raise ValueError("paper.pdf is not a PDF")
    sources = dict(snapshots)
    sources["README.md"] = sources["publication/README_FOR_DEPOSIT.md"]
    sources["publication/metadata.json"] = metadata_data
    sources["publication/package_selection.json"] = json_bytes(selection)
    sources["SOURCE_SHA256SUMS.txt"] = "".join(f"{digest(sources[name])}  {name}\n" for name in sorted(sources)).encode("utf-8")
    source_zip = archive(sources)
    payloads = {"paper.pdf": pdf, "source-and-verification.zip": source_zip}
    manifest = {
        "metadata": metadata,
        "files": [{"path": f"publication/upload-kit/{name}", "name": name} for name in sorted(payloads)],
    }
    receipt = {
        "schema_version": 1, "input_sha256": hashes,
        "payloads": [{"name": name, "bytes": len(data), "sha256": digest(data)} for name, data in sorted(payloads.items())],
        "source_members": [{"name": name, "bytes": len(data), "sha256": digest(data)} for name, data in sorted(sources.items())],
        "archive_policy": "sorted names; ZIP_STORED; fixed 1980-01-01 timestamp; regular files mode 0644; no directory entries",
        "source_hash_manifest_policy": "SOURCE_SHA256SUMS.txt covers every other source archive member; it does not hash itself",
        "operations": "local packaging only; no network, Git, credentials, deposit, or publication",
    }
    kit = dict(payloads)
    kit["metadata.json"] = metadata_data
    kit["PACKAGE_MANIFEST.json"] = json_bytes(receipt)
    kit["SHA256SUMS.txt"] = "".join(f"{digest(payloads[name])}  {name}\n" for name in sorted(payloads)).encode("utf-8")
    kit["LICENSES.md"] = sources["publication/LICENSES.md"]
    kit["UPLOAD.md"] = ("# Exact deposit payloads\n\nUpload paper.pdf and source-and-verification.zip as separate files using the project zenodo-deposit.json manifest. The outer upload-kit.zip is a convenience bundle and is not a deposit payload. Metadata, licenses, and package hashes accompany the kit. Local packaging does not publish a record.\n").encode("utf-8")
    kit["upload-kit.zip"] = archive(kit)
    output = ROOT / "publication" / "upload-kit"
    if output.is_symlink() or (ROOT / "publication").is_symlink():
        raise ValueError("output path must not be a symlink")
    for name, data in sorted(kit.items()):
        atomic_write(output / name, data)
    atomic_write(ROOT / "zenodo-deposit.json", json_bytes(manifest))
    print(json.dumps({"manifest": "zenodo-deposit.json", "output": "publication/upload-kit", "payloads": receipt["payloads"]}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"package error: {error}")
