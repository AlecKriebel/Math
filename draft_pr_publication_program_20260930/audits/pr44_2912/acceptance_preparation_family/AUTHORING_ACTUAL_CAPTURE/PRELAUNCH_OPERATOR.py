"""Launch only this family's authoring, handwritten controls, or closure; retain actual evidence."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import traceback

H = Path(__file__).resolve().parent
R = H.parents[3]
def sha(b): return hashlib.sha256(b).hexdigest()
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
def main():
    name, script_name = sys.argv[1:3]
    if len(sys.argv) != 3 or name in {'.','..'} or '/' in name or script_name not in {'author_sources.py','independent_controls.py','close_source.py'}:
        raise ValueError('Only named source-authoring/private-control/closure operations allowed')
    source = H / script_name
    dest = H / name
    dest.mkdir(mode=0o700, exist_ok=False)
    raw, operator = source.read_bytes(), Path(__file__).read_bytes()
    (dest/'PRELAUNCH_SOURCE.py').write_bytes(raw)
    (dest/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
    pre = {'schema':'pr44-owned-source-prelaunch/v1','operator_pid':os.getpid(),'utc':utc(),'source':script_name,'source_bytes':len(raw),'source_sha256':sha(raw),'operator_sha256':sha(operator),'argv':['/usr/bin/python3','-B',str(source)],'cwd':str(H),'stdin_supplied':False,'production_operations_authorized':False}
    (dest/'PRELAUNCH.json').write_text(json.dumps(pre,indent=2)+'\n')
    rec = {'schema':'pr44-owned-source-actual-capture/v1','operator_pid':os.getpid(),'prelaunch':pre,'actual_execution':False,'pid':None,'completed':False,'exit_code':None,'started_utc':utc()}
    out, err = b'', b''
    try:
        child = subprocess.Popen(pre['argv'],cwd=H,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        rec.update(actual_execution=True,pid=child.pid)
        out,err = child.communicate()
        rec.update(completed=True,exit_code=child.returncode)
    except BaseException:
        rec['operator_error']=traceback.format_exc()
    rec['finished_utc']=utc()
    for n,b in [('stdout.bin',out),('stderr.bin',err)]:
        with (dest/n).open('xb') as stream:
            stream.write(b);stream.flush();os.fsync(stream.fileno())
        rec[n[:-4]]={'path':n,'bytes':len(b),'sha256':sha(b)}
    rec['source_unchanged']=source.read_bytes()==raw
    rec['operator_unchanged']=Path(__file__).read_bytes()==operator
    rec['status']='PASS' if rec['completed'] is True and type(rec['exit_code']) is int and rec['exit_code']==0 and rec['source_unchanged'] and rec['operator_unchanged'] and 'operator_error' not in rec else 'FAIL'
    (dest/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps(rec,sort_keys=True))
    return 0 if rec['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
