#!/usr/bin/env python3
"""Externally authenticate this bootstrap, then verify before executing payload."""
from pathlib import Path
import hashlib
import json
import stat
import subprocess
import sys

EXPECTED_MANIFEST = "690e26d6f9b86e3c95ca74213a49f90c5f9fce5cd769c512bc3698904300e782"

class Rejected(Exception):
    pass

def require(value, message):
    if not value:
        raise Rejected(message)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def pairs(items):
    result = {}
    for k, v in items:
        require(k not in result, "duplicate JSON key")
        result[k] = v
    return result

def bad_constant(value):
    raise Rejected("nonfinite JSON constant")

def ordinary(path):
    require(not path.is_symlink(), "symlink file")
    require(stat.S_ISREG(path.stat().st_mode), "nonregular file")
    return path.read_bytes()

def run():
    require(len(sys.argv) == 1, "bootstrap accepts no arguments")
    script = Path(__file__).absolute()
    require(not script.is_symlink(), "symlink bootstrap")
    root = script.parent
    for part in (root, *root.parents):
        require(not part.is_symlink(), "symlink path ancestor")
    require(root.is_dir(), "author root directory")
    require({p.name for p in root.iterdir()} == {"bootstrap.py", "AUTHOR_MANIFEST.json", "packet"},
            "unexpected author-root inventory")
    raw = ordinary(root / "AUTHOR_MANIFEST.json")
    require(digest(raw) == EXPECTED_MANIFEST, "manifest trust anchor mismatch")
    manifest = json.loads(raw, object_pairs_hook=pairs, parse_constant=bad_constant)
    require(type(manifest) is dict and set(manifest) ==
            {"schema", "problem_id", "disposition", "approaches", "files"}, "manifest shape")
    require(manifest["schema"] == "transverse-surgery-author-manifest-v1", "manifest schema")
    require(type(manifest["problem_id"]) is int and manifest["problem_id"] == 10300034,
            "problem identity")
    require(manifest["disposition"] == "unsolved" and type(manifest["approaches"]) is int
            and manifest["approaches"] == 5, "scope/disposition")
    packet = root / "packet"
    require(packet.is_dir() and not packet.is_symlink(), "packet directory type")
    items = manifest["files"]
    require(type(items) is list and len(items) > 0, "manifest inventory")
    names = set()
    for item in items:
        require(type(item) is dict and set(item) == {"path", "bytes", "sha256"}, "entry shape")
        name = item["path"]
        require(type(name) is str and name not in ("", ".", "..") and "/" not in name
                and "\\" not in name and "\x00" not in name, "unsafe member path")
        require(name not in names, "duplicate member")
        names.add(name)
        require(type(item["bytes"]) is int and item["bytes"] >= 0, "size type")
        require(type(item["sha256"]) is str and len(item["sha256"]) == 64
                and all(c in "0123456789abcdef" for c in item["sha256"]), "digest type")
        payload = ordinary(packet / name)
        require(len(payload) == item["bytes"], "size mismatch: " + name)
        require(digest(payload) == item["sha256"], "hash mismatch: " + name)
    require({p.name for p in packet.iterdir()} == names, "unexpected packet inventory")
    require({"verify.py", "DIAGNOSTICS.json", "CLAIMS.json"} <= names, "required member missing")
    expected = ordinary(packet / "DIAGNOSTICS.json")
    flags = [] if sys.flags.optimize == 0 else ["-O" if sys.flags.optimize == 1 else "-OO"]
    process = subprocess.run([sys.executable, "-I", "-S", "-B", *flags, str(packet / "verify.py")],
                             cwd=packet, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    require(process.returncode == 0, "authenticated diagnostics failed: " +
            process.stderr.decode("utf-8", "replace"))
    require(process.stdout == expected, "diagnostics output mismatch")
    return {"schema": "transverse-surgery-bootstrap-v1", "status": "pass", "files": len(names),
            "manifest_sha256": EXPECTED_MANIFEST, "diagnostics_sha256": digest(expected)}

if __name__ == "__main__":
    try:
        print(json.dumps(run(), sort_keys=True, separators=(",", ":")))
    except (Rejected, OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as exc:
        print("REJECT: " + str(exc), file=sys.stderr)
        sys.exit(1)
