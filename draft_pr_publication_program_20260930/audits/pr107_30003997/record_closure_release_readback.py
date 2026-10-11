from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1];D=A/'actual_completion_release_readback_20261006';D.mkdir(exist_ok=False);records=[]
def require(c,m):
 if not c:raise RuntimeError(m)
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def run(argv):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();i=len(records)
 for name,b in [('stdout',out),('stderr',err)]:(D/(str(i)+'.'+name+'.bin')).write_bytes(b)
 records.append({'argv':argv,'PID':p.pid,'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':p.returncode,'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest(),'stdout_file':str(i)+'.stdout.bin','stderr_file':str(i)+'.stderr.bin'})
 dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'records':records});require(p.returncode==0,err.decode()[:1000]);return out
cp=load(A/'actual_checkpoints/completion_release/RECEIPT.json');commit=cp['commit'];done=load(A/'ROOT_CLOSURE_COMPLETION_20261006.json')
require(cp['remote_verified'] and done['workflow_percent']==100 and done['completed_program_count']==16,'completion prerequisites')
require(run(['git','symbolic-ref','--short','HEAD']).strip()==b'main','branch');require(run(['git','rev-parse','HEAD']).strip().decode()==commit,'HEAD')
require(run(['git','ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main']).decode().split()[0]==commit,'remote advanced')
require(not run(['git','diff','--cached','--name-only','-z']),'foreign index')
progpath=P/'CURRENT_PROGRESS.json';prog=load(progpath)
committed=json.loads(run(['git','show',commit+':'+str(progpath.relative_to(C))]));require(committed==prog and prog['fully_completed_count']==16,'committed program metadata')
native_done=json.loads(run(['git','show',commit+':unsolved_math_prioritization/attempts/30003997/FINAL_DISPOSITION.json']));require(native_done==done,'committed actual native disposition')
t=datetime.datetime.now(datetime.timezone.utc).isoformat();out={'schema':'pr107-actual-completion-release-readback/v1','UTC':t,'actual_operator_PID':os.getpid(),'PR':107,'problem_id':30003997,'commit':commit,'native_commit':done['native_checkpoint_commit'],'remote_verified':True,'branch':'main','same_head_closed_without_merge':True,'human_PR107_disposition_resolved':True,'current_native_status':'already_solved','qualified_scope':'complete hardness bundle as elementary published-construction corollary; exact identity priority unresolved','workflow_percent':100,'original_budget':'1/5','extra_central_proof_search_turns':0,'completed_program_count':16,'dated_eligible_total':99,'program_completion_percent':100*16/99,'next_numeric_intake_cursor':108,'publication':False,'DOI':None,'tracker':False,'persistent_goal_complete':False,'primary_checkout_mutated':False,'this_late_receipt_to_be_checkpointed_with_next_intake':True}
dump(A/'ROOT_CLOSURE_RELEASE_ACTUAL_READBACK_20261006.json',out)
prog.update(UTC=t,updated_UTC=t,last_completed_metadata_checkpoint_commit=commit,last_completed_final_completion_readback='audits/pr107_30003997/ROOT_CLOSURE_RELEASE_ACTUAL_READBACK_20261006.json',last_completed_audit_checkpoint_push_pending=False,completion_metadata_checkpoint_pending_at_snapshot=False,advance_to_next_PR_authorized_now=True,next_step='Fresh status-only draft intake after PR107, starting108.',remaining_current_step='None; PR107 full disposition complete.',persistent_goal_status='active',persistent_goal_complete=False)
dump(progpath,prog)
line=t+' — PR107 completion metadata committed and actual remote/index readback verified. Full disposition100%; program16/99=16.16%; no merge or publication. Original1/5 preserved, newproofturns0. Next ordered claimed_solved-only status intake108 authorized; late release receipt will accompany next checkpoint.\n'
for p in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write('\n'+line)
print(json.dumps(out))
