"""Scoped ordinary audit checkpoint; no PR, publication or tracker mutations."""
import datetime, hashlib, json, os, pathlib, subprocess

HERE = pathlib.Path(__file__).resolve().parent
PROGRAM = HERE.parent.parent
CHECKOUT = PROGRAM.parent
BASE = "4dc84dd2d950d5d60233d742034fd3b9f8fde335"
GIT = "/opt/homebrew/Cellar/git/2.38.2/bin/git"
RECEIPT = HERE / "MATH_AUDIT_CHECKPOINT_ACTUAL_RECEIPT_20261006.json"
events = []

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def run(args):
    child = subprocess.run([GIT, *args], cwd=CHECKOUT, capture_output=True)
    events.append({"UTC": utc(), "argv": [GIT, *args], "returncode": child.returncode,
                   "stdout": child.stdout.decode("utf-8", "replace"),
                   "stderr": child.stderr.decode("utf-8", "replace")})
    if child.returncode:
        raise RuntimeError("Git action failed; inspect actual receipt before retry")
    return child.stdout

def require(value, reason):
    if not value:
        raise RuntimeError(reason)

def write(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

try:
    require(not RECEIPT.exists(), "Existing actual receipt: do not repeat action")
    require(run(["branch", "--show-current"]).strip() == b"main", "Not main")
    require(run(["rev-parse", "HEAD"]).decode().strip() == BASE, "Base changed")
    require(not run(["diff", "--cached", "--name-only"]).strip(), "Index not empty")
    require(run(["ls-remote", "origin", "refs/heads/main"]).decode().split()[0] == BASE,
            "Remote writer/base changed")

    initial = HERE / "root_priority_audit_20261006/INITIAL_FINDINGS.md"
    body = initial.read_text()
    body = body.replace("This is an explicit verification specialization of the already published framework, not a new problem-search mechanism.",
        "This is an explicit reviewer verification specialization of the classical product framework, not an authenticated quotation of a previously published Eden disproof. The downloaded author copy is undated. The dated 2008 publisher record establishes the cascade paper's bibliographic existence, but its full published body was not recovered; the exact identity, numbering and date of the author-copy examples are not authenticated from that record.")
    initial.write_text(body)
    progress_path = PROGRAM / "CURRENT_PROGRESS.json"
    progress = json.loads(progress_path.read_text())
    progress["updated_UTC"] = utc()
    progress["main_writer_owner_at_snapshot"] = "This chat: exclusive short ordinary audit checkpoint; other chat explicitly released checkpoint046. Release pending actual commit/push/readback."
    progress["next_step"] = "Finish PR111 priority adjudication. Ordinary mathematical-audit checkpoint is in progress; no PR/publication action authorized by this checkpoint."
    progress["current_priority_threat"] = "Classical product/irrational-torus specialization defeats the broad manifold-inclusive imported target; no identical prior entire-R5 theorem authenticated. Stronger contribution and original-open-problem claim under final adjudication."
    write(progress_path, progress)

    allowed_dirs = ["original_head_authentication_20261006", "actual_original_head_authentication_20261006",
        "global_flow_attractor_adversary_20261006", "lyapunov_dimension_adversary_20261006",
        "primary_source_scope_adversary_20261006", "repaired_diagnostics_v1", "repaired_diagnostics_v2",
        "root_math_reproduction_20261006_dimension", "root_math_reproduction_20261006_flow",
        "root_math_reproduction_20261006_scope", "root_original_reproduction_20261006", "root_priority_audit_20261006"]
    private_parts = {"tmp", "pdfs", "private_sources", "private_primary_sources", "__pycache__"}
    def public_file(path):
        return (path.is_file() and not path.is_symlink() and not private_parts.intersection(path.parts)
                and (path.suffix in {".json", ".md", ".py", ".log"}
                     or path.name in {".gitignore", "SHA256SUMS"}))
    selected = {p for p in HERE.iterdir() if public_file(p) and p != RECEIPT}
    for name in allowed_dirs:
        selected.update(p for p in (HERE / name).rglob("*") if public_file(p))
    selected.update(p for p in (PROGRAM / "ordered_intake_20261006/after_PR110").iterdir() if public_file(p))
    previous = PROGRAM / "audits/pr110_5100032"
    selected.update(previous / name for name in ["RESEARCH_LOG.md", "FINAL_COMPLETION_OWNER_RELEASE_20261006.json",
        "publication_build_v1/final_readback_and_prepare_release.py", "root_final_readback_20261006/PROCESS_JOURNAL.json",
        "root_final_readback_20261006/PROCESS_LAUNCHES.json"])
    selected.update([progress_path, PROGRAM / "RESEARCH_LOG.md"])
    for path in selected:
        require(public_file(path), "Selected file missing/private/symlink: " + str(path))
        require(path.is_relative_to(CHECKOUT), "Path escapes checkout")
    members = [{"path": str(path.relative_to(CHECKOUT)), "bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in sorted(selected)]
    manifest_path = HERE / "MATH_AUDIT_CHECKPOINT_SELECTION_20261006.json"
    write(manifest_path, {"schema": "pr111-math-audit-scoped-checkpoint/v1", "UTC": utc(), "base": BASE,
        "members": members, "mathematical_gate": "PASS", "priority_disposition": "pending",
        "workflow_estimate_percent": 40, "program_completed": 18, "dated_eligible_total": 99,
        "program_estimate_percent": 18 / 99 * 100, "private_source_bodies_included": False,
        "PR_or_publication_mutation": False, "selection_manifest_self_excluded": True})
    selected.add(manifest_path)
    pins = {str(path.relative_to(CHECKOUT)): path.read_bytes() for path in selected}
    run(["add", "--", *sorted(pins)])
    staged = set(run(["diff", "--cached", "--name-only", "-z"]).decode().split("\0")) - {""}
    require(staged <= set(pins) and len(staged) > 100, "Unexpected staged scope/count")
    require(not run(["diff", "--cached", "--diff-filter=D", "--name-only"]).strip(), "Deletion staged")
    for path in staged:
        require(run(["show", ":" + path]) == pins[path], "Staged bytes changed: " + path)
    run(["commit", "-m", "Audit PR111 mathematics and preserve PR110 final release receipts"])
    commit = run(["rev-parse", "HEAD"]).decode().strip()
    require(run(["rev-parse", "HEAD^"]).decode().strip() == BASE, "Wrong commit parent")
    changed = set(run(["diff-tree", "--no-commit-id", "--name-only", "-r", "-z", commit]).decode().split("\0")) - {""}
    require(changed == staged, "Unexpected commit paths")
    for path in staged:
        require(run(["show", commit + ":" + path]) == pins[path], "Committed body mismatch")
    run(["push", "origin", "HEAD:refs/heads/main"])
    require(run(["ls-remote", "origin", "refs/heads/main"]).decode().split()[0] == commit,
            "Remote post-push mismatch")
    run(["fetch", "--no-tags", "--no-write-fetch-head", "origin", "refs/heads/main"])
    require(run(["rev-parse", "origin/main"]).decode().strip() == commit, "Fetched main mismatch")
    for path in staged:
        require(run(["show", "origin/main:" + path]) == pins[path], "Remote fetched body mismatch")
    require(not run(["diff", "--cached", "--name-only"]).strip(), "Index not empty after commit")
    receipt = {"schema": "pr111-math-checkpoint-actual-receipt/v1", "UTC": utc(), "PID": os.getpid(),
        "base": BASE, "commit": commit, "selected_count": len(pins), "changed_count": len(staged),
        "full_selected_changed_bodies_verified": True, "nonforce_push_actual_success": True,
        "fetched_remote_main_verified": True, "writer_release_pending": True,
        "PR111_disposition": "pending", "program_completed": 18, "program_estimate_percent": 18 / 99 * 100,
        "persistent_goal_status": "active", "events": events}
    write(RECEIPT, receipt)
    print(json.dumps({k: v for k, v in receipt.items() if k != "events"}, sort_keys=True))
except BaseException as exc:
    write(RECEIPT, {"UTC": utc(), "PID": os.getpid(), "stopped": True, "error": str(exc), "events": events})
    raise
