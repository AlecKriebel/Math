#!/usr/bin/env python3
"""Authenticate this bounded priority audit; this is not a novelty/proof oracle."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys

HEAD = "aa44dec3baf8c1cd179cf8b55f32be95c74ee81a"
STATEMENT = "628ed4ce70b7b62857ead560403291f24b890137a8073ce34a17c50d857aa3a6"
REVIEW = "cf0071b62b0e096c74205deac1c8f7cad50cbbf50b4f37d8400170a2d742848f"
SELECTED = "66a5a85f2cd0d2d2aec94ebcc590c6cc05eb7131eff1e29578ff7e8e4c66dbb4"
VERDICT = "PRIORITY_UNRESOLVED_NO_VERIFIED_FULL_PREDECESSOR"


def demand(condition, message):
    if not condition:
        raise ValueError(message)


def pairs(items):
    out = {}
    for key, value in items:
        demand(key not in out, "duplicate JSON key")
        out[key] = value
    return out


def decode(data):
    def bad(value):
        raise ValueError("nonfinite JSON number")
    return json.loads(data, object_pairs_hook=pairs, parse_constant=bad)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def absolute(path):
    return Path(os.path.abspath(os.fspath(path)))


def guard_parents(path):
    path = absolute(path)
    for part in [path] + list(path.parents):
        st = part.lstat()
        demand(stat.S_ISDIR(st.st_mode) and not stat.S_ISLNK(st.st_mode),
               "unsafe directory or ancestor")
    return path


def read(path):
    path = absolute(path)
    guard_parents(path.parent)
    before = path.lstat()
    demand(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
           "nonregular, linked or symlink file")
    fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0))
    with os.fdopen(fd, "rb") as stream:
        opened = os.fstat(stream.fileno())
        demand((before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino),
               "file changed before read")
        data = stream.read()
        after = os.fstat(stream.fileno())
    demand((before.st_size, before.st_mtime_ns, before.st_ino) ==
           (after.st_size, after.st_mtime_ns, after.st_ino), "file changed during read")
    demand(len(data) == before.st_size, "file length changed")
    return data


def relative(value):
    demand(isinstance(value, str) and value and "\\" not in value,
           "unsafe relative path")
    p = PurePosixPath(value)
    demand(not p.is_absolute() and all(x not in ("", ".", "..") for x in value.split("/")),
           "unsafe relative path")
    demand(str(p) == value, "noncanonical path")
    return value


def rows_by_path(rows):
    demand(isinstance(rows, list), "rows must be a list")
    out = {}
    for row in rows:
        demand(isinstance(row, dict) and set(row) == {"path", "bytes", "sha256"},
               "invalid row")
        name = relative(row["path"])
        demand(name not in out, "duplicate row path")
        demand(type(row["bytes"]) is int and row["bytes"] >= 0, "invalid length")
        h = row["sha256"]
        demand(isinstance(h, str) and len(h) == 64 and
               all(c in "0123456789abcdef" for c in h), "invalid hash")
        out[name] = row
    return out


def verify_rows(root, rows):
    root = guard_parents(root)
    for name, row in rows_by_path(rows).items():
        data = read(root / name)
        demand(len(data) == row["bytes"] and digest(data) == row["sha256"],
               "bound input mismatch: " + name)
    return len(rows)


def walk(root):
    result = set()
    def scan(directory):
        entries = list(os.scandir(directory))
        demand(entries, "empty directory in packet")
        for entry in entries:
            p = Path(entry.path)
            st = entry.stat(follow_symlinks=False)
            demand(not stat.S_ISLNK(st.st_mode), "symlink in packet")
            if stat.S_ISDIR(st.st_mode):
                scan(p)
            else:
                demand(stat.S_ISREG(st.st_mode) and st.st_nlink == 1,
                       "nonregular or hardlinked packet entry")
                result.add(p.relative_to(root).as_posix())
    scan(root)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--packet-root", required=True)
    ap.add_argument("--input-root", required=True)
    ap.add_argument("--manifest-sha256", required=True)
    ap.add_argument("--checker-sha256", required=True)
    ap.add_argument("--primary-root")
    args = ap.parse_args()
    self_path = absolute(__file__)
    demand(digest(read(self_path)) == args.checker_sha256, "checker pin mismatch")
    root = guard_parents(args.packet_root)
    demand(self_path == root / "verify_priority.py", "checker invocation/root mismatch")
    mf = read(root / "MANIFEST.json")
    demand(digest(mf) == args.manifest_sha256, "external manifest pin mismatch")
    manifest = decode(mf)
    demand(set(manifest) == {"schema", "files"} and manifest["schema"] ==
           "pr789-priority-structural-manifest-v1", "manifest schema")
    rows = rows_by_path(manifest["files"])
    demand(walk(root) == set(rows) | {"MANIFEST.json"}, "packet closure mismatch")
    verify_rows(root, manifest["files"])
    inputs = decode(read(root / "INPUT_BINDINGS.json"))
    demand(set(inputs) == {"schema", "files"} and inputs["schema"] ==
           "pr789-intake-bindings-v1", "input schema")
    input_count = verify_rows(args.input_root, inputs["files"])
    intake = guard_parents(args.input_root)
    selected_data = read(intake / "SELECTED_PUBLIC_RECORD.json")
    demand(digest(selected_data) == SELECTED, "wrong selected candidate")
    selected = decode(selected_data)
    demand(selected["problem"]["id"] == 30001478 and selected["prior_research"] == {},
           "candidate identity/prior report mismatch")
    demand(digest(selected["problem"]["statement"].encode()) == STATEMENT,
           "wrong exact problem statement")
    demand(digest(json.dumps([selected["problem"], selected["prior_research"]],
                            sort_keys=True).encode()) == REVIEW, "review identity mismatch")
    gate = decode(read(intake / "ELIGIBILITY_GATE.json"))
    demand(gate["pr"] == 789 and gate["queue_status"] == "claimed_solved" and
           gate["pr_metadata"]["headRefOid"] == HEAD, "ineligible or wrong head")
    identity = decode(read(intake / "ROOT_SOURCE_IDENTITY.json"))
    demand(identity["reviewed_head"] == HEAD and identity["statement_sha256"] == STATEMENT
           and identity["review_hash"] == REVIEW, "intake identity mismatch")
    originals = identity["original_files"]
    demand(len(originals) == 58, "wrong original file count")
    for row in originals:
        data = read(intake / "original" / relative(row["path"]))
        git_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        demand(git_blob == row["git_blob"] and digest(data) == row["sha256"] and
               len(data) == row["bytes"], "original source blob mismatch")
    plan = read(root / "INDEPENDENT_PLAN.json")
    provisional = decode(read(root / "PROVISIONAL_INDEPENDENT_VERDICT.json"))
    demand(provisional["independent_plan_sha256"] == digest(plan) and
           provisional["prior_candidate_october_literature_read"] is False and
           provisional["peer_or_root_priority_conclusions_read"] is False,
           "independence binding mismatch")
    final = decode(read(root / "VERDICT.json"))
    demand(provisional["verdict"] == final["verdict"] == VERDICT and
           final["full_matching_prior_resolution_verified"] == [] and
           final["firstness_claim"] is False and final["exhaustive_absence_claim"] is False,
           "unsupported priority promotion")
    demand(final["provisional_sha256"] == digest(read(root / "PROVISIONAL_INDEPENDENT_VERDICT.json")),
           "provisional freeze changed")
    primary = decode(read(root / "PRIMARY_BODY_BINDINGS.json"))
    demand(set(primary) == {"schema", "files"} and primary["schema"] ==
           "pr789-primary-bodies-v1", "primary schema")
    rows_by_path(primary["files"])
    primary_count = verify_rows(args.primary_root, primary["files"]) if args.primary_root else 0
    print(json.dumps({"result": "PASS", "pr": 789, "problem": 30001478,
                      "reviewed_head": HEAD, "packet_files": len(rows) + 1,
                      "intake_inputs_verified": input_count,
                      "original_git_blobs_verified": len(originals),
                      "primary_files_recorded": len(primary["files"]),
                      "primary_files_verified": primary_count,
                      "priority_verdict": VERDICT,
                      "limitation": "Custody and recorded scope only; no automated proof or exhaustive literature claim."},
                     sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, UnicodeError) as exc:
        print("REJECT: " + str(exc), file=sys.stderr)
        sys.exit(2)
