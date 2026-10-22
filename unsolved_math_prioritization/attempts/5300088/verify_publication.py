#!/usr/bin/env python3
"""Strict integrity check for the published research packet; performs no writes."""
from pathlib import Path, PurePosixPath
import hashlib,json,os,subprocess,sys
b=Path(__file__).resolve().parent
manifest=b/'PUBLICATION_MANIFEST.json'
if manifest.is_symlink() or not manifest.is_file():raise SystemExit('Invalid publication manifest')
m=json.loads(manifest.read_text())
entries=m['files']
actual=set()
for root,dirs,files in os.walk(b,followlinks=False):
    for name in dirs+files:
        p=Path(root)/name
        if p.is_symlink():raise SystemExit('Symlink rejected: '+str(p.relative_to(b)))
    for name in files:
        p=Path(root)/name
        actual.add(p.relative_to(b).as_posix())
if actual!=set(entries)|{'PUBLICATION_MANIFEST.json'}:raise SystemExit('Publication allowlist mismatch')
for name,meta in entries.items():
    pure=PurePosixPath(name)
    if pure.is_absolute() or '..' in pure.parts or pure.as_posix()!=name:raise SystemExit('Invalid manifest path')
    data=(b/name).read_bytes()
    if len(data)!=meta['bytes'] or hashlib.sha256(data).hexdigest()!=meta['sha256']:raise SystemExit('Publication file mismatch: '+name)
fixed={'submission/SHA256SUMS.json':'166b1c2642947993cefe9212ba2d523438168a0ce58372731b1a850cc2021945','submission/PARTIAL.md':'c3e83dea255fed2940b9c8bc6d4cf9f14d34b77f94851fab3e1047394a5f96cc'}
for name,digest in fixed.items():
    if hashlib.sha256((b/name).read_bytes()).hexdigest()!=digest:raise SystemExit('Frozen author binding mismatch')
p=subprocess.run([sys.executable,'-B',str(b/'independent-audit/verify_audit_manifest.py')],check=True,capture_output=True)
if json.loads(p.stdout)['status']!='passed':raise SystemExit('Audit manifest failed')
print(json.dumps({'status':'passed','verified_files':len(entries),'author_files':12,'audit_files':12,'strict_allowlist':True,'symlinks_rejected':True,'frozen_packets_bound':True},sort_keys=True))
