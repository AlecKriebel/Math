#!/usr/bin/env python3
"""Strict integrity checks for this accepted packet; no external writes or imports."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re

RELEASE='7757ebce031bfb509cfddd0bef7ef79cff0e6ddd7a6047728a491eebd72b237f'
SUPPLEMENT='45878d297c6c6690b864bb00512a3b48fb708b6172331132ec5d52a4f29dafa6'
AUTHOR='cb1e6bc97269b5d4224bbe9dd8718b860c6764b1db1e60751bb93d072875438f'
ORIGINAL_AUTHOR='2d657668c7f2b47f4429714e3e597baee441f32f58f262dc7bfb9d62dc5b4d8d'
ORIGINAL_AUDIT='c7ef85a28c07d72abc9e2fa2cbbba309d385b31077c58325a0fdcaa2e5350d08'

def require(value, message):
    if not value: raise ValueError(message)

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def safe_name(name):
    path=PurePosixPath(name)
    require(bool(name) and not path.is_absolute() and '\\' not in name and
            all(p not in ('','.','..') for p in name.split('/')) and ':' not in name,
            'Unsafe relative path')
    return path

def inventory(root):
    require(root.is_dir() and not root.is_symlink(),'Unsafe root')
    files=set(); dirs=set()
    for p in root.rglob('*'):
        require(not p.is_symlink(),'Symlink rejected')
        name=p.relative_to(root).as_posix();safe_name(name)
        if p.is_file():files.add(name)
        elif p.is_dir():dirs.add(name)
        else:raise ValueError('Nonregular entry')
    return files,dirs

def check_entries(root, entries, manifest_name, closed):
    for name,h in entries.items():
        safe_name(name)
        require(re.fullmatch(r'[0-9a-f]{64}',h) is not None,'Bad digest')
        p=root/name
        require(p.is_file() and not p.is_symlink(),'Missing or unsafe file')
        require(digest(p)==h,'File hash mismatch: '+name)
    files,dirs=inventory(root)
    if closed:
        expected=set(entries)|{manifest_name}
        require(files==expected,'Unlisted or omitted files')
        expected_dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'}
        require(dirs==expected_dirs,'Unlisted or omitted directories')

def check_manifest(root, expected_hash=None, name='SHA256SUMS', closed=True):
    raw=(root/name).read_bytes()
    if expected_hash is not None:
        require(hashlib.sha256(raw).hexdigest()==expected_hash,'Manifest binding mismatch')
    entries={}
    for line in raw.decode('utf-8').splitlines():
        match=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
        require(match is not None,'Malformed manifest line')
        h,path=match.groups();safe_name(path)
        require(path not in entries,'Duplicate manifest path')
        require(path!=name,'Self-reference in manifest')
        entries[path]=h
    require(bool(entries),'Empty manifest')
    check_entries(root,entries,name,closed)
    return len(entries)

def verify(root):
    outer=json.loads((root/'PUBLICATION_MANIFEST.json').read_text())
    require(outer['id']==30001687 and outer['status']=='unsolved','Wrong identity')
    check_entries(root,outer['files'],'PUBLICATION_MANIFEST.json',True)
    counts={
        'release_bound_files':check_manifest(root/'release',RELEASE),
        'supplement_bound_files':check_manifest(root/'release-review',SUPPLEMENT),
        'corrected_author_files':check_manifest(root/'release',AUTHOR,'AUTHOR_SHA256SUMS',False),
        'original_author_files':check_manifest(root/'release/original_author',ORIGINAL_AUTHOR),
        'original_audit_files':check_manifest(root/'release/audit/original',ORIGINAL_AUDIT)}
    require(counts=={'release_bound_files':27,'supplement_bound_files':4,'corrected_author_files':7,'original_author_files':7,'original_audit_files':7},'Unexpected manifest counts')
    r=json.loads((root/'release/RESULT.json').read_text())
    require(r['id']==30001687 and r['status']=='unsolved' and r['substantive_routes']==5,'Wrong result')
    require(r['full_resolution'] is False and r['novelty_claim'] is False,'Unsupported claim')
    require(r['controls']['infinite_spectrum_certified'] is False,'Unsupported certification')
    return {'status':'PASS','publication_files':len(outer['files'])+1,**counts}

if __name__=='__main__':
    print(json.dumps(verify(Path(__file__).resolve().parent),indent=2))
