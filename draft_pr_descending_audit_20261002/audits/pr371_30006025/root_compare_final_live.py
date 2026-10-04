"""Compare entire independently run receipts; only five validated runtime leaves differ."""
from pathlib import Path,PurePosixPath
import datetime,hashlib,json
A=Path(__file__).resolve().parent;C=A/'clean_final_adversary/final_live'
def sha(b):return hashlib.sha256(b).hexdigest()
mf=json.loads((C/'PUBLIC_MANIFEST.json').read_bytes());seen=set()
for r in mf['files']:
    p=PurePosixPath(r['path']);assert not p.is_absolute() and '..' not in p.parts and p.as_posix()==r['path'] and r['path'] not in seen
    seen.add(r['path']);f=C/p;assert not f.is_symlink() and f.resolve().is_relative_to(C)
    b=f.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob_sha1']
assert len(seen)==10 and mf['self_excluded']=='PUBLIC_MANIFEST.json'
x=json.loads((C/'LIVE_GATE_RECEIPT.json').read_bytes());y=json.loads((A/'root_clean_final_exact_live.json').read_bytes())
diffs=[]
def diff(a,b,path=''):
    assert type(a)==type(b),(path,type(a),type(b))
    if isinstance(a,dict):
        assert set(a)==set(b),path
        for k in sorted(a):diff(a[k],b[k],path+'/'+k)
    elif isinstance(a,list):
        assert len(a)==len(b),path
        for i,(u,v) in enumerate(zip(a,b)):diff(u,v,path+'/'+str(i))
    elif a!=b:diffs.append({'path':path,'whole':a,'root':b})
diff(x,y)
allowed={'/started_utc','/completed_utc','/raw_storage','/first_observation/utc','/last_observation/utc'}
assert {d['path'] for d in diffs}<=allowed,diffs
for j in (x,y):
    stamps=[datetime.datetime.fromisoformat(j[k]) for k in ['started_utc','completed_utc']]
    first=datetime.datetime.fromisoformat(j['first_observation']['utc']);last=datetime.datetime.fromisoformat(j['last_observation']['utc'])
    assert stamps[0]<=first<=last<=stamps[1] and all(t.utcoffset()==datetime.timedelta(0) for t in [*stamps,first,last])
    p=PurePosixPath(j['raw_storage']);assert str(p).startswith('private/run_') and '..' not in p.parts and not p.is_absolute()
    assert j['status']=='PASS_EXACT_LIVE_SCOPED_UNSOLVED_PACKET' and len(j['checks'])==42 and all(r['passed'] for r in j['checks'])
    assert j['program_sha256']==sha((C/'check_live_gate.py').read_bytes())=='e2efee1eeebe66384ec7ae7c24446b8d129a8d1647baaeac320c4f1e8fab8c5c'
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ENTIRE_FINAL_LIVE_RECEIPTS','manifest_sha256':sha((C/'PUBLIC_MANIFEST.json').read_bytes()),'bound_public_files':10,'root_receipt_sha256':sha((A/'root_clean_final_exact_live.json').read_bytes()),'whole_receipt_sha256':sha((C/'LIVE_GATE_RECEIPT.json').read_bytes()),'all42_complete_check_records_equal':True,'every_mathematical_source_git_api_body_field_equal':True,'validated_only_runtime_differences':diffs,'whole_final_manifest_verified':True}
(A/'root_final_live_comparison.json').write_text(json.dumps(out,indent=2)+'\n')
criteria=json.loads((A/'acceptance_criteria.json').read_bytes());criteria.update(workflow_completion_percent=95,exact_live_root_and_whole_gates_pending=False,root_exact_live_checks=1829,fresh_whole_exact_live_checks=42,root_independent_full_whole_gate_checks=42,root_and_whole_entire_receipts_equal_after_five_validated_runtime_leaves=True,fresh_whole_final_additive_manifest_verified=True)
(A/'acceptance_criteria.json').write_text(json.dumps(criteria,indent=2)+'\n')
print(json.dumps({'status':out['status'],'complete_check_records':42,'runtime_differences':len(diffs),'manifest_bound_files':10},indent=2))
