from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, zipfile

PRE = Path(__file__).resolve().parent
D = PRE.parent / 'initial_review_20261013'
B = PRE / 'verification_package'
B.mkdir(exist_ok=True)

def write(path, value):
    p = B / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(value)

def copy(source, target):
    p = B / target
    p.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, p)

copy(PRE / 'critical_wave_growth.tex', 'manuscript/critical_wave_growth.tex')
original = D / 'submitted/unsolved_math_prioritization/attempts/30004630'
for p in original.rglob('*'):
    if p.is_file():
        copy(p, 'original_submission/' + p.relative_to(original).as_posix())

families = [
 ('source_pde_adversary_02','FINAL_AUDIT_MANIFEST.json','public_authored_relative_paths'),
 ('variational_adversary_02','FINAL_AUDIT_MANIFEST.json','files'),
 ('source_pde_adversary_02/addendum_review','FINAL_ADDENDUM_MANIFEST.json','public_authored_relative_paths'),
 ('priority_classical_adversary_01','FINAL_AUDIT_MANIFEST.json','authored_files'),
 ('priority_recent_adversary_01','FINAL_AUDIT_MANIFEST.json','public_authored_files'),
 ('priority_bridge_falsifier_01','FINAL_AUDIT_MANIFEST.json','public_authored_relative_paths'),
 ('priority_attribution_falsifier_01','FINAL_AUDIT_MANIFEST.json','public_authored_relative_paths'),
]
for folder, name, key in families:
    source = D / folder
    m = json.loads((source / name).read_text())
    pins = m[key]
    if isinstance(pins, dict):
        pins = [{'path': k, **v} for k,v in pins.items()]
    copy(source / name, 'audits/' + folder + '/' + name)
    for pin in pins:
        rel = pin.get('path', pin.get('relative_path'))
        p = source / rel
        assert p.resolve().is_relative_to(source.resolve())
        data = p.read_bytes()
        assert len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256']
        copy(p, 'audits/' + folder + '/' + rel)

checks = [
 ('author3937', original/'verify_algebra.py', D/'root_reproduction/author/stdout.json', None),
 ('original_independent1385', original/'independent_review/independent_check.py', D/'root_reproduction/original_independent/stdout.json', None),
 ('source17', D/'source_pde_adversary_02/controls.py', D/'source_pde_adversary_02/INDEPENDENT_CONTROLS.json', 'INDEPENDENT_CONTROLS.json'),
 ('variational215', D/'variational_adversary_02/independent_variational_checks.py', D/'root_reproduction/variational_final/stdout.json', None),
 ('addendum21', D/'source_pde_adversary_02/addendum_review/checks.py', D/'source_pde_adversary_02/addendum_review/CHECKS.json', 'CHECKS.json'),
 ('classical13', D/'priority_classical_adversary_01/priority_bridge_checks.py', D/'root_reproduction/priority_classical13/REFERENCE_EXPECTED.json', None),
 ('fresh_bridge20', D/'priority_bridge_falsifier_01/independent_bridge_checks.py', D/'priority_bridge_falsifier_01/INDEPENDENT_CHECK_RECEIPT.json', 'INDEPENDENT_CHECK_RECEIPT.json'),
]
configuration=[]
for name,script,reference,emitted in checks:
    copy(script, 'checks/'+name+'/'+script.name)
    copy(reference, 'checks/'+name+'/REFERENCE_EXPECTED.json')
    configuration.append({'name':name,'script':'checks/'+name+'/'+script.name,
                          'reference':'checks/'+name+'/REFERENCE_EXPECTED.json','emitted_receipt':emitted})
