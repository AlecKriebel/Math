#!/usr/bin/env python3
"""Run the three finite-control suites in ordinary and optimized Python."""
import argparse
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

SCHEMA = "pr91-finite-verification/v1"
ROOT = Path(__file__).resolve().parent
EXPECTED = {
    "verify.py": ("PASS", 473),
    "independent_checks.py": ("PASS", 907),
    "boundary_checks.py": ("PASS_BOUNDED_CONTROLS", 1340),
}

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dump(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def source_checks():
    provenance_path = ROOT / "SOURCE_PROVENANCE.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    require(provenance.get("schema") == "pr91-verification-source-provenance/v1",
            "unrecognized source provenance schema")
    manifest = {item["file"]: item for item in provenance["sources"]}
    require(set(manifest) == set(EXPECTED), "source provenance does not list exactly three checkers")
    records = []
    for name in sorted(EXPECTED):
        path = ROOT / name
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=name)
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
                "removable assertion in " + name)
        ck = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "ck"]
        require(len(ck) == 1 and isinstance(ck[0].body[0], ast.If),
                "missing explicit condition guard in " + name)
        guard = ck[0].body[0]
        require(isinstance(guard.test, ast.UnaryOp) and isinstance(guard.test.op, ast.Not)
                and isinstance(guard.test.operand, ast.Call)
                and isinstance(guard.test.operand.func, ast.Name)
                and guard.test.operand.func.id == "bool"
                and len(guard.body) == 1 and isinstance(guard.body[0], ast.Raise)
                and not guard.orelse, "unexpected condition guard in " + name)
        actual = sha(path)
        require(actual == manifest[name]["public_source_sha256"], "source hash mismatch: " + name)
        records.append({"file": name, "sha256": actual,
                        "authenticated_original_sha256": manifest[name]["authenticated_original_sha256"],
                        "positive_minimal_repair_sha256": manifest[name]["positive_minimal_repair_sha256"]})
    for name in ["run_all.py", "SOURCE_PROVENANCE.json"]:
        tree = ast.parse((ROOT / name).read_text(encoding="utf-8"), filename=name) if name.endswith(".py") else None
        require(tree is None or not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
                "removable assertion in runner")
        records.append({"file": name, "sha256": sha(ROOT / name)})
    return records

