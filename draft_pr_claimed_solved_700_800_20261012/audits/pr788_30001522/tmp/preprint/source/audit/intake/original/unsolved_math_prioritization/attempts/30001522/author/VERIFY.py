"""Strict flat-packet verifier with verified-source execution and no local imports."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


def fail(message):
    raise ValueError(message)


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            fail("duplicate JSON key: " + key)
        out[key] = value
    return out


def read_json(data):
    return json.loads(data, object_pairs_hook=unique_object)


def verify(root):
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        fail("packet root is not a real directory")
    entries = {}
    for entry in os.scandir(root):
        info = entry.stat(follow_symlinks=False)
        if not stat.S_ISREG(info.st_mode):
            fail("nonregular member or directory: " + entry.name)
        entries[entry.name] = entry
    if "MANIFEST.json" not in entries:
        fail("manifest missing")
    manifest_bytes = (root / "MANIFEST.json").read_bytes()
    manifest = read_json(manifest_bytes)
    if set(manifest) != {"format", "files"} or manifest["format"] != "free-p-toral-v1":
        fail("unsupported manifest")
    files = manifest["files"]
    if not isinstance(files, list) or not files:
        fail("empty or invalid inventory")
    by_name = {}
    for item in files:
        if set(item) != {"name", "sha256", "bytes"}:
            fail("invalid manifest record")
        name = item["name"]
        if not isinstance(name, str) or not name or Path(name).name != name or "\\" in name or name in {".", "..", "MANIFEST.json"}:
            fail("unsafe manifest member")
        if name in by_name:
            fail("duplicate manifest member")
        if not isinstance(item["bytes"], int) or isinstance(item["bytes"], bool) or item["bytes"] < 0:
            fail("invalid byte count")
        by_name[name] = item
    if set(entries) != set(by_name) | {"MANIFEST.json"}:
        fail("inventory mismatch")
    checked = {}
    for name, item in by_name.items():
        # O_NOFOLLOW closes the final-component symlink race on supported POSIX systems.
        fd = os.open(root / name, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        with os.fdopen(fd, "rb") as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                fail("nonregular member on read")
            data = stream.read()
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            fail("content mismatch: " + name)
        checked[name] = data
    for required in ["VERIFY.py", "CHECKS.py", "EXPECTED_RESULTS.json", "PROOF.md", "PROVENANCE.json", "SOURCE_METADATA.json"]:
        if required not in checked:
            fail("required payload missing: " + required)
    provenance = read_json(checked["PROVENANCE.json"])
    if provenance["review_sha256"] != "ca5ea39f6f40b6344a17adf507993b7a3aa628f194669943f2b6acb99876e306":
        fail("review binding mismatch")
    if provenance["statement_sha256"] != "c368a8d0a2095496760c49e9393ba1825274ccad544d6cf16acbca830d7ef0a0":
        fail("statement binding mismatch")
    namespace = {"__name__": "verified_arithmetic_source", "__builtins__": __builtins__}
    exec(compile(checked["CHECKS.py"], "<verified CHECKS.py>", "exec"), namespace)
    result = namespace["run_checks"]()
    if result != read_json(checked["EXPECTED_RESULTS.json"]):
        fail("arithmetic output mismatch")
    return {"status": "PASS", "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            "verified_payload_files": len(checked), "executed_checker_sha256": by_name["CHECKS.py"]["sha256"],
            "arithmetic": result,
            "limitation": "Integrity and finite arithmetic only; no formal topology verification or source reauthentication."}


if __name__ == "__main__":
    try:
        packet = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
        print(json.dumps(verify(packet), sort_keys=True, indent=2))
    except Exception as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
