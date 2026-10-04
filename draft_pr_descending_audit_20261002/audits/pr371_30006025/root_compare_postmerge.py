"""Compare every independent post-merge receipt field; validate runtime differences."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json
A=Path(__file__).resolve().parent;C=A/'clean_final_adversary/post_merge'
def sha(b):return hashlib.sha256(b).hexdigest()
x=json.loads((C/'ACTUAL_MERGE_RECEIPT.json').read_bytes())
y=json.loads((A/'root_postmerge_independent_receipt.json').read_bytes())
differences=[]
def walk(a,b,p=''):
    assert type(a) is type(b),(p,type(a),type(b))
    if isinstance(a,dict):
        assert a.keys()==b.keys(),p
        for k in a:walk(a[k],b[k],p+'/'+str(k))
    elif isinstance(a,list):
        assert len(a)==len(b),p
        for i,(c,d) in enumerate(zip(a,b)):walk(c,d,p+'/'+str(i))
    elif a!=b:differences.append({'path':p,'independent':a,'root':b})
walk(x,y)
allowed={'/started_utc','/completed_utc','/raw_storage','/first_observation/utc','/last_observation/utc'}
assert {d['path'] for d in differences}==allowed
for r in [x,y]:
    assert r['status']=='PASS_ACTUAL_MERGE_SCOPED_UNSOLVED_5_OF_5'
    assert len(r['checks'])==30 and all(c['passed'] for c in r['checks'])
    times=[datetime.datetime.fromisoformat(r['started_utc']),datetime.datetime.fromisoformat(r['first_observation']['utc']),datetime.datetime.fromisoformat(r['last_observation']['utc']),datetime.datetime.fromisoformat(r['completed_utc'])]
    assert times==sorted(times) and all(t.utcoffset()==datetime.timedelta(0) for t in times)
    p=PurePosixPath(r['raw_storage']);assert len(p.parts)==2 and p.parts[0]=='private' and p.parts[1].startswith('run_') and '..' not in p.parts
assert x['program_sha256']==y['program_sha256']==sha((C/'check_actual_merge.py').read_bytes())
manifest=json.loads((C/'PUBLIC_MANIFEST.json').read_bytes());seen=set()
for e in manifest['files']:
    p=PurePosixPath(e['path']);assert not p.is_absolute() and '..' not in p.parts and e['path']!='PUBLIC_MANIFEST.json' and e['path'] not in seen;seen.add(e['path'])
    raw=(C/e['path']).read_bytes();assert len(raw)==e['bytes'] and sha(raw)==e['sha256']
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==e['git_blob_sha1']
assert len(seen)==7
seal=json.loads((C/'ACTUAL_MERGE_SEAL.json').read_bytes())
for e in seal['bound_files']:
    raw=(C/e['path']).read_bytes();assert len(raw)==e['bytes'] and sha(raw)==e['sha256']
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','all_receipt_fields_equal_except_validated_runtime_leaves':True,'runtime_differences':differences,'actual_merge':y['actual_merge'],'root_checks':30,'independent_checks':30,'postmerge_bound_files':len(seen),'manifest_sha256':sha((C/'PUBLIC_MANIFEST.json').read_bytes()),'program_sha256':sha(Path(__file__).read_bytes())}
(A/'root_postmerge_comparison.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
