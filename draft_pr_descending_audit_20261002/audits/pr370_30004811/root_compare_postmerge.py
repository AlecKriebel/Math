"""Validate every actual readback field and each compressed stream in both runs."""
from pathlib import Path,PurePosixPath
import datetime,gzip,hashlib,json
A=Path(__file__).resolve().parent;C=A/'clean_final_adversary/post_merge'
def sha(b):return hashlib.sha256(b).hexdigest()
def diff(a,b,p=''):
    assert type(a)==type(b),(p,type(a),type(b));out=[]
    if isinstance(a,dict):
        assert a.keys()==b.keys(),p
        for k in a:out+=diff(a[k],b[k],p+'/'+k)
    elif isinstance(a,list):
        assert len(a)==len(b),p
        for i,(u,v) in enumerate(zip(a,b)):out+=diff(u,v,p+'/'+str(i))
    elif a!=b:out.append({'path':p,'independent':a,'root':b})
    return out
x=json.loads((C/'RECEIPT_actual02.json').read_bytes());y=json.loads((C/'RECEIPT_root_replay_01.json').read_bytes())
ds=diff(x,y);allowed={'/started_utc','/completed_utc','/label','/private_run_relative','/commands/initial_pr/stdout_sha256','/commands/final_pr/stdout_sha256'}
assert {d['path'] for d in ds}<=allowed,ds
for j,label in [(x,'actual02'),(y,'root_replay_01')]:
    assert j['status']=='PASS_ACTUAL_POST_MERGE_QUALIFIED' and len(j['checks'])==157 and all(c['pass'] for c in j['checks'])
    assert j['label']==label and j['private_run_relative']=='private/'+label
    assert j['program_sha256']==sha((C/'post_merge_gate.py').read_bytes()) and j['pins_sha256']==sha((C/'PINS.json').read_bytes())
    t0=datetime.datetime.fromisoformat(j['started_utc']);t1=datetime.datetime.fromisoformat(j['completed_utc'])
    assert t0<=t1 and t0.utcoffset()==t1.utcoffset()==datetime.timedelta(0)
    assert len(j['commands'])==163
    for name,row in j['commands'].items():
        assert row['returncode']==0
        for stream in ['stdout','stderr']:
            b=gzip.decompress((C/'private'/label/(name+'.'+stream+'.gz')).read_bytes())
            assert len(b)==row[stream+'_bytes'] and sha(b)==row[stream+'_sha256']
api_diffs={}
for phase in ['initial_pr','final_pr']:
    a=json.loads(gzip.decompress((C/'private/actual02'/(phase+'.stdout.gz')).read_bytes()))
    b=json.loads(gzip.decompress((C/'private/root_replay_01'/(phase+'.stdout.gz')).read_bytes()))
    ad=diff(a,b)
    permitted={'/'+side+'/repo/'+k for side in ['base','head'] for k in ['open_issues','open_issues_count','pushed_at','size']}
    assert {d['path'] for d in ad}<=permitted,ad
    for obs in [a,b]:
        for side in ['base','head']:
            r=obs[side]['repo'];assert r['full_name']=='AlecKriebel/Math' and r['open_issues']==r['open_issues_count']>=0 and r['size']>=0
            datetime.datetime.strptime(r['pushed_at'],'%Y-%m-%dT%H:%M:%SZ')
    api_diffs[phase]=ad
for D,count,sealname in [(C,9,'POST_MERGE_SEAL.json'),(A/'clean_final_adversary/final_live',9,'FINAL_LIVE_SEAL.json')]:
    m=json.loads((D/'PUBLIC_MANIFEST.json').read_bytes());seen=set()
    for r in m['files']:
        p=PurePosixPath(r['path']);assert len(p.parts)==1 and r['path'] not in seen and not p.is_absolute();seen.add(r['path'])
        f=D/p;assert not f.is_symlink();b=f.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
    assert len(seen)==count and m['self_excluded']=='PUBLIC_MANIFEST.json'
    seal=json.loads((D/sealname).read_bytes())
    for p,h in seal['files'].items():assert sha((D/p).read_bytes())==h
assert x['observations']==y['observations']
(A/'root_postmerge_receipt.json').write_bytes((C/'RECEIPT_root_replay_01.json').read_bytes())
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','checks':157,'actual_merge':y['pins']['accepted_merge'],'complete_receipts_compared':True,'all_163_command_stream_pairs_validated_per_run':True,'all157_check_records_and_observations_equal':True,'runtime_differences':ds,'raw_API_repository_metadata_differences':api_diffs,'original_and_final_live_manifests_preserved':True,'postmerge_manifest_sha256':sha((C/'PUBLIC_MANIFEST.json').read_bytes()),'whole_receipt_sha256':sha((C/'RECEIPT_actual02.json').read_bytes()),'root_receipt_sha256':sha((A/'root_postmerge_receipt.json').read_bytes()),'program_sha256':sha(Path(__file__).read_bytes())}
(A/'root_postmerge_comparison.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','actual_merge':out['actual_merge'],'checks':157,'complete_check_records_equal':True,'runtime_differences':len(ds)}))
