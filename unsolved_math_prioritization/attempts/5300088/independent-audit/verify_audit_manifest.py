#!/usr/bin/env python3
"""Verify all files bound by BOUND_MANIFEST.json without modifying either packet."""
import argparse
import hashlib
import json
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent.parent/'submission')
    args=p.parse_args()
    audit=Path(__file__).resolve().parent
    m=json.loads((audit/'BOUND_MANIFEST.json').read_text())
    roots={'author_packet':args.packet.resolve(),'audit_packet':audit}
    counts={}
    for group,root in roots.items():
        entries=m[group]['files']
        names=set(entries)
        if group=='audit_packet': names.add('BOUND_MANIFEST.json')
        if {f.name for f in root.iterdir()}!=names:
            raise SystemExit('Allowlist mismatch: '+group)
        for name,metadata in entries.items():
            if Path(name).name!=name:
                raise SystemExit('Invalid manifest filename')
            f=root/name
            if not f.is_file() or f.is_symlink():
                raise SystemExit('Expected regular file: '+name)
            data=f.read_bytes()
            if len(data)!=metadata['bytes'] or hashlib.sha256(data).hexdigest()!=metadata['sha256']:
                raise SystemExit('Bound file mismatch: '+name)
        counts[group]=len(entries)
    print(json.dumps({'status':'passed','verified_files':counts,'manifest_sha256':hashlib.sha256((audit/'BOUND_MANIFEST.json').read_bytes()).hexdigest()},sort_keys=True))
if __name__=='__main__': main()
