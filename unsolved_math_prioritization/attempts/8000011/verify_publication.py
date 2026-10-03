from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
public=json.loads((root/'PUBLIC_MANIFEST.json').read_text())
for name,digest in public.items():assert sha(root/name)==digest,name
prov=json.loads((root/'PUBLICATION_PROVENANCE.json').read_text())
a=root/'random_toda_lattice_8000011/packet';r=root/'review_toda_stopping_time_8000011'
assert sha(a/'FROZEN_MANIFEST.json')==prov['author_manifest_sha256']
assert sha(r/'REVIEW_MANIFEST.json')==prov['review_manifest_sha256']
frozen=json.loads((a/'FROZEN_MANIFEST.json').read_text())
omit=prov['omitted_author_files']
assert set(omit)=={'SOURCE_GATE.md','RESEARCH_LOG.md'}
for name,digest in frozen.items():
 if name in omit:
  assert not (a/name).exists() and omit[name]['sha256']==digest
 else:assert sha(a/name)==digest,name
for turn in range(1,6):
 for name,digest in json.loads((a/'turns'/f'TURN_{turn}_MANIFEST.json').read_text()).items():assert sha(a/name)==digest,name
review=json.loads((r/'REVIEW_MANIFEST.json').read_text())
for name,digest in review['files'].items():assert sha(r/name)==digest,name
for stem in ['turn1_exact','turn3_exact','turn4_numerical','turn5_exact']:
 result=subprocess.run([sys.executable,str(a/'checks'/f'{stem}.py')],capture_output=True,check=True)
 assert result.stdout==(a/'checks'/f'{stem}.stdout.json').read_bytes(),stem
for stem in ['audit_exact','audit_floating']:
 result=subprocess.run([sys.executable,str(r/f'{stem}.py')],capture_output=True,check=True)
 assert result.stdout==(r/f'{stem}.stdout.json').read_bytes(),stem
v=json.loads((r/'VERDICT.json').read_text())
assert v['author_turns']==5 and v['original_problem_resolved'] is False
assert v['partial_theorem_verdict']=='PASS_WITH_MINOR_REPORTING_CORRECTION'
print(json.dumps({'status':'PASS','public_bound_files':len(public),'included_frozen_author_files':len(frozen)-len(omit),'declared_omissions':len(omit),'review_bound_files':len(review['files']),'author_exact_finite_comparisons':2559,'author_executed_python_assertions':2238,'author_floating_diagnostics':4,'independent_exact_predicates':2049,'independent_floating_predicates':47,'author_turns':5,'original_problem_resolved':False,'stopping_rule':'first simultaneous all-coupling crossing'},indent=2))
