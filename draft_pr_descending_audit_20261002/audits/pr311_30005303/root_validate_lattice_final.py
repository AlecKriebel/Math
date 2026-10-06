"""Read-only authentication of the closed fresh lattice/factorization audit."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
A=Path(__file__).resolve().parent;F=A/'lattice_factorization'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
def req(c,label):
    if not c:raise RuntimeError(label)
def load(p):return json.loads(p.read_bytes())
def check(p,j):
    b=p.read_bytes();req(len(b)==j['bytes'] and sha(b)==j['sha256'],'Hash/size mismatch '+str(p))
fixed={'FINAL_WHOLE_PROOF_REPORT.md':'69c516eead3f4b4582a6bcd9985791ba2b9756ac54cafe9ffab8c6a0103ae184',
    'FINAL_AUDIT_MANIFEST.json':'eae6746baa8d258b254978d90b5f9f82350cfb19865d903e72719d39ade2400a',
    'FINAL_SEAL_RECEIPT.json':'2b37cb6759331ed930832e23e99e11c1c630ffc5f279c7bf61eabed7725d7d9a'}
for name,h in fixed.items():req(sha((F/name).read_bytes())==h,'Reported final pin mismatch')
m=load(F/'FINAL_AUDIT_MANIFEST.json');seal=load(F/'FINAL_SEAL_RECEIPT.json')
req(m['completion_percent_math_code_audit']==100 and len(m['files'])==seal['sealed_file_count']==31,'Incomplete final audit')
seen=set()
for j in m['files']:
    p=F/j['relative_path'];req(str(p)==j['path'] and not p.is_symlink(),'Bad artifact path')
    req(j['relative_path'] not in seen,'Duplicate artifact');seen.add(j['relative_path']);check(p,j)
    req((p.stat().st_mode&0o7777)==0o444 and j['new_mode']=='0444' and j['bytes_unchanged_at_seal'],'Artifact not sealed')
for name in ['FINAL_AUDIT_MANIFEST.json','FINAL_SEAL_RECEIPT.json']:
    req((F/name).stat().st_mode&0o7777==0o444,'Final binding unsealed');seen.add(name)
read=load(F/'FINAL_READ_LEDGER.json')
private=set()
for j in read['private_authentication_artifacts']:
    p=Path(j['path']);check(p,j);private.add(str(p.relative_to(F)))
req(seen|private=={str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()},'Unbound namespace file')
inputs=load(F/'AUTHOR_INPUT_BINDINGS.json')
req(inputs['author_packet_count']==19 and len(inputs['files'])==21,'Read scope count mismatch')
for j in inputs['files']:
    p=Path(j['path']);check(p,j);req(format(p.stat().st_mode&0o7777,'04o')==j['mode'],'Input mode changed')
disclosure=load(F/'EXTRA_READ_DISCLOSURE.json')
req(disclosure['use_as_evidence'] is False and disclosure['parent_notified_and_acknowledged'],'Summary exposure not accounted for')
req(disclosure['extra_read_sha256']=='8126cf30aa5dad97738c5f46f91726055f33f139a5f71762817713cb3b134fd8','Summary scope mismatch')
sg=load(A/'ROOT_FAMILY_SOURCE_GATE.json');fg=load(A/'ROOT_FAMILY_FIRST_CANDIDATE_GATE.json')
req(sha((F/'INDEPENDENT_SOURCE_CRITERIA.md').read_bytes())==sg['pins']['lattice_factorization']['sha256'],'Source criteria changed')
req(sha((F/'FIRST_CANDIDATE_ASSESSMENT.md').read_bytes())==fg['first_assessment_pins']['lattice_factorization']['sha256'],'First verdict changed')
r=load(F/'reproduction/RUN_RECEIPTS.json')
req(r['all_runs_passed'] and r['author_assertions']==564189 and len(r['runs'])==5,'Reproduction not complete')
for j in r['runs']:
    req(j['exit_code']==0 and j['stderr_bytes']==0,'Failed native run')
    req(sha(Path(j['argv'][1]).read_bytes())==j['code_sha256'],'Run code changed')
    for k in ['stdout','stderr']:
        b=Path(j[k+'_path']).read_bytes();req(len(b)==j[k+'_bytes'] and sha(b)==j[k+'_sha256'],'Native stream changed')
    if 'expected_output_path' in j:
        req(Path(j['stdout_path']).read_bytes()==Path(j['expected_output_path']).read_bytes(),'Author output differs')
    else:
        orig=F/Path(j['result_path']).name
        req(Path(j['stdout_path']).read_bytes()==orig.read_bytes()==Path(j['result_path']).read_bytes(),'Independent result differs')
root=load(A/'ROOT_INDEPENDENT_CONTROL_REPLAYS.json')['executions']
for tag,code,out in [('lattice_source','source_control_exact.py','source_control_result.json'),('lattice_prose','prose_controls_exact.py','prose_controls_result.json')]:
    req(root[tag]['original_program']['sha256']==sha((F/code).read_bytes()),'Root-replayed independent code changed')
    req(root[tag]['stdout_sha256']==sha((F/out).read_bytes()),'Root-replayed independent output changed')
rec=dict(utc=utc(),status='PASS_CLOSED_LATTICE_FAMILY_ALL_BYTES_MODES_INPUTS_NATIVE_STREAMS_AUTHENTICATED',
    final_pins=fixed,sealed_artifacts=31,sealed_namespace_files=len(seen),private_source_files=len(private),candidate_bound_files=21,
    actual_native_runs=5,full_report_alternative_proof_read_ledger_manifests_runner_code_and_all_streams_root_read=True,
    early_independence_pins_unchanged=True,late_summary_exposure_disclosed_and_excluded=True,family_math_percent=100,
    root_overall_mathematical_acceptance=False,priority_clearance=False,publication_ready=False)
(A/'ROOT_LATTICE_FINAL_ARTIFACT_AUTHENTICATION.json').write_text(json.dumps(rec,indent=2)+'\n')
print(json.dumps(rec,indent=2))
