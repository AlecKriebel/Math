"""Full stream/receipt comparison with explicit, validated runtime normalization."""
from pathlib import Path, PurePosixPath
import collections, datetime, gzip, hashlib, json
A=Path(__file__).resolve().parent; F=A/'clean_final_adversary/final_live'
RUNS=[F/'runs/clean_live_20261003_01',F/'private_runs/root_live_replay_01']
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(j):return json.dumps(j,sort_keys=True,separators=(',',':')).encode()
def differences(a,b,p=''):
    assert type(a)==type(b),(p,type(a),type(b))
    out=[]
    if isinstance(a,dict):
        assert a.keys()==b.keys(),p
        for k in sorted(a):out+=differences(a[k],b[k],p+'/'+str(k))
    elif isinstance(a,list):
        assert len(a)==len(b),p
        for i,(u,v) in enumerate(zip(a,b)):out+=differences(u,v,p+'/'+str(i))
    elif a!=b:out.append({'path':p,'whole':a,'root':b})
    return out
def manifest(root,count):
    m=json.loads((root/'PUBLIC_MANIFEST.json').read_bytes());seen=set()
    for r in m['files']:
        p=PurePosixPath(r['path']);assert not p.is_absolute() and '..' not in p.parts and r['path'] not in seen;seen.add(r['path'])
        f=root/p;assert not f.is_symlink() and f.resolve().is_relative_to(root.resolve());b=f.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256']
    assert len(seen)==count and 'PUBLIC_MANIFEST.json' not in seen
    return sha((root/'PUBLIC_MANIFEST.json').read_bytes())
assert manifest(F,1635)=='3c047d9b0663018219c9f6b4e6898a18175f75cd6e96ee6f93acfb1038d10445'
assert manifest(F.parent,47)=='bf7cece6ed2edc56f2b865baed9f0bcf9a13378511929c3f7f64d0cfb2144036'
objects=[json.loads((d/'RECEIPT.json').read_bytes()) for d in RUNS]
for j in objects:
    assert j['status']=='PASS exact live acceptance as unsolved5/5; actual merge pending' and j['check_count']==len(j['checks'])==8268 and all(r['pass'] for r in j['checks'])
    assert j['program_sha256']==sha((F/'audit_exact_live.py').read_bytes())
assert collections.Counter(canon(r) for r in objects[0]['checks'])==collections.Counter(canon(r) for r in objects[1]['checks'])
stream_pairs=[];normalization_ledger=[];api_differences=[];parsed_by_run=[];normalized=[]
def normalized_pull(v,pins):
    assert v['number']==368 and v['state']=='open' and not v['draft'] and not v['merged'] and v['head']['sha']==pins['head'] and v['base']['sha']==pins['base'] and sha(v['body'].encode())==pins['accepted_body_sha256']
    n=json.loads(json.dumps(v))
    for side in ['base','head']:
        r=v[side]['repo'];assert r['full_name']=='AlecKriebel/Math' and r['open_issues']==r['open_issues_count']>=0 and r['size']>=0
        datetime.datetime.strptime(r['pushed_at'],'%Y-%m-%dT%H:%M:%SZ')
        for key in ['open_issues','open_issues_count','pushed_at','size']:n[side]['repo'][key]='VALIDATED_CURRENT_REPOSITORY_'+key
    return n
def unstream(d,r):
    p=PurePosixPath(r['path']);assert p.parts[0]=='streams' and '..' not in p.parts and not p.is_absolute()
    f=d/p;assert not f.is_symlink();z=f.read_bytes();b=gzip.decompress(z)
    assert len(z)==r['gzip_bytes'] and sha(z)==r['gzip_sha256'] and len(b)==r['bytes'] and sha(b)==r['sha256']
    return b
