"""Caller must independently pin this file and pass a pinned manifest digest."""
import argparse
import hashlib
import json
import pathlib
import runpy
import sys


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, label):
    if not condition:
        raise ValueError(label)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest-sha256", required=True)
    ap.add_argument("--input-root", required=True)
    args = ap.parse_args()
    root = pathlib.Path(__file__).resolve().parent
    manifest_path = root / "MANIFEST.json"
    require(digest(manifest_path) == args.manifest_sha256, "caller manifest pin mismatch")
    manifest = json.loads(manifest_path.read_text())
    require(manifest["format"] == "pr788-definition-topology-v1", "manifest schema")
    rows = manifest["files"]
    names = [row["path"] for row in rows]
    require(len(names) == len(set(names)), "duplicate manifest name")
    require(all(pathlib.PurePosixPath(n).name == n and n not in {".", ".."} for n in names), "nonlocal manifest name")
    require(set(p.name for p in root.iterdir()) == set(names) | {"MANIFEST.json"}, "exact inventory mismatch")
    for row in rows:
        p = root / row["path"]
        require(p.is_file() and not p.is_symlink(), "nonregular packet member")
        require(p.stat().st_size == row["bytes"] and digest(p) == row["sha256"], "packet digest mismatch: " + row["path"])
    bindings = json.loads((root / "INPUT_BINDINGS.json").read_text())
    intake = pathlib.Path(args.input_root).resolve()
    for row in bindings["local_inputs"]:
        p = intake / row["path"]
        require(p.is_file() and not p.is_symlink(), "missing input: " + row["path"])
        require(p.stat().st_size == row["bytes"] and digest(p) == row["sha256"], "input digest mismatch: " + row["path"])
    diagnostic = runpy.run_path(str(root / "DIAGNOSTICS.py"))["diagnostics"]()
    require(diagnostic == json.loads((root / "DIAGNOSTIC_RESULTS.json").read_text()), "diagnostic replay mismatch")
    print(json.dumps({"status": "PASS", "files": len(rows), "bound_local_inputs": len(bindings["local_inputs"]), "diagnostics": diagnostic["status"]}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as error:
        print("FAIL: " + str(error), file=sys.stderr)
        sys.exit(1)
