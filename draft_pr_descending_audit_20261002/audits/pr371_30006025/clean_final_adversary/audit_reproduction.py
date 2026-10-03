#!/usr/bin/env python3
"""Reproduce frozen author/review evidence without modifying the shared checkout.

Run with --python pointing to an interpreter with the declared SymPy dependency.
All source assets, raw API objects, private Git state, and stdout/stderr stay ignored.
The public receipt records every field of each parsed mathematical checker output.
"""
import argparse
import base64
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

HEAD = "51fddd150e8da33f4cf17b1a642a0ffd3466bf5d"
BASE = "efd29c05204703acca9a0860812f54b94fae54b1"
AUTHOR = "308b3ee53312800cfe6a82a2cdcc9763e1f90422"
PREFIX = "problems/30006025_geometric_chapuy/"
ROOT = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT / "private/clone"), *args])


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2) + "\n")


def run_checker(py, directory, script, expected, label, extra=()):
    proc = subprocess.run([py, script, *extra], cwd=directory, capture_output=True)
    out = ROOT / "private/replays"
    out.mkdir(parents=True, exist_ok=True)
    (out / (label + ".stdout")).write_bytes(proc.stdout)
    (out / (label + ".stderr")).write_bytes(proc.stderr)
    row = {"label": label, "exit": proc.returncode, "stdout_sha256": sha(proc.stdout),
           "stderr_sha256": sha(proc.stderr), "stderr_bytes": len(proc.stderr),
           "stdout_bytes": len(proc.stdout)}
    if expected is not None:
        row.update(expected_sha256=sha(expected), byte_equal=proc.stdout == expected)
        if script.endswith("checks.py") or script.startswith("verify_turn"):
            row["parsed_full_stdout"] = json.loads(proc.stdout) if proc.returncode == 0 else None
            row["full_json_equal"] = row["parsed_full_stdout"] == json.loads(expected)
    else:
        row["full_stdout"] = proc.stdout.decode()
    return row


def verify_record(directory, record):
    data = (directory / record["path"]).read_bytes()
    wanted_size = record.get("bytes", record.get("size"))
    wanted_blob = record.get("git_blob_sha1", record.get("sha"))
    row = {"path": record["path"], "bytes": len(data), "sha256": sha(data),
           "git_blob": blob(data), "size_equal": len(data) == wanted_size}
    if "sha256" in record:
        row["sha256_equal"] = row["sha256"] == record["sha256"]
    if wanted_blob:
        row["git_blob_equal"] = row["git_blob"] == wanted_blob
    row["passed"] = all(v for k, v in row.items() if k.endswith("equal"))
    return row


