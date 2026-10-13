"""Compare every receipt leaf and every retained complete stream, without projections."""
from pathlib import Path, PurePosixPath
import datetime, gzip, hashlib, json
A = Path(__file__).resolve().parent
C = A / 'clean_final_adversary/post_merge'
LABELS = ['agent_20261003_post_merge_02', 'root_20261003_post_merge_02']
def sha(b): return hashlib.sha256(b).hexdigest()
def diffs(a,b,p=''):
    assert type(a) == type(b), (p,type(a),type(b))
    out=[]
    if isinstance(a,dict):
        assert a.keys()==b.keys(),p
        for k in sorted(a): out += diffs(a[k],b[k],p+'/'+str(k))
    elif isinstance(a,list):
        assert len(a)==len(b),p
        for i,(x,y) in enumerate(zip(a,b)): out += diffs(x,y,p+'/'+str(i))
    elif a != b: out.append({'path':p,'whole':a,'root':b})
    return out
def manifest(root,count):
    raw=(root/'PUBLIC_MANIFEST.json').read_bytes(); obj=json.loads(raw); seen=set()
    for row in obj['files']:
        p=PurePosixPath(row['path']); assert not p.is_absolute() and '..' not in p.parts
        assert row['path'] not in seen; seen.add(row['path']); f=root/p
        assert not f.is_symlink() and f.resolve().is_relative_to(root.resolve())
        b=f.read_bytes(); assert len(b)==row['bytes'] and sha(b)==row['sha256']
    assert len(seen)==count and 'PUBLIC_MANIFEST.json' not in seen
    return sha(raw)
top=manifest(C,19)
assert top=='6a72d3dd3c12712e4136fbf950410333da1a501790e402e2ba63d89f8015b7e1'
original=manifest(C.parent,19); prior=manifest(C.parent/'final_live',18)
receipts=[]
for label in LABELS:
    run=C/'runs'/label; manifest(run,4)
    raw=(run/'FULL_GATE.json').read_bytes(); obj=json.loads(raw); seal=json.loads((run/'SEAL.json').read_bytes())
    assert obj['label']==label and obj['status']=='PASS_POST_MERGE'
    assert obj['check_count']==1439 and len(obj['checks'])==1439 and all(x['pass'] for x in obj['checks'])
    assert seal['full_gate_sha256']==sha(raw) and seal['program_sha256']==obj['program_sha256']==sha((C/'verify_post_merge.py').read_bytes())
    assert seal['expected_pins']==obj['expected_pins'] and seal['original_frozen_manifest_sha256']==original and seal['prior_final_live_manifest_sha256']==prior
    start=datetime.datetime.fromisoformat(obj['started_utc']); end=datetime.datetime.fromisoformat(obj['finished_utc'])
    assert start<=end and start.utcoffset()==end.utcoffset()==datetime.timedelta(0)
    for value in [obj['start']['utc'],obj['end']['utc'],obj['pre_replay_code_bindings']['utc']]:
        t=datetime.datetime.fromisoformat(value); assert start<=t<=end and t.utcoffset()==datetime.timedelta(0)
    for s in obj['fresh_primary_sources']:
        t0=datetime.datetime.fromisoformat(s['started_utc']); t1=datetime.datetime.fromisoformat(s['finished_utc']); assert start<=t0<=t1<=end
        assert t0.utcoffset()==t1.utcoffset()==datetime.timedelta(0)
        b=(C/'private'/label/'primary'/s['file']).read_bytes(); assert s['matches'] and s['returncode']==0 and len(b)==s['bytes'] and sha(b)==s['sha256']
    inventory=obj['complete_private_stream_inventory']; assert len(inventory)==174
    paths=[r['private_stream'] for r in inventory]; assert len(set(paths))==174
    actual={str(p.relative_to(C)) for p in (C/'private'/label).rglob('*.gz') if p.is_file()}
    assert set(paths)==actual,(label,set(paths)^actual)
    receipts.append(obj)
