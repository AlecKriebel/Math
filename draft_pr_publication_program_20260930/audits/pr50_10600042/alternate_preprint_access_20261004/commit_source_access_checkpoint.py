"""Scoped checkpoint of completed source-access limits; no research promotion."""
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
C = A.parent / "pr45_9900007"
J = F / "private" / "checkpoint_commands.jsonl"
assert not J.exists()

def run(argv):
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = child.communicate()
    record = {"argv": argv, "cwd": str(R), "pid": child.pid, "started_utc": start,
        "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "exit_code": child.returncode,
        "stdout": out.decode("utf-8", "replace"), "stderr": err.decode("utf-8", "replace")}
    with J.open("a") as stream:
        stream.write(json.dumps(record) + "\n")
    if child.returncode:
        raise RuntimeError("Actual command failed; full evidence is retained: " + repr(argv))
    return out

def git(*args):
    return run(["git", *args])

def paths(body):
    return {item.decode() for item in body.split(b"\0") if item}

def bound(path):
    if not path.exists() and not path.is_symlink():
        return {"kind": "absent"}
    mode = stat.S_IMODE(path.lstat().st_mode)
    if path.is_symlink():
        return {"kind": "symlink", "target": str(path.readlink()), "mode": mode}
    assert path.is_file()
    body = path.read_bytes()
    return {"kind": "regular", "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "mode": mode}

assert git("branch", "--show-current").strip() == b"main"
assert git("diff", "--cached", "--name-only", "-z") == b"", "Never unstage foreign entries"
window = json.loads((R / "draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json").read_text())
assert window["shared_git_writes_paused"] is True and "PR50 new source-access" in window["paused_for"]
before = git("rev-parse", "HEAD").decode().strip()
assert before == window["local_main_at_pause"] == window["remote_main_at_pause"]
assert git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == before
record = json.loads((F / "SOURCE_ACCESS_CONTINUATION.json").read_text())
assert record["full_Nencka_body_acquired"] is False and record["publication_approval"] is False
roots = [str(P.relative_to(R) / "CURRENT_PROGRESS.json"), str(A.relative_to(R) / "ROOT_RESEARCH_LOG.md"),
    str(F.relative_to(R)), str(A.relative_to(R) / "nencka_cpt_access_20261004"),
    str(A.relative_to(R) / "root_current_promotion_20261004/V3_SCOPED_CHECKPOINT_RECEIPT.json")]
capture_names = ["root_pr50_v3_checkpoint_push_actual_capture",
    "root_pr50_alternate_cpt_access_20261004_actual_capture",
    "root_pr50_alternate_mp_arc_access_20261004_actual_capture",
    "root_pr50_current_static_archive_20261004_actual_capture",
    "root_pr50_priority_blocker_current_pr_20261004_actual_capture",
    "root_pr50_public_source_access_record_20261004_actual_capture"]
for name in capture_names:
    capture = C / name
    observed = json.loads((capture / "CAPTURE.json").read_text())
    assert observed["completed"] is True and observed["status"] == "PASS"
    roots.append(str(capture.relative_to(R)))
names = paths(git("diff", "--name-only", "-z", "--", *roots))
names |= paths(git("ls-files", "--others", "--exclude-standard", "-z", "--", *roots))
assert names
for name in names:
    assert any(name == root or name.startswith(root + "/") for root in roots)
    assert all(part not in {"private", "tmp", "output", "__pycache__"} for part in Path(name).parts), name
    assert not name.endswith(".log")
assert str((C / capture_names[1] / "stdout.bin").relative_to(R)) not in names
owned = {name: bound(R / name) for name in sorted(names)}
assert all(item["kind"] == "regular" for item in owned.values())
foreign = {name: bound(R / name) for name in sorted(paths(git("diff", "--name-only", "-z")) - names)}
plan_path = F / "SCOPED_SOURCE_CHECKPOINT_PLAN.json"
assert not plan_path.exists()
plan_path.write_text(json.dumps({"UTC": dt.datetime.now(dt.timezone.utc).isoformat(),
    "precommit_main": before, "owned_bindings": owned, "foreign_dirty_bindings": foreign,
    "acknowledged_shared_window": window, "publication_approval": False, "goal_complete": False}, indent=2) + "\n")
plan_name = str(plan_path.relative_to(R))
names.add(plan_name)
owned[plan_name] = bound(plan_path)
git("add", "--", *sorted(names))
assert paths(git("diff", "--cached", "--name-only", "-z")) == names
for name, binding in owned.items():
    assert bound(R / name) == binding
    assert hashlib.sha256(git("show", ":" + name)).hexdigest() == binding["sha256"]
for name, binding in foreign.items():
    assert bound(R / name) == binding
git("commit", "-m", "Record PR50 public source-access limits and preserve priority hold")
after = git("rev-parse", "HEAD").decode().strip()
assert git("rev-list", "--parents", "-n", "1", after).decode().split() == [after, before]
assert paths(git("diff-tree", "--no-commit-id", "--name-only", "-r", "-z", after)) == names
assert git("diff", "--cached", "--name-only", "-z") == b""
for name, binding in owned.items():
    assert hashlib.sha256(git("show", after + ":" + name)).hexdigest() == binding["sha256"]
for name, binding in foreign.items():
    assert bound(R / name) == binding
assert git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == before
git("push", "origin", "main")
assert git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == after
assert git("diff", "--cached", "--name-only", "-z") == b""
for name, binding in foreign.items():
    assert bound(R / name) == binding
receipt = {"UTC": dt.datetime.now(dt.timezone.utc).isoformat(), "status": "PASS_SCOPED_SOURCE_LIMITS_MAIN_PUSH",
    "commit": after, "parent": before, "owned_committed_path_count": len(names),
    "foreign_dirty_tracked_paths_preserved": len(foreign), "index_finally_empty": True,
    "priority_clearance": False, "publication_approval": False, "goal_complete": False,
    "PR_merge_close_Zenodo_tracker_or_advance_performed": False,
    "actual_command_journal_sha256": hashlib.sha256(J.read_bytes()).hexdigest(),
    "receipt_note": "Written after genuine commit and push; not claimed included in its own commit"}
dest = F / "SCOPED_SOURCE_CHECKPOINT_RECEIPT.json"
assert not dest.exists()
dest.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
