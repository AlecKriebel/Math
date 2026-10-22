#!/usr/bin/env python3
"""Portable externally pinned audit wrapper and exact-result verifier."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

def require(ok,message):
    if not ok:raise RuntimeError(message)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--expected-manifest',required=True)
    a=p.parse_args()
    root=Path(__file__).resolve().parent
    manifest=root/'AUDIT_MANIFEST.json'
    require(manifest.is_file() and not manifest.is_symlink(),'manifest must be a regular file')
    raw=manifest.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==a.expected_manifest,'external audit manifest pin')
    m=json.loads(raw)
    require(set(m)=={'format','files'} and m['format']=='sha256-tree-v1','manifest schema')
    files=m['files']; allowed_dirs=set()
    for name in files:
        pp=PurePosixPath(name)
        require(name==str(pp) and not pp.is_absolute() and '..' not in pp.parts and '\\' not in name and name!='AUDIT_MANIFEST.json','unsafe path')
        allowed_dirs.update(str(v) for v in pp.parents if str(v)!='.')
    actual_files=set();actual_dirs=set()
    for f in root.rglob('*'):
        require(not f.is_symlink(),'symlink prohibited')
        rel=f.relative_to(root).as_posix()
        if f.is_dir():actual_dirs.add(rel)
        else:
            require(f.is_file(),'nonregular payload')
            actual_files.add(rel)
    require(actual_files==set(files)|{'AUDIT_MANIFEST.json'},'file allowlist')
    require(actual_dirs==allowed_dirs,'directory allowlist')
    for name,spec in files.items():
        b=(root/name).read_bytes()
        require(set(spec)=={'bytes','sha256'} and len(b)==spec['bytes'] and hashlib.sha256(b).hexdigest()==spec['sha256'],'payload mismatch: '+name)
    receipt=json.loads((root/'AUTHOR_FREEZE_RECEIPT.json').read_bytes())
    archive=(root/'AUTHOR_SAFE_FREEZE.zip').read_bytes()
    require(len(archive)==receipt['archive_bytes'] and hashlib.sha256(archive).hexdigest()==receipt['archive_sha256'],'frozen archive identity')
    with zipfile.ZipFile(root/'AUTHOR_SAFE_FREEZE.zip') as z:
        names=z.namelist()
        require(len(names)==len(set(names)),'duplicate author archive member')
        require(set(names)=={f.name for f in (root/'author').iterdir()},'archive author file allowlist')
        for name in names:
            require('/' not in name and '\\' not in name and name not in ('.','..'),'unsafe author archive path')
            require(z.read(name)==(root/'author'/name).read_bytes(),'frozen author bytes differ')
    for mode in [[],['-O'],['-OO']]:
        command=[sys.executable,'-B']+mode
        r=subprocess.run(command+[str(root/'author/verify_manifest.py'),'--expected-manifest',receipt['manifest_sha256']],capture_output=True,check=True)
        require(json.loads(r.stdout)['exact_math_replay_matches'],'author exact replay')
        # The author's manifest verifier starts its child without inheriting -O.
        # Invoke its math script directly too so all requested modes are exercised.
        r=subprocess.run(command+[str(root/'author/verify_math.py')],capture_output=True,check=True)
        require(r.stdout==(root/'author/EXPECTED_RESULTS.json').read_bytes(),'author direct optimization-mode replay')
        r=subprocess.run(command+[str(root/'verify_independent_math.py')],capture_output=True,check=True)
        require(r.stdout==(root/'INDEPENDENT_MATH_RESULTS.json').read_bytes(),'independent exact replay')
    audited=(root/'ATTEMPTS_AUDITED.json').read_text()
    require('estimated_target_completion_percent' not in audited,'unsupported completion percentage')
    require(json.loads(audited)['status']=='unsolved','target disposition')
    print(json.dumps({'audit_manifest_matches_external_pin':True,'author_archive_preserved':True,'author_payload_preserved':True,'optimization_modes':['normal','-O','-OO'],'exact_replays_match':True,'target_solved':False},sort_keys=True,indent=2))

if __name__=='__main__':main()
