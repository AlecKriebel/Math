#!/usr/bin/env python3
import sys, subprocess, json, os, hashlib
from pathlib import Path
from datetime import datetime, timezone
root=Path(__file__).resolve().parent
name=sys.argv[1]; argv=sys.argv[2:]
started=datetime.now(timezone.utc).isoformat()
try:
 proc=subprocess.Popen(argv,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 stdout,stderr=proc.communicate(); child_pid=proc.pid; exitcode=proc.returncode
except OSError as e:
 stdout=b'';stderr=(repr(e)+'\n').encode(); child_pid=None;exitcode=127
base=root/'processes'/name
base.with_suffix('.stdout').write_bytes(stdout)
base.with_suffix('.stderr').write_bytes(stderr)
record={'name':name,'argv':argv,'cwd':str(root),'operator_PID':os.getpid(),'child_PID':child_pid,'UTC_started':started,'UTC_finished':datetime.now(timezone.utc).isoformat(),'exit':exitcode,'stdout_bytes':len(stdout),'stderr_bytes':len(stderr),'stdout_sha256':hashlib.sha256(stdout).hexdigest(),'stderr_sha256':hashlib.sha256(stderr).hexdigest(),'inputs':[]}
for arg in argv:
 q=Path(arg)
 if q.is_file():
  b=q.read_bytes();record['inputs'].append({'path':str(q.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
base.with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2));print(stdout.decode(errors='replace'));print(stderr.decode(errors='replace'),file=sys.stderr)
sys.exit(exitcode)
