"""Exact inventories and historical seals; Python standard library only."""
import hashlib
import json
from pathlib import PurePosixPath
import re


def safe_path(name):
    if not isinstance(name, str) or not name or name == "." or "\\" in name or ":" in name:
        raise RuntimeError(f"Invalid relative path: {name!r}")
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != name:
        raise RuntimeError(f"Invalid relative path: {name!r}")
    return path


def verify_nested(payloads, registry):
    count = 0
    names = set()
    for item in registry:
        name = safe_path(item["path"]).as_posix()
        if name in names or name not in payloads:
            raise RuntimeError(f"Missing or duplicate seal: {name}")
        names.add(name)
        if hashlib.sha256(payloads[name]).hexdigest() != item["sha256"]:
            raise RuntimeError(f"Seal binding differs: {name}")
        base = safe_path(name).parent
        records = []
        if item["kind"] == "sha256sum":
            for line in payloads[name].decode().splitlines():
                match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
                if match is None:
                    raise RuntimeError(f"Malformed checksum entry: {name}")
                digest, rel = match.groups()
                records.append((rel, digest, None))
        elif item["kind"] == "json-files":
            for record in json.loads(payloads[name])["files"]:
                records.append((record["path"], record["sha256"], record["bytes"]))
        elif item["kind"] == "original-audit-json":
            audit = json.loads(payloads[name])
            for group, source_base in (("publication_safe_author_files", base.parent),
                                       ("publication_safe_audit_files", base)):
                for record in audit[group]:
                    rel = (source_base / safe_path(record["path"])).as_posix()
                    records.append((rel, record["sha256"], record["bytes"]))
            base = PurePosixPath(".")
        else:
            raise RuntimeError(f"Unknown seal type: {item['kind']}")
        seen = set()
        for rel, digest, size in records:
            path = (base / safe_path(rel)).as_posix()
            if path in seen or path == name:
                raise RuntimeError(f"Duplicate or self-sealed entry: {path}")
            seen.add(path)
            if path not in payloads or hashlib.sha256(payloads[path]).hexdigest() != digest:
                raise RuntimeError(f"Nested hash mismatch or missing payload: {path}")
            if size is not None and len(payloads[path]) != size:
                raise RuntimeError(f"Nested size mismatch: {path}")
            count += 1
    snapshot = json.loads(payloads["ORIGINAL_SNAPSHOT.json"])
    original = set()
    for record in snapshot["files"]:
        name = "original/" + safe_path(record["path"]).as_posix()
        if name in original or name not in payloads:
            raise RuntimeError(f"Duplicate or missing original: {name}")
        original.add(name)
        data = payloads[name]
        if len(data) != record["size"] or hashlib.sha256(data).hexdigest() != record["sha256"]:
            raise RuntimeError(f"Original snapshot mismatch: {name}")
    if original != {name for name in payloads if name.startswith("original/")}:
        raise RuntimeError("Original snapshot inventory mismatch")
    return count, len(original)
