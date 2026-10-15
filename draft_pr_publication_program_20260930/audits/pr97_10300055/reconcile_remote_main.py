"""Advance only the private main after a pre-staging concurrent-head rejection."""
from pathlib import Path
import subprocess,json,datetime,hashlib,os
A=Path(__file__).resolve().parent;C=A.parents[2];D=A/'remote_main_reconciliation_20261005';D.mkdir(exist_ok=False);records=[]
def require(ok,message):
    if not ok:raise RuntimeError(message)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def run(args,allow_missing=False):
    start=now();p=subprocess.Popen(['/usr/bin/git',*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();i=len(records)
    for name,b in [('stdout',out),('stderr',err)]:(D/(str(i)+'.'+name+'.bin')).write_bytes(b)
    records.append({'argv':['/usr/bin/git',*args],'PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest(),'stdout_file':str(i)+'.stdout.bin','stderr_file':str(i)+'.stderr.bin'})
    (D/'PROCESS_JOURNAL.json').write_text(json.dumps({'actual_operator_PID':os.getpid(),'records':records},indent=2)+'\n')
    require(p.returncode==0 or allow_missing,err.decode()[:1000]);return p.returncode,out
def git(*a):return run(list(a))[1]
old=git('rev-parse','HEAD').strip().decode();require(old=='c8cb7a1f627567b6ed6c44e80fcdcf4db7e511ea','unexpected local head')
require(git('symbolic-ref','--short','HEAD').strip()==b'main' and not git('diff','--cached','--name-only','-z'),'private main/index')
queue=C/'unsolved_math_prioritization/QUEUE.md';require(queue.read_bytes()==git('show',old+':unsolved_math_prioritization/QUEUE.md'),'foreign queue worktree edits')
git('fetch','--no-tags','https://github.com/AlecKriebel/Math.git','main');new=git('rev-parse','FETCH_HEAD').strip().decode();git('merge-base','--is-ancestor',old,new)
selected=json.loads((A/'SOURCE_GATE_SELECTION.json').read_text())['paths']
for rel in selected:
    status_old,_=run(['cat-file','-e',old+':'+rel],True);status_new,_=run(['cat-file','-e',new+':'+rel],True)
    require(bool(status_old)==bool(status_new),'selected path concurrently introduced/deleted '+rel)
    if status_old==0:require(git('rev-parse',old+':'+rel)==git('rev-parse',new+':'+rel),'selected path concurrently changed '+rel)
new_queue=git('show',new+':unsolved_math_prioritization/QUEUE.md');git('reset','--mixed','--quiet',new);queue.write_bytes(new_queue)
x={'schema':'pr97-private-main-concurrent-head-reconciliation/v1','UTC':now(),'actual_operator_PID':os.getpid(),'old':old,'new':new,'old_is_ancestor':True,'selected_paths_unchanged_in_remote_delta':True,'index_was_empty':True,'primary_checkout_mutated':False,'complete_queue_synced_from_authenticated_new_main':True,'failed_checkpoint_stopped_before_staging':True}
(D/'RECEIPT.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x))
