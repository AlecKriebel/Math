#!/usr/bin/env python3
"""Clean standalone PDF builds and exact finite checks; Python 3.10+, stdlib.

This does not certify the mathematical theorems or replace source audits.
Only the two exported PDFs and the project-local build receipt are written.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile


PROJECT = Path(__file__).resolve().parents[1]
DOCUMENTS = (
    ("manuscript/main.tex", "manuscript/paper.pdf"),
    ("manuscript/height-repair.tex", "manuscript/height-repair.pdf"),
)
CHECK_INPUTS = (
    "reproducibility/arithmetic_checks.py",
    "reproducibility/arithmetic_checks.expected.json",
    "agent_notes/parity_matrix_check.py",
    "verification/check_two_converse_programs.py",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command, cwd=cwd, text=True, capture_output=True, timeout=300
    )
    if result.returncode:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {command!r}\n"
            f"{result.stdout}\n{result.stderr}"
        )
    return result


def finite_checks() -> dict:
    # Isolation disables PYTHONOPTIMIZE and other Python environment settings;
    # the supplied verification scripts deliberately use assertions.
    prefix = [sys.executable, "-I", "-B"]
    arithmetic = run(prefix + [CHECK_INPUTS[0]], PROJECT)
    arithmetic_result = json.loads(arithmetic.stdout)
    expected = json.loads((PROJECT / CHECK_INPUTS[1]).read_text())
    if arithmetic_result != expected:
        raise RuntimeError("Arithmetic output differs from the expected JSON object.")

    parity = run(prefix + [CHECK_INPUTS[2]], PROJECT)
    parity_expected = (
        "PASS: 1960 generated reciprocity-consistent cases; "
        "all q0-J toggles exhausted per case; seed=4003."
    )
    if parity.stdout.strip() != parity_expected:
        raise RuntimeError("Parity-matrix check did not report the expected 1960 cases.")

    graphs = run(prefix + [CHECK_INPUTS[3]], PROJECT)
    graph_result = json.loads(graphs.stdout)
    graph_expected = {
        "group_dimensions": [1, 2, 3, 4, 5],
        "restrictions_checked": 62,
        "programs_per_restriction": 3,
        "result": "All grounding, constant and degree-one pair identities passed.",
    }
    if graph_result != graph_expected:
        raise RuntimeError("Graph-program output differs from the expected 62 restrictions.")
    return {
        "arithmetic": {
            "passed": True,
            "expected_json_object_matched": True,
            "output": arithmetic_result,
        },
        "parity_matrices": {"passed": True, "output": parity.stdout.strip()},
        "graph_programs": {"passed": True, "output": graph_result},
        "scope": "Exact finite interface checks; not proof of the global arithmetic inputs.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tectonic", default="tectonic", help="Tectonic executable or path (default: PATH)."
    )
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.error("Python 3.10 or later is required.")
    tectonic = shutil.which(args.tectonic)
    if not tectonic:
        parser.error("Tectonic was not found; supply its installed path with --tectonic.")

    started = datetime.now(timezone.utc).isoformat()
    version = run([tectonic, "--version"], PROJECT).stdout.strip()
    tracked = [source for source, _ in DOCUMENTS] + list(CHECK_INPUTS)
    tracked += ["reproducibility/build_package.py"]
    input_hashes = {name: sha256(PROJECT / name) for name in tracked}
    checks = finite_checks()
    tmp_parent = PROJECT / "tmp"
    tmp_parent.mkdir(exist_ok=True)
    builds = []

    with tempfile.TemporaryDirectory(prefix="candidate-build-", dir=tmp_parent) as temporary:
        build_root = Path(temporary)
        for number, (source_name, output_name) in enumerate(DOCUMENTS):
            source = PROJECT / source_name
            build_dir = build_root / str(number)
            build_dir.mkdir()
            copied_source = build_dir / source.name
            shutil.copyfile(source, copied_source)
            if sha256(copied_source) != input_hashes[source_name]:
                raise RuntimeError(f"Source changed before its clean build: {source_name}")
            result = run(
                [tectonic, "--outdir", str(build_dir), str(copied_source)], build_dir
            )
            pdf = copied_source.with_suffix(".pdf")
            if not pdf.is_file() or not pdf.read_bytes().startswith(b"%PDF-"):
                raise RuntimeError(f"Compiler did not produce a PDF for {source_name}.")
            source_date = re.search(r"\\date\{([^{}]*)\}", copied_source.read_text())
            builds.append(
                {
                    "source": source_name,
                    "output": output_name,
                    "source_sha256": input_hashes[source_name],
                    "source_displayed_date": source_date.group(1) if source_date else None,
                    "pdf_sha256": sha256(pdf),
                    "pdf_bytes": pdf.stat().st_size,
                    "compiler_stdout": result.stdout,
                    "compiler_stderr": result.stderr,
                    "temporary_pdf": pdf,
                }
            )

        if any(sha256(PROJECT / name) != digest for name, digest in input_hashes.items()):
            raise RuntimeError("A source or check input changed during the run; rerun the build.")
        # Export only after both builds and all checks succeeded.
        for build in builds:
            shutil.copyfile(build.pop("temporary_pdf"), PROJECT / build["output"])
            if sha256(PROJECT / build["output"]) != build["pdf_sha256"]:
                raise RuntimeError(f"Export checksum mismatch: {build['output']}")

    receipt = {
        "started_utc": started,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "clean_build_passed": True,
        "software": {
            "python": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "python_executable": sys.executable,
            "tectonic": version,
            "tectonic_executable": tectonic,
            "platform": platform.platform(),
        },
        "input_sha256": input_hashes,
        "documents": builds,
        "checks": checks,
        "source_inputs_unchanged_during_run": True,
        "visual_inspection_included": False,
        "mathematical_proof_verification_included": False,
        "notes": (
            "UTC receipt timestamps describe this build, not manuscript or public-disclosure dates. "
            "PDF hashes identify these actual exports; other toolchains or builds may change PDF bytes."
        ),
    }
    receipt_dir = PROJECT / "receipts"
    receipt_dir.mkdir(exist_ok=True)
    receipt_path = receipt_dir / "candidate_build.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print("PASS: both clean PDF builds and all three finite checks.")
    for build in builds:
        print(f"{build['output']}: {build['pdf_sha256']} ({build['pdf_bytes']} bytes)")
    print("Receipt: receipts/candidate_build.json")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, subprocess.TimeoutExpired, OSError, ValueError) as error:
        print(f"Build failed: {error}", file=sys.stderr)
        raise SystemExit(1)
