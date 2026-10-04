"""Close PR50 only after actual qualified publication, tracker, merge and mirror."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

Q=Path(__file__).resolve().parent; A=Q.parent; P=A.parents[1]; R=P.parent
O=A/'qualified_publication_operations_20261004'
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def binding(p): return {'path':p.relative_to(R).as_posix(),'sha256':sha(p.read_bytes())}
private=O/'private/final-native-readback'; private.mkdir()
(private/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
commands=[]
def run(argv):
    start=dt.datetime.now(dt.timezone.utc).isoformat()
    child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate(); n=len(commands)+1
    (private/(str(n)+'.stdout')).write_bytes(out); (private/(str(n)+'.stderr')).write_bytes(err)
    commands.append({'argv':argv,'actual_pid':child.pid,'started_utc':start,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err)})
    (private/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
    assert child.returncode==0
    return out
def git(*args): return run(['git','--no-optional-locks',*args])
gate=load(Q/'FINAL_NATIVE_GATE.json'); pub=load(Q/'PUBLICATION_VERIFICATION.json'); tracker=load(Q/'TRACKER_VERIFICATION.json')
assert pub['published'] and pub['all_public_bytes_identical'] and tracker['DOI']==pub['DOI']
assert tracker['independent_readback_exact'] and tracker['fresh_full_table_exactly_one_matching_problem_DOI_row']
for b in gate['final_artifacts']+gate['clean_reviews']+[gate['publication_verification'],gate['tracker_verification']]: assert binding(R/b['path'])==b
merge=load(O/'NATIVE_MERGE_RESULT.json'); mirror=load(O/'NATIVE_ACCEPTANCE_RESULT.json')
base=git('rev-parse','HEAD').decode().strip()
assert base==mirror['acceptance_commit']==git('ls-remote','--heads','origin','main').decode().split()[0]
assert git('branch','--show-current').strip()==b'main' and not git('diff','--cached','--name-only','-z')
pr=json.loads(run(['gh','pr','view','50','--repo','AlecKriebel/Math','--json','number,state,headRefOid,mergeCommit,mergedAt,title,body,url']))
assert pr['state']=='MERGED' and pr['headRefOid']==gate['reviewed_head'] and pr['mergeCommit']['oid']==merge['merge_commit']
assert pr['title']=='Publish verified even-strand Markov calculus; historical priority unresolved'
assert pr['body'].rstrip('\n')==(Q/'PR50_ACCEPTED_BODY.md').read_text().rstrip('\n')
assert git('show','-s','--format=%P',merge['merge_commit']).decode().strip().split()==[merge['base'],gate['reviewed_head']]
assert git('show','-s','--format=%P',base).decode().strip()==merge['merge_commit']
originals=load(A/'ORIGINAL_MANIFEST.json')['files']; assert len(originals)==15
for item in originals:
    path=item['original_git_path']; body=(R/path).read_bytes()
    assert sha(body)==item['sha256']==sha(git('show',base+':'+path))
    tree=git('ls-tree',base,'--',path).decode().split()
    assert tree[0]==item['git_mode'] and tree[2]==item['git_blob_sha1']
    assert stat.S_IMODE((R/path).stat().st_mode)==(0o755 if tree[0]=='100755' else 0o644)
prefix='unsolved_math_prioritization/attempts/10600042'
accept=load(R/(prefix+'/acceptance.json'))
assert accept['outcome']=='verified_research_note_published_priority_unresolved' and accept['doi']==pub['DOI']
assert accept['tracker_range']==tracker['range'] and accept['final_gate']==binding(Q/'FINAL_NATIVE_GATE.json')
assert accept['new_central_attempts']==0 and accept['original_budget']=='1/5'
assert accept['historical_priority_certified'] is False and accept['present_openness_certified'] is False and accept['global_novelty_certified'] is False
for path in [prefix+'/acceptance.json',prefix+'/CURRENT_RESULT.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','unsolved_math_prioritization/QUEUE.md']:
    assert (R/path).read_bytes()==git('show',base+':'+path)
queue='unsolved_math_prioritization/QUEUE.md'
old=git('show',merge['base']+':'+queue).decode().splitlines(keepends=True); new=(R/queue).read_text().splitlines(keepends=True)
assert len(old)==len(new)
changed=[i for i,(x,y) in enumerate(zip(old,new)) if x!=y]; assert len(changed)==1
i=changed[0]; before=old[i].split('|'); after=new[i].split('|')
assert '| 10600042 /' in new[i] and len(before)==len(after)==14
assert [j for j in range(14) if before[j]!=after[j]]==[8,9,11,12]
assert after[8].strip()=='preprint_published' and after[9].strip()=='1/5' and after[12].strip()==pub['DOI']
state='unsolved_math_prioritization/state.json'; history='unsolved_math_prioritization/history.jsonl'
oldstate=json.loads(git('show',merge['merge_commit']+':'+state)); current=load(R/state)
assert '10600042' not in oldstate and {k:v for k,v in current.items() if k!='10600042'}==oldstate
oldhistory=git('show',merge['merge_commit']+':'+history); newhistory=(R/history).read_bytes()
assert newhistory.startswith(oldhistory)
extra=newhistory[len(oldhistory):].splitlines(); assert len(extra)==1
event=json.loads(extra[0]); assert event==current['10600042'] and event['event']=='acceptance_mirror_import' and event['event_id']==mirror['event_id']
assert len([x for x in newhistory.splitlines() if str(json.loads(x).get('id'))=='10600042'])==1
assert load(R/(prefix+'/status.json'))['turns_used']==1 and len((R/(prefix+'/turns.jsonl')).read_bytes().splitlines())==1
now=dt.datetime.now(dt.timezone.utc).isoformat()
record={'schema':'pr50-qualified-note-fully-completed/v1','UTC':now,'actual_pid':os.getpid(),'PR':50,
 'all_required_PR50_steps_complete_under_explicit_human_exception':True,'DOI':pub['DOI'],'record_url':pub['record_url'],
 'reviewed_head':gate['reviewed_head'],'merge_commit':merge['merge_commit'],'acceptance_commit':base,
 'tracker_range':tracker['range'],'two_fresh_exact_package_reviews_clean':True,
 'exact_public_files_and_metadata_verified':True,'unique_tracker_row_and_exact_readbacks_verified':True,
 'GitHub_exact_head_merged':True,'all_15_original_bodies_modes_blobs_preserved':True,
 'queue_only_four_selected_cells_changed':True,'one_present_day_acceptance_event':True,'other_state_and_history_preserved':True,
 'priority_clearance':False,'historical_priority_certified':False,'present_openness_certified':False,
 'qualified_publication_human_exception':binding(Q/'USER_AUTHORIZATION_AND_PREPARATION.json'),
 'final_gate':binding(Q/'FINAL_NATIVE_GATE.json'),'native_merge':binding(O/'NATIVE_MERGE_RESULT.json'),'native_mirror':binding(O/'NATIVE_ACCEPTANCE_RESULT.json'),
 'actual_GitHub_PR':pr,'actual_native_readback_commands':binding(private/'COMMANDS.json'),
 'new_central_proof_attempts':0,'original_budget':'1/5','PR50_completion_percent':100,'dated_program_completion_percent':4.040404,
 'next_PR':55,'persistent_goal_complete':False}
with (Q/'FULLY_COMPLETED_AND_RECONCILED.json').open('x') as f: json.dump(record,f,indent=2); f.write('\n')
progress_path=P/'CURRENT_PROGRESS.json'; previous=progress_path.read_bytes()
with (Q/'PROGRESS_BEFORE_COMPLETION.json').open('xb') as f:f.write(previous)
progress=json.loads(previous)
assert progress['current_PR']==50 and progress['fully_completed_eligible_PRs']==[9,16,18] and progress['dated_eligible_total']==99
progress.update(UTC=now,fully_completed_eligible_PRs=[9,16,18,50],fully_completed_count=4,fully_completed_fraction_percent=4.040404,
 workflow_estimate_percent=4.040404,workflow_estimate_definition='Four completed eligible workflows divided by dated99-PR census; PR50 qualified-note priority exception explicitly authorized by human.',
 current_PR=55,current_PR_workflow_percent=0,current_DOI=None,current_merge_commit=None,
 remaining_current_step='Recheck exact current PR55 claimed_solved eligibility and submitted head; resume scientific and priority adjudication under the original rules.',
 next_eligible_PR_after_current_completion=56,advance_to_next_PR_authorized_now=True,persistent_goal_complete=False,
 last_completed_PR=50,last_completed_PR_workflow_percent=100,last_completed_DOI=pub['DOI'],last_completed_merge_commit=merge['merge_commit'],last_completed_tracker_range=tracker['range'],
 last_completed_record=str((Q/'FULLY_COMPLETED_AND_RECONCILED.json').relative_to(P)))
for key in list(progress):
    if key.startswith('current_priority_') or key in ['current_mathematical_and_package_review_percent','current_publication_authorization','historical_preexception_review_and_hold','current_qualified_input_pins','current_fresh_review_status']:
        progress['last_completed_'+key.removeprefix('current_')]=progress.pop(key)
progress['last_completed_fresh_review_status']='two_new_complete_package_reviews_passed'
progress['last_completed_priority_hold']='Historical priority remains unresolved; inability to access fuller Nencka texts is disclosed. Human explicitly authorized PR50 qualified publication despite this gap; later PR requirements unchanged.'
progress_path.write_text(json.dumps(progress,indent=2)+'\n')
with (Q/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+now+' — PR50 qualified publication complete: DOI '+pub['DOI']+', exact public files/metadata, unique tracker '+tracker['range']+', actual exact-head merge '+merge['merge_commit']+' and native acceptance '+base+'. Historical priority remains unresolved under explicit human exception. Two fresh package reviews clean. Original1/5; new central attempts0. PR50 workflow100%; dated program4/99=4.040404%. NextPR55; persistent goal active.\n')
print(json.dumps(record,indent=2))
