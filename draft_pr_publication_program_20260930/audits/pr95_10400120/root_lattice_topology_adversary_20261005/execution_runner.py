#!/usr/bin/env python3
"""Capture an actual subprocess execution without replacing its streams."""
import datetime, hashlib, json, os, pathlib, subprocess, sys

root = pathlib.Path(__file__).resolve().parent
out = root / 'executions'
out.mkdir(exist_ok=True)
label = sys.argv[1]
argv = sys.argv[2:]
if not argv:
    raise SystemExit('expected label and executable argv')
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
input_paths = [root/'execution_runner.py']
input_paths.extend((pathlib.Path(a) if pathlib.Path(a).is_absolute() else root/a) for a in argv if a.endswith(('.py','.pdf','.txt','.md','.json')) and (pathlib.Path(a) if pathlib.Path(a).is_absolute() else root/a).is_file())
input_hashes = {str(p.resolve()): hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths}
proc = subprocess.Popen(argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = proc.communicate()
ended = datetime.datetime.now(datetime.timezone.utc).isoformat()
(out / (label+'.stdout')).write_bytes(stdout)
(out / (label+'.stderr')).write_bytes(stderr)
record = dict(label=label, runner_pid=os.getpid(), pid=proc.pid, argv=argv, cwd=str(root), started_utc=stamp, ended_utc=ended, exit_code=proc.returncode, stdout_path=label+'.stdout', stderr_path=label+'.stderr', stdout_sha256=hashlib.sha256(stdout).hexdigest(), stderr_sha256=hashlib.sha256(stderr).hexdigest(), input_sha256_at_execution=input_hashes)
(out / (label+'.json')).write_text(json.dumps(record, indent=2)+'\n')
sys.stdout.buffer.write(stdout)
sys.stderr.buffer.write(stderr)
raise SystemExit(proc.returncode)
