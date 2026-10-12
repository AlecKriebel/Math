"""Close source-only preparation; no proposed production or mathematical helper execution."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, os, stat
F=Path(__file__).resolve().parent; A=F.parent
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(o): return (json.dumps(o,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
def verify_capture(name,child):
    d=F/name; c=json.loads((d/'CAPTURE.json').read_bytes())
    assert {p.name for p in d.iterdir()}=={'CAPTURE.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'}
    assert c['actual_execution'] is True and c['completed'] is True and c['exit_code']==0 and type(c['pid']) is int and c['pid']>0
    assert c['production_builder_or_ROOT_operator_executed'] is False and c['source_unchanged'] is True and c['operator_unchanged'] is True
    assert dt.datetime.fromisoformat(c['started_utc'])<dt.datetime.fromisoformat(c['finished_utc'])
    assert (d/'PRELAUNCH_SOURCE.py').read_bytes()==(F/child).read_bytes() and sha((F/child).read_bytes())==c['source_sha256']
    assert (d/'PRELAUNCH_OPERATOR.py').read_bytes()==(F/'capture_preparation_operation.py').read_bytes()
    assert sha((d/'PRELAUNCH_OPERATOR.py').read_bytes())==c['operator_sha256']
    for channel in ['stdout','stderr']:
        b=(d/c[channel]['path']).read_bytes(); assert len(b)==c[channel]['bytes'] and sha(b)==c[channel]['sha256']
    assert not (d/'stderr.bin').read_bytes()
    return c
def main():
    source=Path(__file__).read_bytes()
    with (F/'CLOSURE_PRELAUNCH_SOURCE.py').open('xb') as f: f.write(source); f.flush(); os.fsync(f.fileno())
    captures=[verify_capture(name,child) for name,child in [
      ('AUTHORING_ACTUAL_CAPTURE','author_source_documents.py'),
      ('SOURCE_INPUT_INSPECTION_ACTUAL_CAPTURE','inspect_source_inputs.py'),
      ('PRIVATE_CONTROLS_ACTUAL_CAPTURE','private_contract_controls.py')]]
    status=json.loads((F/'SOURCE_STATUS.json').read_bytes()); assert status['builder_executed'] is False and status['ROOT_operator_executed'] is False and status['ROOT_approval'] is None
    controls=json.loads((F/'PRIVATE_CONTRACT_CONTROL_RESULTS.json').read_bytes())
    assert controls['production_import_compile_or_execution'] is False and controls['independent_predicate_assertions']==376 and len(controls['malformed_predicate_cases_rejected'])==19
    inspection=json.loads((F/'SOURCE_INPUT_INSPECTION.json').read_bytes())
    assert inspection['complete_fixed_reads_count']==319 and inspection['foreign_exclusions_count']==64
    for row in inspection['complete_fixed_member_reads']:
        p=A/row['path']; b=p.read_bytes(); assert len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
    for name in ['DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json']:
        obj=json.loads((F/name).read_bytes()); assert obj['reading_completed'] is False and all(v is False for v in obj['root_flags'].values())
        assert obj['created_utc'] is None and obj['preparation_manifest_sha256'] is None
    for name in ['DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json']:
        obj=json.loads((F/name).read_bytes()); assert obj['approved_by_root'] is False and obj['created_utc'] is None
    assert not (A/'reviewed_candidate').exists()
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    with (F/'SOURCE_PREPARATION_RESEARCH_LOG.md').open('a') as f:
        f.write('\n'+now+' — self-only closure childPID'+str(os.getpid())+'. Source preparation100%; actual current freeze0%; new discovery0%.\n')
        f.write('All319 fixed reads individually matched and64 foreign bodies excluded. Genuine three own operations remain complete;376 independent private predicate assertions/19 rejected malformed cases and dated full-mode/exclusive-rename controls do not execute production. No failed own child launch occurred. Original181+manifest+four outer closure evidence remains unchanged. Production builder/operator never imported, compiled or executed; all ROOT approval drafts false/null. Five genuine future ROOT prerequisites, new different clean source adversary, actual freeze, new whole-current review and final reconciliation remain pending. No native/canonical/index/branch/remote/commit/push or outreach action.\n')
        f.flush(); os.fsync(f.fileno())
    paths=sorted(p for p in F.rglob('*') if p.is_file())
    assert all(not p.is_symlink() for p in F.rglob('*'))
    files={p.relative_to(F).as_posix() for p in paths}
    dirs={p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_dir()}
    expected={q.as_posix() for n in files for q in PurePosixPath(n).parents if str(q)!='.'}
    assert dirs==expected
    rows=[]
    for p in paths:
        assert not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
        b=p.read_bytes(); assert len(b)<100*1024*1024; os.chmod(p,0o444)
        assert stat.S_IMODE(p.stat().st_mode)==0o444
        rows.append({'path':p.relative_to(F).as_posix(),'bytes':len(b),'sha256':sha(b)})
    out={'schema':'PR45_CURRENT_SOURCE_ONLY_CLOSURE_v1','status':'CLOSED_SOURCE_ONLY_CURRENT_PREPARATION',
       'utc':now,'actual_closure_pid':os.getpid(),'self_excluded':['PREPARATION_MANIFEST.json'],
       'files_count':len(rows),'files':rows,'directories':sorted(dirs),'all_full_mode0444':True,
       'original18_manifest_sha256':'7180aa194d0fe99806e8aed1a92cbbc456676f26e0b2a18ad24cfcef4cd77833',
       'production_builder_sha256':sha((F/'prepare_current_packet.py').read_bytes()),
       'production_operator_sha256':sha((F/'capture_root_builder_operation.py').read_bytes()),
       'production_import_compile_or_execution':False,'ROOT_reading_or_approval':None,
       'current_freeze_or_new_whole_current_verdict':None,'original_substantive_attempts':1,
       'new_substantive_attempts':0,'audit_turns':0,'copied_probability_members_including_self_pair':17,
       'copied_literal_members_including_manifest':50,'individually_excluded_literal_foreign_members':64,
       'complete_own_prior_actual_captures':captures,'source_preparation_completion_estimate_percent':100,
       'actual_current_freeze_completion_estimate_percent':0,
       'separate_actual_source_closure_capture':'current_preparation_closure_actual_capture/CAPTURE.json',
       'outer_closure_capture_is_completed_only_after_this_child_exit':True,
       'dated_special_mode_fixtures_frozen0444_after_actual_controls':True,
       'foreign_bodies_copied_into_this_family':False}
    with (F/'PREPARATION_MANIFEST.json').open('xb') as f: f.write(dump(out)); f.flush(); os.fsync(f.fileno())
    os.chmod(F/'PREPARATION_MANIFEST.json',0o444)
    for row in rows:
        p=F/row['path']; b=p.read_bytes(); assert len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
    assert Path(__file__).read_bytes()==source
    print(json.dumps({'status':'CLOSED_SOURCE_ONLY_CURRENT_PREPARATION','files_count':len(rows),
      'manifest_sha256':sha((F/'PREPARATION_MANIFEST.json').read_bytes()),
      'manifest_bytes':(F/'PREPARATION_MANIFEST.json').stat().st_size,
      'builder_sha256':out['production_builder_sha256'],'operator_sha256':out['production_operator_sha256'],
      'ROOT_approval':None,'production_executed':False,'current_freeze':False},sort_keys=True))
if __name__=='__main__': main()
