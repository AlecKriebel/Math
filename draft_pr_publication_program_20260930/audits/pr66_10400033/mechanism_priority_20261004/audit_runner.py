#!/usr/bin/env python3
"""Execute argv without a shell and preserve exact streams and child identity."""
import datetime, hashlib, json, os, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
    if len(sys.argv) < 4 or sys.argv[2] != "--":
        raise SystemExit("usage: audit_runner.py LABEL -- ARGV...")
    label, argv = sys.argv[1], sys.argv[3:]
    dest = ROOT / "commands" / label
    dest.mkdir(parents=True, exist_ok=False)
    start = utc()
    proc = subprocess.Popen(argv, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    initial = {"label": label, "argv": argv, "pid": proc.pid, "cwd": os.getcwd(), "started_utc": start, "runner_pid": os.getpid(), "runner_argv": getattr(sys, "orig_argv", sys.argv)}
    (dest / "record.json").write_text(json.dumps(initial, indent=2) + "\n")
    out, err = proc.communicate()
    (dest / "stdout.bin").write_bytes(out)
    (dest / "stderr.bin").write_bytes(err)
    initial.update({"ended_utc": utc(), "exit_status": proc.returncode, "stdout_bytes": len(out), "stderr_bytes": len(err), "stdout_sha256": hashlib.sha256(out).hexdigest(), "stderr_sha256": hashlib.sha256(err).hexdigest()})
    (dest / "record.json").write_text(json.dumps(initial, indent=2) + "\n")
    sys.stdout.buffer.write(out)
    sys.stderr.buffer.write(err)
    print(json.dumps({"record": str(dest / "record.json"), "pid": proc.pid, "exit_status": proc.returncode}), file=sys.stderr)
    return proc.returncode

if __name__ == "__main__":
    raise SystemExit(main())
