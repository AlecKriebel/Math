"""Real final own inspection capture, then exact first-party self-only closure."""
from pathlib import Path,PurePosixPath
import datetime,hashlib,json,os,stat,subprocess,sys
D=Path(__file__).absolute().parent
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
worker=D/'final_inspect_worker.py';capture=D/'FINAL_INSPECTION_TIME_PRECISION_ACTUAL_CAPTURE';capture.mkdir()
src=worker.read_bytes();op=Path(__file__).read_bytes();(capture/'PRELAUNCH_SOURCE.py').write_bytes(src);(capture/'PRELAUNCH_OPERATOR.py').write_bytes(op)
argv=['/usr/bin/python3','-B',str(worker)]
c={'schema':'pr44-own-final-inspection-actual-capture/v1','operator_pid':os.getpid(),'argv':argv,'cwd':str(D),'started_utc':now(),'source_sha256':sha(src),'operator_sha256':sha(op),'stdin_supplied':False,'actual_execution':False,'completed':False,'pid':None,'exit_code':None};dump(capture/'PRELAUNCH.json',c)
with (capture/'stdout.bin').open('xb') as out,(capture/'stderr.bin').open('xb') as err:
    p=subprocess.Popen(argv,cwd=D,stdin=subprocess.DEVNULL,stdout=out,stderr=err);c.update(pid=p.pid,actual_execution=True);c['exit_code']=p.wait(timeout=60);c['completed']=True
c['finished_utc']=now();c['source_unchanged']=worker.read_bytes()==src;c['operator_unchanged']=Path(__file__).read_bytes()==op
for k in ['stdout','stderr']:
    q=capture/(k+'.bin');b=q.read_bytes();c[k]={'path':q.name,'bytes':len(b),'sha256':sha(b)}
c['status']='PASS_OWN_FINAL_INSPECTION' if c['exit_code']==0 and c['source_unchanged'] and c['operator_unchanged'] else 'FAILED_OWN_FINAL_INSPECTION_PRESERVED';dump(capture/'CAPTURE.json',c)
if c['exit_code']!=0:print(json.dumps(c));sys.exit(1)
files=[];dirs=[]
for p in sorted(D.rglob('*')):
    if p.is_symlink():raise ValueError('Symlink cannot close')
    n=p.relative_to(D).as_posix()
    if p.is_dir():dirs.append(n)
    elif p.is_file():
        if n=='SELF_MANIFEST.json':raise ValueError('Already closed')
        b=p.read_bytes();files.append({'path':n,'bytes':len(b),'sha256':sha(b)})
    else:raise ValueError('Special member')
expected={q.as_posix() for f in files for q in PurePosixPath(f['path']).parents if q.as_posix()!='.'}
if expected!=set(dirs):raise ValueError('Extra empty directory')
mf={'schema':'pr44-whole-current-source-first-self-only-closure/v1','utc':now(),'operator_pid':os.getpid(),'files_count':len(files),'files':files,'directories':dirs,'self_excluded':['SELF_MANIFEST.json'],'full_permission_mode':'0444','foreign_inputs_manifest':'INDIVIDUAL_INPUTS.json','foreign_primary_or_raw_cache_bodies_copied':False,'whole_native4_Git_stdout_is_procedural_actual_evidence':True,'candidate_manifest_sha256':'169f2825a8f730735627bdc33a43366c05e317fdf7ec4df4cd96a31e37329eb0','original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'future_ROOT_acceptance_or_reconciliation_approved':False}
dump(D/'SELF_MANIFEST.json',mf)
for p in D.rglob('*'):
    if p.is_file():p.chmod(0o444)
for row in files:
    p=D/row['path'];b=p.read_bytes()
    if len(b)!=row['bytes'] or sha(b)!=row['sha256'] or stat.S_IMODE(p.stat().st_mode)!=0o444:raise ValueError('Closure mismatch')
if stat.S_IMODE((D/'SELF_MANIFEST.json').stat().st_mode)!=0o444:raise ValueError('Manifest full0444 mismatch')
print(json.dumps({'status':'CLOSED_OWN_WHOLE_CURRENT_SOURCE_FIRST_AUDIT','files_count':len(files),'manifest_sha256':sha((D/'SELF_MANIFEST.json').read_bytes()),'actual_inspection_pid':c['pid'],'current_whole_acceptance_approved':False}))