def initialize_private_snapshot(repository):
    """Extract only the frozen 47-path publication scope into ignored storage."""
    private = ROOT / "private"
    private.mkdir(exist_ok=True)
    clone = private / "clone"
    if not clone.exists():
        subprocess.run(["git", "clone", "--shared", "--no-checkout", str(repository), str(clone)], check=True)
    paths = git("diff", "--name-only", BASE, HEAD).decode().splitlines()
    assert len(paths) == 47
    assert sum(path.startswith(PREFIX) for path in paths) == 46
    assert set(paths) - {path for path in paths if path.startswith(PREFIX)} == {"unsolved_math_prioritization/QUEUE.md"}
    inventory = []
    for path in paths:
        data = git("show", HEAD + ":" + path)
        dest = private / "snapshot" / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        inventory.append({"path": path, "bytes": len(data), "sha256": sha(data), "git_blob": blob(data)})
    save("FROZEN_FILE_INVENTORY.json", {"head": HEAD, "base": BASE, "paths": inventory,
         "path_count": 47, "target_file_count": 46})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--python", required=True)
    ap.add_argument("--remote-bytes", action="store_true")
    ap.add_argument("--repo", type=Path, help="Local repository containing frozen Git objects; initialize an ignored shared clone and 47-file snapshot.")
    args = ap.parse_args()
    if args.repo is not None:
        initialize_private_snapshot(args.repo.resolve())
    directory = ROOT / "private/snapshot" / PREFIX
    rows = []
    for turn in range(1, 6):
        rows.append(run_checker(args.python, directory, f"verify_turn{turn}.py",
                                (directory / f"TURN_{turn}_CHECKS.json").read_bytes(), f"final_author_{turn}"))
    environment = subprocess.check_output([args.python, "-c", "import sys,sympy,json; print(json.dumps({'python':sys.version,'sympy':sympy.__version__}))"]).decode().strip()
    save("AUTHOR_REPLAY_FULL_RECEIPT.json", {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "head": HEAD, "environment": json.loads(environment), "replays": rows,
         "all_passed": all(r["exit"] == 0 and r["byte_equal"] and r["full_json_equal"] and r["stderr_bytes"] == 0 for r in rows),
         "assertions": sum(r["parsed_full_stdout"]["assertions"] for r in rows if r["parsed_full_stdout"])})

    bindings = []
    for name in ["FINAL_AUTHOR_MANIFEST.json", "PUBLICATION_MANIFEST.json", *[f"TURN_{i}_MANIFEST.json" for i in range(1, 6)]]:
        obj = json.loads((directory / name).read_text())
        found = [verify_record(directory, r) for r in obj["files"]]
        extra = {"manifest": name, "manifest_sha256": sha((directory / name).read_bytes()), "records": found}
        if "previous_manifest_sha256" in obj:
            number = int(name.split("_")[1])
            extra["previous_manifest_equal"] = obj["previous_manifest_sha256"] == sha((directory / f"TURN_{number-1}_MANIFEST.json").read_bytes())
        bindings.append(extra)
    review = directory / "independent_review"
    review_manifest = json.loads((review / "REVIEW_MANIFEST.json").read_text())
    bindings.append({"manifest": "independent_review/REVIEW_MANIFEST.json",
                     "records": [verify_record(review, r) for r in review_manifest["files"]]})
    remote_binding = json.loads((review / "REMOTE_BINDING.json").read_text())
    historical = ROOT / "private/historical_author"
    historical.mkdir(exist_ok=True)
    historical_rows = []
    for r in remote_binding["files"]:
        data = git("show", AUTHOR + ":" + PREFIX + r["path"])
        p = historical / r["path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        check = verify_record(historical, r)
        check["publication_bytes_equal"] = data == (directory / r["path"]).read_bytes()
        historical_rows.append(check)
    review_rows = [run_checker(args.python, review, "independent_checks.py", (review / "INDEPENDENT_CHECKS.json").read_bytes(), "historical_independent_checks"),
                  run_checker(args.python, review, "verify_review.py", None, "historical_review_on_actual_author_commit", ("--author-dir", str(historical))),
                  run_checker(args.python, review, "verify_review.py", None, "historical_review_on_publication_target", ("--author-dir", str(directory)))]
    full_old = json.loads((review / "AUTHOR_REPLAY.json").read_text())
    review_checks = {"old_author_receipt": full_old,
                     "old_author_full_json_equal": full_old["receipts"] == [r["parsed_full_stdout"] for r in rows]}
    save("MANIFEST_AND_HISTORICAL_REPLAY.json", {"head": HEAD, "author_commit": AUTHOR,
         "manifest_bindings": bindings, "historical_author_bindings": historical_rows,
         "review_replays": review_rows, "historical_receipt_comparison": review_checks,
         "all_record_bindings_pass": all(r["passed"] for b in bindings for r in b["records"]) and all(r["passed"] and r["publication_bytes_equal"] for r in historical_rows)})

    commits = ["6fb965118ce87d6a25afa60f92cc21c78605eb4b", "649acde2cf13c0a89ba7433b5cf4214e45cb8901", "96158499a002790d1e82a62b8d43ee47836a312b", "67c1e19c1c56f757896f509fab402441e99a58ea", AUTHOR]
    chain = []
    for turn, commit in enumerate(commits, 1):
        parent = git("show", "-s", "--format=%P", commit).decode().strip()
        state = json.loads(git("show", commit + ":" + PREFIX + f"TURN_{turn}_STATE.json"))
        change_paths = git("diff", "--name-only", parent, commit).decode().splitlines()
        scope_paths = git("ls-tree", "-r", "--name-only", commit, PREFIX).decode().splitlines()
        chain.append({"turn": turn, "commit": commit, "parent": parent,
                      "commit_metadata": git("show", "-s", "--format=%aI%n%cI%n%s", commit).decode().splitlines(),
                      "state": state, "parent_is_prior_checkpoint": parent == (BASE if turn == 1 else commits[turn-2]),
                      "changed_paths": change_paths, "target_scope_count": len(scope_paths),
                      "proof_preserved_in_final": git("show", commit + ":" + PREFIX + f"TURN_{turn}.md") == (directory / f"TURN_{turn}.md").read_bytes(),
                      "manifest_preserved_in_final": git("show", commit + ":" + PREFIX + f"TURN_{turn}_MANIFEST.json") == (directory / f"TURN_{turn}_MANIFEST.json").read_bytes()})
    save("CHECKPOINT_PROVENANCE.json", {"head": HEAD, "base": BASE, "head_parents": git("show", "-s", "--format=%P", HEAD).decode().strip().split(),
         "five_checkpoints": chain, "author_wip_changed_paths_from_base": git("diff", "--name-only", BASE, AUTHOR).decode().splitlines(),
         "publication_changed_paths_from_base": git("diff", "--name-only", BASE, HEAD).decode().splitlines(),
         "scope_note": "Historical author binding is the actual 37-file author target at AUTHOR, not the entire WIP repository. Publication is 46 target files plus QUEUE. The old review verifier's author-dir hash binding has been replayed on both exact scopes; it does not certify outside WIP paths."})

    if args.remote_bytes:
        inventories = json.loads((ROOT / "FROZEN_FILE_INVENTORY.json").read_text())["paths"]
        output = ROOT / "private/api/contents"
        output.mkdir(exist_ok=True)

        def get_remote(record):
            path = record["path"]
            result = subprocess.run(["gh", "api", "repos/AlecKriebel/Math/contents/" + path + "?ref=" + HEAD], capture_output=True)
            name = path.replace("/", "__")
            (output / (name + ".stdout")).write_bytes(result.stdout)
            (output / (name + ".stderr")).write_bytes(result.stderr)
            if result.returncode:
                return {"path": path, "exit": result.returncode}
            obj = json.loads(result.stdout)
            data = base64.b64decode(obj["content"])
            return {"path": path, "exit": 0, "api_blob": obj["sha"], "api_size": obj["size"],
                    "byte_equal": data == (ROOT / "private/snapshot" / path).read_bytes(),
                    "git_blob_equal": obj["sha"] == record["git_blob"], "size_equal": len(data) == record["bytes"], "sha256": sha(data)}

        remote_rows = list(concurrent.futures.ThreadPoolExecutor(8).map(get_remote, inventories))
        save("FROZEN_REMOTE_BYTES_RECEIPT.json", {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "head": HEAD,
             "path_count": len(remote_rows), "paths": remote_rows,
             "all_passed": all(r.get("byte_equal") and r.get("git_blob_equal") and r.get("size_equal") for r in remote_rows)})
    print("Completed full author, historical review, manifest, checkpoint, and optional remote-byte replay.")


if __name__ == "__main__":
    main()
