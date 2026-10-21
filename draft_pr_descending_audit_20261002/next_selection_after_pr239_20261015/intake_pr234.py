"""Freeze the entire eligible PR234 attempt from native Git objects."""
from pathlib import Path
from datetime import datetime,timezone
import base64
import hashlib
import json
import subprocess

ROOT=Path('/Users/alec/Documents/Math')
P=ROOT/'draft_pr_descending_audit_20261002'
D=P/'audits/pr234_30002291/initial_review_20261015'
D.mkdir(parents=True,exist_ok=False)
T=D/'private_transport/intake_01';T.mkdir(parents=True)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
seq=0


def get(path):
    global seq
    seq+=1
    run=subprocess.run([GH,'api','repos/AlecKriebel/Math/'+path],capture_output=True,timeout=60)
    (T/f'{seq:02d}-stdout.json').write_bytes(run.stdout)
    (T/f'{seq:02d}-stderr.txt').write_bytes(run.stderr)
    assert run.returncode==0
    return json.loads(run.stdout)


pr=get('pulls/234');head=pr['head']['sha']
assert pr['state']=='open' and pr['draft'] and not pr['merged']
assert head=='34e4dfaeda693b5349b4ef5eec458962781b4bb3'
q=get('contents/unsolved_math_prioritization/QUEUE.md?ref='+head)
queue=base64.b64decode(q['content']).decode()
rows=[line for line in queue.splitlines() if '30002291 / OWR-12337-002' in line]
assert len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved'
prefix='unsolved_math_prioritization/attempts/30002291/'
sha=get('git/commits/'+head)['tree']['sha']
for part in prefix.strip('/').split('/'):
    tree=get('git/trees/'+sha);assert not tree['truncated']
    row=next(row for row in tree['tree'] if row['path']==part)
    assert row['type']=='tree';sha=row['sha']
