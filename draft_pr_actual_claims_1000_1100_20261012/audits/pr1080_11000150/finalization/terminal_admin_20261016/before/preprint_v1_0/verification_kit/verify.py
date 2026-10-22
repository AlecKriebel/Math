#!/usr/bin/env python3
"""Internal integrity verification; an external binding optionally authenticates bytes."""
import argparse
import hashlib
import json
import re
import os
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_input(path):
    """Reject leaf/ancestor symlinks before reading any bootstrap or binding."""
    p = Path(path).absolute()
    for part in [p, *p.parents]:
        require(not part.is_symlink(), "input symlink rejected: " + str(part))
    require(p.is_file(), "input missing or nonregular: " + str(p))
    return p


def fresh_output(path):
    """Inspect the unresolved path before normalization and before any write.

    Every existing leaf is forbidden, including all inode aliases. Exclusive
    creation in the builder additionally handles an intervening leaf creation.
    This is a bounded CLI input guarantee, not an adversarial concurrency lock.
    """
    raw = Path(path).absolute()
    for part in [raw, *raw.parents]:
        require(not part.is_symlink(), "archive output symlink/ancestor rejected: " + str(part))
    output = Path(os.path.abspath(raw))
    require(not output.is_relative_to(ROOT), "archive must be outside the kit")
    require(not output.exists(), "archive destination must be fresh; existing files and aliases rejected")
    require(output.parent.is_dir(), "archive parent must be an existing ordinary directory")
    return output


def native_metadata():
    data = json.loads(regular_input(ROOT / "metadata.json").read_text())
    require(data["upload_type"] == "publication" and data["publication_type"] == "preprint", "native publication type")
    require(data["creators"] == [{"name": "Kriebel, Alec", "affiliation": "Independent researcher", "orcid": "0009-0001-9320-500X"}], "native author/ORCID")
    require(data["license"] == "cc-by-4.0" and data["access_right"] == "open", "native license/access")
    require(data["publication_date"] == "2026-10-14" and data["version"] == "1.0", "native date/version")
    require(bool(data["title"]) and bool(data["description"]), "native title/description")
    for text in ["simultaneous-conjugacy", "Cossu and Tringali", "unresolved in this work", "UNKNOWN", "AI", "unrefereed", "no external human peer review"]:
        require(text in data["description"], "native scope/disclosure absent: " + text)
    return data


def safe_path(name):
    require(isinstance(name, str) and name and "\\" not in name, "bad member name")
    p = PurePosixPath(name)
    require(not p.is_absolute() and all(x not in (".", "..", "") for x in name.split("/")),
            "unsafe member path")
    require(str(p) == name, "noncanonical member path")
    return ROOT / name


