#!/usr/bin/env python3
"""Relocatable exact allowlist, hash verification, and both independent finite replays."""
from pathlib import Path,PurePosixPath
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parent
manifest=json.loads((root/'AUDIT_MANIFEST.json').read_text())
expected={row['path'] for row in manifest['files']}
if len(expected)!=len(manifest['files']):raise SystemExit('FAIL: duplicate manifest path')
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()}
if actual!=expected|{'AUDIT_MANIFEST.json'}:raise SystemExit('FAIL: exact allowlist: '+repr(actual^(expected|{'AUDIT_MANIFEST.json'})))
for row in manifest['files']:
    rel=PurePosixPath(row['path']);path=root/row['path']
    if rel.is_absolute() or '..' in rel.parts or any(part.is_symlink() for part in [path,*path.parents] if part!=root.parent):
        raise SystemExit('FAIL: unsafe path')
    b=path.read_bytes()
    if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:raise SystemExit('FAIL: bytes/hash '+row['path'])
meta=json.loads((root/'VERIFICATION_METADATA.json').read_text())
if hashlib.sha256((root/'author_freeze/MANIFEST.json').read_bytes()).hexdigest()!=meta['author_freeze']['manifest_sha256']:
    raise SystemExit('FAIL: original manifest identity')
res=subprocess.run([sys.executable,str(root/'author_freeze/verify_packet.py')],text=True,capture_output=True,check=True)
original=json.loads(res.stdout)
if original['finite_checks']!=22185 or original['packet']!='PASS':raise SystemExit('FAIL: author replay')
res=subprocess.run([sys.executable,str(root/'independent_checks.py')],text=True,capture_output=True,check=True)
fresh=json.loads(res.stdout)
if fresh!=json.loads((root/'INDEPENDENT_CHECK_RESULTS.json').read_text()):raise SystemExit('FAIL: independent replay')
if fresh['assertions']!=40249:raise SystemExit('FAIL: independent assertion count')
print(json.dumps({'audit_packet':'PASS','author_assertions':22185,'independent_assertions':40249,'mathematical_verdict':'NO RESOLUTION','conditional_theorem':'PASS with explanatory addendum','payload_files':len(manifest['files'])},sort_keys=True))
