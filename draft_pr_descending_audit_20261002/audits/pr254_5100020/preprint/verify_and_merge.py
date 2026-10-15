"""Read back exact reviewed native artifacts, then merge only the guarded PR254 head."""
from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, json, subprocess, time
HERE=Path(__file__).resolve().parent;ROOT=Path('/Users/alec/Documents/Math');PUB=HERE.parent/'publication';OUT=PUB/'native-readback-merge';OUT.mkdir(exist_ok=False)
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh';seq=0

def api(method,path,payload=None):
 global seq
 seq+=1;args=[GH,'api','--method',method,path]
 if payload is not None:
  f=OUT/f'{seq:02d}-request.json';f.write_text(json.dumps(payload));args+=['--input',str(f)]
 r=subprocess.run(args,capture_output=True);(OUT/f'{seq:02d}-stdout.json').write_bytes(r.stdout);(OUT/f'{seq:02d}-stderr.txt').write_bytes(r.stderr)
 if r.returncode:raise RuntimeError(f'Native call {seq} failed; reconcile readback before retrying any action')
 return json.loads(r.stdout)
B='repos/AlecKriebel/Math/';ready=json.loads((PUB/'PR_PREPARED.json').read_text());head=ready['prepared_head'];clear=json.loads((HERE/'FINAL_CLEARANCE.json').read_text());assert clear['mathematical_verdict']=='PASS' and clear['fresh_clean_reviews']>=2
z=json.loads((PUB/'ZENODO_VERIFIED_PUBLICATION.json').read_text());t=json.loads((PUB/'TRACKER_VERIFIED_APPEND.json').read_text());assert z['submitted'] and z['metadata_and_files_verified'] and t['verified'] and t['doi_url']==z['doi_url']
pr=api('GET',B+'pulls/254');assert pr['state']=='open' and not pr['merged'] and pr['head']['sha']==head
pins=[]
def match(local,native):
 data=local.read_bytes();obj=api('GET',B+'contents/'+native+'?ref='+head)
 if obj.get('encoding')=='base64':remote=base64.b64decode(obj['content'])
 else:remote=base64.b64decode(api('GET',B+'git/blobs/'+obj['sha'])['content'])
 assert remote==data,native+' bytes differ from guarded prepared file'
 pins.append({'native_path':native,'native_blob':obj['sha'],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
for f in sorted((HERE/'pr_update/5100020').rglob('*')):
 if f.is_file():match(f,'unsolved_math_prioritization/attempts/5100020/'+f.relative_to(HERE/'pr_update/5100020').as_posix())
for n,pin in clear['candidate_files'].items():
 f=HERE/n;assert len(f.read_bytes())==pin['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==pin['sha256'];match(f,f.relative_to(ROOT).as_posix())
q=api('GET',B+'contents/unsolved_math_prioritization/QUEUE.md?ref='+head);qt=base64.b64decode(q['content']).decode();row=next(x for x in qt.splitlines() if '5100020 / AMR-050-0020' in x);assert row==ready['target_queue_row'] and row.split('|')[8].strip()=='claimed_solved' and z['doi_url'] in row
r={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','head':head,'source_and_candidate_files':pins,'queue_row':row,'metadata_and_files_verified':True,'tracker_verified':True};(PUB/'NATIVE_SCIENTIFIC_READBACK.json').write_text(json.dumps(r,indent=2)+'\n')
# Ready-for-review is a necessary step in this explicitly authorized native merge.
if pr['draft']:
 out=api('POST','graphql',{'query':'mutation($id: ID!) { markPullRequestReadyForReview(input:{pullRequestId:$id}) { pullRequest { id isDraft } } }','variables':{'id':pr['node_id']}})
 assert not out.get('errors') and out['data']['markPullRequestReadyForReview']['pullRequest']['isDraft'] is False
for attempt in range(5):
 pr=api('GET',B+'pulls/254');assert pr['state']=='open' and not pr['merged'] and not pr['draft'] and pr['head']['sha']==head
 if pr['mergeable'] is not None:break
 time.sleep(3)
assert pr['mergeable'] is True, 'Merge conflict or unavailable mergeability; reconcile without forced ref'
request={'sha':head,'merge_method':'merge','commit_title':'Merge PR #254: audited odd-origin pedal-antipedal invariant k403,a'};(PUB/'NATIVE_MERGE_REQUEST.json').write_text(json.dumps(request,indent=2)+'\n')
result=api('PUT',B+'pulls/254/merge',request);assert result['merged'] is True
pr=api('GET',B+'pulls/254');assert pr['merged'] is True and pr['state']=='closed' and pr['merge_commit_sha']==result['sha'] and pr['head']['sha']==head
r={'utc':datetime.now(timezone.utc).isoformat(),'PR':254,'url':pr['html_url'],'merged':True,'merge_commit':result['sha'],'reviewed_head':head,'doi_url':z['doi_url'],'tracker_range':t['updated_range'],'case_completion_percent':100,'program_counts':{'completed':39,'preprints':16,'native_merges':16,'pending_tracker_rows':0}};(PUB/'PR_MERGED.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
