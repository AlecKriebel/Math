"""Own captured child for first-party private models; never production runtime."""
from pathlib import Path
import datetime as dt,hashlib,json,os,stat,subprocess,sys
P=Path(__file__).absolute().parent;A=P.parent;R=A.parents[2]
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,b):
 with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def ref(p):b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
def encode(v):return (json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
def main():
 os.umask(0o022);d=P/'PRIVATE_TIME_CONTROL_ACTUAL_CAPTURE';d.mkdir();s=P/'private_mode_controls.py';sb=s.read_bytes();op=Path(__file__).read_bytes();argv=['/usr/bin/python3','-B',str(s)];put(d/'PRELAUNCH_SOURCE.py',sb);put(d/'PRELAUNCH_OPERATOR.py',op);pre=dict(schema='pr48-V6-first-party-private-prelaunch/v1',argv=argv,cwd=str(P),stdin_supplied=False,source=ref(s),operator=ref(Path(__file__)),created_utc=now());put(d/'PRELAUNCH.json',encode(pre));start=now();child=subprocess.Popen(argv,cwd=P,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate();finish=now();put(d/'stdout.bin',out);put(d/'stderr.bin',err);cap=dict(schema='pr48-V6-first-party-private-actual-capture/v1',prelaunch=pre,actual_execution=True,completed=True,pid=child.pid,exit_code=child.returncode,started_utc=start,finished_utc=finish,source_unchanged=s.read_bytes()==sb,operator_unchanged=Path(__file__).read_bytes()==op,stdout=ref(d/'stdout.bin'),stderr=ref(d/'stderr.bin'),production_executed=False);put(d/'CAPTURE.json',encode(cap))
 if child.returncode!=0 or err or not cap['source_unchanged'] or not cap['operator_unchanged']:raise ValueError('Private failure retained')
 result=json.loads(out);put(P/'PRIVATE_MODE_CONTROL_RESULTS.json',encode(dict(schema='pr48-V6-private-actual-time-model-results/v1',actual_capture=ref(d/'CAPTURE.json'),entire_child_result=result,proposed_or_production_imported_compiled_executed=False)));print(json.dumps(dict(status='PASS_PRIVATE_MODELS_ONLY',pid=child.pid,assertions=result['assertions'],capture=ref(d/'CAPTURE.json'))))
if __name__=='__main__':main()
