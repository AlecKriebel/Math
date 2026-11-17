"""Passive input/primary identity and finite owned-packet metadata seal only."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import time
ROOT=Path(__file__).resolve().parent
assert ROOT.name=='adversarial-continuation-sol-20261117' and ROOT.parents[1].name=='23204810'
def encode(value):
    return (json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def snapshot(root):
    entries=[]
    for path in [root]+sorted(root.rglob('*'),key=lambda p:p.relative_to(root).as_posix()):
        info=path.lstat()
        name='.' if path==root else path.relative_to(root).as_posix()
        row={'path':name,'mode':oct(stat.S_IMODE(info.st_mode)),'mtime_ns':info.st_mtime_ns,'ctime_ns':info.st_ctime_ns,'device':info.st_dev,'inode':info.st_ino,'hidden':any(v.startswith('.') for v in Path(name).parts if v!='.')}
        assert stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)
        if stat.S_ISDIR(info.st_mode):
            row.update(kind='directory',empty=not any(path.iterdir()))
        else:
            raw=path.read_bytes()
            row.update(kind='file',bytes=len(raw),empty=not raw,SHA256=hashlib.sha256(raw).hexdigest())
        entries.append(row)
    return {'root':str(root),'files':sum(r['kind']=='file' for r in entries),'child_directories':sum(r['kind']=='directory' for r in entries)-1,'entries':entries}
before=json.loads((ROOT/'INPUT_GUARDS_BEFORE.json').read_bytes())
def inputs_guard():
    result={key:snapshot(Path(before[key]['root'])) for key in ('source','INITIAL')}
    assert result['source']==before['source'],'entire source61/13 unchanged'
    assert result['INITIAL']==before['INITIAL'],'entire original INITIAL38/1 unchanged'
    return result
after=inputs_guard()
provenance=json.loads((ROOT/'PRIMARY_PROVENANCE.json').read_bytes())
assert len(provenance['EGH'])==11
for row in provenance['EGH']:
    raw=(ROOT/row['local_file']).read_bytes()
    expected=row.get('SHA256_observed_by_shasum',row.get('SHA256_expected'))
    assert hashlib.sha256(raw).hexdigest()==expected
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['Git_blob_SHA']
for name,expected in {
    'primary/HWW-1601.06928v1.pdf':'b66c69b4c9e901ddb2b9fc6e655a9d4a7c276558638014ee5bb0075fbf453172',
    'primary/HWW-1601.06928v1.txt':'ad21ad36c2277a5b9fa1c02c77cd84a75f63abd9ce9a5f03698f087d91900264'
}.items():
    assert digest(ROOT/name)==expected
with (ROOT/'INPUT_GUARDS_AFTER.json').open('xb') as handle:
    handle.write(encode({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),**after,'all_before_after_exact':True,'primary_bytes_match_exact_Git_blob_and_SHA256':True}))
final=json.loads((ROOT/'FINAL.json').read_bytes())
assert final['status']=='SCIENTIFIC_PASS_EXACT_ATTRIBUTED_CONSEQUENCE_WRITTEN_REVIEW_PENDING_ROOT_DISPOSITION'
assert final['completion_percent_assigned_full_written_review']==100
assert final['native_upstream_scientific_execution_import_AST_compile_test']==0
assert final['publication_or_future_action_authority'] is False and final['follow_up'] is None
TERMINALS={'MANIFEST.json','SEAL.json'}
assert all(not os.path.lexists(ROOT/name) for name in TERMINALS)
handles={name:(ROOT/name).open('xb') for name in sorted(TERMINALS)}
freeze_ns=time.time_ns()
freeze_UTC=datetime.datetime.fromtimestamp(freeze_ns/1_000_000_000,datetime.timezone.utc).isoformat()
for name in TERMINALS:
    os.chmod(ROOT/name,0o644)
    os.utime(ROOT/name,ns=(freeze_ns,freeze_ns))
objects=[ROOT]+sorted(ROOT.rglob('*'),key=lambda p:p.relative_to(ROOT).as_posix())
entries=[]
for path in objects:
    name='.' if path==ROOT else path.relative_to(ROOT).as_posix()
    info=path.lstat()
    row={'path':name,'mode':oct(stat.S_IMODE(info.st_mode)),'mtime_ns':info.st_mtime_ns,'hidden':any(v.startswith('.') for v in Path(name).parts if v!='.')}
    assert stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)
    if stat.S_ISDIR(info.st_mode):
        row.update(kind='directory',empty=not any(path.iterdir()))
    else:
        raw=path.read_bytes()
        row.update(kind='file',bytes=len(raw),empty=not raw)
        if name in TERMINALS:
            row['content_hash_exclusion']='Already-created exact terminal pair only; actual mode/mtime/bytes/hidden/empty/topology included'
        else:
            row['SHA256']=hashlib.sha256(raw).hexdigest()
    entries.append(row)
files=sum(row['kind']=='file' for row in entries)
dirs=sum(row['kind']=='directory' for row in entries)-1
assert (files,dirs)==(34,1),(files,dirs)
manifest={'schema':'finite-independent-scientific-continuation-namespace-v1','scope':str(ROOT),'freeze_UTC':freeze_UTC,'file_count':files,'child_directory_count':dirs,'root_including_directory_count':dirs+1,'logical_immutable_freeze_individual_modes_retained':True,'terminal_content_hash_exclusions_exact':sorted(TERMINALS),'entries':entries}
seal={'schema':'23204810-independent-adversarial-continuation-seal-v1','scope':str(ROOT),'freeze_UTC':freeze_UTC,'file_count':files,'child_directory_count':dirs,'status':final['status'],'completion_percent':100,'source61_13_and_old_INITIAL38_1_whole_before_after_exact':True,'primary11_Git_blobs_SHA256_and_HWW_pins_exact':True,'FINAL_SHA256':digest(ROOT/'FINAL.json'),'REPORT_SHA256':digest(ROOT/'REPORT.md'),'PRIMARY_ANALYSIS_SHA256':digest(ROOT/'PRIMARY_ANALYSIS.md'),'PROOF_SHA256':digest(ROOT/'PROOF_AND_BOUNDARY_REVIEW.md'),'READ_LEDGER_SHA256':digest(ROOT/'READ_LEDGER.json'),'manifest_SHA256':'0'*64,'native_upstream_scientific_execution_import_AST_compile_test':0,'own_fully_read_passive_administrative_seal_only':True,'formal_or_human_refereeing_certificate':False,'AA':None,'redirect':None,'follow_up':None,'publication_or_future_action_authority':False,'stop_for_root_disposition':True}
for unused in range(20):
    manifest_bytes=encode(manifest)
    seal['manifest_SHA256']=hashlib.sha256(manifest_bytes).hexdigest()
    seal_bytes=encode(seal)
    sizes={'MANIFEST.json':len(manifest_bytes),'SEAL.json':len(seal_bytes)}
    changed=False
    for row in entries:
        if row['path'] in TERMINALS and (row['bytes']!=sizes[row['path']] or row['empty']):
            row['bytes'],row['empty']=sizes[row['path']],False
            changed=True
    if not changed:
        break
else:
    raise AssertionError('terminal-size fixed point')
for name,raw in (('MANIFEST.json',manifest_bytes),('SEAL.json',seal_bytes)):
    handles[name].write(raw)
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
        assert stat.S_ISDIR(info.st_mode) and row['empty']==(not any(path.iterdir()))
    else:
        assert stat.S_ISREG(info.st_mode)
        raw=path.read_bytes()
        assert len(raw)==row['bytes'] and row['empty']==(not raw)
        if 'SHA256' in row:
            assert hashlib.sha256(raw).hexdigest()==row['SHA256']
assert digest(ROOT/'MANIFEST.json')==seal['manifest_SHA256']
assert inputs_guard()==after
print(json.dumps({'freeze_UTC':freeze_UTC,'files':files,'child_directories':dirs,'source61_13_INITIAL38_1_exact':True,'completion_percent':100,'scientific_execution':0,'external_SHA256':{name:digest(ROOT/name) for name in ('FINAL.json','REPORT.md','MANIFEST.json','SEAL.json')}},indent=2))
