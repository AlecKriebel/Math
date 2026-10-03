"""Lean local process capture, writes only within this family.

Usage: python3 -B capture_run.py LABEL PYTHON SCRIPT [args...]
True process PID/time and full streams; does not infer ROOT acceptance.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

base=Path(__file__).resolve().parent
label,python,script,*args=sys.argv[1:]
if not label.replace('_','').isalnum():
    raise SystemExit('invalid label')
def desc(path):
    p=Path(path).resolve(); b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':oct(p.stat().st_mode & 0o7777)}
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
script=Path(script).resolve()
sources=[script]
if script.name=='verify.py':
    sources.append(script.with_name('CANDIDATE.md'))
before=[desc(p) for p in sources]
cmd=[str(Path(python).absolute()),'-B',str(script),*args]
started=utc()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
child=subprocess.Popen(cmd,cwd=base,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
stdout,stderr=child.communicate()
finished=utc()
for suffix,data in [('stdout.bin',stdout),('stderr.bin',stderr)]:
    (base/(label+'.'+suffix)).write_bytes(data)
after=[desc(p) for p in sources]
meta={'schema':'pr57-family-local-capture/v1','operator':'endpoint_analytic_adversary','capture_process_pid':os.getpid(),'executed_child_pid':child.pid,'started_utc':started,'finished_utc':finished,'command':cmd,'cwd':str(base),'exit_code':child.returncode,'sources_before':before,'sources_after':after,'source_bytes_unchanged':before==after,'full_stdout':desc(base/(label+'.stdout.bin')),'full_stderr':desc(base/(label+'.stderr.bin')),'ROOT_or_mathematical_acceptance':False}
(base/(label+'.CAPTURE.json')).write_text(json.dumps(meta,indent=2,sort_keys=True)+'\n')
print(json.dumps({'child_pid':child.pid,'exit_code':child.returncode,'stdout_bytes':len(stdout),'stderr_bytes':len(stderr),'capture':label+'.CAPTURE.json'}))
raise SystemExit(child.returncode)
