"""Materialize already independently authenticated read-only connector bytes."""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def enc(j):return (json.dumps(j,indent=2)+'\n').encode()
def save(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
 p.chmod(0o444)
j=json.loads((A/'private_ram_materialization_payload.json').read_bytes());i=json.loads((A/'ORIGINAL_STATUS_INTAKE.json').read_bytes())
assert i['eligible'] and i['original_QUEUE_status']=='claimed_solved' and i['PR']==203 and i['problem_id']==5100011
HEAD=i['original_submitted_head'];co=j['original_commit'];pr=j['PR_metadata'];NATIVE='unsolved_math_prioritization/attempts/5100011/';Q='unsolved_math_prioritization/QUEUE.md'
assert HEAD==co['sha']==pr['head']['sha']=='8edca9d773c085adb4ed0611357a7a2957e3395d'
assert co['tree']['sha']==i['head_tree'] and [x['sha'] for x in co['parents']]==[i['head_sole_parent']]
assert pr['state']=='open' and pr['draft'] and not pr['merged'] and pr['created_at']==pr['updated_at']==i['created_at'] and pr['commits']==i['original_author_commit_count']==3
for ep,t in j['tree_metadata'].items():
 assert not t['truncated']
 raw=b''.join(x['mode'].lstrip('0').encode()+b' '+x['path'].encode()+b'\0'+bytes.fromhex(x['sha']) for x in sorted(t['tree'],key=lambda x:x['path'].encode()+(b'/' if x['type']=='tree' else b'')))
 assert hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==t['sha']==ep.split('/')[-1]
pins={};total=0
for rel,x in j['files'].items():
 assert not Path(rel).is_absolute() and '..' not in Path(rel).parts
 b=j['decoded_blob_texts'][x['sha']].encode('utf8');p=pin(b)
 assert p['bytes']==x['size'] and p['git_blob']==x['sha'] and p==j['verified_pins']['native_files'][rel]
 save(A/'original_submitted_head'/rel,b);pins[rel]={**p,'mode':'100644'};total+=len(b)
assert len(pins)==18 and total==59989 and sorted(j['full_original_tree_delta'])==sorted([Q]+[NATIVE+k for k in pins])
qr=j['verified_queue_receipt'];assert qr['original_QUEUE_blob']==i['original_QUEUE_blob'] and qr['foreign_QUEUE_rows_identical'] and qr['own_only_changed_row']
assert {k:qr['original_QUEUE_row'][k] for k in ['bytes','sha256']}==i['original_QUEUE_row']
meta={k:pr[k] for k in ['number','title','body','state','draft','merged','created_at','updated_at','commits','changed_files']};meta['original_head']=HEAD
save(A/'ORIGINAL_PR_METADATA.json',enc(meta))
r={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PR':203,'problem_id':5100011,'original_head':HEAD,'original_tree':co['tree']['sha'],'original_sole_parent':co['parents'][0]['sha'],'original_range_base':i['original_range_base'],'original_author_commit_count':3,'original_QUEUE_status':'claimed_solved','original_QUEUE_effort_cell':'2/5','files':pins,'file_count':18,'total_native_bytes':total,'complete_original_delta':sorted(j['full_original_tree_delta']),'complete_delta_is_exact_native_archive_plus_one_QUEUE_row':True,'foreign_QUEUE_rows_unchanged_at_original_submission':True,'original_QUEUE_blob':qr['original_QUEUE_blob'],'original_QUEUE_row':{k:qr['original_QUEUE_row'][k] for k in ['bytes','sha256']},'original_PR_metadata':{k:pin((A/'ORIGINAL_PR_METADATA.json').read_bytes())[k] for k in ['bytes','sha256']},'all_eight_nonrecursive_Git_tree_native_identities_verified':True,'all18_blob_native_identities_and_bytes_verified':True,'source_and_mathematical_clearance':False,'no_PR_or_native_MAIN_mutation':True,'custody_before_semantic_candidate_review':True,'transport':'Read-only connected GitHub Git-object metadata and decoded UTF8 blobs, all native identities recomputed; immutable raw GitHub QUEUE reads authenticated against original status receipt. CLI hourly rate limit bypassed by authorized connector, not a permission bypass.','resource_recovery':'Disk full; original bytes held and authenticated in memory before materialization after removing regenerable own completed-case page previews.'}
save(A/'ORIGINAL_SUBMISSION_CUSTODY.json',enc(r))
print(json.dumps({k:r[k] for k in ['UTC','PR','original_head','file_count','total_native_bytes','complete_delta_is_exact_native_archive_plus_one_QUEUE_row','source_and_mathematical_clearance']}))
