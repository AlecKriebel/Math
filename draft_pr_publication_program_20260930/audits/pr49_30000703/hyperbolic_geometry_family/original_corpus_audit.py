#!/usr/bin/python3
"""Independently verify the closed original corpus using its actual schemas."""
import datetime,hashlib,json,pathlib,stat
own=pathlib.Path(__file__).resolve().parent;a=own.parent
root45=a.parent/'pr45_9900007'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mode(p):return stat.S_IMODE(p.stat().st_mode)
mf=a/'ORIGINAL_PREPARATION_MANIFEST.json';d=json.loads(mf.read_bytes())
assert sha(mf)=='2eecad772938f3b220936c3317f1266d9a98de0f9d9750a6efa725c665f63b4c' and mf.stat().st_size==126347 and mode(mf)==0o444
assert d['schema']=='pr49-original-preparation-self-only-manifest/v1'
assert d['head']=='036a5ed59bee5ed79f08349290481584610f1456'
assert d['files_count']==len(d['files'])==350 and d['self_excluded']==['ORIGINAL_PREPARATION_MANIFEST.json']
filepaths=set();files=[]
for f in d['files']:
    p=a/f['path'];assert p.is_file() and not p.is_symlink()
    assert f['path'] not in filepaths;filepaths.add(f['path'])
    assert p.stat().st_size==f['bytes'] and sha(p)==f['sha256'] and mode(p)==f['full_mode']==0o444
    files.append({'path':f['path'],'sha256':f['sha256'],'bytes':f['bytes'],'full_mode':mode(p)})
actual_files={n for n in d['authorship_root_files']}
actual_dirs=set()
for n in d['authorship_directory_roots']:
    q=a/n;assert q.is_dir() and not q.is_symlink();actual_dirs.add(n)
    for p in q.rglob('*'):
        assert not p.is_symlink()
        rel=str(p.relative_to(a))
        if p.is_dir():actual_dirs.add(rel)
        elif p.is_file():actual_files.add(rel)
        else:raise AssertionError(rel)
assert actual_files==filepaths
assert actual_dirs==set(d['owned_directories'])=={r['path'] for r in d['owned_directory_bindings']}
assert len(actual_dirs)==63 and mode(a)==d['authorship_root_full_mode']
for r in d['owned_directory_bindings']:assert mode(a/r['path'])==r['full_mode']
captures=[]
for expected in d['complete_prior_actual_captures']:
    p=a/expected['path'];folder=p.parent;c=json.loads(p.read_bytes());pre=json.loads((folder/'PRELAUNCH.json').read_bytes())
    assert sha(p)==expected['capture_sha256']
    assert c['schema'] in ['pr49-original-actual-command/v1','pr49-original-readonly-git-command/v1']
    assert c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0
    assert pre['actual_execution'] is False and pre['completed'] is False and pre['pid'] is None and pre['exit_code'] is None
    for k in ['argv','cwd','operator_pid','operator_sha256','started_utc']:assert pre[k]==c[k]
    assert c['operator_unchanged'] is True and sha(folder/'prelaunch_operator.py')==c['operator_sha256']
    assert c['started_utc']<c['finished_utc']<d['created_utc']
    assert c['pid']==expected['pid'] and c['exit_code']==expected['exit_code']
    names={'CAPTURE.json','PRELAUNCH.json','stdout.bin','stderr.bin','prelaunch_operator.py'}
    target=c.get('target_source')
    if target is not None:
        assert pre['target_source']==target and c['target_unchanged'] is True
        q=folder/'prelaunch_target.py';assert sha(q)==target['sha256'] and q.stat().st_size==target['bytes'];names.add(q.name)
    for k in ['stdout','stderr']:
        q=folder/c[k]['path'];assert sha(q)==c[k]['sha256'] and q.stat().st_size==c[k]['bytes']
    assert {q.name for q in folder.iterdir()}==names
    if c['schema']=='pr49-original-actual-command/v1':
        assert c['expected_exit']==0
        assert c['capture_status']==('EXPECTED_ACTUAL_EXIT_COMPLETE' if c['exit_code']==0 else 'UNEXPECTED_OR_INCOMPLETE_ACTUAL_EXIT')
    else:assert c['exit_code']==0
    captures.append({'path':expected['path'],'schema':c['schema'],'pid':c['pid'],'exit_code':c['exit_code'],'full_split_streams_and_prelaunch_copies_verified':True})
