#!/usr/bin/env python3
"""Read-only input verification; patch reconstruction occurs in a temp directory."""
import argparse
from pathlib import Path
from hashlib import sha256
import json
import shutil
import subprocess
import tempfile
import zipfile

ap=argparse.ArgumentParser()
ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent)
root=ap.parse_args().root.resolve()
v1=root/'hodge_30004494'
v2=root/'hodge_30004494_v2'
audit=root/'hodge_30004494_independent_audit'
patch=root/'HODGE_30004494_V2_FROM_V1.patch'
pins={
 'v1_archive':('HODGE_30004494_AUTHOR_SAFE_FREEZE.zip','2880eb1f6345f6326c5b4ed8ab05801aa3c5db71d07e5a383472c74d69bcddbe'),
 'v2_archive':('HODGE_30004494_V2_SAFE_FREEZE.zip','1cbc6d90a8de7a92094570e9304f0b187ad8d5a8335fbe1546b7c8b09efba8dd'),
 'v1_manifest':('hodge_30004494/MANIFEST.json','1b384c58531496829886e4a0a96820dad434ea796a3c36b96f532e5b6c6a8571'),
 'v2_manifest':('hodge_30004494_v2/MANIFEST.json','8830a464eb9388fa980bc090bd44e17f548a860b39f686ffb45041689ef702c1'),
 'patch':(patch.name,'f384681f53cb6271f593d031c5de483dd60ba98ae12bd92cdb729225f8be6156'),
 'original_audit_archive':('HODGE_30004494_INDEPENDENT_AUDIT_SAFE_FREEZE.zip','48468ecb45f139badd88570fc52a86dd79af4c7baf7d38fa2cb74d3d0ac4bc78'),
 'original_audit_manifest':('hodge_30004494_independent_audit/MANIFEST.json','62ef10b64024f32e58edaa3f53bd6dcf716c4833d967d01d98016913e05fc1fe'),
}
def digest(p):return sha256(p.read_bytes()).hexdigest()
for name,(path,h) in pins.items():assert digest(root/path)==h,name

def verify_manifest(tree):
    m=json.loads((tree/'MANIFEST.json').read_bytes())
    expected={e['path'] for e in m['files']}|{'MANIFEST.json'}
    assert {p.name for p in tree.iterdir()}==expected
    for e in m['files']:
        p=tree/e['path'];assert p.is_file() and not p.is_symlink()
        assert len(p.read_bytes())==e['bytes'] and digest(p)==e['sha256']
    return m
m1=verify_manifest(v1);m2=verify_manifest(v2);ma=verify_manifest(audit)
for tree,key in [(v1,'v1_archive'),(v2,'v2_archive'),(audit,'original_audit_archive')]:
    with zipfile.ZipFile(root/pins[key][0]) as z:
        expected={tree.name+'/'+p.name for p in tree.iterdir()}
        assert set(z.namelist())==expected and len(z.namelist())==len(expected)
        for name in z.namelist():assert z.read(name)==(tree/Path(name).name).read_bytes()

changed=sorted(p.name for p in v1.iterdir() if p.read_bytes()!=(v2/p.name).read_bytes())
expected_changed=['MANIFEST.json','README.md','RESEARCH_LOG.md','RESULT.md','SOURCE_AUDIT.md','SOURCE_MANIFEST.json','readiness.json']
assert changed==expected_changed
unchanged=sorted(set(p.name for p in v1.iterdir())-set(changed))
assert unchanged==['PROOFS.md','VERIFICATION.json','verify.py']
with tempfile.TemporaryDirectory(prefix='hodge_delta_') as t:
    temp=Path(t)/'reconstructed';shutil.copytree(v1,temp)
    run=subprocess.run(['patch','--batch','--forward','--fuzz=0','-p1','-i',str(patch)],cwd=temp,capture_output=True,check=True)
    patch_output=(run.stdout+run.stderr).decode()
    assert 'fuzz' not in patch_output.lower() and 'offset' not in patch_output.lower()
    assert sorted(p.name for p in temp.iterdir())==sorted(p.name for p in v2.iterdir())
    for p in temp.iterdir():assert p.read_bytes()==(v2/p.name).read_bytes(),p.name

for tree in (v1,v2):
    run=subprocess.run(['python3','verify.py'],cwd=tree,capture_output=True,check=True)
    assert not run.stderr
    assert run.stdout==(v1/'VERIFICATION.json').read_bytes()
# Original independent code remains pinned, and all its controls are rerun.
run=subprocess.run(['python3',str(audit/'independent_verify.py'),'--author',str(v1),'--archive',str(root/pins['v1_archive'][0])],capture_output=True,check=True)
assert not run.stderr and run.stdout==(audit/'INDEPENDENT_VERIFICATION.json').read_bytes()
independent=json.loads(run.stdout)
assert m1['turns_used']==m2['turns_used']==5
assert m1['original_target_status']==m2['original_target_status']=='unsolved'
r1=json.loads((v1/'readiness.json').read_bytes());r2=json.loads((v2/'readiness.json').read_bytes())
for field in ('exact_claim','outcome','novelty_claim','statement_hash','review_hash','turns_used','turn_limit','workflow_state','success_test'):
    assert r1[field]==r2[field],field
# Verify frozen source hashes, counts, status and timestamps have not drifted
# outside the disclosed extra inspection scope and DT status qualification.
s1=json.loads((v1/'SOURCE_MANIFEST.json').read_bytes());s2=json.loads((v2/'SOURCE_MANIFEST.json').read_bytes())
assert {x['id'] for x in s1['sources']}=={x['id'] for x in s2['sources']}
for x,y in zip(s1['sources'],s2['sources']):
    if x['id'] not in ('GGR2021','DT2025'):assert x==y
    else:
        allowed={'inspection'}|({'status'} if x['id']=='DT2025' else set())
        assert {k:v for k,v in x.items() if k not in allowed}=={k:v for k,v in y.items() if k not in allowed}
for name,(path,h) in pins.items():assert digest(root/path)==h,name
print(json.dumps({
 'problem_id':'30004494','verdict':'PASS_EXACT_DELTA_INTEGRITY_AND_CONTROLS',
 'v1_and_original_audit_preserved':True,'v2_archive_bytes':(root/pins['v2_archive'][0]).stat().st_size,
 'patch_reconstructs_all_files_byte_for_byte':True,'patch_fuzz':0,'patch_offsets':False,
 'changed_files':changed,'unchanged_files':unchanged,
 'author_replay_checks':18549,'independent_replay_checks':independent['checks'],
 'source_metadata_changes_bounded':True,'core_target_and_status_unchanged':True,
 'original_target_status':'unsolved_5_of_5','pins':{k:{'path':p,'sha256':h} for k,(p,h) in pins.items()},
 'scope':'Integrity, exact delta, and finite controls only. M1 source applicability is accepted separately in DELTA_ACCEPTANCE.md.'
},indent=2,sort_keys=True))
