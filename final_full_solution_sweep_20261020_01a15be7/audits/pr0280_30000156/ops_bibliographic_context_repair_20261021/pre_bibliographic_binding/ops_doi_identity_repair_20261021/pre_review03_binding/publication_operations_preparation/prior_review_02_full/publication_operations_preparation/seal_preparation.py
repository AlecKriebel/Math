#!/usr/bin/env python3
"""Seal or verify all authored PR280 preparation files; no service or Git operations."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
HELPERS=['ops_binding.py','prepublication_check.py','publication_live_gates.py',
         'repository_integration.py','publication_lifecycle.py','record_publication_ledger.py','verify_published_files.py']
EXCLUDED={'MANIFEST.json','MANIFEST.sha256'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def selection():
    paths=[AUDIT/n for n in HELPERS]
    paths += sorted(p for p in HERE.rglob('*') if p.is_file() and p.name not in EXCLUDED
                    and '__pycache__' not in p.parts)
    if any(p.is_symlink() for p in paths):
        raise RuntimeError('Symlink authored evidence is forbidden')
    return sorted(paths)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify',action='store_true')
    args=parser.parse_args()
    path=HERE/'MANIFEST.json'
    seal=HERE/'MANIFEST.sha256'
    if args.verify:
        value=json.loads(path.read_text())
        if seal.read_text().split()[0]!=sha(path.read_bytes()):
            raise RuntimeError('Preparation seal digest differs')
        if {p.relative_to(AUDIT).as_posix() for p in selection()}!={e['path'] for e in value['files']}:
            raise RuntimeError('Authored inventory differs from seal')
        for e in value['files']:
            data=(AUDIT/e['path']).read_bytes()
            if len(data)!=e['bytes'] or sha(data)!=e['sha256']:
                raise RuntimeError('Sealed authored artifact changed: '+e['path'])
        print(json.dumps({'verified':True,'artifacts':len(value['files']),'manifest_sha256':sha(path.read_bytes())}))
        return
    value={'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),'pr':280,
           'scope':'Offline operation preparation only; no scientific clearance or actual publication outcomes asserted.',
           'completion_estimate_percent':100,'files':[{'path':p.relative_to(AUDIT).as_posix(),
               'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in selection()]}
    path.write_text(json.dumps(value,indent=2)+'\n')
    seal.write_text(sha(path.read_bytes())+'  MANIFEST.json\n')
    print(json.dumps({'artifacts':len(value['files']),'manifest_sha256':sha(path.read_bytes())}))


if __name__=='__main__':
    main()