assert len(captures)==58 and sum(c['exit_code']!=0 for c in captures)==2
assert sorted(c['exit_code'] for c in captures if c['exit_code']!=0)==[1,128]
outer=[]
for name in ['root_pr49_original_preparation_closure_actual_capture','root_pr49_original_preparation_closed_readback_actual_capture']:
    folder=root45/name;c=json.loads((folder/'CAPTURE.json').read_bytes())
    assert c['schema']=='root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True
    assert c['exit_code']==0 and c['operator_unchanged'] is True and sha(folder/'prelaunch_operator.py')==c['operator_sha256']
    assert {p.name for p in folder.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}
    for k in ['stdout','stderr']:
        q=folder/c[k]['path'];assert sha(q)==c[k]['sha256'] and q.stat().st_size==c[k]['bytes']
    body=json.loads((folder/'stdout.bin').read_bytes())
    assert body['manifest_sha256']==sha(mf)
    outer.append({'path':str(folder),'pid':c['pid'],'start':c['started_utc'],'finish':c['finished_utc'],'capture_sha256':sha(folder/'CAPTURE.json'),'schema':c['schema'],'actual_four_file_capture_verified':True,'stdout_keys':list(body)})
assert outer[0]['pid']==48827==d['actual_pid'] and outer[1]['pid']==49240
assert outer[0]['start']<=d['created_utc']<=outer[0]['finish']<outer[1]['start']<outer[1]['finish']
assert sha(a/'ROOT_ORIGINAL_CLOSURE_PRELAUNCH_SOURCE.py')==sha(a/'CLOSURE_PRELAUNCH_SOURCE.py')==sha(a/'close_original_preparation.py')
raw=json.loads((a/'ORIGINAL_COMPLETE_RAW_SQL_READ.json').read_bytes())
sel=raw['selected'];assert sel['upstream_report_key_present'] is False and sel['upstream_report_presence']=='ABSENT' and sel['sqlite_report_literal']=='{}'
assert raw['literal_importer_verified_rows']==len(raw['rows'])==raw['raw_problem_count']==raw['all_SQL_rows_read']==15458
native=json.loads((a/'ORIGINAL_NATIVE_SELECTED_READ_V2.json').read_bytes())
assert native['canonical_count']==len(native['current_canonical13_bindings'])==13 and native['transition_performed'] is False
for name in ['head_complete_selected_objects','working_complete_selected_objects']:
    n=native[name];assert n['catalog.json'][0]['local_status']=='queued' and n['catalog.json'][0]['turns_used']==0 and n['catalog.json'][0]['turn_limit']==5
    assert n['state.json']['key_present'] is False and n['history.jsonl']==[]
result={'schema':'pr49-hyperbolic-original-closed-corpus-audit/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_sha256':sha(mf),'complete_payload_files':len(files),'complete_total_files_including_manifest':len(files)+1,'exact_owned_directories':len(actual_dirs),'all4096_permission_bits_verified':True,'all_files_mode':'0444','all_file_bodies_verified':True,'all_58_captures':captures,'retained_original_failures':2,'external_ROOT_closure_and_readback':outer,'prior_report_qualification':'Upstream ABSENT, SQL literal{}, original administrative null','literal_importer_checks_attributed_and_manifest_bound':15458,'fresh_full_raw_SQL_rerun_by_this_family':False,'native_observation':'Original-head and dated working selections queued0/5, no state/history; current future transition remains pending','all_13_dated_binding_identities_closed':True,'current_native_authority':False}
(own/'ORIGINAL_CORPUS_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'original_files':350,'with_manifest':351,'directories':63,'original_captures':58,'original_failures':2,'root_closure_pid':48827,'root_readback_pid':49240,'manifest_sha256':sha(mf),'all_verified':True}))
