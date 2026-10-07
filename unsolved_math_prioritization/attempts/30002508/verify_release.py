#!/usr/bin/env python3
"""Strict final-layout and reproducibility verification; Python standard library."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
MANIFEST='MANIFEST.json'


def unique(pairs):
    d={}
    for k,v in pairs:
        if k in d:
            raise ValueError('duplicate JSON key: '+k)
        d[k]=v
    return d


def strict(root):
    m=json.loads((root/MANIFEST).read_text(),object_pairs_hook=unique)
    if set(m)!={'schema','files'} or m['schema']!=1 or not isinstance(m['files'],dict) or not m['files']:
        raise ValueError('invalid manifest schema')
    expected=m['files']
    for name,entry in expected.items():
        p=PurePosixPath(name)
        if not isinstance(name,str) or str(p)!=name or p.is_absolute() or any(s in ('','..','.') for s in p.parts) or name==MANIFEST:
            raise ValueError('unsafe or noncanonical manifest path')
        if set(entry)!={'sha256','bytes'} or not re.fullmatch('[0-9a-f]{64}',entry['sha256']) or type(entry['bytes']) is not int or entry['bytes']<0:
            raise ValueError('invalid file entry')
    actual=set()
    for p in root.rglob('*'):
        if p.is_symlink():
            raise ValueError('symlink rejected')
        if p.is_file():
            name=p.relative_to(root).as_posix()
            if name!=MANIFEST:
                actual.add(name)
    if actual!=set(expected):
        raise ValueError('missing or unexpected file')
    for name,e in expected.items():
        b=(root/name).read_bytes()
        if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:
            raise ValueError('byte/hash mismatch: '+name)
    return len(expected)


def check_sha_file(root,filename):
    lines=(root/filename).read_text().splitlines()
    if not lines:
        raise ValueError('empty nested manifest')
    seen=set()
    for line in lines:
        digest,name=line.split(maxsplit=1)
        if name in seen or not re.fullmatch('[0-9a-f]{64}',digest):
            raise ValueError('bad nested manifest')
        seen.add(name)
        p=PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or str(p)!=name:
            raise ValueError('unsafe nested manifest path')
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('nested manifest mismatch')
    return len(seen)


def negative_controls():
    names=['missing_file','extra_file','changed_bytes','empty_manifest','duplicate_key',
           'path_escape','invalid_digest','symlink']
    for case in names:
        with tempfile.TemporaryDirectory(prefix='nb-release-mutation-') as td:
            r=Path(td)/'packet'
            shutil.copytree(ROOT,r)
            m=json.loads((r/MANIFEST).read_text())
            target='author/README.md'
            if case=='missing_file': (r/target).unlink()
            elif case=='extra_file': (r/'unexpected.txt').write_text('extra')
            elif case=='changed_bytes': (r/target).write_bytes((r/target).read_bytes()+b'changed')
            elif case=='empty_manifest': m['files']={}
            elif case=='duplicate_key':
                raw=(r/MANIFEST).read_text()
                (r/MANIFEST).write_text(raw.replace('"schema": 1','"schema": 1, "schema": 1',1))
            elif case=='path_escape': m['files']['../escape.txt']=m['files'].pop(target)
            elif case=='invalid_digest': m['files'][target]['sha256']='invalid'
            elif case=='symlink':
                (r/target).unlink()
                (r/target).symlink_to('../RELEASE_ADDENDUM.md')
            if case in ('empty_manifest','path_escape','invalid_digest'):
                (r/MANIFEST).write_text(json.dumps(m,indent=2)+'\n')
            try:
                strict(r)
            except (ValueError,FileNotFoundError):
                pass
            else:
                raise AssertionError('mutation was accepted: '+case)
    return names


def main():
    count=strict(ROOT)
    author_count=check_sha_file(ROOT/'author','SHA256SUMS')
    audit_count=check_sha_file(ROOT/'audit','MANIFEST.sha256')
    for name in sorted((ROOT/'author').iterdir()):
        assert name.read_bytes()==(ROOT/'audit'/'frozen_inputs'/name.name).read_bytes()
    original_before=(ROOT/'author'/'control_results.json').read_bytes()
    independent_before=(ROOT/'audit'/'independent_results.json').read_bytes()
    for relative in ['author/verify_controls.py','audit/independent_controls.py']:
        subprocess.run([sys.executable,str(ROOT/relative)],check=True,capture_output=True,text=True)
    assert (ROOT/'author'/'control_results.json').read_bytes()==original_before
    assert (ROOT/'audit'/'independent_results.json').read_bytes()==independent_before
    a=json.loads(original_before); b=json.loads(independent_before)
    assert sum(x['rational_generator_tests'] for x in a['prime_witnesses'])==701
    assert b['replay_byte_identical'] and b['independent_mobius_identity_checks']==4000
    assert b['independent_generator_pairings']==3080 and b['independent_cutoff_annihilations']==2249
    assert b['independent_Riesz_function_tests']==234 and b['independent_divisor_inversion_checks']==800
    mutations=negative_controls()
    assert strict(ROOT)==count
    return {'status':'passed','target_status':'unsolved','manifest_files':count,
            'author_manifest_entries':author_count,'audit_manifest_entries':audit_count,
            'original_generator_tests':701,'independent_mobius_tests':4000,
            'independent_generator_pairings':3080,'independent_Riesz_tests':234,
            'independent_divisor_inversion_tests':800,'deterministic_replays':True,
            'manifest_mutations_rejected':mutations,
            'mathematical_scope':'partial results including endpoint continuity; full target unsolved'}

if __name__=='__main__': print(json.dumps(main(),indent=2))
