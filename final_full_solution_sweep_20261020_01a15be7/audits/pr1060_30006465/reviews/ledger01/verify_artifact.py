#!/usr/bin/env python3
"""Read-only offline identity/closed-inventory verifier, not a mathematical prover."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat

PUBLIC_FILES={'.gitignore','CHECK_RESULTS.json','RESEARCH_LOG.md','REVIEW.md','verify_artifact.py'}
HEX=re.compile(r'[0-9a-f]{64}')

def require(ok, why):
    if not ok: raise ValueError(why)

def pairs(items):
    obj={}
    for k,v in items:
        require(k not in obj,'Duplicate JSON key')
        obj[k]=v
    return obj

def strict(path):
    def constant(_): raise ValueError('Nonfinite JSON')
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=pairs,parse_constant=constant)

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def safe(name):
    require(type(name) is str and bool(name) and '\\' not in name,'Invalid path')
    p=PurePosixPath(name)
    require(not p.is_absolute() and name==p.as_posix() and all(x not in ('','.','..') for x in p.parts),'Unsafe path')
    return p

def inventory(root):
    files=set();dirs=set()
    require(stat.S_ISDIR(root.lstat().st_mode),'Root is not a real directory')
    for here,subdirs,names in os.walk(root,followlinks=False):
        for name in subdirs:
            p=Path(here)/name;require(stat.S_ISDIR(p.lstat().st_mode),'Non-directory or directory symlink')
            dirs.add(p.relative_to(root).as_posix())
        for name in names:
            p=Path(here)/name;require(stat.S_ISREG(p.lstat().st_mode),'Non-regular or file symlink')
            files.add(p.relative_to(root).as_posix())
    return files,dirs

def verify_manifest(root,basename,expected_files=None):
    manifest=root/(basename+'.json');seal=root/(basename+'.sha256')
    mf=root/(basename+'.json');sf=root/(basename+'.sha256')
    for q in (mf,sf): require(stat.S_ISREG(q.lstat().st_mode),'Manifest/seal must be regular')
    require(seal.read_text()==digest(manifest)+'  '+basename+'.json\n','Manifest seal mismatch')
    m=strict(manifest)
    require(type(m) is dict and set(m)=={'schema','files','directories'},'Manifest schema')
    require(type(m['schema']) is int and m['schema']==1,'Manifest version')
    require(type(m['files']) is list and type(m['directories']) is list,'Manifest arrays')
    paths=set()
    for e in m['files']:
        require(type(e) is dict and set(e)=={'path','bytes','sha256'},'File entry schema')
        safe(e['path']);require(e['path'] not in paths,'Duplicate file path');paths.add(e['path'])
        require(type(e['bytes']) is int and e['bytes']>=0,'Byte count must be nonnegative integer')
        require(type(e['sha256']) is str and HEX.fullmatch(e['sha256']) is not None,'SHA format')
        q=root/e['path'];require(stat.S_ISREG(q.lstat().st_mode),'Pinned file must be regular')
        require(q.stat().st_size==e['bytes'] and digest(q)==e['sha256'],'Pinned file bytes differ: '+e['path'])
    dirs=set()
    for name in m['directories']:
        safe(name);require(name not in dirs,'Duplicate directory');dirs.add(name)
    require(not paths.intersection(dirs),'File-directory overlap')
    if expected_files is not None:require(paths==expected_files,'Public member allowlist mismatch')
    files,actual_dirs=inventory(root)
    if expected_files is None:
        require(files==paths|{basename+'.json',basename+'.sha256'} and actual_dirs==dirs,'Private closed inventory mismatch')
    else:
        require({x for x in files if not x.startswith('private/')}==paths|{basename+'.json',basename+'.sha256'},'Public closed inventory mismatch')
        require({x for x in actual_dirs if x!='private' and not x.startswith('private/')}==dirs,'Public directory mismatch')
    return m

def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',nargs='?',default=str(Path(__file__).parent));ap.add_argument('--private',action='store_true');args=ap.parse_args()
    root=Path(args.root)
    m=verify_manifest(root,'OUTPUT_MANIFEST',PUBLIC_FILES)
    check=strict(root/'CHECK_RESULTS.json')
    require(type(check) is dict and check.get('ready_for_existing_publication_record') is True,'Review is not acceptance')
    seal=check['private_seal'];require(type(seal) is dict and set(seal)=={'manifest_sha256','files','directories'},'Private anchor schema')
    require(type(seal['manifest_sha256']) is str and HEX.fullmatch(seal['manifest_sha256']) is not None,'Private anchor SHA')
    require(type(seal['files']) is int and type(seal['directories']) is int and seal['files']>=0 and seal['directories']>=0,'Private anchor counts')
    result={'public_verified':True,'public_files':len(m['files']),'private_verified':False}
    if args.private:
        p=root/'private';pm=verify_manifest(p,'PRIVATE_MANIFEST')
        require(digest(p/'PRIVATE_MANIFEST.json')==seal['manifest_sha256'],'Private anchor mismatch')
        require(len(pm['files'])==seal['files'] and len(pm['directories'])==seal['directories'],'Private anchor counts differ')
        result.update(private_verified=True,private_files=len(pm['files']),private_directories=len(pm['directories']))
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__': main()
