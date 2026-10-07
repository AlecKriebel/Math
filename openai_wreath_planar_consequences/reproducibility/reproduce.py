#!/usr/bin/env python3
"""Check extracted-package identity and replay authored computations.

Fresh receipts are written outside the extracted package. A temporary copy
protects the supplied evidence files from checkers which write beside code.
Finite computations never replace the written analytic and topological proofs.
"""
from __future__ import annotations
import argparse
import ast
import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest():
    manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text())
    files = manifest["files"]
    names = [entry["path"] for entry in files]
    if names != sorted(set(names)):
        raise ValueError("Manifest paths must be sorted and unique")
    if hashlib.sha256(canonical(files)).hexdigest() != manifest["package_identity_sha256"]:
        raise ValueError("Package identity does not match inventory")
    for entry in files:
        path = ROOT / entry["path"]
        if not path.is_file() or path.is_symlink() or path.stat().st_size != entry["bytes"] or sha(path) != entry["sha256"]:
            raise ValueError(f"File identity mismatch: {entry['path']}")
    if json.loads((ROOT / "reproducibility/package_files.json").read_text())["files"] != names:
        raise ValueError("Manifest does not match explicit package whitelist")
    # The reproduction output and virtual environment belong outside this root.
    actual = {str(path.relative_to(ROOT)) for path in ROOT.rglob("*") if path.is_file()}
    if actual != set(names) | {"PACKAGE_MANIFEST.json"}:
        raise ValueError(f"Unexpected or missing extraction files: {sorted(actual.symmetric_difference(set(names) | {'PACKAGE_MANIFEST.json'}))}")
    return manifest


def verify_mathematical_data():
    """Compare independent checker inputs without importing or executing code."""
    packaged = json.loads((ROOT / "publication/support/data/planar_certificate_tables.json").read_text())
    packaged.pop("provenance")
    for name in ("independent_scalar_checks.py", "independent_validated_integrals.py"):
        tree = ast.parse((ROOT / "target_b" / name).read_text())
        nodes = [node for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "data" for target in node.targets)]
        if len(nodes) != 1 or not isinstance(nodes[0].value, ast.Call) or len(nodes[0].value.args) != 1:
            raise ValueError(f"Cannot inspect exact input data in {name}")
        embedded = json.loads(ast.literal_eval(nodes[0].value.args[0]))
        if embedded != packaged:
            raise ValueError(f"Packaged exact table differs from checker inputs: {name}")
    return {"status": "PASS_EXACT_INPUT_CONSISTENCY", "checkers_compared": 2}


