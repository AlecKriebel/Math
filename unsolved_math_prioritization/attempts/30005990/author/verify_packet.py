#!/usr/bin/env python3
"""Verify flat source-free author packet against its externally bound manifest."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

def fail(msg):
    raise SystemExit('FAIL: '+msg)

root=Path(__file__).resolve().parent
manifest_path=root/'MANIFEST.json'
if manifest_path.is_symlink() or not manifest_path.is_file():
    fail('manifest missing or symlink')
manifest=json.loads(manifest_path.read_text())
entries=manifest.get('files')
if not isinstance(entries,list):
    fail('invalid entries')
names=[]
for item in entries:
    name=item.get('path')
    if not isinstance(name,str) or not name or '/' in name or '\\' in name or name in ('.','..','MANIFEST.json'):
        fail('invalid member name')
    names.append(name)
if len(names)!=len(set(names)):
    fail('duplicate members')
actual={p.name for p in root.iterdir()}
if actual!=set(names)|{'MANIFEST.json'}:
    fail('membership differs')
for p in root.iterdir():
    if p.is_symlink() or not p.is_file():
        fail('nonregular member '+p.name)
for item in entries:
    body=(root/item['path']).read_bytes()
    if len(body)!=item['bytes']:
        fail('byte count '+item['path'])
    if hashlib.sha256(body).hexdigest()!=item['sha256']:
        fail('hash '+item['path'])
if '--replay' in sys.argv:
    flags=['-I','-B']
    if sys.flags.optimize:
        flags.insert(1,'-O')
    result=subprocess.run([sys.executable,*flags,str(root/'check_math.py')],capture_output=True)
    if result.returncode or result.stdout!=(root/'check_results.json').read_bytes():
        fail('mathematical replay mismatch')
    if result.stderr:
        fail('unexpected mathematical replay stderr')
print(json.dumps({'status':'PASS','files':len(entries),'replayed':'--replay' in sys.argv},sort_keys=True))
