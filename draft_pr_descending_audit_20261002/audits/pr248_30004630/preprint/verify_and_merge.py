"""Read back the actual reviewed native PR248 bytes before the authorized merge."""
from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, json, subprocess, time
PRE=Path(__file__).resolve().parent
ROOT=Path('/Users/alec/Documents/Math')
PUB=PRE.parent/'publication'
OUT=PUB/('native-readback-merge-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
OUT.mkdir(exist_ok=False)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
B='repos/AlecKriebel/Math/'
seq=0

def api(method,path,payload=None,graphql=False):
    global seq
    seq+=1;args=[GH,'api','--method',method,path if graphql else B+path]
    if payload is not None:
        f=OUT/f'{seq:02d}-request.json';f.write_text(json.dumps(payload));args+=['--input',str(f)]
    r=subprocess.run(args,capture_output=True)
    (OUT/f'{seq:02d}-stdout.json').write_bytes(r.stdout)
    (OUT/f'{seq:02d}-stderr.txt').write_bytes(r.stderr)
    if r.returncode:raise RuntimeError(f'Native call {seq} failed; reconcile before another mutation')
    return json.loads(r.stdout)

assert not (PUB/'PR_MERGED.json').exists(), 'Merge already confirmed; only read-only reconciliation allowed'
prepared=json.loads((PUB/'PR_PREPARED.json').read_text())
head=prepared['prepared_head']
clear=json.loads((PRE/'FINAL_CLEARANCE.json').read_text())
assert clear['mathematical_verdict']=='PASS' and clear['fresh_clean_reviews']>=3
z=json.loads((PUB/'ZENODO_VERIFIED_PUBLICATION.json').read_text())
t=json.loads((PUB/'TRACKER_VERIFIED_APPEND.json').read_text())
assert z['submitted'] and z['metadata_and_files_verified'] and t['verified'] and t['doi_url']==z['doi_url']
pr=api('GET','pulls/248')
assert pr['state']=='open' and not pr['merged'] and pr['head']['sha']==head
case_prefix=PRE.parent.relative_to(ROOT).as_posix()+'/'
tree_sha=prepared['tree']
for part in PRE.parent.relative_to(ROOT).parts:
    level=api('GET','git/trees/'+tree_sha)
    assert not level['truncated']
    entry=next(p for p in level['tree'] if p['path']==part)
    assert entry['type']=='tree'
    tree_sha=entry['sha']
tree=api('GET','git/trees/'+tree_sha+'?recursive=1')
assert not tree['truncated']
native={case_prefix+p['path']:p for p in tree['tree']}
identities=[]
for p in prepared['included_owned_pins']:
    data=(ROOT/p['path']).read_bytes()
    assert len(data)==p['bytes'] and hashlib.sha256(data).hexdigest()==p['sha256']
    sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert native[p['path']]['sha']==sha and native[p['path']]['type']=='blob'
    identities.append({'path':p['path'],'native_blob_sha1':sha,'bytes':len(data),'sha256':p['sha256'],'native_tree_identity_verified':True})
pins=[]
def match(local,path):
    data=local.read_bytes();obj=api('GET','contents/'+path+'?ref='+head)
    if obj.get('encoding')=='base64':remote=base64.b64decode(obj['content'])
    else:remote=base64.b64decode(api('GET','git/blobs/'+obj['sha'])['content'])
    assert remote==data,path+' differs from prepared reviewed bytes'
    pins.append({'native_path':path,'native_blob':obj['sha'],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})

staged=PRE/'pr_update/30004630'
for f in sorted(staged.rglob('*')):
    if f.is_file():match(f,'unsolved_math_prioritization/attempts/30004630/'+f.relative_to(staged).as_posix())
for name,pin in clear['candidate_files'].items():
    f=PRE/name;data=f.read_bytes()
    assert len(data)==pin['bytes'] and hashlib.sha256(data).hexdigest()==pin['sha256']
    match(f,f.relative_to(ROOT).as_posix())
q=api('GET','contents/unsolved_math_prioritization/QUEUE.md?ref='+head)
qt=base64.b64decode(q['content']).decode()
row=next(x for x in qt.splitlines() if '30004630 / OWR-4990378-001' in x)
assert row==prepared['target_queue_row'] and row.split('|')[8].strip()=='claimed_solved' and z['doi_url'] in row
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','head':head,
         'actual_source_and_candidate_readbacks':pins,'all_included_owned_native_tree_identities':identities,
         'queue_row':row,'metadata_and_files_verified':True,'tracker_verified':True}
(PUB/'NATIVE_SCIENTIFIC_READBACK.json').write_text(json.dumps(receipt,indent=2)+'\n')
if pr['draft']:
    result=api('POST','graphql',{'query':'mutation($id: ID!) { markPullRequestReadyForReview(input:{pullRequestId:$id}) { pullRequest { id isDraft } } }','variables':{'id':pr['node_id']}},graphql=True)
    assert not result.get('errors') and result['data']['markPullRequestReadyForReview']['pullRequest']['isDraft'] is False
for attempt in range(5):
    pr=api('GET','pulls/248')
    assert pr['state']=='open' and not pr['merged'] and not pr['draft'] and pr['head']['sha']==head
    if pr['mergeable'] is not None:break
    time.sleep(3)
assert pr['mergeable'] is True,'Native conflict or unknown mergeability; resolve without forcing main'
request={'sha':head,'merge_method':'merge','commit_title':'Merge PR #248: audited critical-wave unregularized quadratic-growth counterexample'}
(PUB/'NATIVE_MERGE_REQUEST.json').write_text(json.dumps(request,indent=2)+'\n')
result=api('PUT','pulls/248/merge',request)
assert result['merged'] is True
pr=api('GET','pulls/248')
assert pr['merged'] and pr['state']=='closed' and pr['merge_commit_sha']==result['sha'] and pr['head']['sha']==head
receipt={'utc':datetime.now(timezone.utc).isoformat(),'PR':248,'url':pr['html_url'],'merged':True,
         'merge_commit':result['sha'],'reviewed_head':head,'doi_url':z['doi_url'],
         'tracker_range':t['updated_range'],'case_completion_percent':100,
         'program_counts':{'completed':40,'preprints':17,'native_merges':17,'pending_tracker_rows':0}}
(PUB/'PR_MERGED.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
