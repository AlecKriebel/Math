#!/usr/bin/env python3
"""Validate the literal authored manifest and separate seal; no inferred membership."""
import hashlib
import json
from pathlib import Path,PurePosixPath
import sys

class BundleError(Exception):
    pass

def require(ok,msg):
    if not ok:
        raise BundleError(msg)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    root=Path(__file__).resolve().parent
    raw=(root/'MANIFEST.json').read_bytes();manifest=json.loads(raw)
    require(set(manifest)=={'schema','self_excluded','files'},'manifest schema keys')
    require(manifest['schema']=='candidate_adversary_manifest_v1','manifest schema version')
    require(manifest['self_excluded']==['MANIFEST.json','SEAL.json'],'manifest self exclusion')
    require(isinstance(manifest['files'],list),'files must be a literal list')
    seen=set();total=0
    for row in manifest['files']:
        require(set(row)=={'relative_path','bytes','sha256'},'member row schema')
        name=row['relative_path'];rel=PurePosixPath(name)
        require(isinstance(name,str) and str(rel)==name and not rel.is_absolute() and '..' not in rel.parts and len(rel.parts)==1,'unsafe member path')
        require(name not in seen and name not in manifest['self_excluded'] and name!='_local','duplicate or excluded member')
        seen.add(name);path=root/name
        require(path.is_file() and not path.is_symlink(),'member missing or symlink')
        data=path.read_bytes()
        require(len(data)==row['bytes'] and digest(data)==row['sha256'],'member mismatch: '+name)
        total+=len(data)
    actual={p.name for p in root.iterdir() if p.is_file() and p.name not in manifest['self_excluded']}
    require(actual==seen,'unlisted authored top-level files or missing members')
    seal=json.loads((root/'SEAL.json').read_text())
    require(seal['schema']=='candidate_adversary_seal_v1','seal schema')
    require(seal['manifest_relative_path']=='MANIFEST.json' and seal['manifest_bytes']==len(raw) and seal['manifest_sha256']==digest(raw),'seal manifest mismatch')
    for name in ['REPORT.md','PROOF.md']:
        row=seal['key_outputs'][name];data=(root/name).read_bytes()
        require(row['bytes']==len(data) and row['sha256']==digest(data),'seal key-output mismatch')
    print(json.dumps({'status':'PASS','literal_manifest_members':len(seen),'member_bytes':total,'manifest_sha256':digest(raw),'private_scratch':'excluded','self_seal':'separate'},sort_keys=True,separators=(',',':')))

if __name__=='__main__':
    try:
        main()
    except (BundleError,OSError,ValueError,KeyError,TypeError) as error:
        print(json.dumps({'status':'FAIL','error':str(error)},sort_keys=True,separators=(',',':')))
        sys.exit(2)
