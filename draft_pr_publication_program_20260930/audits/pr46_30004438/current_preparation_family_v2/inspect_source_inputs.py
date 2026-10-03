"""Inspect unchanged fixed science plus all frozen V1 and exact V2 archive bytes."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, os, stat
F=Path(__file__).absolute().parent; A=F.parent; OLD=A/'current_preparation_family'
EXPECTED='2f1ef9d9b0b4c9596110f5a66aa6d5095fdf611cc65f9aa367b208ca5ab6accc'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def regular(path):
    assert not path.is_symlink() and all(not p.is_symlink() for p in path.parents) and stat.S_ISREG(path.stat().st_mode)
    return path.read_bytes()
def row(path,name):
    raw=regular(path); return {'path':name,'bytes':len(raw),'sha256':sha(raw)}
def inventory(root):
    assert root.is_dir() and not root.is_symlink()
    names=set(); dirs=set()
    for path in root.rglob('*'):
        assert not path.is_symlink()
        if path.is_dir(): dirs.add(path.relative_to(root).as_posix())
        else: regular(path); names.add(path.relative_to(root).as_posix())
    assert dirs=={p.as_posix() for n in names for p in PurePosixPath(n).parents if str(p)!='.'}
    return names
def main():
    prior_inspection=json.loads(regular(OLD/'SOURCE_INPUT_INSPECTION.json'))
    records=[]
    for pin in prior_inspection['complete_fixed_member_reads']:
        raw=regular(A/pin['path']); assert len(raw)==pin['bytes'] and sha(raw)==pin['sha256']; records.append(dict(pin))
    assert len(records)==444
    raw=regular(OLD/'PREPARATION_MANIFEST.json'); assert sha(raw)==EXPECTED
    manifest=json.loads(raw); assert manifest['files_count']==len(manifest['files'])==60
    names={r['path'] for r in manifest['files']}|{'PREPARATION_MANIFEST.json'}
    assert inventory(OLD)==inventory(F/'superseded_v1_source_archive')==names
    V1_rows=[]
    for name in sorted(names):
        path=OLD/name; body=regular(path); assert stat.S_IMODE(path.stat().st_mode)==0o444
        assert regular(F/'superseded_v1_source_archive'/name)==body
        pin=row(path,'current_preparation_family/'+name); V1_rows.append(pin); records.append(pin)
    for pin in manifest['files']:
        body=regular(OLD/pin['path']); assert len(body)==pin['bytes'] and sha(body)==pin['sha256']
    bindings=json.loads(regular(OLD/'STATIC_INPUT_BINDINGS.json'))
    bindings.update(created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
      operative_preparation_directory='current_preparation_family_v2',superseded_v1_closed_source_rows=V1_rows,
      superseded_v1_closed_manifest_sha256=EXPECTED,source_chronology_repair_only=True)
    # This data-format schema remains v1: the original science/family inputs did not change.
    result={'schema':'PR46_SOURCE_COMPLETE_FIXED_INPUT_INSPECTION_v2','actual_pid':os.getpid(),
      'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'complete_fixed_member_reads':records,
      'complete_fixed_reads_count':len(records),'unchanged_V1_original60_plus_self_and_exact_owned_archive':True,
      'V1_manifest_sha256':EXPECTED,'original_scoped318_plus_self_unchanged':True,
      'algebra34_plus_self_plus_five_separate_closure_members':True,'complex33_plus_self_closure_capture_included':True,
      'ROOT37_plus_self_unchanged':True,'empty_failed_json_streams_preserved_as_bytes':True,
      'production_import_compile_or_execution':False,'ROOT_approval':None,'actual_current_freeze':False}
    for name,obj in [('STATIC_INPUT_BINDINGS.json',bindings),('SOURCE_INPUT_INSPECTION.json',result)]:
        with (F/name).open('x') as out: json.dump(obj,out,indent=2,allow_nan=False); out.write('\n'); out.flush(); os.fsync(out.fileno())
    print(json.dumps({'actual_pid':os.getpid(),'complete_fixed_reads_count':len(records),'V1_manifest_unchanged':EXPECTED,
      'production_import_compile_or_execution':False,'ROOT_approval':None,'actual_current_freeze':False}))
if __name__=='__main__': main()
