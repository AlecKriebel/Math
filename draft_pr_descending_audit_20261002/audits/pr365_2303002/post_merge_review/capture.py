#!/usr/bin/env python3
"""Lossless postmerge command capture; only this open review is written."""
import datetime,gzip,hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent;PRIVATE=ROOT/'private';PRIVATE.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def run(name,argv,cwd='/Users/alec/Documents/Math',expected_exit=0):
    assert not (PRIVATE/(name+'.json')).exists(),name
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1',PYTHONDONTWRITEBYTECODE='1')
    start=now();p=subprocess.run(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    rec=dict(name=name,argv=argv,cwd=str(cwd),environment_changes={k:env[k] for k in ['GIT_OPTIONAL_LOCKS','GIT_NO_LAZY_FETCH','PYTHONDONTWRITEBYTECODE']},started_utc=start,finished_utc=now(),exit_code=p.returncode,expected_exit=expected_exit,streams={})
    for stream,b in [('stdout',p.stdout),('stderr',p.stderr)]:
        z=gzip.compress(b,mtime=0);path=PRIVATE/(name+'.'+stream+'.gz');path.write_bytes(z)
        rec['streams'][stream]=dict(path=path.relative_to(ROOT).as_posix(),stored_bytes=len(z),stored_sha256=sha(z),logical_bytes=len(b),logical_sha256=sha(b))
    (PRIVATE/(name+'.json')).write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps(rec))
    return p
if __name__=='__main__':
    args=sys.argv[1:];display=args[0]=='--display'
    if display:args=args[1:]
    name,cwd,*argv=args;p=run(name,argv,cwd)
    if display:
        sys.stdout.buffer.write(p.stdout);sys.stderr.buffer.write(p.stderr)
    raise SystemExit(p.returncode)
