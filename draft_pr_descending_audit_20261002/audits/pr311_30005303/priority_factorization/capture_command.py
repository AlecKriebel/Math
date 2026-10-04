#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import json, subprocess, sys, hashlib
args=sys.argv[1:]
if len(args)<3 or args[1]!='--':
    raise SystemExit('Usage: capture_command.py NAME -- COMMAND [ARG ...]')
name=args[0]; command=args[2:]
base=Path(__file__).resolve().parent
started=datetime.now(timezone.utc).isoformat(timespec='microseconds')
r=subprocess.run(command,cwd=base,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
ended=datetime.now(timezone.utc).isoformat(timespec='microseconds')
obj={'started_actual_utc':started,'ended_actual_utc':ended,'cwd':str(base),'argv':command,'exit_code':r.returncode,'stdout_utf8':r.stdout.decode('utf-8',errors='replace'),'stderr_utf8':r.stderr.decode('utf-8',errors='replace'),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()}
(base/'command_captures'/f'{name}.json').write_text(json.dumps(obj,indent=2)+'\n')
print(obj['stdout_utf8'],end='')
print(obj['stderr_utf8'],end='',file=sys.stderr)
print(json.dumps({'capture':name,'started_actual_utc':started,'ended_actual_utc':ended,'exit_code':r.returncode}),file=sys.stderr)
raise SystemExit(r.returncode)
