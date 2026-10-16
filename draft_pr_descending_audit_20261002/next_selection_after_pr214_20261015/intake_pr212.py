"""Freeze only the newly selected eligible current PR212; no provider writes."""
from pathlib import Path
from datetime import datetime,timezone
import base64,hashlib,json,subprocess

ROOT=Path('/Users/alec/Documents/Math');P=ROOT/'draft_pr_descending_audit_20261002'
G=Path(__file__).resolve().parent
selected=json.loads((G/'SELECTION.json').read_text())['selected']
assert selected['PR']==212 and selected['problem_id']=='30005310' and selected['status']=='claimed_solved'
D=P/'audits/pr212_30005310/initial_review_20261015';D.mkdir(parents=True,exist_ok=False)
T=D/'private_transport/intake_01';T.mkdir(parents=True)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh';seq=0

def get(path):
    global seq
    seq+=1;r=subprocess.run([GH,'api','repos/AlecKriebel/Math/'+path],capture_output=True,timeout=60)
    (T/f'{seq:02d}-stdout.json').write_bytes(r.stdout);(T/f'{seq:02d}-stderr.txt').write_bytes(r.stderr)
    assert r.returncode==0;return json.loads(r.stdout)

pr=get('pulls/212');head=pr['head']['sha']
assert pr['state']=='open' and pr['draft'] and not pr['merged'] and head==selected['head']
q=get('contents/unsolved_math_prioritization/QUEUE.md?ref='+head)
queue=base64.b64decode(q['content']);assert q['sha']==selected['Queue_blob']
assert hashlib.sha256(queue).hexdigest()==selected['Queue_sha256']
rows=[r for r in queue.decode().splitlines() if '30005310 / OWR-11695865-009' in r]
assert len(rows)==1 and rows[0]==selected['queue_row'] and rows[0].split('|')[8].strip()=='claimed_solved'
turns=int(rows[0].split('|')[9].strip().split('/')[0])
prefix='unsolved_math_prioritization/attempts/30005310/'
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
pr2=get('pulls/212');assert pr2['head']['sha']==head and pr2['state']=='open' and pr2['draft']
t=datetime.now(timezone.utc).isoformat();(D/'.gitignore').write_text('/private_transport/\n/private_reading/\n/private_upstream/\nprivate/\n')
intake=dict(utc=t,PR=212,problem_id=30005310,code='OWR-11695865-009',title=pr['title'],head=head,
            branch=pr['head']['ref'],native_source_prefix=prefix,Queue_path='unsolved_math_prioritization/QUEUE.md',
            Queue_blob=q['sha'],Queue_sha256=hashlib.sha256(queue).hexdigest(),QUEUE_status='claimed_solved',queue_row=rows[0],
            original_source_files=pins,all_native_blob_size_and_SHA1_verified=True,entire_native_attempt_subtree_frozen=True,
            case_completion_percent=5,classification_is_a_hypothesis=True,author_turns=turns,app_PR_attachment='attached successfully',
            previous_complete_merge_PR=214,previous_complete_merge_head='95ba37055ebf1e7b4f9d76aa43816c9978c7bce8',
            previous_completed_PR=214,previous_DOI='10.5281/zenodo.23390551')
(D/'INTAKE.json').write_text(json.dumps(intake,indent=2)+'\n')
state=dict(utc=t,PR=212,problem_id=30005310,head=head,QUEUE_status='claimed_solved',
           stage='full_current_native_source_intake_mathematical_audit_pending',mathematical_verdict='not yet evaluated',
           source_verdict='not yet evaluated',priority_verdict='not yet evaluated',completion_percent=5,
           preprint_upload_cleared=False,counts=[42,19,19,0],goal_active_incomplete=True)
(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
line=t+' — PR212 /30005310 case5%: exact current open draft head and claimed_solved row authenticated, entire attempt frozen with every native blob size/SHA1/SHA256 verified. Author'+str(turns)+'/5. Every mathematical/source/priority claim remains a hypothesis; no acceptance or promotion. Skipped213 by its fresh exact native unsolved status only, without science processing. PR214 is complete, published at DOI10.5281/zenodo.23390551, tracker105, merged4abf30daa991860a275b3d25745159852757ad35. Counts42/19/19/0; held293/292/280/239 unchanged and uncompleted; full goal active/incomplete.\n'
(D/'RESEARCH_LOG.md').write_text('# PR212 /30005310 research log\n\n'+line)
g=json.loads((P/'CURRENT_GOAL_SELECTION_20261013.json').read_text())
g.update(utc=t,current_PR=212,problem_id='30005310',current_PR_head=head,original_PR_head=head,
         status_at_current_PR_head='claimed_solved',Queue_blob=q['sha'],original_Queue_blob=q['sha'],
         current_stage=state['stage'],case_completion_percent=5,native_source_prefix=prefix,current_DOI=None,
         current_tracker_range=None,priority_verdict='not yet evaluated',mathematical_repairs_required=[],
         priority_classification_repairs_required=[],previous_credit_disposition_PR=234,
         previous_credit_disposition_head='91a4477dce003cf563ed6985b27d6e106d7ec981',whole_goal_at_impasse=False,preprint_preparation_cleared=False,preprint_upload_cleared=False,mathematical_verdict='not yet evaluated',source_verdict='not yet evaluated',priority_credit_repairs_required=[])
gates=json.loads((G/'SELECTION.json').read_text())['read_only_current_head_gates']
skips=[r for r in gates if r['PR']>212 and not r['eligible']]
g['skip_PRs']=sorted(set(g['skip_PRs']+[r['PR'] for r in skips]),reverse=True)
g['skip_reasons'].update({str(r['PR']):r.get('status',r['reason']) for r in skips})
g['previous_scope_skip_PR']=213;g['previous_scope_skip_reason']='Exact current PR-head QUEUE status unsolved'
assert g['program_counts']==[42,19,19,0]
(P/'CURRENT_GOAL_SELECTION_20261013.json').write_text(json.dumps(g,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+line)
print(json.dumps(dict(PR=212,head=head,status='claimed_solved',case_percent=5,files=len(pins),bytes=sum(r['bytes'] for r in pins)),indent=2))
print(json.dumps([dict(path=r['native_path'].removeprefix(prefix),bytes=r['bytes']) for r in pins],indent=2))
