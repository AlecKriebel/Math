"""Passive original source and sealed own INITIAL identity; no science execution."""
import hashlib
import json
from pathlib import Path
import stat
import datetime
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'adversarial-sol'
SOURCE=ROOT.parents[1]/'sources'
assert ROOT.name=='adversarial-continuation-sol-20261117' and SOURCE.parent.name=='23204810'
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
for name,expected in {'INITIAL_MANIFEST.json':'44bb8b27b8082e93c3d2b93b72cd8fdcb89dac9899b5b724abf9d83faadde701','INITIAL_SEAL.json':'5690f415d28faae02f504a2bb890af1c9124caf74c9f451d59528964a88a1df6'}.items():
    assert hashlib.sha256((OLD/name).read_bytes()).hexdigest()==expected
source=snapshot(SOURCE)
old=snapshot(OLD)
assert (source['files'],source['child_directories'])==(61,13)
assert (old['files'],old['child_directories'])==(38,1)
expected_source=json.loads((OLD/'SOURCE_AFTER_INITIAL.json').read_bytes())
assert source['root']==expected_source['root']
assert source['entries']==[{k:v for k,v in row.items() if k!='MD5'} for row in expected_source['entries']]
manifest=json.loads((OLD/'INITIAL_MANIFEST.json').read_bytes())
actual={row['path']:row for row in old['entries']}
assert set(actual)=={row['path'] for row in manifest['entries']}
for row in manifest['entries']:
    current=actual[row['path']]
    assert all(current[k]==row[k] for k in ('kind','mode','mtime_ns','hidden','empty'))
    if row['kind']=='file':
        assert current['bytes']==row['bytes']
        if 'SHA256' in row:
            assert current['SHA256']==row['SHA256']
result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':source,'INITIAL':old,'source61_13_and_INITIAL38_1_exact':True,'scientific_execution':0}
with (ROOT/'INPUT_GUARDS_BEFORE.json').open('x') as handle:
    json.dump(result,handle,indent=2)
    handle.write('\n')
print(json.dumps({'status':'BOUND_ORIGINAL_INPUTS_EXACT','source':[61,13],'INITIAL':[38,1],'scientific_execution':0}))
