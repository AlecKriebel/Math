#!/usr/bin/env python3
"""Capture actual process identity, UTC span, complete streams, and source hash."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys

name=sys.argv[1]
argv=sys.argv[2:]
root=Path(__file__).resolve().parent
out=root/'processes'
started=datetime.now(timezone.utc).isoformat()
child=subprocess.Popen(argv,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stdout,stderr=child.communicate()
finished=datetime.now(timezone.utc).isoformat()
(out/(name+'.stdout')).write_bytes(stdout)
(out/(name+'.stderr')).write_bytes(stderr)
inputs=[]
for arg in argv:
    p=Path(arg)
    if not p.is_absolute(): p=root/p
    if p.is_file():
        b=p.read_bytes()
        inputs.append({'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
record={'argv':argv,'cwd':str(root),'operator_PID':os.getpid(),'child_PID':child.pid,
        'UTC_started':started,'UTC_finished':finished,'exit':child.returncode,
        'stdout_bytes':len(stdout),'stderr_bytes':len(stderr),
        'stdout_sha256':hashlib.sha256(stdout).hexdigest(),
        'stderr_sha256':hashlib.sha256(stderr).hexdigest(),'inputs':inputs}
(out/(name+'.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
print(stdout.decode(errors='replace'))
if stderr: print(stderr.decode(errors='replace'),file=sys.stderr)
sys.exit(child.returncode)
