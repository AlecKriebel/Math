"""Own-namespace administrative metadata seal; never interprets helper source."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import time

ROOT=Path(__file__).resolve().parent
assert ROOT.name=='gram-thompson-d4-production-prepare-corrected-sol-20261117'
ORIGINAL=ROOT.parent/'gram-thompson-d4-production-prepare-sol-20261117'
ORIGINAL_PINS={
    'release_overlay.py':'08e8eb267098f0bc922cdeb11ffb7f0ce847347901072657234274a3dbfd5c65',
    'PLAN.json':'0a7b86d1853b3420260e3f04983e23f4196af33879464c603007857b76531d10',
    'FINAL.json':'1232d5290a59c0c48c28fe2895c945aa5955832aa945fc8f42ce69bbd0d8206a',
    'REPORT.md':'5598c318b109fbab0801f8c094ced2d8544afa7881c103fdfc9490983d96d657',
    'MANIFEST.json':'e81bbb91abb9ced77ff1012774a66f15f68a85079ec3e54f8fad06b87318543c',
    'SEAL.json':'1e9123b7b4cabc6778c275e693dabfc6226fd41edc1a28c9dc2606b69b48d141'
}
def original_guard():
    for name,expected in ORIGINAL_PINS.items():
        assert hashlib.sha256((ORIGINAL/name).read_bytes()).hexdigest()==expected
    saved=json.loads((ORIGINAL/'MANIFEST.json').read_bytes())
    assert saved['scope']==str(ORIGINAL)
    assert (saved['file_count'],saved['child_directory_count'])==(9,0)
    assert saved['terminal_content_hash_exclusions_exact']==['MANIFEST.json','SEAL.json']
    actual=[ORIGINAL]+sorted(ORIGINAL.rglob('*'),key=lambda p:p.relative_to(ORIGINAL).as_posix())
    expected={row['path']:row for row in saved['entries']}
    assert set(expected)=={'.' if path==ORIGINAL else path.relative_to(ORIGINAL).as_posix() for path in actual}
    result=[]
    for path in actual:
        name='.' if path==ORIGINAL else path.relative_to(ORIGINAL).as_posix()
        row=expected[name]
        info=path.lstat()
        assert oct(stat.S_IMODE(info.st_mode))==row['mode'] and info.st_mtime_ns==row['mtime_ns']
        assert row['hidden']==any(x.startswith('.') for x in Path(name).parts if x!='.')
        record={'path':name,'mode':info.st_mode,'mtime_ns':info.st_mtime_ns,'ctime_ns':info.st_ctime_ns,'device':info.st_dev,'inode':info.st_ino}
        if row['kind']=='directory':
            assert stat.S_ISDIR(info.st_mode) and row['empty']==(not any(path.iterdir()))
        else:
            assert row['kind']=='file' and stat.S_ISREG(info.st_mode)
            raw=path.read_bytes()
            assert len(raw)==row['bytes'] and row['empty']==(not raw)
            record.update(bytes=len(raw),SHA256=hashlib.sha256(raw).hexdigest())
            if name in ('MANIFEST.json','SEAL.json'):
                assert 'SHA256' not in row and record['SHA256']==ORIGINAL_PINS[name]
            else:
                assert record['SHA256']==row['SHA256']
        result.append(record)
    return result
original_before=original_guard()
final=json.loads((ROOT/'FINAL.json').read_bytes())
assert final['status']=='SOURCE_ONLY_CORRECTED_UNEXECUTED_PENDING_INDEPENDENT_STATIC_AND_ROOT_READ'
assert final['all_old_new_helper_default_modes_import_AST_compile_help_test_executions']==0
assert final['publication_or_future_active_mode_authority'] is False
for key in ('helper','PLAN'):
    row=final[key]
    path=ROOT/row['path']
    data=path.read_bytes()
    assert len(data)==row['bytes'] and len(data.splitlines())==row['lines']
    assert hashlib.sha256(data).hexdigest()==row['SHA256']
    assert format(stat.S_IMODE(path.lstat().st_mode),'04o')==row['mode']=='0644'
assert not os.path.lexists(ROOT.parent/'gram-thompson-d4-runtime-sol-20261117')
TERMINALS={'MANIFEST.json','SEAL.json'}
assert all(not (ROOT/name).exists() for name in TERMINALS)
handles={name:(ROOT/name).open('xb') for name in sorted(TERMINALS)}
freeze_ns=time.time_ns()
freeze_UTC=datetime.datetime.fromtimestamp(freeze_ns/1_000_000_000,datetime.timezone.utc).isoformat()
for name in TERMINALS:
    os.chmod(ROOT/name,0o644)
    os.utime(ROOT/name,ns=(freeze_ns,freeze_ns))
objects=[ROOT]+sorted(ROOT.rglob('*'),key=lambda p:p.relative_to(ROOT).as_posix())
entries=[]
for path in objects:
    rel='.' if path==ROOT else path.relative_to(ROOT).as_posix()
    info=path.lstat()
    assert stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode),str(path)
    row={'path':rel,'mode':oct(stat.S_IMODE(info.st_mode)),'mtime_ns':info.st_mtime_ns,
         'hidden':any(x.startswith('.') for x in Path(rel).parts if x!='.')}
    if stat.S_ISDIR(info.st_mode):
        row.update(kind='directory',empty=not any(path.iterdir()))
    else:
        data=path.read_bytes()
        row.update(kind='file',bytes=len(data),empty=not data)
        if rel in TERMINALS:
            row['content_hash_exclusion']='Already-created exact terminal pair only; full object/mode/mtime/bytes/topology retained'
        else:
            row['SHA256']=hashlib.sha256(data).hexdigest()
    entries.append(row)
files=sum(row['kind']=='file' for row in entries)
dirs=sum(row['kind']=='directory' for row in entries)-1
assert (files,dirs)==(9,0),(files,dirs)
digest=lambda name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
manifest={'schema':'finite-inert-production-source-namespace-v1','scope':str(ROOT),'freeze_UTC':freeze_UTC,
          'file_count':files,'child_directory_count':dirs,'root_including_directory_count':dirs+1,
          'logical_freeze_individual_modes_retained':True,'terminal_content_hash_exclusions_exact':sorted(TERMINALS),'entries':entries}
seal={'schema':'gram-thompson-d4-inert-source-seal-v1','scope':str(ROOT),'freeze_UTC':freeze_UTC,
      'status':'SOURCE_ONLY_CORRECTED_FROZEN_UNEXECUTED_PENDING_INDEPENDENT_STATIC_ROOT_READ',
      'completion_percent_source_preparation':100,'file_count':files,'child_directory_count':dirs,
      'helper_SHA256':digest('release_overlay.py'),'PLAN_SHA256':digest('PLAN.json'),
      'FINAL_SHA256':digest('FINAL.json'),'REPORT_SHA256':digest('REPORT.md'),
      'manifest_SHA256':'0'*64,'production_helper_default_modes_import_AST_compile_help_test_executions':0,
      'original_UNFIT_namespace9_0_before_after_exact':True,'original_external_pins':ORIGINAL_PINS,
      'own_metadata_seal_only':True,'runtime_created':False,'Pignore_W_Git_network_Sheet_mutation':False,
      'execution_install_commit_deploy_live_certificate':False,'AA':None,'redirect':None,'follow_up':None,
      'publication_or_future_active_mode_authority':False,'stop_for_root_adoption':True}
encode=lambda value:(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()
for unused in range(20):
    manifest_bytes=encode(manifest)
    seal['manifest_SHA256']=hashlib.sha256(manifest_bytes).hexdigest()
    seal_bytes=encode(seal)
    sizes={'MANIFEST.json':len(manifest_bytes),'SEAL.json':len(seal_bytes)}
    changed=False
    for row in entries:
        if row['path'] in TERMINALS:
            if row['bytes']!=sizes[row['path']] or row['empty']:
                row['bytes'],row['empty']=sizes[row['path']],False
                changed=True
    if not changed:
        break
else:
    raise AssertionError('Terminal byte-count fixed point failed')
for name,data in (('MANIFEST.json',manifest_bytes),('SEAL.json',seal_bytes)):
    handles[name].write(data)
    handles[name].flush()
    os.fsync(handles[name].fileno())
    handles[name].close()
    os.utime(ROOT/name,ns=(freeze_ns,freeze_ns))
actual=[ROOT]+sorted(ROOT.rglob('*'),key=lambda p:p.relative_to(ROOT).as_posix())
assert actual==objects
for path,row in zip(actual,entries):
    info=path.lstat()
    assert oct(stat.S_IMODE(info.st_mode))==row['mode'] and info.st_mtime_ns==row['mtime_ns']
    if row['kind']=='directory':
        assert stat.S_ISDIR(info.st_mode) and (not any(path.iterdir()))==row['empty']
    else:
        assert stat.S_ISREG(info.st_mode)
        data=path.read_bytes()
        assert len(data)==row['bytes'] and (not data)==row['empty']
        if 'SHA256' in row:
            assert hashlib.sha256(data).hexdigest()==row['SHA256']
assert digest('MANIFEST.json')==seal['manifest_SHA256']
assert original_guard()==original_before
print(json.dumps({'freeze_UTC':freeze_UTC,'files':files,'child_directories':dirs,
                  'status':seal['status'],'external_SHA256':{name:digest(name) for name in
                  ('release_overlay.py','PLAN.json','FINAL.json','REPORT.md','MANIFEST.json','SEAL.json')}},indent=2))
