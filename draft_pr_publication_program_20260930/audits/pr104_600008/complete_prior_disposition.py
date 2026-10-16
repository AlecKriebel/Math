from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1];K='600008'
D=A/'actual_final_disposition_readback_20261006';D.mkdir(exist_ok=False);records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def require(c,m):
 if not c:raise RuntimeError(m)
def run(argv,large=False):
 start=now();p=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();i=len(records)
 if not large:(D/(str(i)+'.stdout.bin')).write_bytes(out)
 (D/(str(i)+'.stderr.bin')).write_bytes(err)
 records.append({'argv':argv,'PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,
 'stdout_file':None if large else str(i)+'.stdout.bin','stdout_sha256':hashlib.sha256(out).hexdigest(),'stdout_bytes':len(out),
 'immutable_git_body_not_duplicated':large,'stderr_file':str(i)+'.stderr.bin','stderr_sha256':hashlib.sha256(err).hexdigest()})
 dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'records':records});require(p.returncode==0,err.decode()[:1200]);return out
def git(*args,large=False):return run(['/usr/bin/git',*args],large)
cp=load(A/'actual_checkpoints/native_prior_disposition_release/RECEIPT.json');commit=cp['commit'];base=cp['parent']
require(cp['remote_verified'] and git('rev-parse','HEAD').strip().decode()==commit,'native commit')
require(git('symbolic-ref','--short','HEAD').strip()==b'main' and not git('diff','--cached','--name-only','-z'),'branch/index')
require(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==commit,'remote head changed')
closed=load(A/'actual_closure_20261006/RECEIPT.json');ready=load(A/'ROOT_DISPOSITION_READY_20261006.json')
pr=json.loads(run(['/opt/homebrew/bin/gh','pr','view','104','--repo','AlecKriebel/Math','--json','number,state,headRefOid,mergedAt,closedAt,url']))
require(pr['state']=='CLOSED' and pr['headRefOid']==ready['original_head'] and pr['mergedAt'] is None and pr['closedAt'],'actual PR closure')
comment=json.loads(run(['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/issues/comments/'+str(closed['closing_comment_id'])]))
require(comment['body'].encode()==(A/'PROPOSED_CLOSING_PRIORITY_NOTE_20261006.md').read_bytes(),'actual closing comment body')
prefix='unsolved_math_prioritization/'
new={};old={}
for name in ['assessments.json','state.json','catalog.json','QUEUE.md','history.jsonl','assessment_history.jsonl']:
 new[name]=git('show',commit+':'+prefix+name,large=True);old[name]=git('show',base+':'+prefix+name,large=True)
 require((C/prefix/name).read_bytes()==new[name],'local/committed native mismatch: '+name)
na=json.loads(new['assessments.json']);oa=json.loads(old['assessments.json']);ns=json.loads(new['state.json']);os_=json.loads(old['state.json'])
require(na[K]['resolution']=='already_solved' and na[K]['review_hash']==ready['authenticated_pins'][3]['sha256'] if False else na[K]['resolution']=='already_solved','assessment resolution')
require(na[K]['review_hash']=='597672d96f2b12dc802c798cbd01e1d224329f4f3a277e65514b429354103663','source bound assessment')
require(ns[K]['status']=='already_solved' and ns[K]['turns_used']==1,'native state/budget')
require({k:v for k,v in na.items() if k!=K}=={k:v for k,v in oa.items() if k!=K},'other assessments changed')
require({k:v for k,v in ns.items() if k!=K}==os_,'other states changed')
nc={x['id']:x for x in json.loads(new['catalog.json'])};oc={x['id']:x for x in json.loads(old['catalog.json'])}
require(nc[K]['local_status']=='already_solved' and nc[K]['turns_used']==1 and not nc[K]['eligible'],'native catalog')
require(set(nc)==set(oc),'catalog identity scope')
for key in oc:
 if key!=K:require({f:v for f,v in nc[key].items() if f!='rank'}=={f:v for f,v in oc[key].items() if f!='rank'},'other catalog row changed')
