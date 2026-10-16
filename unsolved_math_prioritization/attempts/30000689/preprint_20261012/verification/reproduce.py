#!/usr/bin/env python3
"""Reproduce bounded finite controls; this is not a universal proof verifier."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def checked_file(relative_path, expected_hash):
    unresolved = ROOT / relative_path
    path = unresolved.resolve()
    require(path.is_relative_to(ROOT), "Control path escapes package")
    require(unresolved.is_file() and not unresolved.is_symlink(),
            "Missing regular control file")
    data = path.read_bytes()
    require(hashlib.sha256(data).hexdigest() == expected_hash,
            "Control file checksum mismatch: " + relative_path)
    return path, data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("normal", "optimized", "both"), default="both")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "CONTROL_MANIFEST.json").read_text())
    modes = ("normal", "optimized") if args.mode == "both" else (args.mode,)
    results = []
    for case in manifest["cases"]:
        script, _ = checked_file(case["script"], case["script_sha256"])
        _, expected = checked_file(case["expected"], case["expected_sha256"])
        for mode in modes:
            command = [sys.executable]
            if mode == "optimized":
                command.append("-O")
            command.append(str(script))
            run = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=300)
            require(run.returncode == 0,
                    case["script"] + " failed: " + run.stderr.decode(errors="replace"))
            require(not run.stderr, case["script"] + " produced unexpected diagnostic output")
            require(run.stdout == expected, case["script"] + " output differs from recorded bytes")
            results.append({"script": case["script"], "mode": mode,
                            "output_sha256": hashlib.sha256(run.stdout).hexdigest(),
                            "byte_identical": True})
    print(json.dumps({"scope": manifest["scope"], "python": platform.python_version(),
                      "results": results}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
