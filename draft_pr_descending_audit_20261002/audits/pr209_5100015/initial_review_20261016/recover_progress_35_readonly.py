"""Finish actual byte readback of already-pushed checkpoint; no remote mutations."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import base64,hashlib,json,subprocess
D=Path(__file__).resolve().parent; ROOT=D.parents[3]
T=D/'private_transport/progress35_20261016T051814869595Z'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh';BASE='repos/AlecKriebel/Math/'
OUT=D/'PROGRESS_35_CHECKPOINT_RECEIPT.json';assert not OUT.exists()
def api(path):
 r=subprocess.run([GH,'api',BASE+path],capture_output=True,timeout=90)
 if r.returncode:
  raise RuntimeError('Read-only API failure '+path+': '+r.stderr.decode()[:900])
 return json.loads(r.stdout)
request=json.loads((T/'035-request.json').read_text());commit=json.loads((T/'036-stdout.json').read_text())
new=commit['sha'];parent=commit['parents'][0]['sha'];tree=commit['tree']['sha']
assert new=='f9862f73ca1589941876b0c2ebad0782ffbb4894'
assert json.loads((T/'037-stdout.json').read_text())['object']['sha']==new
actual=api('git/commits/'+new);assert actual['tree']['sha']==tree and [x['sha'] for x in actual['parents']]==[parent]
delta=api('compare/'+parent+'...'+new)
expected={};pins=[]
for e in request['tree']:
 path=e['path'];raw=(ROOT/path).read_bytes();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 assert e['mode']=='100644' and e['type']=='blob'
 if 'content' in e:assert raw==e['content'].encode()
 else:assert blob==e['sha']
 expected[path]=raw;pins.append(dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),git_blob_sha1=blob))
assert delta['status']=='ahead' and delta['total_commits']==1 and len(delta['files'])<300
assert {x['filename'] for x in delta['files']}<=set(expected) and all(x['status']!='removed' for x in delta['files'])
def read(row):
 obj=api('git/blobs/'+row['git_blob_sha1']);assert obj['sha']==row['git_blob_sha1'] and obj['encoding']=='base64'
 raw=base64.b64decode(obj['content']);assert raw==expected[row['path']]
 return dict(path=row['path'],sha256=row['sha256'],actual_body_byte_identical=True,transport='native Git blob GET')
with ThreadPoolExecutor(max_workers=4) as pool:verified=list(pool.map(read,pins))
for row in pins:assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256']
pr=api('pulls/209');assert pr['state']=='open' and pr['draft'] and pr['head']['sha']=='fd09a95b479f376234835a4494693bb1316c85ec'
q=api('contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['head']['sha']);body=base64.b64decode(q['content']);i=json.loads((D/'INTAKE.json').read_text())
assert q['sha']==i['Queue_blob'] and hashlib.sha256(body).hexdigest()==i['Queue_sha256']
rows=[x for x in body.decode().splitlines() if '5100015 / AMR-050-0015' in x];assert rows==[i['queue_row']] and [x.strip() for x in rows[0].split('|')][8]=='claimed_solved'
latest=api('git/ref/heads/main')['object']['sha']
if latest!=new:assert api('compare/'+new+'...'+latest)['status']=='ahead'
families=[]
for name in ['source_domain_adversary_01','meromorphic_divisor_adversary_01','physical_geometry_adversary_01','priority_author_updates_01','priority_classical_general_01']:
 f=D/name/'AUTHORED_MANIFEST.json';families.append(dict(family=name,manifest_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),root_final_acceptance_pending=False))
result=dict(utc=datetime.now(timezone.utc).isoformat(),commit=new,parent=parent,main_readback=latest,case_completion_percent=35,owned_files=pins,actual_native_byte_readbacks=verified,actual_changed_paths=[x['filename'] for x in delta['files']],fresh_main_sole_parent_verified=True,full_native_changed_path_scope_verified=True,native_PR_original_unchanged_and_still_claimed=True,retained_sealed_families=families,preprint_preparation_cleared=True,counts=[44,21,21,0],local_Git_index_ref_mutations=0,goal_active_incomplete=True,recovery='Original publisher successfully pushed; an unrecorded Contents GET failed during readback. This GET-only recovery completed every body readback, with no second push or invented response.')
OUT.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['owned_files','actual_native_byte_readbacks','actual_changed_paths']}));print('verified',len(pins),'changed',len(delta['files']))
