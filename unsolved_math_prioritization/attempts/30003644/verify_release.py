#!/usr/bin/env python3
"""Check exact publication layout, strict manifests, and all audited replays."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def sha(data): return hashlib.sha256(data).hexdigest()

def parse_manifest(text):
    out={}
    for line in text.splitlines():
        m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
        if not m: raise ValueError('malformed manifest entry')
        digest,name=m.groups();path=PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or '.' in path.parts or '\\' in name or str(path)!=name:
            raise ValueError('unsafe or noncanonical path')
        if name in out: raise ValueError('duplicate manifest entry')
        out[name]=digest
    if not out: raise ValueError('empty manifest')
    return out

def check_manifest(root,name,expected=None):
    items=parse_manifest((root/name).read_text())
    if expected is not None and set(items)!=set(expected):raise ValueError('inventory mismatch')
    for path,digest in items.items():
        f=root/path
        if not f.is_file() or f.is_symlink() or sha(f.read_bytes())!=digest:
            raise ValueError('missing, symlinked, or changed artifact: '+path)
    return items

def integrity(root):
    files={str(p.relative_to(root)) for p in root.rglob('*')
           if p.is_file() and '__pycache__' not in p.parts}
    if any(p.is_symlink() for p in root.rglob('*')):raise ValueError('symlink in release')
    release=check_manifest(root,'RELEASE_SHA256SUMS',files-{'RELEASE_SHA256SUMS'})
    portable=check_manifest(root,'SHA256SUMS')
    binding=json.loads((root/'RELEASE_BINDING.json').read_text())
    if len(portable)!=23 or len(files)!=28:raise ValueError('unexpected artifact count')
    if set(portable)!={p for p in files if p.startswith(('frozen/','audit/'))}:raise ValueError('portable inventory mismatch')
    for name,meta in binding['portable_files'].items():
        data=(root/name).read_bytes()
        if len(data)!=meta['bytes'] or sha(data)!=meta['sha256']:raise ValueError('binding mismatch')
    if set(binding['portable_files'])!=set(portable)|{'SHA256SUMS'}:raise ValueError('binding inventory mismatch')
    authored=check_manifest(root/'frozen','SHA256SUMS')
    if set(authored)!={p[7:] for p in portable if p.startswith('frozen/')} - {'SHA256SUMS'}:
        raise ValueError('authored inventory mismatch')
    audit=json.loads((root/'audit/AUDIT_MANIFEST.json').read_text())
    if set(audit['entries'])!=set(portable)-{'audit/AUDIT_MANIFEST.json'}:raise ValueError('audit inventory mismatch')
    for name,meta in audit['entries'].items():
        data=(root/name).read_bytes()
        if len(data)!=meta['bytes'] or sha(data)!=meta['sha256']:raise ValueError('audit hash/size mismatch')
    if audit['binds_frozen_manifest_sha256']!=sha((root/'frozen/SHA256SUMS').read_bytes()):
        raise ValueError('frozen binding mismatch')
    return len(files)

def negative_controls():
    rejected=0
    for bad in ['', 'x  test', 'a'*64+'  ../escape', 'a'*64+'  /absolute',
                ('a'*64+'  same\n')*2, 'a'*64+'  a//b', 'a'*64+'  a\\b']:
        try:parse_manifest(bad)
        except ValueError:rejected+=1
        else:raise AssertionError('accepted malformed manifest')
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp);(p/'data').write_bytes(b'expected');(p/'manifest').write_text(sha(b'expected')+'  data\n')
        check_manifest(p,'manifest',{'data'})
        for kind in ['extra-inventory','tampered','missing']:
            try:
                if kind=='extra-inventory':check_manifest(p,'manifest',{'data','extra'})
                elif kind=='tampered':
                    (p/'data').write_bytes(b'changed');check_manifest(p,'manifest',{'data'})
                else:
                    (p/'data').unlink();check_manifest(p,'manifest',{'data'})
            except ValueError:rejected+=1
            else:raise AssertionError('accepted bad artifact state')
    assert rejected==10
    return rejected

def replay():
    runs=[('frozen/verify_controls.py','frozen/control_results.json'),
          ('audit/verify_independent.py','audit/independent_results.json'),
          ('audit/test_adversarial.py','audit/adversarial_results.json')]
    for script,expected in runs:
        actual=subprocess.check_output([sys.executable,str(ROOT/script)],cwd=ROOT,env=None)
        if actual!=(ROOT/expected).read_bytes():raise ValueError('replay differs: '+script)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.check_call([sys.executable,str(ROOT/'audit/export_leaves.py'),str(ROOT/'frozen'),tmp],stdout=subprocess.DEVNULL)
        for name in ['target_leaves.jsonl','negative_leaves.jsonl']:
            if (Path(tmp)/name).read_bytes()!=(ROOT/'audit'/name).read_bytes():raise ValueError('leaf export differs')
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--integrity-only',action='store_true');a=p.parse_args()
    count=integrity(ROOT);neg=negative_controls()
    replayed=False if a.integrity_only else replay()
    assert integrity(ROOT)==count
    print(json.dumps({'files':count,'strict_manifest_negative_controls':neg,'all_nested_manifests':'PASS',
                      'original_independent_adversarial_replays_byte_identical':replayed,
                      'exact_leaf_reexport_byte_identical':replayed,
                      'status':'unsolved','turns':5,'scope':'Only |t|<=10000 is computationally zero-free; Schanuel conclusion remains conditional.'},indent=2,sort_keys=True))

if __name__=='__main__':main()
