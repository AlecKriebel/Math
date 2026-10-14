#!/usr/bin/env python3
"""Fail-closed validation of the manifest and the exact public payload file set."""
import hashlib
import json
import stat
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parent

def require(ok,message):
    if not ok:raise RuntimeError(message)

def main():
    entries=list(ROOT.rglob('*'))
    require(all(not p.is_symlink() for p in entries),'Symlink in public payload')
    require(all(stat.S_ISREG(p.stat().st_mode) or stat.S_ISDIR(p.stat().st_mode)
                for p in entries),'Nonregular object in public payload')
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    paths=[]
    for row in manifest['files']:
        rel=row['path'];parts=PurePosixPath(rel)
        require(not parts.is_absolute() and '..' not in parts.parts and str(parts)==rel
                and '\\' not in rel and bool(rel),'Unsafe path')
        p=ROOT/rel
        require(p.is_file() and not p.is_symlink(),'Missing file or symlink: '+rel)
        data=p.read_bytes()
        require(len(data)==row['bytes'],'Wrong byte count: '+rel)
        require(hashlib.sha256(data).hexdigest()==row['sha256'],'Wrong hash: '+rel)
        paths.append(rel)
    require(len(paths)==len(set(paths)),'Duplicate manifest path')
    actual={p.relative_to(ROOT).as_posix() for p in entries if p.is_file()}
    allowed_dirs={str(parent) for rel in paths for parent in PurePosixPath(rel).parents if str(parent)!='.'}
    actual_dirs={p.relative_to(ROOT).as_posix() for p in entries if p.is_dir()}
    require(actual_dirs==allowed_dirs,'Unexpected or missing payload directory')
    require(actual==set(paths)|{'MANIFEST.json'},'Unexpected or unlisted payload files')
    print(json.dumps({'status':'PASS','file_count':len(paths),'all_hashes_and_sizes_match':True,
                      'exact_file_set':True,'manifest_sha256':hashlib.sha256((ROOT/'MANIFEST.json').read_bytes()).hexdigest()},sort_keys=True))

if __name__=='__main__':main()
