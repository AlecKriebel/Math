"""Full recursive receipt and decompressed-stream comparison, without projections."""
from pathlib import Path,PurePosixPath
import datetime,gzip,hashlib,json
A=Path(__file__).resolve().parent;C=A/'clean_final_adversary/final_live'
LABELS=['agent_20261003_exact_live_02','root_20261003_exact_live_01']
def sha(b):return hashlib.sha256(b).hexdigest()
def differences(a,b,p=''):
 assert type(a)==type(b),(p,type(a),type(b));out=[]
 if isinstance(a,dict):
  assert a.keys()==b.keys(),p
  for k in sorted(a):out+=differences(a[k],b[k],p+'/'+str(k))
 elif isinstance(a,list):
  assert len(a)==len(b),p
  for i,(x,y) in enumerate(zip(a,b)):out+=differences(x,y,p+'/'+str(i))
 elif a!=b:out.append({'path':p,'whole':a,'root':b})
 return out
def mf(root,count):
 obj=json.loads((root/'PUBLIC_MANIFEST.json').read_bytes());seen=set()
 for row in obj['files']:
  p=PurePosixPath(row['path']);assert not p.is_absolute() and '..' not in p.parts and row['path'] not in seen;seen.add(row['path'])
  f=root/p;assert not f.is_symlink() and f.resolve().is_relative_to(root.resolve());raw=f.read_bytes();assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
 assert len(seen)==count and 'PUBLIC_MANIFEST.json' not in seen
 return sha((root/'PUBLIC_MANIFEST.json').read_bytes())
top=mf(C,18);receipts=[]
for label in LABELS:
 root=C/'runs'/label;mf(root,4);obj=json.loads((root/'FULL_GATE.json').read_bytes());seal=json.loads((root/'SEAL.json').read_bytes())
 assert obj['status']=='PASS_EXACT_LIVE' and obj['label']==label and obj['check_count']==929 and len(obj['checks'])==929 and all(r['pass'] for r in obj['checks'])
 assert seal['full_gate_sha256']==sha((root/'FULL_GATE.json').read_bytes()) and seal['program_sha256']==obj['program_sha256']==sha((C/'exact_live_gate.py').read_bytes())
 assert seal['expected_pins']==obj['expected_pins'] and seal['original_frozen_manifest_sha256']==sha((C.parent/'PUBLIC_MANIFEST.json').read_bytes())
 start=datetime.datetime.fromisoformat(obj['started_utc']);end=datetime.datetime.fromisoformat(obj['finished_utc']);assert start<=end and start.utcoffset()==end.utcoffset()==datetime.timedelta(0)
 for phase in ['start','end']:
  t=datetime.datetime.fromisoformat(obj[phase]['utc']);assert start<=t<=end and t.utcoffset()==datetime.timedelta(0)
 for s in obj['fresh_primary_sources']:
  t0=datetime.datetime.fromisoformat(s['started_utc']);t1=datetime.datetime.fromisoformat(s['finished_utc']);assert start<=t0<=t1<=end and t0.utcoffset()==t1.utcoffset()==datetime.timedelta(0)
  raw=(C/'private'/label/'primary'/s['file']).read_bytes();assert s['matches'] and not s['returncode'] and len(raw)==s['bytes'] and sha(raw)==s['sha256']
 receipts.append(obj)
