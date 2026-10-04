#!/usr/bin/env python3
"""Exact root self only; foreign files are individually named and hashed."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath


def strict(root):
    def pairs(items):
        value={}
        for key,item in items:
            assert key not in value,'Duplicate key'
            value[key]=item
        return value
    manifest=root/'FIRST_PARTY_MANIFEST.json'
    assert manifest.is_file() and not manifest.is_symlink()
    obj=json.loads(manifest.read_bytes(),object_pairs_hook=pairs)
    assert obj['self_excluded']==['FIRST_PARTY_MANIFEST.json']
    assert obj['foreign_root']=='foreign_primary'
    names=set()
    for category in ['files','foreign_files']:
        for row in obj[category]:
            assert type(row) is dict and set(row)=={'path','size','sha256'}
            name=row['path'];path=PurePosixPath(name)
            assert type(name) is str and name and not path.is_absolute()
            assert path.as_posix()==name and not {'.','..'}.intersection(path.parts) and '\\' not in name
            assert name not in names and name!='FIRST_PARTY_MANIFEST.json'
            assert (path.parts[0]=='foreign_primary')==(category=='foreign_files')
            assert type(row['size']) is int and row['size']>=0
            assert type(row['sha256']) is str and len(row['sha256'])==64 and all(c in '0123456789abcdef' for c in row['sha256'])
            names.add(name)
            file=root/name
            assert file.is_file() and not file.is_symlink()
            data=file.read_bytes()
            assert len(data)==row['size'] and hashlib.sha256(data).hexdigest()==row['sha256']
    actual=set()
    for path in root.rglob('*'):
        assert not path.is_symlink(),'Symlink rejected'
        if path.is_file():actual.add(path.relative_to(root).as_posix())
        else:assert path.is_dir()
    assert actual==names|{'FIRST_PARTY_MANIFEST.json'},'Exact recursive closure differs'
    return {'status':'PASS_EXACT_ROOT_CLOSURE','first_party':len(obj['files']),'foreign_separately_bound':len(obj['foreign_files']),'self_only':True}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('root',type=Path);args=parser.parse_args()
    print(json.dumps(strict(args.root),indent=2))
