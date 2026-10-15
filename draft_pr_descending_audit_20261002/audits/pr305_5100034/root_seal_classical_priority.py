"""Authenticate and seal ROOT's classical implication evidence; no final priority verdict."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
A=Path(__file__).resolve().parent
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
pin=lambda p:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'mode':format(p.stat().st_mode&0o777,'04o')}
execution=A/'root_runs_private/root_classical_triangle_formula_actual002/execution.json'
j=json.loads(execution.read_text());assert j['exit_code']==0 and j['stderr_bytes']==0
out=A/'root_runs_private/root_classical_triangle_formula_actual002/stdout.bin';result=json.loads(out.read_text());assert sha(out.read_bytes())==j['stdout_sha256']
assert result['status']=='PASS_EXACT_CLASSICAL_SIGNED_TRIANGLE_FORMULA_AND_AUTHENTICATED_FOCAL_POWER_MAP' and result['generic_projection_minus_power_formula']=='0'
assert pin(A/'root_check_classical_triangle_formula_v02.py')['sha256']==j['programs'][0]['sha256']
acq=json.loads((A/'ROOT_CLASSICAL_NONCONSTANCY_ACQUISITION.json').read_text())
assert acq['status']=='PASS_EXACT_CLASSICAL_PRIMARY_ACQUISITION_CONTENT_ADJUDICATION_PENDING'
for name,e in acq['sources'].items():
 p=A/'root_classical_nonconstancy_private_v02'/(name+'.pdf');t=p.with_suffix('.txt')
 assert p.stat().st_size==e['pdf_bytes'] and sha(p.read_bytes())==e['pdf_sha256'] and sha(t.read_bytes())==e['text_sha256']
files={}
for dirname in ['root_classical_nonconstancy_private','root_classical_nonconstancy_private_v02']:
 d=A/dirname
 for p in sorted(d.iterdir()):
  assert p.is_file() and not p.is_symlink();p.chmod(0o444);files[str(p.relative_to(A))]=pin(p)
 d.chmod(0o555)
receipt={'utc':utc(),'status':'PASS_CLASSICAL_NEGATIVE_IMPLICATION_VERIFIED_NO_FULL_E_M_PRIORITY_VERDICT','report':pin(A/'ROOT_CLASSICAL_NONCONSTANCY_COROLLARY.md'),'native_symbolic_execution':pin(execution),'native_symbolic_result':pin(out),'symbolic_program':pin(A/'root_check_classical_triangle_formula_v02.py'),'private_payloads':files,'private_payload_count':len(files),'private_directories_mode':'0555','root_primary_reading_scope':['Querret complete extracted article and visual printed283/284 formulas','Fierobe real-billiard setup, Lemma4.1 and complete proof; visually checked printed9','Version history on primary arXiv page; no earliest-uninspected-v1 content claim'],'historical_qualification':'C falsehood is an explicit classical implication derived in this audit, not claimed as a novel negative theorem or an old explicit focal-ratio statement.','initial_native_failures_retained':['versioned arXiv URL: TLS exit35','initial supplementary checker: incorrect vector determinant API, before any verdict'],'independent_priority_families_still_active':True,'preprint_ready':False,'merge_clearance':False,'publication_clearance':False,'completion_estimates':{'mathematics':100,'priority':45,'workflow':35}}
(A/'ROOT_CLASSICAL_NONCONSTANCY_SEAL.json').write_text(json.dumps(receipt,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n## '+receipt['utc']+' — classical negative implication checked\n\nQuerret\'s signed triangle formula and Fierobe v5 Lemma4.1 imply nonconstant focal ratios in a noncircular triangular billiard family. Complete relevant primary statements/proofs and visual formulas checked; fresh arbitrary-triangle symbolic projection identity and exact PR305 circumcircle/power map pass. Negative claim will be credited as a classical implication, not independently novel or attributed as an old explicit target assertion. Initial TLS and checker API failures retained. Two priority families remain active, final E/M priority pending. Math100%; bounded priority45%; workflow35%.\n')
print(json.dumps({'utc':receipt['utc'],'status':receipt['status'],'private_payload_count':len(files),'report':receipt['report'],'seal':pin(A/'ROOT_CLASSICAL_NONCONSTANCY_SEAL.json'),'completion_estimates':receipt['completion_estimates']},indent=2))
