from pathlib import Path
from datetime import datetime, timezone
import subprocess,json,hashlib,os,shutil
D=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr239_30001321/initial_review_20261015')
R=D/'root_new_control_replays';R.mkdir(exist_ok=False)
py='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python'
families=[('replica_martingale_adversary_01','AUTHORED_MANIFEST.json'),('final_segment_adversary_01','AUTHORED_MANIFEST.json'),('source_scope_provenance_adversary_01','PUBLIC_AUTHORED_MANIFEST.json')]
pins=[]
for folder,manifest in families:
    base=D/folder;m=json.loads((base/manifest).read_text());entries=m['files']
    if isinstance(entries,dict):entries=[dict(path=k,**v) for k,v in entries.items()]
    for e in entries:
        f=base/e['path'];assert f.resolve().is_relative_to(base.resolve())
        b=f.read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],str(f)
    pins.append({'family':folder,'manifest_sha256':hashlib.sha256((base/manifest).read_bytes()).hexdigest(),'authored_pins_verified':len(entries)})
checks=[]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for name,program,expected in [
 ('replica','replica_martingale_adversary_01/independent_controls.py','replica_martingale_adversary_01/independent_controls_receipt.json'),
 ('final_segment','final_segment_adversary_01/independent_controls.py','final_segment_adversary_01/independent_controls_receipt.json'),
 ('source_boundary','source_scope_provenance_adversary_01/check_source_domain_boundaries.py','source_scope_provenance_adversary_01/SOURCE_DOMAIN_BOUNDARY_CHECK.json'),
 ('provenance','source_scope_provenance_adversary_01/verify_provenance.py',None)]:
    start=datetime.now(timezone.utc).isoformat();r=subprocess.run([py,'-I','-B',str(D/program)],capture_output=True,timeout=300,env=env)
    (R/(name+'_stdout.json')).write_bytes(r.stdout);(R/(name+'_stderr.txt')).write_bytes(r.stderr)
    assert r.returncode==0 and not r.stderr,(name,r.returncode,r.stderr)
    out=json.loads(r.stdout);assert out['status']=='PASS'
    equal=r.stdout==(D/expected).read_bytes() if expected else None
    if expected:assert equal,(name,'output bytes differ')
    checks.append({'name':name,'start_utc':start,'end_utc':datetime.now(timezone.utc).isoformat(),'returncode':r.returncode,'empty_stderr':True,'program_sha256':hashlib.sha256((D/program).read_bytes()).hexdigest(),'expected_receipt':expected,'complete_byte_identical':equal,'output':out})
source=json.loads((D/'root_source_reading/PRIMARY_RETRIEVAL.json').read_text())
print(json.dumps({'root_source_receipt_type':type(source).__name__,'keys':list(source) if isinstance(source,dict) else None}),flush=True)
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','family_manifests':pins,'complete_actual_root_replays':checks,'root_original_replays':'ROOT_ORIGINAL_REPLAY_ACCEPTANCE.json','source_note':'Four actual root PDF fetches and byte hashes recorded separately in root_source_reading/PRIMARY_RETRIEVAL.json; direct target pp2151-2152 visually inspected.','limits':'Finite controls support but do not prove the independently reconstructed asymptotic estimates.'}
(D/'ROOT_FRESH_FAMILY_VALIDATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
shutil.copy2('/tmp/pr239_root_validate_20261015.py',R/'validate_families.py')
print(json.dumps({'status':'PASS','manifests':pins,'new_exact_assertions':sum(x['output'].get('exact_assertions',0) for x in checks),'replays':[x['name'] for x in checks]},indent=2))
