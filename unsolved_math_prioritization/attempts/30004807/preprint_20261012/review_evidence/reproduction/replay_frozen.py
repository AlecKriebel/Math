#!/usr/bin/env python3
"""Replay immutable historical programs in private copies; bind all outputs."""
from pathlib import Path
import ast, hashlib, json, platform, shutil, subprocess, sys

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
SNAPSHOT = AUDIT / "source_snapshot"
SOURCE = SNAPSHOT / "unsolved_math_prioritization/attempts/30004807"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def require(condition, name):
    if not condition:
        raise RuntimeError(name)

receipt = json.loads((AUDIT / "SOURCE_RECEIPT.json").read_text())
bound = []
for item in receipt["files"]:
    path = SNAPSHOT / item["path"]
    data = path.read_bytes()
    require(len(data) == item["bytes"] and sha(data) == item["sha256"], item["path"])
    bound.append({**item, "verified": True})

refs = []
frozen = json.loads((SOURCE / "audit/FROZEN_INPUTS.json").read_text())
for item in frozen["files"]:
    data = (SOURCE / "release" / item["path"]).read_bytes()
    require(len(data) == item["bytes"] and sha(data) == item["sha256"], item["path"])
    refs.append({"manifest": "audit/FROZEN_INPUTS.json", **item, "verified": True})
manifest = json.loads((SOURCE / "audit/AUDIT_MANIFEST.json").read_text())
for path, item in manifest["portable_files"].items():
    data = (SOURCE / "audit" / path).read_bytes()
    require(len(data) == item["bytes"] and sha(data) == item["sha256"], path)
    refs.append({"manifest": "audit/AUDIT_MANIFEST.json", "path": path, **item, "verified": True})

cases = [
    ("author", "release/checks/verify_bianchi_counterexample.py", "release/checks/verification_results.json", 17),
    ("historical_independent", "audit/audit_controls.py", "audit/audit_controls.json", 35),
]
out = HERE / "replays"
out.mkdir(exist_ok=True)
run_results = []
for name, program, stored, count in cases:
    tree = ast.parse((SOURCE / program).read_text())
    assert_lines = [node.lineno for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    original = (SOURCE / stored).read_bytes()
    for optimized in (False, True):
        label = name + ("_optimized" if optimized else "_normal")
        private = HERE / "private_sources" / "replays" / label
        private.mkdir(parents=True, exist_ok=True)
        copy = private / Path(program).name
        shutil.copyfile(SOURCE / program, copy)
        command = [sys.executable] + (["-O"] if optimized else []) + [str(copy)]
        proc = subprocess.run(command, capture_output=True, text=True, check=False)
        (out / (label + ".stdout.txt")).write_text(proc.stdout)
        (out / (label + ".stderr.txt")).write_text(proc.stderr)
        require(proc.returncode == 0, label + " exit")
        generated = (private / Path(stored).name).read_bytes()
        obj = json.loads(generated)
        require(obj.get("all_passed") is True, label + " all_passed")
        require(len(obj["checks"]) == count and all(type(v) is bool and v for v in obj["checks"].values()), label + " active result checks")
        require(generated == original, label + " exact historical output bytes")
        (out / (label + ".json")).write_bytes(generated)
        run_results.append({"name": label, "exit_code": proc.returncode, "checks": count, "output_sha256": sha(generated), "byte_identical_to_historical": True, "assert_statement_lines_in_original": assert_lines, "external_explicit_postconditions_active_under_O": True})

for item in receipt["files"]:
    data = (SNAPSHOT / item["path"]).read_bytes()
    require(len(data) == item["bytes"] and sha(data) == item["sha256"], "source changed " + item["path"])

result = {
    "pr": 464, "problem_id": "30004807", "head_sha": receipt["head_sha"],
    "python_version": platform.python_version(), "interpreter": sys.executable,
    "bound_source_files": bound, "extant_manifest_payload_references": refs,
    "bound_source_count": len(bound), "verified_extant_reference_count": len(refs),
    "unattested_reference": {"manifest": "audit/FROZEN_INPUTS.json", "field": "author_manifest_sha256", "recorded_sha256": frozen["author_manifest_sha256"], "reason": "No standalone author-manifest path or bytes are present among the thirteen frozen source files; this reference is not verified or reconstructed."},
    "runs": run_results, "all_original_sources_unchanged": True,
    "assertion_caveat": "The original author program's final assert is disabled under -O. This driver independently requires all seventeen Boolean checks, exact check count, exit status, and byte-identical stored JSON in both modes; its guards use explicit conditional raises.",
    "historical_independent_guard": "The historical independent program uses explicit verify/raise statements rather than assert statements."
}
(HERE / "REPLAY_RECEIPT.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"source_files": len(bound), "manifest_payload_references": len(refs), "replay_runs": len(run_results), "all_sources_unchanged": True, "all_outputs_byte_identical": True}, indent=2))
