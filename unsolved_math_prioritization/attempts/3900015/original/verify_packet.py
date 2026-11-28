#!/usr/bin/env python3
"""Verify packet bytes and independently rerun its exact deterministic diagnostics."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def verify():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "MANIFEST.json").read_text())
    require(manifest.get("schema") == "safe-packet-manifest-v1", "wrong manifest schema")
    declared = manifest["files"]
    require(isinstance(declared, dict), "manifest files must be an object")
    actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    require(actual == set(declared) | {"MANIFEST.json"}, "unexpected or missing file")
    for name, metadata in declared.items():
        p = root / name
        require(not p.is_symlink(), "symlink rejected")
        require(p.resolve().parent == root, "non-flat or escaping file rejected")
        b = p.read_bytes()
        require(len(b) == metadata["bytes"], "size mismatch: " + name)
        require(hashlib.sha256(b).hexdigest() == metadata["sha256"], "hash mismatch: " + name)
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("reciprocal_exact_diagnostics", root / "exact_diagnostics.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    obtained = module.diagnostics()
    expected = json.loads((root / "EXPECTED_DIAGNOSTICS.json").read_text())
    # JSON normalization intentionally makes tuple/list serialization equivalent.
    obtained = json.loads(json.dumps(obtained, sort_keys=True))
    require(obtained == expected, "exact diagnostics differ from expected output")
    print(json.dumps({"verified": True, "problem_id": "3900015", "file_count": len(declared),
                      "full_problem_resolved": False, "diagnostics": obtained}, sort_keys=True, indent=2))


if __name__ == "__main__":
    try:
        verify()
    except Exception as exc:
        print("VERIFICATION FAILED: " + str(exc), file=sys.stderr)
        raise SystemExit(1)
