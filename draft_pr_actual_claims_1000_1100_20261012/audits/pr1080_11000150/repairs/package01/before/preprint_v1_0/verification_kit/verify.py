#!/usr/bin/env python3
"""Internal integrity verification; an external binding optionally authenticates bytes."""
import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    allow = json.loads((ROOT / "ALLOWLIST.json").read_text())
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
    manifest = json.loads((ROOT / "MANIFEST.json").read_text())
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
    require(not require_binding or binding is not None, "external binding required")
    bound = False
    if binding is not None:
        p = Path(binding)
        require(p.is_file() and not p.is_symlink(), "specified external binding missing or symlink")
        data = json.loads(p.read_text())
        require(data["manifest_sha256"] == digest(ROOT / "MANIFEST.json"), "external manifest binding mismatch")
        require(data["metadata_sha256"] == digest(ROOT / "metadata.json"), "external metadata binding mismatch")
        # Present bindings are always strict. Explicit artifact paths work after extraction.
        for key, override in [("pdf", pdf), ("archive", archive)]:
            record = data[key]
            require(Path(record["filename"]).name == record["filename"], "unsafe external filename")
            q = Path(override) if override else p.parent / record["filename"]
            require(q.is_file() and not q.is_symlink(), "bound artifact missing: " + key)
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
