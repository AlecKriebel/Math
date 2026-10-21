"""Record exact native argv, code hashes, UTC times, stdout, and stderr."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
out = root / "executions"
out.mkdir(exist_ok=True)
argv = sys.argv[1:]
if not argv:
    raise SystemExit("Pass an executable and exact arguments")
started = datetime.datetime.now(datetime.timezone.utc)
prefix = started.strftime("%Y%m%dT%H%M%S.%fZ")
hashes = {}
for candidate in [Path(__file__), *[Path(a) for a in argv]]:
    if candidate.is_file():
        hashes[str(candidate.resolve())] = hashlib.sha256(candidate.read_bytes()).hexdigest()
result = subprocess.run(argv, cwd=root, capture_output=True)
stdout_path = out / (prefix + ".stdout")
stderr_path = out / (prefix + ".stderr")
stdout_path.write_bytes(result.stdout)
stderr_path.write_bytes(result.stderr)
record = {
    "started_utc": started.isoformat(),
    "completed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "cwd": str(root), "argv": argv, "input_code_sha256": hashes,
    "exit_code": result.returncode,
    "stdout": str(stdout_path.relative_to(root)),
    "stderr": str(stderr_path.relative_to(root)),
    "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
    "stderr_sha256": hashlib.sha256(result.stderr).hexdigest(),
}
(out / (prefix + ".json")).write_text(json.dumps(record, indent=2) + "\n")
sys.stdout.buffer.write(result.stdout)
sys.stderr.buffer.write(result.stderr)
print("\nNATIVE_EXECUTION_RECORD=" + str(out / (prefix + ".json")), flush=True)
raise SystemExit(result.returncode)
