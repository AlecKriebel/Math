#!/usr/bin/env python3
"""Strict authored-packet verifier with adversarial file-set controls."""
from pathlib import Path
import hashlib
import json
import shutil
import tempfile
import sys

def verify(root):
    root=Path(root)
    manifest=root/'AUTHOR_MANIFEST.json'
    if manifest.is_symlink() or not manifest.is_file():
        raise ValueError('Missing or symlink manifest')
    data=json.loads(manifest.read_text())
    records=data['files']
    expected=set()
    for item in records:
        name=item['path']
        p=Path(name)
        if p.is_absolute() or '..' in p.parts or len(p.parts)!=1 or name in expected or name=='AUTHOR_MANIFEST.json':
            raise ValueError('Unsafe or duplicate path')
        expected.add(name)
        file=root/p
        if file.is_symlink() or not file.is_file():
            raise ValueError('Missing file or symlink')
        raw=file.read_bytes()
        if len(raw)!=item['bytes'] or hashlib.sha256(raw).hexdigest()!=item['sha256']:
            raise ValueError('Hash or size mismatch')
    actual=set()
    for item in root.iterdir():
        if item.name=='AUTHOR_MANIFEST.json':
            continue
        if item.is_symlink() or not item.is_file():
            raise ValueError('Extra directory, special entry, or symlink')
        actual.add(item.name)
    if actual!=expected:
        raise ValueError('Unexpected file set')
    return len(expected)

def self_test(root):
    cases=[]
    for mode in ('changed','missing','extra','nested-extra','symlink','traversal'):
        with tempfile.TemporaryDirectory() as tmp:
            copy=Path(tmp)/'packet'
            shutil.copytree(root,copy)
            target=copy/'README.md'
            if mode=='changed': target.write_bytes(target.read_bytes()+b'changed')
            elif mode=='missing': target.unlink()
            elif mode=='extra': (copy/'extra.txt').write_text('extra')
            elif mode=='nested-extra': (copy/'nested').mkdir(); (copy/'nested'/'extra.txt').write_text('extra')
            elif mode=='symlink': target.unlink(); target.symlink_to(copy/'SOURCE_SCOPE.md')
            elif mode=='traversal':
                p=copy/'AUTHOR_MANIFEST.json'; m=json.loads(p.read_text());m['files'][0]['path']='../escape';p.write_text(json.dumps(m))
            try: verify(copy)
            except (ValueError,OSError): cases.append(mode)
            else: raise RuntimeError('Failed to reject '+mode)
    return cases

if __name__=='__main__':
    root=Path(__file__).resolve().parent
    result={'outcome':'PASS','verified_payload_files':verify(root)}
    if '--self-test' in sys.argv:
        result['rejected_negative_controls']=self_test(root)
    print(json.dumps(result,indent=2,sort_keys=True))
