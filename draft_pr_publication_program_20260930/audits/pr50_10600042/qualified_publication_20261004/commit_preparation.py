"""Push only completed ROOT preparation paths during an acknowledged main writer window."""
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
J = F / "preparation_git_commands.jsonl"
assert not J.exists()
def run(*args):
    argv = ["git", *args]
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    child = subprocess.Popen(argv, cwd=R, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL)
    out, err = child.communicate()
    with J.open("a") as stream:
        stream.write(json.dumps({"argv": argv, "pid": child.pid, "UTC_start": start,
            "UTC_end": dt.datetime.now(dt.timezone.utc).isoformat(), "exit": child.returncode,
            "stdout": out.decode("utf-8", "replace"), "stderr": err.decode("utf-8", "replace")}) + "\n")
    assert child.returncode == 0, (argv, err.decode("utf-8", "replace"))
    return out
def paths(body):
    return {x.decode() for x in body.split(b"\0") if x}
def bind(name):
    p = R / name
    if not p.exists():
        return {"absent": True}
    assert p.is_file() and not p.is_symlink()
    b = p.read_bytes()
    return {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "mode": stat.S_IMODE(p.stat().st_mode)}
assert run("branch", "--show-current").strip() == b"main"
assert run("diff", "--cached", "--name-only", "-z") == b""
w = json.loads((R / "draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json").read_text())
assert w["shared_git_writes_paused"] is True and "PR50" in w["paused_for"]
assert w["utc"] > json.loads((F / "USER_AUTHORIZATION_AND_PREPARATION.json").read_text())["UTC"]
before = run("rev-parse", "HEAD").decode().strip()
assert before == w["local_main_at_pause"] == w["remote_main_at_pause"]
assert run("ls-remote", "origin", "refs/heads/main").decode().split()[0] == before
roots = [str(F.relative_to(R)), str((A / "publication_package_v3").relative_to(R)), str((P / "CURRENT_PROGRESS.json").relative_to(R))]
captures = ["root_pr50_qualified_note_preparation_20261004_actual_capture", "root_pr50_qualified_note_zip_20261004_actual_capture",
    "root_pr50_qualified_note_pdf_20261004_actual_capture", "root_pr50_qualified_pdf_render_20261004_actual_capture", "root_pr50_qualified_kit_check_20261004_actual_capture"]
for name in captures:
    capture = C / name
    assert json.loads((capture / "CAPTURE.json").read_text())["status"] == "PASS"
    roots.append(str(capture.relative_to(R)))
selected = paths(run("diff", "--name-only", "-z", "--", *roots)) | paths(run("ls-files", "--others", "--exclude-standard", "-z", "--", *roots))
selected = {x for x in selected if not x.endswith(".log") and Path(x).name != J.name and not (x.startswith(str(F.relative_to(R)) + "/page-") and x.endswith(".png"))}
assert selected
foreign = {n: bind(n) for n in paths(run("diff", "--name-only", "-z")) - selected}
owned = {n: bind(n) for n in sorted(selected)}
assert all(not x.get("absent") for x in owned.values())
for n in selected:
    assert any(n == r or n.startswith(r + "/") for r in roots)
    assert "private" not in Path(n).parts
plan = F / "PREPARATION_CHECKPOINT_PLAN.json"
assert not plan.exists()
plan.write_text(json.dumps({"UTC": dt.datetime.now(dt.timezone.utc).isoformat(), "parent": before,
    "owned": owned, "foreign": foreign, "window": w, "publication_performed": False}, indent=2) + "\n")
pn = str(plan.relative_to(R)); selected.add(pn); owned[pn] = bind(pn)
run("add", "--", *sorted(selected))
assert paths(run("diff", "--cached", "--name-only", "-z")) == selected
for n, b in owned.items():
    assert bind(n) == b and hashlib.sha256(run("show", ":" + n)).hexdigest() == b["sha256"]
for n, b in foreign.items(): assert bind(n) == b
run("commit", "-m", "Prepare qualified PR50 note with incomplete priority disclosed")
after = run("rev-parse", "HEAD").decode().strip()
assert run("rev-list", "--parents", "-n", "1", after).decode().split() == [after, before]
assert paths(run("diff-tree", "--no-commit-id", "--name-only", "-r", "-z", after)) == selected
assert run("ls-remote", "origin", "refs/heads/main").decode().split()[0] == before
run("push", "origin", "main")
assert run("ls-remote", "origin", "refs/heads/main").decode().split()[0] == after
assert run("diff", "--cached", "--name-only", "-z") == b""
for n, b in foreign.items(): assert bind(n) == b
receipt = {"UTC": dt.datetime.now(dt.timezone.utc).isoformat(), "status": "PASS_SCOPED_PREPARATION_PUSH",
    "commit": after, "parent": before, "committed_paths": len(selected), "foreign_preserved": len(foreign),
    "index_empty": True, "publication_performed": False, "priority_clearance": False, "program_percent": 3.030303}
(F / "PREPARATION_CHECKPOINT_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
