#!/usr/bin/env python3
"""Fail-closed verification of the complete release, including frozen subpackets."""
from pathlib import Path,PurePosixPath
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parent
manifest=root/'RELEASE_MANIFEST.json'
if manifest.is_symlink() or not manifest.is_file():raise SystemExit('Invalid release manifest')
m=json.loads(manifest.read_bytes());files=m['files'];expected=set(files)|{'RELEASE_MANIFEST.json'}
for name in files:
 p=PurePosixPath(name)
 if p.is_absolute() or any(x in ('','.','..') for x in p.parts) or p.as_posix()!=name:raise SystemExit('Unsafe manifest name')
expected_dirs={'author','audit'}
seen=set();dirs=set()
for p in root.rglob('*'):
 rel=p.relative_to(root).as_posix()
 if p.is_symlink():raise SystemExit('Symlink rejected: '+rel)
 if p.is_dir():dirs.add(rel)
 elif p.is_file():seen.add(rel)
 else:raise SystemExit('Nonregular entry rejected: '+rel)
if dirs!=expected_dirs:raise SystemExit('Unexpected/missing directories')
if seen!=expected:raise SystemExit('Unexpected/missing files')
for name,meta in files.items():
 b=(root/name).read_bytes()
 if len(b)!=meta['bytes'] or hashlib.sha256(b).hexdigest()!=meta['sha256']:raise SystemExit('Content mismatch: '+name)
for rel,want in [('author/SHA256SUMS.json','3327ea967f634bb8b57bba52dc46c29ffeaaec98ceeabf8fcaaba12d76cb2d60'),('audit/AUDIT_SHA256SUMS.json','50316f82ad4351d81cd1855bc97bb560425792488dd25f13b915ee4cfa1b7c18')]:
 if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=want:raise SystemExit('Frozen subpacket mismatch')
for args in [('audit/hardened_author_manifest.py','author'),('audit/verify_audit.py',)]:
 r=subprocess.run([sys.executable,'-B',*[str(root/a) for a in args]],capture_output=True)
 if r.returncode:raise SystemExit(r.stderr.decode()+r.stdout.decode())
print(json.dumps({'verified_files':len(files),'closed_allowlist':True,'frozen_author_and_audit_preserved':True},sort_keys=True))
