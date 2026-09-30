#!/usr/bin/env python3
"""Reproduce PR #9's lost status/turn count without touching the live queue.

Uses the immutable Git object named below, the repository's cached source
record, and a one-record temporary database. All rank outputs stay under this
review's ignored tmp directory. No network calls or live queue writes occur.
"""
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import tempfile

HEAD = "a29887ed0e341851d02fa992c26500d4089267be"
TARGET = "30005473"
REVIEW = Path(__file__).resolve().parent
REPOSITORY = REVIEW.parent


def at_head(name):
    return subprocess.check_output(
        ["git", "show", f"{HEAD}:unsolved_math_prioritization/{name}"],
        cwd=REPOSITORY,
        text=True,
    )


def main():
    queue_code = at_head("queue.py")
    policy = json.loads(at_head("policy.json"))
    states = json.loads(at_head("state.json"))
    assessments = json.loads(at_head("assessments.json"))
    manifest = json.loads(at_head("manifest.json"))
    catalog = json.loads(at_head("catalog.json"))
    original_catalog_row = next(row for row in catalog if row["id"] == TARGET)
    pr_queue = at_head("QUEUE.md")
    before = next(line for line in pr_queue.splitlines() if f"{TARGET} /" in line)
    assert "| claimed_solved | 1/5 |" in before
    assert TARGET not in states

    cache = REPOSITORY / "unsolved_math_prioritization/cache/catalog.sqlite"
    with sqlite3.connect(f"file:{cache}?mode=ro", uri=True) as db:
        raw, report = db.execute(
            "SELECT payload, report FROM records WHERE key=?", (TARGET,)
        ).fetchone()
    problem = json.loads(raw)
    prior_report = json.loads(report)
    assert problem["id"] == int(TARGET)

    scratch = REVIEW / "tmp"
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="queue-reproduction-", dir=scratch) as tmp:
        sandbox = Path(tmp)
        module_path = sandbox / "queue.py"
        module_path.write_text(queue_code)
        spec = importlib.util.spec_from_file_location("pr9_queue_snapshot", module_path)
        queue = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(queue)
        assert queue.ROOT == sandbox
        assert queue.digest(json.dumps([problem, prior_report], sort_keys=True)) == assessments[TARGET]["review_hash"]

        inputs = {
            "policy.json": policy,
            "state.json": states,
            "assessments.json": {TARGET: assessments[TARGET]},
            "manifest.json": {**manifest, "records": 1},
            "catalog.json": [row for row in catalog if row["id"] == TARGET],
        }
        for name, value in inputs.items():
            (sandbox / name).write_text(json.dumps(value))
        (sandbox / "QUEUE.md").write_text(pr_queue)
        with queue.connect() as db:
            db.execute("INSERT INTO records VALUES (?, ?, ?)", (TARGET, raw, report))
            db.execute("CREATE TABLE metadata (revision TEXT)")
            db.execute("INSERT INTO metadata VALUES (?)", (manifest["revision"],))
        out = io.StringIO()
        with redirect_stdout(out):
            queue.rank(None)
        after_catalog = json.loads((sandbox / "catalog.json").read_text())
        row = next(item for item in after_catalog if item["id"] == TARGET)
        after = next(
            line for line in (sandbox / "QUEUE.md").read_text().splitlines()
            if f"{TARGET} /" in line
        )
        assert row["local_status"] == "queued"
        assert row["turns_used"] == 0
        assert row["eligible"] is True
        assert "| queued | 0/5 |" in after
        assert "claimed_solved" not in queue.STATES
        evidence = {
            "head": HEAD,
            "target": TARGET,
            "method": "Actual PR-head rank() on one-record source-hash-verified isolated database",
            "before_queue_row": before,
            "state_entry_exists": TARGET in states,
            "claimed_solved_is_supported_state": "claimed_solved" in queue.STATES,
            "rank_stdout": out.getvalue().strip(),
            "after_queue_row": after,
            "after_local_status": row["local_status"],
            "after_turns_used": row["turns_used"],
            "after_eligible": row["eligible"],
            "before_catalog_status": original_catalog_row["local_status"],
            "before_catalog_turns_used": original_catalog_row["turns_used"],
            "before_catalog_eligible": original_catalog_row["eligible"],
            "conclusion": "The old generator reverts the manually maintained displayed row to queued 0/5. The source catalog was already eligible with that state. This is a documented inherited generator incompatibility; the PR also preserves a committed local turn ledger.",
        }
    (REVIEW / "queue_reproduction.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
