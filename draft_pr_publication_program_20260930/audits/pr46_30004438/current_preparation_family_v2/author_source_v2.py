"""Author a distinct SOURCE-only V2; preserve all closed V1 bytes and modes."""
from pathlib import Path
import datetime as dt, difflib, hashlib, json, os, stat
F=Path(__file__).absolute().parent; A=F.parent; OLD=A/'current_preparation_family'
EXPECTED='2f1ef9d9b0b4c9596110f5a66aa6d5095fdf611cc65f9aa367b208ca5ab6accc'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def regular(path):
    assert not path.is_symlink() and all(not p.is_symlink() for p in path.parents) and stat.S_ISREG(path.stat().st_mode)
    return path.read_bytes()
def write(name,data):
    if isinstance(data,str): data=data.encode()
    path=F/name; path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as out: out.write(data); out.flush(); os.fsync(out.fileno())
def structured(name,obj): write(name,json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def main():
    original_manifest_raw=regular(OLD/'PREPARATION_MANIFEST.json'); assert sha(original_manifest_raw)==EXPECTED
    original=json.loads(original_manifest_raw); assert original['files_count']==len(original['files'])==60
    actual={p.relative_to(OLD).as_posix() for p in OLD.rglob('*') if p.is_file()}
    assert actual=={r['path'] for r in original['files']}|{'PREPARATION_MANIFEST.json'}
    for row in original['files']:
        path=OLD/row['path']; raw=regular(path)
        assert len(raw)==row['bytes'] and sha(raw)==row['sha256'] and stat.S_IMODE(path.stat().st_mode)==0o444
        write('superseded_v1_source_archive/'+row['path'],raw)
    write('superseded_v1_source_archive/PREPARATION_MANIFEST.json',original_manifest_raw)
    builder_old=regular(OLD/'prepare_current_packet.py').decode()
    builder=builder_old.replace('current_preparation_family','current_preparation_family_v2')
    builder=builder.replace('PR46_CURRENT_SOURCE_ONLY_CLOSURE_v1','PR46_CURRENT_SOURCE_ONLY_CLOSURE_v2')
    builder=builder.replace('PR46_ROOT_BUILDER_PRELAUNCH_v1','PR46_ROOT_BUILDER_PRELAUNCH_v2')
    builder=builder.replace('root_pr46_current_build_','root_pr46_current_v2_build_').replace('root_pr46_current_outer_','root_pr46_current_v2_outer_')
    mistaken="'final_inner_GIT_COMMANDS_written_only_after_builder_exit':True"
    assert builder.count(mistaken)==1
    corrected="'final_inner_GIT_COMMANDS_written_incrementally_by_builder_before_exit':True,\n      'frozen_inner_command_copy_is_prepublication_prefix':True,\n      'outer_operator_does_not_write_inner_GIT_COMMANDS':True,\n      'ROOT_final_original_inner_commands_inspection_required_AFTER_child_exit':True"
    builder=builder.replace(mistaken,corrected)
    # The V1 source stays a dated archive, not an executable current source.
    insertion="    for row in pins['superseded_v1_closed_source_rows']:\n        checked(row,'dated_superseded_V1_source_mistaken_chronology_attribution_only')\n"
    marker="    require(git('branch','--show-current').strip()==b'main','Stay on main')\n"
    assert builder.count(marker)==1; builder=builder.replace(marker,marker+insertion)
    operator_old=regular(OLD/'capture_root_builder_operation.py').decode()
    operator=operator_old.replace('current_preparation_family','current_preparation_family_v2')
    operator=operator.replace('PR46_ROOT_BUILDER_PRELAUNCH_v1','PR46_ROOT_BUILDER_PRELAUNCH_v2')
    operator=operator.replace('PR46_ROOT_ACTUAL_BUILDER_OPERATION_v1','PR46_ROOT_ACTUAL_BUILDER_OPERATION_v2')
    operator=operator.replace('root_pr46_current_outer_','root_pr46_current_v2_outer_')
    builder=builder.replace("{'schema','approved_by_root','created_utc','notes','manifest','proof_notes','summary','raw_audit','source_adversary'}",
      "{'schema','approved_by_root','created_utc','notes','manifest','proof_notes','summary','raw_audit','source_adversary','operative_preparation_directory'}")
    builder=builder.replace("{'schema','approved_by_root','created_utc','reason','current_head','files'}",
      "{'schema','approved_by_root','created_utc','reason','current_head','files','operative_preparation_directory'}")
    builder=builder.replace("and evidence['schema']=='PR46_ROOT_EVIDENCE_BINDINGS_v1'", "and evidence['operative_preparation_directory']=='current_preparation_family_v2' and evidence['schema']=='PR46_ROOT_EVIDENCE_BINDINGS_v1'")
    builder=builder.replace("and current['schema']=='PR46_ROOT_FRESH13_INPUT_PREIMAGES_v1'", "and current['operative_preparation_directory']=='current_preparation_family_v2' and current['schema']=='PR46_ROOT_FRESH13_INPUT_PREIMAGES_v1'")
    builder=builder.replace("require(obj['schema']==schema and obj['reading_completed'] is True", "require(obj['operative_preparation_directory']=='current_preparation_family_v2' and obj['schema']==schema and obj['reading_completed'] is True")
    write('prepare_current_packet.py',builder); write('capture_root_builder_operation.py',operator)
    diff=''.join(difflib.unified_diff(builder_old.splitlines(keepends=True),builder.splitlines(keepends=True),
      fromfile='closed_V1/prepare_current_packet.py',tofile='SOURCE_V2/prepare_current_packet.py'))
    diff+=''.join(difflib.unified_diff(operator_old.splitlines(keepends=True),operator.splitlines(keepends=True),
      fromfile='closed_V1/capture_root_builder_operation.py',tofile='SOURCE_V2/capture_root_builder_operation.py'))
    write('SOURCE_REPAIR_DELTA.patch',diff)
    chronology=('\n\nV2 execution chronology qualification: the builder writes original inner GIT_COMMANDS.json incrementally in git() finally blocks while the builder is alive. The frozen inner copy is a prepublication prefix. The outer operator does not write inner commands; only its completed OUTER CAPTURE.json is written after child exit. ROOT must fully inspect the original final inner command record and complete streams AFTER actual child exit before promotion. Closed superseded V1 claimed otherwise in one reference field; its bytes remain unchanged and are preserved as dated first-party source evidence. V2 repairs that administrative claim and capture anchors without changing science or producing approval.\n')
    for name in ['CURRENT_OVERVIEW.md','SOURCE_PRECISION_QUALIFICATIONS.md','EXECUTION_CONTRACT.md']:
        doc=regular(OLD/name).decode().replace('current_preparation_family','current_preparation_family_v2')
        doc=doc.replace('SOURCE-only preparation','SOURCE-only V2 preparation')
        if name=='EXECUTION_CONTRACT.md':
            doc=doc.replace('ROOT must personally read the actual final outer CAPTURE and final inner GIT_COMMANDS at their original audit paths before promotion.',
              'The builder writes original inner GIT_COMMANDS incrementally before builder exit; its frozen copy is a prepublication prefix. The outer operator does not write inner commands. ROOT must personally read the actual final outer CAPTURE and original final inner GIT_COMMANDS with full streams AFTER child exit at their original audit paths before promotion.')
        write(name,doc+chronology+'\nEvery actual ROOT JSON prerequisite (read ledger, science card, fresh13, evidence bindings) additionally requires operative_preparation_directory exactly current_preparation_family_v2. For the exact-key fresh13/evidence objects this is an additional required key; old-schema identities for science/evidence remain stable while the directory and pinned SOURCE closure identify V2. The future outer prelaunch schema is PR46_ROOT_BUILDER_PRELAUNCH_v2; actual outer schema PR46_ROOT_ACTUAL_BUILDER_OPERATION_v2; inner/outer directory prefixes are root_pr46_current_v2_build_ and root_pr46_current_v2_outer_.\n')
    for name in ['DRAFT_ROOT_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json']:
        obj=json.loads(regular(OLD/name)); assert obj.get('reading_completed',False) is False and obj.get('approved_by_root',False) is False
        obj['operative_preparation_directory']='current_preparation_family_v2'
        structured(name,obj)
    write('DRAFT_ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md',regular(OLD/'DRAFT_ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md').decode()+chronology)
    status=json.loads(regular(OLD/'SOURCE_STATUS.json')); status.update(schema='PR46_CURRENT_SOURCE_ONLY_STATUS_v2',
      created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),operative_preparation_directory='current_preparation_family_v2',
      superseded_V1_manifest_sha256=EXPECTED,mandatory_administrative_chronology_correction=True)
    structured('SOURCE_STATUS.json',status)
    structured('REPAIR_INPUT_PINS.json',{'schema':'PR46_V2_REPAIR_ORIGINAL_CLOSED_INPUTS_v1',
      'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'V1_manifest_sha256':EXPECTED,
      'V1_manifest_bytes':len(original_manifest_raw),'V1_closed_members':60,'V1_all_original_bytes_and_full0444_unchanged':True,
      'superseded_builder_sha256':sha(builder_old.encode()),'superseded_operator_sha256':sha(operator_old.encode()),
      'new_builder_sha256':sha(builder.encode()),'new_operator_sha256':sha(operator.encode()),
      'production_import_compile_or_execution':False,'ROOT_approval':None})
    print(json.dumps({'actual_pid':os.getpid(),'status':'AUTHORED_DISTINCT_SOURCE_ONLY_V2',
      'V1_manifest_unchanged_sha256':EXPECTED,'new_builder_sha256':sha(builder.encode()),
      'new_operator_sha256':sha(operator.encode()),'production_import_compile_or_execution':False,'ROOT_approval':None}))
if __name__=='__main__': main()
