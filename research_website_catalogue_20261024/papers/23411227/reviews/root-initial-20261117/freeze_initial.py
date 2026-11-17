"""Freeze the finite original-only root assessment; no scientific activity."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat
import time

R = Path(__file__).resolve().parent
assert R.name == 'root-initial-20261117' and R.parent.parent.name == '23411227'
assert (R/'INITIAL.md').is_file()
run = json.loads((R/'RENDER_EXECUTION.json').read_bytes())
assert run['exit'] == 0 and run['source196_21_before_after_exact']
assert json.loads((R/'SOURCE_BEFORE.json').read_bytes()) == json.loads((R/'SOURCE_AFTER.json').read_bytes())
terminals = {'INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'}
assert not any((R/name).exists() for name in terminals)
handles = {name:(R/name).open('xb') for name in sorted(terminals)}
freeze_ns = time.time_ns()
for name in terminals:
    os.utime(R/name, ns=(freeze_ns,freeze_ns))
paths = [R] + sorted(R.rglob('*'))
assert sum(p.is_file() for p in paths) == 18 and sum(p.is_dir() for p in paths) == 2
for p in paths:
    info = p.lstat()
    assert stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)
    os.chmod(p, 0o555 if p.is_dir() else 0o444)
rows=[]
for p in paths:
    rel = p.relative_to(R).as_posix()
    info = p.lstat()
    row={'path':rel,'mode':oct(stat.S_IMODE(info.st_mode)),'mtime_ns':info.st_mtime_ns,
         'hidden':any(x.startswith('.') for x in Path(rel).parts if x!='.')}
    if p.is_dir():
        row.update(kind='directory',empty=not any(p.iterdir()))
    else:
        raw=p.read_bytes()
        row.update(kind='file',bytes=len(raw),empty=not raw)
        if rel in terminals:
            row['content_hash_exclusion']='Exact already-created terminal pair only'
        else:
            row['SHA256']=hashlib.sha256(raw).hexdigest()
    rows.append(row)
utc=datetime.fromtimestamp(freeze_ns/1_000_000_000,timezone.utc).isoformat()
manifest={'schema':'root-original-only-finite-initial-manifest-v1','scope':str(R),'freeze_UTC':utc,
          'files':18,'child_directories':1,'terminal_content_hash_exclusions_exact':sorted(terminals),'entries':rows}
seal={'schema':'root-original-only-INITIAL-seal-v1','scope':str(R),'freeze_UTC':utc,
      'record':23411227,'files':18,'child_directories':1,'review_completion_percent':35,
      'full388TeX_all5freshtext_all5ownrasters_nativeAPI_personally_read':True,
      'own_deductions':14,'support_primary_current_peer_bodies_unread':True,
      'scientific_program_executions':0,'scientific_verdict':None,
      'native196_21_unchanged':True,'files0444_directories0555':True,
      'INITIAL_SHA256':hashlib.sha256((R/'INITIAL.md').read_bytes()).hexdigest(),
      'manifest_SHA256':'0'*64,'checkpoint_before_scientific_continuation_pending':True,
      'programme_reviewed':145,'programme_total':203,'programme_complete':False}
encode=lambda x:(json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
for unused in range(20):
    mb=encode(manifest)
    seal['manifest_SHA256']=hashlib.sha256(mb).hexdigest()
    sb=encode(seal)
    lengths={'INITIAL_MANIFEST.json':len(mb),'INITIAL_SEAL.json':len(sb)}
    changed=False
    for row in rows:
        if row['path'] in terminals and (row['bytes']!=lengths[row['path']] or row['empty']):
            row['bytes']=lengths[row['path']]
            row['empty']=False
            changed=True
    if not changed:
        break
else:
    raise AssertionError('terminal byte-count fixed point')
for name,raw in [('INITIAL_MANIFEST.json',mb),('INITIAL_SEAL.json',sb)]:
    handles[name].write(raw)
    handles[name].flush()
    os.fsync(handles[name].fileno())
    handles[name].close()
    os.utime(R/name,ns=(freeze_ns,freeze_ns))
assert [R]+sorted(R.rglob('*')) == paths
for p,row in zip(paths,rows):
    info=p.lstat()
    assert oct(stat.S_IMODE(info.st_mode))==row['mode'] and info.st_mtime_ns==row['mtime_ns']
    if row['kind']=='file':
        raw=p.read_bytes()
        assert len(raw)==row['bytes'] and (not raw)==row['empty']
        if 'SHA256' in row:
            assert hashlib.sha256(raw).hexdigest()==row['SHA256']
    else:
        assert (not any(p.iterdir()))==row['empty']
assert hashlib.sha256((R/'INITIAL_MANIFEST.json').read_bytes()).hexdigest()==seal['manifest_SHA256']
print(json.dumps({'files':18,'childdirs':1,'review_percent':35,'freeze_UTC':utc,
                  'external_SHA256':{name:hashlib.sha256((R/name).read_bytes()).hexdigest() for name in sorted(terminals)}}))