write('CHECKSETS.json',json.dumps(configuration,indent=2)+'\n')
write('requirements.txt','sympy==1.14.0\nmpmath==1.3.0\n')
write('LICENSE.txt','Original manuscript and authored verification materials: Creative Commons Attribution 4.0 International (CC BY 4.0).\nhttps://creativecommons.org/licenses/by/4.0/\nThird-party works are cited and byte-pinned; their whole reading copies are excluded.\n')
write('README.md', '''# Critical-wave quadratic-growth counterexample: verification package

Author: Alec Kriebel; ORCID 0009-0001-9320-500X. Version 1.0, 2026-10-14 UTC.

The separate six-page PDF proves the explicit negative answer to retaining the source ordinary-critical-cone strict-positivity implication to strong control-L2 quadratic growth after deleting beta2>0. Its cone is {0}; the strict condition is vacuous. A small positive constant cap gives a unique global optimizer. The actual nonlinear state is not confined to one eigenmode. Every fixed finite nonnegative terminal-velocity weight is allowed. The radial comparison neighborhood may depend on that weight; arbitrary-target upper estimates are uniform in the weight.

The paper also proves local L1 quadratic growth and fixed-basepoint optimizer estimates. It does not claim pairwise Lipschitz selection, perturbed uniqueness, L-infinity optimizer convergence, a sharp exponent, or a complete unregularized replacement theory. Classical concentration/noncoercivity, sparse threshold calculus and wave estimates are credited.

## Reproduction

Use Python 3.11 or later. The reference environment used Python 3.14.6, SymPy 1.14.0 and mpmath 1.3.0. Install the two pinned packages:

```text
python -m pip install -r requirements.txt
python verify_all.py
```

The runner first checks every packaged file against FILE_MANIFEST.json, then executes all seven checksets in separate temporary directories. It compares every field of each complete parsed receipt with its reference, excluding only the top-level informational `utc` and `python` fields. Dependency-version fields, all scientific values, category counts, assertions, diagnostic samples and stated limitations are compared. Runtime version is recorded in the resulting report; exclusion of Python text allows the explicitly supported Python versions. For scripts emitting a file, that complete receipt is read and compared; their temporary absolute output path is informational.

Total: 5,603 exact finite assertions plus five noncertified high-precision diagnostic assertions. These check eigenmode identities, pulse integrals, remainder orders, capped moment controls, weaker-norm algebra and threshold estimates. They do not solve a discretized nonlinear PDE, certify a numerical Strichartz constant, replace the analytic proofs, or certify priority. The universal inequalities and all optimizer quantifiers are proved analytically in the manuscript and derivations.

The standalone manuscript source can be compiled with an ordinary LaTeX toolchain. The delivered PDF was exported with Tectonic and all six pages were rendered with Poppler and visually inspected. The source also compiled successfully with the Codex desktop LaTeX compiler.

## Evidence and provenance

`original_submission/` preserves all 19 original files byte-for-byte at native PR head e9c5d10978764db2cf25fa7d49cf4bd14a82d604. Its early unreviewed headers and statuses are historical, not the current review outcome. `audits/` preserves the independently authored mathematical and bounded priority evidence used to develop this note. Source manifests intentionally bind excluded private reading copies; this portable archive does not redistribute whole external PDFs, extracted text, figures or provider responses. Those omitted files are not required to run the seven checksets. The relocated historical_snapshot_01 manifest shares four unchanged input/checker files with its parent audit-family directory; their exact preserved bytes remain in that parent directory. Some audit-only paths refer to the original workspace; the reproduction runner uses only paths inside this archive.

Priority findings are bounded. No earlier authenticated complete or automatically covering negative wave construction was located. Generic failure mechanisms were already known. In particular, applying an old conditional NDC theorem to the newly constructed data does not date the construction to that theorem. Inaccessible original/final publisher bodies and deposit/history searches are documented in the priority reports. No worldwide-firstness claim is made. Dunn's example was checked through the cited Casas-Tröltzsch reproduction, not through an obtained original chapter.

The paper uses a direct compatible-state contraction/local residual. It does not rely on the printed source proof's claimed surjectivity onto arbitrary continuous energy pairs. The direct pulse computation handles both source localizations; the older L2-neighborhood NDC theorem needs an explicit restricted-cap step to handle an L-infinity neighborhood, as the bridge audits explain.

AI tools were used extensively in solving, derivation, independent internal adversarial audits, exact computation, literature research and writing. This is an unrefereed research note without external human peer review or proof-assistant formalization. Later manuscript-review reports are separate repository evidence so that this reviewed scientific payload can remain immutable.

`FILE_MANIFEST.json` excludes itself to avoid recursive hashing. `verify_all.py` writes its final report outside the packaged file set, in the invocation directory. No network, repository mutation or outreach is needed for reproduction.
''')
write('verify_all.py', '''from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'FILE_MANIFEST.json').read_text())
for pin in manifest['files']:
 f=ROOT/pin['path'];assert f.resolve().is_relative_to(ROOT.resolve())
 data=f.read_bytes();assert len(data)==pin['bytes'] and hashlib.sha256(data).hexdigest()==pin['sha256'],str(f)
assert sys.version_info>=(3,11)
def normalize(receipt):
 return {k:v for k,v in receipt.items() if k not in {'utc','python'}}
results=[]
for spec in json.loads((ROOT/'CHECKSETS.json').read_text()):
 with tempfile.TemporaryDirectory(prefix='critical_wave_'+spec['name']+'_') as temp:
  work=Path(temp);script=ROOT/spec['script'];target=work/script.name;shutil.copyfile(script,target)
  run=subprocess.run([sys.executable,str(target)],cwd=work,capture_output=True,text=True,timeout=120)
  assert run.returncode==0,(spec['name'],run.stderr)
  expected=json.loads((ROOT/spec['reference']).read_text())
  actual=json.loads((work/spec['emitted_receipt']).read_text()) if spec['emitted_receipt'] else json.loads(run.stdout)
  assert normalize(actual)==normalize(expected),(spec['name'],'complete scientific receipt mismatch')
  stdout=json.loads(run.stdout)
  if spec['emitted_receipt'] and 'sha256' in stdout:
   assert stdout['sha256']==hashlib.sha256((work/spec['emitted_receipt']).read_bytes()).hexdigest()
  results.append({'checkset':spec['name'],'returncode':0,'complete_receipt_match':True,'receipt':actual,'stderr':run.stderr})
report={'status':'PASS','python_runtime':sys.version,'packaged_files_verified':len(manifest['files']),
        'checksets':len(results),'exact_assertions':5603,'noncertified_diagnostics':5,
        'ignored_top_level_informational_fields':['utc','python'],'results':results}
out=Path.cwd()/'VERIFICATION_RUN.json';assert out.resolve()!=ROOT/'FILE_MANIFEST.json'
out.write_text(json.dumps(report,indent=2)+'\\n')
print(json.dumps({'status':'PASS','checksets':len(results),'exact_assertions':5603,'noncertified_diagnostics':5,'report':str(out)},indent=2))
''')
metadata={
 'title':'Failure of strong quadratic growth in unregularized sparse control of a critical wave equation',
 'upload_type':'publication','publication_type':'preprint',
 'description':'We give an explicit negative answer to retaining ordinary critical-cone strict positivity and strong control-L2 quadratic growth after removing quadratic control regularization from the Kunisch–Meinlschmidt energy-critical quintic-wave model. On the three-dimensional unit ball, zero is the unique global optimizer for a sufficiently small positive pointwise Hilbert control cap. Its ordinary critical cone is zero and the strict condition is vacuous, while feasible controls converging in L-infinity have objective gap o(||u||L2^2). For nearby radial terminal targets, every global optimizer has L2 displacement divided by target displacement tending to infinity. Local L1 quadratic growth survives, with fixed-basepoint weaker-norm bounds. Every fixed finite nonnegative terminal-velocity weight is allowed; the radial lower comparison neighborhood may depend on that weight. The verification archive supplies standalone LaTeX, exact control/algebra checkers with full receipt comparisons, analytic derivations, original submission provenance, source pins and bounded priority audits. Classical wave estimates, group-sparse thresholds and concentration/noncoercivity theory are explicitly credited. The result concerns the unchanged strong-L2 implication, not all adapted unregularized sufficient conditions. No worldwide-firstness certificate or sharp-rate theorem is claimed. AI tools were used extensively in construction, derivation, internal independent adversarial verification, computation, literature research and writing. This is an unrefereed preprint without external human peer review or proof-assistant formalization.',
 'creators':[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],
 'access_right':'open','license':'cc-by-4.0','publication_date':'2026-10-14','version':'1.0',
 'keywords':['energy-critical wave equation','sparse optimal control','quadratic growth','critical cone','concentration','unregularized control','OWR-4990378-001']}
