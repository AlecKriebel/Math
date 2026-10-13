from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parents[1];K='30003997';D=A/'actual_final_disposition_readback_20261006';D.mkdir(exist_ok=False);records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def require(c,m):
 if not c:raise RuntimeError(m)
def run(argv,large=False):
 start=now();p=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();i=len(records)
 if not large:(D/(str(i)+'.stdout.bin')).write_bytes(out)
 (D/(str(i)+'.stderr.bin')).write_bytes(err)
 records.append({'argv':argv,'PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,'stdout_file':None if large else str(i)+'.stdout.bin','stdout_sha256':hashlib.sha256(out).hexdigest(),'stdout_bytes':len(out),'immutable_git_body_not_duplicated':large,'stderr_file':str(i)+'.stderr.bin','stderr_sha256':hashlib.sha256(err).hexdigest()})
 dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'records':records});require(p.returncode==0,err.decode()[:1200]);return out
def git(*args,large=False):return run(['/usr/bin/git',*args],large)
cp=load(A/'actual_checkpoints/native_prior_disposition_release/RECEIPT.json');commit=cp['commit'];base=cp['parent']
require(cp['remote_verified'] and git('rev-parse','HEAD').strip().decode()==commit,'native commit')
require(git('symbolic-ref','--short','HEAD').strip()==b'main' and not git('diff','--cached','--name-only','-z'),'branch/index')
require(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==commit,'remote head advanced')
ready=load(A/'ROOT_DISPOSITION_READY_20261006.json');closed=load(A/'actual_closure_20261006/RECEIPT.json')
pr=json.loads(run(['/opt/homebrew/bin/gh','pr','view','107','--repo','AlecKriebel/Math','--json','number,state,headRefOid,mergedAt,closedAt,url']))
require(pr['state']=='CLOSED' and pr['headRefOid']==ready['original_head'] and pr['mergedAt'] is None and pr['closedAt'],'actual PR closure')
comment=json.loads(run(['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/issues/comments/'+str(closed['closing_comment_id'])]))
require(comment['body'].encode()==(A/'PROPOSED_CLOSURE_COMMENT_20261006.md').read_bytes(),'actual public closing body')
prefix='unsolved_math_prioritization/';new={};old={}
for name in ['assessments.json','state.json','catalog.json','QUEUE.md','history.jsonl','assessment_history.jsonl']:
 new[name]=git('show',commit+':'+prefix+name,large=True);old[name]=git('show',base+':'+prefix+name,large=True)
 require((C/prefix/name).read_bytes()==new[name],'local/committed native mismatch: '+name)
na=json.loads(new['assessments.json']);oa=json.loads(old['assessments.json']);ns=json.loads(new['state.json']);oldstate=json.loads(old['state.json'])
require(na[K]['resolution']=='already_solved' and na[K]['review_hash']=='806c5596635c33619f1a907f0c98bf4762c7cbe77ad8cb384b50d50659e80359','source-bound native assessment')
require(ns[K]['status']=='already_solved' and ns[K]['turns_used']==1,'native status/budget')
require({k:v for k,v in na.items() if k!=K}=={k:v for k,v in oa.items() if k!=K},'other assessments changed')
require({k:v for k,v in ns.items() if k!=K}==oldstate,'other states changed')
nc={x['id']:x for x in json.loads(new['catalog.json'])};oc={x['id']:x for x in json.loads(old['catalog.json'])};require(set(nc)==set(oc),'catalog identities')
require(nc[K]['local_status']=='already_solved' and nc[K]['turns_used']==1 and not nc[K]['eligible'],'native catalog')
for key in oc:
 if key!=K:require({f:v for f,v in nc[key].items() if f!='rank'}=={f:v for f,v in oc[key].items() if f!='rank'},'other catalog semantics changed')
