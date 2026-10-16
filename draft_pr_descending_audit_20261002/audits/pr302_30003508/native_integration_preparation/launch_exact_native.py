"""Record the one separately ROOT-approved native process without retry."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,signal,stat,subprocess,sys
R=Path('/Users/alec/Documents/Math');N=Path(__file__).parent;S=R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def require(v,m):
 if not v:raise RuntimeError(m+'; no automatic retry')
def main():
 require(not sys.flags.optimize,'optimization');p=N/'integrate_pr302.py';c=N/'ROOT_NATIVE_INTEGRATION_CLEARANCE.json';planpath=N/'CONTENT_PLAN.json';clear=json.loads(c.read_bytes());plan=json.loads(planpath.read_bytes());control=json.loads(S.read_bytes())
 require(pin(p)['sha256']=='2dd3f08d52e68aed4b7a66ceea7092681e0f4e05fc5d9c7eb0c1df2757166003' and pin(planpath)['sha256']=='baea4aabf70a814f184826433ab0d62b7fc5dc8177cebaa9d80ed5d43fa6f97c' and pin(p)['mode']==pin(planpath)['mode']==pin(c)['mode']==0o444,'exact immutable source/plan/frozen ROOT approval')
 require(clear['status']=='PASS_EXACT_PR302_NATIVE_ORIGINAL_HEAD_AND_PRESENT_DAY_ACCEPTANCE' and clear['native_execution_authorized'] is True and clear['unresolved_issues']==[] and clear['operator']==pin(p) and clear['plan']==pin(planpath),'genuine ROOT exact native clearance')
 lease=control['descending_302_native_integration_lease'];require(lease['active'] and lease['git_authorized'] and lease['operator']==pin(p) and lease['plan']==pin(planpath) and lease['clearance']==pin(c) and not control['shared_git_writes_paused'] and not control['ascending_pr85_publication_integration_window_granted'],'exact live native scope')
 require(len(plan['bound_inputs'])==len({x['path'] for x in plan['bound_inputs']})==24,'all24nonvacuous role bindings')
 for x in plan['bound_inputs']:require(pin(x['path'])==x,'each current full approved input body/mode')
 out=N/'actual_native_outer';out.mkdir(exist_ok=False);archives=[]
 for i,q in enumerate(dict.fromkeys([Path(__file__),p,planpath,c,S,*[Path(x['path']) for x in plan['bound_inputs']]])):
  b=q.read_bytes();copy=out/(str(i)+'_'+q.name+'.gz');copy.write_bytes(gzip.compress(b,mtime=0));require(gzip.decompress(copy.read_bytes())==b,'complete prelaunch archive');archives.append(dict(source=pin(q),stored=pin(copy)))
 argv=['/opt/homebrew/bin/python3','-E','-B',str(p)];request=dict(argv=argv,cwd=str(R),requested_UTC=utc(),actual_launcher_PID=os.getpid(),automatic_retry=False,full_prelaunch_inputs=archives)
 (out/'request.json').write_text(json.dumps(request,indent=2)+'\n');proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);started=dict(**request,actual_PID=proc.pid,cooperative_process_group=proc.pid,start_UTC=utc());(out/'started.json').write_text(json.dumps(started,indent=2)+'\n');timed=False;failure=None
 try:stdout,stderr=proc.communicate(timeout=540)
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
 completed=dict(**started,end_UTC=utc(),exit_code=proc.returncode,timed_out=timed,exception_after_Popen=failure,parent_reaped=True,full_capture_complete=True,streams=streams);(out/'execution.json').write_text(json.dumps(completed,indent=2)+'\n');require(not timed and failure is None and proc.returncode==0,'actual native failed or uncertain; preserve and reconcile read-only')
 receipt=json.loads(stdout);require(receipt['status']=='PASS_PR302_EXACT_ORIGINAL_HEAD_NATIVE_MERGE_AND_PRESENT_DAY_ACCEPTANCE' and receipt['actual_ROOT_recorder_PID']==proc.pid and not stderr,'actual truthful native result')
 print(json.dumps(dict(status=receipt['status'],actual_launcher_PID=os.getpid(),actual_native_PID=proc.pid,exit_code=proc.returncode,merge=receipt['actual_merge'],execution=pin(out/'execution.json')),indent=2))
if __name__=='__main__':main()
