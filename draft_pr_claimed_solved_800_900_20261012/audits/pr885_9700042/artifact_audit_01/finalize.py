"""Validate completed receipts and write an explicit publication-safe manifest.

Arguments: AUDIT_DIRECTORY SOURCE_DIRECTORY. No original files are changed.
The public allowlist below is explicit and never recursively expands a folder.
"""
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import hashlib
import json
import shutil
import stat
import sys

output, source = map(lambda x: Path(x).resolve(), sys.argv[1:])

def read(relative):
    return json.loads((output / relative).read_bytes())

def write(relative, value):
    (output / relative).write_text(json.dumps(value, indent=2, sort_keys=True)+"\n")

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

before, after = read("AUTHENTICATION_BEFORE.json"), read("AUTHENTICATION_AFTER.json")
require(before == after and after["pass"], "Original bytes or Git authentication changed")
direct, independent = read("DIRECT_ROOT_SUMMARY.json"), read("INDEPENDENT_SUMMARY.json")
require(len(direct) == 2 and all(r["returncode"] == 0 and r["all_passed"] and r["matches_frozen_replay_except_python_version"] for r in direct), "Direct roots did not reproduce")
require(independent["all_passed"] and independent["direct_checker_positive_runs"] == 20, "Independent checker suite incomplete")
checker = read("INDEPENDENT_CHECKER_REPLAYS.json")
require(len(checker) == 20 and all(r["returncode"] == 0 and r["matches_frozen_output_bytes"] and r["forced_assertion_rejected"] and r["checker_compilation_optimize"] == 0 for r in checker), "Direct checker assertions or outputs failed")
observed = read("observed_retry/ROOT_REPLAY_SUMMARY.json")
require(len(observed) == 2 and all(r["all_passed"] and r["returncode"] == 0 for r in observed), "Observed replay incomplete")
traces = []
for mode in ("baseline", "optimized"):
    trace = read("observed_retry/root_"+mode+"/TRACE.json")
    events = trace["events"]
    successful = [e for e in events if e["kind"] == "positive" and e["returncode"] == 0]
    corrupt = [e for e in events if e["kind"] == "positive" and e["returncode"] != 0]
    forced = [e for e in events if e["kind"] == "negative"]
    patches = [e for e in events if e["kind"] == "patch"]
    require((len(events),len(successful),len(corrupt),len(forced),len(patches)) == (64,20,20,20,4), "Unexpected actual nested subprocess count")
    require(all("Checker hash mismatch before execution" in e["stderr_text_normalized"] for e in corrupt), "Corruption rejection did not precede checker execution")
    require(all(e["returncode"] != 0 and "NEGATIVE_CONTROL_ASSERTION" in e["stderr_text_normalized"] for e in forced), "Forced assertion failed to reject")
    require([e["python_requested_flags"] for e in successful] == [m for _ in range(5) for m in ([],["-O"],["-I"],["-I","-O"])], "Unexpected actual nested flag order")
    traces.append({"root_mode": mode, "actual_nested_subprocess_calls":len(events), "successful_checkers":len(successful), "forced_assertion_rejections":len(forced), "corrupt_checker_preexecution_rejections":len(corrupt), "patch_calls":len(patches), "root_effective_flags":trace["root_effective_flags"]})

incidents = []
for relative, description in (("initial_direct_root_baseline_failure", "First direct baseline: patch-result equality failed during concurrent ENOSPC; clean unchanged-script retry passed."), ("initial_direct_root_optimized_failure", "First direct optimized: patch-result equality failed during concurrent ENOSPC; clean unchanged-script retry passed."), ("root_optimized", "First observed optimized: confirmed ENOSPC while retaining child stderr; clean retry passed.")):
    folder = output / relative
    stderr = (folder / "ROOT_STDERR.private").read_bytes()
    stdout = (folder / "ROOT_STDOUT.json").read_bytes()
    text = stderr.decode(errors="replace").replace(str(source), "<original-packet>").replace(str(output), "<audit-root>")
    incidents.append({"attempt_role": relative, "description":description, "stdout_actual_bytes":len(stdout), "stdout_actual_sha256":sha(stdout), "stderr_actual_bytes":len(stderr), "stderr_actual_sha256":sha(stderr), "stderr_text_normalized":text})
