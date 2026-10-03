#!/usr/bin/env python3
"""Capture actual private audit children, with original full streams and prelaunch source."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys

assert __debug__ and sys.flags.optimize == 0
FAMILY = Path(__file__).resolve().parent


def now():
    return datetime.now(timezone.utc).isoformat()


def ref(path):
    path = Path(path).resolve()
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "full_mode": path.stat().st_mode & 0o7777}


def capture(name, argv, cwd, source=None, expected_exit=0):
    assert isinstance(name, str) and name and '/' not in name
    assert isinstance(argv, list) and argv and all(isinstance(x, str) for x in argv)
    cwd = Path(cwd).resolve()
    target = FAMILY / 'captures' / name
    target.mkdir(parents=True, exist_ok=False)
    operator = Path(__file__).resolve()
    (target / 'prelaunch_operator.py').write_bytes(operator.read_bytes())
    child_ref = None
    if source is not None:
        source = Path(source).resolve()
        child_ref = ref(source)
        (target / 'prelaunch_child_source.py').write_bytes(source.read_bytes())
    pre = {"schema": "pr48-algebra-family-real-prelaunch/v1", "created_utc": now(),
           "operator_pid": os.getpid(), "operator": ref(operator), "argv": argv,
           "cwd": str(cwd), "child_source": child_ref, "expected_exit": expected_exit,
           "source_copied_before_launch": child_ref is not None}
    (target / 'PRELAUNCH.json').write_text(json.dumps(pre, indent=2) + '\n')
    started = now()
    with (target / 'stdout.bin').open('xb') as stdout, (target / 'stderr.bin').open('xb') as stderr:
        child = subprocess.Popen(argv, cwd=str(cwd), stdout=stdout, stderr=stderr)
        child_pid = child.pid
        code = child.wait()
    finished = now()
    out = {"schema": "pr48-algebra-family-real-command-capture/v1", "operator_pid": os.getpid(),
           "child_pid": child_pid, "started_utc": started, "finished_utc": finished,
           "argv": argv, "cwd": str(cwd), "exit_code": code, "expected_exit": expected_exit,
           "operator": ref(operator), "prelaunch": ref(target / 'PRELAUNCH.json'),
           "child_source": child_ref, "stdout": ref(target / 'stdout.bin'),
           "stderr": ref(target / 'stderr.bin'),
           "status": "PASS_EXPECTED_EXIT" if code == expected_exit else "FAIL_UNEXPECTED_EXIT"}
    if child_ref is not None:
        assert ref(source)['sha256'] == child_ref['sha256'], 'child source changed during launch'
    (target / 'CAPTURE.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({"name": name, "child_pid": child_pid, "exit_code": code,
                      "status": out['status'], "stdout": out['stdout'], "stderr": out['stderr']}, indent=2))
    assert code == expected_exit, name
    return out


if __name__ == '__main__':
    args = sys.argv[1:]
    assert len(args) >= 4 and args[2] == '--'
    name, cwd = args[:2]
    argv = args[3:]
    source = Path(argv[2]) if len(argv) >= 3 and argv[1] == '-B' and argv[2].endswith('.py') else None
    capture(name, argv, cwd, source)
