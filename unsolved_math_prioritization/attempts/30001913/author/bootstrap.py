"""Verify the complete flat author tree before executing any bundled test code.
Run only through the externally hash-pinned isolated launcher in the freeze receipt.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


def fail(message):
    raise SystemExit('REJECT: '+message)

if not sys.flags.isolated or not sys.flags.no_site:
    fail('Python -I -S is required')
if len(sys.argv)!=3:
    fail('expected root directory and external manifest')
root=Path(sys.argv[1])
manifest_path=Path(sys.argv[2])
if root.is_symlink() or not root.is_dir():
    fail('root is not a real directory')
manifest=json.loads(manifest_path.read_text())
if manifest.get('schema')!='hodge-extremality-author-v1' or manifest.get('problem_id')!=30001913:
    fail('wrong manifest schema or problem')
expected=manifest.get('files')
allowed={'README.md','RESULTS.md','APPROACHES.md','SOURCES.json','STATUS.json','verify.py','bootstrap.py','EXPECTED.json'}
if not isinstance(expected,dict) or set(expected)!=allowed:
    fail('manifest inventory mismatch')
actual=set()
for item in root.iterdir():
    mode=item.lstat().st_mode
    if not stat.S_ISREG(mode):
        fail('nonregular item: '+item.name)
    actual.add(item.name)
if actual!=allowed:
    fail('tree inventory mismatch')
for name,record in sorted(expected.items()):
    data=(root/name).read_bytes()
    if set(record)!={'bytes','sha256'} or len(data)!=record['bytes'] or hashlib.sha256(data).hexdigest()!=record['sha256']:
        fail('byte mismatch: '+name)
# No package code has been imported or executed before all checks passed.
code=(root/'verify.py').read_bytes()
exec(compile(code,str(root/'verify.py'),'exec'),{'__name__':'__main__','__file__':str(root/'verify.py')})
