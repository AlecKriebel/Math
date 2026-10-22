"""Strict consistency checks for this authored-only archive; standard library."""
import hashlib
import json
from pathlib import PurePosixPath
import re


def safe_path(name):
    if not isinstance(name, str) or not name or "\\" in name or ":" in name:
        raise RuntimeError(f"Invalid relative path: {name!r}")
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != name:
        raise RuntimeError(f"Invalid relative path: {name!r}")
    return path


def verify_nested(payloads, registry):
    count = 0
    if len(registry) != len(set(registry)):
        raise RuntimeError("Duplicate seal registry")
    for name in registry:
        base = safe_path(name).parent
        if name not in payloads:
            raise RuntimeError(f"Missing seal: {name}")
        seen = set()
        for line in payloads[name].decode("utf-8").splitlines():
            match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
            if match is None:
                raise RuntimeError(f"Malformed checksum entry: {name}")
            digest, rel = match.groups()
            path = (base / safe_path(rel)).as_posix()
            if path in seen or path == name:
                raise RuntimeError(f"Duplicate or self-sealed entry: {path}")
            seen.add(path)
            if path not in payloads or hashlib.sha256(payloads[path]).hexdigest() != digest:
                raise RuntimeError(f"Nested hash mismatch or missing payload: {path}")
            count += 1
    snapshot = json.loads(payloads["ORIGINAL_SNAPSHOT.json"])
    original = set()
    for record in snapshot["files"]:
        name = "original/" + safe_path(record["path"]).as_posix()
        if name in original:
            raise RuntimeError("Duplicate original snapshot entry")
        original.add(name)
        if name not in payloads:
            raise RuntimeError(f"Missing original snapshot entry: {name}")
        data = payloads[name]
        if len(data) != record["size"] or hashlib.sha256(data).hexdigest() != record["sha256"]:
            raise RuntimeError(f"Original snapshot mismatch: {name}")
    if original != {name for name in payloads if name.startswith("original/")}:
        raise RuntimeError("Original snapshot inventory mismatch")
    return count, len(original)
