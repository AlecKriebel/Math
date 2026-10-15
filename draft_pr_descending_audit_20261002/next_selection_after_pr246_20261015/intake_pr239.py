from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,base64,hashlib
ROOT=Path('/Users/alec/Documents/Math')
P=ROOT/'draft_pr_descending_audit_20261002'
D=P/'audits/pr239_30001321/initial_review_20261015'
D.mkdir(parents=True,exist_ok=False)
T=D/'transport_receipts/intake_01'
T.mkdir(parents=True,exist_ok=False)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
seq=0
def get(path):
    global seq
    seq+=1;r=subprocess.run([GH,'api','repos/AlecKriebel/Math/'+path],capture_output=True)
    (T/f'{seq:02d}-stdout.json').write_bytes(r.stdout)
    (T/f'{seq:02d}-stderr.txt').write_bytes(r.stderr)
    assert r.returncode==0
    return json.loads(r.stdout)
pr=get('pulls/239')
head=pr['head']['sha']
assert pr['state']=='open' and pr['draft'] and head=='7f17eef77c52b2d9b2ec3ad0803c016267fa6496'
q=get('contents/unsolved_math_prioritization/QUEUE.md?ref='+head)
text=base64.b64decode(q['content']).decode()
rows=[x for x in text.splitlines() if '30001321 / OWR-4081-005' in x]
assert len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved'
prefix='unsolved_math_prioritization/attempts/30001321/'
sha=get('git/commits/'+head)['tree']['sha']
for part in prefix.strip('/').split('/'):
    tree=get('git/trees/'+sha);assert not tree['truncated']
    entry=next(x for x in tree['tree'] if x['path']==part)
    assert entry['type']=='tree'
    sha=entry['sha']
tree=get('git/trees/'+sha+'?recursive=1')
assert not tree['truncated']
pins=[]
for entry in tree['tree']:
    if entry['type']!='blob':continue
    assert entry['mode'] in ['100644','100755'],(entry['path'],entry['mode'])
    blob=get('git/blobs/'+entry['sha']);assert blob['encoding']=='base64'
    data=base64.b64decode(blob['content'])
    assert len(data)==blob['size']==entry['size']
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==entry['sha']
    native=prefix+entry['path'];f=D/'submitted'/native
    f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
    pins.append({'native_path':native,'native_blob':entry['sha'],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
assert get('pulls/239')['head']['sha']==head
utc=datetime.now(timezone.utc).isoformat()
intake={'utc':utc,'PR':239,'problem_id':30001321,'code':'OWR-4081-005','title':pr['title'],
        'head':head,'branch':pr['head']['ref'],'native_source_prefix':prefix,
        'Queue_path':'unsolved_math_prioritization/QUEUE.md','Queue_blob':q['sha'],
        'QUEUE_status':'claimed_solved','queue_row':rows[0],'original_source_files':pins,
        'all_native_blob_size_and_SHA1_verified':True,'entire_native_attempt_subtree_frozen':True,
        'previous_completed_PR':248,'previous_DOI':'10.5281/zenodo.23358014','previous_scope_skip_PR':246,'previous_scope_skip_head':'d9fd2b8d1b278430cbf6cb3ae25abd0f9a422034',
        'case_completion_percent':5,'classification_is_a_hypothesis':True,
        'author_turns':3,'app_PR_attachment':'Not attempted for this intake'}
(D/'INTAKE.json').write_text(json.dumps(intake,indent=2)+'\n')
(D/'CURRENT_AUDIT_STATE.json').write_text(json.dumps({'utc':utc,'PR':239,'problem_id':30001321,
    'head':head,'QUEUE_status':'claimed_solved','stage':'full_current_native_source_intake_mathematical_audit_pending',
    'mathematical_verdict':'not yet evaluated','source_verdict':'not yet evaluated','priority_verdict':'not yet evaluated',
    'completion_percent':5,'preprint_upload_cleared':False,'counts':[40,17,17,0],'goal_active_incomplete':True},indent=2)+'\n')
(D/'RESEARCH_LOG.md').write_text('# PR239 /30001321 research log\n\n'+utc+' — Best guess5% case completion. Current open draft head and exactly claimed_solved target QUEUE row authenticated; entire native attempt subtree frozen with size/SHA1/SHA256 identity for every file. Target positive d=1 all-scale RWRE concentration claim remains a hypothesis. Original author turn3/5 retained. No mathematical/source/priority acceptance, paper, upload, tracker or native merge.\n')
sel=json.loads((P/'CURRENT_GOAL_SELECTION_20261013.json').read_text())
sel.update(utc=utc,current_PR=239,problem_id='30001321',current_PR_head=head,original_PR_head=head,
           status_at_current_PR_head='claimed_solved',Queue_blob=q['sha'],original_Queue_blob=q['sha'],
           current_stage='full_current_native_source_intake_mathematical_audit_pending',case_completion_percent=5,
           native_source_prefix=prefix,current_DOI=None,current_tracker_range=None,program_counts=[40,17,17,0])
sel['skip_PRs']=sorted(set(sel['skip_PRs']+[246,245,244,243,242,241,240]),reverse=True)
sel['skip_reasons'].update({'246':'Complete earlier stationary-law coverage; credited already_solved correction','245':'unsolved','244':'unsolved','243':'unsolved','242':'already_solved','241':'unsolved','240':'unsolved'})
sel['previous_scope_skip_PR']=246
sel['previous_scope_skip_reason']='Complete earlier mathematical coverage; credit repair applied and scope skip'
sel['priority_classification_repairs_required']=[]
sel.pop('classification_repair_receipt',None)
sel.pop('next_descending_start_PR',None)
(P/'CURRENT_GOAL_SELECTION_20261013.json').write_text(json.dumps(sel,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+utc+' — PR246 credited already_solved repair head d9fd2b8d1b278430cbf6cb3ae25abd0f9a422034 and main checkpoint3479b3af811083271bc6d3366c760f54bdeb1d48 verified; scope skip with no paper/upload/tracker/merge/close/comment. PR245..240 current nonclaimed statuses skipped without science review/mutation. PR239 /30001321 current claimed_solved selected; entire native attempt subtree frozen, initial5%, author3/5. No theorem/source/priority acceptance. Fresh oldest500 inventory spans20..636 and covers descending range. Counts40/17/17/0, held293/292/280 uncompleted; whole goal active/incomplete.\n')
print(json.dumps({'PR':239,'head':head,'files':len(pins),'bytes':sum(x['bytes'] for x in pins),
                  'status':'claimed_solved','case_percent':5},indent=2))
print(json.dumps([{'path':x['native_path'].removeprefix(prefix),'bytes':x['bytes']} for x in pins],indent=2))
