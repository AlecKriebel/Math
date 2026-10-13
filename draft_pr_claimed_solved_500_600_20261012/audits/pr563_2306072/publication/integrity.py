"""Consistency checks for the explicit authored-file seals; standard library."""
import hashlib
import json
from pathlib import PurePosixPath


def safe_path(name):
    if not isinstance(name, str) or not name or "\\" in name or ":" in name:
        raise RuntimeError(f"Invalid relative path: {name!r}")
    p = PurePosixPath(name)
    if p.is_absolute() or ".." in p.parts or p.as_posix() != name:
        raise RuntimeError(f"Invalid relative path: {name!r}")
    return p


def seal_entries(data):
    records = data.get("files", data.get("authored_files"))
    if isinstance(records, dict):
        return [
            dict(path=name, sha256=value)
            if isinstance(value, str) else dict(path=name, **value)
            for name, value in records.items()
        ]
    if isinstance(records, list):
        return records
    raise RuntimeError("Unsupported authored-file seal")


def verify_nested(payloads, registry):
    count = 0
    for name in registry:
        base = safe_path(name).parent
        if name not in payloads:
            raise RuntimeError(f"Missing seal: {name}")
        seal = json.loads(payloads[name])
        seen = set()
        for item in seal_entries(seal):
            rel = safe_path(item["path"])
            path = (base / rel).as_posix()
            if path in seen:
                raise RuntimeError(f"Duplicate nested entry: {name}: {path}")
            seen.add(path)
            if path not in payloads:
                raise RuntimeError(f"Nested payload omitted: {name}: {path}")
            data = payloads[path]
            size = item.get("bytes", item.get("size_bytes", item.get("size")))
            if size is not None and len(data) != size:
                raise RuntimeError(f"Nested size mismatch: {name}: {path}")
            if hashlib.sha256(data).hexdigest() != item["sha256"]:
                raise RuntimeError(f"Nested hash mismatch: {name}: {path}")
            count += 1
    return count
