#!/usr/bin/env python3
"""Subprocess receipts with actual start/finish, stdout/stderr bytes and hashes."""
import datetime,hashlib,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
label=sys.argv[1]
command=sys.argv[2:]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(command,cwd=HERE,capture_output=True)
end=datetime.datetime.now(datetime.timezone.utc).isoformat()
(HERE/'journals').mkdir(exist_ok=True)
paths={}
for kind,data in [('stdout',r.stdout),('stderr',r.stderr)]:
 p=HERE/'journals'/f'{label}.{kind}.txt';p.write_bytes(data)
 paths[kind]={'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
record={'label':label,'command':command,'cwd':str(HERE),'started_utc':start,'completed_utc':end,
        'returncode':r.returncode,'outputs':paths,'python_executable':sys.executable,
        'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'journals'/f'{label}.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,sort_keys=True))
