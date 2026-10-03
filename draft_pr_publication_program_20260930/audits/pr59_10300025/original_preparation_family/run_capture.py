#!/usr/bin/env python3
"""Capture own local preparation runs, with actual process identities."""
import datetime, hashlib, json, os, pathlib, subprocess, sys
root=pathlib.Path(__file__).resolve().parent
label,script,*args=sys.argv[1:]
assert label.replace('_','').isalnum() and '/' not in script and script.endswith('.py')
prefix=root/'receipts'/label
assert not any(prefix.with_suffix(s).exists() for s in ('.stdout','.stderr','.json'))
source=root/script; utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
argv=[sys.executable,'-B',str(source),*args]; started=utc()
p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=root)
out,err=p.communicate(); ended=utc()
prefix.with_suffix('.stdout').write_bytes(out); prefix.with_suffix('.stderr').write_bytes(err)
r={'operator':'SOURCE subagent /root/algebra_reproduction_audit','capture_pid':os.getpid(),
   'child_pid':p.pid,'started_utc':started,'ended_utc':ended,'argv':argv,'returncode':p.returncode,
   'capture_source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
   'child_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
   'stdout':{'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},
   'stderr':{'bytes':len(err),'sha256':hashlib.sha256(err).hexdigest()}}
prefix.with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
raise SystemExit(p.returncode)