tree=get('git/trees/'+sha+'?recursive=1');assert not tree['truncated']
pins=[]
for row in tree['tree']:
    if row['type']!='blob':continue
    assert row['mode'] in ['100644','100755']
    blob=get('git/blobs/'+row['sha']);assert blob['encoding']=='base64'
    raw=base64.b64decode(blob['content'])
    assert len(raw)==row['size']==blob['size']
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['sha']
    native=prefix+row['path'];path=D/'submitted'/native
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
    pins.append(dict(native_path=native,native_blob=row['sha'],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
assert get('pulls/234')['head']['sha']==head
(D/'.gitignore').write_text('/private_transport/\n/private_reading/\n')
utc=datetime.now(timezone.utc).isoformat()
intake=dict(utc=utc,PR=234,problem_id=30002291,code='OWR-12337-002',title=pr['title'],
            head=head,branch=pr['head']['ref'],native_source_prefix=prefix,
            Queue_path='unsolved_math_prioritization/QUEUE.md',Queue_blob=q['sha'],QUEUE_status='claimed_solved',
            queue_row=rows[0],original_source_files=pins,all_native_blob_size_and_SHA1_verified=True,
            entire_native_attempt_subtree_frozen=True,case_completion_percent=5,
            classification_is_a_hypothesis=True,author_turns=1,app_PR_attachment='attached successfully',
            prior_PR239='held at60%; mathematical PASS; priority original-source gap; unmerged/unpublished',
            previous_completed_PR=248,previous_DOI='10.5281/zenodo.23358014')
(D/'INTAKE.json').write_text(json.dumps(intake,indent=2)+'\n')
state=dict(utc=utc,PR=234,problem_id=30002291,head=head,QUEUE_status='claimed_solved',
           stage='full_current_native_source_intake_mathematical_audit_pending',
           mathematical_verdict='not yet evaluated',source_verdict='not yet evaluated',priority_verdict='not yet evaluated',
           completion_percent=5,preprint_upload_cleared=False,counts=[40,17,17,0],goal_active_incomplete=True)
(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
(D/'RESEARCH_LOG.md').write_text('# PR234 /30002291 research log\n\n'+utc+' — Case5%. Current native open draft head and exact claimed_solved row authenticated. Entire attempt subtree frozen with every native blob size/SHA1 and SHA256 checked. Author turn1/5. Submitted sufficient-condition claim remains a hypothesis; no mathematical/source/priority acceptance. No manuscript/deposit/tracker/merge. PR239 remains an explicit priority hold, not a completed case.\n')
held=P/'audits/pr239_30001321/initial_review_20261015'
old=json.loads((held/'CURRENT_AUDIT_STATE.json').read_text())
old.update(utc=utc,stage='held_priority_missing_original_sources_while_descending_intake_continues',
           consecutive_goal_turns_with_same_material_source_hold=3,
           current_goal_turn_classification='progress: independent next eligible PR234 intake; case239 source hold retained',
           whole_goal_blocked=False,whole_goal_blocked_audit='Not at a whole-goal impasse: independent authorized lower claimed_solved audits remain available',
           next_selected_PR=234)
(held/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(old,indent=2)+'\n')
hold_entry='\n'+utc+' — Case239 remains60% and uncompleted after its third consecutive source-hold turn. No live source-review process exists and named references remain missing. Whole-goal blocked criterion is not satisfied: the full objective authorizes independent lower claimed_solved PR audits. Native gates select234 after skipping238unsolved/237already_solved/236unsolved/235unsolved. Descending intake continues without certifying, publishing, merging, closing, or changing239. Prior held293/292/280 preserved; no individual contacted.\n'
with (held/'RESEARCH_LOG.md').open('a') as stream:stream.write(hold_entry)
selection=json.loads((P/'CURRENT_GOAL_SELECTION_20261013.json').read_text())
selection.update(utc=utc,current_PR=234,problem_id='30002291',current_PR_head=head,original_PR_head=head,
                 status_at_current_PR_head='claimed_solved',Queue_blob=q['sha'],original_Queue_blob=q['sha'],
                 current_stage=state['stage'],case_completion_percent=5,native_source_prefix=prefix,
                 current_DOI=None,current_tracker_range=None,priority_verdict='not yet evaluated',
                 mathematical_repairs_required=[],priority_classification_repairs_required=[],
                 pending_user_input='PR239 missing originals remain requested; independent descent continues',
                 held_case_priority_gaps={'239':['BMP1999 or relevant completeBMP2007','Conlon-Song1999']},
                 whole_goal_at_impasse=False)
selection['held_uncompleted_PRs']=sorted(set(selection['held_uncompleted_PRs']+[239]),reverse=True)
selection['skip_PRs']=sorted(set(selection['skip_PRs']+[238,237,236,235]),reverse=True)
selection['skip_reasons'].update({'238':'unsolved','237':'already_solved','236':'unsolved','235':'unsolved'})
selection['previous_scope_skip_PR']=235;selection['previous_scope_skip_reason']='Exact current PR-head QUEUE status unsolved'
for key in ['consecutive_goal_turns_with_same_material_source_hold','previous_goal_turn_classification',
            'current_goal_turn_classification','new_institutional_source','new_source_scope_audit','source_hold_followup',
            'final_priority_public_artifact_pins','final_priority_source_or_evidence_pins']:
    selection.pop(key,None)
(P/'CURRENT_GOAL_SELECTION_20261013.json').write_text(json.dumps(selection,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as stream:
    stream.write(hold_entry+'\n'+utc+' — PR234 /30002291 selected and entire native source frozen, case5%, author1/5. No acceptance or promotion. Counts40/17/17/0 unchanged; held293/292/280/239 uncompleted; goal active/incomplete.\n')
print(json.dumps(dict(PR=234,head=head,status='claimed_solved',case_percent=5,files=len(pins),bytes=sum(x['bytes'] for x in pins)),indent=2))
print(json.dumps([dict(path=x['native_path'].removeprefix(prefix),bytes=x['bytes']) for x in pins],indent=2))
