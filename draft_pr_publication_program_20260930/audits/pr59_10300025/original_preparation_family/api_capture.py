#!/usr/bin/env python3
"""Capture one public read-only gh API request. No checker execution."""
import datetime, hashlib, json, os, pathlib, subprocess, sys

root = pathlib.Path(__file__).resolve().parent
name, endpoint = sys.argv[1:]
if not name.replace('_', '').isalnum() or not endpoint.startswith('repos/AlecKriebel/Math/'):
    raise SystemExit('invalid capture arguments')
prefix = root / 'receipts' / name
if any(prefix.with_suffix(s).exists() for s in ('.stdout', '.stderr', '.json')):
    raise SystemExit('capture collision')
utc = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
started = utc()
proc = subprocess.Popen(['gh', 'api', endpoint], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = proc.communicate()
ended = utc()
prefix.with_suffix('.stdout').write_bytes(out)
prefix.with_suffix('.stderr').write_bytes(err)
record = {'operator':'SOURCE subagent /root/algebra_reproduction_audit', 'capture_pid':os.getpid(),
          'child_pid':proc.pid, 'started_utc':started, 'ended_utc':ended,
          'argv':['gh','api',endpoint], 'returncode':proc.returncode,
          'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
          'stdout':{'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},
          'stderr':{'bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}}
prefix.with_suffix('.json').write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record))
if proc.returncode: raise SystemExit(proc.returncode)