x,y=receipts; allowed=set(); pairs=[]; observed={}; raw_api_diffs={}
def walk(a,b,p=''):
    assert type(a)==type(b),p
    if isinstance(a,dict):
        assert a.keys()==b.keys(),p
        if 'private_stream' in a:
            raw=[]
            for row,label in [(a,LABELS[0]),(b,LABELS[1])]:
                q=PurePosixPath(row['private_stream']); assert q.parts[:2]==('private',label) and '..' not in q.parts
                path=C/q; assert not path.is_symlink() and path.resolve().is_relative_to((C/'private'/label).resolve())
                z=path.read_bytes(); data=gzip.decompress(z)
                assert len(z)==row['gzip_bytes'] and len(data)==row['bytes'] and sha(data)==row['sha256']
                if 'complete_JSON_canonical_sha256' in row:
                    obj=json.loads(data); canonical=json.dumps(obj,sort_keys=True,separators=(',',':')).encode()
                    assert sha(canonical)==row['complete_JSON_canonical_sha256']
                    assert row['complete_top_level_fields']==(sorted(obj) if isinstance(obj,dict) else None)
                    assert row['complete_top_level_items']==(len(obj) if isinstance(obj,list) else None)
                raw.append(data)
            suffix=PurePosixPath(a['private_stream']).parts[2:]
            assert suffix==PurePosixPath(b['private_stream']).parts[2:]
            allowed.add(p+'/private_stream')
            if raw[0]!=raw[1]:
                assert suffix in [('api','start_pr.stdout.gz'),('api','end_pr.stdout.gz')],(p,suffix)
                values=[json.loads(q) for q in raw]; ds=diffs(*values)
                permitted={'/'+side+'/repo/'+key for side in ['base','head'] for key in ['open_issues','open_issues_count','pushed_at','size']}
                assert {d['path'] for d in ds}<=permitted,ds
                for v in values:
                    pins=x['expected_pins']; assert v['head']['sha']==pins['head'] and v['base']['sha']==pins['base']
                    assert v['state']=='closed' and not v['draft'] and v['merged'] is True and v['merge_commit_sha']==pins['merge_commit'] and v['merged_at']==pins['merged_at']
                    assert sha(v['body'].encode())==pins['body_sha256']
                    for side in ['base','head']:
                        r=v[side]['repo']; assert r['full_name']=='AlecKriebel/Math' and r['open_issues']==r['open_issues_count']>=0 and r['size']>=0
                        datetime.datetime.strptime(r['pushed_at'],'%Y-%m-%dT%H:%M:%SZ')
                raw_api_diffs[p]=ds
                for k in ['sha256','gzip_bytes','bytes','complete_JSON_canonical_sha256']:
                    if k in a: allowed.add(p+'/'+k)
            record={'relative_suffix':'/'.join(suffix),'receipt_path':p,'whole':a,'root':b,'full_bytes_equal':raw[0]==raw[1]}
            key='/'.join(suffix)
            if key in observed:
                assert observed[key]['whole']['sha256']==a['sha256'] and observed[key]['root']['sha256']==b['sha256']
            observed[key]=record; pairs.append(record)
        for k in sorted(a): walk(a[k],b[k],p+'/'+str(k))
    elif isinstance(a,list):
        assert len(a)==len(b),p
        for i,(u,v) in enumerate(zip(a,b)): walk(u,v,p+'/'+str(i))
walk(x,y)
assert len(observed)==174 and set(observed)=={str(PurePosixPath(r['private_stream']).relative_to(PurePosixPath('private')/LABELS[0])) for r in x['complete_private_stream_inventory']}
allowed|={'/label','/started_utc','/finished_utc','/start/utc','/end/utc','/pre_replay_code_bindings/utc'}
for i in range(5): allowed|={f'/fresh_primary_sources/{i}/started_utc',f'/fresh_primary_sources/{i}/finished_utc'}
changes=diffs(x,y); assert {r['path'] for r in changes}<=allowed,[r for r in changes if r['path'] not in allowed]
assert x['checks']==y['checks'] and x['expected_pins']==y['expected_pins']
assert x['start']['local_refs']==x['end']['local_refs']==y['start']['local_refs']==y['end']['local_refs']
actual=json.loads((A/'ACTUAL_MERGE_VERIFICATION.json').read_bytes())
assert actual['status']=='unsolved' and actual['actual_merge']==x['expected_pins']['merge_commit']
assert actual['reviewed_head']==x['expected_pins']['head'] and actual['actual_parents']==x['expected_pins']['merge_ordered_parents']
assert actual['all_expected_paths_exact']==50 and actual['all_target_file_hashes_exact']==49 and actual['queue_physical_line']==404 and actual['only_queue_pipe_cells']==[8,9] and actual['all_other_queue_bytes_equal']
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ENTIRE_POST_MERGE_RECEIPTS','manifest_sha256':top,'public_bindings':19,'whole_receipt_sha256':sha((C/'runs'/LABELS[0]/'FULL_GATE.json').read_bytes()),'root_receipt_sha256':sha((C/'runs'/LABELS[1]/'FULL_GATE.json').read_bytes()),'equal_checks':1439,'distinct_complete_private_stream_pairs':174,'nested_stream_reference_pairs':len(pairs),'streams':list(observed.values()),'all_runtime_differences':changes,'full_raw_API_repository_metadata_differences':raw_api_diffs,'prior_failed_inspections_and_passing_v1_runs_preserved':True,'original_and_final_live_manifests_reverified':True,'original_problem_resolution_percent':0,'workflow_completion_percent':100}
(A/'root_postmerge_comparison.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','equal_checks','distinct_complete_private_stream_pairs','nested_stream_reference_pairs','workflow_completion_percent']},indent=2))
