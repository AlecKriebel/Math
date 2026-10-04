"""Independently verify the actual PR57 native/service outcome and progress."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

F=Path(__file__).resolve().parent; A=F.parent; R=A.parents[2]; P=R/'draft_pr_publication_program_20260930'; O=A/'ordered_publication_operations_20261004'
D=F/'private/final_readback'; D.mkdir(parents=True)
(D/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes()); commands=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def bind(p): return {'path':p.relative_to(R).as_posix(),'sha256':sha(p.read_bytes())}
def run(argv):
    start=dt.datetime.now(dt.timezone.utc).isoformat(); child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE); out,err=child.communicate()
    n=len(commands)+1; (D/(str(n)+'.stdout')).write_bytes(out); (D/(str(n)+'.stderr')).write_bytes(err)
    commands.append({'argv':argv,'actual_pid':child.pid,'started_UTC':start,'finished_UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err)})
    (D/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n'); assert child.returncode==0; return out
def git(*parts): return run(['git','--no-optional-locks',*parts])
merge=load(O/'NATIVE_MERGE_RESULT.json'); native=load(O/'NATIVE_ACCEPTANCE_RESULT.json'); gate=load(F/'FINAL_NATIVE_GATE.json'); pub=load(F/'PUBLICATION_VERIFICATION.json'); tracker=load(F/'TRACKER_VERIFICATION.json')
assert git('branch','--show-current').strip()==b'main' and not git('diff','--cached','--name-only','-z')
head=git('rev-parse','HEAD').decode().strip(); assert head==native['acceptance_commit']==git('ls-remote','--heads','origin','main').decode().split()[0]
assert git('show','-s','--format=%P',head).decode().strip()==merge['merge_commit']
assert git('show','-s','--format=%P',merge['merge_commit']).decode().strip().split()==[merge['base'],merge['submitted_head']]
pr=json.loads(run(['gh','pr','view','57','--repo','AlecKriebel/Math','--json','number,state,isDraft,title,body,headRefOid,mergeCommit,mergedAt,url']))
assert pr['state']=='MERGED' and pr['headRefOid']==merge['submitted_head'] and pr['mergeCommit']['oid']==merge['merge_commit']
assert pr['title']==(O/'PR_TITLE.txt').read_text().strip() and pr['body']==(F/'PREPARED_PR_BODY.md').read_text()
auth=load(A/'original_preparation_family/ORIGINAL_AUTHENTICATION.json'); assert len(auth['original_science_files'])==17
for item in auth['original_science_files']:
    p=R/item['repository_path']; body=p.read_bytes(); assert len(body)==item['bytes'] and sha(body)==item['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o644
    assert sha(git('show',head+':'+item['repository_path']))==item['sha256']
    tree=git('ls-tree',head,'--',item['repository_path']).decode().split(); assert tree[0]==item['git_mode'] and tree[2]==item['git_blob_sha1']
prefix=R/'unsolved_math_prioritization/attempts/30003354'; accepted=load(prefix/'acceptance.json')
assert accepted['full_specified_source_target_solved'] is True and accepted['doi']==pub['DOI']=='10.5281/zenodo.23131374'
assert accepted['final_gate']==bind(F/'FINAL_NATIVE_GATE.json') and accepted['merge_commit']==merge['merge_commit']
assert accepted['publication_verification']==bind(F/'PUBLICATION_VERIFICATION.json') and accepted['tracker_verification']==bind(F/'TRACKER_VERIFICATION.json')
assert accepted['tracker_range']==tracker['range']=="'Math Puzzles'!A19:D19"
assert accepted['exact_scope']==gate['exact_claim'] and accepted['original_budget']=='1/5' and accepted['new_central_proof_attempts']==0
for k in ['worldwide_priority_guarantee','RP2_result','noninteger_topology_result','smooth_topology_result','abstract_homeomorphism_obstruction','human_peer_review','formal_proof_certification']: assert accepted[k] is False
assert accepted['current_source_identity']['review_hash']=='0bd321aaf672e74ea23dc3a6708a5a2df569df4c51bed66fc17f86cb3dafc6a3'
turns=load(prefix/'turns.json'); assert turns['substantive_proof_attempts']==1 and turns['budget']==5 and len(turns['turns'])==1
assert not (prefix/'status.json').exists() and not (prefix/'turns.jsonl').exists()
state=load(R/'unsolved_math_prioritization/state.json'); history=(R/'unsolved_math_prioritization/history.jsonl').read_bytes()
events=[json.loads(s) for s in history.splitlines() if str(json.loads(s).get('id'))=='30003354']
assert len(events)==1 and events[0]==state['30003354'] and events[0]['event_id']==native['event_id']
oldstate=json.loads(git('show',merge['merge_commit']+':unsolved_math_prioritization/state.json')); oldhistory=git('show',merge['merge_commit']+':unsolved_math_prioritization/history.jsonl')
assert {k:v for k,v in state.items() if k!='30003354'}==oldstate and history.startswith(oldhistory) and len(history[len(oldhistory):].splitlines())==1
queue=(R/'unsolved_math_prioritization/QUEUE.md').read_bytes(); assert queue==git('show',head+':unsolved_math_prioritization/QUEUE.md')
rows=[s for s in queue.decode().splitlines() if '| 30003354 /' in s]; assert len(rows)==1
cells=rows[0].split('|'); assert cells[8].strip()=='preprint_published' and cells[9].strip()=='1/5' and cells[12].strip()==pub['DOI']
before=git('show',merge['base']+':unsolved_math_prioritization/QUEUE.md').decode().splitlines(); after=queue.decode().splitlines(); assert len(before)==len(after)
changed=[i for i,(x,y) in enumerate(zip(before,after)) if x!=y]; assert len(changed)==1
prior=before[changed[0]].split('|'); current=after[changed[0]].split('|'); assert all(x==y for i,(x,y) in enumerate(zip(prior,current)) if i not in (8,9,11,12))
now=dt.datetime.now(dt.timezone.utc).isoformat()
done={'schema':'pr57-published-result-completion/v1','UTC':now,'actual_pid':os.getpid(),'PR':57,'all_mathematical_package_priority_publication_tracker_and_native_steps_verified':True,'reviewed_head':merge['submitted_head'],'merge_commit':merge['merge_commit'],'acceptance_commit':head,'DOI':pub['DOI'],'record_url':pub['record_url'],'tracker_range':tracker['range'],'all_17_original_bodies_modes_blobs_preserved':True,'one_present_day_acceptance_event':True,'other_native_states_history_prefix_and_queue_rows_preserved':True,'native_acceptance':bind(prefix/'acceptance.json'),'final_gate':bind(F/'FINAL_NATIVE_GATE.json'),'publication_verification':bind(F/'PUBLICATION_VERIFICATION.json'),'tracker_verification':bind(F/'TRACKER_VERIFICATION.json'),'full_specified_finite_integer_source_target_solved':True,'bounded_priority_audit_complete':True,'worldwide_priority_guarantee':False,'PR50_exception_extended':False,'original_budget':'1/5','new_central_proof_attempts':0,'PR57_workflow_percent':100,'dated_completed_program_fraction_percent':6/99*100,'publication_count':5,'partial_acceptance_count':1,'final_scoped_audit_checkpoint_push_pending':True,'next_numeric_intake_cursor':58,'next_eligible_PR_unverified':True,'persistent_goal_complete':False}
with (F/'FULLY_COMPLETED_PUBLISHED_RESULT.json').open('x') as f: json.dump(done,f,indent=2); f.write('\n')
progress=load(P/'CURRENT_PROGRESS.json'); assert progress['fully_completed_eligible_PRs']==[9,16,18,50,55]
progress.update({'UTC':now,'eligibility_census':'claimed_solved_scope_20261003/LIVE_DRAFT_ELIGIBILITY_REGISTRY.json','eligibility_denominator_record':'claimed_solved_scope_20261003/SCOPE_HANDOFF.json','fully_completed_eligible_PRs':[9,16,18,50,55,57],'fully_completed_count':6,'fully_completed_fraction_percent':6/99*100,'workflow_estimate_percent':6/99*100,'workflow_estimate_definition':'Five published workflows and one scoped attributed partial-result disposition divided by the dated99-PR intake census. The census pointer now correctly identifies the live registry and its99-count handoff rather than the older180-roster44-claimed ledger. PR50 human publication exception remains local to PR50.','published_PRs':[9,16,18,50,57],'current_PR':None,'current_PR_workflow_percent':0,'current_DOI':None,'current_merge_commit':None,'remaining_current_step':'Fresh status-only intake beginning with58 to identify the next literal claimed_solved draft; skip all other statuses entirely.','next_numeric_intake_cursor':58,'next_eligible_PR_after_current_completion':None,'next_eligible_order_requires_fresh_status_check':True,'last_completed_PR':57,'last_completed_PR_workflow_percent':100,'last_completed_DOI':pub['DOI'],'last_completed_merge_commit':merge['merge_commit'],'last_completed_tracker_range':tracker['range'],'last_completed_record':'audits/pr57_30003354/root_ordered_resumption_20261004/FULLY_COMPLETED_PUBLISHED_RESULT.json','last_completed_scientific_disposition_record':'audits/pr57_30003354/root_ordered_resumption_20261004/FULLY_COMPLETED_PUBLISHED_RESULT.json','last_completed_outcome':'full_specified_finite_integer_endpoint_negative_answer_published','last_completed_full_source_solved':True,'last_completed_priority_clearance':True,'last_completed_publication_authorization':'Original claimed_solved publication procedure, current ROOT final gate; PR50 exception not extended.','last_completed_priority_hold':None,'last_completed_final_audit_checkpoint_commit':None,'last_completed_audit_checkpoint_push_pending':True,'last_published_PR':57,'last_published_DOI':pub['DOI'],'persistent_goal_complete':False})
progress.pop('last_completed_scope_interpretation',None)
(P/'CURRENT_PROGRESS.json').write_text(json.dumps(progress,indent=2)+'\n')
with (F/'RESEARCH_LOG.md').open('a') as f: f.write('\n'+now+' — Actual repository-kit publication23131374, anonymous exact PDF/ZIP bytes, intended metadata and resolved DOI verified. GWS row19 uniquely and independently read back; exact original-head merge and present-day acceptance pushed and read back;17 original bodies/modes/blobs, all other queue rows, states and historical prefix preserved. PR57 workflow100%; final audit checkpoint pending. Five publications and one scoped partial acceptance: dated6/99='+str(6/99*100)+'%. Corrected census pointer to the actual live registry99-count handoff; earlier dated records remain unchanged. Next numeric intake58, eligible successor not yet verified. No new proof turn.\n')
print(json.dumps(done,indent=2))
