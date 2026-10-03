"""Post-seal frozen-byte, historical-manifest, and private replay audit."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent
SNAPSHOT = AUDIT / "snapshot"
ATTEMPT = SNAPSHOT / "unsolved_math_prioritization/attempts/2302055"
PYTHON = Path("/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python")

def digest(data):
    return hashlib.sha256(data).hexdigest()

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def run_copy(script, args=(), expected=None):
    rec = {"script": str(script.relative_to(PRIVATE)), "started_utc": now(),
           "interpreter": str(PYTHON), "script_sha256": digest(script.read_bytes())}
    proc = subprocess.run([str(PYTHON), str(script), *map(str, args)], cwd=PRIVATE,
                          capture_output=True, timeout=120)
    stem = script.stem
    (PRIVATE / (stem + ".stdout.bin")).write_bytes(proc.stdout)
    (PRIVATE / (stem + ".stderr.bin")).write_bytes(proc.stderr)
    rec.update(exit_code=proc.returncode, stdout_bytes=len(proc.stdout),
               stdout_sha256=digest(proc.stdout), stderr_bytes=len(proc.stderr),
               stderr_sha256=digest(proc.stderr), finished_utc=now())
    if expected is not None:
        ref = expected.read_bytes()
        rec.update(expected_path=str(expected.relative_to(ATTEMPT)), expected_sha256=digest(ref),
                   complete_stdout_byte_identical=proc.stdout == ref)
    try:
        rec["parsed_output"] = json.loads(proc.stdout)
    except Exception as exc:
        rec["parse_failure"] = str(exc)
    return rec

if __name__ == "__main__":
    assert (ROOT / "MATHEMATICAL_SEAL.json").exists(), "Mathematical seal required first"
    frozen = json.loads((AUDIT / "snapshot_manifest.json").read_text())
    binding = []
    for row in frozen["files"]:
        data = (SNAPSHOT / row["path"]).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        binding.append({"path": row["path"], "bytes_match": len(data) == row["bytes"],
                        "sha256_match": digest(data) == row["sha256"],
                        "git_blob_sha_match": blob == row["git_blob_sha"]})
    manifests = []
    for file in sorted(ATTEMPT.rglob("*MANIFEST.json")):
        obj = json.loads(file.read_text())
        if not isinstance(obj.get("files"), list):
            continue
        rows = []
        for row in obj["files"]:
            actual = file.parent / row["path"]
            data = actual.read_bytes()
            rows.append({"path": row["path"], "exists": True,
                         "sha256_match": digest(data) == row["sha256"],
                         "bytes_match": "bytes" not in row or len(data) == row["bytes"]})
        listed = {str((file.parent / x["path"]).relative_to(ATTEMPT)) for x in obj["files"]}
        target_files = {str(x.relative_to(ATTEMPT)) for x in ATTEMPT.rglob("*") if x.is_file()}
        manifests.append({"manifest": str(file.relative_to(ATTEMPT)), "listed_files": len(rows),
                          "self_excluded": str(file.relative_to(ATTEMPT)) not in listed,
                          "exact_all_other_target_files": listed == target_files - {str(file.relative_to(ATTEMPT))},
                          "checks": rows})
    PRIVATE = ROOT / "private_replay"
    PRIVATE.mkdir(exist_ok=True)
    copied = PRIVATE / "frozen"
    shutil.copytree(ATTEMPT, copied, dirs_exist_ok=True)
    runs = [run_copy(copied / f"verify_turn{i}.py", expected=ATTEMPT / f"TURN_{i}_CHECKS.json")
            for i in range(1, 6)]
    runs.append(run_copy(copied / "review/independent_check.py", expected=ATTEMPT / "review/INDEPENDENT_CHECKS.json"))
    runs.append(run_copy(copied / "review/replay_author.py", args=[copied], expected=ATTEMPT / "review/AUTHOR_REPLAY.json"))
    versions = subprocess.run([str(PYTHON), "-c", "import sys,sympy,json;print(json.dumps({'python':sys.version,'sympy':sympy.__version__}))"],
                              capture_output=True, text=True, check=True)
    report = {"generated_utc": now(), "head": frozen["head"], "base": frozen["base"],
              "snapshot_files": len(binding), "target_files": len([x for x in ATTEMPT.rglob('*') if x.is_file()]),
              "read_coverage": [{"path": str(x.relative_to(ATTEMPT)), "sha256": digest(x.read_bytes()),
                                 "phase": "mathematics first; remaining claim and code content only after mathematical seal"}
                                for x in sorted(ATTEMPT.rglob('*')) if x.is_file()],
              "snapshot_checks": binding, "manifest_checks": manifests,
              "environment": json.loads(versions.stdout), "replays": runs,
              "author_assertion_total": sum(x['parsed_output']['exact_assertions'] for x in runs[:5]),
              "prior_review_assertion_total": runs[5].get('parsed_output', {}).get('independent_assertions'),
              "analytic_proofs_certified_by_computation": False}
    (ROOT / "FROZEN_BINDING_AND_REPLAY.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"snapshot_files": report['snapshot_files'], "target_files": report['target_files'],
                      "snapshot_all_match": all(all(r[k] for k in ('bytes_match','sha256_match','git_blob_sha_match')) for r in binding),
                      "manifests": [{"manifest": x['manifest'], "listed_files": x['listed_files'],
                                     "all_match": all(r['sha256_match'] and r['bytes_match'] for r in x['checks']),
                                     "self_excluded": x['self_excluded'], "exact_all_other_target_files": x['exact_all_other_target_files']} for x in manifests],
                      "runs": [{"script": x['script'], "exit_code": x['exit_code'], "byte_identical": x.get('complete_stdout_byte_identical')} for x in runs],
                      "author_assertions": report['author_assertion_total'], "prior_review_assertions": report['prior_review_assertion_total']} , indent=2))
