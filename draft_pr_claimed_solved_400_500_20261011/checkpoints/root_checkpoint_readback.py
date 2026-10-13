#!/usr/bin/env python3
"""Read-only native GitHub Merkle binding for a positive checkpoint receipt."""
from pathlib import Path
import argparse, datetime, hashlib, json, subprocess

def require(condition, message):
    if not condition:
        raise ValueError(message)

def git_object(kind, data):
    return hashlib.sha1((kind + " " + str(len(data)) + "\0").encode() + data).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    receipt_path = root / args.receipt
    output = root / args.output
    require(receipt_path.is_file(), "receipt missing")
    require(not output.exists(), "refuse to replace previous readback")
    receipt = json.loads(receipt_path.read_text())
    sha = receipt["commit_sha"]
    def get(endpoint):
        run = subprocess.run(["gh", "api", "repos/AlecKriebel/Math/" + endpoint], capture_output=True, text=True, check=True)
        return json.loads(run.stdout)
    commit = get("git/commits/" + sha)
    require(commit["sha"] == sha, "commit identity mismatch")
    require([p["sha"] for p in commit["parents"]] == [receipt["parent_main_sha"]], "unexpected checkpoint parent")
    cache = {}
    def tree(tree_sha):
        if tree_sha not in cache:
            native = get("git/trees/" + tree_sha)
            require(native["sha"] == tree_sha and native.get("truncated") is False, "tree identity/truncation mismatch")
            entries = native["tree"]
            require(all("/" not in e["path"] for e in entries), "tree is not immediate")
            sorted_entries = sorted(entries, key=lambda e: e["path"].encode() + (b"/" if e["type"] == "tree" else b""))
            data = b"".join((("40000" if e["type"] == "tree" else e["mode"]) + " ").encode() + e["path"].encode() + b"\0" + bytes.fromhex(e["sha"]) for e in sorted_entries)
            require(git_object("tree", data) == tree_sha, "immediate-tree serialization mismatch")
            require(len({e["path"] for e in entries}) == len(entries), "duplicate tree path")
            cache[tree_sha] = {e["path"]: e for e in entries}
        return cache[tree_sha]
    records = []
    for path, expected in receipt["files_sha256"].items():
        relative = Path(path)
        require(not relative.is_absolute() and ".." not in relative.parts, "unsafe receipt path")
        require(not any(x in {"private_sources", "private_cases", "mutation_fixtures", ".secrets", ".zenodo-state", "__pycache__", "venv"} for x in relative.parts), "private path")
        local = root / relative
        require(local.is_file() and not local.is_symlink(), "nonregular released local file")
        data = local.read_bytes()
        require(hashlib.sha256(data).hexdigest() == expected, "local released bytes changed: " + path)
        current = commit["tree"]["sha"]
        for component in relative.parts[:-1]:
            entry = tree(current)[component]
            require(entry["type"] == "tree" and entry["mode"] == "040000", "intermediate mode mismatch")
            current = entry["sha"]
        entry = tree(current)[relative.name]
        require(entry["type"] == "blob" and entry["mode"] == "100644", "released mode mismatch")
        require(entry["sha"] == git_object("blob", data), "released Git blob mismatch: " + path)
        records.append({"path": path, "sha256": expected, "blob_sha": entry["sha"], "mode": entry["mode"]})
    main_sha = get("git/ref/heads/main")["object"]["sha"]
    if main_sha != sha:
        comparison = get("compare/" + sha + "..." + main_sha)
        require(comparison["status"] in {"ahead", "identical"} and comparison["merge_base_commit"]["sha"] == sha, "checkpoint not ancestor of current main")
    result = {"time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "checkpoint_commit": sha, "current_main": main_sha, "expected_parent": receipt["parent_main_sha"], "file_count": len(records), "immediate_trees_verified": len(cache), "checks": "Every positive released file independently SHA256/Git-blob bound to SHA-verified immediate Git trees; expected parent and current-main ancestry confirmed", "files": records}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checkpoint": sha, "files_verified": len(records), "main": main_sha, "trees_verified": len(cache)}))

if __name__ == "__main__":
    main()
