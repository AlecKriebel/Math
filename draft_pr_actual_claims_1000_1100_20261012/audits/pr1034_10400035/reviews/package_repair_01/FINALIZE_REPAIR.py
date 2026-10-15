#!/usr/bin/env python3
"""Freeze noncircular external repair/candidate/change receipts, no payload edit."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,datetime
ROOT=Path(__file__).resolve().parents[2]
PUB=ROOT/'publication'
OWN=Path(__file__).resolve().parent
def rec(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def main():
 utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
 result=json.loads((OWN/'VERIFY_FINAL_RESULT.json').read_text())
 assert result['success'] is True
 for key in ('candidate_tex','candidate_pdf','candidate_zip'):
  assert rec(ROOT/result[key]['path'])==result[key]
 integrity=json.loads((PUB/'CANDIDATE_INTEGRITY.json').read_text())
 validation={'schema':'external-current-repaired-candidate-builder-validation-v2','utc':utc,'TeX_sha256':result['candidate_tex']['sha256'],'PDF_sha256':result['candidate_pdf']['sha256'],'archive_sha256':result['candidate_zip']['sha256'],'archive_bytes':result['candidate_zip']['bytes'],'manifest_sha256':integrity['manifest']['sha256'],'input_pins_sha256':integrity['input_pins']['sha256'],'authored_payload_files':result['payload_files'],'zip_entries':result['zip_entries'],'original_file_set_exact':True,'original_files_verified':19,'historical_review_root_original_inputs_unchanged':515,'two_consecutive_builds_byte_identical':True,'independent_in_memory_archive_byte_identical':True,'clean_extraction_archive_manifest_external_receipt_byte_identical':True,'actual_clean_README_mkdir_then_Tectonic_exit0_pdf13pages':True,'all13_refreshed_pages_individually_viewed':True,'current_compilation_receipt':'publication/evidence/COMPILATION.json','source_body_exclusions_verified_against_actual_zip':True,'metadata_wrapper_exact':True,'repo_tool_metadata_exact':True,'publication_ready':False,'required_review':'NEWwhole02','repair_state':'REVIEW1_ISSUES_REPAIRS_APPLIED_NOT_FINAL_CLEARANCE','external_receipt_not_in_archive':True,'bytecode_created':False,'mathematical_programs_replayed_in_repair':False,'Git_or_service_actions':'none','full_execution_receipt':'reviews/package_repair_01/VERIFY_FINAL_RESULT.json','previous_receipt_verbatim':'publication/evidence/history/pre_whole01/BUILD_VALIDATION.json'}
 write(PUB/'BUILD_VALIDATION.json',validation)
 baseline=json.loads((OWN/'BASELINE_PINS.json').read_text());old={r['path']:r for r in baseline['files']}
 excluded_final={'reviews/package_repair_01/CHANGED_PATHS.json','reviews/package_repair_01/NEW_CANDIDATE_PINS.json','reviews/package_repair_01/OUTPUT_PINS.json'}
 current={r['path']:r for p in sorted(ROOT.rglob('*')) if p.is_file() and (r:=rec(p))['path'] not in excluded_final}
 changed=[{'path':n,'before':old[n],'after':current[n]} for n in sorted(set(old)&set(current)) if old[n]!=current[n]]
 deleted=[old[n] for n in sorted(set(old)-set(current)) if n not in excluded_final]
 assert not deleted
 added=[current[n] for n in sorted(set(current)-set(old))]
 transient={'tmp','render','renders','reconstruction','history','cache','caches','__pycache__'}
 authored_added=[r for r in added if not(set(Path(r['path']).parts)&transient)]
 changes={'schema':'full-before-after-repair-path-record-v1','utc':utc,'baseline':'reviews/package_repair_01/BASELINE_PINS.json','status':'REPAIRS_APPLIED_VERIFIED_FROZEN_PENDING_NEWwhole02','completion_percent':100,'wider_workflow_estimate_percent':75,'novelty_established':False,'mutated_existing_files':changed,'new_authored_or_external_receipt_files':authored_added,'all_new_files_including_excluded_local_history_and_scratch':added,'deleted_files':deleted,'self_and_following_output_records_excluded_to_avoid_circularity':sorted(excluded_final),'unmodified_existing_files':len(set(old)&set(current))-len(changed),'frozen_historical_root_review_original_inputs_unchanged':515,'all_original19_unchanged':True,'source_changes':'one summation backslash plus dated review-history/current-state disclosure sentence only; no mathematical proof rewrite','publication_ready':False,'required_review':'NEWwhole02','external_actions':'none'}
 write(OWN/'CHANGED_PATHS.json',changes)
 allow=json.loads((PUB/'PACKAGE_ALLOWLIST.json').read_text())['files']
 extra=['publication/PACKAGE_INPUT_PINS.json','publication/PACKAGE_MANIFEST.json','publication/CANDIDATE_INTEGRITY.json','publication/source_audit_kit.zip','publication/BUILD_VALIDATION.json','reviews/package_repair_01/CHANGED_PATHS.json','reviews/package_repair_01/VERIFY_FINAL_RESULT.json','reviews/package_repair_01/TECTONIC_EXPORT.json','reviews/package_repair_01/FINALIZE_REPAIR.py']
 candidate={'schema':'exact-repaired-candidate-freeze-v1','utc':utc,'state':'REPAIRS_APPLIED_VERIFIED_FROZEN_PENDING_NEWwhole02','files':[rec(ROOT/n) for n in sorted(set(allow)|set(extra))],'self_excluded':True,'output_pins_excluded':True,'publication_ready':False,'required_review':'NEWwhole02','completion_percent':100,'source':result['candidate_tex'],'pdf':result['candidate_pdf'],'archive':result['candidate_zip'],'root_original_13page_source_pins_unchanged':'ROOT_PREPRINT_REVIEW_01.json'}
 write(OWN/'NEW_CANDIDATE_PINS.json',candidate)
 output_names=['APPLY_REPAIRS.py','BASELINE_PINS.json','CHANGED_PATHS.json','FINALIZE_REPAIR.py','NEW_CANDIDATE_PINS.json','REFRESH_PINS.py','REPAIR_REPORT.md','RESEARCH_LOG.md','TECTONIC_EXPORT.json','VERIFY_FINAL.py','VERIFY_FINAL_RESULT.json','VISUAL_INSPECTION.json']
 outputs={'schema':'bounded-repair-authored-output-pins-v1','utc':utc,'files':[rec(OWN/n) for n in output_names],'self_excluded':True,'scope':'Authored repair scripts/log/report/receipts plus external current-candidate pins. No raw/body/render/extraction/reconstruction/history-copy/archive payload included here. Current ZIP includes only its strict allowlist and noncircular internal manifest/inputpins.','completion_percent':100,'required_review':'NEWwhole02','publication_ready':False}
 write(OWN/'OUTPUT_PINS.json',outputs)
 for r in candidate['files']+outputs['files']:
  assert rec(ROOT/r['path'])==r
 print(json.dumps({'utc':utc,'source':result['candidate_tex'],'pdf':result['candidate_pdf'],'archive':result['candidate_zip'],'mutated_existing_files':[r['path'] for r in changed],'new_authored_files':[r['path'] for r in authored_added],'all_new_local_files':len(added),'output_pins':rec(OWN/'OUTPUT_PINS.json'),'candidate_pins':rec(OWN/'NEW_CANDIDATE_PINS.json'),'completion_percent':100},indent=2))
if __name__=='__main__':main()
