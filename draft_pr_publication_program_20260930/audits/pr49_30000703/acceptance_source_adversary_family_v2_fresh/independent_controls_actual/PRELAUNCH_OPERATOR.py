"""Own actual private-child capture. Never executes production acceptance sources."""
from pathlib import Path
import datetime as dt,hashlib,json,os,subprocess,sys
F=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def dump(p,v):p.write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
name,filename,*tail=sys.argv[1:]
assert name and '/' not in name and name not in {'.','..'}
source=F/filename
assert source.parent==F and source.is_file() and not source.is_symlink()
assert filename in {'private_controls.py','check_custody.py'}
dest=F/name;dest.mkdir()
body=source.read_bytes();operator=Path(__file__).read_bytes()
(dest/'PRELAUNCH_SOURCE.py').write_bytes(body)
(dest/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
argv=['/usr/bin/python3','-B',str(source),*tail]
pre=dict(argv=argv,cwd=str(F),stdin_supplied=False,created_utc=utc(),source_sha256=sha(body),operator_sha256=sha(operator))
dump(dest/'PRELAUNCH.json',pre)
started=utc();proc=subprocess.Popen(argv,cwd=F,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err=proc.communicate();finished=utc()
rec=dict(schema='pr49-independent-private-actual-capture/v1',prelaunch=pre,argv=argv,cwd=str(F),pid=proc.pid,actual_execution=True,completed=True,stdin_supplied=False,started_utc=started,finished_utc=finished,exit_code=proc.returncode,source_sha256=sha(body),operator_sha256=sha(operator),source_unchanged=source.read_bytes()==body,operator_unchanged=Path(__file__).read_bytes()==operator)
for key,raw in [('stdout',out),('stderr',err)]:
    path=dest/(key+'.bin')
    with path.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    rec[key]=dict(path=path.name,bytes=len(raw),sha256=sha(raw))
rec['status']='PASS' if proc.returncode==0 and not err and rec['source_unchanged'] and rec['operator_unchanged'] else 'FAIL'
dump(dest/'CAPTURE.json',rec)
print(json.dumps(rec,sort_keys=True,indent=2))
sys.exit(0 if rec['status']=='PASS' else 1)
