#!/usr/bin/env python3
"""Read-only custody check. Supply a trusted external manifest SHA256.
No asserts, network, writes, bundled imports, or optimization-dependent checks.
"""
import argparse
import hashlib
import json
import re
import stat
import sys
from pathlib import Path, PurePosixPath

HEAD = "34f21454986a28ca49f24999be3a0fd1b42755f8"
TARGET = {"pr": 786, "problem_id": 30001223, "head": HEAD}
EXCEPTIONS = ["EXTERNAL_PIN.txt", "FROZEN_MANIFEST.json"]
TREE = "intake/original/unsolved_math_prioritization/attempts/30001223"
EXTRA_INPUTS = {
    "intake/SELECTED_PUBLIC_RECORD.json",
    "intake/ROOT_SOURCE_IDENTITY.json",
    "intake/ELIGIBILITY_GATE.json",
    "root-receipts/MATH_GATE.json",
    "root-receipts/ROOT_MATH_POSITION.md",
}

class CustodyError(Exception):
    pass

def require(condition, message):
    if not condition:
        raise CustodyError(message)

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + str(key))
        result[key] = value
    return result

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def relative(value):
    require(isinstance(value, str) and bool(value), "invalid relative path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and "." not in path.parts and ".." not in path.parts,
            "unsafe relative path: " + value)
    require(str(path) == value and "\\" not in value, "noncanonical path: " + value)
    return path

def regular(path):
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        raise CustodyError("missing/inaccessible file: " + str(path)) from exc
    require(stat.S_ISREG(mode), "not a regular file: " + str(path))

def safe_path(root, name):
    relative(name)
    cursor = root
    for part in PurePosixPath(name).parts:
        cursor = cursor / part
        require(not cursor.is_symlink(), "input symlink: " + str(cursor))
    return cursor

def entry(root, row):
    require(isinstance(row, dict) and set(row) == {"path", "bytes", "sha256"},
            "malformed digest entry")
    name = row["path"]
    relative(name)
    require(type(row["bytes"]) is int and row["bytes"] >= 0, "invalid byte count")
    require(isinstance(row["sha256"], str) and
            re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) is not None, "invalid digest")
    path = safe_path(root, name)
    regular(path)
    data = path.read_bytes()
    require(len(data) == row["bytes"], "byte count mismatch: " + name)
    require(sha(data) == row["sha256"], "digest mismatch: " + name)
    return data

