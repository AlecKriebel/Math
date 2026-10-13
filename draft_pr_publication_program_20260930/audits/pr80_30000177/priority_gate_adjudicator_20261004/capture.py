#!/usr/bin/env python3
"""Capture actual child process streams/status with prelaunch byte pins."""
import argparse, datetime, hashlib, json, os, pathlib, shutil, subprocess, sys
p=argparse.ArgumentParser();p.add_argument('label');p.add_argument('--pin',action='append',default=[]);p.add_argument('command',nargs=argparse.REMAINDER);a=p.parse_args()
cmd=a.command
if cmd and cmd[0]=='--':cmd=cmd[1:]
root=pathlib.Path(__file__).resolve().parent;out=root/'process_evidence'/a.label;out.mkdir(parents=True,exist_ok=False)
def pin(path):
    q=pathlib.Path(path).resolve();b=q.read_bytes();return {'path':str(q),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
paths=[str(pathlib.Path(__file__).resolve())]+a.pin
exe=shutil.which(cmd[0]) if cmd else None
if exe:paths.append(exe)
req={'utc_before_launch':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':cmd,'cwd':os.getcwd(),'launcher_pid':os.getpid(),'prelaunch_pins':[pin(q) for q in dict.fromkeys(paths)]}
(out/'request.json').write_text(json.dumps(req,indent=2)+'\n')
for n,q in enumerate(dict.fromkeys(paths)):
    if str(q).endswith('.py'):shutil.copyfile(q,out/f'{n}_{pathlib.Path(q).name}')
with (out/'stdout.bin').open('wb') as so,(out/'stderr.bin').open('wb') as se:
    try:child=subprocess.Popen(cmd,stdout=so,stderr=se)
    except Exception as e:
        (out/'launch_failure.json').write_text(json.dumps({'child_launched':False,'error_type':type(e).__name__,'error':str(e)},indent=2)+'\n')
        raise
    pid=child.pid
    (out/'child_launch.json').write_text(json.dumps({'child_pid':pid,'utc_launched':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n')
    rc=child.wait()
res={'child_pid':pid,'child_exit_code':rc,'utc_completed':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout':pin(out/'stdout.bin'),'stderr':pin(out/'stderr.bin')}
(out/'result.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'label':a.label,**res},indent=2))
sys.exit(0 if rc==0 else 1)
