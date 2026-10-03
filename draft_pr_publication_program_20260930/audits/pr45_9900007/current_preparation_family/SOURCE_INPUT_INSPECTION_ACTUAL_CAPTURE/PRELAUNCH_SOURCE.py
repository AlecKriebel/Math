"""Inspect all fixed source inputs completely, with foreign bodies hashed in place only."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat
F=Path(__file__).resolve().parent; A=F.parent
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(name,expected=None):
    p=A/name; assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
    b=p.read_bytes(); assert stat.S_IMODE(p.stat().st_mode)==0o444
    if expected is not None: assert len(b)==expected['bytes'] and sha(b)==expected['sha256']
    return {'path':name,'bytes':len(b),'sha256':sha(b),'full_mode':0o444}
def main():
    b=json.loads((F/'STATIC_INPUT_BINDINGS.json').read_bytes()); records=[]
    for r in [b['snapshot_manifest'],b['original_metadata']]+b['auxiliary']:
        records.append(pin(r['path'],r))
    orig=json.loads((A/'ORIGINAL_PREPARATION_MANIFEST.json').read_bytes())
    assert len(orig['files'])==orig['files_count']==181
    assert all((A/r['path']).read_bytes() and len((A/r['path']).read_bytes())==r['bytes'] and sha((A/r['path']).read_bytes())==r['sha256'] if r['bytes'] else (A/r['path']).read_bytes()==b'' for r in orig['files'])
    exclusions=[]
    for family,info in b['families'].items():
        d=A/family; m=info['manifest']; records.append(pin(family+'/'+m['path'],m))
        own={r['path'] for r in info['copied_members']}; foreign={r['path'] for r in info['foreign_members']}
        assert not own & foreign
        files={p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file()}
        dirs={p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_dir()}
        assert files==own|foreign|{m['path']} and dirs==set(info['directories'])==set(info['directory_modes'])
        assert all(not p.is_symlink() for p in d.rglob('*'))
        assert all(stat.S_IMODE((d/name).stat().st_mode)==mode for name,mode in info['directory_modes'].items())
        for r in info['copied_members']+info['foreign_members']:
            rec=pin(family+'/'+r['path'],r); records.append(rec)
            if r['path'] in foreign: exclusions.append(rec)
        mf=json.loads((d/m['path']).read_bytes())
        if family=='probability_metric_family':
            assert own=={r['path'] for r in mf['files']}|{'OWN_CLOSURE.sha256'} and not foreign
            assert (d/'OWN_CLOSURE.sha256').read_text().split()[0]==sha((d/'OWN_CLOSURE.json').read_bytes())
        else:
            assert own=={r['path'] for r in mf['files'] if r['path']!=m['path'] and r['publication_allowed'] is True}
            assert foreign=={r['path'] for r in mf['files'] if r['publication_allowed'] is False}
            assert len(foreign)==64 and len(own)==49
    for family,names in [('probability_metric_family',['REPORT.md','VERDICT.json']),('literal_priority_family',['REVIEW.md','VERDICT.json','PRIORITY_COMPARISON.md'])]:
        for name in names: assert (A/family/name).read_text().strip()
    result={'schema':'PR45_CURRENT_SOURCE_COMPLETE_INPUT_INSPECTION_v1','actual_pid':os.getpid(),
      'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'complete_fixed_member_reads':records,
      'complete_fixed_reads_count':len(records),'individual_foreign_exclusions':exclusions,
      'foreign_exclusions_count':len(exclusions),'all_186_original_preparation_inputs_unchanged':True,
      'family_topologies_and_full_modes_checked':True,'production_import_compile_or_execution':False,
      'ROOT_approval':None,'actual_current_freeze':False}
    with (F/'SOURCE_INPUT_INSPECTION.json').open('x') as f: json.dump(result,f,indent=2); f.write('\n')
    print(json.dumps({k:result[k] for k in ['complete_fixed_reads_count','foreign_exclusions_count','all_186_original_preparation_inputs_unchanged','production_import_compile_or_execution','ROOT_approval']},sort_keys=True))
if __name__=='__main__': main()
