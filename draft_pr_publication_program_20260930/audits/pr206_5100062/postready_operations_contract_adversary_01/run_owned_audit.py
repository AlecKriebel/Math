#!/usr/bin/env python3
"""Run owned OFFLINE synthetic audit processes and preserve exact raw evidence."""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

OWN = pathlib.Path(__file__).resolve().parent

def pin_bytes(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def pin_file(path):
    return pin_bytes(pathlib.Path(path).read_bytes())

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("normal", "optimized", "dispatcher_optimized"):
        raise SystemExit("Usage: run_owned_audit.py normal|optimized|dispatcher_optimized ATTEMPT_NAME")
    mode, name = sys.argv[1:]
    if not name or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789_" for c in name):
        raise SystemExit("unsafe attempt name")
    out = OWN / "runs" / name
    out.mkdir(parents=True, exist_ok=False)
    harness = OWN / "owned_contract_tests.py"
    executable = pathlib.Path(sys.executable).resolve()
    snapshots = out / "sources"
    snapshots.mkdir()
    for name in ("run_owned_audit.py", "owned_contract_tests.py", "synthetic_model.py", "FINAL_SOURCE_PINS.json"):
        (snapshots / name).write_bytes((OWN / name).read_bytes())
    argv = [str(executable), "-E", "-S", "-B", "-P"] + (["-O"] if mode != "normal" else []) + [str(harness), mode]
    binding = {"schema": "pr206-owned-offline-run-v1", "synthetic_only": True,
        "UTC_start": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "cwd": str(OWN), "argv": argv, "runner": pin_file(__file__),
        "harness": pin_file(harness), "synthetic_model": pin_file(OWN / "synthetic_model.py"), "source_snapshots": {name: pin_file(snapshots / name) for name in ("run_owned_audit.py", "owned_contract_tests.py", "synthetic_model.py", "FINAL_SOURCE_PINS.json")}, "interpreter": {"path": str(executable), **pin_file(executable)},
        "source_pin_manifest": pin_file(OWN / "FINAL_SOURCE_PINS.json")}
    try:
        result = subprocess.run(argv, cwd=OWN, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90, check=False)
        stdout, stderr, exit_code = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as e:
        stdout, stderr, exit_code = e.stdout or b"", e.stderr or b"", "TIMEOUT"
    (out / "stdout.bin").write_bytes(stdout)
    (out / "stderr.bin").write_bytes(stderr)
    binding.update({"UTC_end": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "exit_code": exit_code, "stdout": {"path": str((out / "stdout.bin").relative_to(OWN)), **pin_bytes(stdout)},
        "stderr": {"path": str((out / "stderr.bin").relative_to(OWN)), **pin_bytes(stderr)}})
    (out / "RUN_BINDING.json").write_text(json.dumps(binding, indent=2, sort_keys=True) + "\n")
    print(json.dumps(binding, sort_keys=True))
    print(stdout.decode("utf-8", "replace"))
    if stderr:
        print(stderr.decode("utf-8", "replace"), file=sys.stderr)
    raise SystemExit(0 if exit_code == 0 else 1)

if __name__ == "__main__":
    main()
