#!/usr/bin/env python3
"""Replay frozen PR 445 controls and real subprocess mutants, without asserts."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
SOURCE = CASE / "source_snapshot/unsolved_math_prioritization/attempts/30002737"
PRIVATE = HERE / "private/replays"
RECORDS = HERE / "records"
FROZEN_HEAD = "3242c84e06db7e99012c7fe581adde5c3f89fc89"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def replace_once(path, old, new):
    data = path.read_text()
    require(data.count(old) == 1, f"Mutation must uniquely locate {old!r}")
    path.write_text(data.replace(old, new))


def make_copy(name):
    dest = PRIVATE / name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(SOURCE, dest)
    return dest


def execute(name, root, script, optimize):
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)
    if optimize:
        env["PYTHONOPTIMIZE"] = "1"
    start = time.monotonic()
    run = subprocess.run([sys.executable, str(root / script)], capture_output=True,
                         text=True, env=env, cwd=HERE, timeout=300)
    result = {"name": name, "script": script, "inherited_PYTHONOPTIMIZE":
              env.get("PYTHONOPTIMIZE"), "returncode": run.returncode,
              "elapsed_seconds": round(time.monotonic() - start, 6),
              "stdout": run.stdout, "stderr": run.stderr}
    try:
        result["stdout_json"] = json.loads(run.stdout)
    except json.JSONDecodeError:
        result["stdout_json"] = None
    save(RECORDS / (name + ".json"), result)
    print(name, run.returncode, flush=True)
    return result


def main():
    RECORDS.mkdir(parents=True, exist_ok=True)
    receipt = json.loads((CASE / "SOURCE_RECEIPT.json").read_text())
    require(receipt["head_sha"] == FROZEN_HEAD, "Wrong frozen head")
    integrity = []
    for item in receipt["files"]:
        path = CASE / "source_snapshot" / item["path"]
        observed = {"path": item["path"], "bytes": path.stat().st_size,
                    "sha256": sha(path)}
        require(observed["bytes"] == item["bytes"], "Receipt byte mismatch")
        require(observed["sha256"] == item["sha256"], "Receipt hash mismatch")
        integrity.append(observed)
    require(len(integrity) == 12, "Expected all 12 original artifacts")
    for manifest_path, anchor in [(SOURCE / "RELEASE_MANIFEST.json", SOURCE),
                                 (SOURCE / "author/MANIFEST.json", SOURCE / "author")]:
        manifest = json.loads(manifest_path.read_text())
        entries = manifest["files"]
        pairs = entries.items() if isinstance(entries, dict) else ((x["path"], x) for x in entries)
        for name, item in pairs:
            path = anchor / name
            require(sha(path) == item["sha256"], f"Manifest hash mismatch: {name}")
            require(path.stat().st_size == item["bytes"], f"Manifest bytes mismatch: {name}")
    scripts = ["author/checks/verify_counterexample.py", "audit/independent_controls.py"]
    assertion_counts = {s: sum(isinstance(n, ast.Assert) for n in ast.walk(ast.parse((SOURCE / s).read_text())))
                        for s in scripts}
    save(RECORDS / "integrity_environment.json", {"frozen_head": FROZEN_HEAD,
         "captured_at_utc": datetime.now(timezone.utc).isoformat(), "receipt_files": integrity,
         "receipt_and_manifests_match": True, "python_executable": sys.executable,
         "python_version": sys.version, "platform": platform.platform(),
         "dependencies": "Python standard library only", "assertion_nodes": assertion_counts})
    runs = []
    for short, script, output in [("author", scripts[0], "author/checks/verification_results.json"),
                                  ("independent", scripts[1], "audit/independent_controls_results.json")]:
        for optimize in [False, True]:
            name = f"baseline_{short}_{'optimized' if optimize else 'normal'}"
            root = make_copy(name)
            result = execute(name, root, script, optimize)
            require(result["returncode"] == 0, f"Baseline failed: {name}")
            require((root / output).read_bytes() == (SOURCE / output).read_bytes(),
                    f"Baseline bytes differ: {name}")
            result["adjacent_output_byte_identical"] = True
            save(RECORDS / (name + ".json"), result)
            runs.append(result)
    author_mutations = [
        ("author_bad_marker", "E = (F(1, 10), F(1, 10))", "E = (F(1, 6), F(0))"),
        ("author_bad_mean_weights", "D = (F(1), F(1), F(1, 2), F(1, 2))",
         "D = (F(1), F(1), F(1, 2), F(1, 3))"),
        ("author_bad_occupancy", "return F(1 + signs[('x', p) if slot == 2 else ('y', q)], 2)",
         "return F(1 + signs[('x', p) if slot == 2 else ('y', q)], 3)"),
        ("author_bad_suspension", "target = max(F(0), 1-abs(t))",
         "target = max(F(0), 1-abs(t)) + F(1, 10)"),
    ]
    for name, old, new in author_mutations:
        for optimize in [False, True]:
            run_name = name + ("_optimized" if optimize else "_normal")
            root = make_copy(run_name)
            replace_once(root / scripts[0], old, new)
            result = execute(run_name, root, scripts[0], optimize)
            result["mutation"] = {"old": old, "new": new}
            result["expected_rejection"] = True
            save(RECORDS / (run_name + ".json"), result)
            runs.append(result)
    independent_mutations = [
        ("independent_bad_rs_coding", "signs=[1 if c in 'ab' else -1 for c in word]",
         "signs=[1 if c in 'ac' else -1 for c in word]"),
        ("independent_bad_physical_pairs", "actual=sum((p[0]+r[0],p[1]+r[1]) in points for p in points)",
         "actual=1+sum((p[0]+r[0],p[1]+r[1]) in points for p in points)"),
        ("independent_bad_flow", "    return total\nflow_checks=0",
         "    return 2*total\nflow_checks=0"),
    ]
    for name, old, new in independent_mutations:
        for optimize in [False, True]:
            run_name = name + ("_optimized" if optimize else "_normal")
            root = make_copy(run_name)
            replace_once(root / scripts[1], old, new)
            result = execute(run_name, root, scripts[1], optimize)
            result["mutation"] = {"old": old, "new": new}
            result["expected_rejection"] = True
            save(RECORDS / (run_name + ".json"), result)
            runs.append(result)
    for special in ["manifest_hash_mismatch", "replay_result_mismatch", "missing_expected_results"]:
        for optimize in [False, True]:
            name = f"independent_{special}_{'optimized' if optimize else 'normal'}"
            root = make_copy(name)
            manifest_path = root / "author/MANIFEST.json"
            manifest = json.loads(manifest_path.read_text())
            expected_path = root / "author/checks/verification_results.json"
            if special == "manifest_hash_mismatch":
                manifest["files"]["checks/verify_counterexample.py"]["sha256"] = "0" * 64
                save(manifest_path, manifest)
            elif special == "replay_result_mismatch":
                expected = json.loads(expected_path.read_text())
                expected["density"] = "300"
                save(expected_path, expected)
                manifest["files"]["checks/verification_results.json"]["sha256"] = sha(expected_path)
                manifest["files"]["checks/verification_results.json"]["bytes"] = expected_path.stat().st_size
                save(manifest_path, manifest)
            else:
                expected_path.unlink()
                # Keep the deliberately missing input in the frozen manifest.
            result = execute(name, root, scripts[1], optimize)
            result["mutation"] = special
            result["expected_rejection"] = True
            save(RECORDS / (name + ".json"), result)
            runs.append(result)
    for item in receipt["files"]:
        require(sha(CASE / "source_snapshot" / item["path"]) == item["sha256"],
                "Frozen original changed after runs")
    negatives = [r for r in runs if r.get("expected_rejection")]
    summary = {"baseline_runs": 4, "baseline_byte_identical": 4,
               "negative_runs": len(negatives),
               "normal_rejected": sum(r["returncode"] != 0 for r in negatives if r["inherited_PYTHONOPTIMIZE"] is None),
               "optimized_rejected": sum(r["returncode"] != 0 for r in negatives if r["inherited_PYTHONOPTIMIZE"] == "1"),
               "optimized_false_success": [r["name"] for r in negatives if r["inherited_PYTHONOPTIMIZE"] == "1" and r["returncode"] == 0],
               "all_12_frozen_originals_unchanged": True,
               "assertion_nodes": assertion_counts}
    save(RECORDS / "reproduction_summary.json", summary)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
