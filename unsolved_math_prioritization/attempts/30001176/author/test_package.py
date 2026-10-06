#!/usr/bin/env python3
"""Relocation, optimization and negative-inventory regression controls."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def require(value, message):
    if not value:
        raise RuntimeError(message)


def run():
    source = Path(__file__).resolve().parent
    # Authenticate every executable before running it, including this harness.
    pins = json.loads((source / "CODE_PINS.json").read_text())
    for name in ("check_controls.py", "verify_package.py", "test_package.py"):
        data = (source / name).read_bytes()
        require(hashlib.sha256(data).hexdigest() == pins["files"][name]["sha256"], "initial code pin")
        require(len(data) == pins["files"][name]["bytes"], "initial code size")
    outcomes = []
    def execute(root, optimized=False):
        command = [sys.executable, "-B"] + (["-O"] if optimized else []) + [str(root / "verify_package.py")]
        return subprocess.run(command, cwd="/tmp", capture_output=True,
                              env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), check=False)
    with tempfile.TemporaryDirectory(prefix="exchangeable-package-test-") as temp:
        temp = Path(temp)
        pristine = temp / "relocated with spaces"
        shutil.copytree(source, pristine)
        for opt in (False, True):
            result = execute(pristine, opt)
            require(result.returncode == 0, "relocation/replay failed: " + result.stderr.decode())
            outcomes.append({"test": "relocation_optimized" if opt else "relocation_normal", "status": "PASS"})
        def rewrite_manifest(root, filename):
            p = root / "MANIFEST.json"
            doc = json.loads(p.read_text())
            data = (root / filename).read_bytes()
            doc["files"][filename] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            p.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
        tests = ("extra_file", "missing_file", "modified_proof", "cache_directory", "symlink", "fifo",
                 "changed_code_with_manifest_updated", "changed_result_with_manifest_updated")
        for name in tests:
            root = temp / name
            shutil.copytree(source, root)
            if name == "extra_file":
                (root / "EXTRA.txt").write_text("unexpected\n")
            elif name == "missing_file":
                (root / "PROOF.md").unlink()
            elif name == "modified_proof":
                with (root / "PROOF.md").open("a") as handle:
                    handle.write("\nmutation\n")
            elif name == "cache_directory":
                (root / "__pycache__").mkdir()
            elif name == "symlink":
                (root / "SYMLINK").symlink_to("PROOF.md")
            elif name == "fifo":
                os.mkfifo(root / "FIFO")
            elif name == "changed_code_with_manifest_updated":
                with (root / "check_controls.py").open("a") as handle:
                    handle.write("\n# mutation\n")
                rewrite_manifest(root, "check_controls.py")
            elif name == "changed_result_with_manifest_updated":
                p = root / "CONTROL_RESULTS.json"
                data = json.loads(p.read_text())
                data["total_checks"] += 1
                p.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
                rewrite_manifest(root, "CONTROL_RESULTS.json")
            for opt in (False, True):
                result = execute(root, opt)
                require(result.returncode != 0 and b"FAIL:" in result.stderr, "mutation accepted: " + name)
            outcomes.append({"test": name, "status": "REJECTED_NORMAL_AND_OPTIMIZED"})
    return {"status": "PASS", "tests": outcomes, "scope": "Packaging controls, not mathematical certification."}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
