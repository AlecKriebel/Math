#!/usr/bin/env python3
import pathlib,hashlib,json
p=pathlib.Path(__file__).parent
for stem in ['AUTHENTICATION','BOUNDARY_CHECKS','PRIMARY_RETRIEVAL']:
    receipt=json.loads((p/(stem+'_RUN.json')).read_text())
    assert receipt['returncode']==0
    for channel in ['stdout','stderr']:
        name=receipt.get(channel+'_path',stem+('.stdout.json' if channel=='stdout' else '.stderr.txt'))
        assert hashlib.sha256((p/name).read_bytes()).hexdigest()==receipt[channel+'_sha256']
    scriptname={'AUTHENTICATION':'authenticate_sources.py','BOUNDARY_CHECKS':'boundary_checks.py','PRIMARY_RETRIEVAL':'retrieve_primary_hashes.py'}[stem]
    assert hashlib.sha256((p/scriptname).read_bytes()).hexdigest()==receipt['script_sha256']
base=p.parent
manifest=base/'SOURCE_MANIFEST.json';raw=manifest.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='1d677ef16697e1e294f9f86800c10fe3189270cf2d9771a75d7c4e64954c0d1c'
entries=json.loads(raw)['files'];assert len(entries)==18
for e in entries:
    b=(base/'source'/e['path']).read_bytes()
    assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob']
decision=json.loads((p/'DECISION.json').read_text())
assert decision['completion_estimate_percent']==100 and decision['audit_status']=='PASS'
assert not decision['required_repairs'] and decision['exact_mathematical_gap_in_family'] is None
public=[]
for f in sorted(p.rglob('*')):
    if not f.is_file() or 'private_tmp' in f.relative_to(p).parts or f.name=='SAFE_MANIFEST.json':continue
    b=f.read_bytes();assert b'/'+b'Users/' not in b
    assert f.suffix.lower() not in ['.pdf','.zip','.tar','.gz']
    public.append(str(f.relative_to(p)))
primary=json.loads((p/'PRIMARY_RETRIEVAL.stdout.json').read_text())
assert primary['sources'][0]['sha256']=='ffb09776bafa3fa50dfc2bc83ee36b89058f98b7f80ff6fa90e2e34962cc9046'
failure=json.loads((p/'PACKAGING_FAILURE.json').read_text())
assert failure['returncode']==1
assert hashlib.sha256((p/'PACKAGING_FAILURE.stderr.txt').read_bytes()).hexdigest()==failure['raw_stderr_sha256']
print(json.dumps({'status':'PASS','checks':['stored process receipts and raw output/script hashes','all18 frozen source files unchanged','decision/report state','no private absolute path or PDF/archive in public payloads','primary MIT PDF hash','administrative failure preserved'],'public_payloads_checked_before_integrity_run_output':public},indent=2))
