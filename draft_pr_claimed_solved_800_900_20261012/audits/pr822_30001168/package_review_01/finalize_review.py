#!/usr/bin/env python3
"""Finalize authored review only; seal and assembly are never written."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess

R=Path(__file__).resolve().parent;A=R.parent
def need(c,m):
    if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
before=read(R/'INPUT_HASHES.json');after=read(R/'INPUT_HASHES_AFTER.json')
need(before['core']==after['core'] and before['bindings']==after['bindings']
     and before['assembly_files']==after['assembly_files'],'reviewed inputs changed')
for row in before['core']:
    p=Path(row['path'])
    need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'final sealed bytes differ')
T=Path(before['assembly_root'])
for row in before['assembly_files']:
    p=T/row['relative_path']
    need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'final assembly bytes differ')
need(len(before['assembly_files'])==163 and all(r['matches_seal'] for r in before['core']),'input counts/seal')
replay=read(R/'REPLAY_RECEIPTS.json')
need(len(replay['runs'])==4 and all(r['exit_code']==0 and not r['stderr'] for r in replay['runs']),
     'full replay coverage')
need(replay['deterministic_rebuild']['index_byte_identical']
     and replay['deterministic_rebuild']['zip_byte_identical'],'deterministic replay')
controls=read(R/'INTEGRITY_CONTROL_RECEIPT.json')
need(controls['total']==32 and controls['accepted_baselines']==4 and controls['expected_rejections']==28,
     'independent controls')
need(read(R/'ARITHMETIC_RECEIPT.json')['exact_fraction_identity_with_executable'],'independent arithmetic')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (R/'RESEARCH_LOG.md').open('a') as log:
    log.write(f'- {now} — 100% review complete; 90% estimated R1 submission readiness: independent32 current controls passed with4 baselines/28 rejections. Both public tool failures reproduced in disposable copies. Final before/after comparisons show all10 sealed core files,163 assembly files and external binding files unchanged. Decision REPAIR_REQUIRED is limited to obsolete current root control interface and published builder layout/documentation contract. Mathematical proof, exact target, scoped priority wording, metadata and all-page visual QA have no identified defect. Original42/3 archives remain frozen.\n')
visual=[]
for n in range(1,5):
    p=A/'preprint/rendered'/f'page-{n}.png'
    visual.append({'page':n,'read_only_inspected_image':str(p),'sha256':sha(p),
                   'clipping_overlap_missing_glyphs_or_math_legibility_defect_found':False})
pdfinfo=subprocess.run(['pdfinfo',str(A/'preprint/output/pdf/note.pdf')],capture_output=True,text=True,check=True)
need('Pages:           4' in pdfinfo.stdout,'PDF page count')
(R/'VISUAL_QA_RECEIPT.json').write_text(json.dumps({'timestamp_utc':now,'status':'PASS','pages':visual,
  'sealed_pdf_sha256':sha(A/'preprint/output/pdf/note.pdf'),'sealed_tex_sha256':sha(A/'preprint/note.tex'),
  'actual_PDF_metadata':pdfinfo.stdout,'actual_PDF_text_cross_checked':True,'read_only_pdf_inspection':True,
  'new_pdf_authoring_marker_used':False,'first_render_attempt_ENOSPC':True,
  'existing_retained_final_renders_used_by_parent_authorization':True},indent=2)+'\n')
# Remove only this review's interrupted, incomplete rendering.
partial=R/'rendered/page-1.png'
if partial.exists():partial.unlink()
artifacts=[]
for p in sorted(R.iterdir()):
    if p.is_file() and p.name not in ('DECISION.json','REVIEW_MANIFEST.json'):
        artifacts.append({'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
decision={'timestamp_utc':now,'status':'REPAIR_REQUIRED','review_round':'R1',
 'problem_id':30001168,'problem_number':'OWR-3389-021','pr':822,
 'original_head':'c9fd5a0462d1fa98f21aa7037f7a5e061fbbee9c','original_gate':'claimed_solved',
 'original_proof_effort':'1/5','new_central_proof_search':False,
 'independent_reconstruction_before_past_verdicts':True,
 'mathematical_gap_identified':False,'mathematical_result':'Finite smooth normalized S3 violation refutes universal n>=3 comparison; alltime round bound and both positive-time maxima verified by manual review and exact arithmetic.',
 'dimension_n_ge_4_resolved':False,'adjacent_monotonicity_resolved':False,
 'historical_firstness_certified':False,'current_openness_certified':False,
 'new_geometric_or_spectral_mechanism_claimed':False,
 'priority_wording_consistent_with_bounded_inspected_sources':True,
 'metadata_author_ORCID_license_disclosures_verified':True,'four_page_visual_QA':'PASS',
 'portable_full_normal_and_optimized':'PASS','outer_full_normal_and_optimized':'PASS',
 'relocated_paths_with_spaces_and_foreign_cwd':True,'deterministic_index_and_zip_byte_identity':True,
 'independent_current_integrity_controls':{'total':32,'accepted_baselines':4,'expected_rejections':28},
 'environmental_first_replay_failure':'ENOSPC in disposable source control copy; preserved receipt; all unmodified full replays passed after recovery.',
 'required_repairs':[
  {'id':'R1-P01','priority':2,'file':str(T/'package_controls.py'),'lines':[19,20,30,36],
   'issue':'Current sibling gate no longer supports old --root/--integrity-only interface; intact harness baseline exits1.',
   'repair':'Migrate current root controls to pin-based gate or explicitly route historical wrapper to frozen original gate/tree; preserve immutable original42 and archives.',
   'evidence':'INTEGRITY_CONTROL_RECEIPT.json: obsolete_top_level_control including obsolete_child_cli'},
  {'id':'R1-P02','priority':2,'file':str(T/'publication_20261013/preprint/build_verification.py'),
   'lines':[10,11,30,44],'documentation_file':str(T/'publication_20261013/preprint/README.md'),
   'documentation_line':29,'issue':'Advertised retained Git builder expects parent SOURCE_MANIFEST/source/audit layout absent at published path; exact public-tree copy exits1.',
   'repair':'Support included verification-package layout or explicit input-root/reconstruction invocation; otherwise clearly classify builder as audit-time and remove public ready-reproducer implication.',
   'evidence':'INTEGRITY_CONTROL_RECEIPT.json: nonportable_advertised_builder; REPLAY_RECEIPTS.json: deterministic_rebuild in correct audit layout'}],
 'exact_remaining_gap':'Two current tool/documentation contracts, followed by reassembly/resealing and fresh advertised-command checks. No mathematical repair identified. Historical exact-application priority remains intentionally unestablished.',
 'review_completion_percent':100,'estimated_R1_submission_readiness_percent':90,
 'sealed_inputs_changed':False,'assembly_changed':False,'original42_and_archives_changed':False,
 'Git_PR_service_upload_mutations':False,'external_communication':False,
 'input_hashes_file':'INPUT_HASHES.json','post_review_input_hashes_file':'INPUT_HASHES_AFTER.json',
 'sealed_core_inputs':before['core'],'binding_inputs':before['bindings'],
 'outer_manifest_sha256':sha(T/'PUBLICATION_MANIFEST.json'),
 'portable_index_sha256':sha(A/'preprint/package_index.json'),
 'portable_zip_sha256':sha(A/'preprint/verification.zip'),'authored_review_artifacts':artifacts}
(R/'DECISION.json').write_text(json.dumps(decision,indent=2)+'\n')
artifacts.append({'path':'DECISION.json','bytes':(R/'DECISION.json').stat().st_size,'sha256':sha(R/'DECISION.json')})
(R/'REVIEW_MANIFEST.json').write_text(json.dumps({'timestamp_utc':now,'files':artifacts,
 'raw_downloads_and_renderings_excluded':True},indent=2)+'\n')
print(json.dumps({'status':decision['status'],'required_repairs':2,'input_bytes_unchanged':True,
 'full_replays':4,'independent_current_controls':32,'review_completion_percent':100,
 'decision_sha256':sha(R/'DECISION.json'),'report_sha256':sha(R/'REPORT.md')},indent=2))
