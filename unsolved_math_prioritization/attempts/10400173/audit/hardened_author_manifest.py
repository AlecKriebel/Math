#!/usr/bin/env python3
"""Read-only, fail-closed check of the separately supplied frozen author packet."""
from pathlib import Path
import argparse,hashlib,json
EXPECTED_MANIFEST='3327ea967f634bb8b57bba52dc46c29ffeaaec98ceeabf8fcaaba12d76cb2d60'
EXPECTED_NOTE='043b210954b19fdbe23b5377f0b2d79c9c46bea53de4a0e055ca5f7922140eb3'
p=argparse.ArgumentParser();p.add_argument('author_packet',type=Path);args=p.parse_args()
root=args.author_packet
manifest_path=root/'SHA256SUMS.json'
if manifest_path.is_symlink() or not manifest_path.is_file():raise SystemExit('Invalid manifest type')
b=manifest_path.read_bytes()
if hashlib.sha256(b).hexdigest()!=EXPECTED_MANIFEST:raise SystemExit('Frozen author manifest hash mismatch')
m=json.loads(b);files=m['files']
expected=set(files)|{'SHA256SUMS.json'}
entries=list(root.iterdir())
if any(e.is_symlink() or not e.is_file() for e in entries):raise SystemExit('Unexpected directory, symlink, or non-regular entry')
if {e.name for e in entries}!=expected:raise SystemExit('Unexpected/missing top-level entries')
for name,meta in files.items():
 if Path(name).name!=name or name in ('','.','..'):raise SystemExit('Invalid filename')
 b=(root/name).read_bytes()
 if len(b)!=meta['bytes'] or hashlib.sha256(b).hexdigest()!=meta['sha256']:raise SystemExit('Content mismatch: '+name)
if hashlib.sha256((root/'RESEARCH_NOTE.md').read_bytes()).hexdigest()!=EXPECTED_NOTE:raise SystemExit('Frozen note mismatch')
print(json.dumps({'verified_files':len(files),'manifest_sha256':EXPECTED_MANIFEST,'note_sha256':EXPECTED_NOTE,'closed_allowlist':True},sort_keys=True))
