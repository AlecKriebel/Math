"""ROOT independent full recovery custody and fresh read-only endpoint check."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,os,stat,subprocess,sys
R=Path('/Users/alec/Documents/Math');P=R/'draft_pr_descending_audit_20261002';W=Path(__file__).parent;S=P/'SHARED_GIT_WINDOW_STATUS.json';V=W/'actual_recovery_outer';D=W/'actual_push_recovery'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat();load=lambda p:json.loads(Path(p).read_bytes())
def require(v,m):
 if not v:raise RuntimeError(m)
def pin(p):
 p=Path(p);require(p.is_file() and not p.is_symlink(),'literal artifact');b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=stat.S_IMODE(p.stat().st_mode))
def body(x):
 require(pin(x['path'])==x,'entire stored artifact');return Path(x['path']).read_bytes()
def streams(e):
 out={}
 for n in ['stdout','stderr']:
  x=e[n];z=Path(x['path']).read_bytes();b=gzip.decompress(z);require(len(z)==x['stored_bytes'] and sha(z)==x['stored_sha256'] and len(b)==x['logical_bytes'] and sha(b)==x['logical_sha256'],'entire inner stored/logical stream');out[n]=b
 return out
def main():
 require(not sys.flags.optimize,'optimization');x=load(V/'execution.json');q=load(V/'request.json');start=load(V/'started.json')
 require(all(x[k]==v for k,v in q.items()) and all(x[k]==v for k,v in start.items()) and x['actual_PID']==39981 and x['actual_launcher_PID']==39980 and x['exit_code']==0 and not x['timed_out'] and x['exception_after_Popen'] is None and x['parent_reaped'] and x['full_capture_complete'],'complete genuine outer recovery')
 for y in x['full_prelaunch_inputs']:
  b=gzip.decompress(body(y['stored']));require(len(b)==y['source']['bytes'] and sha(b)==y['source']['sha256'],'full immutable prelaunch source/input/control body, historical control epoch')
 outer={}
 for n in ['stdout','stderr']:
  y=x['streams'][n];b=gzip.decompress(body(y['stored']));require(len(b)==y['logical_bytes'] and sha(b)==y['logical_sha256'],'entire outer stream');outer[n]=b
 require(not outer['stderr'],'outer recovery stderr');receipt=load(P/'checkpoint_302_publication_037_recovery_receipt.json');require(json.loads(outer['stdout'])==receipt and receipt['actual_RECOVERY_recorder_PID']==39981 and receipt['original_operator_exit_code']==1 and receipt['original_outer_OS_PID'] is None and receipt['original_failure_is_not_reclassified'],'truthful old failure and separate actual recovery result')
 recorded={int(p.name.split('_')[0]) for p in D.glob('*_execution.json')};require(recorded==set(range(1,len(recorded)+1)) and len(recorded)>740,'nonempty complete numeric recovery captures');captures=[];push=[]
 source=pin(W/'push_verified_existing_commit.py')
 for i in sorted(recorded):
  e=load(D/f'{i}_execution.json');request=load(D/f'{i}_request.json');started=load(D/f'{i}_started.json')
  require(all(e[k]==v for k,v in request.items()) and all(e[k]==v for k,v in started.items()) and e['actual_PID']==e['cooperative_process_group'] and type(e['actual_PID']) is int and e['actual_PID']>0,'every inner actual native request/start/completion/PID')
  require(e['operator']==source and e['cwd']==str(R) and e['automatic_retry'] is False and e['full_stream_capture_complete'] and e['parent_reaped'] and not e['timeout_cleanup_required'] and datetime.fromisoformat(e['start_UTC'])<=datetime.fromisoformat(e['end_UTC']),'whole reviewed source/capture/outcome/time')
  require(e['exit_code']==(1 if i==1 else 0),'all zero children except one permitted empty config search');b=streams(e)
  if i==1:require(e['argv'][2:]==['config','--get-regexp','^url[.]'] and not b['stdout'] and not b['stderr'],'permitted config no-match')
  if e['argv'][2]=='push':push.append(dict(number=i,actual_PID=e['actual_PID'],argv=e['argv'],execution=pin(D/f'{i}_execution.json'),complete_stdout=b['stdout'].decode(),complete_stderr=b['stderr'].decode()))
  require(e['argv'][2] not in ['add','commit','merge','fetch','checkout','reset','switch'],'no repeated checkpoint or native mutation');captures.append(dict(number=i,actual_PID=e['actual_PID'],exit_code=e['exit_code'],execution=pin(D/f'{i}_execution.json'),stdout=e['stdout'],stderr=e['stderr']))
 expected=['/usr/bin/git','--no-optional-locks','push','--force-with-lease=refs/heads/main:2669042ac964d5710972af552df141f7934588af','https://github.com/AlecKriebel/Math.git','0a49d5e66a0fb9d4f78c7f3a7f3b30cd77196567:refs/heads/main']
 require(len(push)==1 and push[0]['argv']==expected,'exact one sole unperformed expected-old descendant push')
 originalbasis=load(W/'PRESERVED_FAILED_BASIS.json')
 for y in originalbasis['files']:require(pin(y['path'])==y,'all4289failed source/capture artifacts remain untouched')
 controls=load(S);require(controls['descending_302_checkpoint037_push_recovery_lease']['completed'] and not controls['descending_302_checkpoint037_push_recovery_lease']['active'] and not controls['descending_302_publication_checkpoint_lease']['active'] and controls['descending_302_publication_checkpoint_lease']['original_operator_completed_successfully'] is False and not controls['shared_git_writes_paused'] and not controls['ascending_pr85_publication_integration_window_granted'],'truthful actual scope closure and still no peer85 grant')
 cap=W/'root_actual_recovery_readback';cap.mkdir(exist_ok=False)
 def run(label,argv):
  q=cap/label;q.mkdir();request=dict(argv=argv,cwd=str(R),requested_UTC=utc(),ROOT_source=pin(__file__),automatic_retry=False);(q/'request.json').write_text(json.dumps(request,indent=2)+'\n');(q/'source.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(),mtime=0))
  proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);started=dict(**request,actual_PID=proc.pid,start_UTC=utc());(q/'started.json').write_text(json.dumps(started,indent=2)+'\n');out,err=proc.communicate(timeout=55);stored={}
  for n,b in [('stdout',out),('stderr',err)]:
   z=q/(n+'.gz');z.write_bytes(gzip.compress(b,mtime=0));stored[n]=dict(stored=pin(z),logical_bytes=len(b),logical_sha256=sha(b))
  (q/'execution.json').write_text(json.dumps(dict(**started,end_UTC=utc(),exit_code=proc.returncode,parent_reaped=True,streams=stored),indent=2)+'\n');require(proc.returncode==0 and not err,'fresh ROOT read-only result');return out
 require(run('branch',['/usr/bin/git','--no-optional-locks','branch','--show-current'])==b'main\n' and run('head',['/usr/bin/git','--no-optional-locks','rev-parse','HEAD']).decode().strip()==receipt['existing_commit'],'fresh actual main')
 require(run('remote',['/usr/bin/git','--no-optional-locks','ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main']).split()[0].decode()==receipt['existing_commit'],'fresh actual literal remote')
 require(not run('staged',['/usr/bin/git','--no-optional-locks','diff','--cached','--raw','-z']) and not (R/'.git/MERGE_HEAD').exists() and not (R/'.git/index.lock').exists(),'fresh empty index/no merge')
 result=dict(status='ROOT_ACCEPTS_ACTUAL_CHECKPOINT037_EXISTING_COMMIT_SEPARATE_PUSH_ONLY_RECOVERY',UTC=utc(),actual_ROOT_recorder_PID=os.getpid(),source=pin(__file__),actual_outer_execution=pin(V/'execution.json'),actual_recovery_PID=x['actual_PID'],actual_launcher_PID=x['actual_launcher_PID'],actual_recovery_exit_code=0,original_operator_exit_code=1,original_outer_OS_PID=None,original_failure_reclassified=False,full_outer_source_input_request_start_streams_authenticated=True,all_inner_native_captures_authenticated=captures,exact_one_push=push[0],all4289failed_evidence_bodies_modes_unchanged=True,receipt=pin(P/'checkpoint_302_publication_037_recovery_receipt.json'),truthful_closed_control=pin(S),fresh_main_equals_explicit_remote=True,index_empty=True,peer85_native_acceptance_checkpoint_remain_PENDING=True,no_native_PR_or_publication_or_tracker_action=True,estimates_percent=dict(publication_checkpoint=100,PR302_workflow=85))
 p=W/'ROOT_ACTUAL_RECOVERY_ACCEPTANCE.json'
 with p.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 p.chmod(0o444);print(json.dumps(dict(status=result['status'],actual_ROOT_recorder_PID=os.getpid(),actual_inner_captures=len(captures),push_child_PID=push[0]['actual_PID'],commit=receipt['existing_commit'],acceptance=pin(p)),indent=2))
if __name__=='__main__':main()