nlines=new['QUEUE.md'].decode().splitlines();olines=old['QUEUE.md'].decode().splitlines();ni=[i for i,s in enumerate(nlines) if '| 30003997 / OWR-16633-014 |' in s];oi=[i for i,s in enumerate(olines) if '| 30003997 / OWR-16633-014 |' in s]
require(len(ni)==len(oi)==1 and ni==oi,'unique campaign row');cells=nlines[ni[0]].split('|');require(cells[8].strip()=='already_solved' and cells[9].strip()=='1/5','campaign status/budget')
require([s for i,s in enumerate(nlines) if i!=ni[0]]==[s for i,s in enumerate(olines) if i!=oi[0]],'other campaign rows changed')
for name in ['history.jsonl','assessment_history.jsonl']:
 require(new[name].startswith(old[name]),'historical prefix changed');events=[json.loads(s) for s in new[name][len(old[name]):].decode().splitlines()]
 require(len(events)==(2 if name=='history.jsonl' else 1) and all(x['id']==K for x in events),'new event scope')
 if name=='history.jsonl':require(events[0]['event']=='import_authenticated_submitted_author_effort' and all(x['turns_used']==1 for x in events),'original effort import')
rootrel=str(A.relative_to(C));proof=git('show',commit+':'+rootrel+'/original_source_authentication_20261006/original_attempt/PROOF.md');ledger=git('show',commit+':'+rootrel+'/original_source_authentication_20261006/original_attempt/turns.jsonl')
require(hashlib.sha256(proof).hexdigest()=='2c219bf80ad4bbba75f8c70169b26b7e9b11b6f5e1742543f25d9cb0d0c5ebe8','immutable original proof')
require([json.loads(s)['turn'] for s in ledger.decode().splitlines()]==[1],'original one-entry ledger')
effective=git('show',commit+':'+rootrel+'/repaired_diagnostics_v2/PROOF.md');require(hashlib.sha256(effective).hexdigest()=='27968a88187710ac83fc68c96cfda1edbdeda1eae6fc7da80929f4def6477436','current effective proof')
prepared=load(A/'native_prior_disposition_20261006/PREPARED_RECEIPT.json')
for pin in prepared['native_pins']:
 b=git('show',commit+':'+pin['path'],large=True);require(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'committed prepared pin')
