"""Freeze exact eligible PR209 source/claim before any mathematical acceptance."""
from pathlib import Path
from datetime import datetime,timezone
import base64,hashlib,json,os,subprocess
ROOT=Path('/Users/alec/Documents/Math');P=ROOT/'draft_pr_descending_audit_20261002'
G=Path(__file__).resolve().parent
selected=json.loads((G/'SELECTION.json').read_text())['selected']
assert selected['PR']==209 and selected['problem_id']=='5100015' and selected['status']=='claimed_solved'
previous=P/'audits/pr210_5100033/initial_review_20261015'
done=json.loads((previous/'FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json').read_text())
assert done['actual_publication_tracker_native_merge_complete'] is True and done['counts']==[44,21,21,0]
C=P/'audits/pr209_5100015';D=C/'initial_review_20261016'
D.mkdir(parents=True,exist_ok=False)
T=D/'private_transport/intake_01';T.mkdir(parents=True)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh';seq=0
def get(path):
    global seq
    seq+=1;run=subprocess.run([GH,'api','repos/AlecKriebel/Math/'+path],capture_output=True,timeout=60)
    (T/f'{seq:02d}-stdout.json').write_bytes(run.stdout)
    (T/f'{seq:02d}-stderr.txt').write_bytes(run.stderr)
    if run.returncode:raise RuntimeError('Read-only intake call failed; inspect retained output before retry')
    return json.loads(run.stdout)
pr=get('pulls/209');head=pr['head']['sha']
assert pr['number']==209 and pr['state']=='open' and pr['draft'] and not pr['merged']
assert head==selected['head'] and pr['head']['ref']==selected['branch']
assert pr['head']['repo']['full_name']==pr['base']['repo']['full_name']=='AlecKriebel/Math'
assert pr['base']['ref']=='main'
q=get('contents/unsolved_math_prioritization/QUEUE.md?ref='+head)
queue=base64.b64decode(q['content'])
assert q['sha']==selected['Queue_blob']
assert hashlib.sha1(b'blob '+str(len(queue)).encode()+b'\0'+queue).hexdigest()==q['sha']
assert hashlib.sha256(queue).hexdigest()==selected['Queue_sha256']
rows=[r for r in queue.decode().splitlines() if '5100015 / AMR-050-0015' in r]
assert rows==[selected['queue_row']] and rows[0].split('|')[8].strip()=='claimed_solved'
turns=int(rows[0].split('|')[9].strip().split('/')[0])
prefix='unsolved_math_prioritization/attempts/5100015/'
tree_sha=get('git/commits/'+head)['tree']['sha']
for component in prefix.strip('/').split('/'):
    listing=get('git/trees/'+tree_sha);assert not listing['truncated']
    matches=[r for r in listing['tree'] if r['path']==component]
    assert len(matches)==1 and matches[0]['type']=='tree';tree_sha=matches[0]['sha']
