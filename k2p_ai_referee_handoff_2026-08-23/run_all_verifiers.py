#!/usr/bin/env python3
"""Run the compact or exhaustive referee qualification and record a ledger."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / "materials" / "k2p_principal_d_plus_submission_referee"


def command(name: str, relative: str, *args: str) -> dict[str, Any]:
    return {"name": name, "argv": [sys.executable, "-B", relative, *args]}


QUICK = [
    {"name": "outer_handoff_integrity", "argv": [sys.executable, "-B", str(ROOT / "verify_handoff.py")]},
    {"name": "outer_handoff_mutations", "argv": [sys.executable, "-B", str(ROOT / "test_handoff_mutations.py")]},
    {"name": "five_source_manuscript_build", "argv": [sys.executable, "-B", str(ROOT / "check_manuscript_build.py")]},
    command("article_static_audit", "proof_compression_submission/adversarial_review/audit_article_sources.py"),
    command("theorem_artifact_crosswalk", "proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py", "--check"),
    command("revised_bundle_primary", "proof_compression_submission/crosswalk/build_revised_referee_bundle.py", "--check"),
    command("revised_bundle_independent", "proof_compression_submission/crosswalk/check_revised_referee_bundle.py"),
    command("revised_bundle_mutations", "proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py", "--check"),
    command("compressed_release", "proof_compression_submission/verify_compressed_release.py", "--check"),
    command("old_new_equivalence", "proof_compression_submission/verify_old_new_equivalence.py", "--check"),
    command("compression_mutations", "proof_compression_submission/run_compression_mutations.py", "--check"),
    command("family_coverage", "proof_compression_submission/analysis/verify_family_coverage_equivalence.py", "--check"),
    command("printed_appendix", "proof_compression_submission/templates/verify_printed_certificate_appendix.py"),
    command("printed_appendix_mutations", "proof_compression_submission/templates/test_printed_certificate_appendix_mutations.py"),
    command("restoration_archetypes", "proof_compression_submission/restoration/verify_restoration_archetypes.py", "--check"),
    command("probe_word_theorem", "proof_compression_submission/probe/verify_probe_word_theorem.py", "--check"),
    command("weak_sharpness_crosswalk", "proof_compression_submission/analysis/verify_weak_sharpness_column_crosswalk.py"),
    command("weak_sharpness_mutations", "proof_compression_submission/analysis/test_weak_sharpness_column_crosswalk_mutations.py"),
    command("release_lock", "work/final_theorem_release/build_release_lock.py", "--check", "--require-ready"),
    command("final_theorem_quick", "work/final_theorem_release/verify_final_theorem_release.py", "--quick", "--timeout-seconds", "7200"),
    command("release_mutations", "work/final_theorem_release/run_release_mutations.py", "--timeout-seconds", "7200"),
]

FULL = QUICK + [
    command("final_theorem_full_primitive_regeneration", "work/final_theorem_release/verify_final_theorem_release.py", "--full", "--timeout-seconds", "7200"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def environment() -> dict[str, Any]:
    try:
        import networkx  # type: ignore
        import sympy  # type: ignore
        dependencies = {"networkx": networkx.__version__, "sympy": sympy.__version__}
    except Exception as exc:  # pragma: no cover - diagnostic path
        dependencies = {"error": repr(exc)}
    return {
        "python": sys.version,
        "executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
        "dependencies": dependencies,
    }


def main() -> None:
    if not __debug__:
        raise SystemExit("optimized Python is forbidden")
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--quick", action="store_true")
    mode.add_argument("--full", action="store_true")
    mode.add_argument("--list", action="store_true")
    parser.add_argument("--keep-going", action="store_true", help="continue after failures for diagnostic coverage")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    commands = FULL if args.full else QUICK
    if args.list:
        for index, row in enumerate(FULL, 1):
            stage = "quick+full" if index <= len(QUICK) else "full-only"
            print(f"{index:02d} [{stage}] {row['name']}: {' '.join(row['argv'])}")
        return
    if not PROJECT.is_dir():
        raise SystemExit(f"project root missing: {PROJECT}")
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = (args.output_dir or ROOT / "referee_outputs" / f"{'full' if args.full else 'quick'}-{stamp}").resolve()
    output.mkdir(parents=True, exist_ok=False)
    rows = []
    overall_start = time.monotonic()
    for index, row in enumerate(commands, 1):
        log = output / f"{index:02d}-{row['name']}.log"
        print(f"[{index}/{len(commands)}] START {row['name']}", flush=True)
        start = time.monotonic()
        with log.open("w", encoding="utf-8") as handle:
            process = subprocess.Popen(
                row["argv"],
                cwd=PROJECT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                errors="replace",
            )
            if process.stdout is None:
                raise RuntimeError(f"stdout pipe unavailable for {row['name']}")
            for line in process.stdout:
                handle.write(line)
            returncode = process.wait()
        elapsed = time.monotonic() - start
        result = {
            "name": row["name"],
            "argv": row["argv"],
            "returncode": returncode,
            "wall_seconds": elapsed,
            "log": log.relative_to(output).as_posix(),
            "log_sha256": sha256(log),
            "status": "PASS" if returncode == 0 else "FAIL",
        }
        rows.append(result)
        print(f"[{index}/{len(commands)}] {result['status']} {row['name']} ({elapsed:.2f}s)", flush=True)
        if returncode != 0 and not args.keep_going:
            break
    report = {
        "schema": "k2p-ai-referee-execution-ledger-v1",
        "mode": "full" if args.full else "quick",
        "status": "PASS" if len(rows) == len(commands) and all(row["returncode"] == 0 for row in rows) else "FAIL",
        "environment": environment(),
        "commands_expected": len(commands),
        "commands_completed": len(rows),
        "wall_seconds": time.monotonic() - overall_start,
        "results": rows,
    }
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    report_path = output / "EXECUTION_LEDGER.json"
    report_path.write_text(encoded, encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "report": str(report_path),
        "report_sha256": sha256(report_path),
        "commands_completed": len(rows),
        "commands_expected": len(commands),
    }, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
