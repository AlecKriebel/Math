"""Independent local-byte checks only. No action helper is imported or executed."""
from pathlib import Path
from datetime import datetime,timezone
import ast,hashlib,json,zipfile

OUT=Path(__file__).resolve().parent;D=OUT.parent;CASE=D.parent;R=CASE/'preprint';P=CASE/'publication'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pins=json.loads((D/'ROOT_RELEASE_BINDING_TEST_RESULTS.json').read_text())['current_helpers']
helper_checks=[]
for row in pins:
    p=P/row['path'];compile(p.read_text(),str(p),'exec');tree=ast.parse(p.read_text())
    helper_checks.append(dict(path=row['path'],bytes=p.stat().st_size,sha256=sha(p),matches_fixed_input=p.stat().st_size==row['bytes'] and sha(p)==row['sha256']))
assert all(r['matches_fixed_input'] for r in helper_checks)
prior=D/'release_helpers_adversary_01';prior_seal=prior/'AUTHORED_MANIFEST.json'
assert sha(prior_seal)=='93dc2effc5e82afb561faa7b992bdd7e95d249ce6d0e9d282427876a98f48619'
prior_files=[]
for row in json.loads(prior_seal.read_text())['files']:
    p=prior/row['path'];prior_files.append(dict(path=row['path'],matches=p.stat().st_size==row['bytes'] and sha(p)==row['sha256']))
assert all(r['matches'] for r in prior_files)
prior_probes=json.loads((prior/'PROBE_RESULTS.json').read_text());frozen=[]
for row in prior_probes['helper_pins']:
    p=D/'history/release_helpers_review01_frozen'/Path(row['path']).name
    frozen.append(dict(path=p.name,matches=p.stat().st_size==row['bytes'] and sha(p)==row['sha256']))
assert all(r['matches'] for r in frozen)
package=json.loads((R/'PACKAGE_MANIFEST.json').read_text());package_checks=[]
for row in package['submission_files']+[package[k] for k in ['source_manifest','manuscript_source','metadata']]:
    p=R/row['path'];package_checks.append(dict(path=row['path'],bytes=p.stat().st_size,sha256=sha(p),matches=p.stat().st_size==row['bytes'] and sha(p)==row['sha256']))
assert all(r['matches'] for r in package_checks)
deposit=json.loads((R/'deposit.json').read_text());meta=json.loads((R/'metadata.json').read_text())
assert set(deposit)=={'metadata','files'} and deposit['metadata']==meta
assert deposit['files']==[dict(path='manuscript.pdf',name='k605a-outer-focal-pedal-areas.pdf'),dict(path='k605a-source-verification.zip',name='k605a-source-verification.zip')]
intake=json.loads((D/'INTAKE.json').read_text());original=[]
with zipfile.ZipFile(R/'k605a-source-verification.zip') as archive:
    names=archive.namelist();assert len(names)==len(set(names))==181
    assert all(not x.startswith('/') and '..' not in Path(x).parts for x in names)
    U=R/'pr_update/5100033';prefix='k605a_outer_focal_pedal_product/pr_update/5100033/'
    native={p.relative_to(U).as_posix():p.read_bytes() for p in U.rglob('*') if p.is_file()}
    zipped={n.removeprefix(prefix):archive.read(n) for n in names if n.startswith(prefix)}
    assert native==zipped
    for row in intake['original_source_files']:
        relative=row['native_path'].removeprefix('unsolved_math_prioritization/attempts/5100033/')
        roots=[D/'submitted/unsolved_math_prioritization/attempts/5100033',U/'history/original_submission_20261015',R/'verification/original_submission']
        for root in roots:
            p=root/relative;original.append(dict(path=str(p.relative_to(CASE)),matches=p.stat().st_size==row['bytes'] and sha(p)==row['sha256']))
    assert len(original)==60 and all(r['matches'] for r in original)
results=dict(utc=datetime.now(timezone.utc).isoformat(),scope='Local byte validation only; not a whole-manuscript review',completion_percent=95,
    helper_checks=helper_checks,first_review_seal_sha256=sha(prior_seal),first_review_payload_checks=prior_files,
    frozen_original_helper_checks=frozen,package_pin_checks=package_checks,zip_entries=len(names),
    native_zip_path_and_byte_equality=True,native_file_count=len(native),original20_three_copy_checks=original,
    actual_final_clearance_present=(R/'FINAL_CLEARANCE.json').exists(),actual_usable_publication_present=(P/'ZENODO_VERIFIED_PUBLICATION.json').exists(),
    provider_or_network_calls=0,action_helpers_executed=False)
(OUT/'LOCAL_INTEGRITY_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({k:v for k,v in results.items() if k not in ['original20_three_copy_checks']},indent=2))