t=now();result={'schema':'pr107-actual-prior-disposition-completion/v1','UTC':t,'actual_operator_PID':os.getpid(),'PR':107,'problem_id':30003997,'source_head':ready['original_head'],'eligible_original_literal_status':'claimed_solved','native_status':'already_solved','scope':'literal destination-cost hardness and full advertised restriction bundle as elementary published-construction corollary','original_budget':'1/5','new_central_proof_search_turns':0,'mathematics_verified':True,'complete_restricted_prior_corollary_verified':True,'substantive_new_contribution_established':False,'exact_optimum_identity_verified':True,'exact_optimum_identity_priority':'unresolved','earliest_priority_or_verbatim_cost_table_printing_verified':False,'fresh_final_disposition_review_authenticated':True,'actual_PR_readback':pr,'closing_comment_url':closed['closing_comment_url'],'actual_comment_body_readback_exact':True,'same_head_closed_without_merge':True,'native_assessment_state_catalog_queue_committed_readback_complete':True,'other_assessments_states_queue_rows_preserved':True,'other_catalog_rows_preserved_except_rank':True,'historical_prefixes_preserved':True,'original_proof_and_ledger_committed_preserved':True,'current_effective_proof_committed_preserved':True,'native_checkpoint_commit':commit,'native_checkpoint_parent':base,'remote_readback':commit,'branch':'main','native_integration_complete':True,'workflow_percent':100,'publication':False,'DOI':None,'tracker':False,'merge_commit':None,'completed_program_count':16,'dated_eligible_total':99,'program_completion_percent':100*16/99,'next_numeric_intake_cursor':108,'persistent_goal_complete':False,'completion_metadata_checkpoint_pending_at_snapshot':True,'primary_checkout_mutated':False}
dump(A/'ROOT_CLOSURE_COMPLETION_20261006.json',result)
prog=load(P/'CURRENT_PROGRESS.json');require(prog['current_PR']==107 and prog['fully_completed_count']==15,'program baseline');prog['fully_completed_eligible_PRs']=sorted(set(prog['fully_completed_eligible_PRs']+[107]));prog['closed_without_publication_PRs']=sorted(set(prog['closed_without_publication_PRs']+[107]))
prog.update(UTC=t,updated_UTC=t,fully_completed_count=16,fully_completed_fraction_percent=100*16/99,workflow_estimate_percent=100*16/99,current_PR_workflow_percent=100,current_workflow_estimate_percent=100,current_native_integration_complete=True,current_native_checkpoint_commit=commit,current_native_checkpoint_remote_verified=True,current_final_actual_completion_record='audits/pr107_30003997/ROOT_CLOSURE_COMPLETION_20261006.json',advance_to_next_PR_authorized_now=False,last_completed_PR=107,last_completed_PR_workflow_percent=100,last_completed_DOI=None,last_completed_merge_commit=None,last_completed_tracker_range=None,last_completed_outcome='closed_without_merge_or_publication_already_solved_as_published_hardness_corollary',last_completed_full_source_solved=True,last_completed_source_resolution_scope='literal source hardness and all advertised restrictions; prior construction corollary',last_completed_priority_clearance=False,last_completed_publication_authorization=False,last_completed_record='audits/pr107_30003997/ROOT_CLOSURE_COMPLETION_20261006.json',last_completed_actual_final_gate='audits/pr107_30003997/ROOT_CLOSURE_COMPLETION_20261006.json',last_completed_closing_comment_url=closed['closing_comment_url'],last_completed_audit_checkpoint_push_pending=True,last_completed_metadata_checkpoint_commit=None,last_completed_final_completion_readback=None,next_numeric_intake_cursor=108,next_step='Release/read back completion metadata; then status-only ordered intake from108.',remaining_current_step='Actual completion metadata release/readback only.',workflow_estimate_definition='Nine published workflows, three credited prior-result dispositions, one verified partial disposition and three novelty-based closures divided by dated99-PR census.',persistent_goal_status='active',persistent_goal_complete=False)
dump(P/'CURRENT_PROGRESS.json',prog);N=C/prefix/'attempts'/K;dump(N/'FINAL_DISPOSITION.json',result)
line=t+' — PR107 terminal disposition independently read back: same original head CLOSED/unmerged, exact comment, committed source-bound native already_solved assessment/state/catalog/QUEUE1/5, other targets and historical prefixes preserved, immutable original and effective proof verified. Math/bounded priority/disposition100%; goal active16/99=16.16%. Exact optimum identity verified, priority unresolved. No paper/DOI/tracker/merge. Completion metadata release pending; next ordered status intake108.\n'
for p in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md',N/'RESEARCH_LOG.md']:
 with p.open('a') as f:f.write('\n'+line)
paths=[P/'CURRENT_PROGRESS.json',P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md',A/'ROOT_CLOSURE_COMPLETION_20261006.json',A/'complete_prior_disposition.py',A/'NATIVE_CHECKPOINT_SELECTION_20261006.json',N/'RESEARCH_LOG.md',N/'FINAL_DISPOSITION.json']
paths += [A/'actual_checkpoints/native_prior_disposition_release'/n for n in ['RECEIPT.json','PROCESS_JOURNAL.json']]
paths += [p for p in D.iterdir() if p.is_file()]
paths += [p for p in (A/'actual_operations/native_prior_disposition_release').iterdir() if p.is_file()]
dump(A/'COMPLETION_CHECKPOINT_SELECTION_20261006.json',{'paths':sorted(set(str(p.relative_to(C)) for p in paths)),'UTC':t,'previous_native_commit':commit})
print(json.dumps({k:v for k,v in result.items() if k!='actual_PR_readback'}))
