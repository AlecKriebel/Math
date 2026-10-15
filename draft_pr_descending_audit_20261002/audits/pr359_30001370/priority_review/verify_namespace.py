#!/usr/bin/env python3
"""Portable, read-only sealed-namespace verifier. Use python3 -B.

No imports of local modules, executions of captured commands, downloads or writes.
Full mode verifies private payloads. --public-only verifies the distributable layer
and explicitly reports that private bytes were not checked.
"""
import argparse,hashlib,json
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def safe(root,rel):
    p=Path(rel)
    if p.is_absolute() or '..' in p.parts or p.as_posix()!=rel:
        raise ValueError('unsafe manifest path: '+rel)
    q=root/p
    if q.is_symlink() or not q.resolve().is_relative_to(root.resolve()):
        raise ValueError('symlink or out-of-root path: '+rel)
    return q
def check(root,e):
    p=safe(root,e['path'])
    if not p.is_file():raise ValueError('missing file: '+e['path'])
    b=p.read_bytes()
    if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:
        raise ValueError('identity mismatch: '+e['path'])

ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--public-only',action='store_true');args=ap.parse_args()
root=args.root.resolve()
closure=read(root/'CLOSURE.json')
for key,name in [('public_manifest','PUBLIC_MANIFEST.json'),('private_manifest','PRIVATE_MANIFEST.json')]:
    check(root,{'path':name,**closure[key]})
pub=read(root/'PUBLIC_MANIFEST.json');prv=read(root/'PRIVATE_MANIFEST.json')
for e in pub['files']:check(root,e)
if not args.public_only:
    for e in prv['files']:check(root,e)
expected={e['path'] for e in pub['files']}|{'PUBLIC_MANIFEST.json','PRIVATE_MANIFEST.json','CLOSURE.json'}
if not args.public_only:expected|={e['path'] for e in prv['files']}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and (not args.public_only or 'private' not in p.relative_to(root).parts)}
if expected!=actual:
    raise ValueError('inventory mismatch: extra='+repr(sorted(actual-expected))+' missing='+repr(sorted(expected-actual)))
if not args.public_only:
    actual_dirs={str(p.relative_to(root)) for p in root.rglob('*') if p.is_dir()}
    if actual_dirs!=set(prv['directories']):raise ValueError('directory inventory mismatch')
baseline=read(root/'BASELINE_SEAL.json')
check(root,baseline['baseline'])
if not args.public_only and sha(root/'private/receipts/input_copies.json')!=baseline['input_receipt_sha256']:
    raise ValueError('baseline input receipt changed')
# Process receipts point to retained complete stdout/stderr/payload bytes.
if not args.public_only:
    def walk(obj):
        if isinstance(obj,dict):
            if set(('path','bytes','sha256')).issubset(obj):check(root,obj)
            for v in obj.values():walk(v)
        elif isinstance(obj,list):
            for v in obj:walk(v)
    for p in (root/'private/receipts').glob('*.json'):walk(read(p))
print(json.dumps({'status':'PASS','head':closure['candidate_head'],'baseline_sha256':baseline['baseline']['sha256'],'public_files':len(pub['files']),'private_files_checked':0 if args.public_only else len(prv['files']),'closure_sha256':sha(root/'CLOSURE.json'),'mode':'public_only_private_unchecked' if args.public_only else 'full_public_and_private','read_only':True},indent=2))
