"""Independently verify parser repairs without network calls or shared writes."""
import datetime
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PROGRAM = HERE.parents[1]
spec = importlib.util.spec_from_file_location("reviewed_intake", PROGRAM / "intake.py")
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)

def rejected(text):
    try:
        intake.queue_rows(text)
    except ValueError:
        return True
    return False

inv = json.loads((PROGRAM / "inventory.json").read_text())
main_rows = intake.queue_rows((PROGRAM / "queue_remote_main.md").read_text())
local_rows = intake.queue_rows((PROGRAM.parent / "unsolved_math_prioritization/QUEUE.md").read_text())
assert len(main_rows) == len(local_rows) == 1951
assert all(main_rows[p["problem_id"]]["status"] == local_rows[p["problem_id"]]["status"]
           == p["queue_status"] == "queued" for p in inv["prs"])
assert all(main_rows[p["problem_id"]]["canonical_width"] and
           local_rows[p["problem_id"]]["canonical_width"] for p in inv["prs"])
first = json.loads((HERE / "parser_edge_case.json").read_text())["row"]
second = json.loads((HERE / "parser_second_edge_case.json").read_text())["synthetic_row"]
assert rejected(first), "First shifted-cell spoof remains accepted"
assert rejected(second), "Second shifted-cell spoof remains accepted"
escaped = r"| 1 | 123 / TEST | Text \| claimed_solved \| 0/5 | 0.1 | 5.5 | 3 | unknown | queued | 0/5 | | | |"
assert intake.queue_rows(escaped)["123"]["status"] == "queued"
ordinary = "| 1 | 123 / TEST | Text | 0.1 | 5.5 | 3 | unknown | claimed_solved | 1/5 | | | |"
assert intake.queue_rows(ordinary)["123"]["status"] == "claimed_solved"
assert rejected(ordinary + "\n" + ordinary), "Duplicate problem IDs must be rejected"
forged = "| 1 | 123 / TEST | Text | 0.1 | 5.5 | 3 | unknown | claimed_solved | 0/5 | 0.1 | 5.5 | 3 | unknown | queued | 0/5 | | | |"
assert not intake.queue_rows(forged)["123"]["canonical_width"]
# Exercise the actual disposition gate with mocked read-only API responses.
# All incidental fixture outputs are isolated in this review's temporary folder.
with tempfile.TemporaryDirectory(dir=HERE) as tmp:
    intake.ROOT = Path(tmp)
    def fixture_gh(*args):
        if args[0] == "pr":
            return [{"number": 1000, "state": "OPEN", "isDraft": True,
                     "title": "123 fixture", "headRefName": "fixture-123",
                     "headRefOid": "1" * 40, "baseRefName": "main", "url": "fixture"}]
        if "commits/main" in args[1]:
            return {"sha": "0" * 40}
        return {"sha": "2" * 40, "content": base64.b64encode(forged.encode()).decode()}
    intake.gh = fixture_gh
    try:
        intake.main()
    except ValueError as exc:
        assert "Ambiguous table delimiters" in str(exc)
    else:
        raise AssertionError("Actual main gate accepted a forged full-schema prefix")
    assert not (Path(tmp) / "inventory.json").exists()
for status in ("queued", "already_solved", "unsolved", "claimed_solved_extra", "partial"):
    text = ordinary.replace("| claimed_solved |", f"| {status} |")
    assert intake.queue_rows(text)["123"]["status"] != "claimed_solved"
out = {"captured_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "intake_source_sha256": hashlib.sha256((PROGRAM / "intake.py").read_bytes()).hexdigest(),
       "full_main_and_local_row_counts": [len(main_rows), len(local_rows)],
       "target_101_statuses_unchanged": True, "both_shifted_cell_spoofs_rejected": True,
       "escaped_title_status_preserved": True, "ordinary_claimed_solved_recognized": True,
       "duplicate_identity_rejected": True, "other_statuses_not_eligible": True,
       "all_target_rows_have_canonical_width": True,
       "actual_main_gate_refuses_full_schema_forged_prefix": True,
       "mathematical_review_performed": False}
(HERE / "repaired_parser_independent_verification.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
