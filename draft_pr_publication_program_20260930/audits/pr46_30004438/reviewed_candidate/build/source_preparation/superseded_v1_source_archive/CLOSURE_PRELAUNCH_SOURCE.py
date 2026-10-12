"""Close only this SOURCE folder; ROOT captures this own child outside the folder."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, os, stat
F=Path(__file__).absolute().parent; A=F.parent
def sha(raw): return hashlib.sha256(raw).hexdigest()
def regular(path):
    assert not path.is_symlink() and all(not p.is_symlink() for p in path.parents) and stat.S_ISREG(path.stat().st_mode)
    return path.read_bytes()
def clock(value):
    result=dt.datetime.fromisoformat(value); assert result.tzinfo is not None and result.utcoffset()==dt.timedelta(0)
    return result
def dump(value): return (json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
def capture(name,source,current,expected):
    directory=F/name; obj=json.loads(regular(directory/'CAPTURE.json'))
    assert {p.name for p in directory.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'}
    assert obj['actual_execution'] is True and obj['completed'] is True and type(obj['pid']) is int and obj['pid']>0
    assert type(obj['exit_code']) is int and obj['exit_code']==expected and obj['stdin_supplied'] is False
    assert obj['production_builder_or_ROOT_operator_executed'] is False and obj['source_unchanged'] is True and obj['operator_unchanged'] is True
    assert clock(obj['started_utc'])<=clock(obj['finished_utc'])<=dt.datetime.now(dt.timezone.utc)
    assert obj['argv']==['/usr/bin/python3','-B',str(F/source)] and obj['cwd']==str(A.parents[2])
    assert sha(regular(directory/'PRELAUNCH_SOURCE.py'))==obj['source_sha256']
    assert sha(regular(directory/'PRELAUNCH_OPERATOR.py'))==obj['operator_sha256']==sha(regular(F/'capture_preparation_operation.py'))
    if current: assert regular(directory/'PRELAUNCH_SOURCE.py')==regular(F/source)
    pre=json.loads(regular(directory/'PRELAUNCH.json'))
    for key in pre: assert obj[key]==pre[key] if key!='schema' else pre[key]=='PR46_SOURCE_PREPARATION_PRELAUNCH_v1'
    for channel in ['stdout','stderr']:
        raw=regular(directory/obj[channel]['path']); assert len(raw)==obj[channel]['bytes'] and sha(raw)==obj[channel]['sha256']
    assert (not regular(directory/'stderr.bin')) if expected==0 else bool(regular(directory/'stderr.bin'))
    return {'directory':name,'entire_actual_capture':obj,'current_source_matches_prelaunch':current,'expected_exit':expected}
def main():
    assert not (F/'PREPARATION_MANIFEST.json').exists()
    source=regular(Path(__file__).absolute())
    captures=[capture(*row) for row in [
      ('AUTHORING_ACTUAL_CAPTURE','author_source_documents.py',True,0),
      ('SOURCE_INPUT_INSPECTION_ACTUAL_CAPTURE','inspect_source_inputs.py',False,1),
      ('SOURCE_INPUT_INSPECTION_REPAIRED_ACTUAL_CAPTURE','inspect_source_inputs.py',True,0),
      ('PRIVATE_CONTROLS_ACTUAL_CAPTURE','private_contract_controls.py',False,1),
      ('PRIVATE_CONTROLS_REPAIRED_ACTUAL_CAPTURE','private_contract_controls.py',True,0)]]
    status=json.loads(regular(F/'SOURCE_STATUS.json'))
    assert status['builder_executed'] is False and status['ROOT_operator_executed'] is False and status['ROOT_approval'] is None
    assert status['production_import_compile_or_execution'] is False and status['actual_current_freeze'] is False
    controls=json.loads(regular(F/'PRIVATE_CONTRACT_CONTROL_RESULTS.json'))
    assert type(controls['independent_predicate_assertions']) is int and controls['independent_predicate_assertions']>4400
    assert controls['all4096_full_modes_enumerated'] is True and controls['production_import_compile_or_execution'] is False
    inspection=json.loads(regular(F/'SOURCE_INPUT_INSPECTION.json'))
    assert inspection['original_scoped318_plus_self_unchanged'] is True and inspection['production_import_compile_or_execution'] is False
    assert inspection['complete_fixed_reads_count']==len(inspection['complete_fixed_member_reads'])
    for row in inspection['complete_fixed_member_reads']:
        raw=regular(A/row['path']); assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
    for name in ['DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json']:
        obj=json.loads(regular(F/name)); assert obj['reading_completed'] is False and all(v is False for v in obj['root_flags'].values())
        assert obj['created_utc'] is None and obj['preparation_manifest_sha256'] is None
    for name in ['DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json']:
        obj=json.loads(regular(F/name)); assert obj['approved_by_root'] is False and obj['created_utc'] is None
    assert 'ROOT_SCOPE_ACCEPTED_EXACT_KNOWN_RESULT_ONLY' not in regular(F/'DRAFT_ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md').decode()
    assert not (A/'reviewed_candidate').exists() and not (A/'reviewed_candidate').is_symlink()
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    with (F/'CLOSURE_PRELAUNCH_SOURCE.py').open('xb') as out: out.write(source); out.flush(); os.fsync(out.fileno())
    with (F/'SOURCE_PREPARATION_RESEARCH_LOG.md').open('a') as out:
        out.write('\n'+now+' — Actual self-only SOURCE closure childPID'+str(os.getpid())+'. Source preparation100%; actual current freeze0%; new-discovery credit0%.\n')
        out.write('Three successful own authoring/inspection/private-control operations and two initial failed own checks are preserved with genuine prelaunch code, operator, PID, aware UTC, complete streams and postexit captures. Fixed-inspection initial failure required distinguishing mutable audit-root note/raw modes from immutable closed copies; repaired source preserves observed external mode policy. Private controls initial failure was a case-sensitive source-marker typo; repaired source passes. All'+str(inspection['complete_fixed_reads_count'])+' fixed byte reads remain exact. Independent private controls'+str(controls['independent_predicate_assertions'])+' assertions include all4096 modes and actual private chmod/exclusive-rename/symlink operations, not production runtime verification. Production builder/operator never imported, compiled or executed; all ROOT approval drafts false/null. Original318+self scoped ownership, algebra34+self plus separatefive, complex33+self and actualROOT37+self remain exact. Future genuine ROOT prerequisites, new different SOURCE adversary, actual freeze, new whole-current review and final acceptance remain pending. No native/canonical/index/branch/remote/commit/push or external communication action.\n')
        out.flush(); os.fsync(out.fileno())
    paths=sorted(p for p in F.rglob('*') if not p.is_dir())
    names={p.relative_to(F).as_posix() for p in paths}; dirs={p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_dir()}
    expected={q.as_posix() for n in names for q in PurePosixPath(n).parents if str(q)!='.'}
    assert dirs==expected and all(not p.is_symlink() for p in F.rglob('*'))
    rows=[]
    for path in paths:
        raw=regular(path); path.chmod(0o444); assert stat.S_IMODE(path.stat().st_mode)==0o444
        rows.append({'path':path.relative_to(F).as_posix(),'bytes':len(raw),'sha256':sha(raw)})
    result={'schema':'PR46_CURRENT_SOURCE_ONLY_CLOSURE_v1','status':'CLOSED_SOURCE_ONLY_CURRENT_PREPARATION',
      'utc':now,'actual_closure_pid':os.getpid(),'self_excluded':['PREPARATION_MANIFEST.json'],'files_count':len(rows),
      'files':rows,'directories':sorted(dirs),'all_full_mode0444':True,
      'original_preparation_manifest_sha256':'da37655e9b3bab420862a0c17c761e67fa9a4bc2028a328d033547249c54ad2e',
      'original_scientific_files':13,'original_preparation_scoped_members':318,
      'production_builder_sha256':sha(regular(F/'prepare_current_packet.py')),
      'production_operator_sha256':sha(regular(F/'capture_root_builder_operation.py')),
      'production_import_compile_or_execution':False,'ROOT_reading_or_approval':None,
      'actual_current_freeze_or_new_whole_current_verdict':None,'original_substantive_attempts':0,
      'original_source_verification_responses':1,'new_substantive_attempts':0,'audit_turns':0,
      'complete_own_prior_actual_captures':captures,'source_preparation_completion_estimate_percent':100,
      'actual_current_freeze_completion_estimate_percent':0,'new_discovery_credit_percent':0,
      'separate_actual_source_closure_capture':'current_preparation_closure_actual_capture/CAPTURE.json',
      'separate_outer_capture_completed_only_after_this_child_exit':True,
      'dated_special_mode_fixtures_frozen0444_after_controls':True,'foreign_bodies_copied_into_this_family':False,
      'new_SOURCE_adversary_personal_ROOT_read_required_before_builder':True,
      'new_whole_current_SOURCE_first_adversary_and_final_ROOT_reconciliation_pending':True}
    with (F/'PREPARATION_MANIFEST.json').open('xb') as out: out.write(dump(result)); out.flush(); os.fsync(out.fileno())
    (F/'PREPARATION_MANIFEST.json').chmod(0o444)
    for row in rows:
        path=F/row['path']; raw=regular(path)
        assert len(raw)==row['bytes'] and sha(raw)==row['sha256'] and stat.S_IMODE(path.stat().st_mode)==0o444
    assert regular(Path(__file__).absolute())==source
    print(json.dumps({'status':result['status'],'files_count':len(rows),'manifest_sha256':sha(regular(F/'PREPARATION_MANIFEST.json')),
      'builder_sha256':result['production_builder_sha256'],'operator_sha256':result['production_operator_sha256'],
      'ROOT_approval':None,'production_executed':False,'actual_current_freeze':False},sort_keys=True))
if __name__=='__main__': main()
