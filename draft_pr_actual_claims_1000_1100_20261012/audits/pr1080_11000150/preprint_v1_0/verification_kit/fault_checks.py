#!/usr/bin/env python3
"""Targeted negative controls in temporary copies, normal and optimized Python."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def execute(kit, script, arguments, optimized):
    command = [sys.executable, "-I"] + (["-O"] if optimized else [])
    return subprocess.run(command + [str(kit / script)] + arguments,
                          capture_output=True, text=True, timeout=120)


def main():
    observations = []
    for optimized in [False, True]:
        for fault in ["word_conjugation", "parity", "erasing"]:
            result = execute(ROOT, "run_checks.py", ["--fault", fault], optimized)
            require(result.returncode != 0 and "portable reviewer guard" in result.stderr,
                    "mathematical fault escaped guard: " + fault)
            observations.append({"fault": fault, "optimized": optimized, "detected": True})
        for fault in ["changed_member", "extra_file", "unsafe_manifest_path", "symlink", "missing_required_binding", "missing_explicit_binding", "malformed_present_binding", "wrong_present_binding"]:
            with tempfile.TemporaryDirectory(prefix="pr1080-fault-") as temp:
                kit = Path(temp) / "verification_kit"
                shutil.copytree(ROOT, kit)
                arguments = []
                if fault == "changed_member":
                    with (kit / "preprint.tex").open("a") as stream:
                        stream.write("% targeted fault\n")
                elif fault == "extra_file":
                    (kit / "unlisted.txt").write_text("fault\n")
                elif fault == "unsafe_manifest_path":
                    p = kit / "MANIFEST.json"
                    data = json.loads(p.read_text()); data["files"][0]["path"] = "../escape"
                    p.write_text(json.dumps(data))
                elif fault == "symlink":
                    p = kit / "preprint.tex"; p.unlink(); p.symlink_to(kit / "README.md")
                elif fault == "missing_required_binding":
                    arguments = ["--require-binding"]
                elif fault == "missing_explicit_binding":
                    arguments = ["--binding", str(Path(temp) / "absent.json")]
                elif fault == "malformed_present_binding":
                    (Path(temp) / "EXTERNAL_BINDING.json").write_text("{broken")
                elif fault == "wrong_present_binding":
                    (Path(temp) / "EXTERNAL_BINDING.json").write_text(json.dumps({"manifest_sha256": "0" * 64}))
                result = execute(kit, "verify.py", arguments, optimized)
                require(result.returncode != 0, "package fault escaped: " + fault)
                observations.append({"fault": fault, "optimized": optimized, "detected": True})
    print(json.dumps({"status": "PASS", "negative_controls": observations,
                      "count": len(observations), "scope": "Targeted faults detected; finite controls do not prove the mathematical theorem."}, indent=2))


if __name__ == "__main__":
    main()
