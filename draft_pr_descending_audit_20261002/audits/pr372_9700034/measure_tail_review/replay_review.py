"""Reproduce this audit's controlled executions without changing the candidate.

Candidate inputs and full stdout/stderr are confined to this folder's ignored
private/reproduction directory. Source files are optional and never copied into
the public audit. The program performs no network access or Git/service writes.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--source-dir", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    private = root / "private" / "reproduction"
    private.mkdir(parents=True, exist_ok=True)
    candidate = private / "candidate"
    shutil.copytree(args.candidate.resolve(), candidate, dirs_exist_ok=True)
    commands = [
        (f"turn_{i}", [sys.executable, "-I", str(candidate / f"check_turn_{i}.py")],
         candidate / f"TURN_{i}_CHECKS.json") for i in range(1, 6)
    ]
    for name in ["verify_packet", "verify_publication"]:
        command = [sys.executable, "-I", str(candidate / f"{name}.py")]
        if args.source_dir:
            command += ["--source-dir", str(args.source_dir.resolve())]
        commands.append((name, command, None))
    commands.append(("original_probability_controls", [sys.executable, "-I", str(root / "audit_probability_controls.py")], root / "AUDIT_CONTROLS.json"))
    results = []
    for name, command, receipt in commands:
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        result = subprocess.run(command, cwd=candidate,
                                env={"PATH": os.environ.get("PATH", ""), "LANG": "C.UTF-8", "PYTHONHASHSEED": "0"},
                                capture_output=True, timeout=120)
        (private / f"{name}.stdout").write_bytes(result.stdout)
        (private / f"{name}.stderr").write_bytes(result.stderr)
        item = {
            "name": name, "command": command, "started_utc": started,
            "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "exit_code": result.returncode,
            "stdout_bytes": len(result.stdout), "stderr_bytes": len(result.stderr),
            "stdout_sha256": sha(result.stdout), "stderr_sha256": sha(result.stderr),
        }
        if receipt is not None:
            item["receipt_byte_match"] = result.stdout == receipt.read_bytes()
        results.append(item)
    metadata = {
        "python": sys.version, "executable": sys.executable,
        "platform": platform.platform(),
        "status": "PASS" if all(r["exit_code"] == 0 and r["stderr_bytes"] == 0 and r.get("receipt_byte_match", True) for r in results) else "FAIL",
        "source_checks_requested": args.source_dir is not None,
        "results": results,
        "scope": "Program reproducibility only; mathematical verdict was sealed separately before program inspection.",
    }
    (private / "COMPLETE.json").write_text(json.dumps(metadata, indent=2) + "\n")
    public_metadata = {key: value for key, value in metadata.items() if key != "results"}
    public_metadata["results"] = [{key: value for key, value in result.items() if key != "command"} for result in results]
    (root / "REPRODUCTION_CHECK.json").write_text(json.dumps(public_metadata, indent=2) + "\n")
    print(json.dumps(public_metadata, indent=2))
    return 0 if metadata["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
