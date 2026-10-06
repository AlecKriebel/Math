#!/usr/bin/env python3
"""Authenticate the accepted original/corrected/audit byte identities; no theorem certification."""
import argparse, hashlib, json, stat, zipfile
from pathlib import Path
PINS = {'corrected': {'archive': 'STABLE_NORMAL_INVARIANTS_2928_CORRECTED_SAFE.zip', 'bytes': 12239, 'manifest': 'STABLE_NORMAL_INVARIANTS_2928_CORRECTED_EXTERNAL_MANIFEST.json', 'manifest_sha256': '28f2a04bde16dc1a47516707153236be71d3a851d5dd466d1d5b6514ec5a3835', 'sha256': '6eb61d12048125141eedb429845a1bced6c930a660ab17ecebb969b4c2cc7f1d'}, 'original': {'archive': 'STABLE_NORMAL_INVARIANTS_2928_AUTHOR_SAFE_FREEZE.zip', 'bytes': 11695, 'manifest': 'STABLE_NORMAL_INVARIANTS_2928_AUTHOR_EXTERNAL_MANIFEST.json', 'manifest_sha256': '0bfbbeb70269e916439dd96622be2e55e22db141bc9632e1e41675eb05004bc7', 'sha256': '184e4e995b419213860f36e8b250aa56bd606b7fd9e6eb8076726dc94524a2bc'}, 'audit': {'archive': 'STABLE_NORMAL_INVARIANTS_2928_INDEPENDENT_AUDIT_SAFE.zip', 'bytes': 18051, 'sha256': '5272356d6dfb202b53258ab11df6400929566c6c2ca3aefe179d7a290be4391e', 'manifest': 'STABLE_NORMAL_INVARIANTS_2928_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json', 'manifest_bytes': 2056, 'manifest_sha256': '3578038499e97857c3ebc2a4b7ade55b7652619866cf59b9ff101054f7c9a4cb', 'member_count': 11}}
def require(ok, message):
    if not ok: raise ValueError(message)
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--release-directory',type=Path,required=True)
    a=ap.parse_args(); checked=[]
    for label,p in PINS.items():
        z=a.release_directory/p['archive']; m=a.release_directory/p['manifest']
        b=z.read_bytes(); require(len(b)==p['bytes'] and sha(b)==p['sha256'],'archive pin mismatch: '+label)
        require(sha(m.read_bytes())==p['manifest_sha256'],'manifest pin mismatch: '+label)
        mm=json.loads(m.read_text()); require(mm['archive_bytes']==len(b) and mm['archive_sha256']==sha(b),'manifest archive mismatch')
        with zipfile.ZipFile(z) as zz:
            names=zz.namelist(); require(len(names)==len(set(names)),'duplicate members')
            require(set(names)=={x['path'] for x in mm['files']},'member set mismatch')
            for f in mm['files']:
                pp=Path(f['path']); require(not pp.is_absolute() and '..' not in pp.parts,'unsafe path')
                require(stat.S_ISREG(zz.getinfo(f['path']).external_attr>>16),'not regular member')
                bb=zz.read(f['path']); require(len(bb)==f['bytes'] and sha(bb)==f['sha256'],'member mismatch')
        checked.append({'label':label,'members':len(mm['files']),'sha256':sha(b)})
    print(json.dumps({'result':'PASS','problem_id':2928,'disposition':'unsolved','turns_used':3,'checked':checked,'scope':'exact bytes only; no mathematical proof certification'},sort_keys=True))
if __name__=='__main__':main()
