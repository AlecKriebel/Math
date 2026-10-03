"""Capture only this review's own private controls/custody scripts."""
import datetime as dt,hashlib,json,os,subprocess,sys,traceback
from pathlib import Path
F=Path(__file__).absolute().parent;R=F.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def dump(p,x):
    with p.open('x') as h:json.dump(x,h,indent=2,sort_keys=True);h.write('\n');h.flush();os.fsync(h.fileno())
def main():
    filename,capture=sys.argv[1:];assert filename in {'private_controls.py','verify_custody.py','verify_closed_inputs.py'} and capture and '/' not in capture
    script=F/filename;body=script.read_bytes();op=Path(__file__).read_bytes();dest=F/capture;dest.mkdir()
    (dest/'PRELAUNCH_SOURCE.py').write_bytes(body);(dest/'PRELAUNCH_OPERATOR.py').write_bytes(op)
    record={'schema':'pr48-v3-fresh-adversary-actual-private-capture/v1','argv':['/usr/bin/python3','-B',str(script)],'cwd':str(R),'operator_pid':os.getpid(),'started_utc':now(),'source_sha256':sha(body),'operator_sha256':sha(op),'actual_execution':False,'completed':False,'pid':None,'exit_code':None,'stdin_supplied':False,'production_imported_compiled_executed':False}
    out=b'';err=b''
    try:
        child=subprocess.Popen(record['argv'],cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        record.update(actual_execution=True,pid=child.pid);out,err=child.communicate(timeout=60);record.update(completed=True,exit_code=child.returncode)
    except BaseException:
        if 'child' in locals() and child.poll() is None:child.kill();out,err=child.communicate()
        record['operator_failure']=traceback.format_exc()
    for channel,raw in [('stdout',out),('stderr',err)]:
        (dest/(channel+'.bin')).write_bytes(raw);record[channel]={'path':channel+'.bin','bytes':len(raw),'sha256':sha(raw)}
    record.update(finished_utc=now(),source_unchanged=script.read_bytes()==body,operator_unchanged=Path(__file__).read_bytes()==op)
    dump(dest/'CAPTURE.json',record);print(json.dumps(record,sort_keys=True))
    return 0 if record['completed'] and record['exit_code']==0 and record['source_unchanged'] and record['operator_unchanged'] and 'operator_failure' not in record else 1
if __name__=='__main__':sys.exit(main())
