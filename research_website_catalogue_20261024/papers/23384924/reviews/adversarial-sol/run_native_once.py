#!/usr/bin/env python3
"""One unchanged stdlib native route with owned streams and full source guards."""
from pathlib import Path
import hashlib
import json
import stat
import subprocess
import datetime
import sys

OWN = Path(__file__).resolve().parent
SOURCE = OWN.parents[1] / "sources"
SCRIPT = SOURCE / "published-source/container-001/tree/native/unsolved_math_prioritization/attempts/2306086/author/exact_controls.py"


def pin(path, root):
    return {"path": path.relative_to(root).as_posix(), "bytes": path.stat().st_size,
            "SHA256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "mode": oct(stat.S_IMODE(path.stat().st_mode))}


def snapshot():
    files, directories = [], []
    for path in sorted(SOURCE.rglob("*")):
        if path.is_symlink():
            raise RuntimeError("unexpected source link")
        if path.is_file():
            files.append(pin(path, SOURCE))
        elif path.is_dir():
            directories.append({"path": path.relative_to(SOURCE).as_posix(),
                                "mode": oct(stat.S_IMODE(path.stat().st_mode))})
        else:
            raise RuntimeError("unexpected source object")
    return {"root_mode": oct(stat.S_IMODE(SOURCE.stat().st_mode)),
            "files": files, "directories": directories}


def write_json(path, value):
    with path.open("x") as handle:
        handle.write(json.dumps(value, indent=2) + "\n")


def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    before = snapshot()
    initial = json.loads((OWN / "SOURCE_CUSTODY.json").read_text())
    for key in ("root_mode", "files", "directories"):
        if before[key] != initial[key]:
            raise RuntimeError("source changed before route: " + key)
    write_json(OWN / "NATIVE_SOURCE_BEFORE.json", before)
    route = OWN / "native-route"
    route.mkdir(exist_ok=False)
    target = route / "exact_controls.py"
    with target.open("xb") as handle:
        handle.write(SCRIPT.read_bytes())
    command = ["/usr/bin/python3", "-I", "-B", str(target)]
    write_json(OWN / "NATIVE_INVOCATION.json", {
        "started_UTC": started, "command": command, "cwd": str(route),
        "exact_relocated_script": pin(target, OWN),
        "all_inputs": "embedded fixed constants and rational loops; no data file",
        "expected_status": "PASS", "expected_predicates_from_hand_count": 3558,
        "expected_family_labels": 16, "native_execution_budget": 1,
        "retry_or_optimized_variant_authorized": False})
    error = None
    try:
        result = subprocess.run(command, cwd=route, capture_output=True, check=False)
        stdout, stderr, code = result.stdout, result.stderr, result.returncode
    except Exception as exc:
        stdout, stderr, code = b"", b"", None
        error = repr(exc)
    for name, value in (("native.stdout.txt", stdout), ("native.stderr.txt", stderr)):
        with (OWN / name).open("xb") as handle:
            handle.write(value)
    after = snapshot()
    write_json(OWN / "NATIVE_SOURCE_AFTER.json", after)
    receipt = {"started_UTC": started,
               "finished_UTC": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "command": command, "exit_code": code, "exception": error,
               "stdout": pin(OWN / "native.stdout.txt", OWN),
               "stderr": pin(OWN / "native.stderr.txt", OWN),
               "source_unchanged": before == after,
               "source_extent": {"files": len(after["files"]),
                                 "child_directories": len(after["directories"])},
               "ordinary_native_invocations": 1 if error is None else 0,
               "process_launch_attempts": 1}
    write_json(OWN / "NATIVE_RECEIPT.json", receipt)
    print(json.dumps(receipt, indent=2))
    return 0 if code == 0 and before == after else 1


if __name__ == "__main__":
    sys.exit(main())
