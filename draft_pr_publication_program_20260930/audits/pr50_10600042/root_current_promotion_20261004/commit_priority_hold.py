"""Scoped main-only checkpoint inside the acknowledged shared writer window."""
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
def run(argv):
    return subprocess.run(argv, cwd=R, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
def git(*args):
    return run(["git", *args])
def bound(path):
    mode = stat.S_IMODE(path.lstat().st_mode)
    if path.is_symlink():
        return {"kind": "symlink", "target": str(path.readlink()), "mode": mode}
    if not path.is_file():
        return {"kind": "nonregular", "mode": mode}
    b = path.read_bytes()
    return {"kind": "regular", "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "mode": mode}
assert git("branch", "--show-current").strip() == b"main"
window = json.loads((R / "draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json").read_text())
assert window["shared_git_writes_paused"] is True and "PR50" in window["paused_for"]
assert git("diff", "--cached", "--name-only", "-z") == b"", "Never unstage foreign index entries"
before = git("rev-parse", "HEAD").decode().strip()
assert git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == before
roots = [str(P.relative_to(R) / "CURRENT_PROGRESS.json"), str(P.relative_to(R) / "README.md")]
for name in ("ROOT_RESEARCH_LOG.md", "ROOT_CURRENT_REVIEW_20261004.md", "current_promotion_adversary_20261004", "native_acceptance_plan_20261004", "nencka_priority_resolution_20261004", "publication_package_v2", "root_current_promotion_20261004"):
    roots.append(str(A.relative_to(R) / name))
C = A.parent / "pr45_9900007"
roots.append(str((C / "root_pr50_priority_hold_scoped_checkpoint_actual_capture").relative_to(R)))
for path in sorted(C.glob("root_pr50_*20261004_actual_capture")):
    assert (path / "CAPTURE.json").exists(), "Capture must be completed before staging"
    roots.append(str(path.relative_to(R)))
names = set()
for args in (("diff", "--name-only", "-z", "--", *roots), ("ls-files", "--others", "--exclude-standard", "-z", "--", *roots)):
    names.update(p.decode() for p in git(*args).split(b"\0") if p)
names = {name for name in names if not name.endswith(".log")}
assert names and all(not ("/private/" in name or "/v2_wholepackage_adversary_20261004/" in name or "/output/" in name or name.endswith(".log")) for name in names)
assert all(any(name == root or name.startswith(root + "/") for root in roots) for name in names)
owned = {name: bound(R / name) for name in sorted(names)}
dirty = set(p.decode() for p in git("diff", "--name-only", "-z").split(b"\0") if p)
foreign = {name: bound(R / name) for name in sorted(dirty - names)}
plan = {"UTC": dt.datetime.now(dt.timezone.utc).isoformat(), "precommit_main": before, "owned_paths": owned,
        "foreign_dirty_bindings": foreign, "index_initially_empty": True, "shared_window": window,
        "claimed_solution_publication_approval": False, "new_priority_gap": "Fuller Nencka sources required", "goal_complete": False}
(F / "SCOPED_CHECKPOINT_PLAN.json").write_text(json.dumps(plan, indent=2) + "\n")
plan_name = str((F / "SCOPED_CHECKPOINT_PLAN.json").relative_to(R))
names.add(plan_name)
owned[plan_name] = bound(R / plan_name)
git("add", "--", *sorted(names))
staged = set(p.decode() for p in git("diff", "--cached", "--name-only", "-z").split(b"\0") if p)
assert staged == names
for name, pin in owned.items():
    assert bound(R / name) == pin, "Owned path changed during stage: " + name
    b = git("show", ":" + name)
    assert hashlib.sha256(b).hexdigest() == pin["sha256"]
for name, pin in foreign.items():
    assert bound(R / name) == pin, "Other writer changed foreign path: " + name
commit_output = git("commit", "-m", "Audit PR50 even-strand proof and preserve unresolved Nencka priority hold")
after = git("rev-parse", "HEAD").decode().strip()
assert git("rev-list", "--parents", "-n", "1", after).decode().split() == [after, before]
changed = set(p.decode() for p in git("diff-tree", "--no-commit-id", "--name-only", "-r", "-z", after).split(b"\0") if p)
assert changed == names and git("diff", "--cached", "--name-only", "-z") == b""
for name, pin in owned.items():
    assert hashlib.sha256(git("show", after + ":" + name)).hexdigest() == pin["sha256"]
for name, pin in foreign.items():
    assert bound(R / name) == pin
push_output = run(["git", "push", "origin", "main"])
assert git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == after
receipt = {"UTC": dt.datetime.now(dt.timezone.utc).isoformat(), "status": "PASS_SCOPED_MAIN_CHECKPOINT_PUSH_AND_FOREIGN_PRESERVATION",
           "commit": after, "parent": before, "staged_and_committed_path_count": len(names),
           "foreign_dirty_existing_paths_preserved": len(foreign), "index_finally_empty": True,
           "original_PR50_head_not_merged": True, "no_Zenodo_Sheets_or_GitHub_action": True,
           "priority_resolution_pending": True, "publication_approval": False, "goal_complete": False}
(F / "SCOPED_CHECKPOINT_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(commit_output.decode())
print(push_output.decode())
print(json.dumps(receipt, indent=2))
