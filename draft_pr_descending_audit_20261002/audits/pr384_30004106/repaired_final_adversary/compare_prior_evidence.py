#!/usr/bin/env python3
from pathlib import Path
import subprocess,hashlib,json,sys
from datetime import datetime,timezone
P=Path(__file__).resolve().parent;A=P.parent
manifests=['banach_sources_review/MANIFEST.json','induced_modules_review/OUTPUT_MANIFEST.json','induced_modules_review/adversary/MANIFEST.json','quaternion_abstract_review/OUTPUT_MANIFEST.json','final_adversary/OUTPUT_MANIFEST.json']
records=[]
for name in manifests:
 m=A/name;d=json.loads(m.read_text());base=m.parent
 for e in d['files']:
  f=base/e['path']
  if not f.exists():f=Path('/Users/alec/Documents/Math')/e['path']
  b=f.read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],(name,e['path'])
  records.append({'manifest':name,**e})
code=A/'final_adversary/new_controls.py';copy=P/'private/original_final_new_controls.py';copy.write_bytes(code.read_bytes())
r=subprocess.run([sys.executable,'-B',str(copy)],capture_output=True,cwd=copy.parent)
(P/'ORIGINAL_FINAL_FRESH.stdout').write_bytes(r.stdout);(P/'ORIGINAL_FINAL_FRESH.stderr').write_bytes(r.stderr)
assert r.returncode==0 and not r.stderr and r.stdout==(A/'final_adversary/NEW_CONTROLS.json').read_bytes()
reports=['banach_sources_review/REPORT.md','induced_modules_review/REPORT.md','induced_modules_review/adversary/REPORT.md','quaternion_abstract_review/REVIEW.md','ROOT_MATHEMATICAL_RECONSTRUCTION.md','final_adversary/REPORT.md','final_adversary/PROOF_RECONSTRUCTION_BEFORE_COMPARISON.md','final_adversary/SOURCE_FIRST_RECONSTRUCTION.md']
summary={'utc':datetime.now(timezone.utc).isoformat(),'prior_sealed_bindings':records,'count':len(records),'reports_compared_after_own_source_reconstruction_and_control_seals':[{'path':f,'sha256':hashlib.sha256((A/f).read_bytes()).hexdigest()} for f in reports],'original_final_controls_fresh_full_stdout_byte_exact':True,'original_final_control_assertions':json.loads(r.stdout)['exact_assertions'],'own_new_controls_assertions':json.loads((P/'FRESH_CONTROLS.json').read_text())['exact_assertions'],'distinct_new_mechanisms':['Full actual coset G-set diagonal tensor orbits and dimension-normalized full Mobius block norms, retaining projective block','Actual full induction endomorphism equations and enumeration of idempotents for cyclic core cases, before coordinates','Full Q8 signed multiplication with real polynomial spectral idempotents in the original full algebra, no stable Fourier-only argument'],'no_prior_verdict_used_as_proof_premise':True}
(P/'COMPARISON_BINDINGS.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({'prior_bindings':len(records),'original_final_exact_assertions':summary['original_final_control_assertions'],'all_full_stdout_byte_exact':True},indent=2))
