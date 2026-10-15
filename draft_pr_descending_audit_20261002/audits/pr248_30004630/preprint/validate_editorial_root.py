from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, subprocess, zipfile

PRE = Path(__file__).resolve().parent
D = PRE.parent / 'initial_review_20261013'
PY = PRE.parents[2] / 'audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python'
HISTORY = Path(json.loads((PRE/'EDITORIAL_REFINEMENT.json').read_text())['history_snapshot'])
R = PRE/'root_editorial_reproduction'
R.mkdir(exist_ok=True)

def pin(p):
    b=p.read_bytes()
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def normal(x):
    return {k:v for k,v in x.items() if k not in {'utc','python'}}

review=PRE/'fresh_review_02'
m=json.loads((review/'FINAL_AUDIT_MANIFEST.json').read_text())
for q in m['public_authored_relative_paths']:
    assert pin(review/q['path'])=={k:q[k] for k in ['bytes','sha256']}
for q in m['candidate_files']:
    assert pin(HISTORY/q['path'])=={k:q[k] for k in ['bytes','sha256']}
assert pin(review/'independent_reconstruction.md')['sha256']==m['initial_proof_sha256']
evidence=json.loads((review/'EVIDENCE_PIN_READBACK.json').read_text())
for q in evidence['external_reading_pins']:
    if 'path' in q:
        p=Path(q['path'])
    else:
        p=D/'priority_recent_adversary_01/private_reading'/q['name']
    assert pin(p)=={k:q[k] for k in ['bytes','sha256']},str(p)
stress=R/'review02_stress2274'
stress.mkdir(exist_ok=True)
shutil.copyfile(review/'independent_stress_checks.py',stress/'independent_stress_checks.py')
run=subprocess.run([str(PY),str(stress/'independent_stress_checks.py')],cwd=stress,capture_output=True,text=True,timeout=120)
(stress/'stdout.txt').write_text(run.stdout)
(stress/'stderr.txt').write_text(run.stderr)
assert run.returncode==0,run.stderr
actual=json.loads((stress/'INDEPENDENT_STRESS_RECEIPT.json').read_text())
expected=json.loads((review/'INDEPENDENT_STRESS_RECEIPT.json').read_text())
assert normal(actual)==normal(expected)
assert actual['assertions']==2274
for spec in json.loads((review/'extracted_archive/CHECKSETS.json').read_text()):
    actual=json.loads((review/'independent_replays'/spec['name']/'ACTUAL_RECEIPT.json').read_text())
    expected=json.loads((review/'extracted_archive'/spec['reference']).read_text())
    assert normal(actual)==normal(expected)
accept={'utc':datetime.now(timezone.utc).isoformat(),'reviewer':'fresh_review_02',
        'verdict':'PASS; no mandatory issues on preserved prior draft',
        'candidate_scope':'Historical draft in '+str(HISTORY),
        'root_full_read':['REPORT.md','independent_reconstruction.md','SOURCE_PRIORITY_LEDGER.md','audit_package.py','audit_evidence.py','independent_stress_checks.py'],
        'public_pins_verified':len(m['public_authored_relative_paths']),
        'historical_candidate_pins_verified':5,'initial_independence_proof_unchanged':True,
        'external_reading_pins_verified':len(evidence['external_reading_pins']),
        'all_seven_scientific_receipts_match':True,'root_isolated_stress_exact_assertions':2274,
        'root_stress_complete_receipt_match_excluding_only_utc_python':True,
        'manifest_sha256':pin(review/'FINAL_AUDIT_MANIFEST.json')['sha256'],
        'editorial_refinements_elected':True,'NEW_full_revised_review_pending':True,
        'upload_clearance':False}
(PRE/'ROOT_REVIEW02_ACCEPTANCE.json').write_text(json.dumps(accept,indent=2)+'\n')

root=R/'extracted'
root.mkdir(exist_ok=True)
with zipfile.ZipFile(PRE/'output/critical_wave_verification.zip') as z:
    assert len(z.infolist())==113 and z.testzip() is None
    z.extractall(root)
run=subprocess.run([str(PY),str(root/'verify_all.py')],cwd=R,capture_output=True,text=True,timeout=240)
(R/'stdout.txt').write_text(run.stdout)
(R/'stderr.txt').write_text(run.stderr)
assert run.returncode==0,run.stderr
report=json.loads((R/'VERIFICATION_RUN.json').read_text())
assert report['status']=='PASS' and report['exact_assertions']==5603 and report['noncertified_diagnostics']==5
assert report['packaged_files_verified']==112 and report['checksets']==7
for spec in json.loads((root/'CHECKSETS.json').read_text()):
    a=next(x['receipt'] for x in report['results'] if x['checkset']==spec['name'])
    assert normal(a)==normal(json.loads((root/spec['reference']).read_text()))
assert (root/'manuscript/critical_wave_growth.tex').read_bytes()==(PRE/'critical_wave_growth.tex').read_bytes()
assert json.loads((root/'metadata.json').read_text())==json.loads((PRE/'metadata.json').read_text())==json.loads((PRE/'deposit.json').read_text())['metadata']
qa=[]
for p in sorted((PRE/'tmp/pdfs_editorial').glob('page-*.png')):
    qa.append({'path':str(p),**pin(p),'root_visually_inspected':True,'layout_defects_found':False})
assert len(qa)==6
freeze=json.loads((PRE/'FROZEN_CANDIDATE.json').read_text())
for q in freeze['files']:
    assert pin(PRE/q['path'])=={k:q[k] for k in ['bytes','sha256']}
accept={'utc':datetime.now(timezone.utc).isoformat(),'case_percent':80,
        'PDF_pages':6,'root_all_pages_visual_QA':qa,'tectonic_export':'success',
        'desktop_source_compilation':'success','latex_warning_scan':'No matches',
        'scientific_equations_and_claims_unchanged':True,
        'archive_files':113,'full_replayed_scientific_receipts':7,
        'exact_assertions':5603,'noncertified_diagnostics':5,
        'root_replay_report':str(R/'VERIFICATION_RUN.json'),
        'candidate_files':freeze['files'],'metadata_exact_three_way_equality':True,
        'two_earlier_full_reviews_PASS_on_preserved_draft':True,
        'revised_NEW_full_review03_pending':True,'revised_review01_delta_pending':True,
        'upload_clearance':False}
(PRE/'ROOT_EDITORIAL_PACKAGE_ACCEPTANCE.json').write_text(json.dumps(accept,indent=2)+'\n')
print(json.dumps({'status':'PASS','old_review02_public_pins':len(m['public_authored_relative_paths']),
                  'root_new_stress_assertions':2274,'revised_archive_checksets':7,
                  'exact_assertions':5603,'diagnostics':5,'upload_clearance':False},indent=2))
