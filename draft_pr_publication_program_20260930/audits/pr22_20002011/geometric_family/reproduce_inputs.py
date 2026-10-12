#!/usr/bin/env python3
"""Check exact Git/snapshot bindings and replay stored scripts in ignored copies."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import datetime
import hashlib
import json
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[2]
SNAPSHOT = AUDIT / "source_snapshot"
META = json.loads((AUDIT / "snapshot_manifest.json").read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


bindings = []
for f in META["files"]:
    p = SNAPSHOT / f["path"]
    content = p.read_bytes()
    gitpath = "unsolved_math_prioritization/attempts/20002011/" + f["path"]
    g = subprocess.run(["git", "show", META["head"] + ":" + gitpath], cwd=ROOT,
                       check=True, capture_output=True).stdout
    blob = subprocess.run(["git", "rev-parse", META["head"] + ":" + gitpath], cwd=ROOT,
                          check=True, capture_output=True, text=True).stdout.strip()
    assert content == g and sha(content) == f["sha256"] and len(content) == f["bytes"]
    assert blob == f["git_blob"]
    bindings.append({"path": f["path"], "bytes": len(content), "sha256": sha(content),
                     "git_blob": blob, "git_head_and_snapshot_identical": True})


def replay(name, script, output):
    dest = HERE / "tmp" / name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(SNAPSHOT, dest)
    cp = subprocess.run(["/usr/bin/python3", str(dest / script)], cwd=dest,
                        check=True, capture_output=True, text=True, timeout=180)
    result = (dest / output).read_bytes()
    original = (SNAPSHOT / output).read_bytes()
    assert result == original, output + " differs"
    parsed = json.loads(result)
    return {"script": script, "script_sha256": sha((SNAPSHOT / script).read_bytes()),
            "output": output, "output_sha256": sha(result),
            "output_byte_identical": True, "assertions": parsed.get("passed", parsed.get("assertions")),
            "sympy_version": parsed["sympy_version"], "interpreter": "/usr/bin/python3",
            "interpreter_version": subprocess.run(["/usr/bin/python3", "--version"],
                                                   check=True, capture_output=True, text=True).stdout.strip(),
            "exit_code": cp.returncode, "stdout_json_matches_output": json.loads(cp.stdout) == parsed}


with ThreadPoolExecutor(max_workers=2) as ex:
    jobs = [ex.submit(replay, "author_replay", "check_jets.py", "check_results.json"),
            ex.submit(replay, "reviewer_replay", "independent_review/independent_checks.py",
                      "independent_review/independent_results.json")]
    replays = [j.result() for j in jobs]

for f in META["files"]:
    assert sha((SNAPSHOT / f["path"]).read_bytes()) == f["sha256"]

provenance = json.loads((SNAPSHOT / "provenance.json").read_text())
review = json.loads((SNAPSHOT / "independent_review/review_summary.json").read_text())
assert provenance["source_status_sha256"] == sha((SNAPSHOT / "SOURCE_STATUS.md").read_bytes())
assert review["reviewed_sha256"] == provenance["source_status_sha256"]
assert review["review_sha256"] == sha((SNAPSHOT / "independent_review/REVIEW.md").read_bytes())
assert json.loads((SNAPSHOT / "turns.json").read_text())["used"] == 1

result = {
    "checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "pr": 22, "head": META["head"], "status": "PASS_EXACT_BINDING_AND_BYTE_REPRODUCTION",
    "frozen_files": bindings, "frozen_files_checked": len(bindings), "replays": replays,
    "snapshot_unmodified": True, "original_substantive_attempts": 1,
    "new_original_attempt": False,
    "provenance_finding": {"priority": 3, "path": "provenance.json",
        "field": "shared_queue_modified", "frozen_value": provenance["shared_queue_modified"],
        "verified_changed_paths_include_queue": "unsolved_math_prioritization/QUEUE.md" in META["changed_paths"],
        "required_current_annotation": "The original PR modifies QUEUE.md as well as its numeric attempt folder; preserve original metadata but correct the current scope record."}
}
(HERE / "INPUT_BINDING_AND_REPRODUCTION.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "frozen_files_checked": len(bindings),
                  "replays": replays, "provenance_finding": result["provenance_finding"]}, indent=2))