x,y=receipts;stream_pairs=[];raw_api_diffs={};allowed=set()
def walk(a,b,p=''):
 assert type(a)==type(b),p
 if isinstance(a,dict):
  assert a.keys()==b.keys(),p
  if 'private_stream' in a:
   raw=[]
   for obj,label in [(a,LABELS[0]),(b,LABELS[1])]:
    path=PurePosixPath(obj['private_stream']);assert path.parts[:2]==('private',label) and '..' not in path.parts
    z=(C/path).read_bytes();q=gzip.decompress(z);assert len(z)==obj['gzip_bytes'] and len(q)==obj['bytes'] and sha(q)==obj['sha256'];raw.append(q)
   assert PurePosixPath(a['private_stream']).parts[2:]==PurePosixPath(b['private_stream']).parts[2:]
   allowed.add(p+'/private_stream')
   if raw[0]!=raw[1]:
    assert p in ['/start/raw_streams/0/stdout','/end/raw_streams/0/stdout'],p
    obs=[json.loads(q) for q in raw];ds=differences(*obs)
    permitted={'/'+side+'/repo/'+key for side in ['base','head'] for key in ['open_issues','open_issues_count','pushed_at','size']}
    assert {d['path'] for d in ds}<=permitted,ds
    for row in obs:
     assert row['head']['sha']==x['expected_pins']['head'] and row['base']['sha']==x['expected_pins']['base'] and row['state']=='open' and not row['draft']
     assert sha(row['body'].encode())==x['expected_pins']['body_sha256']
     for side in ['base','head']:
      r=row[side]['repo'];assert r['full_name']=='AlecKriebel/Math' and r['open_issues']==r['open_issues_count']>=0 and r['size']>=0
      datetime.datetime.strptime(r['pushed_at'],'%Y-%m-%dT%H:%M:%SZ')
    raw_api_diffs[p]=ds;allowed.update({p+'/sha256',p+'/gzip_bytes',p+'/bytes'})
   stream_pairs.append({'receipt_path':p,'whole':a,'root':b,'full_bytes_equal':raw[0]==raw[1]})
  for k in sorted(a):walk(a[k],b[k],p+'/'+str(k))
 elif isinstance(a,list):
  assert len(a)==len(b),p
  for i,(u,v) in enumerate(zip(a,b)):walk(u,v,p+'/'+str(i))
walk(x,y)
allowed|={'/label','/started_utc','/finished_utc','/start/utc','/end/utc'}
for i in range(5):allowed|={f'/fresh_primary_sources/{i}/started_utc',f'/fresh_primary_sources/{i}/finished_utc'}
diffs=differences(x,y);assert {d['path'] for d in diffs}<=allowed,diffs
assert x['checks']==y['checks'] and x['expected_pins']==y['expected_pins'] and x['start']['local_refs']==x['end']['local_refs']==y['start']['local_refs']==y['end']['local_refs']
root=json.loads((A/'root_exact_live_receipt.json').read_bytes());assert root['status']=='PASS_ROOT_EXACT_LIVE' and root['check_count']==1715 and all(c['pass'] for c in root['checks'])
assert root['reviewed_head']==x['expected_pins']['head'] and root['base']==x['expected_pins']['base'] and root['reviewed_tree']==x['expected_pins']['tree']
failed=json.loads((C/'runs/agent_20261003_exact_live_01/FULL_GATE.json').read_bytes());assert failed['status']=='REJECTED' and 'local main and tracking main exactly published base' in failed['error']
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ENTIRE_FINAL_LIVE_RECEIPTS','whole_receipt_sha256':sha((C/'runs'/LABELS[0]/'FULL_GATE.json').read_bytes()),'root_receipt_sha256':sha((C/'runs'/LABELS[1]/'FULL_GATE.json').read_bytes()),'root_separate_gate_sha256':sha((A/'root_exact_live_receipt.json').read_bytes()),'manifest_sha256':top,'public_bindings':18,'complete_equal_checks':929,'root_separate_checks':1715,'all_decompressed_stream_pairs':stream_pairs,'stream_pairs_count':len(stream_pairs),'runtime_differences':diffs,'raw_API_repository_metadata_differences':raw_api_diffs,'failed_stale_main_gate_retained':True,'actual_merge_pending':True}
(A/'root_final_live_comparison.json').write_text(json.dumps(out,indent=2)+'\n')
c=json.loads((A/'acceptance_criteria.json').read_bytes());c.update(workflow_completion_percent=95,exact_live_root_and_whole_gates_pending=False,fresh_whole_exact_live_pending=False,root_exact_live_checks=1715,fresh_whole_exact_live_checks=929,root_independent_full_whole_gate_checks=929,root_and_whole_entire_receipts_equal_after_validated_runtime_leaves=True,fresh_whole_final_additive_manifest_verified=True)
(A/'acceptance_criteria.json').write_text(json.dumps(c,indent=2)+'\n')
print(json.dumps({'status':out['status'],'complete_checks':929,'separate_root_checks':1715,'stream_pairs':len(stream_pairs),'validated_runtime_differences':len(diffs),'public_bindings':18},indent=2))
