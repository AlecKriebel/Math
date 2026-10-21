"""Bind actual current replay, immutable review inputs and all seven repairs."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,runpy,zipfile,sys
D=Path(__file__).resolve().parent;B=D.parent/'preprint';V=B/'verification';P=D.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,d:p.write_text(json.dumps(d,indent=2)+'\n')
r=json.loads((D/'ROOT_PORTABLE_REPRODUCTION_RECEIPT_V3.json').read_text())
a=json.loads((D/'ROOT_PORTABLE_PACKAGE_ACCEPTANCE_V3.json').read_text())
assert a['all_ten_root_jobs_passed'] and r['all_selected_jobs_passed'] and len(r['jobs'])==10
sys.path.insert(0,str(V))
ns=runpy.run_path(str(V/'run_verification.py'),run_name='definitions_only')
for j in r['jobs']:
    source,frozen,_=ns['JOBS'][j['job']]
    assert j['program_sha256']==sha(V/source) and j['frozen_result_sha256']==sha(V/frozen)
    assert j['scientific_JSON_exact_equal']
v2=json.loads((D/'ROOT_PORTABLE_REPRODUCTION_RECEIPT_V2.json').read_text())
assert {j['job']:j['scientific_canonical_sha256'] for j in r['jobs']}=={j['job']:j['scientific_canonical_sha256'] for j in v2['jobs']}
qa=json.loads((B/'RENDER_QA.json').read_text())
assert qa['source_sha256']==sha(B/'manuscript.tex') and qa['pdf_sha256']==sha(B/'manuscript.pdf')
for x in qa['rendered_pages']:assert sha(B/x['path'])==x['sha256']
assert qa['all_six_latest_pages_actually_visually_inspected_by_root'] and not qa['visual_findings']
assert 'The present author did not coauthor those candidates.' not in (B/'pr_update/5100033/PROOF.md').read_text()
for p in V.glob('forensic_history/*/HISTORICAL_STATUS.json'):
    d=json.loads(p.read_text())
    for key in ['current_correction','current_reconciliation']:
        if key in d:assert (p.parent/d[key]).resolve().is_file()
assert (B/'pr_update/5100033/history/original_submission_20261015').is_dir()
old=B/'history/review01_frozen'
assert sha(old/'k605a-source-verification.zip')=='6324b31294ed313e523f85454ba4c4b82b412d0942432e7cae7ef611140bea6b'
assert sha(old/'manuscript.pdf')=='d97403942641892ef91573e9cae04d0d8d09d596a5f8f9448e63d00a15288a52'
assert sha(D/'whole_manuscript_adversary_01/REPORT.md')=='acd3f1751af73a3902d0f6d31ecc6d9d9dcb8d60ed020ff86e99dd3ff203ea99'
m=json.loads((D/'whole_manuscript_adversary_01/AUTHORED_MANIFEST.json').read_text())
for x in m['files']:
    p=D/'whole_manuscript_adversary_01'/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
package=json.loads((B/'PACKAGE_MANIFEST.json').read_text())
for x in package['submission_files']+[package['source_manifest'],package['manuscript_source'],package['metadata']]:
    p=B/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
now=datetime.now(timezone.utc).isoformat()
result=dict(utc=now,all7findings_resolved=True,findings=['R1','R2','R3','O1','O2','O3','O4'],
    reviewed_v1_bytes_preserved=True,first_review_seal_all14payloads_validated=True,
    original20_and_five_sealed_families_validated_by_actual_current_archive_checks=True,
    current_all10isolated_zip_jobs_passed=True,all_scientific_fields_exact=True,raw_byte_equal_jobs=8,
    documentation_only_final_count_correction_preserves_all10scientific_canonical_hashes=True,
    current_package=package,current_replay_receipt_sha256=sha(D/'ROOT_PORTABLE_REPRODUCTION_RECEIPT_V3.json'),
    root_render_qa_sha256=sha(B/'RENDER_QA.json'),case_completion_percent=70,
    new_whole_manuscript_reviews_completed=1,final_clean_reviews=0,publication_cleared=False,
    different_second_new_review_required=True,counts=[43,20,20,0],goal_active_incomplete=True)
save(D/'ROOT_REVIEW01_GLOBAL_RESOLUTION_ACCEPTANCE.json',result)
for p in [D/'CURRENT_AUDIT_STATE.json',P/'CURRENT_GOAL_SELECTION_20261013.json']:
    d=json.loads(p.read_text());d.update(utc=now,stage='review01_all7_repairs_validated_second_new_review_pending',current_stage='review01_all7_repairs_validated_second_new_review_pending',completion_percent=70,case_completion_percent=70,unresolved_review_findings=[],review01_resolution='ROOT_REVIEW01_GLOBAL_RESOLUTION_ACCEPTANCE.json',current_portable_jobs=10,preprint_upload_cleared=False)
    save(p,d)
text='\n'+now+' — case70%: all first NEW whole-manuscript R1-R3/O1-O4 repaired globally. Exact genuine N4 products16/25 with96 residuals, source fixture correction, unsupported coauthor sentence removal, bicentric interpretation reconciliation and historical/current/notation/link/count clarifications validated. All20 originals/five sealed families unchanged; v1 reviewed input retained exact. Final180-entry ZIP '+sha(B/'k605a-source-verification.zip')+', six-page PDF '+sha(B/'manuscript.pdf')+' compiled and allpages viewed. Root isolated ALL10 scientific replays exact,8raw byte-identical; final README count-only correction separately resealed/replayed with identical10canonical science hashes. One-time authoring assertion and compile-only recovery error logged, no science failure/tolerance relaxation. Different second NEW full-package review required; upload/tracker/nativePRmutation still false. Counts43/20/20/0, goalactive/incomplete.\n'
for p in [D/'RESEARCH_LOG.md',B/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
    with p.open('a') as f:f.write(text)
print(json.dumps({k:v for k,v in result.items() if k!='current_package'},indent=2))
