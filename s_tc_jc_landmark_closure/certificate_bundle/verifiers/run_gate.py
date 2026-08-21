#!/usr/bin/env python3
"""Run a mathematical gate in an isolated copy of the proof bundle."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import json


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], cwd: Path, env: dict[str, str]) -> None:
    print("+ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def copy_bundle(target: Path) -> Path:
    work = target / ROOT.name
    ignored = shutil.ignore_patterns(".venv", "__pycache__", "*.pyc", "*.pyo")
    shutil.copytree(ROOT, work, ignore=ignored)
    return work


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("quick", "full", "regenerate-all"))
    args = parser.parse_args()
    run([sys.executable, str(ROOT / "verifiers/verify_certificate_bundle.py")], ROOT, os.environ.copy())
    repetitions = 2 if args.mode == "regenerate-all" else 1
    commitments = []
    with tempfile.TemporaryDirectory(prefix="stc-jc-proof-bundle-") as raw:
        base = Path(raw)
        for repetition in range(repetitions):
            run_dir = base / f"run-{repetition}"
            run_dir.mkdir()
            work = copy_bundle(run_dir)
            commitment = base / f"commitment-{repetition}.json"
            env = os.environ.copy()
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            env["PYTHONHASHSEED"] = "0"
            env["STC_JC_PYTHON"] = sys.executable
            env["STC_JC_COMMITMENT_OUTPUT"] = str(commitment)
            run([sys.executable, str(work / "verifiers/internal_math_gates.py"), args.mode], work, env)
            # Every generator must either reproduce the committed bytes or
            # write only to its declared temporary output.
            run([sys.executable, str(work / "verifiers/verify_certificate_bundle.py"),
                 "--root", str(work)], work, env)
            commitments.append(json.loads(commitment.read_text()))
        if repetitions == 2 and commitments[0] != commitments[1]:
            raise AssertionError("two complete regeneration runs produced different logical commitments")
    print(f"VERIFIED: certificate bundle mode={args.mode}")


if __name__ == "__main__":
    main()
