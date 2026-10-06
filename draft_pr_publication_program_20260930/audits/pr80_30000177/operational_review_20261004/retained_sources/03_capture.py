"""Private, read-only command capture for PR80 custody; no shell interpolation."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent

def digest(data):
    return hashlib.sha256(data).hexdigest()

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def capture(label, argv, cwd="/Users/alec/Documents/Math", sources=()):
    folder = ROOT / "process_evidence" / label
    folder.mkdir(parents=True, exist_ok=False)
    retained = []
    argv_sources = [item for item in argv if item.endswith(".py") and Path(item).is_file()]
    for index, source in enumerate(dict.fromkeys([str(Path(__file__).resolve()), *sources, *argv_sources])):
        path = Path(source).resolve()
        data = path.read_bytes()
        dest = folder / (str(index) + "_" + path.name)
        dest.write_bytes(data)
        retained.append({"path": str(path), "retained_path": str(dest), "bytes": len(data), "sha256": digest(data)})
    request = {"label": label, "argv": argv, "cwd": cwd, "requested_at_UTC": utc(), "retained_sources_prelaunch": retained}
    (folder / "request.json").write_text(json.dumps(request, indent=2) + "\n")
    start = utc()
    timer = time.monotonic()
    process = subprocess.Popen(argv, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid = process.pid
    stdout, stderr = process.communicate()
    end = utc()
    (folder / "stdout.bin").write_bytes(stdout)
    (folder / "stderr.bin").write_bytes(stderr)
    result = {**request, "actual_PID": pid, "start_UTC": start, "end_UTC": end, "elapsed_seconds": time.monotonic()-timer, "exit_code": process.returncode, "stdout_bytes": len(stdout), "stdout_sha256": digest(stdout), "stderr_bytes": len(stderr), "stderr_sha256": digest(stderr), "stdout_path": str(folder / "stdout.bin"), "stderr_path": str(folder / "stderr.bin"), "launcher_claim": "Only this capture process is described; no upstream launcher/environment certification."}
    (folder / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    return result, stdout, stderr

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("label")
    parser.add_argument("argv", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = args.argv[1:] if args.argv and args.argv[0] == "--" else args.argv
    result, _, _ = capture(args.label, argv)
    print(json.dumps(result, indent=2))