def verify(binding=None, require_binding=False, pdf=None, archive=None):
    adjacent = ROOT.parent / "EXTERNAL_BINDING.json"
    if binding is None and (adjacent.exists() or adjacent.is_symlink()):
        binding = adjacent
    allow = json.loads(regular_input(ROOT / "ALLOWLIST.json").read_text())
    names = allow["members"]
    require(names == sorted(set(names)), "allowlist order/duplicates")
    for name in names:
        safe_path(name)
    require("MANIFEST.json" in names and "ALLOWLIST.json" in names, "missing manifest/allowlist")
    expected_dirs = {str(parent) for n in names for parent in PurePosixPath(n).parents
                     if str(parent) != "."}
    files = []
    dirs = set()
    for p in ROOT.rglob("*"):
        require(not p.is_symlink(), "symlink rejected: " + str(p))
        if p.is_file():
            files.append(p.relative_to(ROOT).as_posix())
        elif p.is_dir():
            dirs.add(p.relative_to(ROOT).as_posix())
        else:
            raise RuntimeError("nonregular member")
    require(sorted(files) == names, "unexpected or missing files")
    require(dirs == expected_dirs, "unexpected or missing directories")
    manifest = json.loads(regular_input(ROOT / "MANIFEST.json").read_text())
    require(manifest["self_hash_scope"] == "All allowlisted members except MANIFEST.json", "self scope")
    rows = manifest["files"]
    require([r["path"] for r in rows] == [n for n in names if n != "MANIFEST.json"], "manifest members")
    for r in rows:
        p = safe_path(r["path"])
        require(type(r["bytes"]) is int and r["bytes"] >= 0, "invalid size")
        require(re.fullmatch("[0-9a-f]{64}", r["sha256"]) is not None, "invalid digest")
        require(p.stat().st_size == r["bytes"] and digest(p) == r["sha256"], "member mismatch: " + r["path"])
    ledger = json.loads((ROOT / "COPY_EXCLUSION_LEDGER.json").read_text())
    copied = 0
    for r in ledger["files"]:
        if r["disposition"] == "byte_identical_copy":
            p = safe_path(r["destination"])
            require(p.stat().st_size == r["bytes"] and digest(p) == r["sha256"], "original-copy mismatch")
            copied += 1
        else:
            require(r["disposition"] == "omitted" and bool(r["reason"]), "undocumented omission")
    for r in ledger["historical_pin_references"]:
        if r["disposition"] == "hash_identical_canonical_copy":
            require(digest(safe_path(r["destination"])) == r["sha256"], "historical canonical-copy mismatch")
        else:
            require(r["disposition"] == "omitted" and bool(r["reason"]), "undocumented historical omission")
    stage = json.loads((ROOT / "REPAIR01_STAGE_COPIES.json").read_text())
    for r in stage["files"]:
        q = safe_path(r["destination"])
        require(q.stat().st_size == r["bytes"] and digest(q) == r["sha256"], "repair old-stage copy mismatch")
    history = json.loads((ROOT / "REPAIR01_HISTORY_RESOLUTION.json").read_text())
    for r in history["references"]:
        if r["disposition"] == "exact_captured_stage_or_canonical_copy":
            q = safe_path(r["destination"])
            require(q.stat().st_size == r["bytes"] and digest(q) == r["sha256"], "repair historical pin mismatch")
        else:
            require(r["disposition"] == "omitted" and bool(r["reason"]), "repair historical omission unexplained")
    native = native_metadata()
    require(not require_binding or binding is not None, "external binding required")
    bound = False
    if binding is not None:
        p = regular_input(binding)
        data = json.loads(p.read_text())
        require(data["manifest_sha256"] == digest(ROOT / "MANIFEST.json"), "external manifest binding mismatch")
        require(data["metadata_sha256"] == digest(ROOT / "metadata.json"), "external metadata binding mismatch")
        require(data["research_metadata_sha256"] == digest(ROOT / "research_metadata.json"), "external research metadata mismatch")
        outer = regular_input(p.parent / "metadata.json")
        require(outer.read_bytes() == (ROOT / "metadata.json").read_bytes(), "external native metadata differs")
        wrapper = regular_input(p.parent / "deposit_metadata.json")
        require(digest(wrapper) == data["deposit_manifest_sha256"], "upload manifest binding mismatch")
        upload = json.loads(wrapper.read_text())
        require(set(upload) == {"metadata", "files"} and upload["metadata"] == native, "native upload schema/metadata differs")
        require(upload["files"] == [{"path": "preprint.pdf", "name": "preprint.pdf"},
                                    {"path": "verification_kit.zip", "name": "verification_kit.zip"}], "native upload attachments differ")
        require(regular_input(p.parent / "research_metadata.json").read_bytes() == (ROOT / "research_metadata.json").read_bytes(), "external research object differs")
        require(regular_input(p.parent / "CURRENT_STATUS_REPAIR01.json").read_bytes() == (ROOT / "CURRENT_STATUS_REPAIR01.json").read_bytes(), "external current status differs")
        require([r["filename"] for r in data["external_files"]] ==
                ["CURRENT_STATUS_REPAIR01.json", "README.md", "deposit_metadata.json", "metadata.json", "preprint.tex", "research_metadata.json"], "external delivery file inventory differs")
        for r in data["external_files"]:
            q = regular_input(p.parent / r["filename"])
            require(q.stat().st_size == r["bytes"] and digest(q) == r["sha256"], "external delivery member mismatch")
        # Present bindings are always strict. Explicit artifact paths work after extraction.
        for key, override in [("pdf", pdf), ("archive", archive)]:
            record = data[key]
            require(Path(record["filename"]).name == record["filename"], "unsafe external filename")
            q = regular_input(Path(override) if override else p.parent / record["filename"])
            require(q.stat().st_size == record["bytes"] and digest(q) == record["sha256"], "bound artifact mismatch: " + key)
        bound = True
    else:
        require(pdf is None and archive is None, "artifact overrides need an external binding")
    return {"status": "PASS", "members": len(names), "preserved_original_files": copied,
            "external_binding_verified": bound,
            "scope": "Internal byte integrity; mathematical truth and historical priority require the written evidence."}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--binding", type=Path)
    p.add_argument("--require-binding", action="store_true")
    p.add_argument("--pdf", type=Path)
    p.add_argument("--archive", type=Path)
    a = p.parse_args()
    print(json.dumps(verify(a.binding, a.require_binding, a.pdf, a.archive), indent=2))


if __name__ == "__main__":
    main()
