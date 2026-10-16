#!/usr/bin/env python3
"""Own final review metadata authoring, never candidate execution."""
import datetime as dt
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=Path('/Users/alec/Documents/Math')
AUDIT=HERE.parent
REV=AUDIT/'acceptance_execution_preparation_family/integration_source_revision_v2'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def pin(path):
    raw=path.read_bytes()
    return {'path':str(path.relative_to(ROOT)),'bytes':len(raw),'sha256':sha(raw)}
def load(path): return json.loads(path.read_bytes())
def new(path,obj):
    with path.open('x') as f: f.write(json.dumps(obj,sort_keys=True,indent=2)+'\n')
now=dt.datetime.now(dt.timezone.utc).isoformat()
inspection=load(HERE/'inspect_inputs_actual_capture/stdout.bin')
wrapper=load(HERE/'inspect_wrapper_v2_actual_capture/stdout.bin')
union={}
for item in inspection['input_members']+wrapper['input_members']:
    row={k:item[k] for k in ['path','bytes','sha256']}
    assert item['path'] not in union or union[item['path']]==row
    raw=(ROOT/item['path']).read_bytes()
    assert len(raw)==item['bytes'] and sha(raw)==item['sha256']
    union[item['path']]=row
for f in REV.iterdir(): assert f.is_file() and not f.is_symlink() and f.stat().st_mode & 0o777==0o444
captures=[HERE/(n+'_actual_capture') for n in ['inspect_inputs','predicate_controls','inspect_wrapper','inspect_wrapper_v2']]
for capture in captures:
    receipt=load(capture/'CAPTURE.json')
    assert receipt['actual_execution'] is True and receipt['completed'] is True
    assert type(receipt['pid']) is int and receipt['pid']>0 and type(receipt['exit_code']) is int
    assert dt.datetime.fromisoformat(receipt['started_utc'])<=dt.datetime.fromisoformat(receipt['finished_utc'])
    assert {p.name for p in capture.iterdir()}=={'CAPTURE.json','prelaunch_source.py','stdout.bin','stderr.bin'}
    assert sha((capture/'prelaunch_source.py').read_bytes())==receipt['source_sha256']
    for key in ['stdout','stderr']:
        row=receipt[key]; raw=(capture/row['path']).read_bytes()
        assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
    assert receipt['exit_code']==(1 if capture.name=='inspect_wrapper_actual_capture' else 0)