(PRE/'metadata.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n')
write('metadata.json',(PRE/'metadata.json').read_text())
files=[]
for p in sorted(B.rglob('*')):
    if p.is_file() and p.name != 'FILE_MANIFEST.json':
        assert not p.is_symlink()
        data=p.read_bytes();files.append({'path':p.relative_to(B).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
write('FILE_MANIFEST.json',json.dumps({'schema':'critical-wave-portable-manifest-v1','files':files,'self_hash_omitted':True},indent=2)+'\n')
archive=PRE/'output/critical_wave_verification.zip'
archive.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(B.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(B).as_posix())
deposit={'metadata':metadata,'files':[{'path':'output/pdf/critical_wave_growth.pdf'},{'path':'output/critical_wave_verification.zip'}]}
(PRE/'deposit.json').write_text(json.dumps(deposit,indent=2,ensure_ascii=False)+'\n')
freeze={'utc':datetime.now(timezone.utc).isoformat(),'version':'1.0','pages':6,'archive_files':len(files)+1,
        'exact_assertions':5603,'diagnostic_assertions':5,'fresh_manuscript_reviews_pending':True,'upload_cleared':False,'files':[]}
for p in [PRE/'critical_wave_growth.tex',PRE/'output/pdf/critical_wave_growth.pdf',archive,PRE/'metadata.json',PRE/'deposit.json']:
    data=p.read_bytes();freeze['files'].append({'path':p.relative_to(PRE).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
(PRE/'FROZEN_CANDIDATE.json').write_text(json.dumps(freeze,indent=2)+'\n')
print(json.dumps(freeze,indent=2))
