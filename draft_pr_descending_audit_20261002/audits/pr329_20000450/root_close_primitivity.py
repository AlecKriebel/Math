"""Externally close the held narrow addendum and preserve original audit history."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,stat
A=Path(__file__).resolve().parent;N=A/'geometry_primitivity'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=datetime.now(timezone.utc).isoformat()
assert not (A/'ROOT_PRIMITIVITY_CLOSURE.json').exists()
def pin(p):
    b=p.read_bytes();return dict(path=str(p.relative_to(A)),bytes=len(b),sha256=sha(b),mode=oct(stat.S_IMODE(p.stat().st_mode)))
own=json.loads((N/'namespace_inventory.json').read_bytes())
paths=[p for p in sorted(N.rglob('*')) if p.is_file()]
assert len(paths)==own['file_count']==18 and all(not p.is_symlink() for p in N.rglob('*'))
assert {str(p.relative_to(N)) for p in paths}=={x['path'] for x in own['entries']}
for record in own['entries']:
    if record['path']=='namespace_inventory.json':continue
    b=(N/record['path']).read_bytes();assert len(b)==record['bytes'] and sha(b)==record['sha256']
old=json.loads((A/'ROOT_GEOMETRY_NAMESPACE_MANIFEST.json').read_bytes())
for record in old['files']:assert pin(A/record['path'])==record
old_paths={str(p.relative_to(A)) for p in (A/'geometry').rglob('*') if p.is_file()
    and '.runtime' not in p.relative_to(A).parts and '__pycache__' not in p.relative_to(A).parts}
assert old_paths=={x['path'] for x in old['files']}
for suffix,exitcode,code in [('',0,'verify_primitivity.py'),('_v1',1,'verify_primitivity_v1.py'),('_v2',1,'verify_primitivity_v2.py')]:
    base='verify_primitivity'+suffix;r=json.loads((N/(base+'.receipt.json')).read_bytes())
    assert r['exit_code']==exitcode and r['script_sha256']==sha((N/code).read_bytes())
    for kind in ['stdout','stderr']:
        assert r[kind+'_sha256']==sha((N/(base+'.'+kind+'.txt')).read_bytes())
D=A/'root_runs_private/geometry_primitivity_external001';r=json.loads((D/'execution.json').read_bytes())
assert r['exit_code']==0 and (D/'stderr.bin').read_bytes()==b''
out=(D/'stdout.bin').read_bytes();assert sha(out)==r['stdout_sha256']
assert r['programs']==[{k:v for k,v in pin(N/'verify_primitivity.py').items() if k!='mode' and k!='path'}|{'path':str(N/'verify_primitivity.py')}]
def science(b):
    return '\n'.join(x for x in b.decode().splitlines() if not re.fullmatch(r'native_utc_(?:start|end) \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00',x))+'\n'
assert science(out)==science((N/'verify_primitivity.stdout.txt').read_bytes())
assert 'exact_identity_checks 18 status PASS' in science(out)
assert science(out).count('NEGATIVE_CONTROL_REJECTED ')==3
manifest=dict(utc=utc,namespace='geometry_primitivity',files=[pin(p) for p in paths],
    directories=[dict(path=str(p.relative_to(A)),mode=oct(stat.S_IMODE(p.stat().st_mode))) for p in sorted(N.rglob('*')) if p.is_dir()],
    whole_namespace_pinned=True,historical_failed_versions_preserved=True)
(A/'ROOT_PRIMITIVITY_NAMESPACE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
j=dict(utc=utc,status='PASS_ROOT_EXTERNALLY_CLOSED_PRIMITIVITY_ADDENDUM_PR329',
    report=pin(N/'primitivity_report.md'),program=pin(N/'verify_primitivity.py'),
    namespace_manifest=pin(A/'ROOT_PRIMITIVITY_NAMESPACE_MANIFEST.json'),native_external_replay=r,
    complete_scientific_output_equal_after_only_UTC_removal=True,root_fully_read_complete_proof_code_and_native_records=True,
    historical_code_versions_reconstructed_from_full_current_code_and_exact_single_line_diff=True,
    original_32_file_geometry_namespace_unchanged=True,narrow_mathematical_percent=100,
    exact_remaining_narrow_gap='None identified.',publication_ready=False,persistent_goal_complete=False)
(A/'ROOT_PRIMITIVITY_CLOSURE.json').write_text(json.dumps(j,indent=2)+'\n')
g=dict(utc=utc,status='PASS_ROOT_CURRENT_COMPLETE_MATHEMATICAL_GATE_PR329',
    original_mathematical_gate=pin(A/'ROOT_MATHEMATICAL_GATE.json'),primitivity_addendum=pin(A/'ROOT_PRIMITIVITY_CLOSURE.json'),
    mathematical_verification_percent=100,workflow_percent=50,original_author_turn_count='1/5',
    strongest_verified_result='Complete explicitly normalized characteristic-zero pentagonal torsion theorem, with uniform affine content and projective completion step now explicit.',
    exact_remaining_mathematical_gap='None identified in the stated model.',priority_complete=False,preprint_ready=False,
    merge_ready=False,publication_ready=False,persistent_goal_complete=False)
(A/'ROOT_CURRENT_MATHEMATICAL_GATE.json').write_text(json.dumps(g,indent=2)+'\n')
entry=f'\n{utc} — PR329 manuscript-proof addendum externally closed: mathematics100%, workflow50%. Root identified that function-field irreducibility requires an affine content step; new independent derivation frozen before root calculation exposure. For A-root X0, B(X0)=lambda(lambda+5r)(lambda+5(phi+1))/25; the sole additional B-zero has C(1/2)=-1. Gauss lemma and nonzero infinity restriction promote to entire projective irreducibility. Root fully read complete proof/code/current and failed native records, then actually reproduced18 exact identities/three meaningful false-content controls and complete scientific stdout. All18 new files/modes externally pinned; original32-file geometry namespace unchanged. Historical math gate preserved, current complete gate records the explicit addendum. Current paper/supplement/public export must include it before qualification; fresh full-preprint reviews and publication remain pending.\n'
for p in [A/'RESEARCH_LOG.md',A.parents[1]/'RESEARCH_LOG.md']:
    with p.open('a') as f:f.write(entry)
print(json.dumps(dict(utc=utc,status=j['status'],files=18,math_percent=100,workflow_percent=50),indent=2))