listing=get('git/trees/'+tree_sha+'?recursive=1');assert not listing['truncated']
assert all(r['type'] in ['tree','blob'] for r in listing['tree'])
pins=[]
for row in listing['tree']:
    if row['type']!='blob':continue
    assert row['mode'] in ['100644','100755']
    obj=get('git/blobs/'+row['sha']);assert obj['encoding']=='base64'
    raw=base64.b64decode(obj['content']);assert len(raw)==row['size']==obj['size']
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['sha']
    native=prefix+row['path'];target=D/'submitted'/native
    assert target.resolve().is_relative_to((D/'submitted').resolve())
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    os.chmod(target,int(row['mode'],8))
    pins.append(dict(native_path=native,native_blob=row['sha'],native_mode=row['mode'],
        bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
again=get('pulls/209')
assert again['head']['sha']==head and again['state']=='open' and again['draft'] and not again['merged']
utc=datetime.now(timezone.utc).isoformat()
(D/'.gitignore').write_text('/private_transport/\n/private_reading/\n/private_upstream/\nprivate/\n')
intake=dict(utc=utc,PR=209,problem_id=5100015,code='AMR-050-0015',title=pr['title'],head=head,
    branch=pr['head']['ref'],native_source_prefix=prefix,Queue_path='unsolved_math_prioritization/QUEUE.md',
    Queue_blob=q['sha'],Queue_sha256=hashlib.sha256(queue).hexdigest(),QUEUE_status='claimed_solved',queue_row=rows[0],
    original_source_files=pins,all_native_blob_size_SHA1_SHA256_verified=True,
    entire_native_attempt_subtree_frozen=True,original_file_modes_preserved=True,
    case_completion_percent=5,classification_is_a_hypothesis=True,author_turns=turns,
    app_PR_attachment='attached successfully',previous_completed_PR=210,
    previous_DOI='10.5281/zenodo.23398175',previous_accepted_head='27af3971bac399df78a397328f08d6633b6e13e8',
    previous_merge_commit='15cfbc62df85b211d6a5cbf257d25df06b4a044c',
    previous_completed_main_checkpoint=done['commit'])
(D/'INTAKE.json').write_text(json.dumps(intake,indent=2)+'\n')
stage='exact_source_intake_complete_mathematical_and_source_audit_pending'
state=dict(utc=utc,PR=209,problem_id=5100015,head=head,QUEUE_status='claimed_solved',stage=stage,
    current_stage=stage,mathematical_verdict='not yet evaluated',source_verdict='not yet evaluated',
    priority_verdict='not yet evaluated',completion_percent=5,case_completion_percent=5,
    preprint_preparation_cleared=False,preprint_upload_cleared=False,
    whole_manuscript_reviews_completed=0,release_helper_source_reviews_completed=0,
    counts=[44,21,21,0],goal_active_incomplete=True)
(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
line=utc+' — PR209/5100015 case5%: exact current open/drafthead '+head+' and claimed_solved row authenticated. Entire native attempt frozen with every blob size/SHA1/SHA256/mode verified. Author'+str(turns)+'/5. All mathematical/source/priority claims remain hypotheses; no acceptance, paper or promotion. PreviousPR210 complete with DOI23398175, exactPDF/181ZIP/publicSHA, single113GWSrow/all4cells, merge15cfbc62 and finalmain1a702f88. Counts44/21/21/0; held293/292/280/239 unchanged. Fullgoalactive/incomplete.\n'
(D/'RESEARCH_LOG.md').write_text('# PR209 /5100015 research log\n\n'+line)
old=json.loads((P/'CURRENT_GOAL_SELECTION_20261013.json').read_text())
keep=['skip_PRs','skip_reasons','PR8_excluded','no_shard_chat_coordination','held_uncompleted_PRs',
    'held_case_priority_gaps','pending_user_input','goal_objective_file','previous_scope_skip_PR',
    'previous_scope_skip_reason','previous_credit_disposition_PR','previous_credit_disposition_head']
goal={k:old[k] for k in keep if k in old}
goal.update(utc=utc,current_PR=209,problem_id='5100015',current_PR_head=head,original_PR_head=head,
    status_at_current_PR_head='claimed_solved',status_source='Authenticated current PR-head QUEUE.md',
    previous_completed_PR=210,previous_completed_DOI='10.5281/zenodo.23398175',
    previous_completed_main_checkpoint=done['commit'],previous_completed_merge='15cfbc62df85b211d6a5cbf257d25df06b4a044c',
    previous_case_acceptance='audits/pr210_5100033/initial_review_20261015/ROOT_FINAL_CASE_ACCEPTANCE.json',
    previous_completion_counts=[44,21,21,0],program_counts=[44,21,21,0],counts=[44,21,21,0],
    stage=stage,current_stage=stage,completion_percent=5,case_completion_percent=5,current_case_completion_percent=5,
    native_source_prefix=prefix,Queue_blob=q['sha'],original_Queue_blob=q['sha'],
    accepted_PR_queue_blob=None,accepted_PR_head=None,final_verified_main_checkpoint=None,
    current_DOI=None,current_tracker_range=None,preprint_preparation_cleared=False,preprint_upload_cleared=False,
    mathematical_verdict='not yet evaluated',source_verdict='not yet evaluated',priority_verdict='not yet evaluated',
    mathematical_repairs_required=[],priority_classification_repairs_required=[],priority_credit_repairs_required=[],
    whole_manuscript_reviews_completed=0,release_helper_source_reviews_completed=0,final_clean_reviews=0,
    unresolved_review_findings=[],goal_active_incomplete=True,overall_goal_active_incomplete=True,
    whole_goal_at_impasse=False)
for skipped in json.loads((G/'SELECTION.json').read_text())['read_only_current_head_gates']:
    if skipped['eligible']:continue
    goal['skip_PRs']=sorted(set(goal.get('skip_PRs',[])+[skipped['PR']]),reverse=True)
    goal.setdefault('skip_reasons',{})[str(skipped['PR'])]=skipped.get('status',skipped['reason'])
(P/'CURRENT_GOAL_SELECTION_20261013.json').write_text(json.dumps(goal,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+line)
print(json.dumps(dict(PR=209,head=head,status='claimed_solved',case_percent=5,
    files=len(pins),bytes=sum(r['bytes'] for r in pins)),indent=2))
print(json.dumps([dict(path=r['native_path'].removeprefix(prefix),bytes=r['bytes']) for r in pins],indent=2))