def run_checked(command, cwd, output, label):
    start = time.monotonic()
    process = subprocess.run(command, cwd=cwd, capture_output=True, text=True, env={key: value for key, value in os.environ.items() if key not in {"PYTHONPATH", "PYTHONOPTIMIZE"}})
    (output / f"{label}.stdout.txt").write_text(process.stdout)
    (output / f"{label}.stderr.txt").write_text(process.stderr)
    record = {"label": label, "command": command, "returncode": process.returncode, "elapsed_seconds": time.monotonic() - start, "stdout_sha256": sha(output / f"{label}.stdout.txt"), "stderr_sha256": sha(output / f"{label}.stderr.txt")}
    if process.returncode:
        raise RuntimeError(f"{label} failed with exit {process.returncode}; see saved output")
    return process, record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True, help="New directory outside the package for reproduction receipts")
    parser.add_argument("--quick", action="store_true", help="Omit full integral and secondary Bernstein runs; cannot certify full reproduction")
    parser.add_argument("--pdf", action="store_true", help="Also rebuild with pinned Tectonic and compare all extracted PDF text")
    args = parser.parse_args()
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError("Assertions must remain enabled")
    output = args.output_dir.resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError("Reproduction outputs must be outside the extraction")
    output.mkdir(parents=True, exist_ok=False)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt = {"schema": "clean-reproduction-receipt-v1", "started_utc": started, "status": "running", "python": platform.python_version(), "platform": platform.platform(), "checks": [], "quick": args.quick, "pdf_requested": args.pdf}
    receipt_path = output / "REPRODUCTION_RECEIPT.json"
    try:
        manifest = verify_manifest()
        receipt["package_identity_sha256"] = manifest["package_identity_sha256"]
        receipt["manifest_verified"] = True
        receipt["mathematical_input_consistency"] = verify_mathematical_data()
        env = json.loads((ROOT / "reproducibility/ENVIRONMENT.json").read_text())
        if platform.python_version_tuple()[:2] != tuple(env["python_minor_required"].split(".")):
            raise RuntimeError(f"Use Python {env['python_minor_required']} for the documented environment")
        flint_version = importlib.metadata.version("python-flint")
        if flint_version != env["rigorous_arithmetic"]["version"]:
            raise RuntimeError("The pinned python-flint version is required")
        receipt["python_flint"] = flint_version
        receipt["python_patch_matches_recorded"] = platform.python_version() == env["python"]
        tasks = [
            ("fixed_constants", "target_a/check_fixed_constants.py", None, "all checks passed"),
            ("wreath_orientation", "bridges/wreath/check_orientation.py", None, "passed"),
            ("exact_lattice", "bridges/triangle/check_exact_lattice.py", None, "PASS_EXACT_FINITE_CONTROLS"),
            ("scalar_bounds", "target_b/independent_scalar_checks.py", "target_b/independent_scalar_receipt.json", "pass"),
        ]
        if not args.quick:
            tasks += [
                ("validated_integrals", "target_b/independent_validated_integrals.py", "target_b/independent_validated_integrals_receipt.json", "pass"),
                ("secondary_bernstein", "reproducibility/checks/standalone_arb_bernstein.py", "reproducibility/checks/standalone_arb_bernstein_receipt.json", "pass_all_finite_bernstein_grouped_claims"),
            ]
        with tempfile.TemporaryDirectory(prefix="wreath-planar-reproduction-") as temporary:
            work = Path(temporary) / "package"
            shutil.copytree(ROOT, work)
            for label, relative_script, relative_receipt, status in tasks:
                print(f"Replaying {label}", flush=True)
                result, check = run_checked([sys.executable, "-I", "-B", str(work / relative_script)], work, output, label)
                fresh = json.loads((work / relative_receipt).read_text()) if relative_receipt else json.loads(result.stdout)
                if fresh.get("status") != status:
                    raise ValueError(f"Unexpected mathematical status in {label}")
                if label == "validated_integrals":
                    expected = {"finite_nodes": 51, "matrix_signs": 2, "residual_pairs": 102, "half_gap_intervals": 84, "Bernstein_inequalities": 2436}
                    if fresh.get("full_finite_gates") != "pass" or fresh.get("coverage") != expected:
                        raise ValueError("Incomplete rigorous finite-gate reproduction")
                if label == "secondary_bernstein" and (len(fresh.get("checks", [])) != 84 or sum(len(row["all_29_bernstein_enclosures"]) for row in fresh["checks"]) != 2436):
                    raise ValueError("Incomplete secondary Bernstein reproduction")
                (output / f"{label}.receipt.json").write_text(json.dumps(fresh, indent=2) + "\n")
                check["receipt_sha256"] = sha(output / f"{label}.receipt.json")
                receipt["checks"].append(check)
                receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
            if args.pdf:
                version = subprocess.run(["tectonic", "--version"], capture_output=True, text=True, check=True).stdout.strip()
                if not version.endswith(env["publication_build"]["version"]):
                    raise RuntimeError("The pinned Tectonic version is required")
                pdfout = output / "pdf"
                pdfout.mkdir()
                _, record = run_checked(["tectonic", "--keep-logs", "--outdir", str(pdfout), str(work / "publication/preprint.tex")], work, output, "publication_pdf")
                def text_pdf(path):
                    return subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True, check=True).stdout
                oldtext = text_pdf(ROOT / "publication/preprint.pdf")
                newtext = text_pdf(pdfout / "preprint.pdf")
                (output / "publication_original_text.txt").write_text(oldtext)
                (output / "publication_rebuilt_text.txt").write_text(newtext)
                if re.sub(r"\s+", " ", oldtext).strip() != re.sub(r"\s+", " ", newtext).strip():
                    raise ValueError("Rebuilt PDF text differs from packaged PDF")
                record.update({"compiler": version, "rebuilt_pdf_sha256": sha(pdfout / "preprint.pdf"), "packaged_pdf_sha256": sha(ROOT / "publication/preprint.pdf"), "normalized_all_page_text_matches": True, "visual_inspection_required_separately": True})
                receipt["checks"].append(record)
        receipt["status"] = "PASS_QUICK_SUBSET" if args.quick else "PASS_ALL_AUTHORED_COMPUTATIONS"
        receipt["pdf_build_and_text_verified"] = args.pdf
        receipt["limitations"] = ["Finite arithmetic is not a replacement for the written analytic, probabilistic, topological and literature dependency proofs.", "This runner does not compile the associated Lean construction, which formalizes a different input theorem.", "PDF text agreement does not replace visual inspection of every PDF page.", "Publication and priority gates are assessed independently of this computation runner."]
    except Exception as error:
        receipt["status"] = "FAILED"
        receipt["error"] = str(error)
        raise
    finally:
        receipt["finished_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
