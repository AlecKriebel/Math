"""Commit only completed PR50 v3 work in the acknowledged main writer window."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import stat
import subprocess

F = Path(__file__).resolve().parent
A = F.parent
P = A.parents[1]
R = P.parent
J = F / "tmp" / "v3_checkpoint_commands.jsonl"
J.parent.mkdir(exist_ok=True)
assert not J.exists(), "Keep previous command evidence"

def run(argv):
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    process = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    record = {"argv": argv, "cwd": str(R), "pid": process.pid,
              "started_utc": start, "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "exit_code": process.returncode, "stdout": out.decode("utf-8", "replace"),
              "stderr": err.decode("utf-8", "replace"), "stdin_supplied": False}
    with J.open("a") as f:
        f.write(json.dumps(record) + "\n")
    if process.returncode:
        raise RuntimeError("Command failed; full evidence preserved: " + repr(argv))
    return out

def git(*args):
    return run(["git", *args])

def bound(path):
    if not path.exists() and not path.is_symlink():
        return {"kind": "absent"}
    mode = stat.S_IMODE(path.lstat().st_mode)
    if path.is_symlink():
        return {"kind": "symlink", "target": str(path.readlink()), "mode": mode}
    assert path.is_file(), str(path)
    body = path.read_bytes()
    return {"kind": "regular", "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "mode": mode}

def paths(body):
    return set(p.decode() for p in body.split(b"\0") if p)

assert git("branch", "--show-current").strip() == b"main"
window = json.loads((R / "draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json").read_text())
assert window["shared_git_writes_paused"] is True and "PR50 v3" in window["paused_for"]
assert git("diff", "--cached", "--name-only", "-z") == b"", "Never unstage a foreign index"
before = git("rev-parse", "HEAD").decode().strip()
assert before == window["local_main_at_pause"] == window["remote_main_at_pause"]
assert git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == before
decision = json.loads((F / "V3_FINAL_REVIEW_AND_PRIORITY_HOLD.json").read_text())
assert decision["mandatory_upload_package_repairs_found"] == []
assert decision["publication_approval"] is False and decision["goal_complete"] is False
roots = [str(P.relative_to(R) / name) for name in ["CURRENT_PROGRESS.json", "README.md"]]
roots += [str(A.relative_to(R) / name) for name in [
    "ROOT_RESEARCH_LOG.md", "ROOT_CURRENT_REVIEW_20261004.md", "publication_package_v3",
    "root_current_promotion_20261004", "v2_wholepackage_adversary_20261004", "v3_wholepackage_adversary_20261004"]]
C = A.parent / "pr45_9900007"
roots.append(str((C / "root_pr50_priority_hold_scoped_checkpoint_v2_actual_capture").relative_to(R)))
for capture in sorted(C.glob("root_pr50_v3_*actual_capture")):
    if capture.name == "root_pr50_v3_checkpoint_push_actual_capture":
        continue
    record = json.loads((capture / "CAPTURE.json").read_text())
    assert record["completed"] is True and record["status"] == "PASS"
    roots.append(str(capture.relative_to(R)))
names = paths(git("diff", "--name-only", "-z", "--", *roots))
names |= paths(git("ls-files", "--others", "--exclude-standard", "-z", "--", *roots))
names = {name for name in names if not name.endswith(".log")}
assert names
for name in names:
    assert any(name == root or name.startswith(root + "/") for root in roots)
    assert all(part not in {"private", "output", "tmp", "__pycache__"} for part in Path(name).parts), name
    assert not name.endswith(".log")
owned = {name: bound(R / name) for name in sorted(names)}
assert all(pin["kind"] == "regular" for pin in owned.values())
dirty = paths(git("diff", "--name-only", "-z"))
foreign = {name: bound(R / name) for name in sorted(dirty - names)}
plan_path = F / "V3_SCOPED_CHECKPOINT_PLAN.json"
assert not plan_path.exists()
plan = {"UTC": dt.datetime.now(dt.timezone.utc).isoformat(), "precommit_main": before,
        "scope_roots": roots, "owned_paths": owned, "foreign_dirty_bindings": foreign,
        "index_initially_empty": True, "shared_window": window,
        "review_clearance": "mathematics and exact v3 portable package only",
        "priority_clearance": False, "publication_approval": False, "goal_complete": False}
plan_path.write_text(json.dumps(plan, indent=2) + "\n")
plan_name = str(plan_path.relative_to(R))
names.add(plan_name)
owned[plan_name] = bound(plan_path)
git("add", "--", *sorted(names))
assert paths(git("diff", "--cached", "--name-only", "-z")) == names
for name, pin in owned.items():
    assert bound(R / name) == pin, "Owned file changed during stage: " + name
    assert hashlib.sha256(git("show", ":" + name)).hexdigest() == pin["sha256"]
for name, pin in foreign.items():
    assert bound(R / name) == pin, "Foreign tracked file changed: " + name
git("commit", "-m", "Repair PR50 source-bound diagnostics and record fresh review with priority hold")
after = git("rev-parse", "HEAD").decode().strip()
assert git("rev-list", "--parents", "-n", "1", after).decode().split() == [after, before]
assert paths(git("diff-tree", "--no-commit-id", "--name-only", "-r", "-z", after)) == names
assert git("diff", "--cached", "--name-only", "-z") == b""
for name, pin in owned.items():
    assert hashlib.sha256(git("show", after + ":" + name)).hexdigest() == pin["sha256"]
for name, pin in foreign.items():
    assert bound(R / name) == pin
assert git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == before
git("push", "origin", "main")
assert git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == after
assert git("rev-parse", "HEAD").decode().strip() == after
assert git("diff", "--cached", "--name-only", "-z") == b""
for name, pin in foreign.items():
    assert bound(R / name) == pin
receipt = {"UTC": dt.datetime.now(dt.timezone.utc).isoformat(),
    "status": "PASS_SCOPED_V3_MAIN_COMMIT_PUSH_AND_FOREIGN_PRESERVATION",
    "commit": after, "parent": before, "committed_path_count": len(names),
    "foreign_dirty_existing_paths_preserved": len(foreign), "index_finally_empty": True,
    "genuine_PR_merge_performed": False, "Zenodo_or_tracker_write_performed": False,
    "priority_clearance": False, "publication_approval": False, "goal_complete": False,
    "raw_git_command_evidence": str(J.relative_to(R)),
    "raw_git_command_evidence_sha256": hashlib.sha256(J.read_bytes()).hexdigest(),
    "receipt_self_reference": "Receipt written after the actual commit/push; not claimed as part of that commit"}
receipt_path = F / "V3_SCOPED_CHECKPOINT_RECEIPT.json"
assert not receipt_path.exists()
receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