def verify(root, input_root, expected):
    require(re.fullmatch(r"[0-9a-f]{64}", expected) is not None, "invalid external pin")
    regular(root / "FROZEN_MANIFEST.json")
    data = (root / "FROZEN_MANIFEST.json").read_bytes()
    require(sha(data) == expected, "external manifest pin mismatch")
    manifest = json.loads(data, object_pairs_hook=unique_object)
    require(manifest.get("schema") == "priority-custody/v1", "manifest schema")
    require(manifest.get("target") == TARGET, "target mismatch")
    require(manifest.get("explicit_exceptions") == EXCEPTIONS, "exception mismatch")
    require(isinstance(manifest.get("files"), list), "manifest files missing")
    names = set()
    for row in manifest["files"]:
        name = row.get("path") if isinstance(row, dict) else None
        relative(name)
        require(len(PurePosixPath(name).parts) == 1, "bundle must be flat")
        require(name not in names and name not in EXCEPTIONS, "duplicate/excepted file")
        names.add(name)
        entry(root, row)
    require({p.name for p in root.iterdir()} == names | set(EXCEPTIONS),
            "unexpected/missing packet inventory")
    for path in root.iterdir():
        regular(path)
    require((root / "EXTERNAL_PIN.txt").read_bytes() == (expected + "\n").encode("ascii"),
            "convenience pin mismatch")
    receipts = read_json(root / "INPUT_RECEIPTS.json")
    require(receipts.get("schema") == "full-priority-inputs/v1", "input schema")
    require(receipts.get("original_tree") == TREE and receipts.get("original_count") == 41,
            "original tree declaration mismatch")
    rows = receipts.get("files")
    require(isinstance(rows, list) and len(rows) == 46, "must bind all46 inputs")
    byname = {}
    bodies = {}
    for row in rows:
        require(isinstance(row, dict), "bad input record")
        name = row.get("path")
        relative(name)
        require(name not in byname, "duplicate input")
        byname[name] = row
        bodies[name] = entry(input_root, row)
    originals = {name for name in byname if name.startswith(TREE + "/")}
    require(len(originals) == 41 and set(byname) == originals | EXTRA_INPUTS,
            "input coverage mismatch")
    tree = safe_path(input_root, TREE)
    require(tree.is_dir(), "original tree missing")
    actual_files = set()
    actual_dirs = set()
    for path in tree.rglob("*"):
        require(not path.is_symlink(), "original tree symlink")
        mode = path.lstat().st_mode
        name = path.relative_to(input_root).as_posix()
        if stat.S_ISREG(mode):
            actual_files.add(name)
        elif stat.S_ISDIR(mode):
            actual_dirs.add(name)
        else:
            raise CustodyError("special original entry: " + name)
    require(actual_files == originals, "extra/missing original file")
    expected_dirs = set()
    for name in originals:
        parent = PurePosixPath(name).parent
        while str(parent) != TREE:
            expected_dirs.add(str(parent))
            parent = parent.parent
    require(actual_dirs == expected_dirs, "extra/missing original directory")
    identity = read_json(input_root / "intake/ROOT_SOURCE_IDENTITY.json")
    selected = read_json(input_root / "intake/SELECTED_PUBLIC_RECORD.json")
    eligibility = read_json(input_root / "intake/ELIGIBILITY_GATE.json")
    gate = read_json(input_root / "root-receipts/MATH_GATE.json")
    require(identity.get("reviewed_head") == HEAD and identity.get("pr") == 786,
            "source identity target")
    require(identity.get("problem") == "30001223", "source identity problem")
    require(identity.get("selected_record_sha256") ==
            sha(bodies["intake/SELECTED_PUBLIC_RECORD.json"]), "selected raw identity")
    require(selected.get("problem", {}).get("id") == 30001223 and
            selected.get("prior_research") == {}, "complete selected/prior mismatch")
    statement_pin = sha(selected["problem"]["statement"].encode("utf-8"))
    review_pin = sha(json.dumps([selected["problem"], selected["prior_research"]],
                                sort_keys=True).encode("utf-8"))
    require(identity.get("statement_sha256") == statement_pin and
            identity.get("review_hash") == review_pin, "statement/review identity")
    source_rows = identity.get("original_files")
    require(isinstance(source_rows, list) and len(source_rows) == 41,
            "source original coverage")
    source_names = set()
    for row in source_rows:
        name = "intake/original/" + row["path"]
        require(name in originals and name not in source_names, "source original inventory")
        source_names.add(name)
        require(row.get("bytes") == len(bodies[name]) and
                row.get("sha256") == sha(bodies[name]), "source original digest")
        blob = b"blob " + str(len(bodies[name])).encode("ascii") + b"\0" + bodies[name]
        require(row.get("git_blob") == hashlib.sha1(blob).hexdigest(), "source git blob")
    require(source_names == originals, "source inventory incomplete")
    pr = eligibility.get("pr_metadata", {})
    require(eligibility.get("result") == "ELIGIBLE" and
            eligibility.get("queue_status") == "claimed_solved" and
            eligibility.get("original_explicit_budget") == "1/5", "eligibility mismatch")
    require(pr.get("headRefOid") == HEAD and pr.get("number") == 786 and
            pr.get("state") == "OPEN" and pr.get("isDraft") is True and
            pr.get("merged") is False, "frozen draft/head mismatch")
    require(gate.get("reviewed_head") == HEAD and gate.get("pr") == 786 and
            gate.get("problem") == "30001223", "math gate identity")
    require(gate.get("result") ==
            "PASS_COMPLETE_NEGATIVE_TO_BOTH_BROAD_Miyachi2009_BRIDGES", "closed math gate")
    require(gate.get("statement_sha256") == statement_pin and
            gate.get("review_hash") == review_pin and
            gate.get("original_explicit_budget") == "1/5" and
            gate.get("new_substantive_proof_turns") == 0, "gate binding")
    snapshot = read_json(root / "PEER_READ_SNAPSHOT.json")
    expected_peer = {
        "priority_example/REPORT_PRE_PEER.md": "c85ae98cf29c46d2a3c0b399486edfa1b8c21309da388bfb884b9a2c0b338a47",
        "priority_example/POSITION_PRE_PEER.json": "09755bf50d7e9d25e22d21bde0b3d471843ec9a671aaae91754c159b8174c2d5",
        "priority_example/SOURCE_LEDGER.json": "0d01b47f7d2a75c2c9c105cea99d768e97751f65ed717852bba8f054c7ba0c51",
        "priority_example/EXACT_COMPARISON.md": "37c17bab1398c22b577b216cb5b0f81b2f1949cda601b19add25e68e25e9491b",
    }
    peer_rows = snapshot.get("files")
    require(isinstance(peer_rows, list) and len(peer_rows) == 4, "peer snapshot coverage")
    peer_names = set()
    for row in peer_rows:
        name = row["relative_source"]
        require(name in expected_peer and name not in peer_names, "peer snapshot inventory")
        peer_names.add(name)
        data = row["utf8"].encode("utf-8")
        require(row["bytes"] == len(data) and row["sha256"] == sha(data) ==
                expected_peer[name], "peer snapshot digest")
    require(peer_names == set(expected_peer), "peer snapshot missing")
    return {"result": "PASS", "head": HEAD, "manifest_sha256": expected,
            "hashed_authored_files": len(names), "input_files": len(rows),
            "original_files": len(originals), "explicit_exceptions": EXCEPTIONS,
            "optimized": not __debug__, "source_git_blobs_checked": 41}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-manifest-sha256", required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).absolute().parent)
    parser.add_argument("--input-root", type=Path)
    args = parser.parse_args()
    try:
        require(args.root.is_dir() and not args.root.is_symlink(), "packet root symlink/missing")
        root = args.root.absolute()
        input_root = (args.input_root or root.parent).absolute()
        require(input_root.is_dir() and not input_root.is_symlink(), "input root symlink/missing")
        result = verify(root, input_root, args.expected_manifest_sha256)
    except (CustodyError, OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(json.dumps({"result": "FAIL", "error": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0

if __name__ == "__main__":
    sys.exit(main())
