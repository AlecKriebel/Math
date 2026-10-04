#!/usr/bin/env python3
"""Read-only complete private family check; author input pins remain dated.
Does not treat mutable author inputs as permanently frozen or approve publication.
"""
from pathlib import Path
import argparse, hashlib, json, stat
HERE=Path(__file__).resolve().parent
def pairs(items):
    out={}
    for k,v in items:
        if k in out: raise ValueError('duplicate JSON key '+k)
        out[k]=v
    return out
def require(ok,why):
    if not ok: raise ValueError(why)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--manifest-sha256',required=True)
    args=ap.parse_args(); path=HERE/'SELF_MANIFEST.json'; body=path.read_bytes()
    require(hashlib.sha256(body).hexdigest()==args.manifest_sha256,'whole manifest')
    require(stat.S_IMODE(path.lstat().st_mode)==0o444 and not path.is_symlink(),'manifest regular mode')
    mf=json.loads(body,object_pairs_hook=pairs)
    require(mf['schema']=='pr50-preprint-v1-adversary-self-only-closure/v1','schema')
    require(type(mf['files_count']) is int and mf['files_count']==len(mf['files']),'count')
    actual=sorted(HERE.rglob('*')); require(all(not p.is_symlink() for p in actual),'symlinks')
    require(all(p.is_file() or p.is_dir() for p in actual),'special-file scope')
    files=sorted(str(p.relative_to(HERE)) for p in actual if p.is_file())
    require(files==sorted([r['path'] for r in mf['files']]+['SELF_MANIFEST.json']),'exact whole file scope')
    dirs=sorted(str(p.relative_to(HERE)) for p in [HERE]+[p for p in actual if p.is_dir()])
    require(dirs==sorted(r['path'] for r in mf['directories']),'directory scope')
    for row in mf['files']:
        p=HERE/row['path']; info=p.lstat(); b=p.read_bytes()
        require(stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode)==0o444 and row['mode']=='0444','regular full mode')
        require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'whole body '+row['path'])
    for row in mf['directories']:
        p=HERE/row['path']; require(p.is_dir() and stat.S_IMODE(p.lstat().st_mode)==0o555 and row['mode']=='0555','directory full mode')
    print(json.dumps({'status':'PASS_COMPLETE_SELF_READBACK','files_count':mf['files_count'],
        'manifest_sha256':args.manifest_sha256,'author_inputs_are_dated_pins':True,
        'root_approval_claimed':False,'publication_claimed':False},indent=2))
if __name__=='__main__': main()