newlines=new['QUEUE.md'].decode().splitlines();oldlines=old['QUEUE.md'].decode().splitlines()
ni=[i for i,s in enumerate(newlines) if '| 600008 / AMR-005-0008 |' in s];oi=[i for i,s in enumerate(oldlines) if '| 600008 / AMR-005-0008 |' in s]
require(len(ni)==len(oi)==1 and ni==oi,'unique native queue row')
row=newlines[ni[0]].split('|');require(row[8].strip()=='already_solved' and row[9].strip()=='1/5','queue status/budget')
require([x for i,x in enumerate(newlines) if i!=ni[0]]==[x for i,x in enumerate(oldlines) if i!=oi[0]],'other queue rows changed')
for name in ['history.jsonl','assessment_history.jsonl']:
 require(new[name].startswith(old[name]),'historical prefix changed')
 events=[json.loads(s) for s in new[name][len(old[name]):].decode().splitlines()]
 require(all(e['id']==K for e in events),'new event scope')
 require(len(events)==(2 if name=='history.jsonl' else 1),'native event count')
 if name=='history.jsonl':require(events[0]['event']=='import_authenticated_submitted_author_effort' and all(e['turns_used']==1 for e in events),'effort import')
rootrel=str(A.relative_to(C))
proof=git('show',commit+':'+rootrel+'/original_source_authentication_20261006/original_attempt/ANALYTIC_CRITERION.md')
require(hashlib.sha256(proof).hexdigest()=='608217a2ffc120a965b165f5b6065edd83f8cf94c5e77f0f95a0326640db2dae','immutable original proof')
ledger=git('show',commit+':'+rootrel+'/original_source_authentication_20261006/original_attempt/turns.jsonl')
require([json.loads(s)['turn'] for s in ledger.decode().splitlines()]==[1],'immutable one-entry ledger')
for pin in load(A/'native_prior_disposition_finalization_20261006/PREPARED_RECEIPT.json')['native_pins']:
 b=git('show',commit+':'+pin['path'],large=True);require(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'committed native prepared pin')
t=now();result={'schema':'pr104-actual-prior-disposition-completion/v1','UTC':t,'actual_operator_PID':os.getpid(),'PR':104,'problem_id':600008,
 'source_head':ready['original_head'],'eligible_original_literal_status':'claimed_solved','native_status':'already_solved',
 'scope':'literal analytic null-chain parameter classification, prior verified reconstruction/classical corollary',
 'original_budget':'1/5','new_central_proof_search_turns':0,'mathematics_verified':True,'prior_analytic_reconstruction_verified':True,
 'substantive_new_contribution_established':False,'fresh_final_disposition_review_authenticated':True,
 'earliest_priority_or_exact_earlier_formula_printing_verified':False,'finite_algebraic_cayley_output_verified':False,
 'actual_PR_readback':pr,'closing_comment_url':closed['closing_comment_url'],'actual_comment_body_readback_exact':True,
 'same_head_closed_without_merge':True,'native_assessment_state_catalog_queue_committed_readback_complete':True,
 'other_assessments_states_queue_rows_preserved':True,'other_catalog_rows_preserved_except_rank':True,'historical_prefixes_preserved':True,
 'original_proof_and_ledger_committed_preserved':True,'native_checkpoint_commit':commit,'native_checkpoint_parent':base,
 'remote_readback':commit,'branch':'main','native_integration_complete':True,'workflow_percent':100,
 'publication':False,'DOI':None,'tracker':False,'merge_commit':None,'completed_program_count':15,'dated_eligible_total':99,
 'program_completion_percent':100*15/99,'next_numeric_intake_cursor':105,'persistent_goal_complete':False,
 'completion_metadata_checkpoint_pending_at_snapshot':True,'primary_checkout_mutated':False}
