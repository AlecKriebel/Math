"""Authenticate closed independent families and completed fresh native replays."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
A=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
    assert p.is_file() and not p.is_symlink(),p
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':sha(b),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')}
families=[
 ('meromorphic_family_20261004','ARTIFACT_SEAL.json','b16324a4264d6017e8eda7d9d01fda1da795d7d965a66e7dc9d5727bc2107ff7','REPORT.md','5438c0fb7d268c92c982578dd5c8720494fbcf79766bc6b546541d3379c8da5e',['ARTIFACT_SEAL.json','SEAL_RUN.json']),
 ('source_fidelity_family_20261004','ARTIFACT_SEAL.json','c63f469f50faf20297b14dcf2b00e9c3dcffba357edcf0fb7640719d57f6b582','FINAL_REPORT.md','0d34caa8bc5dcb3f29575fd23ef70f48af33a6f351f69cdbce92f27ae45213c5',['ARTIFACT_SEAL.json']),
 ('geometric_family_20261004','MANIFEST.json','f5f9d15768c096a3b0ba2fdf72c08bbe0c6051223e713ed6b14e7ace3350055a','REPORT.md','78748e02a196a4149877fa510fef107e504d1dcab6bade59dab5ac3357169b2a',['MANIFEST.json'])]
verified={}
for folder,manifest,mhash,report,rhash,envelopes in families:
    D=A/folder;assert stat.S_IMODE(D.stat().st_mode)==0o555
    assert pin(D/manifest)['sha256']==mhash and pin(D/report)['sha256']==rhash
    j=json.loads((D/manifest).read_bytes());expected={}
    for e in j['files']:
        rel=Path(e['path']);assert not rel.is_absolute() and '..' not in rel.parts and str(rel) not in expected
        measured=pin(D/rel);assert measured=={k:e[k] for k in ['bytes','sha256','mode']}
        assert measured['mode']=='0444';expected[str(rel)]=measured
    actual={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file()}
    assert actual==set(expected)|set(envelopes),(folder,actual-set(expected)-set(envelopes))
    assert all(not p.is_symlink() and stat.S_IMODE(p.stat().st_mode)==0o555 for p in D.rglob('*') if p.is_dir())
    terminal={name:pin(D/name) for name in envelopes};assert all(p['mode']=='0444' for p in terminal.values())
    verified[folder]={'report':pin(D/report),'seal':pin(D/manifest),'terminal_envelopes':terminal,'payload_files_verified':len(expected),'directory_mode':'0555','all_files_full_hash_read':True}
def native(label):
    D=A/'root_runs_private'/label;spec=json.loads((D/'execution_spec.json').read_bytes());run=json.loads((D/'execution.json').read_bytes())
    assert run['exit_code']==0
    for kind in ['stdout','stderr']:
        b=(D/(kind+'.bin')).read_bytes();assert len(b)==run[kind+'_bytes'] and sha(b)==run[kind+'_sha256']
    assert not (D/'stderr.bin').read_bytes()
    for e in spec['programs']:
        assert {k:pin(Path(e['path']))[k] for k in ['bytes','sha256']}=={k:e[k] for k in ['bytes','sha256']}
    return json.loads((D/'stdout.bin').read_bytes()),run
# Compare every scientific output entry, not just a PASS marker.
checks=[]
for label,old in [
 ('root_replay_meromorphic_rational_actual001','meromorphic_family_20261004/independent_controls_run.json'),
 ('root_replay_source_symbolic_actual001','source_fidelity_family_20261004/independent_symbolic_control.stdout.txt'),
 ('root_replay_source_decimal_actual001','source_fidelity_family_20261004/independent_triangle_control.stdout.txt'),
 ('root_replay_meromorphic_full_actual001','meromorphic_family_20261004/independent_exact_complex_checks.stdout')]:
    fresh,run=native(label)
    if old.endswith('independent_controls_run.json'):
        receipt=json.loads((A/old).read_bytes());prior=json.loads(receipt['stdout'])
    else:prior=json.loads((A/old).read_bytes())
    if isinstance(fresh,dict):fresh.pop('utc',None);prior.pop('utc',None)
    assert fresh==prior,label
    checks.append({'label':label,'all_scientific_output_entries_equal':True,'actual_native_receipt':run})
j={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_THREE_CLOSED_FAMILY_SEALS_AND_FOUR_FRESH_NATIVE_REPLAYS',
   'families':verified,'fresh_reproductions':checks,'all_three_full_reports_root_read':True,
   'qualification':'Authenticates evidence and four completed controls. Full root direct-reflection replay and final mathematical adjudication remain pending. Numerical checks are finite noninterval diagnostics; the universal deduction is reviewed separately.',
   'mathematical_acceptance_granted':False,'priority_audit_started':False,'workflow_percent':20}
(A/'ROOT_FAMILY_SEAL_AUTHENTICATION.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j,indent=2))