capture_maps=[];capture_raw_maps=[];raw_stream_sets=[]
for d,j in zip(RUNS,objects):
    n=json.loads(json.dumps(j));start=datetime.datetime.fromisoformat(j['start_utc']);end=datetime.datetime.fromisoformat(j['end_utc']);assert start<=end
    def utc(value):
        t=datetime.datetime.fromisoformat(value);assert start<=t<=end and t.utcoffset()==datetime.timedelta(0)
    n['start_utc']=n['end_utc']='VALIDATED_RUN_UTC'
    for phase in ['before','after']:
        utc(j[phase]['utc']);n[phase]['utc']='VALIDATED_BOUNDARY_UTC';n[phase]['pull']=normalized_pull(j[phase]['pull'],j['pins'])
    for s,t in zip(j['all11_new_live_source_retrievals'],n['all11_new_live_source_retrievals']):
        utc(s['live_download_start_utc']);utc(s['live_download_end_utc']);assert s['live_download_start_utc']<=s['live_download_end_utc']
        b=(d/'private/sources'/s['name']).read_bytes();assert len(b)==s['actual_bytes']==s['bytes'] and sha(b)==s['actual_sha256']==s['sha256']
        t['live_download_start_utc']=t['live_download_end_utc']='VALIDATED_FRESH_SOURCE_UTC'
    cm={};rawmap={};occ=collections.Counter();seen=set();by_id={};parsed=[]
    for cap in j['complete_captures']:
        assert cap['exit_code']==0 and cap['id'] not in by_id;by_id[cap['id']]=cap
        utc(cap['start_utc']);utc(cap['end_utc']);assert cap['start_utc']<=cap['end_utc']
        cmd=[v.replace(str(d),'OWN_RUN') for v in cap['command']];cwd=cap['cwd'].replace(str(d),'OWN_RUN');signature=canon([cmd,cwd]).decode();occ[signature]+=1;key=signature+'#'+str(occ[signature])
        assert key not in cm;record={'command':cmd,'cwd':cwd,'exit_code':0};rawmap[key]={}
        for channel in ['stdout','stderr']:
            r=cap[channel]
            if 'path' in r:
                b=unstream(d,r);seen.add(r['path']);rawmap[key][channel]=b;record[channel]={'bytes':len(b),'sha256':sha(b)}
                if channel=='stdout' and cmd[:2]==['gh','api']:
                    obj=json.loads(b);parsed.append((obj,b,'API '+cmd[-1].removeprefix('repos/AlecKriebel/Math/')))
                    if cmd[-1]=='repos/AlecKriebel/Math/pulls/368':record[channel]={'canonical_semantics':normalized_pull(obj,j['pins'])}
                elif channel=='stdout' and cmd[-1]=='OWN_RUN/private/drift_negatives.py':
                    obj=json.loads(b);assert obj==j['old_drift_negative_controls'];parsed.append((obj,b,'new14 negatives'))
                    utc(obj['utc']);assert cap['start_utc']<=obj['utc']<=cap['end_utc'];obj['utc']='VALIDATED_NEGATIVE_REPLAY_UTC'
                    for r0 in obj['results']:
                        if 'exit_code' in r0:
                            label=r0['control'];err=gzip.decompress((d/'streams'/('negative_'+label+'_stderr.gz')).read_bytes());assert len(err)==r0['stderr_bytes'] and sha(err)==r0['stderr_sha256']
                            r0['stderr_bytes']='VALIDATED_PRIVATE_TRACEBACK_LENGTH';r0['stderr_sha256']='VALIDATED_PRIVATE_TRACEBACK_HASH'
                    record[channel]={'canonical_semantics':obj}
            else:
                assert channel=='stdout' and r['retained'] is False and cmd[:5]==['git','ls-tree','-r','-z','--full-tree'];record[channel]=r
        cm[key]=record
    utc(j['old_drift_negative_controls']['utc']);n['old_drift_negative_controls']['utc']='VALIDATED_NEGATIVE_REPLAY_UTC'
    for r0,r1 in zip(j['old_drift_negative_controls']['results'],n['old_drift_negative_controls']['results']):
        if 'exit_code' in r0:
            label=r0['control']
            for ch in ['stdout','stderr']:
                p='streams/negative_'+label+'_'+ch+'.gz';seen.add(p)
                b=gzip.decompress((d/p).read_bytes());rawmap['NEGATIVE '+label+' '+ch]={'raw':b}
                if ch=='stdout':assert b==b''
                else:assert len(b)==r0['stderr_bytes'] and sha(b)==r0['stderr_sha256']
            r1['stderr_bytes']='VALIDATED_PRIVATE_TRACEBACK_LENGTH';r1['stderr_sha256']='VALIDATED_PRIVATE_TRACEBACK_HASH'
    assert seen=={p.relative_to(d).as_posix() for p in (d/'streams').iterdir() if p.is_file()} and len(seen)==1626
    # Every recorded parse hash/leaf digest is independently reconstructed from full bytes.
    for row in j['full_json_all_leaf_reads']:
        if row['path'].startswith('API ') or row['path']=='new14 negatives':
            candidates=[(o,b) for o,b,label in parsed if label==row['path'] and sha(b)==row['sha256']]
            assert candidates,row
            obj,b=candidates[0];leaves=[]
            def walk(v,p):
                if isinstance(v,dict):
                    for k,x in sorted(v.items()):walk(x,p+[k])
                elif isinstance(v,list):
                    for i,x in enumerate(v):walk(x,p+[i])
                else:leaves.append([p,type(v).__name__,v])
            # Parsed negative object was normalized above; reconstruct original raw object.
            obj=json.loads(b);walk(obj,[])
            assert len(b)==row['bytes'] and len(leaves)==row['scalar_leaves'] and sha(canon(leaves))==row['all_scalar_leaf_map_sha256']
    reads=[]
    for row in j['full_json_all_leaf_reads']:
        r=dict(row)
        if r['path'] in ['API pulls/368','new14 negatives']:
            # Entire semantics already checked above; only raw path/counter-derived hashes vary.
            for key in ['bytes','sha256','all_scalar_leaf_map_sha256']:r[key]='VALIDATED_FULL_RUNTIME_JSON_'+key
        reads.append(r)
    n['full_json_all_leaf_reads']=sorted(reads,key=lambda r:canon(r))
    n['checks']=sorted(n['checks'],key=lambda r:canon(r))
    n['complete_captures']=cm
    n['complete_program_replays']=[]
    for row in j['complete_program_replays']:
        cap=by_id[row['capture_id']];assert row['command']==cap['command'] and row['stdout']==cap['stdout'] and row['stderr']==cap['stderr'] and row['exit_code']==cap['exit_code']==0
        cmd=[v.replace(str(d),'OWN_RUN') for v in row['command']]
        keys=[k for k,v in cm.items() if v['command']==cmd];assert len(keys)==1
        n['complete_program_replays'].append({'label':row['label'],'capture_key':keys[0],'complete_capture':cm[keys[0]]})
    normalized.append(n);capture_maps.append(cm);capture_raw_maps.append(rawmap);raw_stream_sets.append(seen)
