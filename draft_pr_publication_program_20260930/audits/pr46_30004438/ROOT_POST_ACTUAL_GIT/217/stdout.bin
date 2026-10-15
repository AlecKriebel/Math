"""Fully inspect fixed first-party closures as bytes; production is never loaded."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, os, stat
F=Path(__file__).absolute().parent; A=F.parent
def sha(raw): return hashlib.sha256(raw).hexdigest()
def regular(p):
    assert not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()
def pin(name,expected=None,required_mode=0o444):
    p=A/name; raw=regular(p)
    if required_mode is not None: assert stat.S_IMODE(p.stat().st_mode)==required_mode
    if expected is not None: assert len(raw)==expected['bytes'] and sha(raw)==expected['sha256']
    return {'path':name,'bytes':len(raw),'sha256':sha(raw)}
def inventory(root):
    names=set(); dirs=set()
    assert root.is_dir() and not root.is_symlink()
    for p in root.rglob('*'):
        assert not p.is_symlink()
        name=p.relative_to(root).as_posix()
        if p.is_dir(): dirs.add(name)
        else: regular(p); names.add(name)
    expect={q.as_posix() for n in names for q in PurePosixPath(n).parents if str(q)!='.'}
    assert dirs==expect
    return names, sorted(dirs)
def normalized(row): return {k:row[k] for k in ['path','bytes','sha256']}
def main():
    records=[]
    original=pin('ORIGINAL_PREPARATION_MANIFEST.json'); records.append(original)
    assert original['sha256']=='da37655e9b3bab420862a0c17c761e67fa9a4bc2028a328d033547249c54ad2e'
    mf=json.loads(regular(A/original['path'])); assert mf['files_count']==len(mf['files'])==318
    members=[normalized(r) for r in mf['files']]
    observed=set(mf['authorship_root_files'])
    for root in mf['authorship_directory_roots']: observed|={root+'/'+n for n in inventory(A/root)[0]}
    assert observed=={r['path'] for r in members}
    records.extend(pin(r['path'],r) for r in members)
    closure=[]
    for n in sorted(inventory(A/'original_preparation_closure_actual_capture')[0]):
        closure.append(pin('original_preparation_closure_actual_capture/'+n))
    assert len(closure)==5
    records.extend(closure)
    families={}
    for family,name,expected,expected_count in [
      ('projective_algebra_family','FAMILY_MANIFEST.json','655e5a8c68cdc44efb78a6538000482b3c91301e1abdc15797e783526d6bea64',34),
      ('complex_dynamics_family','COMPLEX_DYNAMICS_MANIFEST.json','5172b9086230e932fe47b028a7e242ffa9c4fda1c06f19ee41c63753f73eb18e',33)]:
        m=pin(family+'/'+name); assert m['sha256']==expected; records.append(m)
        obj=json.loads(regular(A/family/name)); own=[normalized(r) for r in obj['files']]
        assert len(own)==obj['files_count']==expected_count
        actual,dirs=inventory(A/family); extra=actual-{r['path'] for r in own}-{name}
        expected_extra=set(obj['self_excluded'])-{name}
        assert extra==expected_extra
        assert (len(extra)==5 if family=='projective_algebra_family' else not extra)
        separate=[pin(family+'/'+n) for n in sorted(extra)]
        records.extend(pin(family+'/'+r['path'],r) for r in own); records.extend(separate)
        families[family]={'manifest':dict(m,path=name),'members':own,
          'separate_excluded_closure':[dict(r,path=r['path'][len(family)+1:]) for r in separate],
          'manifest_self_excluded':obj['self_excluded'],'directories':dirs,
          'directory_modes':{n:stat.S_IMODE((A/family/n).stat().st_mode) for n in dirs}}
    root_fixed=[]
    for n in ['root_original_actual_reproduction_v2/MANIFEST.json','ROOT_MATHEMATICAL_REVIEW.md',
      'ROOT_COMPLETE_RAW_SQL_AUDIT.json','root_original_actual_reproduction_v2/ROOT_CURRENT_REPRODUCTION_SUMMARY.json']:
        root_fixed.append(pin(n,required_mode=None if '/' not in n else 0o444))
    root_manifest=json.loads(regular(A/'root_original_actual_reproduction_v2/MANIFEST.json'))
    assert root_manifest['files_count']==len(root_manifest['files'])==37
    assert inventory(A/'root_original_actual_reproduction_v2')[0]=={r['path'] for r in root_manifest['files']}|{'MANIFEST.json'}
    root_fixed.extend(pin('root_original_actual_reproduction_v2/'+r['path'],r) for r in root_manifest['files'])
    root_fixed.extend(pin('root_reproduction_closure_actual_capture/'+n,required_mode=None) for n in sorted(inventory(A/'root_reproduction_closure_actual_capture')[0]))
    records.extend(root_fixed)
    pins={'schema':'PR46_FIXED_CURRENT_SOURCE_INPUTS_v1','status':'SOURCE_ONLY_ROOT_PREREQUISITES_PENDING',
      'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'snapshot_manifest':pin('snapshot_manifest.json'),
      'original_metadata':pin('original_pr_metadata.json'),'original_preparation_manifest':original,
      'original_preparation_members':members,'original_separate_closure_capture':closure,'families':families,
      'genuine_closed_ROOT_evidence_fixed_rows':root_fixed,'ROOT_approval_fields_authored':False,
      'legacy_PDF_hashes_are_attribution_only':True,'foreign_raw_cache_SQL_PDF_header_cookie_bodies_copied':False}
    result={'schema':'PR46_SOURCE_COMPLETE_FIXED_INPUT_INSPECTION_v1','actual_pid':os.getpid(),
      'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'complete_fixed_member_reads':records,
      'complete_fixed_reads_count':len(records),'original_scoped318_plus_self_unchanged':True,
      'algebra34_plus_self_plus_five_separate_closure_members':True,'complex33_plus_self_closure_capture_included':True,
      'empty_failed_json_streams_preserved_as_bytes':True,'ROOT_approval':None,
      'production_import_compile_or_execution':False,'actual_current_freeze':False}
    for name,obj in [('STATIC_INPUT_BINDINGS.json',pins),('SOURCE_INPUT_INSPECTION.json',result)]:
        with (F/name).open('x') as out: json.dump(obj,out,indent=2,allow_nan=False); out.write('\n'); out.flush(); os.fsync(out.fileno())
    print(json.dumps({'actual_pid':os.getpid(),'complete_fixed_reads_count':len(records),'ROOT_approval':None,
      'production_import_compile_or_execution':False,'foreign_bodies_copied':False}))
if __name__=='__main__': main()