def run_child(name, optimized, artifact, output_dir, env):
    label = name.removesuffix(".py") + ("_optimized" if optimized else "_ordinary")
    work = output_dir / label
    work.mkdir()
    receipt_path = work / "receipt.json"
    argv = [sys.executable, "-E", "-B"]
    if optimized:
        argv.append("-O")
    argv.extend([str(ROOT / name), "--output", str(receipt_path)])
    if name == "boundary_checks.py":
        argv.extend(["--details-output", str(work / "details.json")])
    else:
        argv.extend(["--artifact", str(artifact)])
    sources = []
    for source in [ROOT / "run_all.py", ROOT / name, ROOT / "SOURCE_PROVENANCE.json", artifact]:
        target = work / ("source_" + str(len(sources)) + "_" + source.name)
        shutil.copyfile(source, target)
        sources.append({"origin": str(source), "snapshot": target.name,
                        "sha256": sha(target), "bytes": target.stat().st_size})
    record = {"schema": "pr91-verification-process/v1", "label": label,
              "recorder_pid": os.getpid(), "argv": argv, "cwd": str(work),
              "started_utc": utc(), "sources": sources,
              "python_environment_variables_removed": sorted(key for key in os.environ if key.startswith("PYTHON"))}
    began = time.monotonic()
    with (work / "stdout.bin").open("wb") as stdout, (work / "stderr.bin").open("wb") as stderr:
        child = subprocess.Popen(argv, cwd=work, env=env, stdout=stdout, stderr=stderr)
        record["pid"] = child.pid
        dump(work / "execution.json", record)
        exit_code = child.wait()
    record.update({"exit_code": exit_code, "ended_utc": utc(), "elapsed_seconds": time.monotonic() - began})
    for stream in ["stdout.bin", "stderr.bin"]:
        path = work / stream
        record[stream] = {"bytes": path.stat().st_size, "sha256": sha(path)}
    dump(work / "execution.json", record)
    require(exit_code == 0, label + " exited " + str(exit_code) + "; see " + str(work / "stderr.bin"))
    require(receipt_path.is_file(), "child did not write its requested receipt")
    raw = receipt_path.read_bytes()
    require(raw == (work / "stdout.bin").read_bytes(), "stdout/requested receipt mismatch: " + label)
    receipt = json.loads(raw)
    status, count = EXPECTED[name]
    require(receipt.get("status") == status, "unexpected child status: " + label)
    count_key = "total_controls" if name == "boundary_checks.py" else "exact_assertions"
    require(receipt.get(count_key) == count, "unexpected control count: " + label)
    require(sum(receipt["checks"].values()) == count, "family count mismatch: " + label)
    if name == "boundary_checks.py":
        require(receipt.get("exact_rational_or_discrete_controls") == 774
                and receipt.get("floating_controls") == 566, "boundary classification mismatch")
        require(receipt.get("source_sha256") == sha(ROOT / name), "boundary source hash mismatch")
        require(receipt.get("details_sha256") == sha(work / "details.json"), "boundary details hash mismatch")
        details = json.loads((work / "details.json").read_text(encoding="utf-8"))
        require(len(details["events"]) == 1340 and all(event["result"] is True for event in details["events"]),
                "boundary event ledger mismatch")
        require(all(item["error"] <= item["bound"] for item in details["numerical_error_records"]),
                "boundary numerical tolerance exceeded")
        numeric = {"max_recorded_error": max(item["error"] for item in details["numerical_error_records"]),
                   "tolerance_rule": "abs(lhs-rhs) <= 2e-10 * (1+abs(rhs)); floating diagnostics, not certificates"}
    else:
        require(receipt.get("artifact_sha256") == sha(artifact), "artifact hash mismatch: " + label)
        require(receipt.get("checker_sha256") == sha(ROOT / name), "checker hash mismatch: " + label)
        require(receipt.get("sympy_version") == "1.14.0", "use the tested SymPy version 1.14.0")
        numeric = None
    return {"checker": name, "mode": "optimized" if optimized else "ordinary", "exit_code": exit_code,
            "controls": count, "checks": receipt["checks"], "receipt_sha256": sha(receipt_path),
            "elapsed_seconds": record["elapsed_seconds"], "numerical_diagnostics": numeric}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, default=ROOT.parent / "pr91_note.tex",
                        help="artifact whose bytes are identified in receipts (default: ../pr91_note.tex)")
    parser.add_argument("--output-dir", type=Path,
                        help="new/empty directory for results and full process evidence; default: retained temporary directory")
    args = parser.parse_args()
    require(sys.version_info >= (3, 9), "Python 3.9 or later is required")
    artifact = args.artifact.resolve()
    require(artifact.is_file(), "artifact file is missing: " + str(artifact))
    source_records = source_checks()
    artifact_sha = sha(artifact)
    output_dir = args.output_dir.resolve() if args.output_dir else Path(tempfile.mkdtemp(prefix="pr91-verification-"))
    output_dir.mkdir(parents=True, exist_ok=True)
    require(not any(output_dir.iterdir()), "--output-dir must be empty")
    env = {key: value for key, value in os.environ.items() if not key.startswith("PYTHON")}
    started = utc()
    runs = []
    for optimized in [False, True]:
        for name in EXPECTED:
            runs.append(run_child(name, optimized, artifact, output_dir, env))
    require(sha(artifact) == artifact_sha, "artifact changed during verification")
    for source in source_records:
        require(sha(ROOT / source["file"]) == source["sha256"], "source changed during verification")
    for name in EXPECTED:
        matching = [run for run in runs if run["checker"] == name]
        require(matching[0]["checks"] == matching[1]["checks"],
                "ordinary/optimized mathematical family counts differ: " + name)
    result = {
        "schema": SCHEMA, "status": "PASS_FINITE_CONTROLS",
        "started_utc": started, "ended_utc": utc(),
        "artifact": {"file": artifact.name, "sha256": artifact_sha,
                     "hash_meaning": "Input byte identity only; not certification of the manuscript proof."},
        "runtime": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                    "sympy": "1.14.0", "child_flags": ["-E", "-B"],
                    "optimization_modes": ["ordinary", "optimized"],
                    "dependency_resolution": "native interpreter import path; no PYTHONPATH inherited or injected"},
        "sources": source_records,
        "unique_controls_per_mode": {"submitted_exact_finite_algebra": 473,
                                     "independent_exact_finite_algebra": 907,
                                     "boundary_exact_rational_or_discrete": 774,
                                     "boundary_floating": 566, "total": 2720},
        "runs": runs,
        "limitations": "Finite algebra and sampled floating diagnostics only. Floating checks are not certificates. No infinite-dimensional spectrum, universal arbitrary-norm theorem, continuity, density, recurrence, historical-priority, publication, or human-review conclusion follows from this suite."
    }
    dump(output_dir / "results.json", result)
    print(json.dumps({"status": result["status"], "results": str(output_dir / "results.json"),
                      "controls_per_mode": 2720, "runs": len(runs)}, sort_keys=True))

if __name__ == "__main__":
    main()

