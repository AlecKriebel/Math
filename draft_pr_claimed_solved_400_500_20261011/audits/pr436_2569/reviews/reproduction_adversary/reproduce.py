#!/usr/bin/env python3
"""Reproduce frozen PR436 verification in private copies, with real controls.

Usage: python reproduce.py --python /path/to/python-with-sympy
No original source bytes, Git state or remote state are changed.
"""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
SOURCE = CASE / "source_snapshot/unsolved_math_prioritization/attempts/2569"
PRIVATE = CASE / "private_sources/reproduction_adversary"
SCRIPTS = {
    "author": ("verify_counterexample.py", "counterexample_results.json"),
    "controls": ("verify_controls.py", "control_results.json"),
    "contributor": ("contributor_checks/check_character_data.py", "contributor_checks/character_checks.json"),
    "independent": ("independent_audit/independent_audit.py", "independent_audit/independent_results.json"),
}


def stamp():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def snapshot_hashes():
    return {str(p.relative_to(SOURCE)): digest(p.read_bytes())
            for p in SOURCE.rglob("*") if p.is_file()}


def fixture(name):
    out = PRIVATE / "fixtures" / name
    if out.exists():
        raise RuntimeError(f"Refusing to overwrite existing fixture {name}")
    shutil.copytree(SOURCE, out)
    return out


def execute(python, name, folder, args, expected=None):
    start = stamp()
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("PYTHONOPTIMIZE", None)
    env.pop("PYTHONPATH", None)
    proc = subprocess.run([python, "-B", *args], cwd=folder, env=env,
                          capture_output=True, timeout=180)
    end = stamp()
    raw = PRIVATE / "raw" / name
    raw.mkdir(parents=True, exist_ok=True)
    (raw / "stdout.txt").write_bytes(proc.stdout)
    (raw / "stderr.txt").write_bytes(proc.stderr)
    (raw / "execution.json").write_text(json.dumps({
        "started_utc": start, "finished_utc": end,
        "command": [python, "-B", *args], "cwd": str(folder),
        "exit_code": proc.returncode}, indent=2) + "\n")
    rec = {"name": name, "started_utc": start, "finished_utc": end,
           "exit_code": proc.returncode, "optimization": "-O" in args,
           "stdout_sha256": digest(proc.stdout), "stderr_sha256": digest(proc.stderr),
           "stdout_bytes": len(proc.stdout), "stderr_bytes": len(proc.stderr),
           "raw_record": f"private_sources/reproduction_adversary/raw/{name}"}
    if expected:
        output = folder / expected
        old = SOURCE / expected
        rec["output_file"] = expected
        rec["output_sha256"] = digest(output.read_bytes())
        rec["historical_sha256"] = digest(old.read_bytes())
        rec["byte_equal_historical"] = output.read_bytes() == old.read_bytes()
        rec["fields_equal_historical"] = json.loads(output.read_text()) == json.loads(old.read_text())
        rec["stdout_byte_equal_output"] = proc.stdout == output.read_bytes()
        (raw / "generated.json").write_bytes(output.read_bytes())
    print(json.dumps(rec), flush=True)
    return rec


