#!/usr/bin/env python3
"""Root read-only replay after actual immutable Git/disk authentication.

Run only after static review of all nine original Python programs. No network,
original-file mutation, Git mutation, or theorem/priority acceptance is performed.
"""
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile

AUDIT = Path(__file__).absolute().parent
REPO = AUDIT.parents[2]
HEAD = "2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b"
PREFIX = "unsolved_math_prioritization/attempts/30003634"
PIN = "149e6144f0ad90ee12945c29155318100b65c6faee8ba2661d2c09db58b9ae30"
PYTHON = REPO / "draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python"


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def authenticate():
    packet = AUDIT / "original" / PREFIX
    current = packet
    while True:
        need(not current.is_symlink(), "symlink ancestor")
        if current == current.parent:
            break
        current = current.parent
    snapshot = json.loads((AUDIT / "ORIGINAL_SNAPSHOT.json").read_text())
    need(snapshot["head"] == HEAD, "wrong head")
    listing = subprocess.check_output(["git", "ls-tree", "-r", "-z", HEAD, "--", PREFIX], cwd=REPO)
    records = []
    for item in listing.split(b"\0"):
        if not item:
            continue
        metadata, raw_path = item.split(b"\t", 1)
        mode, kind, blob = metadata.decode().split()
        name = raw_path.decode()
        need(mode == "100644" and kind == "blob", "nonregular Git member")
        raw = subprocess.check_output(["git", "cat-file", "blob", blob], cwd=REPO)
        digest = hashlib.sha256(raw).hexdigest()
        disk = AUDIT / "original" / name
        need(stat.S_ISREG(disk.lstat().st_mode), "nonregular disk member")
        need(disk.read_bytes() == raw and snapshot["files"].get(name) == digest, "actual Git/disk/snapshot mismatch")
        if name.endswith(".py"):
            need(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse(raw))), "optimization-removable check")
        records.append({"path": name[len(PREFIX)+1:], "bytes": len(raw), "sha256": digest, "git_blob": blob})
    need(len(records) == 44 and len(snapshot["files"]) == 44, "wrong file count")
    actual = {p.relative_to(packet).as_posix() for p in packet.rglob("*") if p.is_file()}
    need(actual == {r["path"] for r in records}, "copied inventory mismatch")
    for p in packet.rglob("*"):
        need(not p.is_symlink() and (p.is_file() or p.is_dir()), "special copied member")
    return packet, records


def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    packet, before = authenticate()
    private = AUDIT / "private"
    private.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="root-replay-", dir=private) as tmp:
        tmp = Path(tmp)
        work = tmp / "packet"
        shutil.copytree(packet, work)
        for p in [work, *work.rglob("*")]:
            p.chmod(0o755 if p.is_dir() else 0o644)
        launcher = tmp / "external_bootstrap.py"
        launcher.write_bytes((work / "BOOTSTRAP.py").read_bytes())
        env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        command = [str(PYTHON), "-I", "-B", str(launcher), "--packet", str(work), "--expected-manifest", PIN, "--mode=normal"]
        result = subprocess.run(command, cwd=tmp, env=env, capture_output=True, timeout=900)
        need(result.returncode == 0 and not result.stderr, "replay failed: " + result.stderr.decode(errors="replace")[-3000:])
        output = json.loads(result.stdout)
        need(output["status"] == "PASS" and output["bound_files"] == 43, "unexpected finite replay result")
        (AUDIT / "ROOT_PUBLICATION_REPLAY.json").write_bytes(result.stdout)
    _, after = authenticate()
    need(before == after, "original files changed")
    receipt = {"started_utc": started, "completed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "status": "PASS", "head": HEAD, "actual_git_files_authenticated_before_and_after": 44, "original_python_programs_statically_reviewed_before_execution": 9, "copied_packet_executed": True, "external_launcher_sha256": hashlib.sha256((packet / "BOOTSTRAP.py").read_bytes()).hexdigest(), "publication_manifest_sha256": PIN, "scope": "Root normal outer replay; outer result includes its exact component tests. Other parent modes and hostile controls separately reproduced by the independent family. No formal topology, priority, or human review certificate.", "source_download_hashes": "separate ROOT_STATIC_AND_SOURCE_RECEIPT.json, not all historical PDF hashes", "original_author_turns": "1/5", "positive_proof_search_turns_added": 0}
    (AUDIT / "ROOT_REPLAY_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
