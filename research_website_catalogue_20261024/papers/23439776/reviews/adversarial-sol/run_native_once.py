#!/usr/bin/env python3
"""One unchanged native verification route, relocated into this owned folder."""
from pathlib import Path
import datetime
import hashlib
import json
import stat
import subprocess
import sys

OWN = Path(__file__).resolve().parent
SOURCE = OWN.parents[1] / "sources"
TREE = SOURCE / "published-source/container-001/tree"


def pin(path, root):
    return {"path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "SHA256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "mode": oct(stat.S_IMODE(path.stat().st_mode))}


def snapshot():
    files, directories = [], []
    for path in sorted(SOURCE.rglob("*")):
        if path.is_symlink():
            raise RuntimeError("unexpected source symlink")
        if path.is_dir():
            directories.append({"path": path.relative_to(SOURCE).as_posix(),
                                "mode": oct(stat.S_IMODE(path.stat().st_mode))})
        elif path.is_file():
            files.append(pin(path, SOURCE))
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
            raise RuntimeError("source differs from INITIAL custody: " + key)
    route = OWN / "native-route"
    route.mkdir(exist_ok=False)
    write_json(OWN / "NATIVE_SOURCE_BEFORE.json", before)
    for name in ("verify.py", "certificate.json"):
        with (route / name).open("xb") as handle:
            handle.write((TREE / name).read_bytes())
    command = ["/usr/bin/python3", "-I", "-B", str(route / "verify.py")]
    write_json(OWN / "NATIVE_INVOCATION.json", {
        "started_UTC": started, "command": command, "cwd": str(route),
        "exact_relocated_inputs": [pin(route / name, OWN)
                                   for name in ("verify.py", "certificate.json")],
        "expected_summary": {"status": "PASS", "terms": 22,
                             "separation_checks": 968, "rank": 12,
                             "facets": 22, "controls_rejected": 30},
        "execution_budget": "one ordinary route; no retry or optimized variant",
        "source_writes_permitted": False})
    error = None
    try:
        completed = subprocess.run(command, cwd=route, capture_output=True,
                                   check=False)
        stdout, stderr, exit_code = completed.stdout, completed.stderr, completed.returncode
    except Exception as exc:
        stdout, stderr, exit_code = b"", b"", None
        error = repr(exc)
    for name, value in (("native.stdout.txt", stdout), ("native.stderr.txt", stderr)):
        with (OWN / name).open("xb") as handle:
            handle.write(value)
    after = snapshot()
    write_json(OWN / "NATIVE_SOURCE_AFTER.json", after)
    receipt = {"started_UTC": started,
               "finished_UTC": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "command": command, "exit_code": exit_code, "exception": error,
               "stdout": pin(OWN / "native.stdout.txt", OWN),
               "stderr": pin(OWN / "native.stderr.txt", OWN),
               "source_unchanged": before == after,
               "source_extent": {"files": len(after["files"]),
                                 "child_directories": len(after["directories"])},
               "ordinary_native_invocations": 1 if error is None else 0,
               "process_launch_attempts": 1,
               "result": pin(route / "results.json", OWN)
                         if (route / "results.json").is_file() else None}
    write_json(OWN / "NATIVE_RECEIPT.json", receipt)
    print(json.dumps(receipt, indent=2))
    return 0 if exit_code == 0 and before == after else 1


if __name__ == "__main__":
    sys.exit(main())
