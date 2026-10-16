"""Read-only authentication of the closed fresh Markov/closure audit."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
A=Path(__file__).resolve().parent;F=A/'markov_closure'
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.now(timezone.utc).isoformat()
def req(c,label):
    if not c:raise RuntimeError(label)
def check(p,j):
    b=p.read_bytes();req(len(b)==j['bytes'] and sha(b)==j['sha256'],'Hash/size mismatch: '+str(p))
def load(p):return json.loads(p.read_bytes())
fixed={'FINAL_WHOLE_PROOF_REPORT.md':'965f48523340ea9d753cf3d9ce9ab6bffa35834c91af086816b0f51fcb87119f',
       'FINAL_AUDIT_MANIFEST.json':'f7179349eac3082de85e1730ca9ede60dfd9551672555fbe718254cedeac8336',
       'FINAL_SEAL_RECEIPT.json':'277cc24704553c4646d8801cbd0e469dc129632592f26240564cf054e3330e1c'}
for n,h in fixed.items():req(sha((F/n).read_bytes())==h,'Final reported pin mismatch')
m=load(F/'FINAL_AUDIT_MANIFEST.json');seal=load(F/'FINAL_SEAL_RECEIPT.json')
req(m['status']=='PASS' and seal['status']=='PASS' and m['completion_estimate_percent']==100,'Family not complete')
seen=set()
for j in m['artifacts']:
    p=F/j['relative_path'];req(str(p)==j['path'] and p.is_file() and not p.is_symlink(),'Bad local artifact path')
    req(j['relative_path'] not in seen,'Duplicate artifact');seen.add(j['relative_path']);check(p,j)
    req((p.stat().st_mode&0o7777)==0o444 and j['observed_final_mode']=='0o444' and j['bytes_unchanged'],'Unsealed artifact')
for k in ['manifest','sidecar']:
    j=seal[k];p=F/j['relative_path'];check(p,j);req((p.stat().st_mode&0o7777)==0o444,'Unsealed final binding');seen.add(j['relative_path'])
req((F/'FINAL_SEAL_RECEIPT.json').stat().st_mode&0o7777==0o444,'Receipt not sealed');seen.add('FINAL_SEAL_RECEIPT.json')
req(seen=={str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()},'Unbound family file')
req(len(m['artifacts'])==seal['sealed_artifact_count_excluding_manifest_sidecar_receipt']==24,'Artifact count mismatch')
req((F/'FINAL_AUDIT_MANIFEST.sha256').read_text().split()[0]==fixed['FINAL_AUDIT_MANIFEST.json'],'Sidecar mismatch')
for j in m['candidate_inputs']:check(Path(j['path']),j)
req(len(m['candidate_inputs'])==20 and m['author_packet_file_count']==19,'Author read scope mismatch')
sourcegate=load(A/'ROOT_FAMILY_SOURCE_GATE.json');firstgate=load(A/'ROOT_FAMILY_FIRST_CANDIDATE_GATE.json')
req(sha((F/'INDEPENDENT_SOURCE_CRITERIA.md').read_bytes())==sourcegate['pins']['markov_closure']['sha256'],'Early source changed')
req(sha((F/'FIRST_CANDIDATE_ASSESSMENT.md').read_bytes())==firstgate['first_assessment_pins']['markov_closure']['sha256'],'Early first assessment changed')
r=load(F/'REPRODUCTION_MANIFEST.json')
req(r['status']=='PASS' and r['assertions_enabled'] and len(r['runs'])==4 and r['author_assertions']==564189,'Reproduction not passed')
for j in r['runs']:
    for k in ['code','stdout','stderr','expected_output']:check(Path(j[k]['path']),j[k])
    req(j['exit_code']==0 and j['stderr']['bytes']==0 and j['code_bytes_unchanged'] and j['stdout_matches_stored_bytes'],'Native reproduction discrepancy')
    req(Path(j['stdout']['path']).read_bytes()==Path(j['expected_output']['path']).read_bytes(),'Native stdout changed')
    req(not any(arg in ['-O','-OO'] for arg in j['argv']),'Optimized execution')
root=load(A/'ROOT_INDEPENDENT_CONTROL_REPLAYS.json')['executions']['markov_prose']
req(root['original_program']['sha256']==sha((F/'independent_controls.py').read_bytes()),'Independent code changed since root replay')
req(root['stdout_sha256']==sha((F/'INDEPENDENT_CONTROLS_RESULT.json').read_bytes()),'Independent output changed since root replay')
receipt=dict(utc=utc(),status='PASS_CLOSED_MARKOV_FAMILY_ALL_BYTES_MODES_INPUTS_NATIVE_STREAMS_AUTHENTICATED',
    final_pins=fixed,artifact_count=24,total_namespace_files=len(seen),candidate_bound_files=20,native_runs=4,
    root_full_report_manifest_seal_runner_code_and_native_streams_read=True,early_independence_pins_unchanged=True,
    family_math_percent=100,root_overall_mathematical_acceptance=False,other_final_family_pending=True,
    priority_clearance=False,publication_ready=False)
(A/'ROOT_MARKOV_FINAL_ARTIFACT_AUTHENTICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
