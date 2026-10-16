#!/usr/bin/env python3
"""Capture final writing/readonly calls entirely outside the closed namespace."""
import datetime,gzip,hashlib,json,os,pathlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parent;D=R.parent/'root_replay_private/post_merge_tests';D.mkdir(parents=True,exist_ok=True)
name,classification,*argv=sys.argv[1:];assert classification in ['writing','readonly'];assert not (D/(name+'.json')).exists()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1');start=now()
p=subprocess.run(argv,cwd='/Users/alec/Documents/Math',env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
rec=dict(name=name,classification=classification,argv=argv,cwd='/Users/alec/Documents/Math',started_utc=start,finished_utc=now(),exit_code=p.returncode,streams={})
for s,b in [('stdout',p.stdout),('stderr',p.stderr)]:
    z=gzip.compress(b,mtime=0);q=D/(name+'.'+s+'.gz');q.write_bytes(z)
    rec['streams'][s]=dict(path=str(q),stored_bytes=len(z),stored_sha256=sha(z),logical_bytes=len(b),logical_sha256=sha(b))
(D/(name+'.json')).write_text(json.dumps(rec,indent=2)+'\n')
sys.stdout.buffer.write(p.stdout);sys.stderr.buffer.write(p.stderr);print(json.dumps(rec));raise SystemExit(p.returncode)
