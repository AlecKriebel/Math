"""Hash-check a sealed fresh audit and replay its inspected program in a copy."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,subprocess,sys

D=Path(__file__).resolve().parent
name=sys.argv[1]
specs={
    'source_domain_adversary_01':('independent_controls.py','control_results.json',{'created_utc'}),
    'meromorphic_divisor_adversary_01':('check_independent.py','CHECK_RESULTS.json',{'utc'}),
    'physical_geometry_adversary_01':('cartesian_check.py','RESULTS.json',{'utc','created_utc'}),
}
program,result_name,timekeys=specs[name]
F=D/name
manifest=F/'AUTHORED_MANIFEST.json'
raw_manifest=manifest.read_bytes()
obj=json.loads(raw_manifest)
rows=obj['files']

def sha(data):return hashlib.sha256(data).hexdigest()

def validate():
    assert manifest.read_bytes()==raw_manifest
    paths=[]
    for row in rows:
        p=F/row['path']
        assert p.resolve().is_relative_to(F.resolve()) and not p.is_symlink()
        data=p.read_bytes()
        assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
        paths.append(row['path'])
    assert program in paths and result_name in paths and 'REPORT.md' in paths
    return paths

validate()
R=D/'root_reproduction_02'/name
R.mkdir(parents=True,exist_ok=False)
shutil.copyfile(F/program,R/program)
expected=json.loads((F/result_name).read_text())
began=datetime.now(timezone.utc).isoformat()
cmd=['/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python','-B',str(R/program)]
if name=='physical_geometry_adversary_01':
    cmd += ['--output',str(R/result_name),'--dps',str(expected['dps'])]
with (R/'stdout.txt').open('wb') as out,(R/'stderr.txt').open('wb') as err:
    run=subprocess.run(cmd,cwd=R,stdout=out,stderr=err,timeout=900)
assert run.returncode==0,(name,run.returncode)
assert not (R/'stderr.txt').read_bytes()
actual=json.loads((R/result_name).read_text())
ignored=[]
for key in timekeys:
    if key in expected or key in actual:
        assert key in expected and key in actual
        ignored.append(dict(field=key,original=expected.pop(key),replay=actual.pop(key)))
assert actual==expected,(name,'Non-timestamp scientific output differs')
paths=validate()
receipt=dict(utc=datetime.now(timezone.utc).isoformat(),began_utc=began,status='PASS',family=name,original_manifest_sha256=sha(raw_manifest),sealed_payloads=len(paths),all_payload_bytes_before_after_verified=True,program_sha256=sha((F/program).read_bytes()),result_sha256=sha((R/result_name).read_bytes()),exit_code=run.returncode,stderr_bytes=0,all_scientific_fields_exactly_reproduced=True,ignored_fields=ignored,original_family_unchanged=True,source_file_writes=0,limitations='Finite diagnostics are not a universal proof or interval certification. Sealed family program copied before execution; no original file, Git, shared DB, provider, tracker or network mutation.')
(R/'ROOT_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
