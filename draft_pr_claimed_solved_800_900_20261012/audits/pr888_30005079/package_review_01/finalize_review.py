"""Finalize only this review's authored, explicitly allowlisted evidence."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

H=Path(__file__).resolve().parent
A=H.parent
C=A/'candidate'
def sha(b):return hashlib.sha256(b).hexdigest()
def row(p):
    b=p.read_bytes()
    return {'path':p.name,'bytes':len(b),'sha256':sha(b)}
def require(x,s):
    if not x:raise ValueError(s)
def save(n,d):(H/n).write_text(json.dumps(d,indent=2)+'\n')
require(not (H/'DECISION.json').exists(),'final decision must be fresh')
ns={'__name__':'independent_review_finalize_import','__file__':str(H/'independent_controls.py')}
exec(compile((H/'independent_controls.py').read_bytes(),'independent_controls.py','exec',optimize=0),ns)
auth,inner,raw=ns['authenticate']()
for n,size,expected in [('INDEPENDENT_SOURCE_FREEZE.md',4605,'d1fd0f54da2cd68357a1d1db1be2f9721343ba8b7d782a5cb4608b03e251eaea'),
                        ('INDEPENDENT_MATH_FREEZE.md',6417,'dfb1a642e8b6658f837ee35e57599a8e52e164ac7c9e870e80f6d6c7e773805f')]:
    b=(H/n).read_bytes();require((len(b),sha(b))==(size,expected),'original complete freeze bytes restored')
cli=json.loads((H/'CLI_CONTROLS.json').read_text())
require(cli['status']=='PASS' and cli['actual_fresh_cli_invocations']==8,'fresh CLI summary')
direct=[]
for r in cli['receipts']:
    p=H/'private_tmp'/('fresh_'+r['label']+'.process_record.json')
    b=p.read_bytes();require({'bytes':len(b),'sha256':sha(b)}==r['direct_process_record_pin'],'direct actual status record pin')
    d=json.loads(b);require(d['returncode']==r['returncode']==r['expected_returncode'],'direct actual status expected')
    require(d['started_utc'] and d['completed_utc'] and d['returncode_record_provenance'].startswith('Direct actual'),'direct measurement provenance')
    direct.append(d)
save('FRESH_PROCESS_RECORDS.json',{'scope':'Unmodified redacted per-case records persisted immediately after actual subprocess returns, before later assertions. These are eight fresh cases; historical eight are separate.','records':direct})
now=datetime.now(timezone.utc).isoformat()
core_manifest=A/'final_package_engineering_01/CANDIDATE_CORE_PINS.json'
save('FINAL_CORE_UNCHANGED.json',{'timestamp_utc':now,'status':'PASS',**auth,
    'core_manifest':row(core_manifest),'all179_candidate_files_unchanged':True,
    'original_freezes_restored_to_original_full_hashes':True,
    'scope':'End-of-review independent reauthentication, including actual original Git objects; no candidate mutation.'})
gate=A/'PRE_WHOLE_REVIEW_GATE.json'
fresh_source=next(r['result'] for r in cli['receipts'] if r['label']=='source_only_complete_corpora')
save('INPUT_PINS.json',{'timestamp_utc':now,'pr':888,'problem_id':'30005079','original_head':'a7571ddbbbe2de3600b96bd7ccccf86e4d5748e7',
    'original_effort':'1/5','eligibility_gate':row(gate),'external_core_manifest':row(core_manifest),
    'external_original_source_manifest':row(A/'SOURCE_MANIFEST.json'),
    'current_assets':[row(C/n) for n in ['CURRENT_PUBLICATION_MANIFEST.json','portable.py','note.tex','rank-two-fano-note.pdf','rank-two-fano-verification.zip','metadata.json','zenodo-deposit.json']],
    'portable_index':row(C/'verification/package_index.json'),
    'complete_corpora_authenticated_before_target_parsing':fresh_source['inputs'],
    'canonical_pair_bytes':5415,'canonical_pair_sha256':'6bbb2826e583f9ccbbb38411ce780e865c0b9564b74bf9f6eca5250f4b06e083',
    'native_target_report':'ABSENT','primary_route_body_pins':fresh_source['primary_sources']['pins'],
    'paper_pdf_pages_visually_reviewed':5,
    'additional_priority_body_pin_observations':'INDEPENDENT_CONTROLS.json',
    'historical_gate_limit':'The supplied pre-review metadata gate is authenticated here; no fresh remote mutation or second clearance is inferred.'})
save('DECISION.json',{'timestamp_utc':now,'review':'package_review_01','pr':888,'problem_id':'30005079',
    'decision':'CLEAR','review_completion_percent':100,'original_effort':'1/5',
    'original_head':'a7571ddbbbe2de3600b96bd7ccccf86e4d5748e7',
    'candidate_core_manifest_sha256':sha(core_manifest.read_bytes()),
    'current_manifest_sha256':sha((C/'CURRENT_PUBLICATION_MANIFEST.json').read_bytes()),
    'candidate_files':179,'archive_members':150,'original_source_files':21,'original_source_bytes':98055,
    'strongest_verified_result':'The explicit smooth Fano fivefold Bl_C(Q) times F1 has the unique global H-minimizing valuation with exactly aZ+bZ of rational rank two and singular canonical first center Bl_C(Q0) times F1; the original is smooth and the first central pair is already weighted polystable.',
    'blocking_issues':[],'required_candidate_repairs':[],
    'exact_remaining_mathematical_gap':'No unresolved proof or theorem-applicability gap identified, conditional on the stated established theorem inputs and standard foundations.',
    'explicit_external_mathematical_inputs':['Miao-Wang v2 factor special degeneration and weighted polystability','Wang-Zhu smooth toric soliton existence','Han-Li generalized singular soliton/YTD and boundedness facts','Han-Li v1 global minimizer criterion/comparison of infima','BLXZ v2 absolute uniqueness and singular soliton-polystability equivalence','Hermite-Lindemann and standard algebraic/pluripotential foundations'],
    'qualifying_replays':{'directly_recorded_full_replays':4,'original_root_processes':4,'actual_checker_processes':24,'positive_children':8,'assertion_negative_children':8,'corrupt_code_guard_children':8,'separate_in_process_patch_controls':12},
    'additional_actual_cli_counts':{'fresh_collector_cases':8,'historical_initial_collector_cases_separate':8,'initial_manual_wrapper_cases':3,'total_wrapper_invocations':17,'total_direct_optimized_original_root_rejections':2,'total_actual_full_replays_including_historical_hostile':5,'historical_hostile_replay_exit_provenance':'Guard-inferred, explicitly qualified; excluded from four qualifying direct-status replays.'},
    'independent_distinct_in_process_negative_controls':25,
    'reviewer_evidence_repairs':['Original complete freeze bodies restored byte-for-byte; later-observed mutable filesystem times separately qualified.','Initial collector expected-hash typo and inferred recovery preserved; eight fresh cases directly recorded before later assertions.'],
    'priority_boundary':'Bounded and uncertified. Serious Li-Li predecessor credited, its case2 arithmetic rank left unverified; no novelty/firstness/continued-open claim in the paper.',
    'trust_boundaries':['Established external theorem bodies are inputs, not newly formally verified.','AI review; human peer review and formal verification are incomplete.','Selected CPython/standard library trusted and unpinned.','No OS sandbox or adversarial concurrent-filesystem race guarantee.','Compressed-byte equality limited to same Python ZIP/zlib runtime.','Finite controls do not prove universal malformed-input rejection.'],
    'candidate_unchanged':True,'safe_manifest':'SAFE_MANIFEST.json',
    'whole_package_clearance_count_supplied_by_this_review':1,'publication_approval':False,
    'mutations_outside_this_review':False,'external_communication':False})
with (H/'RESEARCH_LOG.md').open('a') as f:
    f.write('- '+now+' — 100%: Eight fresh evidence-repair CLI cases passed with actual per-case status records saved before later assertions. Qualifying four full replays and 25 distinct complementary controls pass. Original full freezes restored; no substantive freeze content changed. End-of-review 179-file core and 21 actual Git blobs reauthenticated unchanged. CLEAR issued for this one review; safe allowlist finalized.\n')
with (H/'PROVENANCE_ERRATUM.md').open('a') as f:
    f.write('\nFinal evidence-repair checkpoint '+now+': all eight fresh actual cases passed. FRESH_PROCESS_RECORDS.json preserves their immediately persisted direct status records. Historical initial cases and qualified recovery remain separate and are not counted as fresh/direct evidence. The original freeze hashes are rechecked at finalization.\n')
allow=['INDEPENDENT_SOURCE_FREEZE.md','INDEPENDENT_MATH_FREEZE.md','FREEZE_TIMESTAMPS.json','PROVENANCE_ERRATUM.md',
       'EARLY_RESEARCH_LOG_RECONSTRUCTION.md','RESEARCH_LOG.md','REPORT.md','DECISION.json','INPUT_PINS.json',
       'BIBLIOGRAPHIC_AND_PDF_CHECKS.md','INITIAL_CORE_AUTHENTICATION.json','INDEPENDENT_CONTROLS.json','CLI_CONTROLS.json',
       'HISTORICAL_CLI_RECOVERY_QUALIFIED.json','FRESH_PROCESS_RECORDS.json','CURRENT_NORMAL_RECEIPT.json',
       'CURRENT_OPTIMIZED_RECEIPT.json','DEFAULT_FRESH_OUTSIDE_BUILD_RECEIPT.json','FINAL_CORE_UNCHANGED.json',
       'independent_controls.py','cli_controls.py','finalize_review.py']
for n in allow:
    p=H/n;require(p.is_file() and not p.is_symlink(),'safe regular file')
    text=p.read_text();require(not re.search(r'/Users/[A-Za-z0-9_.-]+/|/private/(?:var|tmp)/',text),'absolute private path in safe output')
    if n.endswith('.json'):ns['js'](p.read_bytes())
save('SAFE_MANIFEST.json',{'timestamp_utc':now,'schema':'pr888-package-review01-safe-v1','pr':888,'problem_id':'30005079',
    'scope':'Explicit authored reports/code/receipts only; this is one review clearance and not permission to publish.',
    'self_excluded':True,'manifest_filename':'SAFE_MANIFEST.json',
    'files':[row(H/n) for n in sorted(allow)],'total_payload_bytes':sum((H/n).stat().st_size for n in allow),
    'excluded':['SAFE_MANIFEST.json itself from its file-hash list','private_tmp/** including all original raw receipts, failed collector code, fixtures, renders and scratch','complete corpora','raw scholarly bodies','wheels or installed runtimes','all unlisted files'],
    'privacy_scan':'PASS: no absolute private workspace/temp paths in allowlisted text; raw private traces are hashed and transparently qualified/redacted.'})
for n in ['REPORT.md','DECISION.json','SAFE_MANIFEST.json']:
    print(json.dumps(row(H/n)))
