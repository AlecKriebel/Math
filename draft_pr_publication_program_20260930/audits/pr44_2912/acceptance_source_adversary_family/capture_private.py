"""Capture only this adversary's own handwritten reviewer or closure; retain failures."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import traceback
H=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def main():
    if len(sys.argv)!=3 or sys.argv[1] not in {'REVIEW_ACTUAL_CAPTURE','REVIEW_ACTUAL_CAPTURE_V2','CLOSURE_ACTUAL_CAPTURE'} or sys.argv[2] not in {'independent_review.py','close_review.py'}:raise ValueError('Only owned source-review/closure allowed')
    dest=H/sys.argv[1];dest.mkdir(exist_ok=False)
    source=H/sys.argv[2];raw=source.read_bytes();operator=Path(__file__).read_bytes()
    (dest/'PRELAUNCH_SOURCE.py').write_bytes(raw);(dest/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
    pre={'schema':'pr44-source-adversary-prelaunch/v1','operator_pid':os.getpid(),'utc':utc(),'argv':['/usr/bin/python3','-B',str(source)],'cwd':str(H),'stdin_supplied':False,'source_sha256':sha(raw),'operator_sha256':sha(operator),'production_execution_authorized':False}
    (dest/'PRELAUNCH.json').write_text(json.dumps(pre,sort_keys=True,indent=2)+'\n')
    rec={'schema':'pr44-source-adversary-actual-capture/v1','prelaunch':pre,'started_utc':utc(),'actual_execution':False,'completed':False,'pid':None,'operator_pid':os.getpid()};out=err=b''
    try:
        proc=subprocess.Popen(pre['argv'],cwd=H,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);rec.update(pid=proc.pid,actual_execution=True);out,err=proc.communicate();rec.update(completed=True,exit_code=proc.returncode)
    except BaseException:rec['operator_error']=traceback.format_exc()
    rec.update(finished_utc=utc(),source_unchanged=source.read_bytes()==raw,operator_unchanged=Path(__file__).read_bytes()==operator)
    for k,b in [('stdout',out),('stderr',err)]:
        with (dest/(k+'.bin')).open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
        rec[k]={'path':k+'.bin','bytes':len(b),'sha256':sha(b)}
    rec['status']='PASS' if rec['completed'] is True and rec.get('exit_code')==0 and rec['source_unchanged'] and rec['operator_unchanged'] and 'operator_error' not in rec else 'FAIL'
    with (dest/'CAPTURE.json').open('x') as f:json.dump(rec,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    if sys.argv[2]=='close_review.py' and rec['status']=='PASS':
        import stat
        rows=[];dirs=[]
        for p in sorted(H.rglob('*')):
            if p.is_symlink() or not(p.is_file() or p.is_dir()):raise ValueError('Unsafe private closure')
            n=p.relative_to(H).as_posix()
            if p.is_dir():dirs.append(n)
            else:
                b=p.read_bytes();rows.append({'path':n,'bytes':len(b),'sha256':sha(b)})
        with (H/'SELF_MANIFEST.json').open('x') as f:json.dump({'schema':'pr44-acceptance-source-adversary-self-only-closure/v1','utc':utc(),'operator_pid':os.getpid(),'files_count':len(rows),'files':rows,'directories':dirs,'self_excluded':['SELF_MANIFEST.json'],'full_permission_mode':'0444','foreign_inputs_manifest':'INDIVIDUAL_INPUTS.json','foreign_bodies_copied':False,'production_imported_compiled_executed':False,'future_acceptance_approved':False},f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        for p in H.rglob('*'):
            if p.is_file():p.chmod(0o444)
        for p in H.rglob('*'):
            if p.is_file() and stat.S_IMODE(p.stat().st_mode)!=0o444:raise ValueError('Full0444 failed')
        for z in rows:
            b=(H/z['path']).read_bytes()
            if len(b)!=z['bytes'] or sha(b)!=z['sha256']:raise ValueError('Owned member changed during closure')
        rec['outer_return_only_manifest_sha256']=sha((H/'SELF_MANIFEST.json').read_bytes());rec['outer_return_only_members']=len(rows)
    print(json.dumps(rec,sort_keys=True))
    return 0 if rec['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
