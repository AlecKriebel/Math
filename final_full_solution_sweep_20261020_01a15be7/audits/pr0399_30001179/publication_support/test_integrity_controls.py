#!/usr/bin/env python3
"""Active normal/-O integrity negative controls in disposable private fixtures."""
import argparse
import hashlib
import json
import pathlib
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
from integrity import require, verify_bundle


def fresh(base):
    root = base / "fixture"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir()
    (root / "payload.txt").write_bytes(b"independent fixture\n")
    data = (root / "payload.txt").read_bytes()
    manifest = {"schema": 1, "files": [{"path": "payload.txt",
                "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}]}
    write_manifest(root, manifest)
    return root, manifest


def write_manifest(root, manifest):
    (root / "FILES.json").write_text(json.dumps(manifest), encoding="utf-8")


def main(private_dir):
    results = []
    with tempfile.TemporaryDirectory(prefix="integrity-controls-", dir=private_dir) as name:
        base = pathlib.Path(name)
        root, _ = fresh(base)
        require(verify_bundle(root)["files_verified"] == 1, "positive fixture rejected")

        def reject(label, mutate):
            root, manifest = fresh(base)
            mutate(root, manifest)
            try:
                verify_bundle(root)
            except (ValueError, OSError):
                results.append(label)
                return
            raise RuntimeError("negative control unexpectedly accepted: " + label)

        def change(label, key, value):
            def mutate(root, manifest):
                manifest["files"][0][key] = value
                write_manifest(root, manifest)
            reject(label, mutate)

        reject("same_length_tamper", lambda r, m: (r / "payload.txt").write_bytes(b"X" * m["files"][0]["bytes"]))
        reject("appended_bytes", lambda r, m: (r / "payload.txt").write_bytes((r / "payload.txt").read_bytes() + b"extra"))
        reject("missing_file", lambda r, m: (r / "payload.txt").unlink())
        reject("extra_file", lambda r, m: (r / "unexpected.txt").write_text("extra"))
        reject("symlink_file", lambda r, m: ((r / "payload.txt").unlink(), (r / "payload.txt").symlink_to("../elsewhere")))
        reject("symlink_directory", lambda r, m: (r / "unexpected-dir").symlink_to(base, target_is_directory=True))
        change("bool_bytes", "bytes", True)
        change("float_bytes", "bytes", 20.0)
        change("negative_bytes", "bytes", -1)
        change("bool_path", "path", True)
        for label, path in (("parent_path", "../payload.txt"), ("absolute_path", "/payload.txt"),
                            ("dot_component", "a/../payload.txt"), ("empty_component", "a//payload.txt"),
                            ("backslash", "a\\payload.txt"), ("dot_prefix", "./payload.txt"),
                            ("windows_drive", "C:/payload.txt")):
            change(label, "path", path)
        change("uppercase_digest", "sha256", "A" * 64)
        change("nonhex_digest", "sha256", "z" * 64)
        reject("bool_schema", lambda r, m: write_manifest(r, {"schema": True, "files": m["files"]}))
        reject("float_schema", lambda r, m: write_manifest(r, {"schema": 1.0, "files": m["files"]}))
        reject("mapping_instead_of_files_list", lambda r, m: write_manifest(r, {"schema": 1, "files": {}}))
        reject("unknown_top_level_key", lambda r, m: write_manifest(r, dict(m, unknown=1)))
        reject("duplicate_path", lambda r, m: write_manifest(r, {"schema": 1, "files": m["files"] * 2}))
        reject("unknown_record_key", lambda r, m: write_manifest(r, {"schema": 1, "files": [dict(m["files"][0], unknown=1)]}))
        reject("duplicate_json_key", lambda r, m: (r / "FILES.json").write_text('{"schema":1,"schema":1,"files":[]}'))
        reject("manifest_self_reference", lambda r, m: write_manifest(r, {"schema": 1, "files": [dict(m["files"][0], path="FILES.json")]}))
        root, manifest = fresh(base)
        (root / "payload.txt").write_bytes(b"")
        manifest["files"][0].update(bytes=0, sha256=hashlib.sha256(b"").hexdigest())
        write_manifest(root, manifest)
        require(verify_bundle(root)["files_verified"] == 1, "zero-byte positive fixture rejected")
    return {"status": "PASS", "positive_fixtures": 2, "rejected_mutations": len(results),
            "controls": results, "scope": "Inventory, exact manifest types, canonical paths, symlinks, and byte tampering; not mathematical proof certification."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_dir", type=pathlib.Path)
    args = parser.parse_args()
    args.private_dir.mkdir(parents=True, exist_ok=True)
    print(json.dumps(main(args.private_dir), indent=2, sort_keys=True))
