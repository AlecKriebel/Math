"""Capture the one authorized immutable recovery process without retry."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,signal,stat,subprocess,sys
R=Path('/Users/alec/Documents/Math');W=Path(__file__).parent;S=R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def require(v,m):
 if not v:raise RuntimeError(m+'; no automatic retry')
def main():
 require(not sys.flags.optimize,'optimization');p=W/'push_verified_existing_commit.py';c=W/'ROOT_RECOVERY_CLEARANCE.json';clear=json.loads(c.read_bytes());control=json.loads(S.read_bytes())
 require(pin(p)['sha256']=='a8ad4e0a9e42c8b9a6619eabd55b65b8bb969f25de8376a5a3f5aa66fca05fbc' and pin(p)['mode']==0o444 and pin(c)['sha256']=='efa0a07df2aa5d5d2e726888eba03c1cf6dc348dcd36b37148177fb7793efc7d' and pin(c)['mode']==0o444,'exact immutable ROOT-approved recovery')
 lease=control['descending_302_checkpoint037_push_recovery_lease'];require(lease['active'] and lease['operator']==pin(p) and lease['clearance']==pin(c) and lease['push_only'] and not control['descending_302_publication_checkpoint_lease']['active'],'fresh replacement push-only lease')
 out=W/'actual_recovery_outer';out.mkdir(exist_ok=False);archives=[]
 for i,q in enumerate([Path(__file__),p,c,S,*[Path(x['path']) for x in clear['bound_inputs']]]):
  b=q.read_bytes();copy=out/(str(i)+'_'+q.name+'.gz');copy.write_bytes(gzip.compress(b,mtime=0));require(gzip.decompress(copy.read_bytes())==b,'complete prelaunch archive');archives.append(dict(source=pin(q),stored=pin(copy)))
 argv=['/opt/homebrew/bin/python3','-E','-B',str(p)];request=dict(argv=argv,cwd=str(R),requested_UTC=utc(),actual_launcher_PID=os.getpid(),automatic_retry=False,full_prelaunch_inputs=archives)
 (out/'request.json').write_text(json.dumps(request,indent=2)+'\n');proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
 started=dict(**request,actual_PID=proc.pid,cooperative_process_group=proc.pid,start_UTC=utc());(out/'started.json').write_text(json.dumps(started,indent=2)+'\n');timed=False;failure=None
 try:stdout,stderr=proc.communicate(timeout=180)
 except subprocess.TimeoutExpired:
  timed=True;os.killpg(proc.pid,signal.SIGKILL);stdout,stderr=proc.communicate(timeout=10)
 except BaseException as error:
  failure=repr(error)
  try:os.killpg(proc.pid,signal.SIGKILL)
  except ProcessLookupError:pass
  stdout,stderr=proc.communicate(timeout=10)
 streams={}
 for name,b in [('stdout',stdout),('stderr',stderr)]:
  q=out/(name+'.gz');q.write_bytes(gzip.compress(b,mtime=0));require(gzip.decompress(q.read_bytes())==b,'complete outer stream');streams[name]=dict(stored=pin(q),logical_bytes=len(b),logical_sha256=sha(b))
 completed=dict(**started,end_UTC=utc(),exit_code=proc.returncode,timed_out=timed,exception_after_Popen=failure,parent_reaped=True,full_capture_complete=True,streams=streams)
 (out/'execution.json').write_text(json.dumps(completed,indent=2)+'\n');require(not timed and failure is None and proc.returncode==0,'actual separate recovery failed or uncertain; preserve and reconcile read-only')
 receipt=json.loads(stdout);require(receipt['status']=='PASS_EXISTING_CHECKPOINT037_COMMIT_VERIFIED_AND_PUSH_COMPLETED_BY_SEPARATE_RECOVERY' and receipt['actual_RECOVERY_recorder_PID']==proc.pid and receipt['original_operator_exit_code']==1 and not stderr,'actual truthful recovery result')
 print(json.dumps(dict(status=receipt['status'],actual_launcher_PID=os.getpid(),actual_recovery_PID=proc.pid,exit_code=proc.returncode,original_operator_exit_code=1,commit=receipt['existing_commit'],execution=pin(out/'execution.json')),indent=2))
if __name__=='__main__':main()
