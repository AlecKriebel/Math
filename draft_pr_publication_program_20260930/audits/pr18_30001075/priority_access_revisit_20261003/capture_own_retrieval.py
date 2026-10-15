from pathlib import Path
import datetime as dt, hashlib, json, os, subprocess, sys
P=Path(__file__).absolute().parent
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,b):
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def main():
    inp,out,cap=sys.argv[1:];d=P/cap;d.mkdir();source=(P/'fetch_public_routes.py').read_bytes();put(d/'PRELAUNCH_SOURCE.py',source)
    argv=['/usr/bin/python3','-E','-B',str(P/'fetch_public_routes.py'),inp,out]
    z=dict(schema='pr18-own-public-route-child-capture/v1',operator_pid=os.getpid(),argv=argv,cwd=str(P),source_sha256=sha(source),input_sha256=sha((P/inp).read_bytes()),started_utc=utc(),actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False)
    put(d/'PRELAUNCH.json',(json.dumps(z,indent=2)+'\n').encode())
    child=subprocess.Popen(argv,cwd=P,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);z.update(actual_execution=True,pid=child.pid);a,b=child.communicate();z.update(completed=True,exit_code=child.returncode,finished_utc=utc(),source_unchanged=source==(P/'fetch_public_routes.py').read_bytes(),status='PASS_CHILD' if child.returncode==0 else 'FAIL_CHILD')
    for n,body in [('stdout',a),('stderr',b)]:put(d/(n+'.bin'),body);z[n]=dict(path=n+'.bin',bytes=len(body),sha256=sha(body))
    put(d/'CAPTURE.json',(json.dumps(z,indent=2)+'\n').encode());print(json.dumps(z,indent=2))
if __name__=='__main__':main()
