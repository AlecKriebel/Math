"""Own final source-only closure control; parent captures completion then closes all files."""
from pathlib import Path,PurePosixPath
import json,hashlib,datetime,os,stat
H=Path(__file__).resolve().parent;stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
started=stamp();inputs=[]
def require(ok,msg):
    if not ok:raise ValueError(msg)
for p in sorted(H.rglob('*')):
    require(not p.is_symlink() and (p.is_file() or p.is_dir()),'Regular owned closure nodes')
    if p.is_file():
        raw=p.read_bytes();inputs.append({'path':p.relative_to(H).as_posix(),'bytes':len(raw),'sha256':sha(raw),'observed_preclosure_worktree_mode':stat.S_IMODE(p.stat().st_mode)})
require(not (H/'PREPARATION_MANIFEST.json').exists(),'Absent family closure required')
controls=json.loads((H/'OWN_CONTROL_RESULTS.json').read_bytes())
require(controls['status']=='PASS' and controls['production_sources_executed'] is False and controls['production_sources_imported'] is False and controls['production_bytecode_compiled'] is False,'Independent own controls, no production source execution')
require(controls['permission_modes_tested']==4096 and len(controls['actual_private_permission_observations'])==6,'Real complete mode controls')
for name in ['AUTHORING_ACTUAL_CAPTURE','SOURCE_READING_ACTUAL_CAPTURE','CORRECTED_REVISION_ACTUAL_CAPTURE','STRENGTHENING_ACTUAL_CAPTURE','FINAL_DRAFT_CORRECTION_ACTUAL_CAPTURE','CONTROLS_ACTUAL_CAPTURE']:
    cap=json.loads((H/name/'CAPTURE.json').read_bytes());require(cap['actual_execution'] is True and cap['completed'] is True and cap['exit_code']==0 and type(cap['pid']) is int,'Actual completed own source/control child')
    for key in ['stdout','stderr']:
        z=cap[key];raw=(H/name/z['path']).read_bytes();require(len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Complete actual captured stream')
failure=json.loads((H/'REVISION_ACTUAL_CAPTURE/CAPTURE.json').read_bytes());require(failure['exit_code']==1 and failure['status']=='FAIL','Full actual drafting failure retained')
status=json.loads((H/'SOURCE_STATUS.json').read_bytes());status['source_preparation_complete']=True
status.update(own_AST_only_syntax_checked_no_production_bytecode=True,own_control_demands=controls['demands'],actual_private_mode_observations_historical_before_closure=True,closed_source_all_files_literal0444=True,closure_parent_records_after_complete_capture=True)
(H/'SOURCE_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
note='\n## '+stamp()+' — Source package complete, independent final audit remains\n\nPreparation100%; new discovery0%; original0/5,new0,audit0. Own source read7392,\ninitial author14323, corrected drafting16682, strengthening18756, final literal\ncorrection19539, and independent controls21562 are genuine actual captured\nchildren. Initial authoring did not certify syntax: later source reading found\na copied predecessor-count drafting error and interpreted newline escapes.\nFirst own repair15928 failed on an already-corrected message token, after only\nthe guard edit; full prelaunch/streams/partial bodies remain. Corrected sources\nare distinct current administrative drafts. No proposed source was imported,\ncompiled to bytecode or executed; AST syntax trees and own controls ran only.\nExactly4096 permission predicates and6 real files were checked. The private\nmode probes recorded their actual special permission bits before final\nclosure; the source family subsequently freezes every owned member to0444.\nThe simulated future inventory fixture is explicitly private and attests no\nactual PR42 predecessor. Its three required genuine future refs remainNULL.\nA new different adversary must review this exact closed source family before\nROOT authorizes actual final reconciliation. No old42PASS is transferred.\n'
with (H/'RESEARCH_LOG.md').open('a') as f:f.write(note)
record={'schema':'pr43-own-final-source-closure-control/v1','actual_child_pid':os.getpid(),'started_utc':started,'finished_utc':stamp(),'status':'PASS_SOURCE_ONLY_READY_FOR_PARENT_CLOSURE','read_members_before_closure':inputs,'private_source_controls_demands':controls['demands'],'production_helpers_imported_compiled_executed':False,'SOURCE_preparation_complete':True,'ROOT_approval_authored':False,'future_PR42_predecessor_certified':False,'source_preparation_completion_percent':100,'new_discovery_percent':0,'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0}
(H/'CLOSURE_CONTROL_RESULT.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='read_members_before_closure'}))
