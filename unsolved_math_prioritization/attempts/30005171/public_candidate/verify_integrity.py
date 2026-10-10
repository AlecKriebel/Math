#!/usr/bin/env python3
"""Read-only exact inventory and mathematical replay, portable and -O safe."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={x['path']:x for x in manifest['files']}
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
if actual!=set(expected)|{'MANIFEST.json'}:
    raise SystemExit('FAIL: file inventory differs from manifest')
if any(p.is_symlink() for p in root.rglob('*')):
    raise SystemExit('FAIL: symlink in package')
for name,item in expected.items():
    data=(root/name).read_bytes()
    if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:
        raise SystemExit('FAIL: integrity mismatch: '+name)
result=subprocess.run([sys.executable,'-B',str(root/'verify_math.py')],check=True,
                      capture_output=True,text=True,cwd=root)
if json.loads(result.stdout)!=json.loads((root/'checks_result.json').read_text()):
    raise SystemExit('FAIL: mathematics replay differs from recorded result')
print(json.dumps({'status':'PASS','files_verified':len(expected),
                  'mathematical_replay':'PASS','scope':'unresolved, five approaches'},indent=2))
