#!/usr/bin/env python3
"""Reproduce supporting computations in temporary copies, never in author files.

This is a finite-computation control, not verification of the full conjecture.
The infinite deductions require the written proofs and adversarial reviews.
"""
from datetime import datetime, timezone
import argparse
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent.parent
JOBS = [
    "topological/check_thin_branch.py",
    "topological_review/independent_check.py",
    "topological_review/secondary/independent_controls.py",
    "topological/check_abelian_extraction_obstruction.py",
    "abelian_extraction_review/independent_check.py",
    "structural/check_central_countermodel.py",
    "structural/central_countermodel_review/independent_affine_check.py",
    "structural/check_structural_examples.py",
    "structural/route_review/independent_matrix_products.py",
    "counterexample/check_finite_models.py",
    "counterexample_review/independent_models.py",
    "counterexample_review/law_branch_secondary/independent_checks.py",
]
PREFIXES = ("topological", "topological_review", "abelian_extraction_review",
            "structural", "counterexample", "counterexample_review")
EXPLICIT = ("priority/sources/notebook21_fresh.txt",
            "priority/sources/shumyatsky2401.15707v2.txt")
TIME_KEYS = {"utc", "timestamp_utc", "created_utc", "checked_utc", "generated_utc", "updated_utc"}


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items() if k not in TIME_KEYS}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="+", choices=JOBS)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("ROOT_REPRODUCTION.json"))
    args = parser.parse_args()
    jobs = args.only or JOBS
    assert not args.output.exists(), "Preserve previous reproduction receipts"
    frozen = {}
    for prefix in PREFIXES:
        for path in (ROOT / prefix).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts and "tmp" not in path.parts:
                frozen[str(path.relative_to(ROOT))] = path.read_bytes()
    for relative in EXPLICIT:
        frozen[relative] = (ROOT / relative).read_bytes()
    missing = [p for p in jobs if p not in frozen]
    assert not missing, missing
    results = []
    with tempfile.TemporaryDirectory(prefix="kourovka122-root-check-") as directory:
        temporary = Path(directory)
        for job in jobs:
            # Each checker sees the original frozen bytes, including certificate
            # hashes. Timestamped outputs from earlier jobs cannot contaminate it.
            for relative, payload in frozen.items():
                target = temporary / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(payload)
            before = {p: frozen[p] for p in frozen if p.endswith(".json")}
            started = time.monotonic()
            completed = subprocess.run([sys.executable, str(temporary / job)],
                                       cwd=temporary, capture_output=True, text=True,
                                       timeout=120)
            comparisons = []
            for relative, payload in before.items():
                current = (temporary / relative).read_bytes()
                if current != payload:
                    assert clean(json.loads(current)) == clean(json.loads(payload)), (job, relative)
                    comparisons.append(relative)
            result = {"job": job, "exit_code": completed.returncode,
                      "seconds": round(time.monotonic()-started, 3),
                      "stdout_tail": completed.stdout[-1500:],
                      "stderr_tail": completed.stderr[-1000:],
                      "changed_json_equal_except_timestamps": comparisons}
            results.append(result)
            assert completed.returncode == 0, result
    for relative, payload in frozen.items():
        assert (ROOT / relative).read_bytes() == payload, relative
    output = {"utc": datetime.now(timezone.utc).isoformat(), "result": "PASS",
              "scope": "Reproduction of finite supporting computations only; no complete21.122 resolution or novelty claim",
              "jobs": results, "author_and_reviewer_files_unchanged": True,
              "inputs": [{"path": p, "sha256": sha256(frozen[p]).hexdigest()}
                         for p in sorted(frozen)]}
    path = args.output
    with path.open("x") as handle:
        json.dump(output, handle, indent=2)
        handle.write("\n")
    print(json.dumps({"result": "PASS", "jobs": len(results), "input_files": len(frozen),
                      "originals_unchanged": True, "receipt": str(path)}))


if __name__ == "__main__":
    main()
