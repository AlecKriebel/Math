"""Read-only root authentication and reproduction of frozen priority audits."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
A = Path(__file__).resolve().parent
PY = "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14"
def require(value, label):
    if not value: raise ValueError(label)
def pin(path):
    require(path.is_file() and not path.is_symlink(), str(path))
    body = path.read_bytes()
    return {"path": str(path.relative_to(A)), "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}
manifests = {
    "historical_priority_adversary_20261006": "8b1d7fbd3a0689f8a948fbf57b97290345d67dd7c0ce18cd4cc92c0a22fb4a63",
    "modern_citation_priority_adversary_20261006": "01e700d352ef44dd9ef53c20d95abee9c8de14ec88428dd7673bab23e9cdc7d5",
    "quasiperiodic_counterexample_priority_20261006": "4200a96d2f8a9e50609ad73baa09a479ff90f2b2f6474c722ddd0e519fb40431",
    "priority_cross_family_adjudicator_20261006": "ea914ad7b005abb65fe981da1a8a70116ca6fe99e10ef013070706a7ad982941",
}
families = []
for name, expected in manifests.items():
    base = A / name
    meta = pin(base / "OUTPUT_MANIFEST.json")
    require(meta["sha256"] == expected, "Manifest pin " + name)
    manifest = json.loads((base / "OUTPUT_MANIFEST.json").read_text())
    members, seen = [], set()
    for entry in manifest["members"]:
        path = entry["path"]
        require(path not in seen and Path(path).name == path and path not in {".", ".."}, "Flat unique public member")
        seen.add(path)
        actual = pin(base / path)
        require(actual["bytes"] == entry["bytes"] and actual["sha256"] == entry["sha256"], "Member mismatch " + path)
        members.append(actual)
    families.append({"manifest": meta, "members": members})
replays = []
code = A / "priority_cross_family_adjudicator_20261006/verify_adjudication.py"
for optimized in (False, True):
    argv = [PY, "-E", "-S", "-B", "-P"] + (["-O"] if optimized else []) + [str(code)]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    child = subprocess.Popen(argv, cwd=A, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={"PATH":"/usr/bin:/bin", "LC_ALL":"C", "LANG":"C", "TZ":"UTC", "__CF_USER_TEXT_ENCODING":"0x1F5:0x0:0x0"})
    out, err = child.communicate()
    require(child.returncode == 0 and not err, "Actual replay failed")
    result = json.loads(out)
    require(result["status"] == "PASS" and result["explicit_guards"] == 206
            and result["total_family_members_authenticated"] == 45 and not result["priority_clearance"], "Replay result")
    replays.append({"argv": argv, "PID": child.pid, "started_UTC": started,
        "ended_UTC": datetime.datetime.now(datetime.timezone.utc).isoformat(), "exit_code": child.returncode,
        "stdout_sha256": hashlib.sha256(out).hexdigest(), "stderr_bytes": len(err), "result": result})
original = json.loads((A / "original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json").read_text())
for entry in original["all_original_files"]:
    actual = pin(A / "original_head_authentication_20261006/original_attempt" / entry["path"])
    require(actual["bytes"] == entry["bytes"] and actual["sha256"] == entry["sha256"], "Original changed")
v2 = pin(A / "repaired_diagnostics_v2/COUNTEREXAMPLE.md")
require(v2["sha256"] == "0e2e4e1484193c304cb2394142e24460c89a50f6ab3bb58ad838624cabb9035f", "v2 changed")
record = {"schema": "pr111-root-final-priority-family-authentication/v1",
    "UTC": datetime.datetime.now(datetime.timezone.utc).isoformat(), "actual_operator_PID": os.getpid(),
    "families": families, "portable_member_count": sum(len(x["members"]) for x in families), "replays": replays,
    "all_original_files_unchanged": True, "v2": v2, "mathematical_gate_remains_PASS": True,
    "original_genuinely_open_target_established": False, "full_strengthened_theorem_exact_prior_authenticated": False,
    "novelty_clearance": False, "proposed_closure": pin(A / "PROPOSED_CLOSURE_COMMENT_20261006.md"),
    "root_scope_reasoning": pin(A / "ROOT_PRIORITY_DISPOSITION_20261006.md"),
    "new_central_proof_search_turns": 0, "bounded_priority_audit_percent": 100, "PR_workflow_estimate_percent": 75,
    "program_completed": 18, "program_estimate_percent": 18/99*100, "persistent_goal_status": "active",
    "fresh_disposition_review_pending": True, "native_or_external_mutations": False}
(A / "ROOT_PRIORITY_FAMILY_AUTHENTICATION_20261006.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
print(json.dumps({k:v for k,v in record.items() if k not in {"families", "replays"}},sort_keys=True))