new(HERE/'FOREIGN_INPUT_INVENTORIES.json',{'schema':'pr40-v2-adversary-separately-bound-foreign-inventories/v1','utc':now,'foreign_files_are_not_owned_family_members':True,'new_primary_PDF_reading_claimed':False,'inventories':inspection['foreign_inventories_individually_bound']})
new(HERE/'READ_COVERAGE.json',{
    'schema':'pr40-v2-wrapper-source-only-read-coverage/v1','utc':now,
    'entire_v2_17_authored_plus_literal_self_read':True,
    'entire_five_v2_helpers_read':True,'helper_line_count':696,
    'entire_wrapper_475_lines_read':True,'entire_wrapper11_plus_self_packet_read':True,
    'entire_contract_scope_draft_input_revision_predecessor_cache_records_and_patch_read':True,
    'complete_native_driver500_lines_read_as_source':True,
    'inherited_whole_report_assessment_manifest_and_root_science_records_read':True,
    'complete_original_SOURCE_STATUS_current_overview_scope_and_proof_geometry_qualifications_read':True,
    'v2_source_members':[pin(f) for f in sorted(REV.iterdir())],
    'wrapper_source':pin(AUDIT/'execute_root_acceptance_revised.py'),
    'wrapper_manifest':pin(AUDIT/'root_runner_preparation_family/MANIFEST.json'),
    'full_own_input_inspection_result':pin(HERE/'inspect_inputs_actual_capture/stdout.bin'),
    'full_own_wrapper_inspection_result':pin(HERE/'inspect_wrapper_v2_actual_capture/stdout.bin'),
    'new_full_primary_PDF_reading_claimed':False,
    'mathematical_recertification_claimed':False,
    'fully_unexposed_source_first_independence_claimed':False,
    'inherited_exposure_qualification':'Whole review disclosed initial raw-background exposure; ROOT operative reading occurred after earlier interpretation exposure. Optional Han–Yang operative reading belongs to the primary family, not this reviewer or direct ROOT reading.',
    'previous_static_review_missed_S7':True,
    'reviewed_helper_wrapper_or_native_driver_import_compile_execution':False,
    'unique_combined_bound_input_members':len(union),'unique_combined_bound_input_bytes':sum(r['bytes'] for r in union.values()),
    'complete_combined_bound_input_inventory':[union[n] for n in sorted(union)]
})
old=(HERE/'REPORT.md').read_text()
old=old.replace('# PR40 v2 publication adversary — wrapper review pending','# PR40 v2 publication adversary — qualified source-only pass',1)
old=old.replace("The complete v2 helper packet passed this family's source-only review and independent local controls. The closed root wrapper and preparation are still awaited. This report is an interim finding, not a final family disposition or an actual reconciliation, acceptance, merge, native mirror or post result.","The exact closed v2 helper packet and closed root wrapper preparation pass this family's qualified source-only review. No mandatory candidate defect remains from this review. This disposition does not claim an actual reconciliation, preflight, merge, acceptance, native mirror or post result.",1)
tail='Independent review estimate80%; discovery0%; original0/5,new0,audit0. Mandatory candidate defects found so far: none. The closed wrapper must still be fully read and bound before final disposition and seal.'
assert tail in old
extra='''The complete closed root preparation11+self was read and independently checked at MANIFEST SHA256 aa58d2e3a9f470c6ce8d2781e47c72605de8338ee6766bb390a7f57ab7f42d50, all twelve files0444. The standalone wrapper is475 lines/27934 bytes/mode0644, SHA256 f00d8be3926b02d10f46a351802688a87f107d406c842317f51a5674248d4215; its archival copy is exact. The wrapper pins all17 v2 members and five actual sources before/after, preserves all13 native modes and actual HEAD within each child, and admits only queue overlay, inventory finalize, state/history mirror byte changes. The complete root review artifacts are pinned before/after. Final requires the mandatory --output and independently inspects the full final two-member manifest, receipt, complete scope, stdout hashes and real UTC containment. Every nonfinal child receives exactly13 strings for preparation plus six path/SHA pairs, with a phase only for integration; overlay adds only its full automatic-queue pin. PR39-only helper flags are absent. Real Popen/PID/full binary stdout/stderr, timeout/launch/error handling, exact final4/nonfinal5 files and reserved final output names were reviewed. No false/null template is accepted as approval, no failed/unfinished/timed-out/native-changing/errorful capture can PASS, and actual outer exit0 remains required after directory publication.

The corrected wrapper inspector actually exited0 with PID78066 and checked374 wrapper-related inputs,122 recorded local interface/status/phase-scope cases and3 actual macOS directory publication experiments. The absent destination published the full directory; both an empty and a populated intervening destination produced actual EEXIST17 while retaining the complete stage and existing target. An empty intervening directory is intentionally retained and listed explicitly in the final exact directory inventory. These are own private filesystem experiments, not execution of the reviewed wrapper. The directory-publication primitive is compatible with the current macOS host; the wrapper deliberately refuses other platforms.

The initial wrapper inspector genuinely exited1 with PID77706 because its own checker incorrectly required historical closure roots to contain no directories. Its full prelaunch source, empty stdout and complete traceback remain under inspect_wrapper_actual_capture, and the original independently authored inspector is retained. Corrected source is inspect_wrapper_v2.py; exact historical directories now derive from member parent paths. This own harness failure did not execute a candidate helper, did not reach the directory-publication experiments and is not attributed as a submission defect. Earlier own input/predicate captures remain exact. A separately captured first-party metadata writer records the final review without executing candidate code.

The source preparation's recorded PR39 mirror SHA remains null archival template metadata. ROOT has supplied a separately observed actual PR39 mirror SHA; this review makes no independent PR39 post/checkpoint or fresh40 runtime observation. Actual root fresh-main records, approved final plans, complete gate arguments and all actual PR40 stages remain to be created/run by ROOT under their explicit full-byte pins. The qualified static disposition is not future approval or a fabricated PASS.

Independent review completion100%; discovery0%; original0/5,new0,audit0. Mandatory candidate defects: none. The remaining gap is genuine ROOT full review and actual administrative execution with fresh postPR39 native evidence, exact original-head merge, mirror and post checks.
'''
(HERE/'REPORT.md').write_text(old.replace(tail,extra))
with (HERE/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n## '+now+' — Complete wrapper review and final metadata checkpoint\n\nEntire closed wrapper475/11+self reviewed and bound. Own initial inspector PID77706 exit1 retained: incorrect directory-free assumption for historical closures. Corrected inspector PID78066 exit0 checked374 inputs and122 recorded interface/status/phase scope cases; all3 macOS RENAME_EXCL experiments passed, including empty/populated intervening-target preservation. Reviewed candidate code never imported/compiled/executed. No mandatory candidate defect found. Final source-only disposition qualified PASS; actual ROOT gates/merge/mirror/post pending. Independent review100%; discovery0%; original0/5,new0,audit0.\n')
new(HERE/'ASSESSMENT.json',{
    'schema':'pr40-v2-helper-and-wrapper-independent-source-assessment/v1','utc':now,
    'status':'PASS_QUALIFIED_SOURCE_ONLY','mandatory_candidate_defects':[],
    'v2_manifest':pin(REV/'PREPARATION_MANIFEST.json'),'v2_members_excluding_self':17,
    'wrapper_manifest':pin(AUDIT/'root_runner_preparation_family/MANIFEST.json'),'wrapper_members_excluding_self':11,
    'wrapper_source':pin(AUDIT/'execute_root_acceptance_revised.py'),
    'S1_through_S7_source_repairs_survive_review':True,
    'strict_cache3_absent_Git_full_worktree_tracked10_9_queue_separate':True,
    'entire_predecessor15_static31_qualification6_closures_preserved':True,
    'all_original13_current239_dependencies216_preserved':True,
    'foreign_inventories_separately_bound':pin(HERE/'FOREIGN_INPUT_INVENTORIES.json'),
    'full_read_coverage':pin(HERE/'READ_COVERAGE.json'),'report':pin(HERE/'REPORT.md'),
    'own_control_capture_receipts':[pin(p/'CAPTURE.json') for p in captures],
    'own_predicate_controls':56,'own_recorded_wrapper_contract_scope_cases':122,
    'actual_private_publication_controls':5,
    'own_initial_wrapper_inspector_failure_retained':True,
    'own_initial_failure_is_candidate_or_substantive_failure':False,
    'actual_PR40_future_final_gate_merge_mirror_post_claimed':False,
    'reviewed_helper_wrapper_native_driver_import_compile_execution':False,
    'Git_native_canonical_shared_index_remote_mutations':False,'outside_communication':False,
    'mathematical_recertification_claimed':False,'new_full_primary_PDF_reading_claimed':False,
    'previous_qualified_static_review_missed_S7':True,
    'inherited_primary_reading_exposure_and_standard_inputs_qualified':True,
    'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,
    'original_substantive_attempts':0,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,
    'full_problem_solved':False,'partial_valid':True,'source_hold':True,'novelty_claimed':False,
    'paper_or_new_DOI_or_tracker':False,'source_review_completion_estimate_percent':100,
    'scientific_discovery_completion_estimate_percent':0,
    'root_followup':'Read complete new report/assessment/read coverage/captures/results/final manifest, then genuinely execute only after actual PR39 post/checkpoint and fresh reviewed13/main evidence. No future approval or PASS is provided by this family.'
})
print(json.dumps({'status':'OWN_FINAL_SOURCE_REVIEW_METADATA_WRITTEN','utc':now,'unique_combined_bound_input_members':len(union),'unique_combined_bound_input_bytes':sum(r['bytes'] for r in union.values()),'files':[pin(HERE/n) for n in ['FOREIGN_INPUT_INVENTORIES.json','READ_COVERAGE.json','REPORT.md','RESEARCH_LOG.md','ASSESSMENT.json']],'candidate_execution':False,'actual_future_gate_claimed':False},sort_keys=True))
