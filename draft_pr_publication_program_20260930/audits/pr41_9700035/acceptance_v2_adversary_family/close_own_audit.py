#!/usr/bin/env python3
"""Own administrative closure only; no candidate import/compile/execution or Git writes."""
import datetime as dt
import hashlib
import io
import json
import math
import os
from pathlib import Path,PurePosixPath
import stat
import tokenize
P=Path(__file__).resolve().parent;R=P.parent.parents[2]
SHA=lambda b:hashlib.sha256(b).hexdigest()
def parse(raw):
    def pairs(values):
        out={}
        for k,v in values:assert k not in out;out[k]=v
        return out
    def floating(v):
        x=float(v);assert math.isfinite(x);return x
    return json.loads(raw,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
def ref(q,relative_to=P):
    b=q.read_bytes();return {'path':q.relative_to(relative_to).as_posix(),'bytes':len(b),'sha256':SHA(b)}
def put(name,obj):
    q=P/name;assert not q.exists();q.write_text(json.dumps(obj,indent=2)+'\n')
inspection=parse((P/'INPUT_INSPECTION_RESULT.json').read_bytes())
finite=parse((P/'FINITE_SPECIFICATION_RESULT.json').read_bytes())
assert inspection['status']=='PASS_FULL_BYTE_TYPED_READ_STATIC_BINDING_INSPECTION' and inspection['actual_pid']==26376
assert finite['status']=='PASS_OWN_MODELS_AND_ACTUAL_PRIVATE_FILESYSTEM_FIXTURES' and finite['actual_pid']==28812 and finite['checks_count']==93
assert all(z['status']=='PASS_OWN_MODEL_OR_FIXTURE' and z['observed_admission'] is z['expected_admission'] for z in finite['checks'])
external=[]
for z in inspection['files']+[finite['before_inventory_dated_observation']]:
    q=R/z['path'];assert q.is_file() and not q.is_symlink()
    assert all(not ancestor.is_symlink() for ancestor in q.parents)
    b=q.read_bytes();assert len(b)==z['bytes'] and SHA(b)==z['sha256'] and stat.S_IMODE(q.stat().st_mode)==z['worktree_mode']
    external.append({k:z[k] for k in ['path','bytes','sha256','worktree_mode']})
external=list({z['path']:z for z in external}.values());external.sort(key=lambda z:z['path'])
captures=[]
for folder,pid,exit_code,source in [('inspect_inputs_actual_capture',26015,1,'inspect_inputs.py'),('inspect_inputs_v2_actual_capture',26376,0,'inspect_inputs_v2.py'),('finite_specification_actual_capture',28812,0,'finite_specification.py')]:
    root=P/folder;cap=parse((root/'CAPTURE.json').read_bytes())
    assert type(cap['pid']) is int and cap['pid']==pid and type(cap['exit_code']) is int and cap['exit_code']==exit_code
    assert cap['actual_execution'] is True and cap['completed'] is True and cap['stdin_supplied'] is False and cap['candidate_execution'] is False
    assert cap['source_after_unchanged'] is True and SHA((root/'prelaunch_source.py').read_bytes())==SHA((P/source).read_bytes())==cap['source_sha256']
    assert cap['argv'][1]==str(P/source) and cap['cwd']==str(P)
    assert dt.datetime.fromisoformat(cap['started_utc'])<=dt.datetime.fromisoformat(cap['finished_utc'])
    assert {q.name for q in root.iterdir()}=={'CAPTURE.json','prelaunch_source.py','stdout.bin','stderr.bin'}
    for z in [cap['stdout'],cap['stderr']]:
        b=(root/z['path']).read_bytes();assert len(b)==z['bytes'] and SHA(b)==z['sha256']
    captures.append(ref(root/'CAPTURE.json',R))
now=dt.datetime.now(dt.timezone.utc).isoformat()
with (P/'RESEARCH_LOG.md').open('a') as f:f.write('\n## '+now+' — final semantic source verdict and own closure\n\nS1 full typed inventory/retained semantic clock derivation, S2 complete accepted/ROOT/reference schemas, and S3 literal stat.S_IMODE0444 every frozen member+self are addressed. No new mandatory mathematical or administrative correction found. Optional parent-directory fsync after sealer rename strengthens crash durability; not a source blocking defect. All1,299 inspected foreign rows plus dated inventory fixture were rechecked before closure. All93 independent models/private filesystem controls and their genuine captures are retained; own failed PID26015 remains exact. Review100%; acceptance execution0%; unconditional discovery0%; original2/5,new0,audit0. ROOT full report/control/source-delta and mechanical closure reading remains before actual runtime gates. No candidate execution, native/Git/remote mutation or contact.\n')
result={'schema':'pr41-new-independent-v2-acceptance-source-adversary/v1','verdict':'PASS_SOURCE_ONLY_V2_MANDATORY_ADMIN_REPAIRS_ADDRESSED','review_completed':True,'review_completion_estimate_percent':100,'reported_utc':now,'actual_administrative_closure_pid':os.getpid(),'reviewed_preparation_manifest_sha256':inspection['reviewed_preparation_manifest_sha256'],'mandatory_corrections':[],'mandatory_mathematical_repairs_found':[],'mandatory_administrative_source_repairs_found':[],'prior_mandatory_repairs_addressed':['S1','S2','S3'],'optional_hardening':['Parent-directory fsync after absent-only final directory rename strengthens crash namespace durability.'],'source_preparation_members':32,'unique_full_files_read':inspection['unique_full_files'],'full_bytes_read':inspection['full_bytes_read'],'typed_nodes_seen':inspection['typed_nodes_seen'],'independent_controls':93,'complete_canonical_receipt_fixture_fields':55,'actual_special_file_modes_tested':True,'current_members':547,'dependency_members':469,'whole_authored_members':143,'whole_foreign_members':17,'whole_manifest_sha256':'233867cfb7e18b910f1ec17c9a57a386eadd1793ff3a44328260e204d8304130','actual_root_whole_inspection_sha256':'28addc78a418ac5ad72a1e7f8cfacda16ec52ba5db52132b16c92602a3f4965e','original_packet_unchanged_after_audit':True,'full_problem_solved':False,'novelty_claimed':False,'human_peer_review_asserted':False,'literal_target_status':'UNSOLVED','mathematical_scope_recertified':False,'strongest_preserved':'Unconditional interior expected union law/full lower bound; full law only with additional t^4 P(D>t)->0.','exact_remaining_gap':'Expected exterior prescribed all-pair union length o(k) under ordinary SIRSN axioms, or admissible full-SIRSN counterexample.','original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'candidate_helpers_imported_compiled_or_executed':False,'scientific_helpers_reexecuted':False,'actual_PR40_predecessor_records_observed':True,'future_approved_predecessor_pins_status':'NOT_CERTIFIED','future_external_ROOT_bindings_plan_final_capture_status':'NOT_CERTIFIED','future_fresh13_native_runtime_status':'NOT_CERTIFIED','future_actual_runtime_PASS_claimed':False,'future_acceptance_execution_estimate_percent':0,'unconditional_discovery_estimate_percent':0,'shared_native_canonical_Git_index_remote_branch_writes':False,'external_human_contact':False,'paper_or_new_DOI_or_tracker':False,'lossless_oversized_prior_log_recovery_verified':True,'own_failed_captured_runs':[captures[0]],'own_successful_input_inspection_capture':captures[1],'own_successful_finite_controls_capture':captures[2],'full_input_inspection':ref(P/'INPUT_INSPECTION_RESULT.json',R),'finite_controls_result':ref(P/'FINITE_SPECIFICATION_RESULT.json',R),'report':ref(P/'REPORT.md',R),'next_required':'ROOT full report/result/controls/source-delta and exact closure read before genuine approved external runtime inputs and actual reconciliation/integration/mirror/post outcomes.'}
put('RESULT.json',result)
(P/'README.md').write_text('# Independent PR41 V2 acceptance source adversary\n\nRead REPORT.md and RESULT.json. S1/S2/S3 are addressed with no new mandatory source correction. The source-only verdict does not certify future execution. INPUT_INSPECTION_RESULT.json records complete byte/hash/typed traversal; FINITE_SPECIFICATION_RESULT.json records93 independent private specification/actual filesystem checks. Initial failed inspector capture is preserved beside a new corrected source/capture. FIRST_PARTY_MANIFEST.json closes exact owned files and directories, explicitly including one intentional empty negative fixture, and lists all external bindings individually. All owned files+self are frozen0444. No candidate import/compilation/execution, native/Git/remote mutation, paper/DOI/tracker or human contact. Original2/5,new0,audit0; source review100%, execution0%, unconditional discovery0%.\n')
manifest=P/'FIRST_PARTY_MANIFEST.json';assert not manifest.exists()
members=[];dirs=[]
for q in sorted(P.rglob('*')):
    assert not q.is_symlink()
    if q.is_dir():dirs.append(q.relative_to(P).as_posix());continue
    assert q.is_file();raw=q.read_bytes();assert len(raw)<100*1024*1024
    if q.suffix=='.json':parse(raw)
    elif q.suffix=='.py':list(tokenize.tokenize(io.BytesIO(raw).readline))
    members.append(ref(q))
intentional=['private_actual_bundle_fixture/intentional_empty_extra_directory']
parents={a.as_posix() for z in members for a in PurePosixPath(z['path']).parents if a.as_posix()!='.'}
assert set(dirs)==parents|set(intentional)
for z in members:(P/z['path']).chmod(0o444)
packet={'schema':'pr41-independent-v2-source-adversary-strict-owned-closure/v1','status':'CLOSED_INDEPENDENT_SOURCE_ONLY_V2_ADVERSARY','closed_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_administrative_closure_pid':os.getpid(),'self_excluded':['FIRST_PARTY_MANIFEST.json'],'files_count':len(members),'files':members,'exact_directories':dirs,'intentional_empty_directories':intentional,'all_owned_member_and_self_permissions':'0444_STAT_S_IMODE','individual_external_foreign_dependencies_excluded_from_authored_copy':external,'foreign_prefix_exclusions':[],'reviewed_preparation_manifest_sha256':inspection['reviewed_preparation_manifest_sha256'],'report_sha256':SHA((P/'REPORT.md').read_bytes()),'result_sha256':SHA((P/'RESULT.json').read_bytes()),'mandatory_corrections':[],'verdict':result['verdict'],'candidate_helpers_imported_compiled_or_executed':False,'future_actual_runtime_PASS_claimed':False,'native_Git_remote_mutations':False,'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,'novelty_claimed':False,'paper_or_new_DOI_or_tracker':False,'review_completion_estimate_percent':100,'actual_acceptance_execution_estimate_percent':0,'unconditional_discovery_estimate_percent':0}
with manifest.open('xb') as s:s.write((json.dumps(packet,indent=2)+'\n').encode());s.flush();os.fsync(s.fileno())
manifest.chmod(0o444)
for z in members:
    q=P/z['path'];b=q.read_bytes();assert len(b)==z['bytes'] and SHA(b)==z['sha256'] and stat.S_IMODE(q.stat().st_mode)==0o444
assert stat.S_IMODE(manifest.stat().st_mode)==0o444
print(json.dumps({'status':packet['status'],'actual_administrative_closure_pid':os.getpid(),'manifest':ref(manifest,R),'report':ref(P/'REPORT.md',R),'result':ref(P/'RESULT.json',R),'owned_members':len(members),'external_individual_bindings':len(external),'largest_authored_file_bytes':max(z['bytes'] for z in members),'mandatory_corrections':[],'candidate_helpers_imported_compiled_or_executed':False},indent=2))
