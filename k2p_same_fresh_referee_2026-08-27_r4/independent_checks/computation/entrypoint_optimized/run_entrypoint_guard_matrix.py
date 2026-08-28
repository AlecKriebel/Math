#!/usr/bin/env python3
"""Exercise optimized-mode preflights without running any full replay."""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess


ROOT = pathlib.Path(__file__).resolve().parents[3]
PROJECT = ROOT / "execution/k2p_principal_d_plus_submission_referee"
PYTHON = PROJECT / ".venv/bin/python"
OUT = pathlib.Path(__file__).resolve().parent


CASES = (
    ("bundle_builder", "output/referee/build_referee_bundle.py", ["--check-only"]),
    (
        "release_lock_builder",
        "work/final_theorem_release/build_release_lock.py",
        ["--check", "--require-ready"],
    ),
    (
        "final_quick",
        "work/final_theorem_release/verify_final_theorem_release.py",
        ["--quick"],
    ),
    (
        "outer_mutations",
        "work/final_theorem_release/run_release_mutations.py",
        [],
    ),
    (
        "corrected_universe_mutations",
        "work/final_theorem_release/run_corrected_universe_mutations.py",
        ["--output", str(OUT / "optimized-corrected-universe.json")],
    ),
    (
        "outer_output_contract",
        "work/final_theorem_release/test_release_mutation_output_contract.py",
        [],
    ),
    (
        "nested_output_contract",
        "work/final_theorem_release/test_nested_mutation_output_contract.py",
        [],
    ),
    (
        "final_replay_output_contract",
        "work/final_theorem_release/test_final_replay_output_contract.py",
        [],
    ),
    (
        "direct_closure",
        "package/referee/k2p_offline_sweep_portable/verify_direct_closure_release.py",
        ["--quick"],
    ),
    (
        "direct_closure_mutations",
        "package/referee/k2p_offline_sweep_portable/test_direct_closure_release_mutations.py",
        ["--output", str(OUT / "optimized-direct-closure-mutations.json")],
    ),
)


def main() -> None:
    rows = []
    for name, script, arguments in CASES:
        result = subprocess.run(
            [str(PYTHON), "-O", "-B", str(PROJECT / script), *arguments],
            cwd=PROJECT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=20,
            check=False,
        )
        rows.append({
            "name": name,
            "script": script,
            "exit_code": result.returncode,
            "output_sha256": hashlib.sha256(result.stdout).hexdigest(),
            "output": result.stdout.decode("utf-8", errors="replace").strip(),
        })
    print(json.dumps({"cases": rows}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
