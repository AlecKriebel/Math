"""Freeze only the newly selected eligible current PR210; no provider writes."""
from pathlib import Path
from datetime import datetime,timezone
import base64,hashlib,json,subprocess

ROOT=Path('/Users/alec/Documents/Math');P=ROOT/'draft_pr_descending_audit_20261002'
G=Path(__file__).resolve().parent
selected=json.loads((G/'SELECTION.json').read_text())['selected']
assert selected['PR']==210 and selected['problem_id']=='5100033' and selected['status']=='claimed_solved'
D=P/'audits/pr210_5100033/initial_review_20261015';D.mkdir(parents=True,exist_ok=False)
T=D/'private_transport/intake_01';T.mkdir(parents=True)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh';seq=0

def get(path):
    global seq
    seq+=1;r=subprocess.run([GH,'api','repos/AlecKriebel/Math/'+path],capture_output=True,timeout=60)
    (T/f'{seq:02d}-stdout.json').write_bytes(r.stdout);(T/f'{seq:02d}-stderr.txt').write_bytes(r.stderr)
    assert r.returncode==0;return json.loads(r.stdout)

pr=get('pulls/210');head=pr['head']['sha']
assert pr['state']=='open' and pr['draft'] and not pr['merged'] and head==selected['head']
q=get('contents/unsolved_math_prioritization/QUEUE.md?ref='+head)
queue=base64.b64decode(q['content']);assert q['sha']==selected['Queue_blob']
assert hashlib.sha256(queue).hexdigest()==selected['Queue_sha256']
rows=[r for r in queue.decode().splitlines() if '5100033 / AMR-050-0033' in r]
assert len(rows)==1 and rows[0]==selected['queue_row'] and rows[0].split('|')[8].strip()=='claimed_solved'
turns=int(rows[0].split('|')[9].strip().split('/')[0])
prefix='unsolved_math_prioritization/attempts/5100033/'
tree_sha=get('git/commits/'+head)['tree']['sha']
for part in prefix.strip('/').split('/'):
    tree=get('git/trees/'+tree_sha);assert not tree['truncated']
    row=next(r for r in tree['tree'] if r['path']==part);assert row['type']=='tree';tree_sha=row['sha']
tree=get('git/trees/'+tree_sha+'?recursive=1');assert not tree['truncated']
pins=[]
for row in tree['tree']:
    if row['type']!='blob':continue
    assert row['mode'] in ['100644','100755']
    obj=get('git/blobs/'+row['sha']);assert obj['encoding']=='base64';raw=base64.b64decode(obj['content'])
    assert len(raw)==row['size']==obj['size']
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['sha']
    native=prefix+row['path'];target=D/'submitted'/native
    assert target.resolve().is_relative_to((D/'submitted').resolve())
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    pins.append(dict(native_path=native,native_blob=row['sha'],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
pr2=get('pulls/210');assert pr2['head']['sha']==head and pr2['state']=='open' and pr2['draft']
t=datetime.now(timezone.utc).isoformat();(D/'.gitignore').write_text('/private_transport/\n/private_reading/\n/private_upstream/\nprivate/\n')
intake=dict(utc=t,PR=210,problem_id=5100033,code='AMR-050-0033',title=pr['title'],head=head,
            branch=pr['head']['ref'],native_source_prefix=prefix,Queue_path='unsolved_math_prioritization/QUEUE.md',
            Queue_blob=q['sha'],Queue_sha256=hashlib.sha256(queue).hexdigest(),QUEUE_status='claimed_solved',queue_row=rows[0],
            original_source_files=pins,all_native_blob_size_and_SHA1_verified=True,entire_native_attempt_subtree_frozen=True,
            case_completion_percent=5,classification_is_a_hypothesis=True,author_turns=turns,app_PR_attachment='attached successfully',
            previous_complete_merge_PR=211,previous_complete_merge_head='e49dc6cce102465404285f60ced0f9a2818cf4d4',
            previous_completed_PR=211,previous_DOI='10.5281/zenodo.23394004')
(D/'INTAKE.json').write_text(json.dumps(intake,indent=2)+'\n')
state=dict(utc=t,PR=210,problem_id=5100033,head=head,QUEUE_status='claimed_solved',
           stage='full_current_native_source_intake_mathematical_audit_pending',mathematical_verdict='not yet evaluated',
           source_verdict='not yet evaluated',priority_verdict='not yet evaluated',completion_percent=5,
           preprint_upload_cleared=False,counts=[43,20,20,0],goal_active_incomplete=True)
(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
line=t+' — PR210 /5100033 case5%: exact current open drafthead and claimed_solved row authenticated, entireattempt frozen with every nativeblob size/SHA1/SHA256 verified. Author'+str(turns)+'/5. Every mathematical/source/priorityclaim remains a hypothesis; no acceptance/promotion. PreviousPR211 completed, DOI10.5281/zenodo.23394004/publicfiles exact, single GWSrow109/all4cellsverified, native ec6c938f1b734610ba37c21beaf10ec24cdd077c merged/factualmain471fddad3c3d20baf057fd42e20d9bcfb9af6096 verified. Counts43/20/20/0; held293/292/280/239 unchanged/uncompleted; fullgoalactive/incomplete.\n'
(D/'RESEARCH_LOG.md').write_text('# PR210 /5100033 research log\n\n'+line)
g=json.loads((P/'CURRENT_GOAL_SELECTION_20261013.json').read_text())
g.update(utc=t,whole_manuscript_reviews_completed=0,accepted_PR_queue_blob=None,final_verified_main_checkpoint=None,previous_completed_PR=211,previous_completed_DOI='10.5281/zenodo.23394004',previous_completed_main_checkpoint='471fddad3c3d20baf057fd42e20d9bcfb9af6096',current_PR=210,problem_id='5100033',current_PR_head=head,original_PR_head=head,
         status_at_current_PR_head='claimed_solved',Queue_blob=q['sha'],original_Queue_blob=q['sha'],
         current_stage=state['stage'],case_completion_percent=5,native_source_prefix=prefix,current_DOI=None,
         current_tracker_range=None,priority_verdict='not yet evaluated',mathematical_repairs_required=[],
         priority_classification_repairs_required=[],previous_credit_disposition_PR=212,
         previous_credit_disposition_head='99af7a27a711271bcd0b9e7ce90e374e4100ea6d',whole_goal_at_impasse=False,preprint_preparation_cleared=False,preprint_upload_cleared=False,mathematical_verdict='not yet evaluated',source_verdict='not yet evaluated',priority_credit_repairs_required=[])
gates=json.loads((G/'SELECTION.json').read_text())['read_only_current_head_gates']
skips=[r for r in gates if r['PR']>210 and not r['eligible']]
g['skip_PRs']=sorted(set(g['skip_PRs']+[r['PR'] for r in skips]),reverse=True)
g['skip_reasons'].update({str(r['PR']):r.get('status',r['reason']) for r in skips})
g['previous_scope_skip_PR']=212;g['previous_scope_skip_reason']='Exact prior numerical negative coverage; corrected already_solved after eligible-intake review'
assert g['program_counts']==[43,20,20,0]
(P/'CURRENT_GOAL_SELECTION_20261013.json').write_text(json.dumps(g,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+line)
print(json.dumps(dict(PR=210,head=head,status='claimed_solved',case_percent=5,files=len(pins),bytes=sum(r['bytes'] for r in pins)),indent=2))
print(json.dumps([dict(path=r['native_path'].removeprefix(prefix),bytes=r['bytes']) for r in pins],indent=2))
