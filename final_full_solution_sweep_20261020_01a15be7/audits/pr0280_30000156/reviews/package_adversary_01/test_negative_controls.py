#!/usr/bin/env python3
"""Disposable package mutation tests. Never modifies the bound/extracted evidence."""
from pathlib import Path
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import datetime

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'extracted' / 'birational-cycle-verification'
WORK = ROOT / 'negative_controls'
WORK.mkdir(exist_ok=True)

def manifest(root, transform):
    p=root/'MANIFEST.json'
    obj=json.loads(p.read_text())
    transform(obj)
    p.write_text(json.dumps(obj,indent=2)+'\n')

def change(root,name):
    p=root/name
    p.write_bytes(p.read_bytes()+b'\n')

cases={
 'schema_true':lambda r: manifest(r,lambda m:m.update(schema=True)),
 'schema_float':lambda r: manifest(r,lambda m:m.update(schema=1.0)),
 'schema_two':lambda r: manifest(r,lambda m:m.update(schema=2)),
 'schema_extra':lambda r: manifest(r,lambda m:m.update(extra=1)),
 'bytes_boolean':lambda r:manifest(r,lambda m:m['files'][0].update(bytes=True)),
 'bytes_float':lambda r:manifest(r,lambda m:m['files'][0].update(bytes=float(m['files'][0]['bytes']))),
 'duplicate_member':lambda r:manifest(r,lambda m:m['files'].append(copy.deepcopy(m['files'][0]))),
 'path_parent':lambda r:manifest(r,lambda m:m['files'][0].update(path='../outside')),
 'path_absolute':lambda r:manifest(r,lambda m:m['files'][0].update(path='/outside')),
 'path_backslash':lambda r:manifest(r,lambda m:m['files'][0].update(path='x\\y')),
 'proof_modified':lambda r:change(r,'paper/main.tex'),
 'checker_modified':lambda r:change(r,'check_math.py'),
 'expected_modified':lambda r:change(r,'expected_checks.json'),
 'file_extra':lambda r:(r/'EXTRA').write_text('unexpected\n'),
 'file_missing':lambda r:(r/'LICENSE.txt').unlink(),
 'file_symlink':lambda r:((r/'LICENSE.txt').unlink(),(r/'LICENSE.txt').symlink_to('../outside')),
 'directory_symlink':lambda r:(r/'EXTRA').symlink_to('/tmp',target_is_directory=True),
 'manifest_symlink':lambda r:((r/'MANIFEST.json').rename(r/'other-manifest.json'),(r/'MANIFEST.json').symlink_to('other-manifest.json')),
}
rows=[]
for name,mutate in cases.items():
    target=WORK/name
    if target.exists():shutil.rmtree(target)
    shutil.copytree(SOURCE,target)
    mutate(target)
    for mode in ('normal','optimized'):
        cmd=[sys.executable]
        if mode=='optimized':cmd.append('-O')
        cmd+=['-B',str(target/'verify.py')]
        p=subprocess.run(cmd,capture_output=True,text=True)
        rows.append({'case':name,'mode':mode,'expected':'reject','returncode':p.returncode,
                     'rejected':p.returncode!=0,'stdout':p.stdout,'stderr_tail':p.stderr[-1000:]})
for mode in ('normal','optimized'):
    cmd=[sys.executable]+(['-O'] if mode=='optimized' else [])+['-B',str(SOURCE/'verify.py'),'--limit','3']
    p=subprocess.run(cmd,capture_output=True,text=True)
    rows.append({'case':'command_line_override','mode':mode,'expected':'reject','returncode':p.returncode,
                 'rejected':p.returncode!=0,'stdout':p.stdout,'stderr_tail':p.stderr[-1000:]})
out={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,
     'attempts':len(rows),'rejected':sum(r['rejected'] for r in rows),
     'unexpected_acceptances':[{'case':r['case'],'mode':r['mode']} for r in rows if not r['rejected']],
     'results':rows}
(ROOT/'NEGATIVE_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
