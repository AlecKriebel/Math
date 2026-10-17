#!/usr/bin/env python3
"""Fail-closed verification of the exact public file set and canonical manifest."""
import argparse
import hashlib
import json
import re
import stat
from pathlib import Path, PurePosixPath
ROOT=Path(__file__).resolve().parent

def require(ok,message):
    if not ok: raise RuntimeError(message)

def no_duplicate_keys(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'Duplicate JSON key: '+key)
        result[key]=value
    return result

def verify(expected=None):
    entries=list(ROOT.rglob('*'))
    require(all(not p.is_symlink() for p in entries),'Symlink in public payload')
    require(all(stat.S_ISREG(p.lstat().st_mode) or stat.S_ISDIR(p.lstat().st_mode) for p in entries),'Nonregular object in public payload')
    raw=(ROOT/'MANIFEST.json').read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if expected is not None: require(digest==expected,'External manifest pin mismatch')
    manifest=json.loads(raw,object_pairs_hook=no_duplicate_keys)
    require(raw==(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode(),'Noncanonical manifest encoding')
    require(manifest.get('schema')=='jones-public-manifest-v1','Wrong manifest schema')
    rows=manifest['files'];require(isinstance(rows,list),'Files must be a list')
    paths=[]
    for row in rows:
        require(set(row)=={'path','bytes','sha256'},'Unexpected file-entry fields')
        rel=row['path'];require(isinstance(rel,str),'Nonstring path')
        parts=PurePosixPath(rel)
        require(not parts.is_absolute() and '..' not in parts.parts and str(parts)==rel and '\\' not in rel and rel not in ('','.','MANIFEST.json'),'Unsafe or self-referential path')
        require(type(row['bytes']) is int and row['bytes']>=0,'Invalid byte count')
        require(isinstance(row['sha256'],str) and re.fullmatch('[0-9a-f]{64}',row['sha256']),'Invalid hash')
        p=ROOT/rel
        require(p.is_file() and not p.is_symlink(),'Missing file or symlink: '+rel)
        data=p.read_bytes()
        require(len(data)==row['bytes'],'Wrong byte count: '+rel)
        require(hashlib.sha256(data).hexdigest()==row['sha256'],'Wrong hash: '+rel)
        paths.append(rel)
    require(paths==sorted(set(paths)),'Unsorted or duplicate manifest paths')
    actual={p.relative_to(ROOT).as_posix() for p in entries if p.is_file()}
    allowed_dirs={str(parent) for rel in paths for parent in PurePosixPath(rel).parents if str(parent)!='.'}
    actual_dirs={p.relative_to(ROOT).as_posix() for p in entries if p.is_dir()}
    require(actual_dirs==allowed_dirs,'Unexpected or missing payload directory')
    require(actual==set(paths)|{'MANIFEST.json'},'Unexpected or unlisted payload files')
    identities=json.loads((ROOT/'ORIGINAL_IDENTITIES.json').read_bytes(),object_pairs_hook=no_duplicate_keys)['files']
    seen=set()
    for row in identities:
        require(row['path'] not in seen,'Duplicate original/public identity path')
        seen.add(row['path']);p=ROOT/row['path'];data=p.read_bytes()
        require(len(data)==row['public_bytes'] and hashlib.sha256(data).hexdigest()==row['public_sha256'],'Public-edition identity mismatch: '+row['path'])
        require(type(row['original_bytes']) is int and row['original_bytes']>=0 and re.fullmatch('[0-9a-f]{64}',row['original_sha256']),'Invalid original identity')
    lookup={r['path']:r for r in identities}
    bindings=json.loads((ROOT/'AUDIT_BINDINGS.json').read_bytes(),object_pairs_hook=no_duplicate_keys)['bindings']
    for binding in bindings:
        raw_audit=(ROOT/binding['historical_manifest']).read_bytes()
        require({'bytes':len(raw_audit),'sha256':hashlib.sha256(raw_audit).hexdigest()}==binding['manifest_identity'],'Historical audit manifest identity mismatch')
        for row in binding['rows']:
            if row['public_counterpart'] is None:continue
            source=lookup[row['public_counterpart']]
            require(all(row[k]==source[k] for k in ['original_bytes','original_sha256','public_bytes','public_sha256']),'Audit/public edition binding mismatch')
    return {'status':'PASS' ,'payload_file_count':len(paths)+1,'all_hashes_and_sizes_match':True,'exact_file_set':True,'canonical_manifest':True,'external_pin_checked':expected is not None,'manifest_sha256':digest}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--manifest-sha256')
    args=parser.parse_args();print(json.dumps(verify(args.manifest_sha256),sort_keys=True))
if __name__=='__main__':main()
