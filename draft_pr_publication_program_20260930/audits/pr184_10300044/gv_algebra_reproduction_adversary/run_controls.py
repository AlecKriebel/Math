#!/usr/bin/env python3
"""Run only isolated controls, recording argv, clocks, status, streams and hashes."""
from pathlib import Path
import subprocess, hashlib, datetime, json, sys
OWN=Path(__file__).resolve().parent

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(label,argv,bindings):
    start=datetime.datetime.now(datetime.timezone.utc)
    p=subprocess.run(argv,cwd=OWN,capture_output=True,text=True)
    end=datetime.datetime.now(datetime.timezone.utc)
    out=OWN/'receipts'/f'{label}.stdout.txt';err=OWN/'receipts'/f'{label}.stderr.txt'
    out.write_text(p.stdout);err.write_text(p.stderr)
    r={'label':label,'argv':argv,'cwd':str(OWN),'start_utc':start.isoformat(),'end_utc':end.isoformat(),'exit_code':p.returncode,'stdout_sha256':digest(out),'stderr_sha256':digest(err),'bindings':[{ 'path':str(Path(b).resolve()),'sha256':digest(b)} for b in bindings]}
    (OWN/'receipts'/f'{label}.json').write_text(json.dumps(r,indent=2,sort_keys=True))
    print(json.dumps({'label':label,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr},indent=2))
    return p.returncode
if __name__=='__main__':
    label=sys.argv[1];argv=sys.argv[2:]
    run(label,argv,[a for a in argv if Path(a).is_file()])
