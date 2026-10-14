"""Build the authored portable verification kit; exclude third-party reading copies."""
from pathlib import Path
import hashlib,json,shutil,zipfile
P=Path(__file__).resolve().parent;D=P.parent/'initial_review_20261013'
S=D/'submitted/unsolved_math_prioritization/attempts/5100020'
V=P/'verification';V.mkdir(exist_ok=True)
def copy(src,dst):
 p=V/dst;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,p)
metadata={'title':'An odd-period pedal-antipedal area invariant in elliptic billiards',
'upload_type':'publication','publication_type':'preprint',
'description':"We prove the k403,a observation of Reznik, Garcia and Koiller: the signed area product of the original orbit's origin pedal and origin antipedal is phase independent for every primitive least odd period in a noncircular elliptic billiard with a strict confocal elliptical caustic. All admitted coprime stars are included and every real antipedal intersection is finite. The construction-specific proof distinguishes coincident and opposite complex endpoints, cancels incident double poles and identifies the odd-period quotient lattice. The earlier credited origin-pedal trace supplies the complementary factor. A direct circular extension and an exact same-caustic four-periodic counterexample delimit the theorem. The verification archive contains the standalone LaTeX source, exact algebra and reflected-orbit certificates, independent high-precision geometry and near-pole diagnostics, full receipt comparisons, source hashes, mathematical audits and bounded priority reports. The original observation, prior campaign pedal argument and classical elliptic/cyclic-identity methods are credited. No historical-firstness certificate is claimed. AI tools were used extensively in solving, verification, literature research, coding, writing and internal adversarial review. This is an unrefereed preprint without external human peer review or proof-assistant formalization.",
'creators':[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],
'access_right':'open','license':'cc-by-4.0','publication_date':'2026-10-13','version':'1.0',
'keywords':['elliptic billiards','Poncelet polygons','pedal polygons','antipedal polygons','signed area product','odd periods','k403,a','Jacobi elliptic functions']}
(P/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
(P/'requirements.txt').write_text('sympy==1.14.0\nmpmath==1.3.0\n')
(P/'LICENSE').write_text('Copyright 2026 Alec Kriebel.\n\nAuthored manuscript and verification materials: Creative Commons Attribution 4.0 International.\nhttps://creativecommons.org/licenses/by/4.0/\nThird-party papers and raw extracts are excluded. Mathematical inputs retain their stated credit.\n')
(P/'README.md').write_text('''# Odd-period origin-pedal and antipedal area product

This kit accompanies the unrefereed note An odd-period pedal-antipedal area invariant in elliptic billiards, by Alec Kriebel, ORCID 0009-0001-9320-500X. It proves the k403,a observation of Reznik, Garcia and Koiller for the original orbit, a strict confocal elliptical caustic, primitive least odd period and every admitted coprime star. All areas are ordered signed shoelace areas; real intersections are finite. Circles are handled separately.

The written analytic proof establishes the universal theorem. Finite exact controls and high-precision diagnostics corroborate its algebra and construction domain; they are not proof-assistant formalization or interval certificates. The earlier campaign origin-pedal mechanism and classical canonical, Jacobi, cyclic-master-identity and Landen inputs are credited. Extensive bounded priority audits found no earlier covering result, without certifying worldwide firstness.

## Contents

- paper/odd_origin_area_product.tex is the standalone current source. The PDF is deposited separately.
- checks/, expected/ and CHECKSETS.json contain nine successful checksets and their complete reference receipts.
- run_verification.py verifies distributed hashes and executes programs in isolated temporary directories.
- audits/ contains authored mathematical/priority reports, derivations, source pins and root acceptance.
- proof/ORIGINAL_FROZEN_PROOF.md preserves the original proof bytes. Its historical candidate/pending-review labels refer to the 1 October packet; the current note and root acceptance govern the current result.
- provenance/ records immutable input identity and bibliographic hashes. Full third-party PDFs, archives, extracted text, images and raw web/API responses are excluded.
- MANIFEST.json hashes every distributed file except itself.

Historical audit manifests may mention original paths or excluded reading copies; they preserve provenance and are not runtime dependencies. Initially failed reviewer scripts remain in repository audit history and are excluded from executable PASS checksets. Fresh manuscript-review reports are recorded separately in the repository so adding a report cannot silently change a reviewed ZIP.

## Reproduce

Use Python 3.11 or newer, from the extracted package root:

~~~sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_verification.py
~~~

On Windows use the corresponding .venv/Scripts/python.exe. Dependencies are SymPy 1.14.0 and mpmath 1.3.0; NumPy/SciPy are not needed. The reference runtime was Python 3.14.6 on macOS. The runner checks hashes first, copies each script to its own temporary directory, and compares complete receipts ignoring only top-level generation UTC and elapsed time. It leaves this package unchanged.

Exact evidence includes named-line identities, Jacobi reductions, divisor coefficients, finite primitive lattice controls, and complete reflected strict-caustic constructions. Two distinct noncircular N3 trajectories have product 6860/81. An excluded same-caustic N4 pair has products 225/4 and 289/4, falsifying an all-parity extension. Diagnostics include Cartesian reflection, tangency, closing stars, reversal/repetition, extreme interior moduli, large odd periods and near-complex-pole phases. They do not replace the all-period proof.

Compile the standalone source with a modern LaTeX engine such as Tectonic if a PDF rebuild is desired; this is independent of the checksets.

AI tools were used extensively in derivation, verification, literature research, coding, writing and internal adversarial review. This is unrefereed, without external human peer review or formal proof-assistant verification.
''')
runner='''"""Execute the frozen checksets without changing the distributed files."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,shutil,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
manifest=json.loads((HERE/'MANIFEST.json').read_text())
for row in manifest['files']:
 assert hashlib.sha256((HERE/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
jobs=json.loads((HERE/'CHECKSETS.json').read_text())
def run(job):
 with tempfile.TemporaryDirectory(prefix='k403a-'+job['name']+'-') as tmp:
  d=Path(tmp);p=d/Path(job['script']).name;shutil.copyfile(HERE/job['script'],p)
  assert hashlib.sha256(p.read_bytes()).hexdigest()==job['source_script_sha256']
  r=subprocess.run([sys.executable,str(p)],capture_output=True)
  if r.returncode:raise RuntimeError(job['name']+': '+r.stderr.decode())
  actual=json.loads((d/job['result_file']).read_text()) if job['result_file'] else json.loads(r.stdout)
  expected=json.loads((HERE/job['expected']).read_text())
  for obj in [actual,expected]:
   for key in ['utc','elapsed_seconds']:obj.pop(key,None)
  if actual!=expected:raise AssertionError(job['name']+' differs from its complete reference receipt')
  return {'checkset':job['name'],'status':'PASS','complete_receipt_match':True}
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(run,jobs))
print(json.dumps({'status':'PASS','results':results,'scope':'Finite algebra/constructions and diagnostics; universal proof is in the manuscript. No interval or proof-assistant certification.'},indent=2))
'''
(P/'run_verification.py').write_text(runner)
jobs=[
('author_exact',S/'check_exact.py',S/'exact_receipt.json',None),
('author_numeric',S/'check_numerical.py',S/'numerical_receipt.json',None),
('original_independent_exact',S/'independent_review/independent_checks.py',S/'independent_review/INDEPENDENT_CHECKS.json',None),
('original_independent_numeric',S/'independent_review/independent_diagnostics.py',S/'independent_review/INDEPENDENT_DIAGNOSTICS.json',None),
('complex_exact',D/'meromorphic_adversary_01/fresh_exact_checks.py',D/'meromorphic_adversary_01/EXACT_CHECKS.json',None),
('complex_near_poles',D/'meromorphic_adversary_01/fresh_near_pole_diagnostics.py',D/'meromorphic_adversary_01/NEAR_POLE_DIAGNOSTICS.json',None),
('cartesian_exact',D/'geometric_adversary_01/cartesian_exact_checks.py',D/'geometric_adversary_01/CARTESIAN_EXACT_CHECKS.json','CARTESIAN_EXACT_CHECKS.json'),
('cartesian_numeric',D/'geometric_adversary_01/cartesian_numeric_checks.py',D/'geometric_adversary_01/CARTESIAN_NUMERIC_CHECKS.json','CARTESIAN_NUMERIC_CHECKS.json'),
('priority_construction',D/'priority_classical_adversary_01/construction_checks.py',D/'priority_classical_adversary_01/CONSTRUCTION_CHECKS.json','CONSTRUCTION_CHECKS.json')]
rows=[]
for name,script,receipt,outfile in jobs:
 dst='checks/'+name+'.py';expected='expected/'+name+'.json'
 copy(script,dst);copy(receipt,expected)
 rows.append({'name':name,'script':dst,'expected':expected,'result_file':outfile,'source_script_sha256':hashlib.sha256(script.read_bytes()).hexdigest()})
(V/'CHECKSETS.json').write_text(json.dumps(rows,indent=2)+'\n')
copy(P/'odd_origin_area_product.tex','paper/odd_origin_area_product.tex')
copy(S/'PROOF.md','proof/ORIGINAL_FROZEN_PROOF.md')
copy(D/'INTAKE.json','provenance/ORIGINAL_INTAKE.json')
copy(S/'source_manifest.json','provenance/source_manifest.json')
for name in ['ROOT_MATHEMATICAL_ACCEPTANCE.md','ROOT_PRIORITY_ACCEPTANCE.md','ROOT_PRIORITY_ROUTE_NOTES.md','ROOT_PRIORITY_SOURCE_HASH_CHECKS.json']:copy(D/name,'audits/'+name)
for folder,names in {
'meromorphic_adversary_01':['REPORT.md','INDEPENDENT_DERIVATION.md','FROZEN_HASHES.json'],
'geometric_adversary_01':['REPORT.md','INDEPENDENT_DERIVATION.md','FINAL_AUDIT_MANIFEST.json','SOURCE_AUTHENTICATION.json'],
'priority_classical_adversary_01':['REPORT.md','BIBLIOGRAPHY.md','QUERY_LOG.md','FINAL_AUDIT_INTEGRITY.json','PUBLICATION_POLICY.md'],
'priority_recent_adversary_01':['REPORT.md','QUERY_SCOPE.md','PUBLIC_SOURCE_PINS.json','CURRENT_SOURCE_SCREENING_LEDGER.json','FINAL_AUDIT_MANIFEST.json']
}.items():
 for name in names:copy(D/folder/name,'audits/'+folder+'/'+name)
for name in ['README.md','LICENSE','requirements.txt','run_verification.py','metadata.json']:copy(P/name,name)
# Fresh manuscript reports remain separately recorded; no post-review ZIP additions.
files=[{'path':f.relative_to(V).as_posix(),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(V.rglob('*')) if f.is_file() and f.name!='MANIFEST.json' and '__pycache__' not in f.parts]
(V/'MANIFEST.json').write_text(json.dumps({'version':'1.0','problem':'5100020 /AMR-050-0020 /k403,a','paper_source_sha256':hashlib.sha256((P/'odd_origin_area_product.tex').read_bytes()).hexdigest(),'files':files},indent=2)+'\n')
target=P/'odd-origin-area-product-verification.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(V.rglob('*')):
  if f.is_file() and '__pycache__' not in f.parts:z.write(f,'odd-origin-area-product-verification/'+f.relative_to(V).as_posix())
(P/'zenodo-deposit.json').write_text(json.dumps({'metadata':metadata,'files':[{'path':'output/pdf/odd_origin_area_product.pdf'},{'path':target.name}]},indent=2)+'\n')
state={'stage':'candidate_before_fresh_manuscript_reviews','paper_pdf':{'bytes':(P/'output/pdf/odd_origin_area_product.pdf').stat().st_size,'sha256':hashlib.sha256((P/'output/pdf/odd_origin_area_product.pdf').read_bytes()).hexdigest()},'paper_tex_sha256':hashlib.sha256((P/'odd_origin_area_product.tex').read_bytes()).hexdigest(),'zip':{'files':len(files)+1,'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()},'metadata_sha256':hashlib.sha256((P/'metadata.json').read_bytes()).hexdigest(),'preprint_upload_cleared':False}
(P/'PACKAGE_STATE.json').write_text(json.dumps(state,indent=2)+'\n')
print(json.dumps(state,indent=2))
