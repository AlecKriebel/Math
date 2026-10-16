"""Read actual PR55 completion and record progress; no Git/remote mutation."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

F=Path(__file__).resolve().parent; A=F.parent; P=A.parents[1]; R=P.parent
O=A/'partial_integration_operations_20261004'
private=F/'private/final-readback'; private.mkdir()
(private/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
commands=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def run(argv):
    started=dt.datetime.now(dt.timezone.utc).isoformat()
    child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate(); n=len(commands)+1
    (private/(str(n)+'.stdout')).write_bytes(out); (private/(str(n)+'.stderr')).write_bytes(err)
    commands.append({'argv':argv,'actual_pid':child.pid,'started_UTC':started,'finished_UTC':dt.datetime.now(dt.timezone.utc).isoformat(),
                     'exit_code':child.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err)})
    (private/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
    assert child.returncode==0
    return out
def git(*parts): return run(['git','--no-optional-locks',*parts])
def load(p): return json.loads(p.read_bytes())
def binding(p): return {'path':p.relative_to(R).as_posix(),'sha256':sha(p.read_bytes())}
merge=load(O/'NATIVE_MERGE_RESULT.json'); mirror=load(O/'NATIVE_ACCEPTANCE_RESULT.json')
gate=load(F/'ROOT_REVIEW_AND_SCOPE_BINDING.json')
assert gate['root_authorizes_guarded_partial_disposition_under_combined_scope'] is True
assert gate['full_source_solved'] is False and gate['prepare_paper'] is False
assert git('branch','--show-current').strip()==b'main' and not git('diff','--cached','--name-only','-z')
head=git('rev-parse','HEAD').decode().strip()
assert head==mirror['acceptance_commit']==git('ls-remote','--heads','origin','main').decode().split()[0]
assert git('show','-s','--format=%P',head).decode().strip()==merge['merge_commit']
assert git('show','-s','--format=%P',merge['merge_commit']).decode().strip().split()==[merge['base'],merge['submitted_head']]
w=load(R/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json')
assert w['shared_git_writes_paused'] is True and 'PR55' in w['paused_for']
assert w['local_main_at_pause']==w['remote_main_at_pause']==merge['base']
pr=json.loads(run(['gh','pr','view','55','--repo','AlecKriebel/Math','--json','number,state,isDraft,title,body,headRefOid,mergeCommit,mergedAt,url']))
assert pr['state']=='MERGED' and pr['headRefOid']==merge['submitted_head'] and pr['mergeCommit']['oid']==merge['merge_commit']
assert pr['title']=='Accept scoped Hurwitz polytope comparison as prior-theorem corollary'
assert pr['body']==(F/'PREPARED_PR_BODY.md').read_text()
auth=load(A/'original_preparation_family/ORIGINAL_AUTHENTICATION.json')
for item in auth['original_science_files']:
    p=R/item['repository_path']; b=p.read_bytes()
    assert sha(b)==item['sha256'] and len(b)==item['bytes'] and stat.S_IMODE(p.stat().st_mode)==0o644
    assert sha(git('show',head+':'+item['repository_path']))==item['sha256']
    tree=git('ls-tree',head,'--',item['repository_path']).decode().split()
    assert tree[0]==item['git_mode'] and tree[2]==item['git_blob_sha1']
prefix=R/'unsolved_math_prioritization/attempts/30006309'
acceptance=load(prefix/'acceptance.json')
assert acceptance['status']=='already_solved' and acceptance['accepted_as']=='partial_attributed_prior_theorem_corollary'
assert acceptance['full_source_solved'] is False and acceptance['broader_combinatorial_bijection_certified'] is False
assert acceptance['merge_commit']==merge['merge_commit'] and acceptance['final_gate']==binding(F/'ROOT_REVIEW_AND_SCOPE_BINDING.json')
for k in ('new_paper','Zenodo_upload','new_publication_DOI','tracker_row','global_novelty_certified','human_peer_review','formal_proof_certification'):
    assert acceptance[k] is False
assert acceptance['current_source_identity']['review_hash']=='1977a9fb3d6f860866cacdc4293e50016f17c4a3d169701470eb41be8eda7bfd'
assert acceptance['original_budget']=='1/5' and acceptance['new_central_proof_attempts']==0
assert len((prefix/'turns.jsonl').read_bytes().splitlines())==1
state=load(R/'unsolved_math_prioritization/state.json'); history=(R/'unsolved_math_prioritization/history.jsonl').read_bytes()
events=[json.loads(s) for s in history.splitlines() if str(json.loads(s).get('id'))=='30006309']
assert len(events)==1 and events[0]==state['30006309'] and events[0]['event_id']==mirror['event_id']
assert events[0]['turns_used']==1 and events[0]['evidence']['full_source_solved'] is False
rows=[s for s in (R/'unsolved_math_prioritization/QUEUE.md').read_text().splitlines() if '| 30006309 /' in s]
assert len(rows)==1
cells=rows[0].split('|')
assert cells[8].strip()=='already_solved' and cells[9].strip()=='1/5' and not cells[12].strip()
assert 'Esterov2010' in cells[11] and 'full-source/bijection unresolved' in cells[11]
specialization=prefix/'CURRENT_PRIORITY_SPECIALIZATION.md'
assert acceptance['current_priority_specialization']==binding(specialization)
assert specialization.read_bytes().endswith((A/'current_preparation_family/science/PRIOR_ART_SPECIALIZATION.md').read_bytes())
now=dt.datetime.now(dt.timezone.utc).isoformat()
done={'schema':'pr55-scoped-prior-result-completion/v1','UTC':now,'actual_pid':os.getpid(),'PR':55,
      'all_required_scoped_partial_outcome_steps_verified':True,'outcome':'already_solved_scoped_prior_theorem_corollary_accepted_partial',
      'scope_interpretation':binding(F/'ROOT_REVIEW_AND_SCOPE_BINDING.json'),'reviewed_head':merge['submitted_head'],
      'merge_commit':merge['merge_commit'],'acceptance_commit':head,'actual_GitHub_PR':pr,
      'all_16_original_bodies_modes_blobs_preserved':True,'one_present_day_acceptance_event':True,
      'original_budget':'1/5','new_central_proof_attempts':0,'full_source_solved':False,
      'new_paper':False,'Zenodo_upload':False,'new_publication_DOI':None,'tracker_row':False,
      'global_novelty_certified':False,'exact_earlier_printed_Hurwitz_proof_located':False,
      'current_priority_specialization':binding(specialization),'native_acceptance':binding(prefix/'acceptance.json'),
      'native_merge_receipt':binding(O/'NATIVE_MERGE_RESULT.json'),'native_mirror_receipt':binding(O/'NATIVE_ACCEPTANCE_RESULT.json'),
      'PR55_workflow_percent':100,'dated_completed_program_fraction_percent':5/99*100,
      'publication_count':4,'partial_acceptance_count':1,'final_scoped_audit_checkpoint_push_pending':True,
      'next_PR':56,'persistent_goal_complete':False}
with (F/'FULLY_COMPLETED_SCOPED_RESULT.json').open('x') as out: json.dump(done,out,indent=2);out.write('\n')
progress=load(P/'CURRENT_PROGRESS.json')
assert progress['fully_completed_eligible_PRs']==[9,16,18,50] and progress['current_PR']==55
progress.update({'UTC':now,'fully_completed_eligible_PRs':[9,16,18,50,55],'fully_completed_count':5,
                 'fully_completed_fraction_percent':5/99*100,'workflow_estimate_percent':5/99*100,
                 'workflow_estimate_definition':'Four published workflows and one scoped attributed partial-result disposition divided by the dated99-PR intake census. PR50 human publication exception is local to PR50; PR55 disposition follows the expressly recorded combined intake/outcome scope interpretation.',
                 'published_PRs':[9,16,18,50],'accepted_partial_prior_result_PRs':[55],
                 'current_PR':56,'current_PR_workflow_percent':0,'current_DOI':None,'current_merge_commit':None,
                 'remaining_current_step':'Independently recheck exact current PR56 claimed_solved eligibility and submitted head before scientific and priority review.',
                 'next_eligible_PR_after_current_completion':57,'last_completed_PR':55,'last_completed_PR_workflow_percent':100,
                 'last_completed_DOI':None,'last_completed_merge_commit':merge['merge_commit'],'last_completed_tracker_range':None,
                 'last_completed_record':'audits/pr55_30006309/root_goal_resumption_20261004/FULLY_COMPLETED_SCOPED_RESULT.json',
                 'last_completed_outcome':'already_solved_scoped_prior_theorem_corollary_accepted_partial',
                 'last_completed_priority_clearance':False,'last_completed_full_source_solved':False,
                 'last_completed_publication_authorization':None,
                 'last_completed_priority_hold':'No new preprint: prior Esterov formula sufficiently implies the scoped smooth model comparison. Exact prior target-specific proof and candidate-method priority unestablished; broader source/bijection uncertified.',
                 'last_completed_scope_interpretation':binding(F/'ROOT_REVIEW_AND_SCOPE_BINDING.json'),
                 'last_published_PR':50,'last_published_DOI':'10.5281/zenodo.23131001','persistent_goal_complete':False})
for key in list(progress):
    if key.startswith('last_completed_') and key in ('last_completed_priority_access_readback','last_completed_historical_preexception_review_and_hold','last_completed_qualified_input_pins','last_completed_fresh_review_status'):
        progress.pop(key)
progress['last_completed_mathematical_and_package_review_percent']=100
progress['last_completed_priority_audit_percent']=100
(P/'CURRENT_PROGRESS.json').write_text(json.dumps(progress,indent=2)+'\n')
with (F/'RESEARCH_LOG.md').open('a') as out:
    out.write(f'\n{now} — Exact GitHub merge, native attributed acceptance, all16 original files, one present-day state/history event and empty DOI cell independently read back. PR55 scoped partial disposition100%; dated completed workflows5/99={5/99*100:.6f}% (four publications, one partial acceptance). Final scoped audit checkpoint push remains pending; next intake56. No new proof attempt or PR55 publication.\n')
print(json.dumps({k:v for k,v in done.items() if k!='actual_GitHub_PR'},indent=2))
