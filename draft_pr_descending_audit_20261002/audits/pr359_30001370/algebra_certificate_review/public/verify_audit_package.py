#!/usr/bin/env python3
"""Read-only sealed public namespace check; private payload check is optional."""
import argparse,hashlib,json,stat
from pathlib import Path

def sha(b):
    return hashlib.sha256(b).hexdigest()

def verify(base,manifest,excluded):
    rows=json.loads(manifest.read_bytes())['files']
    expected={row['path'] for row in rows}
    assert len(expected)==len(rows)
    actual={str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}
    assert actual==expected|set(excluded),(sorted(actual-expected-set(excluded)),sorted(expected-actual))
    for row in rows:
        p=base/row['path']
        assert p.resolve().is_relative_to(base.resolve())
        mode=p.lstat().st_mode
        assert stat.S_ISREG(mode) and stat.S_IMODE(mode)==int(row['mode'],8)
        b=p.read_bytes()
        assert len(b)==row['bytes'] and sha(b)==row['sha256'],row['path']
    return len(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--public-dir',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--private-dir',type=Path)
    a=p.parse_args()
    seal=json.loads((a.public_dir/'FINAL_SEAL.json').read_bytes())
    assert sha((a.public_dir/'PUBLIC_MANIFEST.json').read_bytes())==seal['public_manifest_sha256']
    count=verify(a.public_dir,a.public_dir/'PUBLIC_MANIFEST.json',{'PUBLIC_MANIFEST.json','FINAL_SEAL.json'})
    assert count==seal['public_files']
    private='not_checked: use --private-dir only for locally retained private material'
    if a.private_dir:
        mf=a.private_dir/'PRIVATE_MANIFEST.json'
        assert sha(mf.read_bytes())==seal['private_manifest_sha256']
        private=verify(a.private_dir,mf,{'PRIVATE_MANIFEST.json'})
        assert private==seal['private_files']
    print(json.dumps(dict(status='PASS',sealed_utc=seal['utc'],public_files=count,private_files=private,
                         scope='Immutable namespace, hashes and modes only; no theorem or novelty follows from this checker.'),indent=2,sort_keys=True))

if __name__=='__main__':
    main()
