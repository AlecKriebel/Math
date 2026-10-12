#!/usr/bin/env python3
"""Actual child execution receipt; no reused output directory."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
base = Path(__file__).resolve().parent
name, *argv = sys.argv[1:]
dest = base / 'private' / 'commands' / name
dest.mkdir(parents=True, exist_ok=False)
source = Path(argv[-1])
if source.suffix == '.py' and source.is_file():
    (dest / 'prelaunch_child.py').write_bytes(source.read_bytes())
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
child = subprocess.Popen(argv, cwd=base, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = child.communicate()
ended = datetime.datetime.now(datetime.timezone.utc).isoformat()
(dest / 'stdout.bin').write_bytes(stdout)
(dest / 'stderr.bin').write_bytes(stderr)
receipt = {'argv': argv, 'cwd': str(base), 'operator_pid': os.getpid(), 'child_pid': child.pid,
 'started_utc': started, 'finished_utc': ended, 'exit_code': child.returncode,
 'completed': True, 'stdout': {'bytes':len(stdout), 'sha256':hashlib.sha256(stdout).hexdigest()},
 'stderr': {'bytes':len(stderr), 'sha256':hashlib.sha256(stderr).hexdigest()},
 'prelaunch_child_source_saved': (dest / 'prelaunch_child.py').is_file()}
(dest / 'CAPTURE.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt,indent=2))
print(stdout.decode('utf-8','replace'))
if stderr: print(stderr.decode('utf-8','replace'),file=sys.stderr)
raise SystemExit(child.returncode)