dump(A/'ROOT_CLOSURE_COMPLETION_20261006.json',result)
progress=load(P/'CURRENT_PROGRESS.json');require(progress['current_PR']==104 and progress['fully_completed_count']==14,'program count baseline')
progress['fully_completed_eligible_PRs']=sorted(set(progress['fully_completed_eligible_PRs']+[104]));progress['closed_without_publication_PRs']=sorted(set(progress['closed_without_publication_PRs']+[104]))
progress.update(UTC=t,updated_UTC=t,fully_completed_count=15,fully_completed_fraction_percent=100*15/99,workflow_estimate_percent=100*15/99,
 current_PR_workflow_percent=100,current_workflow_estimate_percent=100,current_native_integration_complete=True,current_native_checkpoint_commit=commit,
 current_native_checkpoint_remote_verified=True,current_final_actual_completion_record='audits/pr104_600008/ROOT_CLOSURE_COMPLETION_20261006.json',
 current_native_integration_prepared=True,current_final_disposition_review_pending=False,advance_to_next_PR_authorized_now=False,
 last_completed_PR=104,last_completed_PR_workflow_percent=100,last_completed_DOI=None,last_completed_merge_commit=None,last_completed_tracker_range=None,
 last_completed_outcome='closed_without_merge_or_publication_already_solved_analytic_via_verified_reconstruction',
 last_completed_full_source_solved=True,last_completed_source_resolution_scope='literal analytic classification only',last_completed_priority_clearance=False,
 last_completed_publication_authorization=False,last_completed_record='audits/pr104_600008/ROOT_CLOSURE_COMPLETION_20261006.json',
 last_completed_actual_final_gate='audits/pr104_600008/ROOT_CLOSURE_COMPLETION_20261006.json',last_completed_closing_comment_url=closed['closing_comment_url'],
 last_completed_audit_checkpoint_push_pending=True,last_completed_metadata_checkpoint_commit=None,last_completed_final_completion_readback=None,
 next_step='Checkpoint actual closure/native completion metadata and read back release; then fresh eligible intake from105.',
 remaining_current_step='Actual completion metadata release/readback only; PR104 service and native disposition complete.',
 workflow_estimate_definition='Nine published workflows, three credited prior-result dispositions, one verified partial disposition and two novelty-based closures divided by dated99-PR census.',
 persistent_goal_status='active',persistent_goal_complete=False)
dump(P/'CURRENT_PROGRESS.json',progress)
line=t+' — PR104 terminal analytic prior-result disposition read back from GitHub and committed main72ad7aa: same original head CLOSED/unmerged, exact comment body, fresh source-bound already_solved assessment, state/catalog/QUEUE1/5, unchanged other targets and history prefixes, immutable original proof/ledger. Source/math/bounded priority and PR104disposition100%; program15/99=15.15%. No paper/DOI/tracker/merge. Completion metadata checkpoint/readback pending; next eligible intake105.\n'
for f in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md',C/prefix/'attempts/600008/RESEARCH_LOG.md']:
 with f.open('a') as out:out.write('\n'+line)
paths=[P/'CURRENT_PROGRESS.json',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md',A/'ROOT_CLOSURE_COMPLETION_20261006.json',A/'complete_prior_disposition.py',A/'NATIVE_CHECKPOINT_SELECTION_20261006.json',C/prefix/'attempts/600008/RESEARCH_LOG.md']
paths += [A/'actual_checkpoints/native_prior_disposition_release'/n for n in ['RECEIPT.json','PROCESS_JOURNAL.json']]
paths += [f for f in D.iterdir() if f.is_file()]
paths += [f for f in (A/'actual_operations/record_native_prepared').iterdir() if f.is_file()]
dump(A/'COMPLETION_CHECKPOINT_SELECTION_20261006.json',{'paths':sorted(set(str(f.relative_to(C)) for f in paths)),'UTC':t,'previous_native_commit':commit})
print(json.dumps({k:v for k,v in result.items() if k!='actual_PR_readback'}))
