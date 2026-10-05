#!/usr/bin/env python3
"""Execute actual corruptions in disposable copies; explicit checks survive -O."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('publication',Path(__file__).with_name('verify_publication.py'))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

def change_manifest(root, mutate):
    p = root/v.MANIFEST
    data = json.loads(p.read_text())
    mutate(data)
    p.write_text(json.dumps(data))

def rehash(root,name):
    raw = (root/name).read_bytes()
    change_manifest(root,lambda m:[row.update(bytes=len(raw),sha256=v.digest(raw)) for row in m['files'] if row['path']==name])

def rehashed_anchor(root):
    p = root/'author/safe/MANIFEST.json'
    p.write_bytes(p.read_bytes()+b' ')
    rehash(root,'author/safe/MANIFEST.json')

def altered_scope(root):
    p = root/'PUBLICATION_STATUS.json'
    d = json.loads(p.read_text()); d['global_uniqueness_proved'] = True
    p.write_text(json.dumps(d))
    rehash(root,'PUBLICATION_STATUS.json')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root',type=Path)
    ap.add_argument('expected_manifest_sha256')
    args = ap.parse_args()
    root = args.root.resolve()
    v.verify(root,args.expected_manifest_sha256)
    cases = [
        ('changed_proof',lambda p:(p/'author/safe/TURN_5_GENERALIZED_ROUNDING.md').write_bytes(b'changed'),False),
        ('missing_audit',lambda p:(p/'independent_audit/AUDIT.md').unlink(),False),
        ('extra_file',lambda p:(p/'extra.txt').write_text('extra'),False),
        ('extra_directory',lambda p:(p/'unexpected').mkdir(),False),
        ('source_like_intrusion',lambda p:(p/'source.pdf').write_bytes(b'%PDF synthetic'),False),
        ('payload_symlink',lambda p:((p/'README.md').unlink(),(p/'README.md').symlink_to('PUBLICATION_STATUS.json')),False),
        ('directory_symlink',lambda p:(p/'link').symlink_to('.',target_is_directory=True),False),
        ('manifest_symlink',lambda p:((p/v.MANIFEST).unlink(),(p/v.MANIFEST).symlink_to('PUBLICATION_STATUS.json')),False),
        ('changed_external_manifest',lambda p:(p/v.MANIFEST).write_bytes((p/v.MANIFEST).read_bytes()+b' '),False),
        ('duplicate_manifest_path',lambda p:change_manifest(p,lambda m:m['files'].append(m['files'][0].copy())),True),
        ('parent_path',lambda p:change_manifest(p,lambda m:m['files'][0].update(path='../escape')),True),
        ('absolute_path',lambda p:change_manifest(p,lambda m:m['files'][0].update(path='/escape')),True),
        ('boolean_byte_count',lambda p:change_manifest(p,lambda m:m['files'][0].update(bytes=True)),True),
        ('duplicate_json_key',lambda p:(p/v.MANIFEST).write_text('{"files":[],"files":[]}'),True),
        ('frozen_manifest_rehashed_outside',rehashed_anchor,True),
        ('unsupported_global_claim_rehashed_outside',altered_scope,True),
        ('truncated_archive',lambda p:(p/'author/DIRICHLET_ZERO_30002507_AUTHOR_FREEZE.zip').write_bytes(b'PK'),False),
    ]
    results = {}
    for label,mutate,reanchor in cases:
        with tempfile.TemporaryDirectory(prefix='dirichlet-publication-corruption-') as tmp:
            copied = Path(tmp)/'package'; shutil.copytree(root,copied)
            mutate(copied)
            anchor = v.digest((copied/v.MANIFEST).read_bytes()) if reanchor else args.expected_manifest_sha256
            try:
                v.verify(copied,anchor)
            except (ValueError,OSError,KeyError):
                results[label] = 'rejected'
            else:
                raise ValueError('Corruption incorrectly accepted: '+label)
    with tempfile.TemporaryDirectory(prefix='dirichlet-root-symlink-') as tmp:
        link = Path(tmp)/'link'; link.symlink_to(root,target_is_directory=True)
        try:
            v.verify(link,args.expected_manifest_sha256)
        except ValueError:
            results['root_symlink'] = 'rejected'
        else:
            raise ValueError('Root symlink incorrectly accepted')
    v.verify(root,args.expected_manifest_sha256)
    print(json.dumps({'result':'PASS','intact':'accepted','negative_cases':len(results),'cases':results,'scope':'Executed integrity corruptions only; not a mathematical proof checker.'},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