write("ENVIRONMENT_INCIDENTS.json", {"incidents":incidents, "additional_interruption": "Initial independent suite executed its first positive checker and forced failure but receipt writing raised ENOSPC; its complete clean retry passed. Some retry helper setup calls failed before launching roots while mkdir/rename was unavailable. Raw terminal tool receipts exist in the audit conversation.", "attribution": "Observed ENOSPC is direct evidence. Attribution of concurrent initial direct patch mismatches to that resource condition is an inference, supported by unchanged-source clean retries."})

# Remove only now-empty own scratch directories, never retained receipts.
for relative in ("root_baseline/scratch", "root_optimized/scratch", "observed_retry/root_baseline/scratch", "observed_retry/root_optimized/scratch", "independent_scratch"):
    folder = output / relative
    if folder.exists():
        require(not any(folder.iterdir()), "Nonempty scratch directory requires review")
        folder.rmdir()

result = {"verdict":"PASS", "scope":"Authenticity and finite artifact reproduction only; theorem truth, external mathematical premises, novelty, priority, and mathematical acceptance are separate.", "head":after["head"], "original_file_count":30, "original_total_bytes":214980, "original_effort":"5/5", "external_manifest_sha256":after["external_manifest_sha256"], "originals_unchanged":before == after, "direct_original_root_successful_invocations":2, "observed_successful_invocations_in_final_pair":2, "observed_actual_nested_counts":traces, "independent_suite":independent, "accepted_format_boundaries": [r["case"] for r in read("FORMAT_CONTROLS.json")["controls"] if r["accepted"] and r["case"] != "unchanged"], "mathematical_claim_accepted_by_this_audit":False, "priority_claim_accepted_by_this_audit":False, "completion_estimate_percent":100, "completed_utc":datetime.now(timezone.utc).isoformat()}
write("DECISION.json", result)

PUBLIC = [
    "SOURCE_CONTRACT.md", "RESEARCH_LOG.md", "REPORT.md", "DECISION.json",
    "authenticate.py", "observe_root.py", "run_roots.py", "direct_roots.py", "independent_checks.py", "finalize.py",
    "AUTHENTICATION_BEFORE.json", "AUTHENTICATION_INTERIM.json", "AUTHENTICATION_AFTER.json",
    "MANIFEST_SEMANTICS.json", "FORMAT_CONTROLS.json", "INDEPENDENT_PATCH_REPLAYS.json",
    "INDEPENDENT_CHECKER_REPLAYS.json", "NESTED_FLAG_PREFIX_PROBES.json", "INDEPENDENT_SUMMARY.json",
    "DIRECT_ROOT_SUMMARY.json", "ENVIRONMENT_INCIDENTS.json",
    "direct_root_baseline/ROOT_STDOUT.json", "direct_root_baseline/RECEIPT.json",
    "direct_root_optimized/ROOT_STDOUT.json", "direct_root_optimized/RECEIPT.json",
    "root_baseline/ROOT_STDOUT.json", "root_baseline/TRACE.json",
    "observed_retry/ROOT_REPLAY_SUMMARY.json",
    "observed_retry/root_baseline/ROOT_STDOUT.json", "observed_retry/root_baseline/TRACE.json",
    "observed_retry/root_optimized/ROOT_STDOUT.json", "observed_retry/root_optimized/TRACE.json",
]
inventory = []
for relative in PUBLIC:
    rel = PurePosixPath(relative)
    require(not rel.is_absolute() and ".." not in rel.parts and relative == rel.as_posix(), "Unsafe public relative path")
    path = output / relative
    require(stat.S_ISREG(path.lstat().st_mode) and not path.is_symlink(), "Public entry is not a regular authored file")
    data = path.read_bytes()
    private_markers = (b"/"+b"Users"+b"/", b"/"+b"private"+b"/"+b"var"+b"/", b"/"+b"var"+b"/"+b"folders"+b"/")
    require(not any(marker in data for marker in private_markers), "Private absolute path leaked into public artifact: "+relative)
    inventory.append({"path":relative,"bytes":len(data),"sha256":sha(data)})
write("PUBLIC_MANIFEST.json", {"scope":"Explicit authored safe files only; this manifest excludes itself to avoid self-reference. No recursive allowance; no original corpus copy, source PDF/HTML, renders, credentials, or private raw process files.", "files":inventory})
print(json.dumps({"verdict":"PASS","public_files":len(inventory),"original_files_unchanged":30,"original_bytes_unchanged":214980,"original_effort":"5/5"},sort_keys=True))