assert capture_maps[0].keys()==capture_maps[1].keys() and capture_raw_maps[0].keys()==capture_raw_maps[1].keys()
for key in sorted(capture_raw_maps[0]):
    a=capture_raw_maps[0][key];b=capture_raw_maps[1][key];assert a.keys()==b.keys()
    for channel in a:
        u,v=a[channel],b[channel];equal=u==v;detail=None
        if not equal:
            if key.startswith('NEGATIVE '):
                assert channel=='raw' and key.endswith(' stderr');assert u.replace(str(RUNS[0]/'private/private_controls').encode(),b'OWN_PRIVATE')==v.replace(str(RUNS[1]/'private/private_controls').encode(),b'OWN_PRIVATE');detail='complete traceback identical after validated private directory substitution'
            elif 'repos/AlecKriebel/Math/pulls/368' in key and 'files?' not in key:
                assert channel=='stdout';ds=differences(json.loads(u),json.loads(v));permitted={'/'+side+'/repo/'+k for side in ['base','head'] for k in ['open_issues','open_issues_count','pushed_at','size']};assert {r['path'] for r in ds}<=permitted;api_differences.append({'command_key':key,'differences':ds});detail='only validated repository metadata counters/time/size'
            elif 'OWN_RUN/private/drift_negatives.py' in key:
                assert channel=='stdout' and capture_maps[0][key][channel]==capture_maps[1][key][channel];detail='entire negative record semantics and full traceback bytes verified'
            else:raise AssertionError(('unexpected full stream difference',key,channel))
        stream_pairs.append({'command_key':key,'channel':channel,'whole_bytes':len(u),'root_bytes':len(v),'whole_sha256':sha(u),'root_sha256':sha(v),'complete_bytes_equal':equal,'validated_difference':detail})
assert len(stream_pairs)==1626 and normalized[0]==normalized[1],differences(normalized[0],normalized[1])
for d,j in zip(RUNS,objects):
    normalization_ledger.append({'run':str(d),'original_receipt_sha256':sha((d/'RECEIPT.json').read_bytes()),'normalized_complete_receipt_sha256':sha(canon(normalized[RUNS.index(d)])),'complete_capture_keys':len(capture_maps[RUNS.index(d)]),'all1626_stream_paths_rehashed':True,'all8268_check_records_compared_as_complete_multiset':True,'normalizations':'Validated run/source/capture UTCs; exact owned directory substitution; matching commands by occurrence; full capture ID/reference rebinding; complete check/parse-record multiset ordering; raw PR repo counters/pushed_at/size after exact pin validation; six negative traceback length/hash values after whole-byte private-root comparison.'})
evidence=[json.loads((F/'COMPLETE_EVIDENCE.json').read_bytes()),json.loads((A/'root_final_live_complete_evidence.json').read_bytes())]
assert all(e['status']=='PASS' and e['complete_evidence_checks']==len(e['checks'])==6794 and all(r['pass'] for r in e['checks']) and e['complete_gzip_streams']==1626 for e in evidence)
assert evidence[0]['checks']==evidence[1]['checks']
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_FULL_FINAL_LIVE_COMPARISON','equal_live_checks':8268,'equal_complete_evidence_checks':6794,'complete_unique_stream_pairs':1626,'additive_manifest_public_files':1635,'original47_manifest_unchanged':True,'literal_pins':objects[0]['pins'],'all_normalization_validation_records':normalization_ledger,'raw_API_repo_metadata_differences':api_differences,'all_complete_stream_comparisons':stream_pairs,'independent_normalized_entire_receipts_equal':True,'actual_merge_pending':True,'workflow_completion_percent':95,'original_problem_resolution_percent':0}
(A/'root_final_live_comparison.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','equal_live_checks','equal_complete_evidence_checks','complete_unique_stream_pairs','workflow_completion_percent']},indent=2))