def negative_wrapper(folder, script, fault):
    original = folder / script
    wrapper = folder / "negative_control.py"
    if fault in ("author_rank_zero", "controls_rank_zero"):
        function = "a5_augmentation" if fault == "author_rank_zero" else "jordan_controls"
        rankfn = "rank2" if fault == "author_rank_zero" else "rank_mod"
        wrapper.write_text(
            "import json,runpy\n"
            f"ns=runpy.run_path({str(original)!r})\n"
            f"fn=ns[{function!r}]\n"
            f"fn.__globals__[{rankfn!r}]=lambda *a:0\n"
            "print(json.dumps(fn()))\n")
    elif fault == "contributor_bad_class_size":
        tree = ast.parse(original.read_text())
        target = next(n.lineno for n in ast.walk(tree)
                      if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "X" for t in n.targets))
        wrapper.write_text(
            "import runpy,sys\n"
            f"script={str(original)!r}\n"
            "injected=False\n"
            "def trace(frame,event,arg):\n"
            " global injected\n"
            f" if not injected and event=='line' and frame.f_code.co_filename==script and frame.f_lineno=={target}:\n"
            "  frame.f_globals['sizes'][0]=2\n"
            "  injected=True\n"
            " return trace\n"
            "sys.settrace(trace)\n"
            "runpy.run_path(script,run_name='__main__')\n")
    else:
        raise ValueError(fault)
    return wrapper


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args()
    PRIVATE.mkdir(parents=True, exist_ok=True)
    before = snapshot_hashes()
    environment = execute(args.python, "environment", PRIVATE,
                          ["-c", "import sys,sympy; print(sys.version); print('SymPy',sympy.__version__)"])
    records = []
    for name, (script, output) in SCRIPTS.items():
        for optimized in (False, True):
            run_name = name + ("_optimized" if optimized else "_normal")
            folder = fixture(run_name)
            records.append(execute(args.python, run_name, folder,
                                   [*( ["-O"] if optimized else []), str(folder / script)], output))
    negative = []
    faults = [("author_rank_zero", "author"), ("controls_rank_zero", "controls"),
              ("contributor_bad_class_size", "contributor"),
              ("independent_nonidempotent_input", "independent"),
              ("independent_changed_proof_bytes", "independent")]
    for fault, family in faults:
        for optimized in (False, True):
            run_name = fault + ("_optimized" if optimized else "_normal")
            folder = fixture(run_name)
            script = SCRIPTS[family][0]
            if fault == "independent_changed_proof_bytes":
                with (folder / "COUNTEREXAMPLE.md").open("a") as out:
                    out.write("\nPrivate fault injection: changed proof bytes.\n")
                entry = folder / script
            elif fault == "independent_nonidempotent_input":
                datafile = folder / "independent_audit/a5_idempotents.json"
                data = json.loads(datafile.read_text())
                identity = next(e for e in data["entries"] if e["permutation"] == list(range(5)))
                from fractions import Fraction
                identity["coefficients"][0] = str(Fraction(identity["coefficients"][0]) + 1)
                datafile.write_text(json.dumps(data, indent=2) + "\n")
                entry = folder / script
            else:
                entry = negative_wrapper(folder, script, fault)
            rec = execute(args.python, run_name, folder,
                          [*( ["-O"] if optimized else []), str(entry)])
            rec["fault"] = fault
            rec["normal_should_reject"] = True
            rec["fault_rejected"] = rec["exit_code"] != 0
            raw = PRIVATE / "raw" / run_name
            stdout = (raw / "stdout.txt").read_text()
            if rec["exit_code"] == 0:
                value = json.loads(stdout)
                rec["incorrect_success_field"] = value.get("all_checks_passed", value.get("check")) if isinstance(value, dict) else None
                if fault == "author_rank_zero":
                    rec["wrong_matrix_span_dimension"] = value["matrix_algebra_span_dimension"]
                    rec["unsupported_absolutely_irreducible_field"] = value["absolutely_irreducible"]
                elif fault == "controls_rank_zero":
                    rec["incorrect_regular_ranks"] = [row["regular_g_minus_1_rank"] for row in value]
                elif fault == "contributor_bad_class_size":
                    rec["wrong_class_size_sum"] = sum(value["class_sizes"])
                elif fault == "independent_nonidempotent_input":
                    rec["wrong_first_projective_rank"] = value["source_Table5_idempotents"][0]["rank_F2"]
            negative.append(rec)
    after = snapshot_hashes()
    result = {"record_type": "reproduction_execution_results", "finished_utc": stamp(),
              "environment": environment, "baseline_original_runs": records,
              "meaningful_fault_controls": negative, "source_before": before,
              "source_after": after, "sealed_source_unchanged": before == after,
              "baseline_run_count": len(records), "fault_execution_count": len(negative),
              "distinct_fault_count": len(faults)}
    (HERE / "EXECUTION_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"finished": True, "baseline_runs": len(records),
                      "fault_executions": len(negative), "source_unchanged": before == after}), flush=True)


if __name__ == "__main__":
    main()
