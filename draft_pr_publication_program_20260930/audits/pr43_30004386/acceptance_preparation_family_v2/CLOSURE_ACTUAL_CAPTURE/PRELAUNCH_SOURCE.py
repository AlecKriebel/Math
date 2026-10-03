"""Own final source-only checks; parent records capture before exact V2 closure."""
from pathlib import Path
import json,hashlib,datetime,os,stat
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
controls=json.loads((H/'OWN_CONTROL_RESULTS.json').read_bytes());require(controls['status']=='PASS_SOURCE_ONLY_CORRELATIONS_AND_FULL_DELTA' and controls['five_production_delta_exactly_two_tokens'] is True and controls['all_original108_plus_self_unchanged'] is True,'Genuine independent narrow repair controls')
require(controls['production_helpers_imported_compiled_executed'] is False and len(controls['negative_correlations'])==6 and controls['permission_modes_checked']==4096,'Source-only controls with known complete scope')
for name in ['AUTHORING_ACTUAL_CAPTURE','CONTROLS_ACTUAL_CAPTURE']:
    cap=json.loads((H/name/'CAPTURE.json').read_bytes());require(type(cap['pid']) is int and cap['actual_execution'] is True and cap['completed'] is True and cap['exit_code']==0 and cap['source_unchanged'] is True,'Actual completed own V2 child')
    for channel in ['stdout','stderr']:
        z=cap[channel];raw=(H/name/z['path']).read_bytes();require(len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Complete actual own stream')
refs=json.loads((H/'V1_SOURCE_REFERENCES.json').read_bytes())
for z in refs['files']:
    p=R/z['path'];raw=p.read_bytes();require(len(raw)==z['bytes'] and sha(raw)==z['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444,'Every complete old V1 body still unchanged')
require(not (H/'PREPARATION_MANIFEST.json').exists(),'Absent own new closure')
status=json.loads((H/'SOURCE_STATUS.json').read_bytes());status.update(source_preparation_complete=True,own_control_demands=controls['checks'],closed_source_all_files_literal0444=True,closure_parent_records_after_complete_capture=True)
require(status['ROOT_source_approval_authored'] is False and status['future_acceptance_performed'] is False and status['independent_acceptance_source_verdict'] is None,'No future ROOT/new independent gate promoted')
(H/'SOURCE_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
note='\n## '+datetime.datetime.now(datetime.timezone.utc).isoformat()+' — Own V2 controls complete; new independent gate remains\n\nPreparation100%; newdiscovery0%; original0/5,new0,audit0. Own actual author\n32531 and independent control35483 completed successfully. The old nonexistent\nfilename and old guard/writer scope mismatch were detected directly from their\nsource operands, without executing helpers. Exactly two production token\nchanges are verified; every other production/science/draft byte remains exact.\nSix deliberate correlation mutants reject. All109 originalV1 source members\nremain independently full-byte and full-mode bound, including all old failures.\nOwn actual six permission probes record preclosure modes; the final family\nsubsequently freezes all owned files to0444. V1 finite successful checks did not\ncatch the runtime correlations and are not transferred as a V2 review PASS.\nSource-only initial metadata inherited some V1 own-check/closure descriptions;\nthe V2 controls cleared them until real V2 checks/closure. No ROOT approval or\nactualPR42 handoff is inferred. A new different independent adversary and ROOT\npersonal reading are required before actual final reconciliation.\n'
with (H/'RESEARCH_LOG.md').open('a') as f:f.write(note)
obj={'schema':'pr43-V2-own-source-closure-control/v1','actual_child_pid':os.getpid(),'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_SOURCE_ONLY_READY_FOR_CAPTURE_THEN_CLOSURE','own_control_checks':controls['checks'],'production_delta_exactly_two_tokens':True,'all_V1_108_plus_self_preserved':True,'production_imports_compilation_execution':False,'future_ROOT_or_acceptance_certified':False,'new_independent_source_audit_complete':False,'future_actual_PR42_predecessor_certified':False,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0}
(H/'CLOSURE_CONTROL_RESULT.json').write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps(obj))
