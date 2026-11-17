"""Single ordinary unmodified default package reproduction in an isolated copy.

Review infrastructure only. No installation, interpreter changes, retries,
network, source mutations, Git, TeX compilation, or Lean build are performed.
The entrypoint and both called custom scientific script bodies were personally
read before this runner was created. Native inputs are separately guarded.
"""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import stat
import subprocess
import time

LANE = Path(__file__).resolve().parent
ORIGINAL = LANE.parents[1] / "sources/archives/02-source-and-verification.zip.extracted"
WORKSPACE = LANE / "native-workspace"


def inventory(root):
    entries = []
    for path in [root, *sorted(root.rglob("*"))]:
        metadata = path.lstat()
        relative = "." if path == root else path.relative_to(root).as_posix()
        kind = "directory" if path.is_dir() else "file" if path.is_file() else "other"
        entry = {"path": relative, "kind": kind,
                 "mode": oct(stat.S_IMODE(metadata.st_mode))}
        if kind == "file":
            data = path.read_bytes()
            entry.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        elif kind == "directory":
            entry["empty"] = not any(path.iterdir())
        entries.append(entry)
    return entries


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


assert not (LANE / "NATIVE_RESULT.json").exists(), "A native route already ran"
assert not WORKSPACE.exists(), "Do not reuse or retry a native workspace"
shutil.copytree(ORIGINAL, WORKSPACE)
before = inventory(WORKSPACE)
(LANE / "NATIVE_INPUTS_BEFORE.json").write_text(json.dumps(before, indent=2) + "\n")
command = ["python3", "verification/reproduce.py"]
start = utc()
monotonic_start = time.monotonic()
timeout = False
try:
    result = subprocess.run(command, cwd=WORKSPACE, capture_output=True,
                            timeout=120, check=False)
    stdout, stderr, returncode = result.stdout, result.stderr, result.returncode
except subprocess.TimeoutExpired as error:
    timeout = True
    stdout, stderr, returncode = error.stdout or b"", error.stderr or b"", None
elapsed = time.monotonic() - monotonic_start
end = utc()
(LANE / "NATIVE.stdout.txt").write_bytes(stdout)
(LANE / "NATIVE.stderr.txt").write_bytes(stderr)
after = inventory(WORKSPACE)
(LANE / "NATIVE_INPUTS_AFTER.json").write_text(json.dumps(after, indent=2) + "\n")
receipt = {"command": command, "cwd": str(WORKSPACE),
           "started_utc": start, "completed_utc": end, "elapsed_seconds": elapsed,
           "timeout_seconds": 120, "timed_out": timeout, "exit_status": returncode,
           "ordinary_default_route_count": 1, "unmodified_native_entrypoint": True,
           "custom_called_bodies_read_complete": [
               "verification/reproduce.py",
               "agent_notes/upstream_audit_tensor_certificate.py",
               "agent_notes/moment_dependencies_tensor_check.py"],
           "input_guard_identical": before == after,
           "stdout_bytes": len(stdout), "stderr_bytes": len(stderr),
           "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
           "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
           "scope": "Finite package checks only; no verification of an analytic theorem",
           "follow_up": None}
(LANE / "NATIVE_RESULT.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
