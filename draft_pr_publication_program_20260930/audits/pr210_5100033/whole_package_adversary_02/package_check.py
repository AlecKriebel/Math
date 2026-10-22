#!/usr/bin/env python3
"""Read-only independent package hashing; writes one sibling JSON only.
No target code is imported or executed. No Git, network, service, or subprocess.
"""
from pathlib import Path
import hashlib,json,zipfile,ast
A=Path(__file__).resolve().parent.parent
OWN=Path(__file__).resolve().parent
U=OWN/'_private_reading/unpacked/k605a_outer_focal_pedal_product'
P=A/'native_custody_01/archive/published'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_rows(base,rows):
    seen=set()
    for r in rows:
        assert r['path'] not in seen
        seen.add(r['path']);p=base/r['path']
        assert p.is_file() and not p.is_symlink()
        assert len(p.read_bytes())==r['bytes'] and digest(p)==r['sha256'],str(p)
    return seen
candidate=A/'review_candidate_02/PUBLIC_REVIEW_MANIFEST.json'
m=json.loads(candidate.read_text());verify_rows(A,m['files'])
s=json.loads((U/'SOURCE_MANIFEST.json').read_text());source_paths=verify_rows(U,s['files'])
actual={p.relative_to(U).as_posix() for p in U.rglob('*') if p.is_file()}
assert actual==source_paths|{'SOURCE_MANIFEST.json'}
vm=json.loads((U/'verification/MANIFEST.json').read_text());vp=verify_rows(U/'verification',vm['files'])
va={p.relative_to(U/'verification').as_posix() for p in (U/'verification').rglob('*') if p.is_file()}
assert va==vp|{'MANIFEST.json'}
publication=json.loads((P/'PACKAGE_MANIFEST.json').read_text())
for key in ['source_manifest','manuscript_source','metadata']:
 r=publication[key];assert len((P/r['path']).read_bytes())==r['bytes'] and digest(P/r['path'])==r['sha256']
for r in publication['submission_files']:
 assert len((P/r['path']).read_bytes())==r['bytes'] and digest(P/r['path'])==r['sha256']
for name in ['SOURCE_MANIFEST.json','manuscript.tex','manuscript.pdf','metadata.json']:
 assert (P/name).read_bytes()==(U/name).read_bytes()
assert json.loads((P/'deposit.json').read_text())['metadata']==json.loads((P/'metadata.json').read_text())
assert json.loads((U/'metadata.json').read_text())['creators'][0]['orcid']=='0009-0001-9320-500X'
with zipfile.ZipFile(P/'k605a-source-verification.zip') as z:
 names=z.namelist();assert len(names)==len(set(names))==181
 for n in names:
  q=Path(n);assert not q.is_absolute() and '..' not in q.parts
  assert z.read(n)==(OWN/'_private_reading/unpacked'/n).read_bytes()

# Independently verify archived-family payload bindings, without importing validators.
prov=json.loads((U/'verification/PROVENANCE.json').read_text())
for r in prov['original_files']:
 p=U/'verification'/r['portable_path'];assert p.stat().st_size==r['bytes'] and digest(p)==r['sha256']
families={}
for r in prov['families']:
 p=U/'verification/audits'/r['family']/'AUTHORED_MANIFEST.json'
 assert digest(p)==r['manifest_sha256']
 fm=json.loads(p.read_text());rows=fm.get('authored_files',fm.get('files'))
 verify_rows(p.parent,rows);families[r['family']]=len(rows)

# Read the literal job table via AST, never execute it.
t=ast.parse((U/'verification/run_verification.py').read_text());jobs=None;exclusions=None
for n in t.body:
 if isinstance(n,ast.Assign):
  for target in n.targets:
   if isinstance(target,ast.Name) and target.id=='JOBS':jobs=ast.literal_eval(n.value)
   if isinstance(target,ast.Name) and target.id=='EXCLUSIONS':exclusions=ast.literal_eval(n.value)
assert len(jobs)==10
receipt_rows=[]
for rel in ['DEFAULT_ATTESTED_TEN_JOBS.json','GENUINE_PRIMARY_MEROMORPHIC.json']:
 receipt=json.loads((A/'root_reproduction_preparation_01/results'/rel).read_text())
 assert receipt['integrity_before']==receipt['integrity_after']
 assert receipt['integrity_before']['manifest_sha256']==digest(U/'verification/MANIFEST.json')
 assert receipt['no_interval_certification'] is True and receipt['whole_manuscript_review'] is False
 assert receipt['sympy']=='1.14.0' and receipt['mpmath']=='1.3.0'
 for r in receipt['jobs']:
  job=r['job'];script,frozen,output=jobs[job]
  assert r['program_sha256']==digest(U/'verification'/script)
  assert r['frozen_result_sha256']==digest(U/'verification'/frozen)
  assert r['excluded_top_level_fields']==exclusions.get(job,{})
  expected=json.loads((U/'verification'/frozen).read_text())
  for k in exclusions.get(job,{}):del expected[k]
  canonical=json.dumps(expected,sort_keys=True,separators=(',',':')).encode()
  assert hashlib.sha256(canonical).hexdigest()==r['scientific_canonical_sha256']
  assert r['scientific_JSON_exact_equal'] is True
  receipt_rows.append({'receipt':rel,'job':job,'primary_mode':r['primary_mode'],'canonical_frozen_hash_verified':True})
primary={}
for name,path,h in [('invariants_v11.pdf',A/'_private_primary/RGK2020v11.pdf','c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da'),('invariants_final.pdf',A/'_private_primary/RGK2021.pdf','c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42'),('stachel_published.pdf',A/'root_reproduction_preparation_01/_private_primary/stachel_published.pdf','9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8')]:
 assert digest(path)==h;primary[name]=h
report={'passed':True,'candidate':{'manifest_bytes':candidate.stat().st_size,'manifest_sha256':digest(candidate),'files':len(m['files']),'payload_bytes':sum(r['bytes'] for r in m['files'])},'zip_entries':181,'zip_uncompressed_bytes':sum((U/p).stat().st_size for p in actual),'source_manifest_rows':len(source_paths),'portable_verification_manifest_rows':len(vp),'all_file_sets_exact':True,'original_submission_files':len(prov['original_files']),'authored_family_rows':families,'external_and_zip_paper_source_metadata_equal':True,'deposit_metadata_equal':True,'root_receipt_rows_bound':receipt_rows,'genuine_primary_pdf_hashes':primary,'executed_existing_jobs':False,'local_dependencies':'system and bundled Python lacked sympy; independent new controls use stdlib only; no installation attempted','effects':'read-only existing input; one sibling PACKAGE_CHECK_RESULTS.json written'}
(OWN/'PACKAGE_CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
