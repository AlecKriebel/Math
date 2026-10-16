#!/usr/bin/env python3
"""Reproduce all reported integer computations and compile the standalone note.

Extract source.zip and verification.zip into one empty directory, then run this
script there. No network service or credentials are required for the arithmetic.
Tectonic may download its ordinary TeX resource bundle if it is not cached.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--compiler", default="tectonic")
    parser.add_argument("--skip-pdf", action="store_true")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    receipt = {"python": sys.version, "proof_limit": "Computations are bounded illustrations/audits, not a proof of EGH."}
    with tempfile.TemporaryDirectory(prefix="sperner-reproduction-", dir=root) as name:
        work = Path(name)
        for folder in ["manuscript", "verification", "notes"]:
            shutil.copytree(root / folder, work / folder)
        def run(cmd):
            result = subprocess.run(cmd, cwd=work, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
            return result.stdout, result.stderr
        stdout, _ = run([sys.executable, "verification/hilbert_examples.py"])
        examples = json.loads(stdout)
        reference = json.loads((root / "verification/hilbert_examples.json").read_text())
        assert examples == reference
        receipt["hilbert_examples"] = {"exact_match": True, "small_cases": examples["independent_small_cases_checked"]}
        stdout, _ = run([sys.executable, "notes/companion_checks.py"])
        arithmetic = [ast.literal_eval(line) for line in stdout.splitlines()]
        assert sum(x.get("pairs_checked", 0) for x in arithmetic) == 87108
        assert arithmetic[-1]["frobenius_orders_checked"] == 396
        receipt["companion_arithmetic"] = arithmetic
        run([sys.executable, "notes/lpp_box_tests.py"])
        box = json.loads((work / "notes/lpp_box_tests.json").read_text())
        old = json.loads((root / "notes/lpp_box_tests.json").read_text())
        assert box["status"] == "no_counterexample_in_exhaustive_domain"
        assert box["limits"]["skipped_larger_degree_boxes"] == []
        for key in ["bound_tuples", "degree_boxes", "stable_sets", "strict_comparison_counts", "rows"]:
            assert box[key] == old[key]
        receipt["bounded_box_audit"] = {k: box[k] for k in ["bound_tuples", "degree_boxes", "stable_sets", "max_degree_box_size"]}
        if not args.skip_pdf:
            compiler = shutil.which(args.compiler) or args.compiler
            version, _ = run([compiler, "--version"])
            output = work / "output"
            output.mkdir()
            _, stderr = run([compiler, "--keep-logs", "--outdir", str(output), "manuscript/main.tex"])
            pdf = output / "main.pdf"
            assert pdf.read_bytes().startswith(b"%PDF-")
            log = (output / "main.log").read_text()
            assert "Overfull" not in log and "undefined" not in log.lower()
            receipt["pdf_build"] = {"compiler": version.strip(), "bytes": pdf.stat().st_size,
                                    "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
                                    "no_overfull_or_undefined": True}
        result = json.dumps(receipt, indent=2) + "\n"
        if args.receipt:
            args.receipt.write_text(result)
        print(result)


if __name__ == "__main__":
    main()
